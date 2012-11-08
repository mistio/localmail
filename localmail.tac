from twisted.application import service

import localmail

application = service.Application("localmail")
smtp, imap = localmail.get_services(2025, 2143)
smtp.setServiceParent(application)
imap.setServiceParent(application)
