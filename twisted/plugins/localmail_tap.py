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
try:
    from zope.interface import implements
except:
    # 6.0+
    from zope.interface import classImplements as implements

from twisted.application import service
from twisted import plugin
from twisted.python import usage

import localmail


class Options(usage.Options):
    optFlags = [
        ["random", "r", "Use random ports. Overides any other port options"],
    ]
    optParameters = [
        ["smtp", "s", 2025, "The port number the SMTP server will listen on"],
        ["imap", "i", 2143, "The port number the IMAP server will listen on"],
        ["http", "h", 8880, "The port number the HTTP server will listen on"],
        ["file", "f", None, "File to write messages to"],
    ]


class LocalmailServiceMaker(object):
    implements(service.IServiceMaker, plugin.IPlugin)
    tapname = "localmail"
    description = "A test SMTP/IMAP server"
    options = Options

    def makeService(self, options):
        svc = service.MultiService()
        svc.setName("localmail")
        if options['random']:
            smtp_port = imap_port = http_port = 0
        else:
            smtp_port = int(options['smtp'])
            imap_port = int(options['imap'])
            http_port = int(options['http'])

        smtp, imap, http = localmail.get_services(
            smtp_port, imap_port, http_port
        )
        if options['file']:
            from localmail.inbox import INBOX
            INBOX.setFile(options['file'])
        imap.setServiceParent(svc)
        smtp.setServiceParent(svc)
        http.setServiceParent(svc)
        return svc


# The name of this variable is irrelevant, as long as there is *some*
# name bound to a provider of IPlugin and IServiceMaker.
localmailServiceMaker = LocalmailServiceMaker()
