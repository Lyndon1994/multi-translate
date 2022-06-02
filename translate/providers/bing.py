import requests_async as requests
import uuid
import json
import logging

from .base import BaseProvider
from ..exceptions import TranslationError


class BingProvider(BaseProvider):
    name = 'bing'
    base_url = "https://api.cognitive.microsofttranslator.com/translate"

    def __init__(self, **kwargs):
        try:
            super().__init__(**kwargs)
        except TypeError:
            super(BingProvider, self).__init__(**kwargs)

        self.location = kwargs.get('location', 'eastus')
        self.secret_key = kwargs.get('secret_key', '')


    async def get_translation(self, txt):
        try:
            headers = {
                'Ocp-Apim-Subscription-Key': self.secret_key,
                'Ocp-Apim-Subscription-Region': self.location,
                'Content-type': 'application/json',
                'X-ClientTraceId': str(uuid.uuid4())
            }
            params = {
                'api-version': '3.0',
                'from': self.from_lang,
                'to': [self.to_lang]
            }
            # You can pass more than one object in body.
            body = [{
                'text': txt
            }]

            request = await requests.post(
                self.base_url, params=params, headers=headers, json=body, verify=False)
            response = request.json()
            return [response[0]['translations'][0]['text']]
        except Exception as err:
            if self.ignore_error:
                logging.error(err)
            else:
                raise TranslationError(err)
