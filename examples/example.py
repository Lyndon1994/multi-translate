#!/usr/bin/env python
# encoding: utf-8
from translate import Translator
translator = Translator(to_lang='zh')
translation = translator.translate('hello world')
print(translation)

translator = Translator(to_lang='zh', providers=['google'])
translation = translator.translate('hello world')
print(translation)