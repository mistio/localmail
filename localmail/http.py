
from twisted.web.server import Site
from twisted.web.resource import Resource

from localmail.inbox import INBOX


class Index(Resource):
    isLeaf = True

    def render_GET(self, request):
        x = "\n".join("<li>%s</li>" % m.msg['Subject'] for m in INBOX.msgs)
        return "<html><body><h1>Localmail</h1><div><ul>%s</ul></div></body></html>" % x

index = Index()


class TestServerHTTPFactory(Site):
    pass
