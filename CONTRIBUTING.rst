Contributing
============

To set up a development environment, create a virtualenv and then run the
following in it. The main dependency is twisted, and tox for running tests,
and flake8 for linting. Unittest2 is pulled in of you are on python 2.6.

::
    python setup.py develop

Testing
-------

The test suite is very simple. It starts localmail in a thread listening on
random ports. The tests then run in the main thread using the python stdlib
imaplib and smtplib modules as clients, so it's more integration tests rather
than unit tests.

I probably should add some proper unit tests and use twisted's SMTP/IMAP
clients as well, but twisted.trial scares me a little.

To run the full suite, use tox to run on python 2.6, 2.7, and pypy. Works in
parallel with detox too, thanks to using random ports, for faster runs.

::

    make test

Note: this will also run flake8, which is required to pass to merge.

To run the suite manually, or with specific tests, use:

::
    python setup.py test [-s tests.test_localmail.SomeTestCase.test_something]
