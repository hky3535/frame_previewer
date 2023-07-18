# frame_previewer

## 程序介绍
* 程序会创建一个网页，用户可以通过post请求将图像发送至该网页，便可以实时预览图像

## 程序运行
* 在main.py中设定程序的两个端口，http端口为实际网页服务和post服务端口，ws端口为前后端通信端口
* ws端口如果发生改变，请在utils/index.html中同样更改ws端口
> 注：如果使用docker进行运行，则需要docker中同事开放映射这两个端口，且html中需要填写最终映射到物理机上的端口  
> 例：docker run --name test -p 50001:8888 -p 50002:8889 ubuntu:latest  
> 这种情况下，main.py中需要将html端口设置为8888，ws端口设置为8889，而html中需要设置端口为50002，网页访问也需要使用0.0.0.0:50001访问（因为最终是在物理机上进行html网页访问）  

## 客户端示例
* 当服务器html和ws部署完成后，便可以在其他程序中，通过post的方式实时在网页中预览图像
* 目前示例中含有两种客户端
### python的opencv方法
```python
def http_show(cv2_frame, url):
    _, buffer = cv2.imencode('.jpg', cv2_frame)
    bytes_frame = buffer.tobytes()      # 转为比特流

    headers = {"Content-Type": "application/octet-stream"}
    res = requests.post(url, headers=headers, data=bytes_frame)     # 发送到网页服务器
```
* 程序等价为cv2中的imshow函数，输入cv2格式的图像即可发送大http前端
* 所以可以近似播放视频
### linux shell方法
```shell
#!/bin/bash
frame_path="source/test.jpg"
url="http://0.0.0.0:50001"  # 发送POST请求
headers="Content-Type: application/octet-stream"
curl -X POST -H "$headers" --data-binary "@$frame_path" "$url"
```
* 程序读取一个jpg文件并通过curl发送
