from google.appengine.ext import ndb
from google.appengine.api import memcache
import logging


#db table for pair
class Hist(ndb.Model):
  type = ndb.StringProperty()
  #data = ndb.IntegerProperty()
  # JSON string data
  data = ndb.StringProperty()


def save(data,type):
  qry = Hist.query(Hist.type == type)
  if qry.count() > 0:
    p = qry.get()
    p.data = data
    p.put()
  
  client = memcache.Client()
  if type == 'pt': #patterns
    client.set(key='hist',value=data,time=3600)
  else:
    client.set(key='pv_hist',value=data,time=3600)

def get(type):
  client = memcache.Client()
  pt = None
  if type == 'pt': # patterns
   pt = client.get(key='hist')
  else
   pt = client.get(key='pv_hist')
  
  if pt is None or len(pt) == 0:
   qry = Hist.query(Hist.type == type)
  if qry.count() > 0:
    p = qry.get()
    pt = p.data
    if type == 'pt': #patterns
     client.set(key='hist',value=pt,time=3600)
    else:
     client.set(key='pv_hist',value=pt,time=3600)
  return pt
