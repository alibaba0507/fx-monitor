from google.appengine.ext import ndb
from google.appengine.api import memcache
import logging
import json
#db table for pair
class Pair(ndb.Model):
  name = ndb.StringProperty()
  value = ndb.IntegerProperty()
  email = ndb.StringProperty()

#db table for pattern
class Pattern(ndb.Model):
  name = ndb.StringProperty()
  value = ndb.IntegerProperty()
  pair = ndb.StructuredProperty(Pair)
  # This will change any time when pattern of the day is found
  sendEmail = ndb.IntegerProperty(default = 0)

#Save user pattern settings
def savePaternSettings(u_email,pair,pattern,value):
   client = memcache.Client()
   pair = pair.lower()
   qry = Pair.query(Pair.name == pair,Pair.email == u_email)
   if qry.count() > 0:
     p = qry.get()
     q_pattern = Pattern.query(Pattern.name == pattern,Pattern.pair == p)
     if value > 0:
       if q_pattern.count() == 0:
        pt = Pattern(name = pattern,value = 1,pair = p)
        pt.put() # save to db
       saved = json.dumps([p.to_dict() for p in Pattern.query(Pattern.pair.email == u_email).fetch()])
       client.set(key='pairs_pattern[' + u_email + ']',value=saved,time=3600)
     else:
       if q_pattern.count() > 0:
         pt = q_pattern.get()
         pt.key.delete() # remove from db
       saved = json.dumps([p.to_dict() for p in Pattern.query(Pattern.pair.email == u_email).fetch()])
       client.set(key='pairs_pattern[' + u_email + ']',value=saved,time=3600)
   else: # save pair
    p = Pair(name = pair,email = u_email,value = 1)
    p.put()
    savePaternSettings(u_email,pair,pattern,value)


# create list of all users settings linked to selected pair
#@param u_email - user mail
#@param pair - selected pair
#@return list key = pattern name , values
def getUserPatternSettings(u_email,pair):
 
  l = {'Strong_Pearcing': getPaternSettings(u_email,pair,'Strong_Pearcing'),
       'Strong_Dark_cloud': getPaternSettings(u_email,pair,'Strong_Dark_cloud'),
       'Pearcing': getPaternSettings(u_email,pair,'Pearcing'),
       'Dark_cloud': getPaternSettings(u_email,pair,'Dark_cloud'),
       'Bulish_Endulfing': getPaternSettings(u_email,pair,'Bulish_Endulfing'),
       'Berish_Endulfing': getPaternSettings(u_email,pair,'Berish_Endulfing'),
       'Bulish_Harami': getPaternSettings(u_email,pair,'Bulish_Harami'),
       'Berish_Harami': getPaternSettings(u_email,pair,'Berish_Harami')
       }

  #logging.info('User Pattern Settings [' + str(l) + ']')
  #logging.info('User Pattern Settings INFO ##### [' + str(l['Strong_Pearcing']) + ']')
  return l


  
def getPaternSettings(u_email,pair,pattern):
   client = memcache.Client()
   pair = pair.lower()
   ret_pattern = client.get(key='pairs_pattern[' + u_email + ']')
   if ret_pattern is None or len(ret_pattern) == 0:
    saved = json.dumps([p.to_dict() for p in Pattern.query(Pattern.pair.email == u_email).fetch()])
    #logging.info('Saved pair [' + saved  + ']')
    client.set(key='pairs_pattern[' + u_email + ']',value=saved,time=3600)
    return getPaternSettings(u_email,pair,pattern)
    #logging.info(' Patterns are [' + ret_pattern  + ']')
  
   def f(x):
     return x['name'] == pattern and x['pair']['name'] == pair and x['pair']['email'] == u_email
   ret_patterns = filter(f, json.loads(ret_pattern))
   
   #patterns = json.loads(ret_pattern).fromkeys(key_email,u_email).fromkeys(key,pair).fromkeys(key_pattern,pattern)
   if ret_patterns is not None and len(ret_patterns): return ret_patterns
   else:    
     return 0
     '''
     qry = Pair.query(Pair.name == pair,Pair.email == u_email)
     if qry.count() > 0:
      p = qry.get()
      q_pattern = Pattern.query(Pattern.name == pattern,Pattern.pair == p)
      if q_pattern.count() > 0:
       client.set(key='pairs[' + pair + '][' + u_email + '][' + pattern + ']',value=1,time=3600)
       return 1
      else: 
       client.set(key='pairs[' + pair + '][' + u_email + '][' + pattern + ']',value=0,time=3600)
       return 0
     else: 
      client.set(key='pairs[' + pair + '][' + u_email + '][' + pattern + ']',value=0,time=3600)
      return 0
      '''
       