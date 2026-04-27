# import numpy as np
# # 导入昨天写好的读取函数（确保昨天的文件名是 lazy_reader.py）
# from lazy_reader import lazy_read_signal

# if __name__ == "__main__":
#     # 你的 Mac 外接硬盘绝对路径
#     test_file_path = "/Volumes/LKs' disk/中海油能源发展装备公司海上油气管道含砂监测技术应用研究/结题资料/现场数据/2022523928.txt"
    
#     print("开始初始化生成器...")
#     # 调用昨天的函数，每次读 700 行作为一块
#     signal_generator = lazy_read_signal(test_file_path, chunk_size=700)
    
#     # 我们先只拿第一块数据（700行）来做 NumPy 测试
#     # next() 的作用是让生成器吐出一次数据然后暂停
#     first_chunk_text = next(signal_generator) 
    
#     print("正在进行 NumPy 数组转换...")
#     # 步骤1：因为每行有很多用空格隔开的数字，我们先把这 700 行文本用空格粘成一个超长的字符串
#     merged_text = " ".join(first_chunk_text)
    
#     # 步骤2：利用 np.fromstring 瞬间把纯文本转化为 float32 精度的高效数组！
#     signal_array = np.fromstring(merged_text, dtype=np.float32, sep=' ')
    
#     print(f"转换成功！当前 NumPy 数组里共有 {signal_array.shape} 个数字。")
#     print(f"数据类型为: {signal_array.dtype}")
#     print("-" * 40)
    
#     # 步骤3：零原生 for 循环的高速极值统计（向量化计算）
#     print("开始向量化极值计算...")
#     max_val = np.max(signal_array)
#     min_val = np.min(signal_array)
#     mean_val = np.mean(signal_array)
    
#     print(f"最大值: {max_val}")
#     print(f"最小值: {min_val}")
#     print(f"均值: {mean_val:.6f}")
#     print("-" * 40)
#     print("第三天任务完美通过！没有使用任何一个 for 循环！")



#######################################

# import numpy as np
# from lazy_reader import lazy_read_signal

# if __name__ == "__main__":
#     test_file_path = "/Volumes/LKs' disk/中海油能源发展装备公司海上油气管道含砂监测技术应用研究/结题资料/现场数据/2022523928.txt"
#     print(" 开始将分块列表转化为numpy数组")
#     data_chunk_generator = lazy_read_signal(test_file_path)
#     data_chunks = next(data_chunk_generator)
#     contdata_string_merge = " ".join(data_chunks)
#     numpy_data = np.fromstring(contdata_string_merge, dtype=np.float32, sep=' ')#这一句的参数记不住，是直接复制粘贴过来的
#     print("接下来测试这个numpy的维数")
#     print(f"这个切片一共有{numpy_data.shape}个数据")
#     print(f"其中最大值为{np.max(numpy_data)}，最小值为{np.min(numpy_data)}，平均值为{np.mean(numpy_data)}")



#######################################
# import numpy as np
# from lazy_reader import lazy_read_signal

# if __name__ == "__main__":
#     test_file_path = "/Volumes/LKs' disk/中海油能源发展装备公司海上油气管道含砂监测技术应用研究/结题资料/现场数据/2022523928.txt"
#     max_min_mean = [-np.inf, np.inf]
#     total_count = 0
#     size_count = 0
#     data_generator = lazy_read_signal(test_file_path)
#     for data_piece in data_generator:
#         merge_data = ' '.join(data_piece)
#         numpy_data = np.fromstring(merge_data, dtype=np.float32, sep=' ')
#         numpy_data_size = numpy_data.shape
#         piece_max = np.max(numpy_data)
#         piece_min = np.min(numpy_data)
#         if max_min_mean[0] < piece_max:
#             max_min_mean[0] = piece_max
#         if max_min_mean[1] > piece_min:
#             max_min_mean[1] = piece_min
#         total_count  = total_count + np.sum(numpy_data)
#         size_count = size_count + numpy_data_size[0]
#     total_mean = total_count / size_count
#     max_min_mean.append(total_mean)
#     print(f"整个文件最大值是{max_min_mean[0]}，最小值是{max_min_mean[1]}，平均值是{max_min_mean[2]}")

#######################################
#######################################
import numpy as np
# 导入昨天写好的分块读取函数
from lazy_reader import lazy_read_signal

# 【工程准则 1：函数化封装】
# 不要把所有的逻辑都堆在 if __name__ == "__main__": 里面。
# 将其封装成一个独立的功能函数，这样未来你可以直接循环遍历63个文件调用它。
def calculate_global_stats(file_path):
    """
    流式读取大文件，并计算全局最大值、最小值和平均值
    """
    # 【工程准则 2：语义化命名】
    # 抛弃 max_min_mean 这种“混合用途”的列表。
    # 建立四个独立的、名字一看就懂的变量，这在团队协作中极其重要。
    global_max = -np.inf
    global_min = np.inf
    global_sum = 0.0
    global_count = 0
    global_sq_sum = 0.0
    
    data_generator = lazy_read_signal(file_path,700)
    
    for data_piece in data_generator:
        merge_data = ' '.join(data_piece)
        numpy_data = np.fromstring(merge_data, dtype=np.float32, sep=' ')
        
        # 【工程准则 3：剔除无效算力】
        # 在你原先的代码中，计算了 piece_mean = np.mean(numpy_data) 但却从未使用。
        # 在几千万行的数据处理中，任何多余的运算都会拖慢整体速度，必须果断删掉。
        piece_max = np.max(numpy_data)
        piece_min = np.min(numpy_data)
        piece_sq_sum = np.sum(numpy_data ** 2) 
        
        # 【工程准则 4：利用内置函数替代繁琐的 if 判断】
        # 使用 Python 原生的 max() 和 min()，代码更加“Pythonic（优雅）”。
        global_max = max(global_max, piece_max)
        global_min = min(global_min, piece_min)
        
        # 累加总和与总数据点数
        global_sum += np.sum(numpy_data)
        global_count += numpy_data.size  # 使用 .size 直接获取总个数，比 .shape 更直观
        global_sq_sum += piece_sq_sum
        
    # 【工程准则 5：防御性编程】
    # 防止万一读到了一个空文件，导致 global_count 为 0 触发“除以零 (ZeroDivisionError)”崩溃。
    global_mean = global_sum / global_count if global_count > 0 else 0.0
    global_sq_mean = global_sq_sum / global_count if global_count > 0 else 0.0
    global_sigma_sq = max(0, global_sq_mean - (global_mean ** 2)) #\sigma^2 = E(x^2)-(E(X))^2
    global_sigma = np.sqrt(global_sigma_sq)
    # 返回三个清晰的结果
    return global_max, global_min, global_mean, global_sigma


# --- 主程序测试入口 ---
if __name__ == "__main__":
    test_file_path = "/Volumes/LKs' disk/中海油能源发展装备公司海上油气管道含砂监测技术应用研究/结题资料/现场数据/2022523928.txt"
    
    print(f"正在分析文件: {test_file_path}")
    print("这可能需要几秒钟，请稍候...")
    
    # 优雅地接收函数返回的三个值
    final_max, final_min, final_mean, final_sigma = calculate_global_stats(test_file_path)
    
    print("-" * 40)
    print(f"分析完成！")
    print(f"📈 极值上限 (Max): {final_max}")
    print(f"📉 极值下限 (Min): {final_min}")
    print(f"🎯 全局均值 (Mean): {final_mean:.6f}")
    print("-" * 40)