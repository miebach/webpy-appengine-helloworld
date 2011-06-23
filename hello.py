from google.appengine.ext import db
from vendor import web
from models import *

import os
import sys
sys.path.append("vendor")

from vendor.mako.template import Template 
from vendor.mako.lookup import  TemplateLookup 
from vendor.web.contrib.template import render_mako

urls = (
  '/', 'index',
  '/list', 'list'
)


tdir = os.path.join(os.path.dirname(__file__),"templates")
# input_encoding and output_encoding is important for unicode
# template file. Reference:
# http://www.makotemplates.org/docs/documentation.html#unicode
# Also see http://webpy.org/cookbook/template_mako
render = render_mako(
    directories=[tdir],
    input_encoding='utf-8',
    output_encoding='utf-8',
)


class index:
    def GET(self):
        return render.index()

    def POST(self):
        i = web.input()
        person = Person()
        person.name = i.name
        person.put()
        return web.seeother('/list')

class list:
    def GET(self):
        people = db.GqlQuery("SELECT * FROM Person ORDER BY created DESC LIMIT 10")
        return render.list(people=people)

app = web.application(urls, globals())
main = app.cgirun()
