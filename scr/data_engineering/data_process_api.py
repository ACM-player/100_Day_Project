import os
import glob
import numpy as np
from tqdm import tqdm

class AcousticPreprocessor:
    """
    声发射数据预处理类：负责从原始数据到标准化 BIN 的转换
    """
    
    def __init__(self, raw_dir, output_dir, fs=44100):
        # 机器出厂设置，这里不用改
        self.raw_dir = raw_dir
        self.output_dir = output_dir
        self.fs = fs
        self.file_list = [] 
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def scan_files(self, extension="*.txt"):
        """
        扫描指定文件夹下的所有原始文件
        """
        print(f"正在扫描 {self.raw_dir} 下的 {extension} 文件...")
        
        # >>>>>>>>>> 【第 1 天任务：路径扫描】 开始填空 >>>>>>>>>>
        # 提示：在这里把你第一天用 glob 或 os.walk 获取文件列表的代码贴过来。
        # 你的终极目标是：把你找到的所有文件路径的列表，赋值给 self.file_list 这个变量。
        search_pattern = os.path.join(self.raw_dir,'**',extension)
        relative_paths = glob.glob(search_pattern,recursive=True)
        abs_paths = []
        for i in relative_paths:
            abs_path = os.path.abspath(i)
            abs_paths.append(abs_path)
        self.file_list = abs_paths
        
        print("所有文件路径已经保存在self.file_list属性下")
        
        # <<<<<<<<<< 【第 1 天任务：路径扫描】 结束填空 <<<<<<<<<<
        
        print(f"共扫描到 {len(self.file_list)} 个文件。")

    def _get_basic_info(self, data_array):
        """
        计算单条数据的基本统计信息
        注意：这里的 data_array 应该已经是 numpy 数组类型了，不用再做字符串转换。
        """
        # Numpy 直接一步到位算出极值、均值和标准差
        array_max = np.max(data_array)
        array_min = np.min(data_array)
        array_mean = np.mean(data_array)
        array_std = np.std(data_array) # 直接替代你那 4 行硬核推导！

        # 💡 工程小建议：返回字典比返回四个孤零零的数字更好
        # 这样以后调用的时候就知道哪个数字对应什么特征，比如 info['mean']
        return {
            "max": array_max,
            "min": array_min,
            "mean": array_mean,
            "std": array_std
        }

    # ==========================================
    # 你的杰作：懒加载齿轮 (变成了私有方法)
    # ==========================================
    def _lazy_read_signal(self, file_path, chunk_size=400000):
        """
        内部生成器：按块读取 TXT，包含路径防御机制
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"🚨 内部警报：文件 '{file_path}' 不存在！")
            
        with open(file_path, 'r', encoding='utf-8') as file:
            file_chunk = []
            for file_piece in file:
                file_chunk.append(file_piece.strip())
                
                if len(file_chunk) == chunk_size:
                    yield file_chunk  # 交出一桶数据 (字符串列表)
                    file_chunk = []
                    
            if len(file_chunk) > 0:
                yield file_chunk

    # ==========================================
    # 大总装：流水线调度中心
    # ==========================================
    def process_and_save(self, file_path):
        """
        核心流水线：懒加载 -> 格式转换 -> 零均值化 -> 存入 BIN
        """
        file_name = os.path.basename(file_path).replace(".txt", ".bin")
        save_path = os.path.join(self.output_dir, file_name)
        
        # 只要用 'wb' 打开输出文件，准备源源不断地写入
        with open(save_path, 'wb') as f_out:
            
            # 1. 启动你的“懒加载齿轮”！每次要 chunk_size 行数据
            # 注意前面加了 self. 来调用机器内部的方法
            # 1. 启动你的“懒加载齿轮”！每次要 chunk_size 行数据
            for str_chunk in self._lazy_read_signal(file_path, chunk_size=400000):
                
                # 2. 字符串转数组 (用你绝对稳妥的拼合切分法！)
                merge_data = ' '.join(str_chunk)
                chunk_array = np.fromstring(merge_data, dtype=np.float32, sep=' ')
                
                # 防呆：如果刚好读到空行，跳过
                if chunk_array.size == 0:
                    continue

                # 3. 递给你的“测量仪”算一下特征
                info = self._get_basic_info(chunk_array)

                # 4. 零均值化清洗
                clean_chunk = chunk_array - info['mean']

                # 5. 立刻存入硬盘
                clean_chunk.tofile(f_out)
                
        return save_path
    
    # def run_all(self):
    #     """
    #     一键启动方法 (这个不用改，直接用)
    #     """
    #     if not self.file_list:
    #         print("没有发现可处理的文件，请先检查路径或运行 scan_files()")
    #         return
            
    #     print("开始批量处理数据流水线...")
    #     for f in self.file_list:
    #         # 遍历列表里的每一个文件，塞进清洗流水线
    #         out = self.process_and_save(f)
    #         print(f"成功处理: {os.path.basename(f)} -> {os.path.basename(out)}")
    #     print("所有任务处理完毕！")

    def run_all(self):
        """
        一键启动方法 (加入 tqdm 进度条)
        """
        if not self.file_list:
            print("没有发现可处理的文件，请先检查路径或运行 scan_files()")
            return
            
        print(f"开始批量处理 {len(self.file_list)} 个文件...")
        
        # 使用 tqdm 包装你的文件列表，desc 是进度条前面的文字，unit 是单位
        for f in tqdm(self.file_list, desc="数据清洗转换中", unit="file"):
            # 遍历列表里的每一个文件，塞进清洗流水线
            out = self.process_and_save(f)
            
        print("\n🎉 所有任务处理完毕！")


# ==========================================
# 遥控器区域：实例化并运行你的机器
# ==========================================
if __name__ == "__main__":
    # 1. 设置输入和输出文件夹路径 (请替换为你自己的真实路径)
    # 注意：raw_dir 是包含你那些 txt 文件的文件夹
    INPUT_DIR = "/Volumes/LKs' disk/中海油能源发展装备公司海上油气管道含砂监测技术应用研究/结题资料/现场数据" 
    
    # 你希望把转换后的 bin 文件存在哪里？(文件夹不存在会自动创建)
    OUTPUT_DIR = "/Users/lk/XJTU_Research/Code_Playground/100_Day_Project/outputs" 

    # 2. 按下“出厂配置”按钮，造出这台机器
    processor = AcousticPreprocessor(raw_dir=INPUT_DIR, output_dir=OUTPUT_DIR, fs=44100)

    # 3. 按下“扫描文件”按钮
    processor.scan_files(extension="*.txt")

    # 4. 按下“全自动清洗转存”总开关！
    # 准备好看着控制台刷屏吧！
    processor.run_all()