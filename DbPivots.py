from google.appengine.ext import ndb
from google.appengine.api import memcache
import logging
import json

#db table for pattern
class Pivots(ndb.Model):
  pair = ndb.StringProperty()
  email = ndb.StringProperty()
  child = ndb.StringProperty()
  child_1 = ndb.StringProperty()
  child_2 = ndb.StringProperty()
  # This will change any time when pattern of the day is found
  sendEmail = ndb.IntegerProperty(default = 0)
  

def translatePattern(shortName):
  if shortName == 'SR': return 'Pivot Sell Range'
  elif shortName == 'BR': return 'Pivot Buy Range'
  elif shortName == 'ST': return 'Pivot Sell Trend'
  elif shortName == 'BT': return 'Pivot Buy Trend'
  else: return None
# will get the settings from memcache
# if not exist will created from the ndb
# @retrun json object of the Pivots objects
def getPvSettings(u_email,pair):
  client = memcache.Client()
  pair = pair.lower()
  #ret_pattern = client.get(key='pvsettings[' + pair + '][' + u_email + ']')
  ret_pattern = client.get(key='pvsettings[' + u_email + ']')
  #logging.info(' Get Pivot Patterns Settings [' + pair  +'][' + str(ret_pattern) + ']')
  if ret_pattern is not None and len(ret_pattern) > 0: 
    logging.info('Read MEMCASHE ......')
    def f(x):
     return x['pair'] == pair and x['email'] == u_email
    result = filter(f, json.loads(ret_pattern))
    logging.info('Pivots filter [' + json.dumpp(result) + ']')
    return result
    
  else:
   #store as json string
   saved = json.dumps([p.to_dict() for p in Pivots.query(Pivots.email == u_email).fetch()])
   logging.info('Read Pivots DBase ......[' + saved + ']')
   if saved and len(saved) > 2:
    client.set(key='pvsettings[' + u_email + ']',value=saved,time=3600)
    getPvSettings(u_email,pair) #call again  
     
def savePvPattern(u_email,pair,pattern,child_1,child_2,delete):
 client = memcache.Client()
 #logging.debug('Email[' + u_email + '] pair ['+ pair + '] pattern [' + pattern + '] child ['+ child_1 + '] child 2['+ child_2 + ']')
 q = Pivots.query(Pivots.pair == pair,Pivots.email == u_email,Pivots.child == pattern)
 p = Pivots(pair = pair,email = u_email,child = pattern)
 if q.count() > 0:
   p = q.get()
   if delete:
    p.key.delete() # remove from db
    #clear cache
    client.delete(key='pvsettings[' + u_email + ']')
    return 0
 #if child_1 is None:
 p.child_1 = child_1
 p.child_2 = child_2
 p.put()
 #clear cache
 client.delete(key='pvsettings[' + u_email + ']') 