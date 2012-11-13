# Copyright (C) 2012- Canonical Ltd
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
from twisted.internet import protocol
from twisted.mail import imap4
from twisted.python import log
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
    debug = False

    def lineReceived(self, line):
        if self.debug:
            log.msg("CLIENT:", line)
        imap4.IMAP4Server.lineReceived(self, line)

    def sendLine(self, line):
        imap4.IMAP4Server.sendLine(self, line)
        if self.debug:
            log.msg("SERVER:", line)


class TestServerIMAPFactory(protocol.Factory):
    protocol = IMAPServerProtocol
    portal = None  # placeholder

    def buildProtocol(self, address):
        p = self.protocol()
        # self.portal will be set up already "magically"
        p.portal = self.portal
        p.factory = self
        return p
