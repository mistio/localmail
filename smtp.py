from cStringIO import StringIO

from zope.interface import implements

from twisted.python import log
from twisted.internet import protocol, defer
from twisted.mail import smtp

from inbox import get_inbox

class MemoryMessage(object):
    """Reads a message into a StringIO"""
    implements(smtp.IMessage)

    def __init__(self, user):
        self.inbox = get_inbox(user)
        self.file = StringIO()

    def lineReceived(self, line):
        log.msg("recv: " + line)
        self.file.write(line + '\n')

    def eomReceived(self):
        self.file.seek(0)
        self.inbox.addMessage(self.file)#, [r'\Recent', r'\Unseen'])
        self.file.close()
        return defer.succeed(None)

    def connectionLost(self):
        self.file.close()

class MemoryDelivery(object):
    implements(smtp.IMessageDelivery)

    def validateTo(self, user):
        email = str(user)
        if '+' in email:
            name, domain = email.split('@')
            email = email.split('+')[0] + '@' + domain
        return lambda: MemoryMessage(email)

    def validateFrom(self, helo, origin):
        return origin

    def receivedHeader(self, helo, origin, recipients):
        return 'Received: Test Server.'

class TestServerDeliveryFactory(object):
    implements(smtp.IMessageDeliveryFactory)

    def getMessageDelivery(self):
        return MemoryDelivery()

class TestServerESMTPFactory(protocol.ServerFactory):
    protocol = smtp.ESMTP

    def buildProtocol(self, addr):
        p = self.protocol()
        p.deliveryFactory = TestServerDeliveryFactory()
        p.factory = self
        return p

