#!/usr/bin/env python
# encoding: utf-8
import hashlib
import json
import random
import requests_async as requests
import logging

from .base import BaseProvider
from ..exceptions import TranslationError


class BaiduProvider(BaseProvider):

    name = 'baidu'
    base_url = "http://fanyi-api.baidu.com/api/trans/vip/translate"

    def __init__(self, **kwargs):
        try:
            super().__init__(**kwargs)
        except TypeError:
            super(BaiduProvider, self).__init__(**kwargs)

        self.appid = kwargs.get('appid', '')
        self.secret_key = kwargs.get('secret_key', '')
        self.salt = random.randint(32768, 65536)

    async def get_translation(self, txt):
        try:
            # Generate signature
            sign = self.appid + txt + str(self.salt) + self.secret_key
            sign = hashlib.md5(sign.encode()).hexdigest()
            data = {
                "appid": self.appid,
                "q": txt,
                "from": self.from_lang,
                "to": self.to_lang,
                "salt": str(self.salt),
                "sign": sign,
            }
            res = await requests.post(self.base_url, data=data)
            trans_result = json.loads(res.content).get(
                'trans_result')[0].get("dst")
            return [trans_result]
        except Exception as err:
            if self.ignore_error:
                logging.error(err)
            else:
                raise TranslationError(err)

