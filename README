Localmail
=========

Localmail is SMTP and IMAP server that writes/reads all messages into a single
in-memory mailbox. It is designed to be used to speed up running test suites on
systems that send email, such as new account sign up emails with confirmation
codes.

Authentication is supported but completely ignored, and all senders and
receiver email addresses are treated the same. Messages are not persisted, and
will be lost on shutdown.

Limitations
 - logging is bit verbose
 - no SSL support
 - very simple tests

WARNING: not a real SMTP/IMAP server - not for production usage.

Install
=======

Localmail depends on Twisted, tested with version 11.0.0 and up.

::

    pip install Twisted

Run
===

There are multiple ways to run localmail

::

    twistd localmail

This will run localmail in the background, SMTP on port 2025 and IMAP on 2143,
It will log to a file twistd.log. Use the -n option if you want to run oin the
foreground, like so.

::

    twistd -n localmail

You can pass in arguments to control parameters.

::

   twistd localmail --imap <port> --smtp <port> -l localmail.log

Alternatively, run via tac file:

::

    twistd -y localmail.tac

Embedding
=========

If you want to embed localmail in another non-twisted program, such as test
runner, do the following.

::

    import threading
    import localmail

    thread = threading.Thread(target=localmail.run, args=(2025, 2143))
    thread.start()

    ...

    localmail.shutdown_thread(thread)

This will run the twisted reactor in a separate thread, and shut it down on
exit.


Testing
=======

The test suite is very simple, it uses the python stdlib imaplib and smtplib
modules as clients, rather than twisted IMAP/SMTP, so it's more integration
tests rather than unit tests

::

    ./test.sh
