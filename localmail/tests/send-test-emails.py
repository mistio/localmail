import glob
import sys
from email.parser import Parser
import smtplib

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 2025
    smtp = smtplib.SMTP("localhost", port)
    for file in glob.glob('spam/*.txt'):
        msg = Parser().parse(open(file, 'rb'))
        smtp.sendmail('a@b.com', ['a@b.com'], msg.as_string())
