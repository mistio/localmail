from email.parser import Parser
import glob

for file in glob.glob('*.txt'):
    print file
    msg = Parser().parse(open(file, 'rb'))
    print "Type: ", msg.get_content_type()
    for k, v in msg.items():
        print("%s: %s" % (k, v))
    for part in msg.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        print "PART:"
        print part.get_content_type()
        print part.get_payload()[:150]
        print
    print
    print "-------------------------------------------------"
    print
