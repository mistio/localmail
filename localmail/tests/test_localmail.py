import os
import time
import threading
import imaplib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

try:
    import unittest2 as unittest
except ImportError:
    import unittest  # NOQA

import localmail

from helpers import (
    SMTPClient,
    IMAPClient,
    clean_inbox,
)

thread = None

HOST = 'localhost'
SMTP_PORT = 2025
IMAP_PORT = 2143

if 'LOCALMAIL_EXTERNAL' not in os.environ:
    def setUpModule():
        global thread
        thread = threading.Thread(target=localmail.run, args=(2025, 2143))
        thread.start()
        time.sleep(1)

    def tearDownModule():
        localmail.shutdown_thread(thread)


class BaseLocalmailTestcase(unittest.TestCase):

    def setUp(self):
        super(BaseLocalmailTestcase, self).setUp()
        self.addCleanup(clean_inbox, HOST, IMAP_PORT)


class AuthTestCase(BaseLocalmailTestcase):

    def test_smtp_any_auth_allowed(self):
        smtp = smtplib.SMTP(HOST, SMTP_PORT)
        smtp.login('a', 'b')
        smtp.sendmail('a@b.com', ['c@d.com'], 'Subject: test\n\ntest')
        smtp.quit()
        smtp = smtplib.SMTP(HOST, SMTP_PORT)
        smtp.login('c', 'd')
        smtp.sendmail('a@b.com', ['c@d.com'], 'Subject: test\n\ntest')
        smtp.quit()

    def test_smtp_anonymous_allowed(self):
        smtp = smtplib.SMTP(HOST, SMTP_PORT)
        smtp.sendmail('a@b.com', ['c@d.com'], 'Subject: test\n\ntest')
        smtp.quit()

    def test_imap_any_auth_allowed(self):
        imap = imaplib.IMAP4(HOST, IMAP_PORT)
        imap.login('any', 'thing')
        imap.select()
        self.assertEqual(imap.search('ALL'), ('OK', [None]))
        imap.close()
        imap.logout()

        imap = imaplib.IMAP4(HOST, IMAP_PORT)
        imap.login('other', 'something')
        imap.select()
        self.assertEqual(imap.search('ALL'), ('OK', [None]))
        imap.close()
        imap.logout()

    def test_imap_anonymous_not_allowed(self):
        imap = imaplib.IMAP4(HOST, IMAP_PORT)
        with self.assertRaises(imaplib.IMAP4.error):
            imap.select()
            self.assertEqual(imap.search('ALL'), ('OK', [None]))


class SequentialIdTestCase(BaseLocalmailTestcase):
    uid = False

    def setUp(self):
        super(SequentialIdTestCase, self).setUp()
        self.smtp = SMTPClient()
        self.smtp.start()
        self.imap = IMAPClient(uid=self.uid)
        self.imap.start()
        msgs = self.imap.search('ALL')
        self.assertEqual(msgs, [])
        self.addCleanup(self.smtp.stop)
        self.addCleanup(self.imap.stop)

    def _testmsg(self, n):
        msg = MIMEText("test %s" % n)
        msg['Subject'] = "test %s" % n
        msg['From'] = 'from%s@example.com' % n
        msg['To'] = 'to%s@example.com' % n
        return msg

    def assert_message(self, msg, n):
        expected = self._testmsg(n)
        self.assertEqual(msg['From'], expected['From'])
        self.assertEqual(msg['To'], expected['To'])
        self.assertEqual(msg['Subject'], expected['Subject'])
        self.assertEqual(msg.is_multipart(), expected.is_multipart())
        if msg.is_multipart():
            for part, expected_part in zip(msg.walk(), expected.walk()):
                self.assertEqual(part.get_content_maintype(),
                                 expected_part.get_content_maintype())
                if part.get_content_maintype() != 'multipart':
                    self.assertEqual(part.get_payload().strip(),
                                     expected_part.get_payload().strip())
        else:
            self.assertEqual(msg.get_payload().strip(),
                             expected.get_payload().strip())

    def test_simple_message(self):
        self.smtp.send(self._testmsg(1))
        msg = self.imap.fetch(1)
        self.assert_message(msg, 1)

    def test_multiple_messages(self):
        self.smtp.send(self._testmsg(1))
        self.smtp.send(self._testmsg(2))
        msg1 = self.imap.fetch(1)
        msg2 = self.imap.fetch(2)
        self.assert_message(msg1, 1)
        self.assert_message(msg2, 2)

    def test_delete_single_message(self):
        self.smtp.send(self._testmsg(1))
        self.imap.store(1, '(\Deleted)')
        self.imap.client.expunge()
        self.assertEqual(self.imap.search('ALL'), [])

    def test_delete_with_multiple(self):
        self.smtp.send(self._testmsg(1))
        self.smtp.send(self._testmsg(2))
        self.imap.store(1, '(\Deleted)')
        self.imap.client.expunge()
        self.assertEqual(self.imap.search('ALL'), [self.imap.msgid(1)])

    def test_search_deleted(self):
        self.smtp.send(self._testmsg(1))
        self.smtp.send(self._testmsg(2))
        self.imap.store(1, '(\Deleted)')
        self.assertEqual(self.imap.search('(DELETED)'),
                [self.imap.msgid(1)])
        self.assertEqual(self.imap.search('(NOT DELETED)'),
                [self.imap.msgid(2)])


class UidTestCase(SequentialIdTestCase):
    uid = True


class MultipartTestCase(SequentialIdTestCase):

    def _testmsg(self, n):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'test %s' % n
        msg['From'] = 'from%s@example.com' % n
        msg['To'] = 'to%s@example.com' % n
        html = MIMEText('<b>test %s</b>' % n, 'html')
        text = MIMEText('test %s' % n, 'plain')
        msg.attach(html)
        msg.attach(text)
        return msg
