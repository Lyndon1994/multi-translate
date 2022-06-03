Multi Translate Tool in Python
==============================

|PyPI latest| |PyPI Version| |PyPI License| |Docs|

Translate is a simple but powerful translation tool written in python
with support for multiple translation providers. By now we offer
integration with Baidu, Bing, Deepl, Google, MyMemory, Tencent, Youdao
translation APIs.

It is forked from `translate <https://pypi.org/project/translate/>`__,
and it is compatible with this pack.

Why Should I Use This?
----------------------

The biggest reason to use translate is to make translations in wox and
alfred quickly, and I would like to see the translation results of
various platforms and choose the best one. I want to share with you, and
it supports concurrent request for multiple platform translation
results.

Installation
------------

.. code:: bash

   $ pip install multi-translate

Or, you can download the source and

.. code:: bash

   $ python setup.py install

Prefix 'sudo' if you encounter a problem.

Features
--------

-  Translate text in real time and support concurrent request for
   multiple platform translation results
-  Do translation in your terminal using the command line
-  Default Youdao Translator, and it has built-in Youdao Translator
   APP_KEY, so you can use Youdao Translator directly.

Usage
-----

Use As A Python Module
~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

   In [1]: from translate import Translator
   In [2]: translator = Translator(to_lang="zh")
   In [3]: translation = translator.translate("This is a pen.")
   Out [3]: 这是一支笔

The result is usually a unicode string.

Use a different translation provider
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

   In [1]: from translate import Translator
   In [2]: to_lang = 'zh'
   In [3]: secret = '<your secret from Microsoft or DeepL>'
   In [4]: translator = Translator(provider='<the name of the provider, eg. bing or deepl>', to_lang=to_lang, secret_key=secret)
   In [5]: translator.translate('the book is on the table')
   Out [5]: '碗是在桌子上。'

Use multi translation provider
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

   from translate import Translator
   baidu = {
       'appid': 'xxx',
       'secret_key': 'xxx'
   }
   tencent = {
       'secret_id': 'xxx',
       'secret_key': 'xxx'
   }
   bing = {
       'location': 'eastus',
       'secret_key': 'xxx'
   }
   youdao = {
       'app_key': 'xxx',
       'app_secret': 'xxx'
   }
   translator = Translator(to_lang='zh', provider='baidu,tencent,youdao,bing',
                           baidu=baidu, tencent=tencent, bing=bing, youdao=youdao)
   translation = translator.translate('hello world', return_str=False)
   print(translation)

   # output: {'youdao': '你好世界', 'tencent': '你好世界', 'bing': '世界您好', 'baidu': '你好，世界'}

The DeepL Provider
^^^^^^^^^^^^^^^^^^

To use DeepL's pro API, pass an additional parameter named pro to the
Translator object and set it to True and use your pro authentication key
as the secret_key

.. code:: python

   In: translator = Translator(provider='microsoft', to_lang=to_lang, secret_key=secret, pro=True)

Use As A Command Line
~~~~~~~~~~~~~~~~~~~~~

In your command-line:

.. code:: bash

   $ translate-cli -t zh "This is a pen."

   Translation: 这是一支钢笔。
   -------------------------
   Translated by: youdao

Or

.. code:: bash

   $ translate-cli -t zh "This is a pen." -o
   这是一支钢笔。

Options
^^^^^^^

.. code:: bash

   $ translate-cli --help
   Usage: __main__.py [OPTIONS] TEXT...

     Python command line tool to make online translations

     Example:

          $ translate-cli -t zh the book is on the table
          碗是在桌子上。

     Available languages:

          https://en.wikipedia.org/wiki/ISO_639-1
          Examples: (e.g. en, ja, ko, pt, zh, zh-TW, ...)

   Options:
     --version                 Show the version and exit.
     --generate-config-file    Generate the config file using a Wizard and exit.
     -f, --from TEXT           Sets the language of the text being translated.
                               The default value is 'auto'.
     -t, --to TEXT             Set the language you want to translate.
     -p, --provider TEXT       Set the provider you want to use. The default value is 'youdao'.
     --appid TEXT              appid, needed by baidu translator
     --secret_id TEXT          Set the secret id used to get provider oAuth token.
     --secret_key TEXT         Set the secret access key used to get provider oAuth token.
     -o, --output_only         Set to display the translation only.
     --help                    Show this message and exit.

Change Default Languages
^^^^^^^^^^^^^^^^^^^^^^^^

In ~/.python-translate.cfg:

.. code:: bash

   [DEFAULT]
   from_lang = autodetect
   to_lang = de
   provider = youdao
   secret_key =

The cfg is not for use as a Python module. or run the command line and
follow the steps:

.. code:: bash

   $ translate-cli --generate-config-file
   Translate from [autodetect]:
   Translate to: <language you want to translate>
   Provider [youdao]:
   Secret Access Key []:

Documentation
-------------

Check out the latest ``translate`` documentation at `Read the
Docs <http://translate-python.readthedocs.io/en/latest/>`__

   It's document of `translate <https://pypi.org/project/translate/>`__,
   but it's still available, although no new features.

Contributing
------------

Please send pull requests, very much appreciated.

1. Fork the
   `repository <https://github.com/Lyndon1994/multi-translate>`__ on
   GitHub.
2. Make a branch off of main and commit your changes to it.
3. (Optional) if you want an isolated environment, you can install nixOS
   (`https://nixos.org <https://nixos.org>`__) and run
   ``nix-shell --pure`` under the project folder
4. Install requirements. ``pip install -r requirements-dev.txt``
5. Install pre-commit. ``pre-commit install``
6. Run the tests with ``py.test -vv -s``
7. Create a Pull Request with your contribution.

.. |PyPI latest| image:: https://img.shields.io/pypi/v/translate.svg?maxAge=360
   :target: https://pypi.python.org/pypi/multi-translate
.. |PyPI Version| image:: https://img.shields.io/pypi/pyversions/translate.svg?maxAge=2592000
   :target: https://pypi.python.org/pypi/multi-translate
.. |PyPI License| image:: https://img.shields.io/pypi/l/translate.svg?maxAge=2592000
   :target: https://github.com/Lyndon1994/multi-translate/blob/main/LICENSE
.. |Docs| image:: https://readthedocs.org/projects/translate-python/badge/?version=latest
   :target: http://translate-python.readthedocs.org/en/latest/?badge=latest
