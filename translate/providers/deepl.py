#!/usr/bin/env python
# encoding: utf-8
import requests_async as requests
import json

from .base import BaseProvider
from ..exceptions import TranslationError

TRANSLATION_FROM_DEFAULT = 'autodetect'

class DeeplProvider(BaseProvider):
    '''
    @DeeplProvider: This is a integration with DeepL Translator API.
    Website: https://www.deepl.com
    Documentation: https://www.deepl.com/docs-api
    '''
    name = 'Deepl'
    base_free_url = 'https://api-free.deepl.com/v2/translate'
    base_pro_url = 'https://api.deepl.com/v2/translate'
    session = None

    def __init__(self, **kwargs):
        try:
            super().__init__(**kwargs)
        except TypeError:
            super(DeeplProvider, self).__init__(**kwargs)
        self.pro = self.kwargs.get('pro', False)
        self.base_url = self.base_pro_url if self.pro else self.base_free_url
        self.secret_key = kwargs.get('secret_key', '')

    async def _make_request(self, text):
        params = {
            'auth_key': self.secret_key,
            'target_lang': self.to_lang,
            'text': text
        }

        if self.from_lang != TRANSLATION_FROM_DEFAULT:
            params['source_lang'] = self.from_lang

        if self.session is None:
            self.session = requests.Session()
        response = await self.session.post(self.base_url, params=params, headers=self.headers, json=[{}])
        # response.raise_for_status()
        return json.loads(response.text)

    async def get_translation(self, text):
        data = await self._make_request(text)

        if "error" in data:
            raise TranslationError(data["error"]["message"])

        return [data["translations"][0]["text"]]
