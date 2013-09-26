from google.appengine.api import memcache
from google.appengine.api import urlfetch
import logging
import json
import os
from datetime import date
import urllib
from google.appengine.ext import ndb
#import Utils

class Pair(ndb.Model):
  name = ndb.StringProperty()
  value = ndb.IntegerProperty()
  email = ndb.StringProperty()


class Pattern(ndb.Model):
  name = ndb.StringProperty()
  value = ndb.IntegerProperty()
  pair = ndb.StructuredProperty(Pair)


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
       client.set(key='pairs[' + pair + '][' + u_email + '][' + pattern + ']',value=1,time=3600)
     else:
       if q_pattern.count() > 0:
         pt = q_pattern.get()
         pt.key.delete() # remove from db
       client.delete(key='pairs[' + pair + '][' + u_email + '][' + pattern + ']')
   else: # save pair
    p = Pair(name = pair,email = u_email,value = 1)
    p.put()
    q_pattern = Pattern.query(Pattern.name == pattern,Pattern.pair == p)
    if value > 0:
      if q_pattern.count() == 0:
       pt = Pattern(name = pattern,value = 1,pair = p)
       pt.put() # save to db
       client.set(key='pairs[' + pair + '][' + u_email + '][' + pattern + ']',value=1,time=3600)
      else:
       if q_pattern.count() > 0:
         pt = q_pattern.get()
         pt.key.delete() # remove from db
       client.delete(key='pairs[' + pair + '][' + u_email + '][' + pattern + ']')

def getUserPatternSettings(u_email,pair):
  #l = []
  '''
  l.insert(0, getPaternSettings(u_email,pair,'Strong_Pearcing'))
  l.insert(1, getPaternSettings(u_email,pair,'Strong_Dark_cloud'))
  l.insert(2, getPaternSettings(u_email,pair,'Pearcing'))
  l.insert(3, getPaternSettings(u_email,pair,'Dark_cloud'))
  l.insert(4, getPaternSettings(u_email,pair,'Bulish_Endulfing'))
  l.insert(5, getPaternSettings(u_email,pair,'Berish_Endulfing'))
  l.insert(6, getPaternSettings(u_email,pair,'Bulish_Harami'))
  l.insert(7, getPaternSettings(u_email,pair,'Berish_Harami'))
  '''
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
   ret_pattern = client.get(key='pairs[' + pair + '][' + u_email + '][' + pattern + ']')
   #logging.info(' Get Patterns Settings [' + pair  +'][' + pattern + '][' + str(ret_pattern) + ']')
   if ret_pattern: return ret_pattern
   else:
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
       

# Will save all settings from form to DB
def saveUserSettings(u_email,pair,val):
  qry = Pair.query(Pair.name == pair,Pair.email == u_email)
  b_found = 0
  if qry.count() > 0:
   p = qry.get()
   p.value = int(val)
   p.put()
   b_found = 1
   #logging.info(' Save Found in DB [' + pair + '] after save [' + str(p.value) + '] value [' + str(val) + ']')
  if b_found == 0:
   #logging.info(' Save NOT found in DB [' + pair + '] [' + str(val) + ']')
   p = Pair(name = pair,email = u_email,value = int(val))
   p.put()
   #logging.info(' Save NOT found in DB [' + pair + '] after save [' + str(p.value) + '] value [' + str(val) + ']')
  
  client = memcache.Client()
  client.set(key='pairs[' + pair + '][' + u_email + ']',value=int(val),time=3600)
  
# This will populate cache and will keep it for 1 hour  = 3600
def getUserSettings(u_email,pair):
   l = []
   client = memcache.Client()
   p = client.get('pairs[' + pair + '][' + u_email + ']')
   if p is None :
    # check Database 
    #logging.info('Empty memcache for [' + pair  + ']')
    qry = Pair.query(Pair.name == pair,Pair.email == u_email)
    if qry.count() > 0:
      p = qry.get()
     # logging.info('Found In DB [' + pair  + '][' + p  +']')
      val = p.value
      client.set(key='pairs[' + pair + '][' + u_email + ']',value=val,time=3600)
    #  logging.info('Found In DB Save and retunr  [' + pair  + '][' + str(val)  +']')
      return val
    else: return 0
   else:
    #logging.info('Found In Memcache Save and retunr  [' + pair  + '][' + str(p)  +']')
    return p
    
def clearData():
  client = memcache.Client()
  hist_json = client.delete('hist')
  client.delete('h_gbp')
  client.delete('h_eur')
  client.delete('h_chf')
  client.delete('h_cad')
  client.delete('h_aud')
  client.delete('pv')

#- description: Check for SR Level broke and send email notification
#  url: /?c=1
#  schedule: every 5 minutes

def checkSRLevels():
  msg = ''
  client = memcache.Client()
  sr_lines = client.get('sr_lines');
  #logging.debug('****** [' + sr_lines  + ']')
  if sr_lines is None or len(sr_lines) == 0:
    loadData()
    checkSRLevels()
  
  srLines = json.loads(sr_lines)
  url_link = "https://script.google.com/macros/s/AKfycbzFDj3RD57LI-W8ppcyHVhNq_3-_MQ-WUP9sttWZoO8ocvhF-Dh/exec?lastprice=1"
  urlfetch.set_default_fetch_deadline(45)
  result = urlfetch.fetch(url_link)
  if result.status_code == 200:
    url = 'http://' + os.environ['HTTP_HOST'] + '/?r=1&p='
    resJSON = json.loads(result.content)
    #logging.debug('Calling  checkSRLevels ...' + str(resJSON[0]))
    pairs = {0:'AUDUSD',1:'EURGBP',2:'EURJPY',3:'EURUSD',4:'GBPJPY',5:'GBPUSD',6:'USDCAD',7:'USDCHF',8:'USDJPY'}
    i = 0
    for e in resJSON[0]:
      #client.delete(pairs[i] + 'old')
      oldPrice = client.get(pairs[i] + 'old')
      lastSRLevel = client.get(pairs[i] + 'price')
      #logging.debug('['  + pairs[i] + ']  *********** ' + str(e))
      if oldPrice:
        k = 0
        for l in srLines:       
          #if pairs[i].upper() == srLines[str(k)]['name']:
          #logging.debug('Current Level Price is [' + str(srLines[str(k)]['price']) + ']')
          #if pairs[i].upper() == srLines[str(k)]['name'] and srLines[str(k)]['price'] > min(float(oldPrice),float(j)) and srLines[str(k)]['price'] < max(float(oldPrice),float(j)) and lastSRLevel is None or (lastSRLevel is not None and len(lastSRLevel) != 0 and float(lastSRLevel) != srLines[str(k)]['price']):
          #  msg += 'Pair [<a href="' +  url + pairs[i] + '">' + pairs[i] + '</a>] S/R level broke at [' + str(srLines[str(k)]['price']) + ']<br />'
          if pairs[i].upper() == srLines[str(k)]['name'] and (max(float(oldPrice),float(e)) > float(srLines[str(k)]['price']) > min(float(oldPrice),float(e))) and float(lastSRLevel) != srLines[str(k)]['price']:
            #logging.debug('Pair [' +  pairs[i] + '] S/R level broke at [' + str(srLines[str(k)]['price']) + ']Saved level[' + str(lastSRLevel) + '][' + str(e) + ']['+ srLines[str(k)]['name']+ ']')
            msg += 'Pair [<a href="' +  url + pairs[i] + '">' + pairs[i] + '</a>] S/R level broke at [' + str(srLines[str(k)]['price']) + ']<br />'
            memcache.add(key=pairs[i] + 'price',value=str(srLines[str(k)]['price'])) # save price value
          elif lastSRLevel is not None and len(lastSRLevel) != 0:
            memcache.add(key=pairs[i] + 'price',value=lastSRLevel) # save price value
          k += 1
          #logging.debug('Add to memcache')
      memcache.add(key=pairs[i] + 'old',value=str(e)) # save price value
      i += 1
  return msg      

# check the date of the candlestick pattern
# if find any will add to memcache 
def chekEmailPatterns(result):
   client = memcache.Client()
   today = date.today()
   resultJSON = json.loads(result)
   cnt = 0
   for elem in resultJSON['hist']:
    cnt += 1
    #self.response.write("<tr>")
    i = 0
    #logging.info(' Start check Email patterns .... ')
    for e in elem:
      s = urllib.unquote(e).decode("utf-8")
      if i == 0:
        pair = s
      if i == 2: # fromat time
       l = s.split('T')
       if len(l) > 0 and (today.isoformat() == l[0]):
        if (today.isoformat() == l[0]): # only today patterns
         pattern = client.get('email[' + pair  +'][' + today.isoformat() + ']');
         if pattern is None or len(pattern) == 0: # add to memcache
          logging.info(' Add pattern for [' + pair  + ']')
          memcache.add(key='email[' + pair  +'][' + today.isoformat() + ']',value=pair,time=3600);
      i += 1
      
      
def loadData():
  client = memcache.Client()
  hist_json = client.get('hist')
  pv_json = client.get('pv')
  h_gbp = client.get('h_gbp')
  h_eur = client.get('h_eur')
  h_chf = client.get('h_chf')
  h_cad = client.get('h_cad')
  h_aud = client.get('h_aud')
  h_eurgbp = client.get('h_eurgbp')
  h_gbpjpy = client.get('h_gbpjpy')
  h_eurjpy = client.get('h_eurjpy')
  
  sr_lines = client.get('sr_lines')
  
  if sr_lines is None or len(sr_lines) == 0:
    url_link = "https://script.google.com/macros/s/AKfycbzFDj3RD57LI-W8ppcyHVhNq_3-_MQ-WUP9sttWZoO8ocvhF-Dh/exec?r=1"
    urlfetch.set_default_fetch_deadline(45)
    result = urlfetch.fetch(url_link)
    if result.status_code == 200:
      memcache.add(key='sr_lines',value=result.content,time=3600)
  if pv_json is None or len(pv_json) == 0:
    url_link = "https://script.google.com/macros/s/AKfycbzFDj3RD57LI-W8ppcyHVhNq_3-_MQ-WUP9sttWZoO8ocvhF-Dh/exec?pv=1"
    urlfetch.set_default_fetch_deadline(45)
    result = urlfetch.fetch(url_link)
    logging.debug('before save to memcache')
      #self.redirect(url_link)
    if result.status_code == 200:
      logging.debug('save to memcache')
      memcache.add(key='pv',value=result.content,time=3600)

  if hist_json is None or len(hist_json) == 0:
    #load from url
    url_link = "https://script.google.com/macros/s/AKfycbzFDj3RD57LI-W8ppcyHVhNq_3-_MQ-WUP9sttWZoO8ocvhF-Dh/exec?h=1"
    urlfetch.set_default_fetch_deadline(45)
    result = urlfetch.fetch(url_link)
      #self.redirect(url_link)
    if result.status_code == 200:
      memcache.add(key='hist',value=result.content,time=3600)
      chekEmailPatterns(result.content)
  
  if h_gbp is None or len(h_gbp) == 0:
    url_link = "https://script.google.com/macros/s/AKfycbzFDj3RD57LI-W8ppcyHVhNq_3-_MQ-WUP9sttWZoO8ocvhF-Dh/exec?h=1&p=gbpusd"
    urlfetch.set_default_fetch_deadline(45)
    result = urlfetch.fetch(url_link)
      #self.redirect(url_link)
    if result.status_code == 200:
      memcache.add(key='h_gbp',value=result.content,time=3600)
      
  if h_eur is None or len(h_eur) == 0:
    url_link = "https://script.google.com/macros/s/AKfycbzFDj3RD57LI-W8ppcyHVhNq_3-_MQ-WUP9sttWZoO8ocvhF-Dh/exec?h=1&p=eurusd"
    urlfetch.set_default_fetch_deadline(45)
    result = urlfetch.fetch(url_link)
      #self.redirect(url_link)
    if result.status_code == 200:
      memcache.add(key='h_eur',value=result.content,time=3600)
  
  if h_chf is None or len(h_chf) == 0:
    url_link = "https://script.google.com/macros/s/AKfycbzFDj3RD57LI-W8ppcyHVhNq_3-_MQ-WUP9sttWZoO8ocvhF-Dh/exec?h=1&p=usdchf"
    urlfetch.set_default_fetch_deadline(45)
    result = urlfetch.fetch(url_link)
      #self.redirect(url_link)
    if result.status_code == 200:
      memcache.add(key='h_chf',value=result.content,time=3600)
  
  if h_cad is None or len(h_cad) == 0:
    url_link = "https://script.google.com/macros/s/AKfycbzFDj3RD57LI-W8ppcyHVhNq_3-_MQ-WUP9sttWZoO8ocvhF-Dh/exec?h=1&p=usdcad"
    urlfetch.set_default_fetch_deadline(45)
    result = urlfetch.fetch(url_link)
      #self.redirect(url_link)
    if result.status_code == 200:
      memcache.add(key='h_cad',value=result.content,time=3600)
      
  if h_aud is None or len(h_aud) == 0:
    url_link = "https://script.google.com/macros/s/AKfycbzFDj3RD57LI-W8ppcyHVhNq_3-_MQ-WUP9sttWZoO8ocvhF-Dh/exec?h=1&p=audusd"
    urlfetch.set_default_fetch_deadline(45)
    result = urlfetch.fetch(url_link)
      #self.redirect(url_link)
    if result.status_code == 200:
      memcache.add(key='h_aud',value=result.content,time=3600)
      
  if h_eurgbp is None or len(h_eurgbp) == 0:
    url_link = "https://script.google.com/macros/s/AKfycbzFDj3RD57LI-W8ppcyHVhNq_3-_MQ-WUP9sttWZoO8ocvhF-Dh/exec?h=1&p=eurgbp"
    urlfetch.set_default_fetch_deadline(45)
    result = urlfetch.fetch(url_link)
      #self.redirect(url_link)
    if result.status_code == 200:
      memcache.add(key='h_eurgbp',value=result.content,time=3600)
      
  
  if h_eurjpy is None or len(h_eurjpy) == 0:
    url_link = "https://script.google.com/macros/s/AKfycbzFDj3RD57LI-W8ppcyHVhNq_3-_MQ-WUP9sttWZoO8ocvhF-Dh/exec?h=1&p=eurjpy"
    urlfetch.set_default_fetch_deadline(45)
    result = urlfetch.fetch(url_link)
      #self.redirect(url_link)
    if result.status_code == 200:
      memcache.add(key='h_eurjpy',value=result.content,time=3600)
      
  
  if h_gbpjpy is None or len(h_gbpjpy) == 0:
    url_link = "https://script.google.com/macros/s/AKfycbzFDj3RD57LI-W8ppcyHVhNq_3-_MQ-WUP9sttWZoO8ocvhF-Dh/exec?h=1&p=gbpjpy"
    urlfetch.set_default_fetch_deadline(45)
    result = urlfetch.fetch(url_link)
      #self.redirect(url_link)
    if result.status_code == 200:
      memcache.add(key='h_gbpjpy',value=result.content,time=3600)
      