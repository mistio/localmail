#!/usr/bin/env python
#
# Copyright (C) 2012- Canonical Ltd
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

from setuptools import setup

DESCRIPTION = """Test SMTP/IMAP server for local integration testing"""

LONG_DESCRIPTION = open('README').read()

setup(
    name='localmail',
    version='0.2',
    author='Simon Davy',
    author_email='simon.davy@canonical.com',
    url='https://launchpad.net/localmail',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    license='GPLv3',
    packages=['localmail', 'localmail.tests', 'twisted.plugins'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Framework :: Twisted',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Intended Audience :: Developers',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2 :: Only',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Communications :: Email',
        'Topic :: Communications :: Email :: Mail Transport Agents',
        'Topic :: Communications :: Email :: Post-Office :: IMAP',
        'Topic :: Software Development :: Testing',
    ],
    install_requires=[
        "Twisted >= 11.0.0",
    ],
)

# Make Twisted regenerate the dropin.cache, if possible.  This is necessary
# because in a site-wide install, dropin.cache cannot be rewritten by
# normal users.
try:
    from twisted.plugin import IPlugin, getPlugins
except ImportError:
    pass
else:
    list(getPlugins(IPlugin))
