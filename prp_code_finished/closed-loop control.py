import cv2
import cv2.aruco as aruco
import numpy as np
import math
import time
import sys

# 配置socket
import socket
client = socket.socket()
ip_port = ('192.168.1.110', 8888)
client.connect(ip_port)

file_path = "C:/opencv/files/manip.txt"  # 替换为你的文件路径

# 读取txt文件中的内容
with open(file_path, 'r') as file:
    content = file.read()

# 将字符串分割成坐标对
points_str = content.strip().split()
points_list = [point.split(',') for point in points_str]

# 将坐标对转换为嵌套列表
path = [[int(coord) for coord in point] for point in points_list]

# 获取当前运行次数
current_run = int(sys.argv[1]) if len(sys.argv) > 1 else 1

# 输出对应次数的元素
if 1 <= current_run <= len(path):
    location=path[current_run]
print(location)

# 创建空白图像，用于输出
output_size = (800, 600, 3)
output_image = np.zeros(output_size, dtype=np.uint8)

h = 800
w = 600
# 四个待选取的点坐标
src_points = np.float32([[125, 50], [645, 15], [170, 410], [635, 400]])
dst_points = np.float32([[0.0, 0.0], [w, 0.0], [0.0, h], [w, h]])


# 初始化摄像头
cap = cv2.VideoCapture(1)

# 设置 ArUco 字典
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)

# 创建 ArUco 参数
parameters = cv2.aruco.DetectorParameters_create()
 
# 读取摄像头帧
ret, frame = cap.read()
    
matrix = cv2.getPerspectiveTransform(src_points, dst_points)
    
warped_image = cv2.warpPerspective(frame, matrix, (w, h))

# 将仿射变换后的图像复制到输出图像中
output_image[:warped_image.shape[0], :warped_image.shape[1]] = warped_image

# 调整输出图像的大小
output_image_resized = cv2.resize(output_image, (800, 600))
    
gray = cv2.cvtColor(output_image_resized, cv2.COLOR_BGR2GRAY)

# 检测 ArUco 标记
corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

# 在图像上绘制检测到的标记
if ids is not None:
    for i in range(len(ids)):
        # 获取标记的中心坐标
        center_x = int(np.mean(corners[i][0][:, 0])) - 20
        center_y = int(np.mean(corners[i][0][:, 1]))

        # 在图像上绘制中心点
        cv2.circle(output_image_resized, (center_x, center_y), 5, (0, 255, 0), -1)

        # 在图像上显示坐标信息
        cv2.putText(output_image_resized, f"Center: ({center_x}, {center_y})", (center_x, center_y - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
else:
    center_x=550
    center_y=550
    direction_vector=[1,0]
    # 在图像上绘制中心点
    cv2.circle(output_image_resized, (center_x, center_y), 5, (0, 255, 0), -1)

    # 在图像上显示坐标信息
    cv2.putText(output_image_resized, f"Center: ({center_x}, {center_y})", (center_x, center_y - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    cv2.putText(output_image_resized, f"Direction: {direction_vector}", (center_x, center_y + 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
while True:
    
    # 读取摄像头帧
    ret, frame = cap.read()
    print("get new frame")
    matrix = cv2.getPerspectiveTransform(src_points, dst_points)
    
    warped_image = cv2.warpPerspective(frame, matrix, (w, h))

    # 将仿射变换后的图像复制到输出图像中
    output_image[:warped_image.shape[0], :warped_image.shape[1]] = warped_image

    # 调整输出图像的大小
    output_image_resized = cv2.resize(output_image, (800, 600))
    
    gray = cv2.cvtColor(output_image_resized, cv2.COLOR_BGR2GRAY)

    # 检测 ArUco 标记
    corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    # 在图像上绘制检测到的标记
    if ids is not None:
        cv2.aruco.drawDetectedMarkers(output_image_resized, corners)
        for i in range(len(ids)):
            # 获取标记的中心坐标
            center_x = int(np.mean(corners[i][0][:, 0])) - 20
            center_y = int(np.mean(corners[i][0][:, 1]))

            # 在图像上绘制中心点
            cv2.circle(output_image_resized, (center_x, center_y), 5, (0, 255, 0), -1)

            # 在图像上显示坐标信息
            cv2.putText(output_image_resized, f"Center: ({center_x}, {center_y})", (center_x, center_y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            print(f"Center: ({center_x}, {center_y})")

        # 循环的条件在每次迭代时重新计算
        if abs(center_x - location[0]) > 25 or abs(center_y - location[1]) > 25:
            #写入命令
            f=open('C:/python programs/test.txt','w')
            f.writelines('1')
            f.close()
            if abs(center_x - location[0]) > abs(center_y - location[1]):
                if center_x - location[0] < 0:
                    datamanip = '5 0'
                    print('5')
                else:
                    datamanip = '1 0'
                    print('1')
            else:
                if center_y - location[1] < 0:
                    datamanip = '3 0'
                    print('3')
                else:
                    datamanip = '7 0'
                    print('7')
            # 发送命令
            client.setblocking(False)
            msg_input = datamanip
            client.send(msg_input.encode())
            send_result = client.send(msg_input.encode())
            break
        else:
            datamanip = '0'
            print('0')
            #写入命令
            f=open('C:/python programs/test.txt','w')
            f.writelines('0')
            f.close()
            client.setblocking(False)
            msg_input = datamanip
            client.send(msg_input.encode())
            send_result = client.send(msg_input.encode())
            break
    else:
        center_x=location[0]
        center_y=location[1]
        direction_vector=[1,0]
        # 在图像上绘制中心点
        cv2.circle(output_image_resized, (center_x, center_y), 5, (0, 255, 0), -1)

        # 在图像上显示坐标信息
        cv2.putText(output_image_resized, f"Center: ({center_x}, {center_y})", (center_x, center_y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.putText(output_image_resized, f"Direction: {direction_vector}", (center_x, center_y + 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)