# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        # eat time
        for x in xrange(1, 9000):
            _ = x ** x
        self.write('... Main.')


if __name__ == '__main__':
    application = tornado.web.Application([
        (r'/', MainHandler),
    ])
    application.listen(8882)
    tornado.ioloop.IOLoop.current().start()
