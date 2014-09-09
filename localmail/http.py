from email.header import decode_header

from twisted.web.server import Site
from twisted.web.resource import Resource

from localmail.inbox import INBOX

index_template = u"""\
<!DOCTYPE html>
<html lang="en">
  <head>
    <title>localmail</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap-theme.min.css">
    <script src="https://code.jquery.com/jquery-2.1.1.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js"></script>
    <style>
        table.headers {{
            display: none;
        }}
        .summary .from    {{
            display: inline-block;
            width: 15em;
            overflow: hidden;
            margin: 0;
            padding 0;
        }}
        #inbox ul {{
            margin: 0;
            padding: 0;
            list-style-type: none;
        }}
        .msg {{
            display: none;
        }}
        #messages {{
            border: 2px solid grey;
        }}
    </style>
    <script type="text/javascript">
        $(function() {{
            $('.link').click(function(ev) {{
                console.log('here');
                $('.link').each(function(i, elem) {{
                    $($(elem).attr('href')).hide();
                }});
                console.log($(this).attr('href'));
                $($(this).attr('href')).show();
            }});
        }});
    </script>
  </head>
  <body>
    <div class="container-fluid">
      <div class="row">
        <section id="inbox" class="col-md-4">
        {inbox}
        </section>
        <section id="messages" class="col-md-8">
        {messages}
        </section>
      </div>
    </div>
  </body>
</html>"""

msg_template = u"""\
<article class="msg" id="{uid}">
<header class="subject">{subject}<header>
<hr/>
<p class="headline">
  <span class="from">From: {frm}</span>
  <span class="to">To: {to}</span>
  <span class="date">{date}</span>
</p>
<p>Show headers</p>
<table class="headers">
{headers}
</table>
{payloads}
</article>
"""

summary_template = u"""\
<li class="summary">
  <a href="#{uid}" class="link">
  <p class="subject">{subject}</p>
  <p class="from">{frm}</p>
  </a>
</li>
"""


class TestServerHTTPFactory(Site):
    pass


class Index(Resource):
    isLeaf = True

    def render_GET(self, request):
        request.setHeader('Content-type', 'text/html; charset=utf-8')
        return index_template.format(
            inbox=self.get_inbox(),
            messages=self.get_messages(),
        ).encode('utf8')

    def get_inbox(self):
        return u"<ul>{}</ul>".format(u"\n".join(self.get_summaries()))

    def get_messages(self):
        return u"\n".join(self.get_full_messages())

    def get_summaries(self):
        for msg in INBOX.msgs:
            yield summary_template.format(
                uid=msg.uid,
                frm=unicode_header(msg.msg['From']),
                subject=unicode_header(msg.msg['Subject'])
            )

    def get_full_messages(self):
        for msg in INBOX.msgs:
            yield msg_template.format(
                to=msg.msg['To'],
                date=msg.date,
                frm=unicode_header(msg.msg['From']),
                subject=unicode_header(msg.msg['Subject']),
                uid=msg.uid,
                headers=self.header(msg),
                payloads=u"\n".join(self.payloads(msg)),
            )

    def header(self, msg):
        header = u'<tr><td>{}</td><td>{}</td></tr>'
        return u"\n".join(
            header.format(k, unicode_header(v)) for k, v in msg.msg.items()
        )

    def payloads(self, msg):
        for part in msg.msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            content_type = part.get_content_type()
            if 'text/html' in content_type:
                tag = u'div'
            else:
                tag = u'pre'
            enc = part.get_charset()
            payload = part.get_payload(decode=True)
            if enc is None:
                enc = parse_charset(part['Content-Type'])
            yield u"<{0}>{1}</{0}>".format(tag, payload.decode(enc))


def parse_charset(content_type, default='utf8'):
    for chunk in content_type.split(';'):
        if 'charset' in chunk:
            return chunk.split('=')[1]
    return default


def unicode_header(header):
    orig, enc = decode_header(header)[0]
    if enc is None:
        enc = 'ascii'
    return orig.decode(enc)

index = Index()
