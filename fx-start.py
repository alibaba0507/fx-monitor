import webapp2
import json
import os
from google.appengine.ext.webapp import template
import cachedJson
from google.appengine.api import memcache
import logging
from google.appengine.api import users
import Fx_Utils


    
# Class that handle url reqest (GET or POST)
class MainHandler(webapp2.RequestHandler):
  
  def get(self):
   userInfo = getLoginInfo(self.request.uri)
   # make sure data is cached
   cachedJson.loadData()
   if self.request.get('pair'):
     pair = self.request.get('pair')
     hist_json = Fx_Utils.getCachedPairData(pair)
     while hist_json is None: # looping till get some data
      cachedJson.loadData()
      hist_json = Fx_Utils.getCachedPairData(pair)
      # get data as json
     resultJSON = json.loads(hist_json) 
     patternList = Fx_Utils.constPatternList(resultJSON['hist'])
     template_values = Fx_Utils.constTemplateValues(userInfo,patternList)
   elif self.request.get('pv'):
     hist_json = memcache.get('pv')
     while hist_json is None: # looping till get some data
      cachedJson.loadData()
      hist_json = memcache.get('pv')
   else:
    # get history table for all pairs patterns
    hist_json = memcache.get('hist')
    while hist_json is None: # looping till get some data
     cachedJson.loadData()
     hist_json = memcache.get('hist')
    # get data as json
    resultJSON = json.loads(hist_json) 
    patternList = Fx_Utils.constPatternList(resultJSON['hist'])
    template_values = Fx_Utils.constTemplateValues(userInfo,patternList)
   
   path = os.path.join(os.path.dirname(__file__), 'index1.html')
   self.response.out.write(template.render(path,template_values))
    
    




app = webapp2.WSGIApplication([
  ('/.*', MainHandler),
], debug=True)