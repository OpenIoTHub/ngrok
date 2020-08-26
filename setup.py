#!/usr/bin/env python
from __future__ import division, print_function

import os

from setuptools import setup
def read(*names, **kwargs):
    import io
    with io.open(
            os.path.join(os.path.dirname(__file__), *names),
            encoding=kwargs.get("encoding", "utf8")
    ) as fp:
        return fp.read()


def find_version(*file_paths):
    import re
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")
long_description = """
==========
Ngrok NAT Downloader for Pyhton
==========
"""
entry_points = {
        'console_scripts': ['ngrok=ngrok:_main'],
    }
setup(
    name='ngrok',
    py_modules=['ngrok'],
    version=find_version("ngrok.py"),
    description='ngrok NAT.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/OpenIoTHub/ngrok',
    author='Farry',
    author_email='yu@iotserv.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Environment :: Console',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    tests_require=[],
    install_requires=["ping",],
    scripts=None,
    entry_points=entry_points,
)
