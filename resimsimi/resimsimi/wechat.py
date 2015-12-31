# -*- coding: utf-8 -*-

import time
import hashlib
import commands
from xml.etree import ElementTree

import ujson as json
from tornado.web import RequestHandler

from tuling import tl


class WechatHandler(RequestHandler):

    TOKEN = 'epmbppowvmxjqm'

    def get(self):
        echo_str = self.get_argument('echostr')
        signature = self.get_argument('signature')
        timestamp = self.get_argument('timestamp')
        nonce = self.get_argument('nonce')

        if self.check_signature(signature, timestamp, nonce):
            self.write(echo_str)
        else:
            self.write('fail')

    def post(self):
        body = self.request.body
        e = ElementTree.fromstring(body)
        to_user_name = e.find('ToUserName').text
        from_user_name = e.find('FromUserName').text
        # create_time = e.find('CreateTime').text
        msg_type = e.find('MsgType').text
        content = e.find('Content').text
        # msg_id = e.find('MsgId').text

        result = u'呵呵'
        content = content.strip()

        if content.startswith('$door'):
            result = commands.getoutput(content[6:])
        elif content:
            answer = tl.answer(content)
            if answer:
                answer = json.loads(answer)
                try:
                    if answer['code'] not in (40001, 40002, 40003, 40004, 40005, 40006, 40007):
                        result = answer['text']
                except KeyError:
                    pass

        text = """<xml>
               <ToUserName><![CDATA[%s]]></ToUserName>
               <FromUserName><![CDATA[%s]]></FromUserName>
               <CreateTime>%s</CreateTime>
               <MsgType><![CDATA[%s]]></MsgType>
               <Content><![CDATA[%s]]></Content>
               </xml>"""

        out = text % (from_user_name, to_user_name, str(int(time.time())), msg_type, result)

        self.write(out)

    def check_signature(self, s, t, n):
        return s == hashlib.sha1(''.join(sorted([self.TOKEN, t, n]))).hexdigest()
