import smtplib
import imaplib
from email.mime.text import MIMEText


class ContextHelper(object):
    def __enter__(self):
        return self.start()

    def __exit__(self, type=None, value=None, traceback=None):
        return self.stop()


class SMTPHelper(ContextHelper):
    def __init__(self, host='localhost', port=2025):
        self.host = host
        self.port = port

    def start(self):
        self.smtp = smtplib.SMTP(self.host, self.port)
        #self.smtp.set_debuglevel(1)
        return self

    def stop(self):
        self.smtp.quit()

    def login(self, un='', pw=''):
        self.smtp.login(un, pw)

    def send(self, from_, to, subject, body):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = from_
        msg['To'] = to
        self.smtp.sendmail(from_, [to], msg.as_string())


class IMAPHelper(ContextHelper):
    def __init__(self, host='localhost', port=2143):
        self.host = host
        self.port = port

    def start(self):
        self.imap = imaplib.IMAP4(self.host, self.port)
        return self

    def stop(self):
        self.remove(self.search('ALL'))
        self.imap.close()
        self.imap.logout()

    def login(self, un='', pw=''):
        self.imap.login(un, pw)
        self.imap.select()

    def fetch(self, seq):
        typ, data = self.imap.fetch(seq, '(RFC822)')
        return data[0][1]

    def search(self, *terms):
        status, data = self.imap.search(None, *terms)
        assert status == 'OK'
        if data and data[0]:
            return data[0].split()
        else:
            return []

    def remove(self, msgs):
        for num in msgs:
            self.imap.store(num, '+FLAGS', r'\Deleted')
        self.imap.expunge()


TESTMSG_DATA = (
    'test@example.com',
    'test2@example.com',
    "test",
    "test\n" * 3
)
