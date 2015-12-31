# # -*- coding: utf-8 -*-
#
# import tornado.ioloop
#
#
# instance = tornado.ioloop.IOLoop.instance()
#
#
# def do_division(a, b):
#     return a / b
#
#
# def async_division(a, b, callback):
#     if a == 0:
#         raise Exception('always equal to zero')
#     instance.add_callback(callback, a, b)
#
#
# # try:
# #     async_division(0, 2, do_division)
# # except Exception as e:
# #     print e.message
#
#
# # def wrapper(fn):
# #     def _wrap(*args, **kwargs):
# #         try:
# #             fn(*args, **kwargs)
# #         except Exception as e:
# #             print e.message
# #     return _wrap
#
# # wrapper(async_division)(2, 0, wrapper(do_division))
#
# from tornado import stack_context
#
#
# def handle_division_exception(exc_type, exc_val, exc_tb):
#     print 'division exception:', exc_val
#     return True
#
#
# # with stack_context.ExceptionStackContext(handle_division_exception):
# #     async_division(2, 0, do_division)
#
#
# # with stack_context.ExceptionStackContext(handle_division_exception):
# #     do_division = stack_context.wrap(do_division)
# #     async_division(2, 0, do_division)
#
# m, n = 5, 0
#
#
# def do_minus(b, rate):
#     if b == rate:
#         raise Exception('divided by one')
#
#
# def async_minus(b, rate, callback):
#     instance.add_callback(callback, b, rate)
#
#
# def handle_minus_exception(exc_type, exc_val, exc_tb):
#     print 'minus exception:', exc_val
#     return True
#
#
# with stack_context.ExceptionStackContext(handle_division_exception):
#     if m - n == 5:
#         with stack_context.ExceptionStackContext(handle_minus_exception):
#             do_minus = stack_context.wrap(do_minus)
#             async_minus(n, n, do_minus)
#     do_division = stack_context.wrap(do_division)
#     async_division(m, n, do_division)
#
#
# instance.start()


# def counter():
#     n = 0
#     while True:
#         yield n
#         n += 1
#
#
# c = counter()
# print next(c)
# print c.next()
#
#
# def counter():
#     n = [-1]
#
#     def wrap():
#         n[0] += 1
#         return n[0]
#     return wrap
#
# c = counter()
#
# print c()
# print c()


# def add(x):
#
#     def adder(y):
#         print x + y
#
#     return adder
#
#
# add3 = add(3)
# add3(2)


# def add(x):
#
#     y = yield
#
#     print x + y
#
#
# add3 = add(3)
# add3.next()
# add3.send(2)


# xrange

# def _xrange(n):
#     _ = 0
#     while True:
#         if _ < n:
#             yield _
#         else:
#             return
#         _ += 1

# import time
# import random
# from datetime import datetime
#
#
# class Future(object):
#     def __init__(self):
#         self.result = None
#         self.callback = None
#
#     def add_callback(self, callback):
#         self.callback = callback
#
#     def set_result(self, result):
#         self.result = result
#         self.set_done()
#
#     def set_done(self):
#         if self.callback:
#             self.callback(self.result)


# def get():
#     dark_time(callback=pretty_print)


# def dark_time(callback):
#     timestamp = time.time()
#     for _ in xrange(random.choice([6000, 7000, 8000])):
#         _ = _ ** _
#     if callback:
#         callback(timestamp)

#
# def pretty_print(timestamp):
#     print datetime.utcfromtimestamp(timestamp), '->', datetime.utcfromtimestamp(time.time())
#
#
# def eat_time(callback):
#     timestamp = time.time()
#     for _ in xrange(random.choice([6000, 7000, 8000])):
#         _ = _ ** _
#     callback(timestamp)
#
#
# def dark_time(callback=None):
#     future = Future()
#     if callback:
#         future.add_callback(callback)
#
#     def handle_result(result):
#         future.set_result(result)
#
#     eat_time(handle_result)
#
#     return future
#
#
# def concurrent(fn):
#     def wrapper(*args, **kwargs):
#         try:
#             gen = fn(*args, **kwargs)
#             print 2
#         except Exception as e:
#             print e.message
#         else:
#             import types
#             if isinstance(gen, types.GeneratorType):
#                 try:
#                     yielded = next(gen)
#                 except StopIteration as e:
#                     print e.message
#                 except Exception as e:
#                     print e.message
#                 else:
#                     Runner(gen, yielded)
#                     print 3
#     return wrapper
#
#
# class Runner(object):
#     def __init__(self, gen, yielded):
#         self.gen = gen
#         self.yielded = yielded
#         self.begin()
#
#     def begin(self):
#         self.yielded.add_callback(self.run)
#         print 4
#         print self.yielded.callback
#
#     def run(self, result):
#         print 5, result
#         self.gen.send(result)
#
#
# @concurrent
# def get():
#     print 1
#     result = yield dark_time()
#     pretty_print(result)
#
#
# get()
# get()

import time
from tornado import ioloop
from tornado import gen, web
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor


class IndexHandler(web.RequestHandler):
    executor = ThreadPoolExecutor(2)

    @gen.coroutine
    def get(self):  # 用yield来返回一个迭代器函数
        mov = yield self.query_movie()
        self.write(mov)
        self.finish()

    @run_on_executor  # 此处是耗时的操作
    def query_movie(self):
        timestamp = time.time()
        time.sleep(5)
        # for _ in xrange(8000):
        #     _ = _ ** _
        return str(timestamp)


application = web.Application([
    (r"/", IndexHandler),
])
application.listen(8888)
ioloop.IOLoop.current().start()
