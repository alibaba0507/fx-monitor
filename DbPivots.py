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
  

# will get the settings from memcache
# if not exist will created from the ndb
# @retrun json object of the Pivots objects
def getPvSettings(u_email,pair):
  client = memcache.Client()
  pair = pair.lower()
  ret_pattern = client.get(key='pvsettings[' + pair + '][' + u_email + ']')
   #logging.info(' Get Patterns Settings [' + pair  +'][' + pattern + '][' + str(ret_pattern) + ']')
  if ret_pattern: return json.load(ret_pattern)
  else:
   #store as json string
   client.set(key='pvsettings[' + pair + '][' + u_email + ']',value=json.dumps([p.to_dict() for p in Pivots.query(Pivots.pair == pair,Pivots.email == u_email).fetch()]),time=3600)
   getPvSettings(u_email,pair) #call again  
     
def savePvPattern(u_email,pair,pattern,child_1,child_2,delete):
 q = Pivots.query(Pivots.pair == pair,Pivots.email == u_email,Pivots.child == pattern)
 p = Pivots(pair = pair,email = u_email,child = pattern)
 if q.count() > 0:
   p = q.get()
   if delete:
    p.key.delete() # remove from db
    #clear cache
    client.delete(key='pvsettings[' + pair + '][' + u_email + ']')
    return 0
 #if child_1 is None:
 p.child_1 = child_1
 p.child_2 = child_2
 p.put()
 #clear cache
 client.delete(key='pvsettings[' + pair + '][' + u_email + ']') 