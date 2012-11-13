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
from zope.interface import implements
from twisted.internet import defer
from twisted.cred import portal, checkers, credentials
from twisted.mail import smtp, imap4

from imap import IMAPUserAccount
from smtp import MemoryDelivery


class TestServerRealm(object):
    implements(portal.IRealm)
    avatarInterfaces = {
        imap4.IAccount: IMAPUserAccount,
        smtp.IMessageDelivery: MemoryDelivery,
    }

    def requestAvatar(self, avatarId, mind, *interfaces):
        for requestedInterface in interfaces:
            if requestedInterface in self.avatarInterfaces:
                avatarClass = self.avatarInterfaces[requestedInterface]
                avatar = avatarClass()
                # null logout function: take no arguments and do nothing
                logout = lambda: None
                return defer.succeed((requestedInterface, avatar, logout))

        # none of the requested interfaces was supported
        raise KeyError("None of the requested interfaces is supported")


class CredentialsNonChecker(object):
    implements(checkers.ICredentialsChecker)
    credentialInterfaces = (credentials.IUsernamePassword,
                            credentials.IUsernameHashedPassword)

    def requestAvatarId(self, credentials):
        """automatically validate *any* user"""
        return credentials.username
