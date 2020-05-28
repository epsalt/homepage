#!/usr/bin/env python3

# Simple http.server modified to serve extensionless
# files as text/html.
# Modified from https://gist.github.com/HaiyangXu/ec88cbdce3cdbac7b8d5

from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
from os import chdir
import socketserver
import argparse

DEFAULT_PORT = 8080


def serve(port):
    Handler = SimpleHTTPRequestHandler
    Handler.extensions_map = {
        ".manifest": "text/cache-manifest",
        ".html": "text/html",
        ".png": "image/png",
        ".jpg": "image/jpg",
        ".svg": "image/svg+xml",
        ".css": "text/css",
        ".js": "application/x-javascript",
        "": "text/html",
    }

    httpd = socketserver.TCPServer(("", port), Handler)
    print("Serving HTTP at Port", port)
    httpd.serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple web server")
    parser.add_argument("dir", help="directory to serve files from")
    parser.add_argument("-p", "--port", type=int, help="port to serve on")
    args = parser.parse_args()

    chdir(args.dir)

    if args.port is not None:
        serve(port=args.port)
    else:
        serve(port=DEFAULT_PORT)
