import unittest
import imaplib
from helpers import (
    IMAPHelper,
    SMTPHelper,
    TESTMSG_DATA,
)


class AuthTestCase(unittest.TestCase):

    def test_smtp_any_auth_allowed(self):
        with SMTPHelper() as smtp:
            smtp.login('any', 'thing')
            smtp.send(*TESTMSG_DATA)
        with SMTPHelper() as smtp:
            smtp.login('something', 'else')
            smtp.send(*TESTMSG_DATA)

    def test_smtp_anonymous_allowed(self):
        with SMTPHelper() as smtp:
            smtp.send(*TESTMSG_DATA)

    def test_imap_any_auth_allowed(self):
        with IMAPHelper() as imap:
            imap.login('any', 'thing')
            assert imap.search('ALL') == []
        with IMAPHelper() as imap:
            imap.login('somthing', 'else')
            assert imap.search('ALL') == []

    def test_imap_anonymous_not_allowed(self):
        with self.assertRaises(imaplib.IMAP4.error):
            with IMAPHelper() as imap:
                imap.search('ALL') == []


class LocalmailTestCase(unittest.TestCase):

    def test_single_message(self):
        with SMTPHelper() as smtp:
            smtp.send(*TESTMSG_DATA)
        with IMAPHelper() as imap:
            imap.login()
            msg = imap.fetch('1')
            print msg



