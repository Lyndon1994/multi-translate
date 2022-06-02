#!/usr/bin/env python
# encoding: utf-8

from .mymemory import MyMemoryProvider  # noqa
from .deepl import DeeplProvider  # noqa
from .baidu import BaiduProvider
from .bing import BingProvider
from .google import GoogleProvider
from .tencent import TencentProvider
from .youdao import YoudaoProvider

__all__ = ['MyMemoryProvider', 'BaiduProvider', 'DeeplProvider', 'BingProvider', 'GoogleProvider', 'TencentProvider', 'YoudaoProvider']
