from zope.interface import implements

from twisted.application import service
from twisted import plugin
from twisted.python import usage

import localmail


class Options(usage.Options):
    optParameters = [
        ["smtp", "s", 2025, "The port number the SMTP server will listen on"],
        ["imap", "i", 2143, "The port number the IMAP server will listen on"]
    ]


class LocalmailServiceMaker(object):
    implements(service.IServiceMaker, plugin.IPlugin)
    tapname = "localmail"
    description = "A test SMTP/IMAP server"
    options = Options

    def makeService(self, options):
        svc = service.MultiService()
        svc.setName("localmail")
        smtp, imap = localmail.get_services(
            int(options['smtp']),
            int(options['imap'])
        )
        imap.setServiceParent(svc)
        smtp.setServiceParent(svc)
        return svc


# The name of this variable is irrelevant, as long as there is *some*
# name bound to a provider of IPlugin and IServiceMaker.
localmailServiceMaker = LocalmailServiceMaker()
