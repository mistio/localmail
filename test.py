import smtplib
import imaplib
from email.mime.text import MIMEText

def print_msgs(imap, msgs):
    for num in msgs:
        typ, data = m.fetch(num, '(RFC822)')
        print 'Message %s\n%s\n' % (num, data[0][1])



if __name__ == '__main__':
    s = smtplib.SMTP('localhost', 2025)
    s.set_debuglevel(1)
    def send(from_, to, subject, body):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = from_
        msg['To'] = to
        s.sendmail(from_, [to], msg.as_string())

    send('test@example.com', 'test@example.com', "test", "test\n"*5)
    send('test@example.com', 'test@example.com', "test2", "test2\n"*5)
    send('test@example.com', 'test2@example.com', "test3", "test3\n"*5)
    send('test@example.com', 'test2@example.com', "test4", "test4\n"*5)

    s.quit()

    m = imaplib.IMAP4_SSL('localhost', 2143)
    m.login("test@example.com", "xxx")
    m.select()

    status, data = m.search(None, 'TO', 'test@example.com')
    assert status == 'OK'
    assert data[0], "Failed to get messages!"

    msgs = data[0].split()
    assert len(msgs) == 2, "Not 2 messages"
    print_msgs(m, msgs)

    print "deleting"
    for num in msgs:
        m.store(num, '+FLAGS', r'\Deleted')
    m.expunge()

    status, data = m.search(None, 'ALL')
    assert data[0], "Should have messages"
    assert status == 'OK'
    msgs = data[0].split()
    assert len(msgs) == 2

    m.close()
    m.logout()



