from google.appengine.ext import ndb
from google.appengine.api import memcache
import logging
import urllib

#db table for pair
class Hist(ndb.Model):
  type = ndb.StringProperty()
  #data = ndb.IntegerProperty()
  # JSON string data
  data = ndb.BlobProperty()


def save(type):
  
  #logging.debug('Data ..... [' + data  + ']')
  qry = Hist.query(Hist.type == type)
  if qry.count() > 0:
    p = qry.get()
    #p.data = data
  else:
    #logging.debug('Before add to DB')
    p = Hist(type = type)#,data = data)
    #p.put()
    logging.debug('After add to DB')
  
  client = memcache.Client()
  if type == 'pt': #patterns
    url_link = "https://script.google.com/macros/s/AKfycbzFDj3RD57LI-W8ppcyHVhNq_3-_MQ-WUP9sttWZoO8ocvhF-Dh/exec?h=1"
    urlfetch.set_default_fetch_deadline(45)
    result = urlfetch.fetch(url_link)
    if result.status_code == 200:
      client.set(key='hist_pt',value=result.content)
      p.data = result.content
      p.put()
  else:
    url_link = "https://script.google.com/macros/s/AKfycbzFDj3RD57LI-W8ppcyHVhNq_3-_MQ-WUP9sttWZoO8ocvhF-Dh/exec?pv=1"
    urlfetch.set_default_fetch_deadline(45)
    result = urlfetch.fetch(url_link)
    if result.status_code == 200:
     client.set(key='pv_hist',value=result.content)
     p.data = result.content
     p.put()

def get(type):
  client = memcache.Client()
  pt = None
  if type == 'pt': # patterns
   pt = client.get(key='hist_pt')
  else:
   pt = client.get(key='pv_hist')
  
  if pt is None or len(pt) == 0:
   qry = Hist.query(Hist.type == type)
   if qry.count() > 0:
    p = qry.get()
    pt = p.data
    if type == 'pt': #patterns
     client.set(key='hist_pt',value=pt,time=3600)
    else:
     client.set(key='pv_hist',value=pt,time=3600)
  return pt
