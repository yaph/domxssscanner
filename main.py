# -*- coding: utf-8 -*-
import webapp2
import json
from gae_utils import BaseHandler, HTTP
from domxss import DOMXSS


class MainHandler(BaseHandler):
    def get(self):
        self.generate('text/html', 'index.html')


class ScanHandler(BaseHandler):

    def error(self, message):
        self.set_template_value('error', message)
        self.set_template_value('title', message)
        if self.is_ajax():
            self.generate('text/html', 'error.html')
        else:
            self.generate('text/html', '404.html')


    def get(self):
        self.jinja_env.cache = None
        url = self.get_param('url', '', 'url')
        if url:
            self.set_template_value('url', url)
            self.set_template_value('title', 'DOM XSS Scanner - Scan %s' % url)
            response = HTTP().request(url)
            if response:
                content = response.content
                encoding = False
                dxs = DOMXSS()

                # try to determine charset from request headers
                ctype = response.headers['content-type'].strip()
                pos = ctype.find('charset=')
                if pos > 0:
                    encoding = ctype[pos+8:len(ctype)].lower()

                if ctype.startswith('text/html') or ctype.startswith('text/xml'):
                    # try to determine charset from html if not set before
                    if not encoding:
                        encoding = dxs.get_charset_from_html(content)
                    script_urls = dxs.get_script_urls(url, content)
                    self.set_template_value('script_urls', json.dumps(script_urls))

                if not encoding:
                    encoding = 'utf-8'

                response_text = content.decode(encoding, 'ignore')
                self.set_template_value('response_text', response_text)

                if self.is_ajax():
                    self.generate('text/javascript', 'response.html')
                else:
                    self.generate('text/html', 'scan.html')

            else:
                self.error('Error: Supplied URL could not be fetched.')

        else:
            self.error('Error: Supplied URL is not valid.')


class PageHandler(BaseHandler):
    def get(self, name):

        self.set_template_value('title', '%s DOM XSS Scanner' % name)
        self.generate('text/html', '%s.html' % name)


app = webapp2.WSGIApplication([('/', MainHandler),
                               ('/scan.*', ScanHandler),
                               ('/info/([\w-]*)', PageHandler),
                               ], debug=True)
