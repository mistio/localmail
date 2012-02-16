import random
import email
from itertools import count
from cStringIO import StringIO

from zope.interface import implements

from twisted.mail import imap4

MAILBOXDELIMITER = "."
MSG_COUNTER = count()
MSG_COUNTER.next()


class IMAPUserAccount(object):
    implements(imap4.IAccount)

    def __init__(self, user):
        self.inbox = get_inbox(user)
        self.user = user

    def listMailboxes(self, ref, wildcard):
        "only support one folder"
        return [("INBOX", self.inbox)]

    def select(self, path, rw=True):
        "return the same mailbox for every path"
        return self.inbox

    def create(self, path):
        "nothing to create"
        pass

    def delete(self, path):
        "delete the mailbox at path"
        raise imap4.MailboxException("Permission denied.")

    def rename(self, oldname, newname):
        "rename a mailbox"
        pass

    def isSubscribed(self, path):
        "return a true value if user is subscribed to the mailbox"
        return True

    def subscribe(self, path):
        return True

    def unsubscribe(self, path):
        return True



class Message(object):
    implements(imap4.IMessage)
    def __init__(self, fp, flags, date):
        self.msg = email.message_from_file(fp)
        self.data = str(self.msg)
        self.uid = MSG_COUNTER.next()
        self.flags = set(flags)
        self.date = date
        self.payload = self.msg.get_payload()

    def getUID(self):
        return self.uid

    def getFlags(self):
        return self.flags

    def getInternalDate(self):
        return self.date

    def getHeaders(self, negate, *names):
        headers = {}
        if negate:
            for header in self.msg.keys():
                if header.upper() not in names:
                    headers[header.lower()] = self.msg.get(header, '')
        else:
            for name in names:
                headers[name.lower()] = self.msg.get(name, '')
        return headers


    def getBodyFile(self):
        return StringIO(self.payload)

    def getSize(self):
        return len(self.data)

    def isMultipart(self):
        return False

    def getSubPart(self, part):
        if part == 0:
            return self.payload
        raise IndexError


class MemoryIMAPMailbox(object):
    implements(imap4.IMailbox)

    def __init__(self):
        self.msgs = []
        self.listeners = []
        self.uidvalidity = random.randint(1000000, 9999999)

    def getHierarchicalDelimiter(self):
        return MAILBOXDELIMITER

    def getFlags(self):
        "return list of flags supported by this mailbox"
        return [r'\Seen', r'\Unseen', r'\Deleted',
                r'\Flagged', r'\Answered', r'\Recent']

    def getMessageCount(self):
        return len(self.msgs)

    def getRecentCount(self):
        return 0

    def getUnseenCount(self):
        return 0

    def isWriteable(self):
        return True

    def getUIDValidity(self):
        return self.uidvalidity

    def getUID(self, messageNum):
        return self.msgs[messageNum-1].uid

    def getUIDNext(self):
        return MSG_COUNTER.next()

    def fetch(self, msg_set, uid):
        if uid:
            messages = self._get_msgs_by_uid(msg_set)
        else:
            messages = self._get_msgs_by_seq(msg_set)
        return messages.items()

    def addListener(self, listener):
        self.listeners.append(listener)
        return True

    def removeListener(self, listener):
        self.listeners.remove(listener)
        return True

    def requestStatus(self, path):
        return imap4.statusRequestHelper(self, path)

    def addMessage(self, msg, flags=None, date=None):
        if flags is None: 
            flags = []
        self.msgs.append(Message(msg, flags, date))

    def _get_msgs_by_uid(self, msg_set):
        return dict((i+1,m) for i,m in enumerate(self.msgs)
                    if m.uid in msg_set)

    def _get_msgs_by_seq(self, msg_set):
        l = len(self.msgs)
        if not msg_set.last:
            msg_set.last = l
        d = dict()
        for i in msg_set:
            x = i - 1
            if -1 < x < l:
                d[i] = self.msgs[x]
        return d

    def store(self, msg_set, flags, mode, uid):
        if uid:
            messages = self._get_msgs_by_uid(msg_set)
        else:
            messages = self._get_msgs_by_seq(msg_set)
        setFlags = {}
        for seq, msg in messages.items():
            uid = self.getUID(seq)
            if mode == 0: # replace flags
                msg.flags = set(flags)
            else:
                for flag in flags:
                    # mode 1 is append, mode -1 is delete
                    if mode == 1 and flag not in msg.flags:
                        msg.flags.add(flag)
                    elif mode == -1 and flag in msg.flags:
                        msg.flags.remove(flag)
            setFlags[seq] = msg.flags
        return setFlags

    def expunge(self):
        "remove all messages marked for deletion"
        remove = []
        for i, msg in enumerate(self.msgs[:]):
            if r"\Deleted" in msg.flags:
                self.msgs.remove(msg)
                remove.append(msg.uid)
        return remove

    def destroy(self):
        "complete remove the mailbox and all its contents"
        raise imap4.MailboxException("Permission denied.")


INBOX = MemoryIMAPMailbox()
def get_inbox(email):
    return INBOX
