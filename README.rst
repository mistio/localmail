Localmail
=========

For local people.

Localmail is an SMTP and IMAP server that stores all messages into a single
in-memory mailbox. It is designed to be used to speed up running test suites on
systems that send email, such as new account sign up emails with confirmation
codes. It can also be used to test SMTP/IMAP client code.

Features:

  * Fast and robust IMAP/SMTP implementations, including multipart
    messages and unicode support.

  * Includes simple HTTP interface for reading messages, which is useful for
    checking html emails.

  * Compatible with python's stdlib client, plus clients like mutt and
    thunderbird.

  * Authentication is supported but completely ignored, all message go in
    single mailbox.

  * Messages not persisted by default, and will be lost on shutdown.
    Optionally, you can log messages to disk in mbox format.

Missing features/TODO:

  * SSL support

WARNING: not a real SMTP/IMAP server - not for production usage.


Running localmail
-----------------

.. code-block:: bash

    twistd -y localmail mail

This will run localmail in the background, SMTP on port 2025 and IMAP on 2143,
It will log to a file ./twistd.log. Use the -n option if you want to run in
the foreground, like so.

.. code-block:: bash

    twistd -n -y localmail mail


You can pass in arguments to control parameters.

.. code-block:: bash

   twistd  localmail --imap <port> --smtp <port> --http <port> --file localmail.mbox


You can have localmail use random ports if you like. The port numbers will be logged.
TODO: enable writing random port numbers to a file.

.. code-block:: bash

   twisted -n localmail --random


Embedding
---------

If you want to embed localmail in another non-twisted program, such as test
runner, do the following.

.. code-block:: python

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

If you want to use random ports, you can pass a callback that will have the
ports the service is listening on.

.. code-block:: python

    import threading
    import localmail

    def report(smtp, imap, http):
        """do stuff with ports"""

    thread = threading.Thread(
       target=localmail.run,
       args=(0, 0, 0, None, report)
    )
    thread.start()


