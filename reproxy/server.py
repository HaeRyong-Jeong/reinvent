# -*- coding: utf-8 -*-

import os
import socket
import logging

from tornado.ioloop import IOLoop
from tornado.web import Application
from tornado.httpserver import HTTPServer
from tornado.netutil import bind_sockets
from tornado import options

from proxy import FetchHandler, ProxyHandler

options.define('port', default=8990, type=int)

options.parse_command_line()


application = Application([
    (r'/fetch', FetchHandler),
    (r'/proxy', ProxyHandler),
])

port = options.options.port

sockets = bind_sockets(port, family=socket.AF_INET)

server = HTTPServer(application, xheaders=True)
server.add_sockets(sockets)

logging.warning('Starting Server... PID: %s PORT: %d' % (os.getpid(), port))

IOLoop.instance().start()
