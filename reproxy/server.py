# -*- coding: utf-8 -*-

import logging
import os
import re
import sys
import socket
from urlparse import urlparse

import tornado.httpserver
import tornado.ioloop
import tornado.iostream
import tornado.web
from tornado.httpclient import HTTPRequest, AsyncHTTPClient


logger = logging.getLogger()


class Proxy(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    def get(self):
        url = self.request.uri
        method = self.request.method
        headers = self.request.headers
        body = self.request.body

        logger.debug('Handle %s request to %s', method, url)

        ua = headers.get('User-Agent', '')
        client_ip = self.request.remote_ip

        def _on_local_write(response):
            headers = response.headers
            cookies = response.headers.get_list('Set-Cookie')
            body = response.body

            self.set_status(response.code)

            items = ['Date', 'Cache-Control', 'Server', 'Content-Type', 'Location']
            for item, header in filter(lambda _: _[1], zip(items, map(headers.get, items))):
                self.set_header(item, header)

            for cookie in cookies:
                self.add_header('Set-Cookie', cookie)

            self.add_header('VIA', 'ReProxy')

            if body:
                self.write(body)

            self.finish()

        def _on_remote_read(url, **kwargs):
            request = HTTPRequest(url, **kwargs)
            client = AsyncHTTPClient()
            client.fetch(request, _on_local_write, follow_redirects=True, max_redirects=3)

        try:
            _on_remote_read(url, method=method, headers=headers, body=body,
                            follow_redirects=False, allow_nonstandard_methods=True)
        except tornado.httpclient.HTTPError as e:
            self.set_status(500)
            self.write('Internal Server Error: %s' % e.message)
            self.finish()

    @tornado.web.asynchronous
    def post(self):
        return self.get()


def run_server(port):
    app = tornado.web.Application([
        # TODO 这里可以。。。控制规则。。
        (r'.*', Proxy),
    ])
    app.listen(port)
    ioloop = tornado.ioloop.IOLoop.instance()
    ioloop.start()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', action='store', default=8899)

    args = parser.parse_args()
    port = int(args.port)

    run_server(port)

