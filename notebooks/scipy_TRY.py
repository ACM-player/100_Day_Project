# 这是一个使用了 yield 的函数（在 Python 里它有个高大上的名字，叫“生成器”）
def magic_box():
    print("准备变出第一个苹果...")
    yield "🍎 苹果"
    
    print("准备变出第二个香蕉...")
    yield "🍌 香蕉"
    
    print("准备变出第三个西瓜...")
    yield "🍉 西瓜"

# 1. 把盒子拿过来（此时函数并没有真正运行，只是做好了准备）
box = magic_box()

# 2. 我们用 for 循环来向盒子要东西（就像你在项目代码里写的那样）
for fruit in box:
    print(f"我拿到了：{fruit}")
    print("--- 休息一下 ---")