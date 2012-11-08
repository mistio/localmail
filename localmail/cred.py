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
