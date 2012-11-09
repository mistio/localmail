import smtplib
import imaplib
from email.mime.text import MIMEText


def print_msgs(imap, msgs):
    for num in msgs:
        typ, data = imap.fetch(num, '(RFC822)')
        print 'Message %s\n%s\n' % (num, data[0][1])

def send(s, from_, to, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_
    msg['To'] = to
    s.sendmail(from_, [to], msg.as_string())

def test():

    s = smtplib.SMTP('localhost', 2025)
    s.set_debuglevel(1)
    s.login('any', 'thing')


    print "Sending messages to SMTP"
    send('test@example.com', 'test+2@example.com', "test", "test\n" * 5)
    send('test@example.com', 'test+2@example.com', "test2", "test2\n" * 5)
    send('test@example.com', 'test2+2@example.com', "test3", "test3\n" * 5)
    send('test@example.com', 'test2+2@example.com', "test4", "test4\n" * 5)
    send('test@example.com', 'test2+3@example.com', "test5", "test5\n" * 5)
    s.quit()
    print "Done\n"

    m = imaplib.IMAP4('localhost', 2143)
    m.login("test@example.com", "xxx")
    m.select()

    def get(*terms):
        status, data = m.search(None, *terms)
        assert status == 'OK'
        if data and data[0]:
            return data[0].split()
        else:
            return []

    def remove(msgs):
        for num in msgs:
            print "deleting msg %s" % num
            m.store(num, '+FLAGS', r'\Deleted')
        m.expunge()

    msgs = get('TO', 'test+2@example.com')
    assert msgs, "Failed to get messages!"
    assert len(msgs) == 2, "Not 2 messages"
    print_msgs(m, msgs)
    remove(msgs)

    msgs = get('TO', 'test2+2@example.com')
    assert len(msgs) == 2, "Should have two messages"

    msgs = get('ALL')
    assert len(msgs) == 3, "Should have two messages"

    remove(msgs)

    m.close()
    m.logout()


if __name__ == '__main__':
    test()
