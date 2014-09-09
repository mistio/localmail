from pkg_resources import resource_string
from twisted.web.server import Site
from twisted.web.resource import Resource

from localmail.inbox import INBOX
from jinja2 import Template

index_template = Template(resource_string(
    __name__, 'templates/index.html').decode('utf8'))


class TestServerHTTPFactory(Site):
    noisy = False


class Index(Resource):
    isLeaf = True

    def render_GET(self, request):
        request.setHeader('Content-type', 'text/html; charset=utf-8')
        return index_template.render(msgs=INBOX.msgs).encode('utf8')


index = Index()
