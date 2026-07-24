%% data_generate_comsol_sol.m
%% ============================================================
%%  解析解参考数据集生成脚本（矩形 / 楔形，均无椭圆挖空）
%% ============================================================
%%  与 data_generate_comsol.m 的关键区别：
%%
%%    ★ 数据集「参考解 / 训练目标」使用【解析解】，而非 COMSOL 解。
%%      （原脚本因这两种带椭圆的几何无解析解，只能用 COMSOL 解作参考；
%%        本脚本针对两个「无椭圆」规范波导，解析解存在，直接作为 ground truth。）
%%
%%    ★ COMSOL 仅用于【验证】：每频率随机抽取 n_val 个样本用 COMSOL 求解，
%%      与解析解逐点比对（相对 L2 误差 / TL RMSE / 复相关），
%%      以证明解析解实现正确、数据生成可信。全部样本的目标仍是解析解。
%%
%%  解析解来源（ASA.tex）：
%%    · 矩形波导（range-independent，简正模）：
%%        p(x,z) = (i/D) Σ_m sin(k_zm z_s) sin(k_zm z) e^{i k_rm |x-x_s|} / k_rm
%%        k_zm = (2m-1)π/(2D),   k_rm = sqrt(k^2 - k_zm^2),   D = Ly（水深）
%%      注：ASA.tex 式(54) 印为 i/(2D) 系数，经方法-of-images 独立核验，
%%          正确系数应为 i/D（式(47)+(25) 推导一致）。本脚本采用 i/D。
%%
%%    · 楔形波导（polar，非整数阶 Bessel 简正模）：
%%        P(r,θ) = (iπ/θ0) Σ_n sin(γ_n θ_s) sin(γ_n θ) J_{γ_n}(k r_<) H^{(1)}_{γ_n}(k r_>)
%%        γ_n = (2n-1)π/(2θ0),  θ0 = atan(Ly/Lx),  r_<=min(r,r_s), r_>=max(r,r_s)
%%      两式均已用「方法 of images」独立核验到机器精度（θ0=π/4 时 8 个镜像）。
%%
%%  坐标约定（与 data_generate_comsol.m / 下游 Python 完全一致）：
%%    矩形：x 为水平距离(range)，y 为深度(depth)，海面 y=0 (Dirichlet p=0)，
%%          海底 y=Ly (Rigid Neumann)。解析式中 z ≡ y，D ≡ Ly。
%%    楔形：顶点在原点，海面 θ=0 (y=0, Dirichlet)，海底斜边 θ=θ0 (Rigid Neumann)，
%%          右截断 x=Lx (Robin ABC)。解析式中 r=hypot(x,y)，θ=atan2(y,x)。
%%
%%  归一化：COMSOL 源项 f = p_ref * Gauss，p_ref = i*besselh(0,1,k)/4，
%%    故 u_comsol ≈ p_ref * G_analytic（G 为单位点源 Green 函数）。
%%    数据集存储 U = p_ref * G_analytic，与原脚本 U_vertex_batch 量纲一致。
%% ============================================================

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
samples_per_freq = 2000;      % 解析解全量目标（便宜）；比原 2000 小即可验证
backup_ratio     = 0.1;      % 备份少量即可（下游需要非空备份数组）
boundary_margin  = 5.0;

%% ---- 解析解 / 验证专属参数 ----
n_val_per_freq   = 20;       % 每频率用 COMSOL 验证的样本数（0 = 跳过 COMSOL 验证）
mode_evan_decay  = 8.0;      % 矩形：evanescent 模保留到 k_zm*ref ~ e^-decay
wedge_evan_margin= 30.0;     % 楔形：模阶 γ_n 保留到 k*r_max + margin（防 Hankel 溢出）
mode_cap_rect    = 4000;     % 矩形模数硬上限
mode_cap_wedge   = 2000;     % 楔形模数硬上限
src_exclude_lam  = 1.0;      % 验证时排除源点周围 src_exclude_lam*波长 内节点
right_exclude_m  = 8.0;      % 验证时排除右截断边界附近 right_exclude_m 米（ABC 反射区）
apex_exclude_m   = 8.0;      % 楔形：排除楔尖附近 apex_exclude_m 米（r 小、模收敛慢）

random_seed      = 32;

%% 无椭圆（本脚本核心前提，强制关闭）
use_ellipse      = false;

%% 生成哪些域（两个解析解案例）
domains_to_run   = {'rectangle', 'wedge'};

%% export_dir 基础根目录
export_base = fullfile(fileparts(mfilename('fullpath')), 'comsol_dataset_export');

%% ============================================================
%%  UT4_OVERRIDE（便于批处理 / 单元测试覆盖参数）
%% ============================================================
if exist('UT4_OVERRIDE', 'var') && isstruct(UT4_OVERRIDE)
    ov = UT4_OVERRIDE;
    flds = {'Lx','Ly','c0','H_grid','amp','freqs','samples_per_freq', ...
            'backup_ratio','boundary_margin','n_val_per_freq', ...
            'mode_evan_decay','wedge_evan_margin','mode_cap_rect','mode_cap_wedge', ...
            'src_exclude_lam','right_exclude_m','apex_exclude_m', ...
            'random_seed','export_base','domains_to_run'};
    for fi_ = 1:numel(flds)
        f_ = flds{fi_};
        if isfield(ov, f_); eval(sprintf('%s = ov.%s;', f_, f_)); end
    end
end

use_ellipse = false;   % 再次强制（override 不可打开）

%% ============================================================
%% 初始化 COMSOL（仅验证需要；n_val_per_freq=0 时仍尝试建模导出网格）
%% ============================================================
addpath('D:\Comsol\COMSOL64\Multiphysics\mli');
import com.comsol.model.* com.comsol.model.util.*
try; mphstart; catch; end

num_freqs       = numel(freqs);
backup_per_freq = max(1, round(samples_per_freq * backup_ratio));

freq_tag = strjoin(arrayfun(@(x) num2str(x), sort(freqs), ...
    'UniformOutput',false), '_');

%% ============================================================
%% 主循环：逐个域生成
%% ============================================================
for dom_i = 1:numel(domains_to_run)
    domain = domains_to_run{dom_i};
    if ~ismember(domain, {'rectangle','wedge'})
        error('domain 非法: "%s"', domain);
    end

    %% ── 区分性输出目录（加 _analyticsol 后缀，避免与 COMSOL 参考数据集互盖）──
    dir_name = sprintf('%s_Lx%d_Ly%d_H%.3f_f%s_spf%d_analyticsol', ...
        domain, Lx, Ly, H_grid, freq_tag, samples_per_freq);
    export_dir = fullfile(export_base, dir_name);
    if ~exist(export_dir, 'dir'); mkdir(export_dir); end
    plot_dir = fullfile(export_dir, 'validation_plots');
    if ~exist(plot_dir, 'dir'); mkdir(plot_dir); end

    file_prefix = sprintf('Lx%d_Ly%d_H%.3f', Lx, Ly, H_grid);

    %% ── 日志 ──
    log_filename = sprintf('run_%s_%s.log', dir_name, datestr(now,'yyyymmdd_HHMMSS'));
    log_path = fullfile(export_dir, log_filename);
    diary(log_path); diary on;
    fprintf('[LOG] 日志: %s\n', log_path);

    theta0 = atan2(Ly, Lx);   % 楔形角（矩形不用）
    fprintf('\n============================================================\n');
    fprintf('  解析解参考数据集生成: 域=%s (无椭圆)\n', upper(domain));
    fprintf('  域: %d x %d m, H=%.3f, c0=%.1f\n', Lx, Ly, H_grid, c0);
    if strcmp(domain,'wedge')
        fprintf('  楔形角 θ0 = %.4f rad (%.2f°)\n', theta0, theta0*180/pi);
    else
        fprintf('  水深 D = Ly = %d m\n', Ly);
    end
    fprintf('  频率: [%s] Hz | 每频样本(解析): %d | COMSOL验证/频: %d\n', ...
        freq_tag, samples_per_freq, n_val_per_freq);
    fprintf('  参考解: 解析解 (ground truth) | COMSOL: 仅验证\n');
    fprintf('  输出: %s\n', export_dir);
    fprintf('============================================================\n\n');

    %% ── 步骤1: 建 COMSOL 模型（无椭圆）+ 导出网格 ──
    fprintf('步骤 1/4: 建立 COMSOL 模型 (%s, 无椭圆) 并导出网格...\n', domain);
    sp.ex=0; sp.ey=0; sp.a_hull=0; sp.b_hull=0;   % 无椭圆
    k_first     = 2*pi*freqs(1)/c0;
    p_ref_first = 1i * besselh(0,1,k_first) / 4;
    tmp_src = [Lx/2, Ly/4];

    if strcmp(domain,'wedge')
        [model, ph] = build_pde_model_wedge( ...
            Lx, Ly, H_grid, k_first, false, sp, tmp_src, p_ref_first);
    else
        [model, ph] = build_pde_model_comsol_mesh( ...
            Lx, Ly, H_grid, k_first, false, sp, tmp_src, p_ref_first);
    end

    meshdata = mphmesh(model, 'mesh1');
    tri_struct = [];
    for i = 1:numel(meshdata)
        if ~iscell(meshdata{i}); continue; end
        for j = 1:numel(meshdata{i})
            s = meshdata{i}{j};
            if isfield(s,'t') && size(s.t,1)==3; tri_struct = s; break; end
        end
        if ~isempty(tri_struct); break; end
    end
    if isempty(tri_struct); error('无法提取三角单元'); end

    p_out  = tri_struct.p;
    N_mesh = size(p_out, 2);
    t_raw  = tri_struct.t;
    if min(t_raw(:)) == 0; t_raw = t_raw + 1; end
    t_out   = t_raw;
    Ne_mesh = size(t_out, 2);
    fprintf('  网格: N=%d 节点, Ne=%d 单元\n', N_mesh, Ne_mesh);

    tol_bnd     = H_grid * 2;
    bnd_left    = find(abs(p_out(1,:))     <= tol_bnd);
    bnd_right   = find(abs(p_out(1,:)-Lx)  <= tol_bnd);
    bnd_surface = find(abs(p_out(2,:))     <= tol_bnd);
    if strcmp(domain,'wedge')
        slope = Ly/Lx; a_c=slope; b_c=-1.0;
        line_norm = sqrt(a_c^2+b_c^2);
        d_seabed = abs(a_c*p_out(1,:)+b_c*p_out(2,:))/line_norm;
        bnd_seabed = find(d_seabed <= tol_bnd);
    else
        bnd_seabed = find(abs(p_out(2,:)-Ly) <= tol_bnd);
    end

    Nmax = max([numel(bnd_left),numel(bnd_right),numel(bnd_surface),numel(bnd_seabed)]);
    B_out = zeros(4, Nmax, 'int32');
    B_out(1,1:numel(bnd_left))    = int32(bnd_left);
    B_out(2,1:numel(bnd_right))   = int32(bnd_right);
    B_out(3,1:numel(bnd_surface)) = int32(bnd_surface);
    B_out(4,1:numel(bnd_seabed))  = int32(bnd_seabed);

    all_edges = [t_out(1:2,:), t_out(2:3,:), t_out([3,1],:)];
    all_edges_sorted = sort(all_edges,1);
    [~, ia, ic] = unique(all_edges_sorted.','rows');
    edge_count = accumarray(ic,1);
    e_out = all_edges(:, ia(edge_count==1));

    mesh_filename = sprintf('comsol_mesh_%s.mat', file_prefix);
    mesh_save_path = fullfile(export_dir, mesh_filename);
    save(mesh_save_path,'p_out','t_out','e_out','B_out', ...
        'N_mesh','Ne_mesh','H_grid','Lx','Ly','domain','-v7.3');
    fprintf('  ✓ 网格已保存: %s\n', mesh_save_path);

    %% ── 步骤2: 源点采样（无椭圆，默认节点级无放回）──
    fprintf('\n步骤 2/4: 源点采样...\n');
    all_bnd_set = unique([bnd_left,bnd_right,bnd_surface,bnd_seabed]);
    x_nodes=p_out(1,:); y_nodes=p_out(2,:);
    margin_ok = (x_nodes>=boundary_margin)&(x_nodes<=Lx-boundary_margin)&(y_nodes>=boundary_margin);
    if strcmp(domain,'wedge')
        slope_w=Ly/Lx; ln_w=sqrt(slope_w^2+1);
        margin_ok = margin_ok & (slope_w*x_nodes-y_nodes > boundary_margin*ln_w);
        margin_ok = margin_ok & (y_nodes < slope_w*x_nodes);
    else
        margin_ok = margin_ok & (y_nodes<=Ly-boundary_margin);
    end
    is_bnd=false(1,N_mesh); is_bnd(all_bnd_set)=true;
    candidate_nodes = find(~is_bnd & margin_ok);
    N_candidates = numel(candidate_nodes);
    fprintf('  总节点 %d | 边界 %d | 有效候选 %d\n', N_mesh, numel(all_bnd_set), N_candidates);

    [all_src_depth, backup_src_depth, all_freq_indices, backup_freq_idx, ...
     all_src_node_idx, bak_src_node_idx] = ...
        default_sample_source_points(freqs, samples_per_freq, backup_per_freq, ...
            p_out, candidate_nodes, N_candidates, random_seed);
    num_samples = size(all_src_depth,1);
    split_info  = [];
    fprintf('  ✓ 采样完成: %d 主 + %d 备份\n', num_samples, size(backup_src_depth,1));

    %% ── 步骤3: 逐频率 解析解(全量) + COMSOL验证(子集) ──
    fprintf('\n步骤 3/4: 解析解计算 + COMSOL 验证...\n');
    t_total = tic;

    %% 纯解析自检（不依赖 COMSOL）：海面 Dirichlet 残差应 ~0
    fprintf('  [自检] 解析解边界条件（不依赖 COMSOL）:\n');

    val_summary = struct('freq',{},'n_val',{},'rel_l2_mean',{}, ...
        'tl_rmse_mean',{},'corr_mean',{},'bc_surface_max',{});

    for fi = 1:num_freqs
        freq = freqs(fi);
        k    = 2*pi*freq/c0;
        p_ref= 1i * besselh(0,1,k)/4;
        lam  = 2*pi/k;
        fprintf('\n  [%d/%d] %d Hz  k=%.4f  λ=%.2f m  |p_ref|=%.4g\n', ...
            fi, num_freqs, freq, k, lam, abs(p_ref));

        src_start = (fi-1)*samples_per_freq + 1;
        src_end   = fi*samples_per_freq;
        src_fi    = all_src_depth(src_start:src_end, :);   % [spf,2]

        %% ── 解析解：全量样本（数据集参考解）──
        U_analytic = zeros(samples_per_freq, N_mesh);   % 复数
        t_an = tic;
        for is = 1:samples_per_freq
            if strcmp(domain,'wedge')
                G = analytic_wedge(p_out, src_fi(is,:), k, theta0, ...
                                   wedge_evan_margin, mode_cap_wedge);
            else
                G = analytic_rect(p_out, src_fi(is,:), k, Ly, ...
                                  mode_evan_decay, H_grid, mode_cap_rect);
            end
            U_analytic(is,:) = p_ref * G;   % 与 COMSOL 量纲对齐

            if mod(is,50)==0 || is==samples_per_freq
                el  = toc(t_an);
                eta = el/is*(samples_per_freq-is);
                fprintf('    [解析解] %d/%d  %.1f 样本/s  已用 %.1fs  剩 %.1fs\n', ...
                    is, samples_per_freq, is/el, el, eta);
            end
        end
        U_vertex_batch = U_analytic;        % ★ 数据集目标 = 解析解

        %% ── 解析解边界条件自检（海面 y=0 应满足 Dirichlet p=0）──
        bc_surface_max = 0;
        if ~isempty(bnd_surface)
            bc_vals = abs(U_analytic(:, bnd_surface));
            ref_mag = mean(abs(U_analytic(:)));
            bc_surface_max = max(bc_vals(:)) / max(ref_mag, eps);
        end
        fprintf('    [自检] 海面 max|p|/mean|p| = %.2e （应 ≈ 0）\n', bc_surface_max);

        %% ── COMSOL 验证（随机抽 n_val 个样本）──
        n_val = min(n_val_per_freq, samples_per_freq);
        rel_l2_arr = []; tl_rmse_arr = []; corr_arr = [];
        U_comsol_val = [];
        val_idx = [];
        if n_val > 0
            update_freq_coeff(ph, k);
            [minfo,~] = mphmatrix(model,'sol1','out',{'K'},'initmethod','init');
            K = sparse(minfo.K); N_dof = size(K,1);

            rng(random_seed + 100 + fi, 'twister');
            val_idx = sort(randperm(samples_per_freq, n_val));
            U_comsol_val = zeros(n_val, N_mesh);

            t_val = tic;
            val_step = max(1, min(50, round(n_val/4)));   % 验证样本少，按 ~1/4 进度或50取小
            for vv = 1:n_val
                is = val_idx(vv);
                set_gaussian_source_ph(ph, src_fi(is,:), H_grid, p_ref);
                model.sol('sol1').runAll;
                dsets = model.result.dataset.tags;
                u_v = double(mphinterp(model,'u','coord',p_out,'dataset',char(dsets(1))));
                U_comsol_val(vv,:) = u_v(:).';

                %% 验证掩码：排除源点邻域 / 右边界 / (楔形)楔尖
                [m_ok] = validation_mask(p_out, src_fi(is,:), lam, ...
                    src_exclude_lam, Lx, right_exclude_m, ...
                    domain, apex_exclude_m);
                uc = U_comsol_val(vv, m_ok);
                ua = U_analytic(is, m_ok);
                rel_l2 = norm(uc-ua) / max(norm(ua), eps);

                TLc = 20*log10(abs(uc)/abs(p_ref) + eps);
                TLa = 20*log10(abs(ua)/abs(p_ref) + eps);
                tl_rmse = sqrt(mean((TLc-TLa).^2));
                cc = abs(sum(uc.*conj(ua))) / max(sqrt(sum(abs(uc).^2)*sum(abs(ua).^2)),eps);

                rel_l2_arr(end+1)  = rel_l2;   %#ok<AGROW>
                tl_rmse_arr(end+1) = tl_rmse;  %#ok<AGROW>
                corr_arr(end+1)    = cc;       %#ok<AGROW>

                if mod(vv,val_step)==0 || vv==n_val
                    el  = toc(t_val);
                    eta = el/vv*(n_val-vv);
                    fprintf('    [COMSOL验证] %d/%d  %.1f 样本/s  已用 %.1fs  剩 %.1fs\n', ...
                        vv, n_val, vv/el, el, eta);
                end
            end

            fprintf('    [验证] n=%d | rel-L2 mean=%.3e max=%.3e | TL-RMSE mean=%.2f dB | corr mean=%.4f\n', ...
                n_val, mean(rel_l2_arr), max(rel_l2_arr), mean(tl_rmse_arr), mean(corr_arr));

            %% 画第一个验证样本的对比图
            plot_validation(p_out, t_out, U_comsol_val(1,:), U_analytic(val_idx(1),:), ...
                p_ref, src_fi(val_idx(1),:), freq, domain, Lx, Ly, ...
                fullfile(plot_dir, sprintf('val_%s_%dHz.png', domain, freq)));
        else
            N_dof = N_mesh;
            K = sparse(N_dof, N_dof);
            fprintf('    [验证] n_val_per_freq=0，跳过 COMSOL 验证\n');
        end

        val_summary(fi).freq           = freq;
        val_summary(fi).n_val          = n_val;
        val_summary(fi).rel_l2_mean    = tern(isempty(rel_l2_arr),NaN,mean(rel_l2_arr));
        val_summary(fi).tl_rmse_mean   = tern(isempty(tl_rmse_arr),NaN,mean(tl_rmse_arr));
        val_summary(fi).corr_mean      = tern(isempty(corr_arr),NaN,mean(corr_arr));
        val_summary(fi).bc_surface_max = bc_surface_max;

        %% ── 保存每频率 batch（U_vertex_batch = 解析解）──
        [K_i,K_j,K_v] = find(K);
        K_i0=int64(K_i(:)-1); K_j0=int64(K_j(:)-1); K_data=K_v(:);
        K_shape=int64([N_dof,N_dof]);
        freq_idx_fi = all_freq_indices(src_start:src_end);
        src_node_idx_fi = int32(all_src_node_idx(src_start:src_end));
        src_depth_fi = src_fi;
        wavenumber=k; frequency=freq; p_ref_val=p_ref;
        Lx_export=Lx; Ly_export=Ly; H_grid_export=H_grid;
        N_dof_export=int64(N_dof); N_mesh_export=int64(N_mesh);
        split_info_fi=[];
        reference_solution_type = 'analytic';   % ★ 标记参考解类型
        U_comsol_val_fi = U_comsol_val;
        val_idx_fi = int32(val_idx(:));
        val_rel_l2 = rel_l2_arr(:); val_tl_rmse = tl_rmse_arr(:); val_corr = corr_arr(:);

        batch_filename = sprintf('comsol_batch_%s_f%dHz.mat', file_prefix, freq);
        out_mat = fullfile(export_dir, batch_filename);
        save(out_mat, ...
            'K_i0','K_j0','K_data','K_shape', ...
            'U_vertex_batch', ...
            'src_depth_fi','freq_idx_fi','src_node_idx_fi', ...
            'frequency','wavenumber','p_ref_val', ...
            'Lx_export','Ly_export','H_grid_export', ...
            'N_dof_export','N_mesh_export','split_info_fi', ...
            'reference_solution_type', ...
            'U_comsol_val_fi','val_idx_fi','val_rel_l2','val_tl_rmse','val_corr', ...
            '-v7.3');
        fprintf('    ✓ 已保存: %s\n', out_mat);
    end

    %% ── 步骤4: 保存清单 + 验证汇总 ──
    fprintf('\n步骤 4/4: 保存清单...\n');
    selected_frequencies=freqs; samples_per_frequency=samples_per_freq;
    Lx_m=Lx; Ly_m=Ly; H_grid_m=H_grid; c0_m=c0; amp_m=amp;
    use_ellipse_m=false; ellipse_cx_m=0; ellipse_cy_m=0;
    ellipse_a_m=0; ellipse_b_m=0;
    boundary_margin_m=boundary_margin;
    random_seed_m=random_seed; backup_ratio_m=backup_ratio;
    N_mesh_m=int64(N_mesh);
    total_export_time_s=toc(t_total);
    split_train_test_m=false; train_max_x_m=0; train_max_y_m=0; train_ratio_m=0;
    domain_m=domain;
    reference_solution_type_m='analytic';
    theta0_m = theta0;
    validation_summary_m = val_summary;

    manifest_filename = sprintf('comsol_batch_manifest_%s_f%s.mat', file_prefix, freq_tag);
    manifest_path = fullfile(export_dir, manifest_filename);
    save(manifest_path, ...
        'selected_frequencies','samples_per_frequency', ...
        'all_src_depth','backup_src_depth', ...
        'all_freq_indices','backup_freq_idx', ...
        'all_src_node_idx','bak_src_node_idx', ...
        'split_info','N_mesh_m', ...
        'Lx_m','Ly_m','H_grid_m','c0_m','amp_m', ...
        'use_ellipse_m','ellipse_cx_m','ellipse_cy_m','ellipse_a_m','ellipse_b_m', ...
        'boundary_margin_m','random_seed_m','backup_ratio_m','total_export_time_s', ...
        'split_train_test_m','train_max_x_m','train_max_y_m','train_ratio_m', ...
        'domain_m','reference_solution_type_m','theta0_m', ...
        'validation_summary_m', ...
        '-v7.3');
    fprintf('  ✓ 清单已保存: %s\n', manifest_path);

    %% ── 验证总表 ──
    fprintf('\n  ┌───────── 验证汇总 (域=%s) ─────────┐\n', domain);
    fprintf('  freq(Hz) | n_val | rel-L2   | TL-RMSE(dB) | corr   | BC海面\n');
    for fi=1:num_freqs
        v=val_summary(fi);
        fprintf('  %6d   |  %3d  | %.2e | %8.3f | %.4f | %.1e\n', ...
            v.freq, v.n_val, v.rel_l2_mean, v.tl_rmse_mean, v.corr_mean, v.bc_surface_max);
    end
    fprintf('  └──────────────────────────────────────────┘\n');
    fprintf('  总耗时: %.1f s\n', total_export_time_s);

    %% ── 下游 Python 调用建议 ──
    fprintf('\n  建议运行:\n');
    fprintf('    python Ocean_Dataset_barrier_comsol.py \\\n');
    fprintf('        --data_dir "%s" \\\n', export_dir);
    fprintf('        --frequencies %s --samples_per_freq %d\n', num2str(freqs), samples_per_freq);

    try; ModelUtil.remove(model.tag); catch; end
    diary off;
    fprintf('日志已保存: %s\n\n', log_path);
end

fprintf('\n★ 全部域生成完毕。\n');


%% ============================================================
%%  解析解函数
%% ============================================================

%% ------------------------------------------------------------------
%% analytic_rect：矩形波导简正模 Green 函数（单位点源）
%%   p(x,z) = (i/D) Σ_m sin(k_zm z_s) sin(k_zm z) e^{i k_rm|x-x_s|}/k_rm
%%   已用方法-of-images 独立核验（系数 i/D，非 ASA 式54 印刷的 i/2D）。
%% 输入: p_out[2,N]（x=行1,z=行2）, src[1,2], k, D(=Ly)
%% 输出: G[1,N] 复数
%% ------------------------------------------------------------------
function G = analytic_rect(p_out, src, k, D, evan_decay, H_grid, mode_cap)
    x = p_out(1,:);  z = p_out(2,:);      % 1×N
    xs = src(1);     zs = src(2);
    N = numel(x);
    G = zeros(1, N);

    %% 模数上限：传播模 + 足够 evanescent 模（近场衰减 e^-decay 覆盖）
    kzm_max = evan_decay / max(H_grid, 0.25);
    M_evan  = ceil((kzm_max * 2 * D / pi + 1) / 2);
    M_prop  = ceil((k       * 2 * D / pi + 1) / 2) + 5;
    Mmax = min(max(M_prop, M_evan), mode_cap);

    dx = abs(x - xs);
    for m = 1:Mmax
        kzm = (2*m-1)*pi/(2*D);
        krm = sqrt(k*k - kzm*kzm);        % 复数：kzm>k → 纯虚（衰减）
        if imag(krm) < 0; krm = -krm; end % 保证外行/衰减分支
        if real(krm) < 0; krm = -krm; end
        G = G + (2.0/D) * sin(kzm*zs) .* sin(kzm.*z) ...
                .* (1i ./ (2*krm)) .* exp(1i * krm * dx);
    end
    % 前因子 (2/D)*(1/2)*i = i/D ✓
end


%% ------------------------------------------------------------------
%% analytic_wedge：楔形波导简正模 Green 函数（单位点源）
%%   P(r,θ) = (iπ/θ0) Σ_n sin(γ_n θ_s) sin(γ_n θ) J_{γ_n}(k r_<) H1_{γ_n}(k r_>)
%%   γ_n=(2n-1)π/(2θ0)。已用方法-of-images(θ0=π/4) 核验到机器精度。
%%   数值防护：模阶超 k*r_max+margin 即截断（此后 J≈0、H 溢出，乘积→0）；
%%             非有限项置 0。
%% 输入: p_out[2,N]（x=行1,y=行2）, src[1,2], k, theta0
%% 输出: G[1,N] 复数
%% ------------------------------------------------------------------
function G = analytic_wedge(p_out, src, k, theta0, evan_margin, mode_cap)
    x = p_out(1,:);  y = p_out(2,:);
    r  = hypot(x, y);          % 1×N
    th = atan2(y, x);          % ∈ (0, theta0) 内部
    xs = src(1); ys = src(2);
    rs = hypot(xs, ys);  ths = atan2(ys, xs);

    N = numel(r);
    G = zeros(1, N);
    rlt = min(r, rs);          % r_<
    rgt = max(r, rs);          % r_>
    pre = 1i * pi / theta0;

    g_max = k * max(rgt) + evan_margin;
    n = 1;
    while true
        g = (2*n-1)*pi/(2*theta0);
        if g > g_max || n > mode_cap; break; end
        Jl = besselj(g, k*rlt);        % 1×N
        Hg = besselh(g, 1, k*rgt);     % 1×N
        term = pre * sin(g*ths) .* sin(g.*th) .* Jl .* Hg;
        term(~isfinite(term)) = 0;     % 防溢出污染
        G = G + term;
        n = n + 1;
    end
end


%% ------------------------------------------------------------------
%% validation_mask：验证时排除不可靠区域
%%   · 源点邻域（Gaussian 源 vs delta 源差异 + 模截断近场误差）
%%   · 右截断边界附近（一阶 ABC 反射）
%%   · 楔形：楔尖附近（r 小、Bessel 模收敛慢）
%% 输出: m_ok [1,N] logical
%% ------------------------------------------------------------------
function m_ok = validation_mask(p_out, src, lam, src_excl_lam, ...
        Lx, right_excl, domain, apex_excl)
    x = p_out(1,:); y = p_out(2,:);
    d_src = hypot(x - src(1), y - src(2));
    m_ok = d_src > (src_excl_lam * lam);
    m_ok = m_ok & (x < Lx - right_excl);      % 排除右 ABC 边界
    if strcmp(domain, 'wedge')
        r = hypot(x, y);
        m_ok = m_ok & (r > apex_excl);        % 排除楔尖
    end
end


%% ------------------------------------------------------------------
%% plot_validation：COMSOL vs 解析解 TL 三联图
%% ------------------------------------------------------------------
function plot_validation(p_out, t_out, u_comsol, u_analytic, p_ref, ...
        src, freq, domain, Lx, Ly, save_path)
    try
        X = p_out(1,:); Y = p_out(2,:);
        tri = t_out(1:3,:)';
        TLc = 20*log10(abs(u_comsol)/abs(p_ref) + eps);
        TLa = 20*log10(abs(u_analytic)/abs(p_ref) + eps);
        err = TLc - TLa;

        f = figure('Visible','off','Position',[100 100 1500 420]);
        vmin=-60; vmax=0;
        titles = {'COMSOL TL (dB)','解析解 TL (dB)','误差 (COMSOL−解析, dB)'};
        data = {TLc, TLa, err};
        clims = {[vmin vmax],[vmin vmax],[-10 10]};
        for s = 1:3
            subplot(1,3,s);
            trisurf(tri, X, Y, zeros(size(X)), data{s}, ...
                'EdgeColor','none','FaceColor','interp'); view(2);
            axis equal tight; set(gca,'YDir','reverse');
            caxis(clims{s}); colorbar; colormap(gca, jet);
            hold on; plot(src(1), src(2), 'r*','MarkerSize',10);
            if strcmp(domain,'wedge')
                plot([0 Lx],[0 Ly],'k-','LineWidth',1);
            end
            title(sprintf('%s', titles{s}));
            xlabel('X (m)'); ylabel('Y / Depth (m)');
        end
        sgtitle(sprintf('[%s] %d Hz  验证对比', upper(domain), freq));
        saveas(f, save_path); close(f);
    catch ME
        fprintf('    [绘图警告] %s\n', ME.message);
    end
end


function out = tern(cond, a, b)
    if cond; out = a; else; out = b; end
end


%% ============================================================
%%  以下 COMSOL 建模 / 采样 辅助函数
%%  （从 data_generate_comsol.m 复制，保持自包含；逻辑一致，仅无椭圆路径生效）
%% ============================================================

%% ------------------------------------------------------------------
%% default_sample_source_points（节点级无放回采样）
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
        drawn_idx = candidate_nodes(perm);

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
        assert(isempty(intersect(main_nodes, bak_nodes)), ...
            '[default] %d Hz 主/备节点存在交集', freqs(fi));

        fprintf('  [%d/%d] %d Hz: 主 %d | 备 %d\n', ...
            fi, num_freqs, freqs(fi), samples_per_freq, backup_per_freq);
    end
end


%% ------------------------------------------------------------------
%% build_pde_model_wedge（楔形域，无椭圆时 with_sub=false）
%% ------------------------------------------------------------------
function [model, ph] = build_pde_model_wedge( ...
        Lx, Ly, H, k, with_sub, sp, src_depth, p_ref)
    import com.comsol.model.* com.comsol.model.util.*
    tag   = sprintf('SolGenWedge_%d', randi(1e9));
    model = ModelUtil.create(tag);
    comp  = model.component.create('comp1', true);
    geom  = comp.geom.create('geom1', 2);

    poly1 = geom.create('poly1', 'Polygon');
    poly1.set('source', 'table');
    poly1.set('table', {num2str(0),  num2str(0);   ...
                        num2str(Lx), num2str(0);   ...
                        num2str(Lx), num2str(Ly)});
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

    slope=Ly/Lx; line_norm=sqrt(slope^2+1); tol=max(H*3,1.0);
    bnd_surface=[]; bnd_left=[]; bnd_right=[]; bnd_obs=[];
    for ib = 1:10000
        try; xy = mphgetcoords(model,'geom1','boundary',ib); catch; break; end
        if isempty(xy) || size(xy,2) < 2; continue; end
        xm=mean(xy(1,:)); ym=mean(xy(2,:));
        if abs(ym)<tol && xm>tol
            bnd_surface(end+1)=ib; %#ok<AGROW>
        elseif abs(xm-Lx)<tol
            bnd_right(end+1)=ib; %#ok<AGROW>
        elseif abs(xm)<tol
            bnd_left(end+1)=ib; %#ok<AGROW>
        else
            dist_to_slope = abs(slope*xm-ym)/line_norm;
            if dist_to_slope>tol*2 && with_sub
                bnd_obs(end+1)=ib; %#ok<AGROW>
            end
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
    bnd_robin = unique(bnd_right);
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


%% ------------------------------------------------------------------
%% build_pde_model_comsol_mesh（矩形域，无椭圆时 with_sub=false）
%% ------------------------------------------------------------------
function [model, ph] = build_pde_model_comsol_mesh( ...
        Lx, Ly, H, k, with_sub, sp, src_depth, p_ref)
    import com.comsol.model.* com.comsol.model.util.*
    tag   = sprintf('SolGen_%d', randi(1e9));
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

    tol=max(H*3,1.0);
    bnd_surface=[]; bnd_left=[]; bnd_right=[]; bnd_obs=[];
    for ib = 1:10000
        try; xy = mphgetcoords(model,'geom1','boundary',ib); catch; break; end
        if isempty(xy) || size(xy,2) < 2; continue; end
        xm=mean(xy(1,:)); ym=mean(xy(2,:));
        if     abs(ym)    < tol; bnd_surface(end+1)=ib; %#ok<AGROW>
        elseif abs(ym-Ly) < tol; % 海底 Neumann（自然 BC）
        elseif abs(xm)    < tol; bnd_left(end+1)=ib; %#ok<AGROW>
        elseif abs(xm-Lx) < tol; bnd_right(end+1)=ib; %#ok<AGROW>
        else;                     bnd_obs(end+1)=ib; %#ok<AGROW>
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
    ph.feature('cfeq1').set('a', sprintf('%.15g', -k^2));
    try
        ph.feature('wc_rb').set('weakExpression', ...
            sprintf('(-j*%.15g)*u*test(u)', k));
    catch; end
end
