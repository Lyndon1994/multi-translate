#!/usr/bin/env python
# encoding: utf-8
from ..exceptions import TranslationError
from .base import BaseProvider
from ..constants import YOUDAO_APP_KEY, YOUDAO_APP_SECRET
import logging
import uuid
import requests_async as requests
import hashlib
import time


class YoudaoProvider(BaseProvider):
    # https://ai.youdao.com/DOCSIRMA/html/%E8%87%AA%E7%84%B6%E8%AF%AD%E8%A8%80%E7%BF%BB%E8%AF%91/API%E6%96%87%E6%A1%A3/%E6%96%87%E6%9C%AC%E7%BF%BB%E8%AF%91%E6%9C%8D%E5%8A%A1/%E6%96%87%E6%9C%AC%E7%BF%BB%E8%AF%91%E6%9C%8D%E5%8A%A1-API%E6%96%87%E6%A1%A3.html

    name = 'youdao'
    base_url = "http://openapi.youdao.com/api"

    def __init__(self, **kwargs):
        try:
            super().__init__(**kwargs)
        except TypeError:
            super(YoudaoProvider, self).__init__(**kwargs)

        self.app_key = kwargs.get('app_key', YOUDAO_APP_KEY)
        self.app_secret = kwargs.get('app_secret', YOUDAO_APP_SECRET)

    def __encrypt(self, signStr):
        hash_algorithm = hashlib.sha256()
        hash_algorithm.update(signStr.encode('utf-8'))
        return hash_algorithm.hexdigest()

    def __truncate(self, q):
        if q is None:
            return None
        size = len(q)
        return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]

    async def get_translation(self, txt):
        try:
            data = {}
            data['from'] = self.from_lang
            data['to'] = self.to_lang
            data['signType'] = 'v3'
            curtime = str(int(time.time()))
            data['curtime'] = curtime
            salt = str(uuid.uuid1())
            signStr = self.app_key + \
                      self.__truncate(txt) + salt + curtime + self.app_secret
            sign = self.__encrypt(signStr)
            data['appKey'] = self.app_key
            data['q'] = txt
            data['salt'] = salt
            data['sign'] = sign

            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            response = await requests.post(self.base_url, data=data, headers=headers)
            result = response.json()
            if result.get('basic', {}).get('explains'):
                return '||'.join(result.get('basic', {}).get('explains'))
            return result['translation'][0]
        except Exception as err:
            self.error = err
