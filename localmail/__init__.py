from twisted.application import internet
from twisted.cred import portal, checkers
from .cred import TestServerRealm, CredentialsNonChecker
from .smtp import TestServerESMTPFactory
from .imap import TestServerIMAPFactory


def get_portal():
    localmail_portal = portal.Portal(TestServerRealm())
    localmail_portal.registerChecker(CredentialsNonChecker())
    localmail_portal.registerChecker(checkers.AllowAnonymousAccess())
    return localmail_portal


def get_services(smtp_port, imap_port):
    auth = get_portal()

    smtpServerFactory = TestServerESMTPFactory(auth)
    smtp = internet.TCPServer(smtp_port, smtpServerFactory)

    imapServerFactory = TestServerIMAPFactory()
    imapServerFactory.portal = auth
    imap = internet.TCPServer(imap_port, imapServerFactory)

    return smtp, imap


def run(smtp_port, imap_port):
    import reactor
    reactor.install()
    auth = get_portal()

    smtpServerFactory = TestServerESMTPFactory(auth)
    reactor.listenTCP(smtp_port, smtpServerFactory)

    imapServerFactory = TestServerIMAPFactory()
    imapServerFactory.portal = auth
    reactor.listenTCP(imap_port, imapServerFactory())

    reactor.run()
