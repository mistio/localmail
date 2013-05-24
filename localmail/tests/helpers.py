import smtplib
import imaplib
from email import message_from_string


class ContextHelper(object):
    def __enter__(self):
        return self.start()

    def __exit__(self, type=None, value=None, traceback=None):
        return self.stop()


def clean_inbox(host, port):
    imap = imaplib.IMAP4(host, port)
    imap.login('x', 'y')
    imap.select()
    success, data = imap.search(None, 'ALL')
    for msgs in data:
        if msgs:
            for id in msgs.split():
                imap.store(id, '+FLAGS', r'(\Deleted)')
    imap.expunge()
    imap.close()
    imap.logout()


class SMTPClient(ContextHelper):
    def __init__(self, host='localhost', port=2025, user='x', password='y'):
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    def start(self):
        self.client = smtplib.SMTP(self.host, self.port)
        #self.client.set_debuglevel(1)
        self.client.login(self.user, self.password)
        return self

    def stop(self):
        self.client.quit()

    def send(self, msg):
        self.client.sendmail(msg['From'], msg['To'], msg.as_string())


class IMAPClient(ContextHelper):
    def __init__(self,
            host='localhost',
            port=2143,
            username='x',
            password='y',
            uid=False):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.uid = uid

    def start(self):
        self.client = imaplib.IMAP4(self.host, self.port)
        self.client.login(self.username, self.password)
        self.client.select()
        return self

    def stop(self):
        self.client.close()
        self.client.logout()

    def call(self, func, *args):
        assert func in ('store', 'fetch', 'search')
        if self.uid:
            success, data = self.client.uid(func, *args)
        else:
            success, data = getattr(self.client, func)(*args)
        assert success == 'OK'
        return data

    def fetch(self, id):
        data = self.call('fetch', self.msgid(id), '(RFC822)')
        return message_from_string(data[0][1])

    def search(self, *terms):
        data = self.call('search', None, *terms)
        if data and data[0]:
            return data[0].split()
        else:
            return []

    def store(self, id, flags, type='+FLAGS'):
        return self.call('store', self.msgid(id), type, flags)

    def msgid(self, seq):
        seq = int(seq)
        if self.uid:
            msgs = self.search('ALL')
            if seq > len(msgs):
                return None
            msg_set = msgs[seq - 1]
        else:
            msg_set = str(seq)
        return msg_set
