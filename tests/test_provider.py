#!/usr/bin/env python
# encoding: utf-8
try:
    from unittest import mock
except Exception:
    import mock

from translate.providers import MyMemoryProvider


def test_provider_mymemory_languages_attribute():
    from_lang = 'zh'
    to_lang = 'en'
    provider = MyMemoryProvider(to_lang=to_lang, from_lang=from_lang, headers={})
    expected = '{}|{}'.format(from_lang, to_lang)
    assert provider.languages == expected


def test_provider_mymemory_default_email():
    provider = MyMemoryProvider(to_lang='en', headers={})
    assert provider.email == ''
