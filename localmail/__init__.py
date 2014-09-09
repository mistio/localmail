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
from twisted.application import service
from twisted.internet import reactor
from twisted.cred import portal, checkers
from .cred import TestServerRealm, CredentialsNonChecker
from .smtp import TestServerESMTPFactory
from .imap import TestServerIMAPFactory
from .http import TestServerHTTPFactory, index


class PortReporterTCPServer(service.Service, object):

    def __init__(self, name, port, factory, reportPort):
        self.name = name
        self.port = port
        self.factory = factory
        self.reportPort = reportPort

    def privilegedStartService(self):
        self.listeningPort = reactor.listenTCP(self.port, self.factory)
        if self.reportPort is not None:
            self.reportPort(self.name, self.listeningPort.getHost().port)
        return super(PortReporterTCPServer, self).privilegedStartService()

    def stopService(self):
        self.listeningPort.stopListening()
        return super(PortReporterTCPServer, self).stopService()


def get_portal():
    localmail_portal = portal.Portal(TestServerRealm())
    localmail_portal.registerChecker(CredentialsNonChecker())
    localmail_portal.registerChecker(checkers.AllowAnonymousAccess())
    return localmail_portal


def get_factories():
    auth = get_portal()
    smtpServerFactory = TestServerESMTPFactory(auth)
    imapServerFactory = TestServerIMAPFactory()
    imapServerFactory.portal = auth
    httpServerFactory = TestServerHTTPFactory(index)
    return smtpServerFactory, imapServerFactory, httpServerFactory


def get_services(smtp_port, imap_port, http_port, callback=None):
    smtpFactory, imapFactory, httpFactory = get_factories()

    smtp = PortReporterTCPServer('smtp', smtp_port, smtpFactory, callback)
    imap = PortReporterTCPServer('imap', imap_port, imapFactory, callback)
    http = PortReporterTCPServer('http', http_port, httpFactory, callback)

    return smtp, imap, http


def run(smtp_port=2025,
        imap_port=2143,
        http_port=8880,
        mbox_path=None,
        callback=None):
    from twisted.internet import reactor
    if mbox_path is not None:
        from localmail.inbox import INBOX
        INBOX.setFile(mbox_path)
    smtpFactory, imapFactory, httpFactory = get_factories()
    smtp = reactor.listenTCP(smtp_port, smtpFactory)
    imap = reactor.listenTCP(imap_port, imapFactory)
    http = reactor.listenTCP(http_port, httpFactory)
    if callback is not None:
        callback(smtp.getHost().port, imap.getHost().port, http.getHost().port)
    reactor.run(installSignalHandlers=0)


def shutdown_thread(thread):
    from twisted.internet import reactor
    reactor.callFromThread(reactor.stop)
    thread.join()
