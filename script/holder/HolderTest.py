import psutil
import pygetwindow as gw

# 获取所有正在运行的进程
processes = psutil.process_iter()

# 遍历每个进程并打印PID
for process in processes:
    try:
        pid = process.pid
        # 获取窗口标题
        window_titles = gw.getAllTitles()
    except  Exception as e:
        # print(process.pid,process.name())
        continue
