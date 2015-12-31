# -*- coding: utf-8 -*-

"""
    proxy.py
    ~~~~~~~~

    ProxyHandler

    handle GET, POST, CONNECT
"""

import socket
import logging

from tornado.iostream import IOStream
from tornado.web import RequestHandler, asynchronous, HTTPError as sHTTPError
from tornado.httpclient import HTTPRequest, AsyncHTTPClient, HTTPError as cHTTPError


class HiHandler(RequestHandler):
    def get(self):
        self.write('hi...')


class AgentHandler(RequestHandler):

    SUPPORTED_METHODS = ('GET', 'POST', 'CONNECT')

    @asynchronous
    def get(self):
        url = self.request.uri
        method = self.request.method
        headers = self.request.headers
        body = self.request.body

        logging.debug('Handle %s request to %s' % (method, url))

        ua = headers.get('User-Agent', '')
        client_ip = self.request.remote_ip

        try:
            self._on_remote_read(url, method=method, headers=headers, body=body,
                                 follow_redirects=False, allow_nonstandard_methods=True)
        except cHTTPError as e:
            if hasattr(e, 'response') and e.response:
                self._on_local_write(e.response)
            else:
                raise sHTTPError(500)

    def _on_remote_read(self, url, **kwargs):
        AsyncHTTPClient().fetch(HTTPRequest(url, **kwargs), self._on_local_write)

    def _on_local_write(self, response):
        if response.error and not isinstance(response.error, cHTTPError):
            raise sHTTPError(500)
        else:
            headers = response.headers
            cookies = response.headers.get_list('Set-Cookie')
            body = response.body
            items = ('Date', 'Cache-Control', 'Server', 'Content-Type', 'Location')

            self.set_status(response.code)
            self.add_header('Via', 'ReProxy')

            for item, header in filter(lambda (__, _): _, zip(items, map(headers.get, items))):
                self.set_header(item, header)

            for cookie in cookies:
                self.add_header('Set-Cookie', cookie)

            if body:
                self.write(body)

            self.finish()

    @asynchronous
    def post(self):
        return self.get()

    @asynchronous
    def connect(self):
        url = self.request.uri
        method = self.request.method

        logging.debug('Handle %s request to %s' % (method, url))

        host, port = url.split(':')
        remote_sock = self._create_remote_socket(host, port)

        self.local_stream = self.request.connection.stream
        self.remote_stream = IOStream(remote_sock)

        self.remote_stream.connect((host, int(port)), self._tunnel)

    def _read_local_stream(self, data):
        self.remote_stream.write(data)

    def _close_local_stream(self, data=None):
        if self.remote_stream.closed():
            return
        if data:
            self.remote_stream.write(data)
        self.remote_stream.close()

    def _read_remote_stream(self, data):
        self.local_stream.write(data)

    def _close_remote_stream(self, data=None):
        if self.local_stream.closed():
            return
        if data:
            self.local_stream.write(data)
        self.local_stream.close()

    def _tunnel(self):
        self.local_stream.read_until_close(self._close_local_stream, self._read_local_stream)
        self.remote_stream.read_until_close(self._close_remote_stream, self._read_remote_stream)
        self.local_stream.write(b'HTTP/1.0 200 Connection Established\r\n\r\n')

    @staticmethod
    def _create_remote_socket(host, port):
        addresses = socket.getaddrinfo(host, port, 0, socket.SOCK_STREAM, socket.SOL_TCP)

        if len(addresses) == 0:
            raise Exception('getaddrinfo failed for %s:%d' % (host, port))

        af, socktype, proto, canonname, sa = addresses[0]

        # if forbidden_iplist: if ... raise Exception()

        remote_sock = socket.socket(af, socktype, proto)
        remote_sock.setblocking(0)
        remote_sock.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)

        return remote_sock
