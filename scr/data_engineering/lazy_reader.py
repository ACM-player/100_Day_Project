# import os

# def lazy_read_signal(file_path, chunk_size=400000):
#     """
#     分块读取大文件，每次只返回 chunk_size 行数据（默认 40万行，即1秒数据）
#     """
#     print(f"准备打开水龙头，开始读取: {file_path}")
    
#     # 知识点 1：with open 上下文管理器（全自动安全水龙头）
#     with open(file_path, 'r', encoding='utf-8') as file:
        
#         # 准备一个小水桶，用来装这 40 万行数据
#         chunk_data = []
        
#         # 开始一行一行地接水
#         for line in file:
#             # 把每一行开头和结尾的空白字符去掉，放进小水桶
#             chunk_data.append(line.strip())
            
#             # 如果小水桶装满了 40 万行
#             if len(chunk_data) == chunk_size:
#                 # 知识点 2：yield 关键字（智能流水线暂停键）
#                 # 把装满水的小水桶交出去，然后在这里“暂停”
#                 yield chunk_data
                
#                 # 等主程序处理完上一桶水后，代码从这里“苏醒”
#                 # 清空小水桶，准备接下一桶 40 万行的数据
#                 chunk_data = []
        
#         # 知识点 3：收尾工作
#         # 文件读到最后，可能剩下不足 40 万行的数据，也要交出去
#         if len(chunk_data) > 0:
#             yield chunk_data

# # --- 主程序入口 ---
# if __name__ == "__main__":
#     # 使用你刚才上传的测试数据文件
#     test_file_path = "/Volumes/LKs' disk/中海油能源发展装备公司海上油气管道含砂监测技术应用研究/结题资料/现场数据/2022523928.txt"
    
#     # 确保文件存在再运行
#     if os.path.exists(test_file_path):
#         # 创建生成器（此时还没有真正开始读文件）
#         signal_generator = lazy_read_signal(test_file_path)
        
#         print("-" * 40)
#         chunk_count = 0
        
#         # 主程序的流水线：每次从生成器里要一桶 40 万行的数据
#         for data_chunk in signal_generator:
#             chunk_count += 1
#             print(f"成功读取第 {chunk_count} 块数据，本块包含 {len(data_chunk)} 行 [维度检查通过]")
            
#             # 这里你可以打印前3行看看长什么样，验证数据没读错
#             if chunk_count == 1:
#                 print("第一块的前 3 行数据长这样：")
#                 for i in range(3):
#                     print(f"  {data_chunk[i]}")
#                 print("-" * 40)
                
#         print(f"全部读取完毕！总共切分了 {chunk_count} 块。你的内存安全保住了！")
#     else:
#         print(f"找不到文件 {test_file_path}，请检查路径是否正确。")


########################################
########################################

# import os
# def lazy_read_signal(file_path, chunk_size):
#     print("准备开始持续分块读取数据:")
#     with open(file_path,'r',encoding='utf-8') as file:
#         file_chunk = []
#         chunk_count = 0
#         for file_piece in file:
#             file_chunk.append(file_piece.strip())
#             chunk_count += 1
#             if len(file_chunk) == chunk_size:
#                 yield file_chunk
#                 file_chunk = []
#         if len(file_chunk) > 0:
#             yield file_chunk

# if __name__ == "__main__":
#     test_file_path = "/Volumes/LKs' disk/中海油能源发展装备公司海上油气管道含砂监测技术应用研究/结题资料/现场数据/2022523928.txt"
#     if os.path.exists(test_file_path):
#         test_file_generator = lazy_read_signal(test_file_path,700)
#         pieces_num = 0
#         for chunks in test_file_generator:
#             pieces_num += 1
#             print(f"第{pieces_num}块数据已读取，此块包括{len(chunks)}行数据")
#             if pieces_num == 1:
#                 for line in range(2):
#                     print(chunks[line])
#         print(f"数据已读取完毕，共分{pieces_num}块读完")
#     else:
#         print("路径有误，请重新检查路径文件是否存在")


#######################################
#######################################

import os

def lazy_read_signal(file_path, chunk_size=700):
    """
    带有内置路径检查的生成器函数
    """
    # 1. 封装在内部的路径检查：如果不满足条件，直接拉响警报！
    if not os.path.exists(file_path):
        # raise 关键字会立刻中止函数，并向上层（主程序）抛出一个错误对象
        raise FileNotFoundError(f"🚨 内部警报：你要找的文件 '{file_path}' 根本不存在！")
        
    print(f"✅ 路径检查通过，准备开始读取: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as file:
        file_chunk = []
        for file_piece in file:
            file_chunk.append(file_piece.strip())
            
            if len(file_chunk) == chunk_size:
                yield file_chunk
                file_chunk = []
                
        if len(file_chunk) > 0:
            yield file_chunk

# --- 主程序（包工头） ---
if __name__ == "__main__":
    # 💡 你可以尝试修改下面这个路径，比如在末尾加个 "123"，故意让它变成错误路径来测试报错
    test_file_path = "/Volumes/LKs' disk/中海油能源发展装备公司海上油气管道含砂监测技术应用研究/结题资料/现场数据/20225239289.txt"
    
    # 2. 包工头的防御机制：try...except
    try:
        # 尝试派工人去干活
        test_file_generator = lazy_read_signal(test_file_path, 700)
        pieces_num = 0
        
        # 注意：生成器内部的代码，直到这个 for 循环第一次执行 next() 时才会真正跑起来
        for chunks in test_file_generator:
            pieces_num += 1
            print(f"第 {pieces_num} 块数据已读取，此块包括 {len(chunks)} 行数据")
            
            if pieces_num == 1:
                print("--- 前两行数据展示 ---")
                for line in range(2):
                    print(chunks[line])
                print("-" * 20)
                
        print(f"🎉 数据已全部读取完毕，共分 {pieces_num} 块读完。")

    # 3. 如果工人在干活时拉响了 FileNotFoundError 警报，就会被这里拦截
    except FileNotFoundError as error_message:
        print("⚠️ 主程序捕获到了异常：")
        # 打印出工人在 raise 时喊出的那句警报语
        print(error_message)
        print("🔧 请检查你的硬盘有没有插好，或者路径拼写是否正确。")