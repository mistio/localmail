import smtplib
import imaplib

if __name__ == '__main__':
    s = smtplib.SMTP('localhost', 2025)
    s.sendmail('test@example.com', ['test@example.com'], "test")
    s.sendmail('test@example.com', ['test@example.com'], "test2!")
    s.quit()

    m = imaplib.IMAP4('localhost', 2143)
    m.login("test@example.com", "xxx")
    m.select()
    typ, data = m.search(None, 'ALL')
    if data[0]:
        for num in data[0].split():
            typ, data = m.fetch(num, '(RFC822)')
            print 'Message %s\n%s\n' % (num, data[0][1])
    m.close()
    m.logout()



