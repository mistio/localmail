from zope.interface import implements

from twisted.application import service
from twisted import plugin
from twisted.python import usage

from cred import setup_portal
from imap import setup_imap_server
from smtp import setup_smtp_server


class Options(usage.Options):
    optParameters = [
        ["smtp", "s", 2025, "The port number the SMTP server will listen on"],
        ["imap", "i", 2143, "The port number the IMAP server will listen on"]
    ]


class LocalmailServiceMaker(object):
    implements(service.IServiceMaker, plugin.IPlugin)
    tapname = "localmail"
    description = "Run localmail"
    options = Options

    def makeService(self, options):
        localmail = service.MultiService()
        localmail.setName("localmail")
        auth = setup_portal()
        imap = setup_imap_server(int(options['imap']), auth)
        imap.setServiceParent(localmail)
        smtp = setup_smtp_server(int(options['smtp']), auth)
        smtp.setServiceParent(localmail)
        return localmail


# The name of this variable is irrelevant, as long as there is *some*
# name bound to a provider of IPlugin and IServiceMaker.
localmailServiceMaker = LocalmailServiceMaker()
