import sys
import threading
import localmail

from twisted.python import log
log.startLogging(sys.stdout)

from simple import test

thread = threading.Thread(target=localmail.run, args=(2025, 2143))
thread.start()

print "Starting run"
try:
    test()
except:
    pass

localmail.shutdown_thread(thread)
