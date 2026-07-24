%% data_generate_comsol_v6.m
%% COMSOL 全流程批量数据集生成脚本
%% v6 相对 v5 变更：
%%   ★ 新增楔形域（wedge）求解支持
%%     · domain='wedge' 时用多边形几何替代矩形，切掉楔形斜底以下区域
%%     · 楔形坐标约定（与 models.py / trainer 完全对齐）：
%%         x=0 左顶点（楔尖，退化点，无边界条件）
%%         y=0 上边（Pressure-Release，Dirichlet p=0）    ← 海面
%%         斜边 y = (Ly/Lx)*x（Rigid Boundary，Neumann，自然 BC） ← 海底
%%         右边 x=Lx（Nonreflecting，Robin ABC）
%%     · 楔形角 theta_0 = arctan(Ly/Lx)（与 models.py 中 theta0 计算一致）
%%     · 源点候选节点在楔形内部：y < (Ly/Lx)*x - boundary_margin/sin(theta_0)
%%     · 网格、批次、清单文件命名和下游 Python 流程与矩形域完全对齐
%%
%%   ★ [源点复用] snap 逻辑优化（本版核心改动）
%%     · 原 resolve_collision / resolve_collision_excl 用随机补点处理碰撞 +
%%       候选集外节点，丢失了源点空间位置。
%%     · 改为多近邻贪心唯一映射 snap_knn_unique：每个参考点优先取最近邻，
%%       若该节点不在候选集或已被占用，自动顺延到第 2、3… 近邻，直到找到
%%       「在候选集内且未占用」者。同时解决碰撞与候选集外两个问题，
%%       几何保真度高，且为确定性（不依赖随机种子，结果可复现）。

clearvars -except UT4_OVERRIDE; close all; clc;

%% ============================================================
%%  可调参数
%% ============================================================
Lx               = 128;
Ly               = 128;
c0               = 1500.0;
H_grid           = 1.000;
amp              = 1500.0;
freqs            = [25 50 75 100];
samples_per_freq = 2000;
backup_ratio     = 1.0;
boundary_margin  = 5.0;
ellipse_tol      = 0.1;

use_ellipse      = true;
ellipse_cx       = 96.0;
ellipse_cy       = 32.0;
ellipse_a        = 16.0;
ellipse_b        = 8.0;
ellipse_margin   = boundary_margin;
random_seed      = 32;

%% export_dir 基础根目录（子目录由参数自动生成，见下方步骤）
export_base = fullfile(fileparts(mfilename('fullpath')), 'comsol_dataset_export');

%% domain：指定计算域几何形状，用于路径前缀区分
%% 可选值：'rectangle'（矩形域）| 'wedge'（楔形域）
domain = 'wedge';

%% ---- 楔形域专属参数（仅 domain='wedge' 时生效）----
%% 楔形定义：顶点在坐标原点，x 方向为水平距离，y 方向为深度
%%   海面（上边界）：y = 0，Dirichlet p=0（压力释放）
%%   海底（斜边界）：y = (Ly/Lx)*x，Neumann（刚性，自然边界条件）
%%   两侧开放边界：x=0 及 x=Lx 截断处，Robin/Sommerfeld ABC
%%   楔形角 theta_0 = arctan(Ly/Lx)（自动计算，无需手动设置）
%% 注意：Lx 为水平范围（截面宽度），Ly 为最大水深（斜底底端深度）

%% ---- [功能1] 网格源点复用参数 ----
%% reuse_src_manifest 须包含：all_src_depth, backup_src_depth,
%%   all_freq_indices, backup_freq_idx, selected_frequencies,
%%   samples_per_frequency, Lx_m, Ly_m, H_grid_m
%% ★ 要求：参考 H_grid_m ≥ 当前 H_grid（参考更粗，粗→细 snap 保证唯一性）
reuse_src          = false;
reuse_src_manifest = '';

%% ---- [功能2] 训练/测试分区采样参数 ----
%% 训练池：x ≤ train_max_x AND y ≤ train_max_y
%% 测试池：其余候选节点
%% 备份：训练/测试各自独立从池内剩余节点中无放回抽取
split_train_test = false;
train_max_x      = 96.0;
train_max_y      = 128.0;
train_ratio      = 0.9;   % 训练集比例（默认 9:1）

%% ---- [源点复用] snap 贪心近邻搜索初始 K（碰撞稀疏时 16 绰绰有余）----
snap_K0          = 16;

%% ============================================================
%%  UT4_OVERRIDE
%% ============================================================
if exist('UT4_OVERRIDE', 'var') && isstruct(UT4_OVERRIDE)
    ov = UT4_OVERRIDE;
    flds = {'Lx','Ly','c0','H_grid','amp','freqs','samples_per_freq', ...
            'backup_ratio','boundary_margin','ellipse_tol', ...
            'use_ellipse','ellipse_cx','ellipse_cy','ellipse_a','ellipse_b', ...
            'ellipse_margin','random_seed','export_base','domain', ...
            'reuse_src','reuse_src_manifest', ...
            'split_train_test','train_max_x','train_max_y','train_ratio', ...
            'snap_K0'};
    for fi_ = 1:numel(flds)
        f_ = flds{fi_};
        if isfield(ov, f_); eval(sprintf('%s = ov.%s;', f_, f_)); end
    end
end

%% ============================================================
%%  ★ 自动生成区分性 export_dir 和文件名前缀
%%
%%  目录结构示例（rectangle 域，split_train_test=true）：
%%    comsol_dataset_export/
%%      rectangle_Lx128_Ly128_H1.000_f25_50_75_100_spf2000_split64x64/
%%        comsol_mesh_Lx128_Ly128_H1.000.mat
%%        comsol_batch_Lx128_Ly128_H1.000_f25Hz.mat
%%        comsol_batch_manifest_Lx128_Ly128_H1.000_f25_50_75_100.mat
%%
%%  未分区示例：
%%    comsol_dataset_export/
%%      rectangle_Lx128_Ly128_H1.000_f25_50_75_100_spf2000/
%% ============================================================
freq_tag = strjoin(arrayfun(@(x) num2str(x), sort(freqs), 'UniformOutput',false), '_');

if split_train_test
    split_tag = sprintf('_split%.0fx%.0f', train_max_x, train_max_y);
else
    split_tag = '';
end

%% domain 合法性检查
valid_domains = {'rectangle', 'wedge'};
if ~ismember(domain, valid_domains)
    error('domain 参数非法: "%s"。可选值: rectangle | wedge', domain);
end

dir_name   = sprintf('%s_Lx%d_Ly%d_H%.3f_f%s_spf%d%s', ...
    domain, Lx, Ly, H_grid, freq_tag, samples_per_freq, split_tag);
export_dir = fullfile(export_base, dir_name);

%% 文件名前缀（嵌入物理参数，不含 split——那在目录里体现）
file_prefix = sprintf('Lx%d_Ly%d_H%.3f', Lx, Ly, H_grid);

if ~exist(export_dir, 'dir'); mkdir(export_dir); end

%% ── log 文件（与 export_dir 同级，含时间戳）──────────────────────────
log_filename = sprintf('run_%s_%s.log', dir_name, datestr(now, 'yyyymmdd_HHMMSS'));
log_path     = fullfile(export_dir, log_filename);
diary(log_path);
diary on;
fprintf('[LOG] 日志文件: %s\n', log_path);
fprintf('[LOG] 启动时间: %s\n', datestr(now, 'yyyy-mm-dd HH:MM:SS'));

%% ============================================================
%%  参数合法性预检
%% ============================================================
if reuse_src
    if isempty(reuse_src_manifest) || ~isfile(reuse_src_manifest)
        error('[功能1] reuse_src=true 但 reuse_src_manifest 文件不存在:\n  %s', ...
            reuse_src_manifest);
    end
end
if split_train_test
    if train_ratio <= 0 || train_ratio >= 1
        error('[功能2] train_ratio 须在 (0,1) 内，当前值: %.4f', train_ratio);
    end
    if train_max_x < 0 || train_max_x > Lx
        error('[功能2] train_max_x=%.1f 须在 (0, Lx=%.1f) 内', train_max_x, Lx);
    end
    if train_max_y < 0 || train_max_y > Ly
        error('[功能2] train_max_y=%.1f 须在 (0, Ly=%.1f) 内', train_max_y, Ly);
    end
end

%% ============================================================
%% 初始化 COMSOL
%% ============================================================
addpath('D:\Comsol\COMSOL64\Multiphysics\mli');
import com.comsol.model.* com.comsol.model.util.*
try; mphstart; catch; end

num_freqs       = numel(freqs);
num_samples     = samples_per_freq * num_freqs;
backup_per_freq = round(samples_per_freq * backup_ratio);

if split_train_test
    n_train_per_freq = round(samples_per_freq * train_ratio);
    n_test_per_freq  = samples_per_freq - n_train_per_freq;
    if n_train_per_freq < 1 || n_test_per_freq < 1
        error('[功能2] train_ratio=%.4f 导致训练=%d 或测试=%d 为零，请调整。', ...
            train_ratio, n_train_per_freq, n_test_per_freq);
    end
else
    n_train_per_freq = samples_per_freq;
    n_test_per_freq  = 0;
end

fprintf('\n========================================\n');
fprintf('  COMSOL 批量数据集生成 v6\n');
fprintf('  域形状: %s\n', upper(domain));
fprintf('  域: %d x %d m,  H=%.3f m\n', Lx, Ly, H_grid);
if strcmp(domain, 'wedge')
    fprintf('  楔形角 theta_0 = %.4f rad (%.2f°)\n', ...
        atan2(Ly, Lx), atan2(Ly, Lx)*180/pi);
end
fprintf('  频率: [%s] Hz\n', freq_tag);
fprintf('  每频率样本数: %d,  备份比例: %.0f%%\n', samples_per_freq, backup_ratio*100);
fprintf('  椭圆: cx=%.1f cy=%.1f a=%.1f b=%.1f\n', ellipse_cx, ellipse_cy, ellipse_a, ellipse_b);
if reuse_src
    fprintf('  [功能1] 源点复用: 启用 ← %s\n', reuse_src_manifest);
    fprintf('          snap 贪心近邻初始 K = %d\n', snap_K0);
else
    fprintf('  [功能1] 源点复用: 关闭（新采样）\n');
end
if split_train_test
    fprintf('  [功能2] 训练/测试分区: 启用\n');
    fprintf('          训练池: x≤%.1f AND y≤%.1f\n', train_max_x, train_max_y);
    fprintf('          训练比例: %.0f%%  (每频率 训练=%d / 测试=%d)\n', ...
        train_ratio*100, n_train_per_freq, n_test_per_freq);
else
    fprintf('  [功能2] 训练/测试分区: 关闭\n');
end
fprintf('  输出目录: %s\n', export_dir);
fprintf('========================================\n\n');

%% ============================================================
%% 步骤 1：建立 COMSOL 模型（含网格）
%% ============================================================
fprintf('步骤 1/5: 建立 COMSOL 模型 (%s)...\n', domain);

sp.ex = ellipse_cx; sp.ey = ellipse_cy;
sp.a_hull = ellipse_a; sp.b_hull = ellipse_b;
k_first     = 2*pi*freqs(1)/c0;
p_ref_first = 1i * besselh(0,1,k_first) / 4;

tmp_src = [Lx/2, Ly/4];   % 临时源点，楔形/矩形均安全
if strcmp(domain, 'wedge')
    [model, ph] = build_pde_model_wedge( ...
        Lx, Ly, H_grid, k_first, use_ellipse, sp, tmp_src, p_ref_first);
else
    [model, ph] = build_pde_model_comsol_mesh( ...
        Lx, Ly, H_grid, k_first, use_ellipse, sp, tmp_src, p_ref_first);
end
fprintf('  ✓ 模型建立完成\n');

%% ============================================================
%% 步骤 2：导出 COMSOL 网格
%% ============================================================
fprintf('\n步骤 2/5: 导出 COMSOL 网格...\n');

meshdata = mphmesh(model, 'mesh1');
tri_struct = [];
for i = 1:numel(meshdata)
    if ~iscell(meshdata{i}); continue; end
    for j = 1:numel(meshdata{i})
        s = meshdata{i}{j};
        if isfield(s,'t') && size(s.t,1)==3
            tri_struct = s; break;
        end
    end
    if ~isempty(tri_struct); break; end
end
if isempty(tri_struct)
    error('无法从 mphmesh 提取三角单元。请检查 COMSOL 版本。');
end

p_out  = tri_struct.p;
N_mesh = size(p_out, 2);
t_raw  = tri_struct.t;
if min(t_raw(:)) == 0; t_raw = t_raw + 1; end
t_out   = t_raw;
Ne_mesh = size(t_out, 2);
fprintf('  COMSOL 网格: N=%d 节点, Ne=%d 单元\n', N_mesh, Ne_mesh);

tol_bnd     = H_grid * 2;
bnd_left    = find(abs(p_out(1,:))      <= tol_bnd);
bnd_right   = find(abs(p_out(1,:)-Lx)  <= tol_bnd);
bnd_surface = find(abs(p_out(2,:))      <= tol_bnd);   % y=0 海面（两域均有）

if strcmp(domain, 'wedge')
    %% 楔形：海底是斜边 y = (Ly/Lx)*x，用点到直线距离判断
    slope   = Ly / Lx;   % tan(theta_0)
    %% 直线方程 y - slope*x = 0，即 slope*x - y = 0
    %% 点到直线 ax+by+c=0 距离 = |ax0+by0+c|/sqrt(a^2+b^2)
    a_coef  = slope; b_coef = -1.0; c_coef = 0.0;
    line_norm = sqrt(a_coef^2 + b_coef^2);
    dist_to_seabed = abs(a_coef*p_out(1,:) + b_coef*p_out(2,:) + c_coef) / line_norm;
    bnd_seabed = find(dist_to_seabed <= tol_bnd);
    fprintf('  边界节点: 左=%d 右=%d 海面(y=0)=%d 海底(斜边)=%d\n', ...
        numel(bnd_left), numel(bnd_right), numel(bnd_surface), numel(bnd_seabed));
else
    %% 矩形：海底是水平边 y=Ly
    bnd_seabed  = find(abs(p_out(2,:)-Ly)  <= tol_bnd);
    fprintf('  边界节点: 左=%d 右=%d 海面=%d 海底=%d\n', ...
        numel(bnd_left), numel(bnd_right), numel(bnd_surface), numel(bnd_seabed));
end

%% B_out 编码（行语义固定：0=左，1=右，2=海面，3=海底/斜底，两域通用）
Nmax  = max([numel(bnd_left), numel(bnd_right), numel(bnd_surface), numel(bnd_seabed)]);
B_out = zeros(4, Nmax, 'int32');
B_out(1,1:numel(bnd_left))    = int32(bnd_left);
B_out(2,1:numel(bnd_right))   = int32(bnd_right);
B_out(3,1:numel(bnd_surface)) = int32(bnd_surface);
B_out(4,1:numel(bnd_seabed))  = int32(bnd_seabed);

all_edges        = [t_out(1:2,:), t_out(2:3,:), t_out([3,1],:)];
all_edges_sorted = sort(all_edges, 1);
[~, ia, ic]      = unique(all_edges_sorted.', 'rows');
edge_count        = accumarray(ic, 1);
boundary_edge_idx = ia(edge_count == 1);
e_out             = all_edges(:, boundary_edge_idx);

%% 网格文件名：仅含物理参数（与 split 无关，同域可共用网格）
mesh_filename  = sprintf('comsol_mesh_%s.mat', file_prefix);
mesh_save_path = fullfile(export_dir, mesh_filename);
save(mesh_save_path, 'p_out','t_out','e_out','B_out', ...
    'N_mesh','Ne_mesh','H_grid','Lx','Ly','domain', '-v7.3');
fprintf('  ✓ 网格已保存: %s\n', mesh_save_path);

%% ============================================================
%% 步骤 3：源点采样
%% ============================================================
fprintf('\n步骤 3/5: 源点采样...\n');

all_bnd_set = unique([bnd_left, bnd_right, bnd_surface, bnd_seabed]);
x_nodes = p_out(1,:);
y_nodes = p_out(2,:);

%% margin_ok：矩形包围盒内缩 boundary_margin
margin_ok = (x_nodes >= boundary_margin) & (x_nodes <= Lx - boundary_margin) & ...
            (y_nodes >= boundary_margin);
if strcmp(domain, 'wedge')
    %% 楔形：上界改为斜边内缩距离
    %% 斜边 y = slope*x，法向量 (slope, -1)/norm，沿法向内缩 boundary_margin
    slope_w   = Ly / Lx;
    line_norm_w = sqrt(slope_w^2 + 1);
    margin_ok = margin_ok & ...
        (slope_w * x_nodes - y_nodes > boundary_margin * line_norm_w);
    %% 同时排除在楔形斜边以外（y > slope*x）的节点（几何清理）
    margin_ok = margin_ok & (y_nodes < slope_w * x_nodes);
else
    margin_ok = margin_ok & (y_nodes <= Ly - boundary_margin);
end
ellipse_ok = true(1, N_mesh);
if use_ellipse && ellipse_a > 0 && ellipse_b > 0
    a_ex = ellipse_a + ellipse_margin;
    b_ex = ellipse_b + ellipse_margin;
    dist_sq = ((x_nodes - ellipse_cx)/a_ex).^2 + ...
              ((y_nodes - ellipse_cy)/b_ex).^2;
    ellipse_ok = dist_sq > 1.0;
end
is_bnd = false(1, N_mesh);
is_bnd(all_bnd_set) = true;
candidate_mask  = ~is_bnd & margin_ok & ellipse_ok;
candidate_nodes = find(candidate_mask);
N_candidates    = numel(candidate_nodes);
fprintf('  总节点: %d  |  边界节点: %d  |  有效候选: %d\n', ...
    N_mesh, numel(all_bnd_set), N_candidates);

if reuse_src
    fprintf('\n  ★ [功能1] 启用网格源点复用模式（多近邻贪心唯一映射）\n');
    [all_src_depth, backup_src_depth, all_freq_indices, backup_freq_idx, split_info, ...
     all_src_node_idx, bak_src_node_idx] = ...
        reuse_source_points( ...
            reuse_src_manifest, freqs, samples_per_freq, backup_per_freq, ...
            Lx, Ly, H_grid, p_out, candidate_mask, candidate_nodes, ...
            split_train_test, n_train_per_freq, n_test_per_freq, ...
            train_max_x, train_max_y, snap_K0);
    num_samples = size(all_src_depth, 1);
else
    if split_train_test
        fprintf('\n  ★ [功能2] 启用训练/测试分区采样模式\n');
        [all_src_depth, backup_src_depth, all_freq_indices, backup_freq_idx, split_info, ...
         all_src_node_idx, bak_src_node_idx] = ...
            split_sample_source_points( ...
                freqs, samples_per_freq, backup_per_freq, ...
                p_out, candidate_nodes, N_candidates, ...
                n_train_per_freq, n_test_per_freq, ...
                train_max_x, train_max_y, random_seed);
        num_samples = size(all_src_depth, 1);
    else
        fprintf('  使用原版节点级无放回采样...\n');
        [all_src_depth, backup_src_depth, all_freq_indices, backup_freq_idx, ...
         all_src_node_idx, bak_src_node_idx] = ...
            default_sample_source_points( ...
                freqs, samples_per_freq, backup_per_freq, ...
                p_out, candidate_nodes, N_candidates, random_seed);
        num_samples = size(all_src_depth, 1);
        split_info  = [];
    end
end

fprintf('  ✓ 源点采样完成: %d 主 + %d 备份\n', num_samples, size(backup_src_depth,1));

%% ============================================================
%% 步骤 4：逐频率求解 + mphinterp 顶点提取
%% ============================================================
fprintf('\n步骤 4/5: 逐频率求解 + mphinterp 顶点提取...\n');
t_total = tic;

%% 全局计时数组（每样本耗时，ms）
all_sample_times_ms = zeros(num_samples, 1);   % 全部频率打平存储

for fi = 1:num_freqs
    freq  = freqs(fi);
    k     = 2*pi*freq/c0;
    p_ref = 1i * besselh(0,1,k) / 4;

    fprintf('\n  [%d/%d] %d Hz  k=%.4f  |p_ref|=%.4g\n', ...
        fi, num_freqs, freq, k, abs(p_ref));

    src_idx_start = (fi-1)*samples_per_freq + 1;
    update_freq_coeff(ph, k);

    [minfo, ~] = mphmatrix(model,'sol1','out',{'K'},'initmethod','init');
    K     = sparse(minfo.K);
    N_dof = size(K, 1);
    fprintf('    K: %dx%d\n', N_dof, N_dof);

    U_vertex_batch   = zeros(samples_per_freq, N_mesh);
    sample_times_ms  = zeros(samples_per_freq, 1);   % 本频率每样本耗时（ms）
    t_freq = tic;

    for isrc = 1:samples_per_freq
        t_sample = tic;                              % ← 单样本计时开始
        src_i = all_src_depth(src_idx_start + isrc - 1, :);
        set_gaussian_source_ph(ph, src_i, H_grid, p_ref);
        model.sol('sol1').runAll;
        dsets = model.result.dataset.tags;
        u_v   = double(mphinterp(model,'u','coord',p_out, ...
            'dataset',char(dsets(1))));
        U_vertex_batch(isrc,:)  = u_v(:)';
        sample_times_ms(isrc)   = toc(t_sample) * 1e3;   % ← 单样本计时结束，转 ms

        if mod(isrc,50)==0 || isrc==samples_per_freq
            t_elap = toc(t_freq);
            fprintf('    求解+插值: %d/%d  %.1f src/s  (本样本 %.1f ms)\n', ...
                isrc, samples_per_freq, isrc/t_elap, sample_times_ms(isrc));
        end
    end

    t_freq_total = toc(t_freq);

    %% ── 本频率计时统计 ──────────────────────────────────────────
    t_mean   = mean(sample_times_ms);
    t_median = median(sample_times_ms);
    t_std    = std(sample_times_ms);
    t_min    = min(sample_times_ms);
    t_max    = max(sample_times_ms);
    t_p95    = prctile(sample_times_ms, 95);

    fprintf('    本频率耗时: %.0f s (%.0f min)\n', t_freq_total, t_freq_total/60);
    fprintf('    ┌──────────────────────────────────────────┐\n');
    fprintf('    │  %d Hz 每样本求解时间统计（ms）           │\n', freq);
    fprintf('    ├──────────────────────────────────────────┤\n');
    fprintf('    │  样本数 : %6d                          │\n', samples_per_freq);
    fprintf('    │  均值   : %8.1f ms                    │\n', t_mean);
    fprintf('    │  中位数 : %8.1f ms                    │\n', t_median);
    fprintf('    │  标准差 : %8.1f ms                    │\n', t_std);
    fprintf('    │  最小值 : %8.1f ms                    │\n', t_min);
    fprintf('    │  最大值 : %8.1f ms                    │\n', t_max);
    fprintf('    │  P95    : %8.1f ms                    │\n', t_p95);
    fprintf('    │  吞吐量 : %8.2f samples/s             │\n', samples_per_freq/t_freq_total);
    fprintf('    └──────────────────────────────────────────┘\n');

    %% 写入全局数组
    g_start = (fi-1)*samples_per_freq + 1;
    g_end   = fi*samples_per_freq;
    all_sample_times_ms(g_start:g_end) = sample_times_ms;

    [K_i, K_j, K_v] = find(K);
    K_i0    = int64(K_i(:)-1);
    K_j0    = int64(K_j(:)-1);
    K_data  = K_v(:);
    K_shape = int64([N_dof, N_dof]);

    src_depth_fi  = all_src_depth(src_idx_start:src_idx_start+samples_per_freq-1,:);
    freq_idx_fi   = all_freq_indices(src_idx_start:src_idx_start+samples_per_freq-1);
    %% 节点索引（1-based，Python 读后 -1 转 0-based，无需再 snap）
    src_node_idx_fi = int32(all_src_node_idx(src_idx_start:src_idx_start+samples_per_freq-1));
    wavenumber    = k; frequency = freq; p_ref_val = p_ref;
    Lx_export     = Lx; Ly_export = Ly; H_grid_export = H_grid;
    N_dof_export  = int64(N_dof);
    N_mesh_export = int64(N_mesh);
    split_info_fi = [];
    if ~isempty(split_info); split_info_fi = split_info(fi); end

    %% 每频率输出文件名：含物理参数 + 频率
    batch_filename = sprintf('comsol_batch_%s_f%dHz.mat', file_prefix, freq);
    out_mat = fullfile(export_dir, batch_filename);
    save(out_mat, ...
        'K_i0','K_j0','K_data','K_shape', ...
        'U_vertex_batch', ...
        'src_depth_fi','freq_idx_fi','src_node_idx_fi', ...
        'frequency','wavenumber','p_ref_val', ...
        'Lx_export','Ly_export','H_grid_export', ...
        'N_dof_export','N_mesh_export', ...
        'split_info_fi', '-v7.3');
    fprintf('    ✓ 已保存: %s\n', out_mat);
end

try; ModelUtil.remove(model.tag); catch; end

%% ── 全局计时汇总（所有频率合并）────────────────────────────────
t_all_mean   = mean(all_sample_times_ms);
t_all_median = median(all_sample_times_ms);
t_all_std    = std(all_sample_times_ms);
t_all_min    = min(all_sample_times_ms);
t_all_max    = max(all_sample_times_ms);
t_all_p95    = prctile(all_sample_times_ms, 95);
t_all_total  = sum(all_sample_times_ms) / 1e3;   % 求解总耗时（秒）

fprintf('\n');
fprintf('  ╔══════════════════════════════════════════════╗\n');
fprintf('  ║    全局每样本求解时间统计（所有频率合并）    ║\n');
fprintf('  ╠══════════════════════════════════════════════╣\n');
fprintf('  ║  总样本数 : %6d                          ║\n', num_samples);
fprintf('  ║  均值     : %8.1f ms                    ║\n', t_all_mean);
fprintf('  ║  中位数   : %8.1f ms                    ║\n', t_all_median);
fprintf('  ║  标准差   : %8.1f ms                    ║\n', t_all_std);
fprintf('  ║  最小值   : %8.1f ms                    ║\n', t_all_min);
fprintf('  ║  最大值   : %8.1f ms                    ║\n', t_all_max);
fprintf('  ║  P95      : %8.1f ms                    ║\n', t_all_p95);
fprintf('  ║  求解总计 : %8.1f s (%.1f min)         ║\n', t_all_total, t_all_total/60);
fprintf('  ║  平均吞吐 : %8.2f samples/s             ║\n', num_samples/t_all_total);
fprintf('  ╚══════════════════════════════════════════════╝\n');

%% ============================================================
%% 步骤 5：保存全局清单
%% ============================================================
fprintf('\n步骤 5/5: 保存清单...\n');

selected_frequencies  = freqs;
samples_per_frequency = samples_per_freq;
Lx_m=Lx; Ly_m=Ly; H_grid_m=H_grid; c0_m=c0; amp_m=amp;
use_ellipse_m=use_ellipse;
ellipse_cx_m=ellipse_cx; ellipse_cy_m=ellipse_cy;
ellipse_a_m=ellipse_a; ellipse_b_m=ellipse_b;
ellipse_tol_m=ellipse_tol; ellipse_margin_m=ellipse_margin;
boundary_margin_m=boundary_margin;
random_seed_m=random_seed; backup_ratio_m=backup_ratio;
N_mesh_m = int64(N_mesh);
total_export_time_s = toc(t_total);
reuse_src_m = reuse_src; reuse_src_manifest_m = reuse_src_manifest;
split_train_test_m = split_train_test;
train_max_x_m=train_max_x; train_max_y_m=train_max_y;
train_ratio_m=train_ratio;
domain_m = domain;
snap_K0_m = snap_K0;

%% manifest 文件名：含物理参数 + 频率列表（区分不同频率组合）
%% 求解计时统计
timing_stats_m = struct(...
    'all_sample_times_ms', all_sample_times_ms, ...
    'mean_ms',   t_all_mean,   ...
    'median_ms', t_all_median, ...
    'std_ms',    t_all_std,    ...
    'min_ms',    t_all_min,    ...
    'max_ms',    t_all_max,    ...
    'p95_ms',    t_all_p95,    ...
    'total_solve_s', t_all_total, ...
    'throughput_samples_per_s', num_samples/t_all_total);

manifest_filename = sprintf('comsol_batch_manifest_%s_f%s.mat', ...
    file_prefix, freq_tag);
manifest_path = fullfile(export_dir, manifest_filename);
save(manifest_path, ...
    'selected_frequencies','samples_per_frequency', ...
    'all_src_depth','backup_src_depth', ...
    'all_freq_indices','backup_freq_idx', ...
    'all_src_node_idx','bak_src_node_idx', ...
    'split_info', ...
    'N_mesh_m', ...
    'Lx_m','Ly_m','H_grid_m','c0_m','amp_m', ...
    'use_ellipse_m','ellipse_cx_m','ellipse_cy_m', ...
    'ellipse_a_m','ellipse_b_m', ...
    'ellipse_tol_m','ellipse_margin_m','boundary_margin_m', ...
    'random_seed_m','backup_ratio_m','total_export_time_s', ...
    'reuse_src_m','reuse_src_manifest_m', ...
    'split_train_test_m','train_max_x_m','train_max_y_m','train_ratio_m', ...
    'domain_m', 'snap_K0_m', ...
    'timing_stats_m', ...
    '-v7.3');

fprintf('  ✓ 清单已保存: %s\n', manifest_path);
fprintf('  建模+导出总耗时: %.1f s (%.1f min)\n', ...
    total_export_time_s, total_export_time_s/60);

%% 打印建议的 Python 调用命令
fprintf('\n✓ MATLAB 导出完毕，建议运行：\n');
fprintf('  python Ocean_Dataset_barrier_comsol.py \\\n');
fprintf('      --matlab_dir  "%s" \\\n', export_dir);
fprintf('      --mat_dir     "%s" \\\n', export_dir);
fprintf('      --mesh_file   "%s" \\\n', mesh_filename);
fprintf('      --manifest    "%s" \\\n', manifest_filename);
fprintf('      --grid_x %d --grid_y %d --H %.3f \\\n', Lx, Ly, H_grid);
fprintf('      --domain %s \\\n', domain);
fprintf('      --frequencies %s \\\n', num2str(freqs));
fprintf('      --samples_per_freq %d \\\n', samples_per_freq);
if split_train_test
    fprintf('      --split_train_test \\\n');
    fprintf('      --train_max_x %.1f --train_max_y %.1f\n', train_max_x, train_max_y);
else
    fprintf('      # (无 split_train_test)\n');
end


fprintf('[LOG] 结束时间: %s\n', datestr(now, 'yyyy-mm-dd HH:MM:SS'));
diary off;
fprintf('日志已保存: %s\n', log_path);

%% ============================================================
%%  局部辅助函数
%% ============================================================

%% ------------------------------------------------------------------
%% default_sample_source_points（无分区、无复用的原版逻辑）
%%
%% 防碰撞机制：
%%   · 每频率一次 randperm(N_candidates, spf+bak)，无放回，主+备互斥
%%   · 不同频率可复用相同节点（与原版语义一致）
%%   · 两重 assert 确认唯一性
%% ------------------------------------------------------------------
function [all_src, bak_src, all_fi, bak_fi, all_node_idx, bak_node_idx] = ...
        default_sample_source_points( ...
            freqs, samples_per_freq, backup_per_freq, ...
            p_out, candidate_nodes, N_candidates, random_seed)

    num_freqs = numel(freqs);
    all_src      = zeros(samples_per_freq * num_freqs, 2);
    all_fi       = zeros(samples_per_freq * num_freqs, 1, 'int32');
    all_node_idx = zeros(samples_per_freq * num_freqs, 1, 'int32');
    bak_src      = zeros(backup_per_freq  * num_freqs, 2);
    bak_fi       = zeros(backup_per_freq  * num_freqs, 1, 'int32');
    bak_node_idx = zeros(backup_per_freq  * num_freqs, 1, 'int32');

    n_draw = samples_per_freq + backup_per_freq;
    if N_candidates < n_draw
        error('候选节点 %d < 每频率所需 %d（主%d+备%d）', ...
            N_candidates, n_draw, samples_per_freq, backup_per_freq);
    end

    for fi = 1:num_freqs
        rng(random_seed + (fi-1), 'twister');
        perm      = randperm(N_candidates, n_draw);
        drawn_idx = candidate_nodes(perm);   % 1-based 网格节点索引，无放回

        row_s = (fi-1)*samples_per_freq + 1;
        row_e = fi*samples_per_freq;
        main_nodes = drawn_idx(1:samples_per_freq);
        bak_nodes  = drawn_idx(samples_per_freq+1:end);

        all_src(row_s:row_e, :)  = p_out(:, main_nodes)';
        all_fi(row_s:row_e)      = int32(fi-1);
        all_node_idx(row_s:row_e)= int32(main_nodes(:));

        bk_s = (fi-1)*backup_per_freq + 1;
        bk_e = fi*backup_per_freq;
        bak_src(bk_s:bk_e, :)  = p_out(:, bak_nodes)';
        bak_fi(bk_s:bk_e)      = int32(fi-1);
        bak_node_idx(bk_s:bk_e)= int32(bak_nodes(:));

        assert(numel(unique(main_nodes)) == samples_per_freq, ...
            '[default] %d Hz 主样本节点不唯一', freqs(fi));
        assert(numel(unique(bak_nodes)) == backup_per_freq, ...
            '[default] %d Hz 备份节点不唯一', freqs(fi));
        assert(isempty(intersect(main_nodes, bak_nodes)), ...
            '[default] %d Hz 主/备节点存在交集', freqs(fi));

        fprintf('  [%d/%d] %d Hz: 主 %d | 备份 %d（主/备互斥✓）\n', ...
            fi, num_freqs, freqs(fi), samples_per_freq, backup_per_freq);
    end
end


%% ------------------------------------------------------------------
%% split_sample_source_points（[功能2] 训练/测试分区采样）
%%
%% 防碰撞机制（v4 加固）：
%%   · 训练池 = candidate_nodes 中 x≤train_max_x AND y≤train_max_y 的子集
%%   · 测试池 = 其余候选节点
%%   · 训练主样本：从训练池无放回抽 n_train
%%   · 训练备份：  从训练池剩余（已去掉训练主样本）无放回抽 backup_per_freq
%%   · 测试主样本：从测试池无放回抽 n_test
%%   · 测试备份：  从测试池剩余（已去掉测试主样本）无放回抽 backup_per_freq
%%   → 任意两组之间均无公共节点
%%   · 3 重 assert 验证：训练内唯一、测试内唯一、训练∩测试=∅
%% ------------------------------------------------------------------
function [all_src, bak_src, all_fi, bak_fi, split_info, all_node_idx, bak_node_idx] = ...
        split_sample_source_points( ...
            freqs, samples_per_freq, backup_per_freq, ...
            p_out, candidate_nodes, N_candidates, ...
            n_train_per_freq, n_test_per_freq, ...
            train_max_x, train_max_y, random_seed)

    num_freqs = numel(freqs);

    %% 池划分
    x_cand = p_out(1, candidate_nodes);
    y_cand = p_out(2, candidate_nodes);
    in_train_zone = (x_cand <= train_max_x) & (y_cand <= train_max_y);

    train_pool = candidate_nodes(in_train_zone);
    test_pool  = candidate_nodes(~in_train_zone);
    N_train_pool = numel(train_pool);
    N_test_pool  = numel(test_pool);

    need_train = n_train_per_freq + backup_per_freq;
    need_test  = n_test_per_freq  + backup_per_freq;

    fprintf('\n  ┌─────────────────────────────────────────────────────────┐\n');
    fprintf('  │  [功能2] 训练/测试分区节点配额检查                     │\n');
    fprintf('  ├─────────────────────────────────────────────────────────┤\n');
    fprintf('  │  训练区 (x≤%.1f AND y≤%.1f)\n', train_max_x, train_max_y);
    fprintf('  │    可用节点: %7d\n', N_train_pool);
    fprintf('  │    每频率需: %7d (主 %d + 备 %d)\n', need_train, n_train_per_freq, backup_per_freq);
    fprintf('  │    总需 (×%d 频率): %d\n', num_freqs, need_train*num_freqs);
    fprintf('  │    注：不同频率可共用同一节点（池不跨频重置）\n');
    fprintf('  │  测试区 (其余)\n');
    fprintf('  │    可用节点: %7d\n', N_test_pool);
    fprintf('  │    每频率需: %7d (主 %d + 备 %d)\n', need_test, n_test_per_freq, backup_per_freq);
    fprintf('  └─────────────────────────────────────────────────────────┘\n');

    if N_train_pool < need_train
        error(['[功能2] 训练池节点不足: 可用 %d < 单频率需要 %d (主%d+备%d)\n' ...
               '  建议：增大 train_max_x/y，减小 train_ratio 或 samples_per_freq。'], ...
            N_train_pool, need_train, n_train_per_freq, backup_per_freq);
    end
    if N_test_pool < need_test
        error(['[功能2] 测试池节点不足: 可用 %d < 单频率需要 %d (主%d+备%d)\n' ...
               '  建议：减小 train_max_x/y，增大 train_ratio 或减小 samples_per_freq。'], ...
            N_test_pool, need_test, n_test_per_freq, backup_per_freq);
    end
    fprintf('  ✓ 配额充足: 训练池余量 %d，测试池余量 %d\n', ...
        N_train_pool - need_train, N_test_pool - need_test);

    %% 输出分配
    all_src      = zeros(samples_per_freq * num_freqs, 2);
    all_fi       = zeros(samples_per_freq * num_freqs, 1, 'int32');
    all_node_idx = zeros(samples_per_freq * num_freqs, 1, 'int32');
    bak_src      = zeros(2 * backup_per_freq * num_freqs, 2);
    bak_fi       = zeros(2 * backup_per_freq * num_freqs, 1, 'int32');
    bak_node_idx = zeros(2 * backup_per_freq * num_freqs, 1, 'int32');
    split_info = repmat(struct( ...
        'freq',0,'freq_idx',0, ...
        'train_start',0,'n_train',0, ...
        'test_start',0,'n_test',0, ...
        'bak_train_start',0,'n_bak_train',0, ...
        'bak_test_start',0,'n_bak_test',0), 1, num_freqs);

    for fi = 1:num_freqs
        rng(random_seed + (fi-1), 'twister');
        perm_tr    = randperm(N_train_pool, n_train_per_freq + backup_per_freq);
        main_train = train_pool(perm_tr(1:n_train_per_freq));
        bak_train  = train_pool(perm_tr(n_train_per_freq+1:end));

        rng(random_seed + num_freqs + (fi-1), 'twister');
        perm_te   = randperm(N_test_pool, n_test_per_freq + backup_per_freq);
        main_test = test_pool(perm_te(1:n_test_per_freq));
        bak_test  = test_pool(perm_te(n_test_per_freq+1:end));

        assert(numel(unique(main_train)) == n_train_per_freq, '[功能2] %d Hz 训练主节点不唯一', freqs(fi));
        assert(numel(unique(bak_train))  == backup_per_freq,  '[功能2] %d Hz 训练备节点不唯一', freqs(fi));
        assert(numel(unique(main_test))  == n_test_per_freq,  '[功能2] %d Hz 测试主节点不唯一', freqs(fi));
        assert(numel(unique(bak_test))   == backup_per_freq,  '[功能2] %d Hz 测试备节点不唯一', freqs(fi));
        assert(isempty(intersect(main_train, bak_train)),     '[功能2] %d Hz 训练主/备交集非空', freqs(fi));
        assert(isempty(intersect(main_test,  bak_test)),      '[功能2] %d Hz 测试主/备交集非空', freqs(fi));
        assert(isempty(intersect(main_train, main_test)),     '[功能2] %d Hz 训练/测试主样本交集非空', freqs(fi));

        row_s  = (fi-1)*samples_per_freq + 1;
        tr_end = row_s + n_train_per_freq - 1;
        te_end = tr_end + n_test_per_freq;

        all_src(row_s:tr_end,   :) = p_out(:, main_train)';
        all_src(tr_end+1:te_end,:) = p_out(:, main_test)';
        all_fi(row_s:te_end)       = int32(fi-1);
        all_node_idx(row_s:tr_end)    = int32(main_train(:));
        all_node_idx(tr_end+1:te_end) = int32(main_test(:));

        bk_base  = (fi-1)*2*backup_per_freq;
        bk_tr_s  = bk_base + 1;
        bk_tr_e  = bk_base + backup_per_freq;
        bk_te_s  = bk_tr_e + 1;
        bk_te_e  = bk_base + 2*backup_per_freq;

        bak_src(bk_tr_s:bk_tr_e, :) = p_out(:, bak_train)';
        bak_src(bk_te_s:bk_te_e, :) = p_out(:, bak_test)';
        bak_fi(bk_tr_s:bk_tr_e)     = int32(fi-1);
        bak_fi(bk_te_s:bk_te_e)     = int32(fi-1);
        bak_node_idx(bk_tr_s:bk_tr_e) = int32(bak_train(:));
        bak_node_idx(bk_te_s:bk_te_e) = int32(bak_test(:));

        split_info(fi).freq            = freqs(fi);
        split_info(fi).freq_idx        = fi-1;
        split_info(fi).train_start     = row_s - 1;
        split_info(fi).n_train         = n_train_per_freq;
        split_info(fi).test_start      = tr_end;
        split_info(fi).n_test          = n_test_per_freq;
        split_info(fi).bak_train_start = bk_tr_s - 1;
        split_info(fi).n_bak_train     = backup_per_freq;
        split_info(fi).bak_test_start  = bk_te_s - 1;
        split_info(fi).n_bak_test      = backup_per_freq;

        fprintf('  [%d/%d] %d Hz: 训练主=%d 训练备=%d | 测试主=%d 测试备=%d（全部互斥✓）\n', ...
            fi, num_freqs, freqs(fi), n_train_per_freq, backup_per_freq, n_test_per_freq, backup_per_freq);
    end
    fprintf('  ✓ 分区采样完成\n');
end


%% ------------------------------------------------------------------
%% reuse_source_points（[功能1] 从粗网格 manifest 复用源点）
%%
%% snap 策略（本版优化核心）：
%%   · 多近邻贪心唯一映射 snap_knn_unique 取代原随机补点：
%%     每个参考点优先取最近邻；若该节点不在候选集或已被占用，
%%     自动顺延到第 2、3… 近邻，直到找到「在候选集内且未占用」者。
%%   · 同时解决「碰撞」与「候选集外」两个问题，几何保真度高。
%%   · 确定性：不依赖随机种子，同一参考 manifest 每次结果一致。
%%   · used_mask 每频率重置 → 不同频率可复用同一节点（与原语义一致），
%%     但同频率内主样本与备份互斥（备份继承主样本的 used_mask）。
%% ------------------------------------------------------------------
function [all_src, bak_src, all_fi, bak_fi, split_info, all_node_idx, bak_node_idx] = ...
        reuse_source_points( ...
            manifest_path, freqs, samples_per_freq, backup_per_freq, ...
            Lx, Ly, H_grid, p_out, candidate_mask, candidate_nodes, ...
            split_train_test, n_train_per_freq, n_test_per_freq, ...
            train_max_x, train_max_y, snap_K0)

    fprintf('    载入参考 manifest: %s\n', manifest_path);
    ref = load(manifest_path, ...
        'all_src_depth','backup_src_depth', ...
        'all_freq_indices','backup_freq_idx', ...
        'selected_frequencies','samples_per_frequency', ...
        'Lx_m','Ly_m','H_grid_m');

    %% 验证1：域尺寸
    if abs(ref.Lx_m - Lx) > 1e-6 || abs(ref.Ly_m - Ly) > 1e-6
        error('[功能1] 域尺寸不一致: 参考 Lx=%.1f Ly=%.1f vs 当前 Lx=%.1f Ly=%.1f', ...
            ref.Lx_m, ref.Ly_m, Lx, Ly);
    end
    fprintf('    ✓ 域尺寸一致: Lx=%d Ly=%d\n', Lx, Ly);

    %% 验证2：分辨率方向（H_ref ≥ H_grid，粗→细 snap）
    H_ref = double(ref.H_grid_m);
    if H_ref < H_grid - 1e-9
        error(['[功能1] 分辨率校验失败:\n' ...
               '  参考 H=%.4f < 当前 H=%.4f（参考更细，细→粗 snap 易碰撞）\n' ...
               '  需提供 H_ref ≥ %.4f 的 manifest，或将当前 H_grid 减小。'], ...
            H_ref, H_grid, H_grid);
    end
    fprintf('    ✓ 分辨率校验通过: 参考 H=%.4f ≥ 当前 H=%.4f（粗→细 snap）\n', ...
        H_ref, H_grid);

    %% 验证3：频率兼容
    ref_freqs = ref.selected_frequencies(:)';
    cur_freqs = freqs(:)';
    missing   = setdiff(cur_freqs, ref_freqs);
    if ~isempty(missing)
        error('[功能1] 参考 manifest 缺少频率: %s Hz', mat2str(missing));
    end
    fprintf('    ✓ 频率兼容: %s Hz\n', mat2str(cur_freqs));

    %% 验证4：样本数
    ref_spf = ref.samples_per_frequency;
    if ref_spf < samples_per_freq
        error('[功能1] 参考每频率样本数 %d < 需求 %d', ref_spf, samples_per_freq);
    end
    ref_bak = size(ref.backup_src_depth,1) / numel(ref_freqs);
    if ref_bak < backup_per_freq
        error('[功能1] 参考备份每频率 %d < 需求 %d', round(ref_bak), backup_per_freq);
    end
    fprintf('    ✓ 样本数兼容: 参考 %d ≥ 需求 %d\n', ref_spf, samples_per_freq);

    %% 构建 KD-Tree（当前细网格，[N,2]）
    fprintf('    构建 KD-Tree (N=%d)...\n', size(p_out,2));
    kd_pts = p_out';   % [N, 2]
    N_all  = size(p_out, 2);

    num_freqs_cur = numel(freqs);
    all_src      = zeros(samples_per_freq * num_freqs_cur, 2);
    all_fi       = zeros(samples_per_freq * num_freqs_cur, 1, 'int32');
    all_node_idx = zeros(samples_per_freq * num_freqs_cur, 1, 'int32');
    bak_src      = zeros(backup_per_freq  * num_freqs_cur, 2);
    bak_fi       = zeros(backup_per_freq  * num_freqs_cur, 1, 'int32');
    bak_node_idx = zeros(backup_per_freq  * num_freqs_cur, 1, 'int32');
    split_info = [];

    for fi = 1:num_freqs_cur
        freq_cur      = freqs(fi);
        ref_fi_idx    = find(ref_freqs == freq_cur) - 1;   % 0-based
        freq_mask_ref = (ref.all_freq_indices == ref_fi_idx);
        freq_mask_bak = (ref.backup_freq_idx  == ref_fi_idx);

        ref_src_fi = ref.all_src_depth(freq_mask_ref, :);
        ref_bak_fi = ref.backup_src_depth(freq_mask_bak, :);
        ref_src_fi = ref_src_fi(1:samples_per_freq, :);
        ref_bak_fi = ref_bak_fi(1:backup_per_freq,  :);

        %% ── 多近邻贪心唯一映射（次/三…佳回退）──────────────────
        %% used_mask 每频率重置：跨频率允许复用同一节点（与原语义一致）
        used_mask = false(1, N_all);   % 本频率占用表

        [snap_idx_main, st_main] = snap_knn_unique( ...
            ref_src_fi, kd_pts, candidate_mask, used_mask, snap_K0, freq_cur, '主样本');
        used_mask = st_main.used_mask;     % 主样本占用 → 传给备份，保证互斥

        [snap_idx_bak,  st_bak]  = snap_knn_unique( ...
            ref_bak_fi, kd_pts, candidate_mask, used_mask, snap_K0, freq_cur, '备份');

        %% 报告最终选中节点 vs 参考点的实际误差 + 回退统计
        d_main = vecnorm(p_out(:, snap_idx_main)' - ref_src_fi, 2, 2);
        d_bak  = vecnorm(p_out(:, snap_idx_bak)'  - ref_bak_fi, 2, 2);
        fprintf('    [%d Hz] 主: snap误差 max=%.4f mean=%.4f m | 回退 %d/%d 个(最远第%d近邻)\n', ...
            freq_cur, max(d_main), mean(d_main), st_main.n_bumped, samples_per_freq, st_main.max_rank);
        fprintf('    [%d Hz] 备: snap误差 max=%.4f mean=%.4f m | 回退 %d/%d 个(最远第%d近邻)\n', ...
            freq_cur, max(d_bak),  mean(d_bak),  st_bak.n_bumped,  backup_per_freq,  st_bak.max_rank);

        %% 唯一性 / 候选集 / 主备互斥 验证
        assert(numel(unique(snap_idx_main)) == samples_per_freq, ...
            '[功能1] %d Hz 主样本不唯一', freq_cur);
        assert(numel(unique(snap_idx_bak))  == backup_per_freq, ...
            '[功能1] %d Hz 备份不唯一',   freq_cur);
        assert(isempty(intersect(snap_idx_main, snap_idx_bak)), ...
            '[功能1] %d Hz 主/备重叠',     freq_cur);
        assert(all(candidate_mask(snap_idx_main)) && all(candidate_mask(snap_idx_bak)), ...
            '[功能1] %d Hz 存在候选集外节点', freq_cur);

        %% 写入
        row_s = (fi-1)*samples_per_freq + 1;
        row_e = fi*samples_per_freq;
        all_src(row_s:row_e, :)   = p_out(:, snap_idx_main)';
        all_fi(row_s:row_e)       = int32(fi-1);
        all_node_idx(row_s:row_e) = int32(snap_idx_main(:));

        bk_s = (fi-1)*backup_per_freq + 1;
        bk_e = fi*backup_per_freq;
        bak_src(bk_s:bk_e, :)   = p_out(:, snap_idx_bak)';
        bak_fi(bk_s:bk_e)       = int32(fi-1);
        bak_node_idx(bk_s:bk_e) = int32(snap_idx_bak(:));

        %% [功能1+2 联合] 生成 split_info（按 snap 后坐标判断区域归属）
        if split_train_test
            si = build_split_info_from_coords( ...
                all_src(row_s:row_e,:), fi, freq_cur, ...
                n_train_per_freq, n_test_per_freq, ...
                train_max_x, train_max_y, row_s, ...
                bk_s, backup_per_freq);
            split_info = [split_info, si]; %#ok<AGROW>
        end
    end
    fprintf('    ✓ 源点复用完成（多近邻贪心唯一映射）\n');
end


%% ------------------------------------------------------------------
%% snap_knn_unique
%%   多近邻贪心唯一映射：每个参考点优先取最近邻；若该节点不在候选集
%%   或已被占用，自动顺延到第 2、3… 近邻，直到找到合法节点。
%%   used_mask 进出（便于把主样本占用传给备份）。
%%
%%   输入：
%%     ref_pts        [M,2] 参考点坐标
%%     kd_pts         [N,2] 当前细网格全部节点坐标
%%     candidate_mask [1,N] logical，true=候选集内（允许）节点
%%     used_mask      [1,N] logical，true=已被占用（不可再选）
%%     K0             初始近邻数（碰撞稀疏时 16 足够；耗尽则自动扩大）
%%     freq, label    仅用于报错/统计文案
%%
%%   输出：
%%     idx_out [M,1] 唯一节点索引（全部在候选集内且互不重复、不与 used 冲突）
%%     stats.n_bumped  退出最近邻（用了第≥2近邻）的点数
%%     stats.max_rank  实际用到的最大近邻序号
%%     stats.used_mask 更新后的占用表
%% ------------------------------------------------------------------
function [idx_out, stats] = snap_knn_unique( ...
        ref_pts, kd_pts, candidate_mask, used_mask, K0, freq, label)
    M = size(ref_pts, 1);
    idx_out = zeros(M, 1);
    K0 = min(K0, size(kd_pts, 1));
    [nn_idx, ~] = knnsearch(kd_pts, ref_pts, 'K', K0);

    rank_used = ones(M, 1);   % 每点最终用了第几近邻
    n_bumped  = 0;            % 退出最近邻的点数

    for m = 1:M
        placed = false;
        for r = 1:K0
            c = nn_idx(m, r);
            if candidate_mask(c) && ~used_mask(c)
                idx_out(m)   = c;
                used_mask(c) = true;
                rank_used(m) = r;
                if r > 1; n_bumped = n_bumped + 1; end
                placed = true; break;
            end
        end
        if ~placed
            %% K0 个近邻全占用/越界，逐步扩大单点搜索
            [c, r_eff] = expand_search( ...
                ref_pts(m,:), kd_pts, candidate_mask, used_mask, K0, freq, label);
            idx_out(m)    = c;
            used_mask(c)  = true;
            rank_used(m)  = r_eff;
            n_bumped      = n_bumped + 1;
        end
    end
    stats.n_bumped  = n_bumped;
    stats.max_rank  = max(rank_used);
    stats.used_mask = used_mask;
end


%% ------------------------------------------------------------------
%% expand_search
%%   单点 K 耗尽时的兜底：指数扩大 K，直至找到「候选集内且未占用」节点。
%%   返回节点索引及其在扩展近邻列表中的序号（用于 max_rank 统计）。
%% ------------------------------------------------------------------
function [node, r_eff] = expand_search( ...
        pt, kd_pts, candidate_mask, used_mask, K_start, freq, label)
    Nmax = size(kd_pts, 1);
    K = K_start;
    while K < Nmax
        K = min(K * 4, Nmax);
        nn = knnsearch(kd_pts, pt, 'K', K);
        for r = 1:numel(nn)
            c = nn(r);
            if candidate_mask(c) && ~used_mask(c)
                node = c; r_eff = r; return;
            end
        end
    end
    error('[功能1] %d Hz %s: 全网格已无可用候选节点（已耗尽）', freq, label);
end


%% ------------------------------------------------------------------
%% build_split_info_from_coords（功能1+2 联合时辅助）
%% ------------------------------------------------------------------
function si = build_split_info_from_coords( ...
        src_coords, fi, freq_cur, ...
        n_train_per_freq, n_test_per_freq, ...
        train_max_x, train_max_y, row_s_global, ...
        bak_start_global, backup_per_freq)

    in_train    = (src_coords(:,1) <= train_max_x) & ...
                  (src_coords(:,2) <= train_max_y);
    actual_train = sum(in_train);
    actual_test  = sum(~in_train);

    if actual_train < n_train_per_freq
        warning(['[功能1+2] %d Hz: snap 后训练区源点 %d < 需求 %d，' ...
                 '参考 manifest 布局与训练区不完全兼容。'], ...
            freq_cur, actual_train, n_train_per_freq);
    end

    si.freq            = freq_cur;
    si.freq_idx        = fi - 1;
    si.train_start     = row_s_global - 1;
    si.n_train         = actual_train;
    si.test_start      = row_s_global - 1 + actual_train;
    si.n_test          = actual_test;
    si.bak_train_start = bak_start_global - 1;
    si.n_bak_train     = backup_per_freq;
    si.bak_test_start  = bak_start_global - 1 + backup_per_freq;
    si.n_bak_test      = backup_per_freq;

    fprintf('    [功能1+2] %d Hz: 坐标划分 → 训练区 %d / 测试区 %d\n', ...
        freq_cur, actual_train, actual_test);
end


%% ------------------------------------------------------------------
%%  楔形域 COMSOL 模型构建
%%
%%  几何约定（与图示及 models.py 完全对齐）：
%%    顶点在原点 (0,0)
%%    上边界 (y=0)         : Pressure-Release, Dirichlet p=0
%%    斜底边 (y=slope*x)   : Rigid Boundary, Neumann（自然 BC，无需显式设置）
%%    左顶点 (x=0, 退化)   : 楔尖，几何退化点，无可施加边界条件的边
%%    右边界 (x=Lx, 截断面): Nonreflecting, Robin/Sommerfeld ABC
%%
%%  楔形多边形顶点（逆时针）：
%%    (0,0) → (Lx,0) → (Lx,Ly) → (0,0)
%%    → 上边 y=0 从 (0,0)→(Lx,0)
%%    → 右截断边 从 (Lx,0)→(Lx,Ly)
%%    → 斜底边 从 (Lx,Ly)→(0,0)
%% ------------------------------------------------------------------
function [model, ph] = build_pde_model_wedge( ...
        Lx, Ly, H, k, with_sub, sp, src_depth, p_ref)
    import com.comsol.model.* com.comsol.model.util.*
    tag   = sprintf('DatasetGenWedge_%d', randi(1e9));
    model = ModelUtil.create(tag);
    comp  = model.component.create('comp1', true);
    geom  = comp.geom.create('geom1', 2);

    %% 楔形多边形：(0,0)→(Lx,0)→(Lx,Ly)→(0,0)
    poly1 = geom.create('poly1', 'Polygon');
    poly1.set('source', 'table');
    poly1.set('table', {num2str(0),  num2str(0);   ...   % 顶点（原点）
                        num2str(Lx), num2str(0);   ...   % 右上
                        num2str(Lx), num2str(Ly)});      % 右下
    %% 若有障碍椭圆（潜艇），做差集
    if with_sub && sp.a_hull > 0 && sp.b_hull > 0
        e1 = geom.create('e1','Ellipse');
        e1.set('semiaxes',[sp.a_hull, sp.b_hull]);
        e1.set('pos',[sp.ex, sp.ey]);
        dif = geom.create('dif1','Difference');
        dif.selection('input').set({'poly1'});
        dif.selection('input2').set({'e1'});
        dif.set('keepsubtract','off');
    end
    geom.run('fin');

    msh = comp.mesh.create('mesh1');
    msh.create('sz1','Size').set('hmax', num2str(H));
    msh.create('ftri1','FreeTri');
    msh.run;
    fprintf('    楔形网格生成完成\n');

    %% 边界分类（通过边中点坐标判断）
    slope     = Ly / Lx;
    line_norm = sqrt(slope^2 + 1);
    tol = max(H*3, 1.0);

    bnd_surface = [];   % y=0，上边，Dirichlet
    bnd_left    = [];   % x=0，退化点（楔形顶点），无需设置（面积为零）
    bnd_right   = [];   % x=Lx，截断面，Robin
    bnd_obs     = [];   % 椭圆边界，Dirichlet

    for ib = 1:10000
        try; xy = mphgetcoords(model,'geom1','boundary',ib); catch; break; end
        if isempty(xy) || size(xy,2) < 2; continue; end
        xm = mean(xy(1,:));
        ym = mean(xy(2,:));
        %% 判断归属
        if abs(ym) < tol && xm > tol
            %% 上边 y≈0（但排除退化顶点）
            bnd_surface(end+1) = ib; %#ok<AGROW>
        elseif abs(xm - Lx) < tol
            %% 右截断面 x=Lx
            bnd_right(end+1) = ib; %#ok<AGROW>
        elseif abs(xm) < tol
            %% 退化的左顶点（楔尖），通常只有一个节点，跳过
            bnd_left(end+1) = ib; %#ok<AGROW>
        else
            %% 其余：斜边（Rigid Neumann，自然 BC，无需显式设置）
            %% 或椭圆边界
            dist_to_slope = abs(slope*xm - ym) / line_norm;
            if dist_to_slope > tol * 2 && with_sub
                bnd_obs(end+1) = ib; %#ok<AGROW>
            end
            %% 斜边：不加到 bnd_obs，保持自然 Neumann
        end
    end

    ph = comp.physics.create('pde1','CoefficientFormPDE','geom1');
    ph.feature('cfeq1').set('c','1');
    ph.feature('cfeq1').set('a', sprintf('%.15g', -k^2));
    set_gaussian_source_ph(ph, src_depth, H, p_ref);

    %% 上边界 y=0：Dirichlet p=0（压力释放海面）
    if ~isempty(bnd_surface)
        d = ph.create('dir_surf','DirichletBoundary',1);
        d.selection.set(unique(bnd_surface)); d.set('r','0');
    end
    %% 障碍椭圆边界：Dirichlet p=0
    if with_sub && ~isempty(bnd_obs)
        d2 = ph.create('dir_obs','DirichletBoundary',1);
        d2.selection.set(unique(bnd_obs)); d2.set('r','0');
    end
    %% 右截断面：Robin ABC（Sommerfeld, -i*k）
    %% 左顶点(楔尖)通常面积为零，不施加 Robin
    bnd_robin = unique(bnd_right);
    if ~isempty(bnd_robin)
        wc = ph.create('wc_rb','WeakContribution',1);
        wc.selection.set(bnd_robin);
        wc.set('weakExpression', sprintf('(-j*%.15g)*u*test(u)', k));
    end
    %% 斜底边(Rigid Neumann)：COMSOL 默认自然边界条件，无需显式设置

    std1 = model.study.create('std1'); std1.create('stat','Stationary');
    sol1 = model.sol.create('sol1');   sol1.study('std1');
    sol1.create('st1','StudyStep').set('study','std1');
    sol1.create('v1','Variables');
    s1 = sol1.create('s1','Stationary');
    s1.set('nonlin','off'); s1.create('d1','Direct');
end


%% ------------------------------------------------------------------
%%  矩形域 COMSOL 模型构建（原版，保持不变）
%% ------------------------------------------------------------------
function [model, ph] = build_pde_model_comsol_mesh( ...
        Lx, Ly, H, k, with_sub, sp, src_depth, p_ref)
    import com.comsol.model.* com.comsol.model.util.*
    tag   = sprintf('DatasetGen_%d', randi(1e9));
    model = ModelUtil.create(tag);
    comp  = model.component.create('comp1', true);
    geom  = comp.geom.create('geom1', 2);

    r1 = geom.create('r1','Rectangle');
    r1.set('size',[Lx,Ly]); r1.set('pos',[0,0]);
    if with_sub && sp.a_hull > 0 && sp.b_hull > 0
        e1 = geom.create('e1','Ellipse');
        e1.set('semiaxes',[sp.a_hull, sp.b_hull]);
        e1.set('pos',[sp.ex, sp.ey]);
        dif = geom.create('dif1','Difference');
        dif.selection('input').set({'r1'});
        dif.selection('input2').set({'e1'});
        dif.set('keepsubtract','off');
    end
    geom.run('fin');

    msh = comp.mesh.create('mesh1');
    msh.create('sz1','Size').set('hmax', num2str(H));
    msh.create('ftri1','FreeTri');
    msh.run;
    fprintf('    网格生成完成\n');

    tol = max(H*3, 1.0);
    bnd_surface=[]; bnd_left=[]; bnd_right=[]; bnd_obs=[];
    for ib = 1:10000
        try; xy = mphgetcoords(model,'geom1','boundary',ib); catch; break; end
        if isempty(xy) || size(xy,2) < 2; continue; end
        xm = mean(xy(1,:)); ym = mean(xy(2,:));
        if     abs(ym)    < tol; bnd_surface(end+1) = ib;
        elseif abs(ym-Ly) < tol; % 海底 Neumann
        elseif abs(xm)    < tol; bnd_left(end+1) = ib;
        elseif abs(xm-Lx) < tol; bnd_right(end+1) = ib;
        else;                     bnd_obs(end+1) = ib;
        end
    end

    ph = comp.physics.create('pde1','CoefficientFormPDE','geom1');
    ph.feature('cfeq1').set('c','1');
    ph.feature('cfeq1').set('a', sprintf('%.15g', -k^2));
    set_gaussian_source_ph(ph, src_depth, H, p_ref);

    if ~isempty(bnd_surface)
        d = ph.create('dir_surf','DirichletBoundary',1);
        d.selection.set(unique(bnd_surface)); d.set('r','0');
    end
    if with_sub && ~isempty(bnd_obs)
        d2 = ph.create('dir_obs','DirichletBoundary',1);
        d2.selection.set(unique(bnd_obs)); d2.set('r','0');
    end
    bnd_robin = unique([bnd_left, bnd_right]);
    if ~isempty(bnd_robin)
        wc = ph.create('wc_rb','WeakContribution',1);
        wc.selection.set(bnd_robin);
        wc.set('weakExpression', sprintf('(-j*%.15g)*u*test(u)', k));
    end

    std1 = model.study.create('std1'); std1.create('stat','Stationary');
    sol1 = model.sol.create('sol1');   sol1.study('std1');
    sol1.create('st1','StudyStep').set('study','std1');
    sol1.create('v1','Variables');
    s1 = sol1.create('s1','Stationary');
    s1.set('nonlin','off'); s1.create('d1','Direct');
end


function set_gaussian_source_ph(ph, src_depth, H, p_ref)
    sigma = 1.5*H; norm2 = 2*pi*sigma^2;
    xs = src_depth(1); ys = src_depth(2);
    G = sprintf('exp(-((x-%.15g)^2+(y-%.15g)^2)/(2*%.15g^2))/%.15g', ...
        xs, ys, sigma, norm2);
    f_re = real(p_ref); f_im = imag(p_ref);
    if abs(f_im) > 0
        ph.feature('cfeq1').set('f', sprintf('(%.15g%+.15gi)*(%s)', f_re, f_im, G));
    else
        ph.feature('cfeq1').set('f', sprintf('%.15g*(%s)', f_re, G));
    end
end


function update_freq_coeff(ph, k)
    %% 更新亥姆霍兹系数 -k^2 和 Robin ABC（矩形/楔形均使用 wc_rb 标签）
    ph.feature('cfeq1').set('a', sprintf('%.15g', -k^2));
    try
        ph.feature('wc_rb').set('weakExpression', ...
            sprintf('(-j*%.15g)*u*test(u)', k));
    catch; end
end