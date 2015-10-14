from pkg_resources import resource_string
from twisted.web.server import Site
from twisted.web.resource import Resource

from localmail.inbox import INBOX


class TestServerHTTPFactory(Site):
    noisy = False


class Index(Resource):
    isLeaf = True
    index_template = None

    def __init__(self, *args, **kwargs):
        Resource.__init__(self, *args, **kwargs)

        # defer import so is optional
        try:
            from jinja2 import Template
            self.index_template = Template(resource_string(
                __name__, 'templates/index.html').decode('utf8'))
        except ImportError:
            pass

    def render_GET(self, request):
        if self.index_template is None:
            return "Web interface not available: Jinja2 not installed"

        request.setHeader('Content-type', 'text/html; charset=utf-8')
        return self.index_template.render(msgs=INBOX.msgs).encode('utf8')


index = Index()
