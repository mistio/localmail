from cStringIO import StringIO

from twisted.application import internet
from twisted.internet import defer
from twisted.mail import smtp
from twisted.mail.imap4 import LOGINCredentials, PLAINCredentials
from zope.interface import implements

from inbox import INBOX


class MemoryMessage(object):
    """Reads a message into a StringIO, and passes on to global inbox"""
    implements(smtp.IMessage)

    def __init__(self):
        self.file = StringIO()

    def lineReceived(self, line):
        self.file.write(line + '\n')

    def eomReceived(self):
        self.file.seek(0)
        INBOX.addMessage(self.file, [r'\Recent', r'\Unseen'])
        self.file.close()
        return defer.succeed(None)

    def connectionLost(self):
        self.file.close()


class MemoryDelivery(object):
    """Null-validator for email address - always delivers succesfully"""
    implements(smtp.IMessageDelivery)

    def validateTo(self, user):
        return MemoryMessage

    def validateFrom(self, helo, origin):
        return origin

    def receivedHeader(self, helo, origin, recipients):
        return 'Received: Test Server.'


class TestServerESMTPFactory(smtp.SMTPFactory):
    """Factort for SMTP connections that authenticates any user"""
    protocol = smtp.ESMTP
    challengers = {
        "LOGIN": LOGINCredentials,
        "PLAIN": PLAINCredentials
    }

    def buildProtocol(self, addr):
        p = smtp.SMTPFactory.buildProtocol(self, addr)
        p.challengers = self.challengers
        return p
