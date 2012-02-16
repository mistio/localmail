from twisted.application import service
from twisted.application import internet
from twisted.cred import portal, checkers

from smtp import TestServerESMTPFactory
from imap import TestServerIMAPFactory
from cred import TestServerRealm, CredentialsNonChecker


application = service.Application("Testing Email Server")

# setup auth
portal = portal.Portal(TestServerRealm())
portal.registerChecker(CredentialsNonChecker())
portal.registerChecker(checkers.AllowAnonymousAccess())

imapServerFactory = TestServerIMAPFactory()
imapServerFactory.portal = portal
smtpServerFactory = TestServerESMTPFactory(portal)

#context = ssl.DefaultOpenSSLContextFactory('keys/server.key', 'keys/server.crt')
imapServerService = internet.TCPServer(2143, imapServerFactory)
imapServerService.setServiceParent(application)

smtpServerService = internet.TCPServer(2025, smtpServerFactory)
smtpServerService.setServiceParent(application)
