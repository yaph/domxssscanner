# -*- coding: utf-8 -*-
import os
import urllib
import jinja2

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

url = 'http://www.google.com/'
body = ''

fh = urllib.urlopen(url)
body = unicode(fh.read(), 'utf-8', 'ignore')
print body
#body = fh.read()

#template = jinja_environment.get_template('form.html')
#print template.render({'body':body})