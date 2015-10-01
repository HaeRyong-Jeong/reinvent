# -*- coding: utf-8 -*-

"""
    server.py
    ~~~~~~~~~

    tornado server

    IPv4 HTTP(S) based Proxy Server.
"""

import time
import socket
import signal
import logging
from functools import partial

from tornado.ioloop import IOLoop
from tornado.web import Application
from tornado.httpserver import HTTPServer
from tornado.netutil import bind_sockets
from tornado import options
from tornado import process

from proxy import ProxyHandler


MAX_WAIT_SECONDS_BEFORE_SHUTDOWN = 10


def signal_handler(sig, _):
    logging.warning('Caught Signal: %s', sig)
    IOLoop.instance().add_callback(shutdown)


def shutdown():
    server.stop()
    logging.warning('Stopping HttpServer...')

    deadline = time.time() + MAX_WAIT_SECONDS_BEFORE_SHUTDOWN
    io_loop = IOLoop.instance()

    _safe_stop(deadline, io_loop)


def _safe_stop(deadline, io_loop):
    now = time.time()

    if now < deadline and (io_loop._callbacks or io_loop._timeouts):
        io_loop.add_timeout(now + 1, partial(_safe_stop, deadline, io_loop))
    else:
        io_loop.stop()
        logging.warning('Stopping IOLoop...')


options.define('debug', default=True)
options.define('port', default=8899, type=int)
options.define('fork', default=False, type=int)
options.define('process', default=0, type=int)

options.parse_command_line()

application = Application([
    (r'.*', ProxyHandler)
])

if __name__ == '__main__':
    sockets = bind_sockets(options.options.port, family=socket.AF_INET)

    if options.options.fork:
        process.fork_processes(options.options.process or 0)

    server = HTTPServer(application, xheaders=True)
    server.add_sockets(sockets)

    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    IOLoop.instance().start()
