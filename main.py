# -*- coding: utf-8 -*-
import webapp2
import json
from gae_utils import BaseHandler, HTTP
from domxss import DOMXSS


class MainHandler(BaseHandler):
    def get(self):
        self.generate('text/html', 'index.html')


class ScanHandler(BaseHandler):
    def get(self):
        url = self.get_param('url', '', 'url')
        if url:
            self.set_template_value('url', url)
            self.set_template_value('title', 'DOM XSS Scanner - Scan %s' % url)
            response = HTTP().request(url)
            if response:
                html = response.content
                try:
                    self.set_template_value('response_text', html.decode('utf8'))
                except UnicodeDecodeError:
                    self.set_template_value('error', 'Error: Content could not be parsed.')
                    self.generate('text/html', '404.html')
                    return

                # For now only call get_script_urls with HTML or XML files
                ctype = response.headers['content-type']
                if ctype.find('html') > 0 or ctype.find('xml') > 0:
                    script_urls = DOMXSS().get_script_urls(url, html)
                    self.set_template_value('script_urls', json.dumps(script_urls))

                if self.is_ajax():
                    self.generate('text/javascript', 'response.html')
                else:
                    self.generate('text/html', 'scan.html')

            else:
                self.set_template_value('error', 'Error: Supplied URL could not be fetched.')
                self.generate('text/html', 'error.html')

        else:
            self.set_template_value('error', 'Error: Supplied URL is not valid.')
            self.generate('text/html', 'error.html')


class PageHandler(BaseHandler):
    def get(self, name):

        self.set_template_value('title', '%s DOM XSS Scanner' % name)
        self.generate('text/html', '%s.html' % name)


app = webapp2.WSGIApplication([('/', MainHandler),
                               ('/scan.*', ScanHandler),
                               ('/info/([\w-]*)', PageHandler),
                               ], debug=True)