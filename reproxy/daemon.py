# -*- coding: utf-8 -*-

"""
    utils.py
    ~~~~~~~~

"""

import os
import sys
import time
import stat
import fcntl
import errno
import signal
import logging

from signals import set_signal_handler, exit_handler


def with_pid_file(pid_file, pid):
    """"""
    try:
        fd = os.open(pid_file, os.O_RDWR | os.O_CREAT, stat.S_IRUSR | stat.S_IWUSR)
    except OSError as e:
        logging.error(e.message)
        return False

    flags = fcntl.fcntl(fd, fcntl.F_GETFD)
    assert flags != -1

    flags = fcntl.fcntl(fd, fcntl.F_SETFD, flags | fcntl.FD_CLOEXEC)
    assert flags != -1

    try:
        fcntl.lockf(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError:
        pid = os.read(fd, 32)
        logging.error('already started %(pid)s' % {'pid': pid})
        os.close(fd)
        return False

    os.ftruncate(fd, 0)
    os.write(fd, str(pid))
    return True


def freopen(log_file, mode, stream):
    """c语言中相同函数"""
    # TODO stdout, stderr 重定向到文件而已.. 搜到的做法貌似不太一样, 先看懂原来的语句
    f = open(log_file, mode)
    fd = f.fileno()
    stream_fd = stream.fileno()
    os.close(stream_fd)
    os.dup2(fd, stream_fd)


def start(path):
    set_signal_handler(exit_handler)

    pid_file = os.path.join(path, 're-proxy.pid')
    log_file = os.path.join(path, 're-proxy.log')

    pid = os.fork()
    assert pid != -1

    if pid > 0:
        sys.exit(0)

    if not with_pid_file(pid_file, os.getpid()):
        sys.exit(1)

    os.setsid()  # TODO What's this
    signal.signal(signal.SIG_IGN, signal.SIGHUP)  # TODO and what's this

    sys.stdin.close()
    try:
        freopen(log_file, 'a', sys.stdout)
        freopen(log_file, 'a', sys.stderr)
    except IOError as e:
        logging.error(e.message)
        sys.exit(1)


def shutdown(path):
    pid_file = os.path.join(path, 're-proxy.pid')

    try:
        with open(pid_file) as f:
            pid = f.read()
            if not pid:
                logging.error('not running...')
    except IOError as e:
        logging.error(e.message)
        if e.errno == errno.ENOENT:
            # always exit 0 if we are sure daemon is not running
            logging.error('not running')
            return
        sys.exit(1)

    pid = int(pid)

    if pid > 0:
        try:
            os.kill(pid, signal.SIGTERM)
        except OSError as e:
            if e.errno == errno.ESRCH:
                logging.error('not running...')
                # always exit 0 if we are sure daemon is not running
                return
            logging.error(e.message)
            sys.exit(1)
    else:
        logging.error('pid is not positive: %d' % pid)

    # sleep for maximum 0.05 * 200 = 10s
    for i in range(0, 200):
        try:
            # query for the pid
            os.kill(pid, 0)
        except OSError as e:
            if e.errno == errno.ESRCH:
                break
        time.sleep(0.05)
    else:
        logging.error('timed out when stopping pid %d' % pid)
        sys.exit(1)

    logging.info('stopped...')
    os.unlink(pid_file)
