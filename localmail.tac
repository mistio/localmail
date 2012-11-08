from twisted.application import service

from cred import setup_portal
from imap import setup_imap_server
from smtp import setup_smtp_server

application = service.Application("localmail")
auth = setup_portal()
smtp = setup_smtp_server(2025, auth)
smtp.setServiceParent(application)
imap = setup_imap_server(2143, auth)
imap.setServiceParent(application)
