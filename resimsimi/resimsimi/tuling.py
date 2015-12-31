# -*- coding: utf-8 -*-

import requests


class Tuling(object):

    API = 'http://www.tuling123.com/openapi/api'
    API_KEY = '4a041960b808c1d3cc232d59b03fef60'

    def answer(self, text, loc=None, lon=None, lat=None):
        params = {
            'key': self.API_KEY,
            'info': text,
            'userid': 143933,
            'loc': loc,
            'lon': lon,
            'lat': lat,

        }
        r = requests.get(self.API, params=params)
        if r.status_code == 200:
            return r.content
        return None

tl = Tuling()
