#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'whj'
import socketserver
from core.server import Server


def run():
    # 服务端的IP地址和端口
    ip_port = ('127.0.0.1', 8899)
    # 设置allow_reuse_address允许服务器重用地址
    socketserver.TCPServer.allow_reuse_address = True
    # 绑定IP地址和端口,并且启动定义Server类
    server = socketserver.ThreadingTCPServer(ip_port, Server)
    # 让server永远运行下去，除非强制停止程序
    server.serve_forever()


if __name__ == '__main__':
    import os
    import sys

    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    run()
