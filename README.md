# Spider Utility

![Version](https://img.shields.io/pypi/v/spiderutil)
![Download](https://img.shields.io/pypi/dm/spiderutil)
![License](https://img.shields.io/pypi/l/spiderutil)
![Status](https://img.shields.io/pypi/status/spiderutil)

Utilities for spider, including connectors to databases, path generators, loggers and exceptions.

## Docs

### Connector

#### MongoDB

#### Redis

#### LocalFolder

#### LocalFile

### Network

#### Session

#### User Agent

### Path Generator

#### Store Simply

#### Store By UserName

#### Store By User Name Per Folder

### Data Structure

#### Dict

#### TextDict

### Log

#### Logger

### Exceptions

### Typing

#### Media Type

## Recommend packages

* BeautidfulSoup: beautifulsoup4

* Parsel: parsel

* Brotli: brotli

## How to contribute

### Distribute

Refer to the official doc: https://packaging.python.org/guides/distributing-packages-using-setuptools/

```bash
python setup.py sdist
python setup.py bdist_wheel --universal
twine upload dist/*
```

## Todo

* Fulfill the docs

* Multi-thread / multi-processing / Asycio

* Decorator

* Monitor
