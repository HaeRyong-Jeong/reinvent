# -*- coding: utf-8 -*-

import time
import logging
import requests

import tornado.ioloop
import tornado.web
import tornado.gen
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from tornado.concurrent import run_on_executor
# 这个并发库在python3自带在python2需要安装sudo pip install futures
from concurrent.futures import ThreadPoolExecutor


index = 0


class AsyncHandler(tornado.web.RequestHandler):

    executor = ThreadPoolExecutor(50)

    @tornado.web.asynchronous
    def get(self):
        logging.error(str(time.time()))
        global index
        index += 1
        if index == 1:
            url = 'http://localhost:8881'
        else:
            url = 'http://localhost:8882'
        AsyncHTTPClient().fetch(HTTPRequest(url), self._on_response)

    @run_on_executor
    def _on_response(self, response):
        self.write(str(time.time()))
        self.finish()


class AsyncCoroutineHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        logging.error(str(time.time()))
        self.write(str(time.time()))
        # yield AsyncHTTPClient().fetch(HTTPRequest('http://localhost:8889'))
        time.sleep(5)
        self.finish()


class TestHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    def get(self):

        AsyncHTTPClient().fetch(HTTPRequest('http://localhost:8881'), self._on_response)

    def _on_response(self, response):
        self.finish()
    #     AsyncHTTPClient().fetch(HTTPRequest('http://localhost:8882'), self._on_response1)
    #
    # def _on_response1(self, response):
    #     self.finish()


if __name__ == '__main__':
    application = tornado.web.Application([
        (r'/async', AsyncHandler),
        (r'/asyncc', AsyncCoroutineHandler),
        (r'/test', TestHandler),
    ])
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()
