=============
number-parser
=============
.. image:: https://img.shields.io/pypi/pyversions/price-parser.svg
   :target: https://pypi.python.org/pypi/price-parser
   :alt: Supported Python Versions

``number-parser`` is a simple library that allows you to convert numbers written in the natural
language to it's equivalent numeric forms. It currently supports cardinal numbers in the following
languages - English, Hindi, Spanish, Ukrainian and Russian and ordinal numbers in English.

Installation
============
::

    pip install number-parser

number-parser requires Python 3.9+.

Usage
=====

The library provides the following common usages.

Converting numbers in-place
---------------------------

Identifying the numbers in a text string, converting them to corresponding numeric values while ignoring non-numeric words.
This also supports ordinal number conversion (for English only).

>>> from number_parser import parse
>>> parse("I have two hats and thirty seven coats")
'I have 2 hats and 37 coats'
>>> parse("One, Two, Three go")
'1, 2, 3 go'
>>> parse("First day of year two thousand")
'1 day of year 2000'

Parsing a number
----------------

Converting a single number written in words to it's corresponding integer.

>>> from number_parser import parse_number
>>> parse_number("two thousand and twenty")
2020
>>> parse_number("not_a_number")

Parsing an ordinal
------------------

Converting a single ordinal number written in words to its corresponding integer. (Support for English only)

>>> from number_parser import parse_ordinal
>>> parse_ordinal("twenty third")
23
>>> parse_ordinal("seventy fifth")
75

Parsing a fraction
------------------

Converting a fractional number written in words to its corresponding integral fraction. (Support for English only)

>>> from number_parser import parse_fraction
>>> parse_fraction("forty two divided by five hundred and six")
'42/506'
>>> parse_fraction("one over two")
'1/2'
>>> parse_fraction("forty two / one million")
'42/1000000'


Language Support
----------------

The default language is English, you can pass the language parameter with corresponding locale for other languages.
It currently supports cardinal numbers in the following
languages - English, Hindi, Spanish, Ukrainian and Russian and ordinal numbers in English.

>>> from number_parser import parse, parse_number
>>> parse("Hay tres gallinas y veintitrés patos", language='es')
'Hay 3 gallinas y 23 patos'
>>> parse_number("चौदह लाख बत्तीस हज़ार पाँच सौ चौबीस", language='hi')
1432524

Supported cases
---------------

The library has extensive tests.
Some of the supported cases are described below.

Accurately handling usage of conjunction while forming the number.

>>> parse("doscientos cincuenta y doscientos treinta y uno y doce", language='es')
'250 y 231 y 12'


Handling ambiguous cases without proper separators.

>>> parse("two thousand thousand")
'2000 1000'
>>> parse_number("two thousand two million")
2002000000


Handling nuances in the languag ith different forms of the same number.

>>> parse_number("пятисот девяноста шести", language='ru')
596
>>> parse_number("пятистам девяноста шести", language='ru')
596
>>> parse_number("пятьсот девяносто шесть", language='ru')
596

Contributing
============

* Source code: https://github.com/scrapinghub/number-parser
* Issue tracker: https://github.com/scrapinghub/number-parser/issues
