
import threading
import localmail

from simple import test
thread = threading.Thread(target=localmail.run_thread, args=(2025, 2143))
thread.start()

print "Starting run"
try:
    test()
except:
    pass

localmail.shutdown_thread(thread)
