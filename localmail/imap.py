from twisted.application import internet
from twisted.internet import protocol
from twisted.mail import imap4
from zope.interface import implements

from inbox import INBOX


class IMAPUserAccount(object):
    implements(imap4.IAccount)

    def listMailboxes(self, ref, wildcard):
        "only support one folder"
        return [("INBOX", INBOX)]

    def select(self, path, rw=True):
        "return the same mailbox for every path"
        return INBOX

    def create(self, path):
        "nothing to create"
        pass

    def delete(self, path):
        "delete the mailbox at path"
        raise imap4.MailboxException("Permission denied.")

    def rename(self, oldname, newname):
        "rename a mailbox"
        pass

    def isSubscribed(self, path):
        "return a true value if user is subscribed to the mailbox"
        return True

    def subscribe(self, path):
        return True

    def unsubscribe(self, path):
        return True


class IMAPServerProtocol(imap4.IMAP4Server):
    "Subclass of imap4.IMAP4Server that adds debugging."
    debug = True

    def lineReceived(self, line):
        if self.debug:
            print "CLIENT:", line
        imap4.IMAP4Server.lineReceived(self, line)

    def sendLine(self, line):
        imap4.IMAP4Server.sendLine(self, line)
        if self.debug:
            print "SERVER:", line


class TestServerIMAPFactory(protocol.Factory):
    protocol = IMAPServerProtocol
    portal = None  # placeholder

    def buildProtocol(self, address):
        p = self.protocol()
        # self.portal will be set up already "magically"
        p.portal = self.portal
        p.factory = self
        return p
