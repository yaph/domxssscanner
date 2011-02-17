#!/usr/bin/env python
import unittest
import os
import sys
sys.path.append(os.path.join(os.getcwd(), '..'))
from domxss import DOMXSS

class TestDOMXSS(unittest.TestCase):

    def setUp(self):
        self.dxs = DOMXSS()
        self.url = 'http://localhost:8080/'

    def get_scripts(self, file_name):
        return self.dxs.get_script_urls(self.url, open(file_name, 'r').read())

    def test_base_tag(self):
        scripts = self.get_scripts('./base_tag.html')
        self.assertEqual("http://localhost:8080/static/js/lib/modernizr-1.6.min.js", scripts[0])

    def test_script_count(self):
        scripts = self.get_scripts('./script_count.html')
        self.assertEqual(3, len(scripts))

if __name__ == '__main__':
    unittest.main()