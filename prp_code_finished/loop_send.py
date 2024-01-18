import subprocess
import time

current_run = 1
adjust_time = 0

def run_another_script1():
    try:
        # 在这里替换成你想要运行的脚本的路径
        script_path = 'C:/python programs/closed-loop direction.py'
        
        # 使用subprocess运行脚本
        subprocess.run(['python', script_path])
    except Exception as e:
        print(f"Error running script: {e}")

def run_another_script2():
    try:
        # 在这里替换成你想要运行的脚本的路径
        script_path = 'C:/python programs/closed-loop control.py'
        
        # 使用subprocess运行脚本
        subprocess.run(['python', script_path ,str(current_run)])
    except Exception as e:
        print(f"Error running script: {e}")

# 循环运行的次数，可以根据需要更改
num_runs = 1000

# 循环
for i in range(num_runs):
    
    adjust_time+=1
    flag1=False
    flag2=False

    print(f"Running script iteration {i + 1}")
    
    # 调用运行另一个脚本的函数
    run_another_script1()
    
    # 检测状态
    f=open('C:/python programs/test.txt','r')
    if(f.read()=='0') :
        flag1=True
    f.close()
    
    
    # 调用运行另一个脚本的函数
    run_another_script2()
    
    # 检测状态
    f=open('C:/python programs/test.txt','r')
    if(f.read()=='0') :
        flag2=True
    f.close()
    

    # 判断是否需要进入下一个点
    if((flag1==True and flag2==True) or adjust_time > 10):
        current_run += 1
        adjust_time=0