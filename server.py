from twisted.application import service
from twisted.application import internet
from twisted.cred import portal

from smtp import TestServerESMTPFactory
from imap import MailUserRealm, CredentialsChecker, IMAPFactory

application = service.Application("Testing Email Server")

portal = portal.Portal(MailUserRealm())
checker = CredentialsChecker()
portal.registerChecker(checker)
imapServerFactory = IMAPFactory()
imapServerFactory.portal = portal
imapServerService = internet.TCPServer(2143, imapServerFactory)
imapServerService.setServiceParent(application)

smtpServerFactory = TestServerESMTPFactory()
smtpServerService = internet.TCPServer(2025, smtpServerFactory)
smtpServerService.setServiceParent(application)
