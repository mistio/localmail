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
from cStringIO import StringIO

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
