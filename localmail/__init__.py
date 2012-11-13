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


def get_factories():
    auth = get_portal()
    smtpServerFactory = TestServerESMTPFactory(auth)
    imapServerFactory = TestServerIMAPFactory()
    imapServerFactory.portal = auth
    return smtpServerFactory, imapServerFactory


def get_services(smtp_port, imap_port):
    smtpFactory, imapFactory = get_factories()

    smtp = internet.TCPServer(smtp_port, smtpFactory)
    imap = internet.TCPServer(imap_port, imapFactory)

    return smtp, imap


def run(smtp_port=2025, imap_port=2143):
    from twisted.internet import reactor
    smtpFactory, imapFactory = get_factories()
    reactor.listenTCP(smtp_port, smtpFactory)
    reactor.listenTCP(imap_port, imapFactory)
    reactor.run(installSignalHandlers=0)


def shutdown_thread(thread):
    from twisted.internet import reactor
    reactor.callFromThread(reactor.stop)
    thread.join()
