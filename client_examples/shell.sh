#!/bin/bash

# 读取图像
frame_path="test.jpg"
url="http://192.168.1.10:60005"  # 发送POST请求
headers="Content-Type: application/octet-stream"
curl -X POST -H "$headers" --data-binary "@$frame_path" "$url"

# 读取视频（暂时不能用）
# video_path="test.mp4"
# url="http://192.168.1.10:60005"  # 发送POST请求
# headers="Content-Type: application/octet-stream"
# ffmpeg -i /root/repo/frame_previewer/client_examples/source/test.mp4 -vf "select=eq(n\,0)" -f image2pipe -pix_fmt rgb24 -vcodec rawvideo - | while read -r line; do
#    # 将图像转换为比特流，并使用curl发送
#    echo "$line" | curl -X POST -H "Content-Type: application/octet-stream" --data-binary @- "$url"
#    sleep 0.1
# done
