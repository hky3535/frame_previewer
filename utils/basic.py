"""
何恺悦 hekaiyue 2023-07-18
"""
from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import os
import time
import base64
from io import BytesIO
import asyncio
import websockets
import atexit


class Basic:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.index_html_dir = f"utils/index.html"
        self.bytes_frame = open(f"{self.base_dir}/blank.jpg", "rb").read()

    def index_html(self, ip, port):
        def index_html_handler(self):
            parent = self
            class RequestHandler(SimpleHTTPRequestHandler):
                def do_GET(self):
                    self.path = parent.index_html_dir
                    return SimpleHTTPRequestHandler.do_GET(self)
                def do_POST(self):
                    content_length = int(self.headers['Content-Length'])
                    post_data = self.rfile.read(content_length)

                    parent.bytes_frame = post_data

                    self.send_response(200)
                    self.send_header('Content-Type', 'text/plain')
                    self.end_headers()
                    self.wfile.write(b'Frame_Received')
                        
            return RequestHandler
        
        request_handler = HTTPServer((ip, port), index_html_handler(self))
        request_handler.serve_forever()
        atexit.register(request_handler.shutdown)   # 在程序退出时关闭 WebSocket 连接
    
    def index_ws(self, ip, port):
        async def update(ws, _):
            parent = self
            while True:
                base64_frame = base64.b64encode(parent.bytes_frame).decode('utf-8')
                try:
                    await ws.send(base64_frame)
                except websockets.exceptions.ConnectionClosedError:
                    break
                except websockets.exceptions.ConnectionClosedOK:
                    break
                time.sleep(0.01)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        start_server = websockets.serve(update, ip, port)
        loop.run_until_complete(start_server)
        loop.run_forever()
