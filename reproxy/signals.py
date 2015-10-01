# -*- coding: utf-8 -*-

"""
    signals.py
    ~~~~~~~~~~

"""

import os
import sys
import time
import errno
import signal
import logging
from functools import partial

from tornado.ioloop import IOLoop

MAX_WAIT_SHUTDOWN = 10


def shutdown_handler(children_pid, signum, _):
    """
    主进程关闭时, 主动关闭所有子进程
    children_pid: multiprocess.Queue instance
    """
    while True:
        if not children_pid.empty():
            pid = children_pid.get(True)
            try:
                os.kill(pid, signum)
                # os.waitpid(pid, 0)  # TODO 有这个会报错。wait是个啥。。
            except OSError as e:
                if e.errno == errno.ESRCH:
                    logging.error('not running...')
                    # always exit 0 if we are sure daemon is not running
                    return
                logging.error(e.message)
        else:
            break


def wait_handler(signum, _):
    """当以多进程方式运行时, 主进程忽略设定的信号"""
    logging.warning('Caught Signal: %s PID: %s waite child shutdown...' % (signum, os.getpid()))


def close_handler(server, signum, _):
    """safe stop Server and IOLoop"""
    logging.warning('Caught Signal: %s PID: %s shutdown...' % (signum, os.getpid()))
    callback = partial(shutdown, server)
    IOLoop.instance().add_callback(callback)


def shutdown(server):
    logging.warning('Stopping HttpServer...')
    server.stop()

    deadline = time.time() + MAX_WAIT_SHUTDOWN
    io_loop = IOLoop.instance()

    _safe_stop(deadline, io_loop)


def _safe_stop(deadline, io_loop):
    now = time.time()

    if now < deadline and (io_loop._callbacks or io_loop._timeouts):
        io_loop.add_timeout(now + 1, partial(_safe_stop, deadline, io_loop))
    else:
        logging.warning('Stopping IOLoop...')
        io_loop.stop()


def exit_handler(signum, _):
    if signum == signal.SIGTERM:
        sys.exit(0)
    sys.exit(1)


def set_signal_handler(handler):
    signal.signal(signal.SIGTERM, handler)
    signal.signal(signal.SIGQUIT, handler)
    signal.signal(signal.SIGINT, handler)




