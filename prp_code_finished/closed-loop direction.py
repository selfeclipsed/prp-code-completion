import cv2
import cv2.aruco as aruco
import numpy as np
import math
import time

# 配置socket
import socket
client = socket.socket()
ip_port = ('192.168.1.110', 8888)
client.connect(ip_port)


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

        # 计算方向向量
        direction_vector = (corners[i][0][1] - corners[i][0][0]) / np.linalg.norm(corners[i][0][1] - corners[i][0][0])
        cv2.putText(output_image_resized, f"Direction: {direction_vector}", (center_x, center_y + 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        # 循环的条件在每次迭代时重新计算
        if abs(direction_vector[0] - 1) > 0.015:
            #写入命令
            f=open('C:/python programs/test.txt','w')
            f.writelines('1')
            f.close()
            if direction_vector[1] > 0:
                datamanip = '2 0'
                print('2')
            else:
                datamanip = '8 0'
                print('8') 
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
    direction_vector=[1,0]
