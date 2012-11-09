#!/usr/bin/env python
# TODO add lisence
#

from setuptools import setup

DESCRIPTION = """Test SMTP/IMAP server for local integration testing"""

LONG_DESCRIPTION = open('README.rst').read()

setup(name='localmail',
    version='0.1',
    author='Simon Davy',
    author_email='simon.davy@canonical.com',
    url='https://launchpad.net/localmail',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=['localmail', 'localmail.tests'],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Communications :: Email',
    ],
    install_requires=[
        "Twisted >= 11.0.0",
    ],
)
