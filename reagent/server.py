# -*- coding: utf-8 -*-

"""
    server.py
    ~~~~~~~~~

    tornado server

    IPv4 HTTP(S) based Proxy Server.
"""

import os
import sys
import socket
import logging
import multiprocessing
from functools import partial

from tornado.ioloop import IOLoop
from tornado.web import Application
from tornado.httpserver import HTTPServer
from tornado.netutil import bind_sockets
from tornado import options
from tornado import process

from agent import AgentHandler, HiHandler
from signals import set_signal_handler, close_handler, shutdown_handler
from daemon import start, shutdown


PATH = os.path.dirname(__file__)

options.define('port', default=8899, type=int)
options.define('fork', default=False)
options.define('process', default=0, type=int)
options.define('daemon', default='')
options.define('path', default=PATH)

options.parse_command_line()

application = Application([
    (r'/hi', HiHandler),
    (r'.*', AgentHandler),
])

if __name__ == '__main__':
    is_fork = options.options.fork
    process_num = options.options.process
    daemonize = options.options.daemon
    path = options.options.path

    if daemonize == 'start':
        start(path)
    elif daemonize == 'shutdown':
        shutdown(path)
        sys.exit(0)
    elif daemonize == 'restart':
        shutdown(path)
        start(path)

    pid = os.getpid()
    children_pid = multiprocessing.Queue()

    sockets = bind_sockets(options.options.port, family=socket.AF_INET)

    # Tornado － 多进程
    # 1. 创建 server socket.
    # 2. fork 子进程, 所有的子进程都监听server socket.
    #
    # 主进程只做监管, os.wait()
    # 子进程accept, 某子进程成功accept, 其他子进程再尝试accept就会 EWOULDBLOCK 或 EAGAIN 异常, 不处理直接返回.
    if is_fork:
        shutdown_handler = partial(shutdown_handler, children_pid)
        set_signal_handler(shutdown_handler)
        process.fork_processes(process_num or 0)

    if pid == os.getppid():
        children_pid.put(os.getpid())

    logging.warning('Starting Server... PID: %s' % os.getpid())

    # server = HTTPServer(application, xheaders=True)
    server = HTTPServer(application)
    server.add_sockets(sockets)

    close_handler = partial(close_handler, server)
    set_signal_handler(close_handler)

    IOLoop.instance().start()

    logging.warning('Stopped Server... PID: %s' % os.getpid())
