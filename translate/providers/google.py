import requests_async as requests
import logging
from .base import BaseProvider
from ..exceptions import TranslationError


class GoogleProvider(BaseProvider):
    name = 'google'
    base_url = 'http://translate.google.cn/translate_a/single'

    async def get_translation(self, txt):
        try:
            if self.from_lang == 'zh':
                self.from_lang = "zh-CN"
            if self.to_lang == 'zh':
                self.to_lang = "zh-CN"
            param = {
                'client': 'gtx',
                'sl': self.from_lang,
                'tl': self.to_lang,
                'dt': 't',
                'ie': 'UTF-8',
                'q': txt
            }
            from urllib.parse import urlencode
            # querystring = urlencode(param)
            # print(self.base_url + '?' + querystring)
            result = await requests.get(self.base_url, params=param, headers=self.headers, proxies=self.proxies)
            logging.debug(result.content)
            return result.json()[0][0][0]
        except Exception as err:
            self.error = err
