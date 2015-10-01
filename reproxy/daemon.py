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


def to_bytes(s):
    if bytes != str:
        if type(s) == str:
            return s.encode('utf-8')
    return s


def to_str(s):
    if bytes != str:
        if type(s) == bytes:
            return s.decode('utf-8')
    return s


def with_pid_file(pid_file, pid):
    """"""
    try:
        fd = os.open(pid_file, os.O_RDWR | os.O_CREAT, stat.S_IRUSR | stat.S_IWUSR)
    except OSError as e:
        logging.error(e.message)
        return -1

    flags = fcntl.fcntl(fd, fcntl.F_GETFD)
    assert flags != -1

    flags |= fcntl.FD_CLOEXEC

    # TODO why use r not flags
    # r = fcntl.fcntl(fd, fcntl.F_SETFD, flags)
    # assert r != -1
    flags = fcntl.fcntl(fd, fcntl.F_SETFD, flags)
    assert flags != -1

    try:
        fcntl.lockf(fd, fcntl.LOCK_EX | fcntl.LOCK_NB, 0, 0, os.SEEK_SET)
    except IOError:
        r = os.read(fd, 32)
        if r:
            logging.error('already started at pid %s' % to_str(r))
        else:
            logging.error('already started')
        os.close(fd)
        return -1

    os.ftruncate(fd, 0)
    os.write(fd, to_bytes(str(pid)))
    return 0


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
        time.sleep(5)
        sys.exit(0)

    ppid = os.getppid()
    pid = os.getpid()

    if with_pid_file(pid_file, pid) != 0:
        os.kill(ppid, signal.SIGINT)
        sys.exit(1)

    os.setsid()  # TODO What's this
    signal.signal(signal.SIG_IGN, signal.SIGHUP)  # TODO and what's this

    os.kill(ppid, signal.SIGTERM)

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
            buf = f.read()
            pid = to_str(buf)
            if not buf:
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
