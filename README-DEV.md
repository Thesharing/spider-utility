# Spider Utility

![Version](https://img.shields.io/pypi/v/spiderutil)
![Download](https://img.shields.io/pypi/dm/spiderutil)
![License](https://img.shields.io/pypi/l/spiderutil)
![Status](https://img.shields.io/pypi/status/spiderutil)

## Distribution

Refer to the official doc: https://packaging.python.org/guides/distributing-packages-using-setuptools/

```bash
python setup.py sdist
python setup.py bdist_wheel --universal
twine upload dist/*
```

## Doc Generation

### Installation

```bash
pip install sphinx recommonmark sphinx_rtd_theme
```

### Run

```bash
cd doc
sphinx-apidoc -o source -f ../spiderutil
make.bat html
cd ..
```

## Todo

- [ ]  Fulfill the docs

- [ ]  Multi-thread / multi-processing / Asycio

- [ ]  Decorator

- [ ]  Monitor

- [ ]  Unit tests
