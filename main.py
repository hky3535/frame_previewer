"""
何恺悦 hekaiyue 2023-07-17
"""
from utils import basic
import threading
import time
import subprocess


class Main:
    def __init__(self):
        self.basic = basic.Basic()

    def main(self):
        # 启动HTTP服务器
        http_server_thread = threading.Thread(
            target=self.basic.index_html, 
            args=("0.0.0.0", 30001)
        )
        http_server_thread.start()

        # 启动ws服务器
        ws_server_thread = threading.Thread(
            target=self.basic.index_ws, 
            args=("0.0.0.0", 30002)
        )
        ws_server_thread.start()

        # 启动Nginx
        try:
            subprocess.check_call(['nginx', '-c', 'nginx.conf'])
        except subprocess.CalledProcessError as e:
            pass
        finally:
            pass

        while True:
            time.sleep(1)


if __name__ == "__main__":
    Main().main()