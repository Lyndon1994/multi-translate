#!/usr/bin/env python
# encoding: utf-8
import asyncio
import logging

from .exceptions import InvalidProviderError
from .providers import MyMemoryProvider, BaiduProvider, DeeplProvider, TencentProvider, YoudaoProvider, GoogleProvider, \
    BingProvider

PROVIDERS_CLASS = {
    'mymemory': MyMemoryProvider,
    'deepl': DeeplProvider,
    'baidu': BaiduProvider,
    'tencent': TencentProvider,
    'youdao': YoudaoProvider,
    'google': GoogleProvider,
    'bing': BingProvider,
}


class Translator:
    def __init__(self, to_lang, from_lang='en', provider='youdao', timeout=2, **kwargs):
        self.available_providers = list(PROVIDERS_CLASS.keys())
        self.from_lang = from_lang
        self.to_lang = to_lang
        self.timeout = timeout
        self.ignore_error = kwargs.get('ignore_error', True)

        providers = filter(None, provider.strip().split(','))
        self.providers = []
        for provider in providers:
            if provider not in self.available_providers:
                raise InvalidProviderError(
                    'Provider {} invalid. '
                    'Please check providers list below: {!r}'.format(
                        provider,
                        self.available_providers)
                )

            provider_class = PROVIDERS_CLASS.get(provider)
            kwargs.update(kwargs.get(provider, {}))
            self.providers.append(provider_class(
                name=provider,
                from_lang=from_lang,
                to_lang=to_lang,
                **kwargs
            ))

    def translate(self, text, return_str=True, result_separator="___"):
        if self.from_lang == self.to_lang:
            return text
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        # loop = asyncio.get_event_loop()
        result = loop.run_until_complete(self.run(text))
        if return_str:
            return result_separator.join(filter(None, result.values()))
        return result

    async def run(self, query):
        tasks = []
        for provider in self.providers:
            tasks.append(asyncio.create_task(
                provider.get_translation(query), name=provider.name))
        dones, pending = await asyncio.wait(tasks, timeout=self.timeout)
        pending and logging.warning("pending task:" + ','.join(x.get_name() for x in pending))
        if not self.ignore_error:
            for provider in self.providers:
                if provider.error is not None:
                    logging.error(provider.error)
                    raise provider.error
        results = {}
        for done in dones:
            results[done.get_name()] = done.result()
        return results
