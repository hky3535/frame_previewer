# frame_previewer

## 程序介绍
* 程序会创建一个网页，用户可以通过post请求将图像发送至该网页，便可以实时预览图像

## docker使用方式
### 一键部署
```bash
git clone https://github.com/hky3535/frame_previewer.git && cd frame_previewer && docker build -t frame_previewer:latest . && docker run -itd --name frame_previewer -p 60005:30000 --restart always --privileged frame_previewer:latest
```
* 可以使用docker logs frame_previewer查看初始化进度，等待所有初始化库安装完成即可开始运行
### 分解部署
```bash
git clone https://github.com/hky3535/frame_previewer.git
cd frame_previewer
docker build -t frame_previewer:latest .
docker run -itd --name frame_previewer -p 60005:30000 --restart always --privileged frame_previewer:latest
```
* 可以使用docker logs frame_previewer查看初始化进度，等待所有初始化库安装完成即可开始运行
### 访问http://0.0.0.0:60005进入网站在线预览post上去的图片
### 使用POST请求http://0.0.0.0:60005发送图片（发送方法详见client_examples示例）

## 客户端示例
* 容器内通过nginx将http服务器的30001端口，和websocket的30002端口绑定至30000端口
* 容器启动后可以在其他程序中，通过post的方式实时在网页中刷新图像
* 目前示例中含有三种客户端
### python的opencv方法
```python
def http_show(cv2_frame, url):
    # 输入cv2格式图像，直接就能在url目标服务器网页上播放
    _, buffer = cv2.imencode('.jpg', cv2_frame)
    bytes_frame = buffer.tobytes()      # 转为比特流

    headers = {"Content-Type": "application/octet-stream"}
    res = requests.post(url, headers=headers, data=bytes_frame)     # 发送到网页服务器
url = "http://192.168.1.10:60005"
```
* 程序等价为cv2中的imshow函数，输入cv2格式的图像即可发送至http前端进行预览
* 视频播放同理，直接代替imshow函数进行播放
### C++的opencv方法
```c++
void http_show(cv::Mat cv2_frame, std::string ip_address, int port) {
    /*读取并处理mat图像*/
    std::vector<uchar> buffer;
    cv::imencode(".jpg", cv2_frame, buffer);

    /*启动socket连接模拟post请求*/
    int sock = socket(AF_INET, SOCK_STREAM, 0); if (sock < 0) {return;}

    struct sockaddr_in server_address{};
    server_address.sin_family = AF_INET;
    server_address.sin_addr.s_addr = inet_addr(ip_address);
    server_address.sin_port = htons(port);

    if (connect(sock, (struct sockaddr *)&server_address, sizeof(server_address)) < 0) {return;}

    /*构造post请求体*/
    std::string request;
    request += "POST / HTTP/1.1\r\n";
    request += "Host: 127.0.0.1\r\n";
    request += "Content-Type: image/jpeg\r\n";
    request += "Content-Length: " + std::to_string(buffer.size()) + "\r\n\r\n";
    request += std::string(buffer.begin(), buffer.end());

    /*发送请求并接收回复*/
    if (send(sock, request.c_str(), request.size(), 0) != request.size()) {return;}
    char response[1024] = {0};
    if (recv(sock, response, sizeof(response), 0) < 0) {return;}

    /*关闭并结束socket连接*/
    close(sock);
    return;
}
std::string ip_address = "192.168.1.10";
int port = 60005;
```
* 与以上python方法一致，可以取代imshow函数
* 为了避免引入过多库（尤其是交叉编译的时候）使用了socket套接字模拟post请求，当然也可以用cpr、curl之类的库代替
### linux shell方法
```shell
#!/bin/bash
frame_path="test.jpg"
url="http://192.168.1.10:60005"  # 发送POST请求
headers="Content-Type: application/octet-stream"
curl -X POST -H "$headers" --data-binary "@$frame_path" "$url"
```
* 程序读取一个jpg文件并通过curl发送
