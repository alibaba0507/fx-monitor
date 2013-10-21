from google.appengine.ext import ndb
from google.appengine.api import memcache
from google.appengine.api import urlfetch
import urllib
import logging
import json


#db table for pattern
class DbNews(ndb.Model):
  pair = ndb.StringProperty()
  pr = ndb.StringProperty()
  alexa = ndb.StringProperty()
  positive = ndb.IntegerProperty()
  negative = ndb.IntegerProperty()
  raatio = ndb.IntegerProperty()
  

def search(q,pair):
  #if (!type || type == '')
  type = 'all+types';
  url = 'http://pipes.yahoo.com/pipes/pipe.run?_id=16f66113a9aa9c39dd93df8806949159&_render=json&filterinput=' + type + '&maininput=' + q 
  urlfetch.set_default_fetch_deadline(45)
  result = urlfetch.fetch(url)
  if result.status_code == 200:
    resJSON = json.loads(result.content)
    items = resJSON.value.items
    
    cnt = 0
    for i in items:
      link = i.link
      title = i.title
      url_link = 'http://dotfornote.appspot.com/?url=' + link + '&wrds=1'
      urlfetch.set_default_fetch_deadline(45)
      result = urlfetch.fetch(url)
      if result.status_code == 200:
       resItems = json.loads(result.content)
       pos += int(resItems['positive'])
       neg += int(resItems['negative'])
       cnt += 1
    return '<p> pos = [' + str((pos/cnt)) + '] Neg [' + str((neg/cnt)) + ']<br />'
  else:
    return '<p> No Resilt for this request <br/>'
    
    