# import numpy as np
# from lazy_reader import lazy_read_signal
# from numpy_test import calculate_global_stats


# # 阶段 2：今日核心任务 - 零均值化与 3-sigma 清洗
# # ==========================================
# def clean_and_zero_mean(file_path, global_mean, global_sigma):
#     """
#     第二遍扫描：零均值化，并利用物理常识剔除孤立毛刺
#     """
#     data_generator = lazy_read_signal(file_path)
    
#     # 划定 3-sigma 报警红线
#     threshold = 3 * global_sigma
#     print(f"  └─ 已划定 3-Sigma 红线: 绝对值超过 {threshold:.6f} 将被视为疑似异常")

#     chunk_count = 0
#     for data_piece in data_generator:
#         merge_data = ' '.join(data_piece)
#         numpy_data = np.fromstring(merge_data, dtype=np.float32, sep=' ')
        
#         # 【魔法 1：广播机制 (Broadcasting)】
#         # 一行代码，让几万个数据点瞬间减去同一个均值，全军拉回 0 轴
#         zero_mean_data = numpy_data - global_mean
        
#         # 【魔法 2：布尔掩码 (Boolean Mask)】
#         # 瞬间找出现有数据中所有越界的值，生成一个装满 True/False 的矩阵
#         is_over_threshold = np.abs(zero_mean_data) > threshold
        
#         # 【魔法 3：错位排查法 (找孤立毛刺)】
#         # 物理常识：真实的砂子撞击是连续震动，电路毛刺是孤立的单点。
#         # 我们用 np.roll 把掩码向左和向右各“错位”一格，查看它的左右邻居
#         left_neighbor_over = np.roll(is_over_threshold, 1)
#         right_neighbor_over = np.roll(is_over_threshold, -1)
        
#         # 判断条件：自己超标了 (True)，并且左边没超标 (~False)，并且右边也没超标 (~False)
#         # 用 & (与) 符号瞬间完成几万次对比
#         is_isolated_glitch = is_over_threshold & (~left_neighbor_over) & (~right_neighbor_over)
        
#         # 【执行清洗】
#         # 直接把被判定为“孤立毛刺”的坐标，强行按在 0 轴上（杀掉）
#         cleaned_data = np.copy(zero_mean_data)
#         cleaned_data[is_isolated_glitch] = 0.0
        
#         chunk_count += 1
        
#         # 切片测试：我们今天依然只看第一块数据的清洗效果
#         if chunk_count == 1:
#             glitches_killed = np.sum(is_isolated_glitch) # 统计杀掉了多少个毛刺
#             print(f"  └─ 🎯 第一块数据清洗完毕！")
#             print(f"  └─ 自动识别并清除了 {glitches_killed} 个非物理电路毛刺。")
#             print(f"  └─ 清洗前最大值: {np.max(zero_mean_data):.6f}，清洗后最大值: {np.max(cleaned_data):.6f}")
            
#             # 优雅地产出干净的数据，供明天的数据存盘使用
#             yield cleaned_data
#             break # 测试阶段，先刹车

# # --- 主程序测试入口 ---
# if __name__ == "__main__":
#     test_file_path = "/Volumes/LKs' disk/中海油能源发展装备公司海上油气管道含砂监测技术应用研究/结题资料/现场数据/2022523928.txt"
    
#     print("\n>>> 启动第一阶段：计算全局统计特征 <<<")
#     final_max, final_min, final_mean, final_sigma = calculate_global_stats(test_file_path)
#     print(f"  └─ 全局均值: {final_mean:.6f}")
#     print(f"  └─ 全局标准差 (Sigma): {final_sigma:.6f}")
    
#     print("\n>>> 启动第二阶段：执行容错清洗流水线 <<<")
#     # 把第一阶段算出来的均值和标准差，喂给第二阶段的清洗机
#     clean_generator = clean_and_zero_mean(test_file_path, final_mean, final_sigma)
    
#     # 吐出第一块清洗完毕的干净数据
#     clean_chunk = next(clean_generator)
#     print("-" * 40)
#     print("✅ Day 4 任务测试完美通关！")


#######################################
# #=========3 sigma失效，由于采样率为44.1khz，太低了============#
# import numpy as np
# import matplotlib.pyplot as plt
# # 导入你昨天的流式读取函数
# from lazy_reader import lazy_read_signal 
# from numpy_test import calculate_global_stats

# if __name__ == "__main__":
#     test_file_path = "/Volumes/LKs' disk/中海油能源发展装备公司海上油气管道含砂监测技术应用研究/结题资料/现场数据/2022523928.txt"
    
#     # 假设你昨天算出来的全局均值是这个数（你需要替换成你实际跑出来的结果）
#     global_max, global_min, global_mean, global_sigma = calculate_global_stats(test_file_path) 
    
#     # 1. 读出第一块数据做实验 (读个大概 2000 行，方便画图看细节)
#     data_generator = lazy_read_signal(test_file_path, chunk_size=2000)
#     data_piece = next(data_generator)
#     merge_data = ' '.join(data_piece)
#     signal_array = np.fromstring(merge_data, dtype=np.float32, sep=' ')
    
#     # 2. 零均值化 (利用强大的广播机制，瞬间完成！)
#     centered_signal = signal_array - global_mean
    
#     # 3. 方案A：智能 3-Sigma 异常清洗
#     # 直接使用 Day 3 算出的全局标准差！
#     threshold = 3 * global_sigma
    
#     # 找出所有超出 3-Sigma 的点 (得到一个布尔数组 [False, True, False...])
#     is_outlier = np.abs(centered_signal) > threshold
    
#     # 核心逻辑：找“孤立”毛刺。利用 np.roll 把数组向左/右平移一位，判断邻居是否正常
#     left_neighbor_normal = ~np.roll(is_outlier, 1)  # 左边没超标
#     right_neighbor_normal = ~np.roll(is_outlier, -1) # 右边没超标
    
#     # 为了防止头尾越界报错，强制首尾邻居为正常
#     left_neighbor_normal[0] = True
#     right_neighbor_normal[-1] = True
    
#     # 满足三个条件：自己是异常值 & 左边正常 & 右边正常 -> 这就是瞬间电路毛刺！
#     isolated_spikes = is_outlier & left_neighbor_normal & right_neighbor_normal
    
#     # 复制一份数据用来清洗
#     cleaned_signal = centered_signal.copy()
#     # 把这些孤立的脏毛刺直接归零 (或者你想更温柔点，可以替换为0)
#     cleaned_signal[isolated_spikes] = 0
    
#     print(f"标准差: {global_sigma:.4f}, 3-Sigma阈值: {threshold:.4f}")
#     print(f"在这个切片中发现了 {np.sum(isolated_spikes)} 个孤立异常脉冲。")

#     # 4. 画图对比！(Matplotlib 登场)
#     plt.figure(figsize=(12, 6)) # 设置画布大小
    
#     # 画子图1：处理前 (仅做了零均值)
#     plt.subplot(2, 1, 1) 
#     plt.plot(centered_signal, color='red', alpha=0.7, label="Original (Zero-Mean)")
#     plt.axhline(threshold, color='black', linestyle='--', label='+3 Sigma')
#     plt.axhline(-threshold, color='black', linestyle='--', label='-3 Sigma')
#     plt.title("Before Smart Cleaning")
#     plt.legend(loc="upper right")
    
#     # 画子图2：处理后 (清除了孤立毛刺)
#     plt.subplot(2, 1, 2)
#     plt.plot(cleaned_signal, color='blue', alpha=0.7, label="Cleaned (Isolated Spikes Removed)")
#     plt.axhline(threshold, color='black', linestyle='--', label='+3 Sigma')
#     plt.axhline(-threshold, color='black', linestyle='--', label='-3 Sigma')
#     plt.title("After Smart Cleaning")
#     plt.legend(loc="upper right")
    
#     plt.tight_layout() # 自动调整间距
#     plt.show()         # 弹出图像窗口


#######################################
# 仅进行零化均值
import numpy as np
from lazy_reader import lazy_read_signal
from numpy_test import calculate_global_stats 

def zero_mean(file_path, global_mean):
    data_generator = lazy_read_signal(file_path,100000)
    for data_piece in data_generator:
        merge_data = ' '.join(data_piece)
        signal_array = np.fromstring(merge_data,dtype=np.float32,sep=' ')
        zero_mean_array = signal_array - global_mean
        yield zero_mean_array

if __name__ == "__main__":
    test_file_path = "/Volumes/LKs' disk/中海油能源发展装备公司海上油气管道含砂监测技术应用研究/结题资料/现场数据/2022523928.txt"
    file_zero_array = []
    final_max, final_min, final_mean, final_sigma = calculate_global_stats(test_file_path)
    data_generator_file = zero_mean(test_file_path, final_mean)
    # for data_pieces in data_generator_file:
    #     file_zero_array.append(data_pieces)

    # final_processed_signal = np.concatenate(file_zero_array)
    # print(f"零化均值已完成，本文件共有{len(file_zero_array)}个分块")
    # print(f"零化均值已完成，本文件共有{np.size(final_processed_signal)}个元素")

    total_elements = 0 # 定义一个计数器
    data_generator_file = zero_mean(test_file_path, final_mean)
    
    for data_pieces in data_generator_file:
        # file_zero_array.append(data_pieces) # 不要攒着！
        total_elements += data_pieces.size    # 读到一块，就把这一块的大小加进总数
        
    print(f"处理完成，总计数据点: {total_elements}")