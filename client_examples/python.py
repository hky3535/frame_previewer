"""
何恺悦 hekaiyue 2023-07-18
"""
import requests
import cv2
import time

# 示例函数
def http_show(cv2_frame, url):
    _, buffer = cv2.imencode('.jpg', cv2_frame)
    bytes_frame = buffer.tobytes()      # 转为比特流

    headers = {"Content-Type": "application/octet-stream"}
    res = requests.post(url, headers=headers, data=bytes_frame)     # 发送到网页服务器

"""
# http_show 效果上而言等同于 cv2.imshow

# 本地图片
cv2_frame = cv2.imread("source/test.jpg")
http_show(cv2_frame, "http://0.0.0.0:50001")

# 本地视频
cv2_video = cv2.VideoCapture("source/test.mp4")
while True:
    ret, cv2_frame = cv2_video.read()
    if not ret: break
    http_show(cv2_frame, "http://0.0.0.0:50001")
    time.sleep(0.1)

cv2_video.release()
"""