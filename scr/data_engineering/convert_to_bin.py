# import numpy as np
# import os
# # 导入你前几天的核心模块
# from path_scanner import scan_signal_files
# from numpy_test import calculate_global_stats
# from zero_mean import zero_mean

# def run_streaming_conversion(source_folder, output_folder,file_types):
#     """
#     高兼容性流式转换脚本
#     1. 为每个 .txt 生成独立的 .bin
#     2. 即使单文件巨大也能流式处理，不使用 np.concatenate
#     """
#     # 1. 扫描所有待处理文件
#     file_list = scan_signal_files(source_folder, file_types)
    
#     if not os.path.exists(output_folder):
#         os.makedirs(output_folder)
#         print(f"✅ 已创建输出仓库: {output_folder}")

#     print(f"🚀 开始转换任务，共计 {len(file_list)} 个文件...")

#     for file_path in file_list:
#         # 获取文件名（不含路径），并构建对应的 .bin 路径
#         base_name = os.path.basename(file_path)
#         output_name = base_name.replace(".txt", ".bin")
#         save_path = os.path.join(output_folder, output_name)
        
#         print(f"--------------------------------------------------")
#         print(f"正在处理文件: {base_name}")
        
#         # 2. 优雅获取全局均值（使用 _ 丢弃不需要的统计量）
#         # 这里的 calculate_global_stats 内部也是流式的，不会崩内存
#         _, _, f_mean, _ = calculate_global_stats(file_path)
        
#         # 3. 开启零均值化生成器
#         data_gen = zero_mean(file_path, f_mean)
        
#         # 4. 【核心逻辑】流式追加写入
#         # 使用 'wb' (Write Binary) 模式
#         # 单个文件内部循环写，内存中只保存当前的 chunk
#         with open(save_path, 'wb') as bin_file:
#             chunk_count = 0
#             for chunk in data_gen:
#                 # 直接将 NumPy 的比特流刷入硬盘，不进行任何中间累积
#                 chunk.tofile(bin_file)
#                 chunk_count += 1
        
#         print(f"💾 转换完成，已存入: {output_name} (分 {chunk_count} 次写入完成)")

# if __name__ == "__main__":
#     # 路径建议使用绝对路径
#     SRC_DIR = "/Volumes/LKs' disk/中海油能源发展装备公司海上油气管道含砂监测技术应用研究/结题资料/现场数据"
#     OUT_DIR = "/Users/lk/XJTU_Research/Code_Playground/100_Day_Project/outputs"
    
#     run_streaming_conversion(SRC_DIR, OUT_DIR, "*.txt")

#######################################

import numpy as np
import os
from tqdm import tqdm  # 🌟 引入进度条神器

from path_scanner import scan_signal_files
from numpy_test import calculate_global_stats
from zero_mean import zero_mean

def run_streaming_conversion(source_folder, output_folder, file_types):
    file_list = scan_signal_files(source_folder, file_types)
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"✅ 已创建输出仓库: {output_folder}")

    # print(f"🚀 开始转换任务，共计 {len(file_list)} 个文件...")

    # 🌟 魔法在这里！用 tqdm() 把 file_list 包裹起来
    # desc="转换进度" 会显示在进度条最前面
    for file_path in tqdm(file_list, desc="二进制转换进度"):
        base_name = os.path.basename(file_path)
        output_name = base_name.replace(".txt", ".bin")
        save_path = os.path.join(output_folder, output_name)
        
        # ⚠️ 注意：使用进度条时，把循环里那些繁琐的 print 都注释掉！
        # 否则它们会把进度条冲乱。让 tqdm 安静地表演即可。
        
        _, _, f_mean, _ = calculate_global_stats(file_path)
        data_gen = zero_mean(file_path, f_mean)
        
        with open(save_path, 'wb') as bin_file:
            for chunk in data_gen:
                chunk.tofile(bin_file)

if __name__ == "__main__":
    SRC_DIR = "/Volumes/LKs' disk/中海油能源发展装备公司海上油气管道含砂监测技术应用研究/结题资料/现场数据"
    OUT_DIR = "/Users/lk/XJTU_Research/Code_Playground/100_Day_Project/outputs"
    
    run_streaming_conversion(SRC_DIR, OUT_DIR, "*.txt")