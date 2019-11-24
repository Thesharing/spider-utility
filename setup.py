from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='spiderutil',
    version='0.1.6',
    packages=['spiderutil', 'spiderutil.path', 'spiderutil.connector',
              'spiderutil.network', 'spiderutil.structure'],
    url='https://github.com/Thesharing/spider-utility',
    license='MIT',
    author='Thesharing',
    author_email='',
    description='Utilities for spider.',
    long_description=long_description,
    long_description_content_type='text/markdown',

    install_requires=[
        'redis>=3.3.0',
        'pymongo>=3.8.0',
        'requests>=2.20.0'
    ],

    zip_safe=False,

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ],

    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, <4',
)
