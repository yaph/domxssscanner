# -*- coding: utf-8 -*-
import os
import urlparse
import logging
import webapp2
import jinja2
import json
from google.appengine.api import urlfetch
from domxss import DOMXSS

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))

class BaseHandler(webapp2.RequestHandler):
    template_values = {};

    def generate(self, content_type='text/html', template_name='index.html'):
        # set the content type
        content_type += '; charset=utf-8'
        self.response.headers["Content-Type"] = content_type

        values = {
                  'request': self.request,
                  'host': self.request.host,
                  'page_url': self.request.url,
                  'base_url': self.request.application_url
                  }
        values.update(self.template_values)

        template = jinja_environment.get_template(template_name)
        self.response.out.write(template.render(self.template_values).encode('utf8'))

    def set_template_value(self, name, value):
        self.template_values[name] = value;

    def get_param(self, name, default_value, type):
        param = self.request.get(name)
        if '' == param:
            return default_value
        if 'int' == type:
            param = int(param)
        elif 'url' == type:
            if Validate().uri(param) is False:
                return None
        return param

    def is_ajax(self):
        return "XMLHttpRequest" == self.request.headers.get("X-Requested-With")

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
            logging.info( response )
            if response:
                html = response.content
                self.set_template_value('response_text', html.decode('utf8'))

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


class Validate():
    def uri(self, uri):
        try:
            if urlparse.urlparse(uri).netloc:
                return True
            else:
                return False
        except AttributeError:
            return False


class HTTP():
    request_url = ''

    headers = {}

    def set_header(self, name, value):
        self.headers[name] = value

    def get_headers(self):
        return self.headers

    def request(self, url, **params):
        if 0 < len(params):
            self.request_url = "%s?%s" % (url, urllib.urlencode(params))
        else:
            self.request_url = url
        try:
            result = urlfetch.fetch(self.request_url)
            if result.status_code == 200:
                return result
            elif result.status_code == 400:
                logging.error('HTTP Status 400: Limit exceeded')
        except:
            logging.error('HTTP Request: Result could not be fetched')
        return None

    def get_request_url(self):
        return self.request_url


app = webapp2.WSGIApplication([('/', MainHandler),
                               ('/scan.*', ScanHandler),
                               ('/info/([\w-]*)', PageHandler),
                               ], debug=True)