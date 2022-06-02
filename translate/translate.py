#!/usr/bin/env python
# encoding: utf-8
import asyncio
from .exceptions import InvalidProviderError
from .providers import MyMemoryProvider, BaiduProvider, DeeplProvider, TencentProvider, YoudaoProvider, GoogleProvider, BingProvider


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
    def __init__(self, to_lang, from_lang='auto', providers=[MyMemoryProvider], timeout=2, **kwargs):
        self.available_providers = list(PROVIDERS_CLASS.keys())
        self.from_lang = from_lang
        self.to_lang = to_lang
        self.timeout = timeout

        self.providers = []
        for provider in providers:
            if provider not in self.available_providers:
                raise InvalidProviderError(
                    'Provider class invalid. '
                    'Please check providers list below: {!r}'.format(
                        self.available_providers)
                )

            provider_class = PROVIDERS_CLASS.get(provider)

            self.providers.append(provider_class(
                name=provider,
                from_lang=from_lang,
                to_lang=to_lang,
                **kwargs.get(provider)
            ))

    def translate(self, text):
        if self.from_lang == self.to_lang:
            return text
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        # loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.run(text))

    async def run(self, query):
        tasks = []
        for provider in self.providers:
            tasks.append(asyncio.create_task(
                self.provider.get_translation(query), name=provider.name))
        dones, _ = await asyncio.wait(tasks, timeout=self.timeout)
        results = {}
        for done in dones:
            results[done.get_name()] = done.result()
        return results
