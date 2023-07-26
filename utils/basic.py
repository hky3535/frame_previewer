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


class Basic:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.index_html_dir = f"utils/index.html"
        self.bytes_frame = open(f"{self.base_dir}/blank.bytes")

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
    
    def index_ws(self, ip, port):
        async def update(ws, _):
            parent = self
            try:
                while True:
                    base64_frame = base64.b64encode(parent.bytes_frame).decode('utf-8')
                    await ws.send(base64_frame)
                    time.sleep(0.01)
            except websockets.exceptions.ConnectionClosedError:
                pass

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        start_server = websockets.serve(update, ip, port)
        loop.run_until_complete(start_server)
        loop.run_forever()

        # 处理前端连接丢失后的后处理
        try:
            loop.run_until_complete(start_server)
        except KeyboardInterrupt:
            pass
        finally:
            loop.stop()
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()