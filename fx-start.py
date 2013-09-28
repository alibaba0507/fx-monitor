import webapp2
import json
import os
from google.appengine.ext.webapp import template
import cachedJson
from google.appengine.api import memcache
import logging
from google.appengine.api import users
import Fx_Utils

#function that will get current loggin user
# @param url ussually from self.request.uri
# @return list(url,url_text = 'Login' or 'Logout', user)
# from user can extract email and other info
def getLoginInfo(uri):
    user = users.get_current_user()
    url = users.create_login_url(uri)
    url_linktext = 'Login'
    url_user = ''
    if user: # check for user is login
     url = users.create_logout_url(uri)
     url_linktext = 'Logout'
     
    ret = []
    ret.insert(0,url)
    ret.insert(1, url_linktext)
    ret.insert(2,user) 
    return ret
    
# Class that handle url reqest (GET or POST)
class MainHandler(webapp2.RequestHandler):
  
  def get(self):
   userInfo = getLoginInfo(self.request.uri)
   # make sure data is cached
   cachedJson.loadData()
   # get history table for all pairs patterns
   hist_json = memcache.get('hist')
   while hist_json is None: # looping till get some data
    cachedJson.loadData()
   # get data as json
   resultJSON = json.loads(hist_json)
   cn = 0 
   big_f = []
   for elem in resultJSON['hist']:
    f = []
    cnt += 1
    if cnt > 20: break # only 20 row on display
    #self.response.write("<tr>")
    i = 0
    for e in elem:
     s = urllib.unquote(e).decode("utf-8")
     if i == 2: # fromat time
      l = s.split('T')
      if len(l) > 0:
       s = '&nbsp; ' + l[0] + '&nbsp; '
       f.append(s )
       i += 1
    big_f.append(f)
    user = users.get_current_user()
    if user is None:
      template_values = {
        'pair_html' : Fx_Utils.getPairsAsLinks(),
        'html_table' : big_f,
        'url' : userInfo[0],
        'url_text' : userInfo[1],
        'user' : userInfo[2]
            
      }
    else:
      template_values = {
        'pair_html' : Fx_Utils.getPairsAsLinks(),
         'html_table' : big_f,
         'url' : userInfo[0],
         'url_text' : userInfo[1],
         'user' : userInfo[2],
         'GBPUSD' : cachedJson.getUserPatternSettings(user.email(),'GBPUSD'),
         'EURUSD' : cachedJson.getUserPatternSettings(user.email(),'EURUSD'),
         'USDCHF' : cachedJson.getUserPatternSettings(user.email(),'USDCHF'),
         'USDCAD' : cachedJson.getUserPatternSettings(user.email(),'USDCAD'),
         'AUDUSD' : cachedJson.getUserPatternSettings(user.email(),'AUDUSD'),
         'EURGBP' : cachedJson.getUserPatternSettings(user.email(),'EURGBP'),
         'GBPJPY' : cachedJson.getUserPatternSettings(user.email(),'GBPJPY'),
         'EURJPY' : cachedJson.getUserPatternSettings(user.email(),'EURJPY'),
         'USDJPY' : cachedJson.getUserPatternSettings(user.email(),'USDJPY')
     }
          
        
   path = os.path.join(os.path.dirname(__file__), 'index1.html')
   self.response.out.write(template.render(path,template_values))
    
    




app = webapp2.WSGIApplication([
  ('/.*', MainHandler),
], debug=True)