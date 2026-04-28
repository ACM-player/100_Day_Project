import numpy as np
import matplotlib.pyplot as plt
import os

def plot_first_100ms(bin_file_path):
    """
    极速加载 .bin 裸二进制数据，并绘制前 0.1 秒的高清物理波形图
    """
    # 【物理参数设定】
    fs = 44100  # 真实采样率 44.1 kHz
    target_duration = 0.1  # 目标时长 0.1 秒
    
    # 算出 0.1 秒需要多少个数据点
    n_points = int(fs * target_duration)  # 4410 个点
    
    print(f"正在闪电加载纯二进制数据: {bin_file_path}")
    # 【工程魔法：裸二进制内存映射】
    # 因为是 .bin 文件，必须手动指定 dtype=np.float32
    # 使用 np.memmap 依然实现“硬盘虚读”，只加载前 4410 个点，保护内存！
    data = np.memmap(bin_file_path, dtype=np.float32, mode='r')
    
    # 防御性切片：万一总数据连 0.1 秒都不到，就取实际最大长度
    actual_points = min(n_points, len(data))
    slice_data = data[:actual_points]
    
    # 【核心任务：构建精确到毫秒 (ms) 的物理时间轴】
    t_ms = (np.arange(actual_points) / fs) * 1000.0
    
    print(f"提取完成！准备渲染前 {actual_points} 个点...")
    
    # === 开始 Matplotlib 高清绘制 ===
    # plt.figure(figsize=(12, 4), dpi=300)
    plt.figure(figsize=(10, 3.5), dpi=120)
    plt.plot(t_ms, slice_data, color='#1f77b4', linewidth=1.0)
    
    plt.title("Raw Time-Domain Waveform (First 0.1s)", fontsize=14, fontweight='bold')
    plt.xlabel("Time (ms)", fontsize=12)
    plt.ylabel("Amplitude (Zero-Mean)", fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # 指向你昨天刚输出的 .bin 文件路径
    test_bin_path = "/Users/lk/XJTU_Research/Code_Playground/100_Day_Project/outputs/2022523928.bin"
    
    if os.path.exists(test_bin_path):
        plot_first_100ms(test_bin_path)
    else:
        print(f"未找到文件 {test_bin_path}，请检查路径！")