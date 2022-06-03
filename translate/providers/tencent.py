#!/usr/bin/env python
# encoding: utf-8

from datetime import datetime
import hashlib
import hmac
import logging
import time
# import requests
import requests_async as requests
from urllib.parse import urlencode

from .base import BaseProvider
from ..exceptions import TranslationError


class TencentProvider(BaseProvider):
    name = 'tencent'

    endpoint = "tmt.tencentcloudapi.com"
    base_url = "https://" + endpoint

    def __init__(self, **kwargs):
        try:
            super().__init__(**kwargs)
        except TypeError:
            super(TencentProvider, self).__init__(**kwargs)

        self.secret_id = kwargs.get('secret_id', '')
        self.secret_key = kwargs.get('secret_key', '')
        self.project_id = kwargs.get('project_id', 0)
        self.headers = {
            'Host': self.endpoint,
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-TC-Action': 'TextTranslate',
            'X-TC-Version': '2018-03-21',
            'X-TC-Region': 'ap-beijing',
            'X-TC-Language': 'zh-CN',
            'X-TC-RequestClient': 'SDK_PYTHON_3.0.644'
        }

    async def get_translation(self, txt):
        try:
            params = {
                "SourceText": txt,
                "Source": self.from_lang,
                "Target": self.to_lang,
                "ProjectId": self.project_id,
            }
            querystring = urlencode(params)
            service = self.endpoint.split('.')[0]
            timestamp = int(time.time())
            self.headers["X-TC-Timestamp"] = str(timestamp)
            date = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d')
            signature = self._get_tc3_signature(querystring, date, service)

            auth = "TC3-HMAC-SHA256 Credential=%s/%s/%s/tc3_request, SignedHeaders=content-type;host, Signature=%s" % (
                self.secret_id, date, service, signature)
            self.headers["Authorization"] = auth

            request = await requests.get(
                self.base_url + '?' + querystring, None, headers=self.headers, verify=False)
            return request.json()['Response']['TargetText']
        except Exception as err:
            self.error = err

    def _get_tc3_signature(self, querystring, date, service):
        canonical_uri = "/"
        canonical_querystring = querystring
        payload = ""
        method = "GET"

        payload = payload.encode("utf8")

        payload_hash = hashlib.sha256(payload).hexdigest()

        canonical_headers = 'content-type:%s\nhost:%s\n' % (
            self.headers["Content-Type"], self.headers["Host"])
        signed_headers = 'content-type;host'
        canonical_request = '%s\n%s\n%s\n%s\n%s\n%s' % (method,
                                                        canonical_uri,
                                                        canonical_querystring,
                                                        canonical_headers,
                                                        signed_headers,
                                                        payload_hash)

        algorithm = 'TC3-HMAC-SHA256'
        credential_scope = date + '/' + service + '/tc3_request'
        # if sys.version_info[0] == 3:
        canonical_request = canonical_request.encode("utf8")
        digest = hashlib.sha256(canonical_request).hexdigest()
        string2sign = '%s\n%s\n%s\n%s' % (algorithm,
                                          self.headers["X-TC-Timestamp"],
                                          credential_scope,
                                          digest)
        return self.__sign_tc3(self.secret_key, date, service, string2sign)

    def __sign_tc3(self, secret_key, date, service, str2sign):
        def _hmac_sha256(key, msg):
            return hmac.new(key, msg.encode('utf-8'), hashlib.sha256)

        def _get_signature_key(key, date, service):
            k_date = _hmac_sha256(('TC3' + key).encode('utf-8'), date)
            k_service = _hmac_sha256(k_date.digest(), service)
            k_signing = _hmac_sha256(k_service.digest(), 'tc3_request')
            return k_signing.digest()

        signing_key = _get_signature_key(secret_key, date, service)
        signature = _hmac_sha256(signing_key, str2sign).hexdigest()
        return signature
