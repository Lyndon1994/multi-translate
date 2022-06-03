#!/usr/bin/env python
# encoding: utf-8
try:
    from unittest import mock
except Exception:
    import mock

import pytest

from translate import Translator
from translate.exceptions import InvalidProviderError, TranslationError
from translate.providers import MyMemoryProvider

from .vcr_conf import vcr


def test_tranlate_with_invalid_provider():
    with pytest.raises(InvalidProviderError) as error:
        Translator(to_lang='en', provider='invalid_provider')

    assert 'Provider invalid_provider invalid. Please check providers list below:' in str(error.value)


def test_tranlate_with_valid_provider():
    translator = Translator(to_lang='en', provider='mymemory')
    assert isinstance(translator.providers[0], MyMemoryProvider)


def test_tranlate_with_provider_extra_argument():
    # Case from MyMemoryProvider extra argument
    email = 'test@test.com'
    translator = Translator(to_lang='en', provider='mymemory', email=email)
    assert translator.providers[0].email == email


@vcr.use_cassette
def test_tranlate_english_to_english():
    translator = Translator(to_lang='en')
    translation = translator.translate('why')
    assert 'why' == translation


@vcr.use_cassette
def test_translate_english_to_portuguese():
    translator = Translator(to_lang='pt')
    translation = translator.translate('hello world')
    assert u'Olá, mundo' == translation


@vcr.use_cassette
def test_translate_english_to_chinese_simplified():
    translator = Translator(to_lang='zh')
    translation = translator.translate('hello world')
    assert u'你好世界' == translation


@vcr.use_cassette
def test_translate_with_quote():
    translator = Translator(to_lang='zh')
    translation = translator.translate("What is 'yinyang'?")
    assert u'“阴阳”是什么?' == translation


@vcr.use_cassette
def test_translate_with_multiple_sentences():
    translator = Translator(to_lang='zh')
    translation = translator.translate('yes or no')
    assert u'是或不是' in translation


@vcr.use_cassette
def test_translate_with_HTTPError():
    import requests_async as requests
    t = Translator(to_lang='de', provider='mymemory', ignore_error=False)
    t.providers[0].base_url += '-nonsense'
    with pytest.raises(requests.HTTPError) as error:
        t.translate('hello')
    assert '404' in str(error)


@vcr.use_cassette
def test_translate_with_status_error():
    import requests_async as requests
    t = Translator(to_lang='de', provider='mymemory', email='invalid', ignore_error=False)
    with pytest.raises((TranslationError, requests.HTTPError)) as error:
        t.translate('hello again!')
    assert 'INVALID EMAIL' in str(error).upper()


@mock.patch('requests.get')
def test_tranlate_taking_secondary_match(mock_requests, main_translation_not_found):
    mock_requests.return_value.json.return_value = main_translation_not_found
    translator = Translator(to_lang='zh')
    translation = translator.translate('unknown')
    assert '未知' in translation
