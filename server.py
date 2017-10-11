# /usr/bin/env python3
# Simple http.server modified to serve extensionless
# files as text/html.
# Modified from https://gist.github.com/HaiyangXu/ec88cbdce3cdbac7b8d5

from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
import socketserver

PORT = 8080

Handler = SimpleHTTPRequestHandler

Handler.extensions_map={
        '.manifest': 'text/cache-manifest',
	'.html': 'text/html',
        '.png': 'image/png',
	'.jpg': 'image/jpg',
	'.svg':	'image/svg+xml',
	'.css':	'text/css',
	'.js':	'application/x-javascript',
	'': 'text/html'
    }

httpd = socketserver.TCPServer(("", PORT), Handler)

print("Serving HTTP at Port", PORT)
httpd.serve_forever()
