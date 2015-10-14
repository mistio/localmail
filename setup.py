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

__VERSION__ = "0.4.1"

# hide behind main to setup can be imported to find __VERSION__
if __name__ == '__main__':

    import sys
    from setuptools import setup, find_packages

    DESCRIPTION = """Test SMTP/IMAP server for local integration testing"""

    LONG_DESCRIPTION = (open('README.rst').read() + '\n\n' +
                        open('HISTORY.rst').read() + '\n\n' +
                        open('AUTHORS.rst').read())

    test_requirements = ['tox', 'flake8']
    if sys.version_info[1] < 7:
        test_requirements.append('unittest2')
        test_suite = 'unittest2.collector'
    else:
        test_suite = 'tests'

    setup(
        name='localmail',
        version=__VERSION__,
        author='Simon Davy',
        author_email='simon.davy@canonical.com',
        url='https://launchpad.net/localmail',
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        license='GPLv3',
        packages=find_packages(exclude=["tests*"]) + ['twisted.plugins'],
        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Framework :: Twisted',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Intended Audience :: Developers',
            'Operating System :: POSIX',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: Implementation :: CPython',
            'Programming Language :: Python :: Implementation :: PyPy',
            'Topic :: Communications :: Email',
            'Topic :: Communications :: Email :: Mail Transport Agents',
            'Topic :: Communications :: Email :: Post-Office :: IMAP',
            'Topic :: Software Development :: Testing',
        ],
        include_package_data=True,
        install_requires=[
            'Twisted >= 11.0.0',
            'jinja2 >= 2.0.0',
        ],
        tests_require=test_requirements,
        test_suite=test_suite,
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
