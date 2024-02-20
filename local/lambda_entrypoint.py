#!/usr/bin/env python
import importlib
import json
import os
import sys
import traceback
from http.server import BaseHTTPRequestHandler, HTTPServer

sys.path.append("/var/task")
module_name, handler_name = sys.argv[1].rsplit(".", 1)
handler_module = importlib.import_module(module_name)
handler = getattr(handler_module, handler_name)


class LambdaSimulator(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)

        event = json.loads(post_data.decode("utf-8"))
        try:
            response = handler(event, None)
        except Exception as e:
            response = {
                "errorMessage": str(e),
                "errorType": e.__class__.__name__,
                "stackTrace": traceback.format_exc(),
            }

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode("utf-8"))


def main():
    os.chdir("/var/task")

    server_address = ("", 8080)
    httpd = HTTPServer(server_address, LambdaSimulator)
    print(f"Starting httpd on port {server_address[1]}...")
    httpd.serve_forever()


if __name__ == "__main__":
    main()
