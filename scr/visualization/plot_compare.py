import numpy as np
import matplotlib.pyplot as plt
import os

def smart_signal_slicer(bin_file_path):
    """
    利用 NumPy 极值定位，智能截取撞击段与噪声段，并绘制对比子图
    """
    fs = 44100  # 采样率 44.1 kHz
    target_duration = 0.1  # 目标总时长 0.1 秒
    half_window = int(fs * (target_duration / 2))  # 半窗口 2205 个点
    
    print(f"正在加载纯二进制数据: {bin_file_path}")
    data = np.memmap(bin_file_path, dtype=np.float32, mode='r')
    total_len = len(data)
    
    # ==========================================
    # 第一刀：精准定位“疑似撞击段” (靶心切片法)
    # ==========================================
    peak_idx = np.argmax(np.abs(data))
    i_start = max(0, peak_idx - half_window)
    i_end = min(total_len, peak_idx + half_window)
    
    impact_slice = data[i_start:i_end]
    t_impact_ms = (np.arange(i_start, i_end) / fs) * 1000.0
    print(f"[第一刀完成] 找到全局峰值，索引位置: {peak_idx}")

    # ==========================================
    # 第二刀：稳妥截取“纯净噪声段” (你的动态滑动算法！)
    # ==========================================
    noise_points = int(fs * target_duration)  # 需要 4410 个点
    n_start = 0
    noise_threshold = 0.005
    found_clean_noise = False
    
    while n_start + noise_points <= total_len:
        current_window = data[n_start : n_start + noise_points]
        
        # 找出当前窗口内所有绝对值大于等于阈值的点的【本地索引】
        exceed_indices = np.where(np.abs(current_window) >= noise_threshold)[0]
        
        if len(exceed_indices) == 0:
            # 数组为空，说明这个窗口里没有任何点超标，我们找到了完美区间！
            found_clean_noise = True
            break
        else:
            # 你的核心逻辑：找到这个窗口里【最后一个】超标的点
            last_invalid_local_idx = exceed_indices[-1]
            # 下一个有可能纯净的窗口，只能从这个点的下一个位置开始
            n_start += (last_invalid_local_idx + 1)

    # 防御性截取：如果滑到最后都没找到，强行取头部
    if not found_clean_noise:
        print("[警告] 遍历全图未找到完全低于 0.005 的纯净段，已默认截取文件头部！")
        n_start = 0
        
    n_end = n_start + noise_points
    noise_slice = data[n_start:n_end]
    t_noise_ms = (np.arange(n_start, n_end) / fs) * 1000.0
    print(f"[第二刀完成] 锁定纯净噪声段，起始索引: {n_start}，结束索引: {n_end}")

    # ==========================================
    # 开始 Matplotlib 高清绘制
    # ==========================================
    fig, axes = plt.subplots(2, 1, figsize=(12, 6), dpi=300, sharey=True)
    
    # [上图] 绘制纯净噪声段
    axes[0].plot(t_noise_ms, noise_slice, color='gray', linewidth=1.0)
    axes[0].set_title(f"Pure Background Noise (Max Amp < {noise_threshold})", fontsize=12, fontweight='bold')
    axes[0].set_ylabel("Amplitude", fontsize=10)
    axes[0].grid(True, linestyle='--', alpha=0.6)
    
    # [下图] 绘制撞击波包切片
    axes[1].plot(t_impact_ms, impact_slice, color='#d62728', linewidth=1.0)
    axes[1].scatter((peak_idx / fs) * 1000.0, data[peak_idx], color='#2ca02c', s=50, zorder=5, label='Global Peak')
    
    axes[1].set_title(f"Impact Envelope Centered at {round((peak_idx/fs)*1000, 2)} ms", fontsize=12, fontweight='bold')
    axes[1].set_xlabel("Time (ms)", fontsize=10)
    axes[1].set_ylabel("Amplitude", fontsize=10)
    axes[1].legend(loc='upper right')
    axes[1].grid(True, linestyle='--', alpha=0.6)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    test_bin_path = "/Users/lk/XJTU_Research/Code_Playground/100_Day_Project/outputs/2022523928.bin"
    if os.path.exists(test_bin_path):
        smart_signal_slicer(test_bin_path)
    else:
        print(f"未找到文件 {test_bin_path}")