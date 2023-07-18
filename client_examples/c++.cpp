#include <iostream>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <string.h>
#include <unistd.h>

#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>

/*
安装：
apt install g++
apt install libopencv-dev
编译语句：
g++ -o c++ c++.cpp -I /usr/include/opencv4 -L /usr/lib -lopencv_core -lopencv_highgui -lopencv_imgcodecs
*/

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

int main() {
    cv::Mat cv2_frame = cv::imread("source/test.jpg");
    http_show(cv2_frame, "0.0.0.0", 50001);
}