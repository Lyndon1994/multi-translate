#!/usr/bin/env python
# encoding: utf-8

from abc import ABCMeta, abstractmethod


class BaseProvider:
    __metaclass__ = ABCMeta

    name = ''
    base_url = ''

    def __init__(self, to_lang, from_lang='en', **kwargs):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebit/535.19'
                                      '(KHTML, like Gecko) Chrome/18.0.1025.168 Safari/535.19'}
        self.from_lang = from_lang
        self.to_lang = to_lang
        self.ignore_error = kwargs.get('ignore_error', True)
        self.proxies = kwargs.get("proxies")
        self.kwargs = kwargs
        self.error = None

    @abstractmethod
    async def get_translation(self, params):
        return NotImplemented('Please Implement this method')
