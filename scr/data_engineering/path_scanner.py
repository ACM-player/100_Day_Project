# import os
# import glob

# def scan_signal_files(target_folder):
#     """
#     扫描目标文件夹下的所有 txt 信号文件，并返回绝对路径列表。
#     """
#     print(f"正在扫描文件夹: {target_folder} ...")
    
#     # 1. 跨平台拼接搜索模式：使用 os.path.join 避免手动输入斜杠
#     # 这等同于在文件夹内寻找 **/*.txt
#     search_pattern = os.path.join(target_folder, '**', '*.txt')
    
#     # 2. 使用 glob 递归寻找所有的 txt 文件
#     relative_paths = glob.glob(search_pattern, recursive=True)
    
#     # 3. 创建一个空列表，用来装转换后的绝对路径
#     absolute_paths = []
    
#     # 4. 用 for 循环处理每一个找到的相对路径
#     for rel_path in relative_paths:
#         # 核心：使用 os.path.abspath 将其转化为当前操作系统的绝对路径
#         abs_path = os.path.abspath(rel_path)
#         absolute_paths.append(abs_path)
        
#     return absolute_paths

# # --- 主程序开始 ---
# if __name__ == "__main__":
#     # 假设您的数据存放在当前目录下一个叫 "data" 的文件夹里
#     # 您可以把 "data" 替换成您实际存放 63 个 txt 文件的文件夹名字
#     folder_to_scan = "/Volumes/LKs' disk/中海油能源发展装备公司海上油气管道含砂监测技术应用研究/结题资料/现场数据" 
    
#     # 调用我们写好的函数
#     result_paths = scan_signal_files(folder_to_scan)
    
#     # 5. 在终端输出结构化的结果
#     print("-" * 30)
#     print(f"扫描完毕！共找到 {len(result_paths)} 个 txt 信号文件。")
#     print("-" * 30)
    
#     # 打印前 5 个绝对路径作为检查（避免终端输出太长）
#     for path in result_paths[:5]:
#         print(path)
#     if len(result_paths) > 5:
#         print("...... (省略显示剩余路径)")


############################################
# import os
# import glob

# def scan_signal_files(target_folder):
#     print(f"开始扫描{target_folder}")
#     search_pattern = os.path.join(target_folder,'**',"*.txt")
#     relative_paths = glob.glob(search_pattern,recursive=True)
#     abs_paths = []
#     for i in relative_paths:
#         abs_path = os.path.abspath(i)
#         abs_paths.append(abs_path)
#     return abs_paths

# if __name__ == "__main__":
#     scan_folder = "/Volumes/LKs' disk/中海油能源发展装备公司海上油气管道含砂监测技术应用研究/结题资料/现场数据"
#     results_path = scan_signal_files(scan_folder)
#     print(f"一共找到{len(results_path)}个文件")
#     for i in results_path[:7]:
#         print(i)
#     if len(results_path)>7:
#         print("仅显示7个文件")


##########################################
import os
import glob

def scan_signal_files(target_folder,file_type):
    print(f"开始扫描{target_folder}")
    search_pattern = os.path.join(target_folder,'**',file_type)
    relative_paths = glob.glob(search_pattern,recursive=True)
    abs_paths = []
    for i in relative_paths:
        abs_path = os.path.abspath(i)
        abs_paths.append(abs_path)
    return abs_paths

if __name__ == "__main__":
    scan_folder = "/Volumes/LKs' disk/中海油能源发展装备公司海上油气管道含砂监测技术应用研究/结题资料/现场数据"
    results_path = scan_signal_files(scan_folder,"*.txt")
    print(f"一共找到{len(results_path)}个文件")
    for i in results_path[:7]:
        print(i)
    if len(results_path)>7:
        print("仅显示7个文件")