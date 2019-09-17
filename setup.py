from setuptools import setup

setup(
    name='spiderutil',
    version='0.1.1',
    packages=['spiderutil', 'spiderutil.path', 'spiderutil.connector', 'spiderutil.network'],
    url='https://github.com/Thesharing/spiderutil',
    license='MIT',
    author='Thesharing',
    author_email='',
    description='Utilities for spider.',

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
