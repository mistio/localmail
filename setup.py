#!/usr/bin/env python

from distutils.core import setup

DESCRIPTION = """Test STMP/IMAP server for local integration testing"""

LONG_DESCRIPTION = DESCRIPTION + "\n" + """
Runs a local SMTP server that dumps all messages into a single in-memory
mailbox, and an IMAP server that can read them. It is designed to be used to
speed up testing scenarios when you need to test systems that send email.

Authentication is supported but completely ignored, and all senders and
receiver email addresses are treated the same. Messages are not persisted, and
will be lost on shutdown.

WARNING: not a real SMTP/IMAP server - not for production usage.
"""

setup(name='localmail',
    version='0.1',
    author='Simon Davy',
    author_email='simon.davy@canonical.com',
    url='https://code.launchpad.net/~bloodearnest/+junk/test-email-server',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=['localmail'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Communications :: Email',
    ],

)
