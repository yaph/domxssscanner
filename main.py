#!/usr/bin/env python
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from django.utils import simplejson
import gae_utils as gae
from domxss import DOMXSS

class BaseHandler(gae.BaseHandler):
    pass

class MainHandler(BaseHandler):
    def get(self):
        self.generate('text/html', 'index.html')

class ScanHandler(BaseHandler):
    def get(self):
        title = 'DOMXSS Scanner - Scan %s'

        url = self.get_param('url', '', 'url')
        if url:
            self.set_template_value('url', url)
            response = gae.HTTP().request(url)
            if response:
                html = response.content
                self.set_template_value('response_text', html)

                # For now only call get_script_urls with HTML or XML files
                ctype = response.headers['content-type']
                if ctype.find('html') > 0 or ctype.find('xml') > 0:
                    script_urls = DOMXSS().get_script_urls(url, html)
                    self.set_template_value('script_urls', simplejson.dumps(script_urls))
        else:
            url = ''

        self.set_template_value('title', title % url)

        if self.is_ajax():
            self.generate('text/javascript', 'response.html')
        else:
            self.generate('text/html', 'scan.html')

class PageHandler(BaseHandler):
    def get(self, name):
        self.set_template_value('title', '%s DOMXSS Scanner' % name)
        self.generate('text/html', 'pages/%s.html' % name)

def main():
    application = webapp.WSGIApplication([
                                          ('/', MainHandler),
                                          ('/scan.*', ScanHandler),
                                          ('/info/([\w-]*)', PageHandler),
                                          ], debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()