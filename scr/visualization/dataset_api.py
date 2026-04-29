import numpy as np
import matplotlib.pyplot as plt
import os

class AcousticDataset:
    """
    声发射数据集预处理管线 (Day 8 封装)
    """

    def __init__(self, file_path, fs=44100):
        """
        初始化机器（出厂设置）
        这里接收的 file_path 和 fs，都会被存入 self（机器本身）的记忆中。
        """
        self.file_path = file_path
        self.fs = fs  # 真实采样率 44.1 kHz
        self.data = None  # 预留位置，等按了 load_data 按钮后再把数据装进来

    def load_data(self):
        """
        数据加载方法（Day 4/5/6 的融合）
        极速加载 .bin 裸二进制数据
        """
        if not os.path.exists(self.file_path):
            print(f"错误：找不到文件 {self.file_path}")
            return

        print(f"正在通过内存映射 (memmap) 极速加载: {self.file_path} ...")
        # 将读取的数据存给 self.data，这样后面的画图按钮也能直接用！
        self.data = np.memmap(self.file_path, dtype=np.float32, mode='r')
        print(f"加载成功！共包含 {len(self.data)} 个采样点。")

    def plot_raw(self, target_duration=0.1):
        """
        全局波形查看方法（Day 6 任务：绘制高精度原始波形图）
        """
        # 防呆设计：检查是否已经加载了数据
        if self.data is None:
            print("请先调用 load_data() 加载数据！")
            return

        print(f"正在绘制前 {target_duration} 秒的物理波形图...")
        
        # 直接使用 self.fs，不用再当作参数传进来了
        num_samples = int(self.fs * target_duration) 
        
        # 切片截取数据
        plot_data = self.data[:num_samples]
        time_axis = np.linspace(0, target_duration, num_samples)

        # Matplotlib 绘图逻辑 (你 Day 6 的优秀代码)
        plt.figure(figsize=(12, 4))
        plt.plot(time_axis, plot_data, color='#1f77b4', linewidth=0.8, label="Raw Waveform")
        plt.title(f"Acoustic Emission Raw Waveform (First {target_duration}s)", fontsize=14)
        plt.xlabel("Time (Seconds)", fontsize=12)
        plt.ylabel("Amplitude", fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend(loc="upper right")
        plt.tight_layout()
        plt.show()

    def plot_subplots(self, noise_start=0.0, impact_start=0.05, duration=0.01):
        """
        局部对比查看方法（Day 7 任务：绘制背景噪声与疑似撞击的 subplots 对比图）
        """
        if self.data is None:
            print("请先调用 load_data() 加载数据！")
            return

        print("正在绘制背景噪声与撞击信号的对比图...")

        # 计算噪声段的起始和结束索引
        n_start_idx = int(noise_start * self.fs)
        n_end_idx = n_start_idx + int(duration * self.fs)
        noise_data = self.data[n_start_idx:n_end_idx]
        noise_time = np.linspace(noise_start, noise_start + duration, len(noise_data))

        # 计算撞击段的起始和结束索引
        i_start_idx = int(impact_start * self.fs)
        i_end_idx = i_start_idx + int(duration * self.fs)
        impact_data = self.data[i_start_idx:i_end_idx]
        impact_time = np.linspace(impact_start, impact_start + duration, len(impact_data))

        # 创建上下两个子图，并强制共享 Y 轴 (sharey=True)
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6), sharey=True)

        # 画上面的噪声图
        ax1.plot(noise_time, noise_data, color='gray', linewidth=0.8)
        ax1.set_title("Background Noise Segment", fontsize=12)
        ax1.grid(True, linestyle='--', alpha=0.6)

        # 画下面的疑似撞击图
        ax2.plot(impact_time, impact_data, color='red', linewidth=0.8)
        ax2.set_title("Suspected Impact Segment", fontsize=12)
        ax2.set_xlabel("Time (Seconds)")
        ax2.grid(True, linestyle='--', alpha=0.6)

        plt.tight_layout()
        plt.show()

# ==========================================
# 下面是测试区域 (你的遥控器)
# ==========================================
if __name__ == "__main__":
    # 指向你的 .bin 文件路径
    test_bin_path = "/Users/lk/XJTU_Research/Code_Playground/100_Day_Project/outputs/2022523928.bin"
    
    # 1. 实例化对象（按图纸造出机器）
    my_dataset = AcousticDataset(file_path=test_bin_path, fs=44100)

    # 2. 按下“加载数据”按钮
    my_dataset.load_data()

    # 3. 按下“画全局图”按钮 (Day 6 任务)
    my_dataset.plot_raw(target_duration=0.1)
    
    # 4. 按下“画局部对比图”按钮 (Day 7 任务)
    # 假设 0~0.01秒是噪声，0.05~0.06秒是撞击
    my_dataset.plot_subplots(noise_start=0.0, impact_start=0.05, duration=0.01)