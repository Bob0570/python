#testing

import sys
import os
import time
import struct
import tkinter
import tkinter.messagebox

import http.server
import socketserver

#python -m http.server 8000

PORT = 80

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
