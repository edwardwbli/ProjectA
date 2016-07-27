#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import os
from StringIO import StringIO
from google.appengine.ext.webapp import template
import urllib

#insert libs into 0 position, for app engine to invoke third party libs
#import sys
#sys.path.insert(0, 'libs')
import pyqrcode
import re

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        
        template_values = {
        'url': '/images/test.png',
        'url_linktext': 'test',}
        path = os.path.join(os.path.dirname(__file__), 'webpage.html')
        self.response.out.write(template.render(path, template_values))

class M2(webapp2.RequestHandler):
    def get(self):
        s = self.request.get('s')
        
        query_params = {'s':s}
        #self.redirect('/?' + urllib.urlencode(query_params))
        img = pyqrcode.create(s,encoding='utf8')
        buffer = StringIO()
        img.svg(buffer,scale=4)
        p = re.compile(r'<svg.*</svg>')
        svgsegment = re.search(p, buffer.getvalue())
        testsvg = svgsegment.group(0)
      
        template_values = {}
        self.response.out.write(testsvg)
        #self.redirect('/')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/convert',M2)
], debug=True)
