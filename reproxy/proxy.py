# -*- coding: utf-8 -*-

import logging
import traceback

from tornado.web import RequestHandler

from controls import FetchProxy


class FetchHandler(RequestHandler):

    SUPPORTED_METHODS = ('GET', )

    def get(self):
        for url in FetchProxy.PROXY_SITE:
            try:
                logging.warning('fetching url: %s ...' % url[0])
                FetchProxy(*url).fetch_proxy()
            except Exception as e:
                logging.warning(traceback.format_exc(e))
        self.write('Fetch Done.')


class ProxyHandler(RequestHandler):

    SUPPORTED_METHODS = ('GET', )

    def get(self):
        self.write('ProxyHandler...')
