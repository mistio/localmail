Localmail
=========

For local people.

Localmail is SMTP and IMAP server that writes/reads all messages into a single
in-memory mailbox. It is designed to be used to speed up running test suites on
systems that send email, such as new account sign up emails with confirmation
codes. It can also be used to test SMTP/IMAP client code.

Authentication is supported but completely ignored, and all senders and
receiver email addresses are treated the same. Messages are not persisted by
default, and will be lost on shutdown.  Optionally, you can log messages to
disk in mbox format.

It also supports a simple HTTP interface for reading the mail in the inbox.

Limitations
 - no SSL support, but coming

WARNING: not a real SMTP/IMAP server - not for production usage.

Install
=======

::

    pip install localmail


Run
===

There are multiple ways to run localmail

::

    twistd localmail

This will run localmail in the background, SMTP on port 2025 and IMAP on 2143,
It will log to a file ./twistd.log. Use the -n option if you want to run in
the foreground, like so.

::

    twistd -n localmail


You can pass in arguments to control parameters.

::

   twistd localmail --imap <port> --smtp <port> --http <port> --file localmail.mbox


Embedding
=========

If you want to embed localmail in another non-twisted program, such as test
runner, do the following.

::

    import threading
    import localmail

    thread = threading.Thread(
       target=localmail.run,
       args=(2025, 2143, 8880, 'localmail.mbox')
    )
    thread.start()

    ...

    localmail.shutdown_thread(thread)

This will run the twisted reactor in a separate thread, and shut it down on
exit.


Development
===========

::
    python setup.py develop

Testing
=======

The test suite is very simple, it uses the python stdlib imaplib and smtplib
modules as clients, rather than twisted IMAP/SMTP, so it's more integration
tests rather than unit tests.

To run the full suite, use tox to run on python 2.6, 2.7, and pypy.

To run the suite in the current version, or specific tests, use:

::
    python setup.py test [-s tests.test_localmail.SomeTestCase.test_something]
