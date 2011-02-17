#!/usr/bin/env python
from inspect import stack
import os
import sys
sys.path.append(os.path.join(os.getcwd(), '..'))
from domxss import DOMXSS

def test_base_tag():
    f = open('./base_tag.html', 'r')
    html = f.read()
    scripts = DOMXSS().get_script_urls('http://localhost:8080/', html)
    if "http://localhost:8080/static/js/lib/modernizr-1.6.min.js" == scripts[0]:
        print success()
    else:
        print fail()

def success():
    print 'Test success: %s' % get_test_name()

def fail():
    print 'Test fail: %s' % get_test_name()

def get_test_name():
    return stack()[2][3]

def run_tests():
    test_base_tag()

if __name__ == '__main__':
    run_tests()