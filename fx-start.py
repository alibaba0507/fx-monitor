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
   #invoke by cron job
   if self.request.get('cron'):
      cachedJson.loadData()
   elif self.request.get('pair'):
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
     pair = None
     if self.request.get('p'):
      pair = self.request.get('p')
     resultJSON = json.loads(hist_json)
     patternList = Fx_Utils.constPatternList(resultJSON['hist'],pair)
     template_values = Fx_Utils.constTemplateValues(userInfo,patternList)
     
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
    
    
  def post(self):
    user = users.get_current_user()
    l = []
    #logging.debug('Strong_Pearcing [' + self.request.get('Strong_Pearcing') + '][' + self.request.get('hStrong_Pearcing') + '][' + self.request.get('p') + ']')
    if self.request.get('Strong_Pearcing') != self.request.get('hStrong_Pearcing'):
     #logging.info('Return from checkbox [' + self.request.get('p') + '] Strong_Pearcing ')
     if len(self.request.get('Strong_Pearcing')) > 0:
     # logging.info('Calling saveUserSettings ......')
      DbUtils.savePaternSettings(user.email(),self.request.get('p'),'Strong_Pearcing',1)
     else:
       DbUtils.savePaternSettings(user.email(),self.request.get('p'),'Strong_Pearcing',0)
    
    if self.request.get('Strong_Dark_cloud') != self.request.get('hStrong_Dark_cloud'):
     #logging.info('Return from checkbox [' + self.request.get('p') + '] Strong_Dark_cloud ')
     if len(self.request.get('Strong_Dark_cloud')) > 0:
     # logging.info('Calling saveUserSettings ......')
      DbUtils.savePaternSettings(user.email(),self.request.get('p'),'Strong_Dark_cloud',1)
     else:
       DbUtils.savePaternSettings(user.email(),self.request.get('p'),'Strong_Dark_cloud',0)
       
    
     if self.request.get('Pearcing') != self.request.get('hPearcing'):
      #logging.info('Return from checkbox [' + self.request.get('p') + '] Pearcing ')
      if len(self.request.get('Pearcing')) > 0:
     # logging.info('Calling saveUserSettings ......')
       DbUtils.savePaternSettings(user.email(),self.request.get('p'),'Pearcing',1)
      else:
       DbUtils.savePaternSettings(user.email(),self.request.get('p'),'Pearcing',0)
    
     logging.debug('Dark_cloud [' + self.request.get('Dark_cloud') + '][' + self.request.get('hDark_cloud') + '][' + self.request.get('p') + ']')
   
    if self.request.get('Dark_cloud') != self.request.get('hDark_cloud'):
      #logging.info('Return from checkbox [' + self.request.get('p') + '] Dark_cloud ')
     #logging.info('Return from checkbox [' + self.request.get('GBPUSD') + '] hCheckBox [' + self.request.get('hGBPUSD') + ']')
      if len(self.request.get('Dark_cloud')) > 0:
     # logging.info('Calling saveUserSettings ......')
       DbUtils.savePaternSettings(user.email(),self.request.get('p'),'Dark_cloud',1)
      else:
       DbUtils.savePaternSettings(user.email(),self.request.get('p'),'Dark_cloud',0)
    
    if self.request.get('Bulish_Endulfing') != self.request.get('hBulish_Endulfing'):
     # logging.info('Return from checkbox [' + self.request.get('p') + '] Bulish_Endulfing ')
     #logging.info('Return from checkbox [' + self.request.get('GBPUSD') + '] hCheckBox [' + self.request.get('hGBPUSD') + ']')
      if len(self.request.get('Bulish_Endulfing')) > 0:
     # logging.info('Calling saveUserSettings ......')
       DbUtils.savePaternSettings(user.email(),self.request.get('p'),'Bulish_Endulfing',1)
      else:
       DbUtils.savePaternSettings(user.email(),self.request.get('p'),'Bulish_Endulfing',0)
       
    if self.request.get('Berish_Endulfing') != self.request.get('hBerish_Endulfing'):
    #logging.info('Return from checkbox [' + self.request.get('p') + '] Berish_Endulfing ')
     #logging.info('Return from checkbox [' + self.request.get('GBPUSD') + '] hCheckBox [' + self.request.get('hGBPUSD') + ']')
      if len(self.request.get('Berish_Endulfing')) > 0:
     # logging.info('Calling saveUserSettings ......')
       DbUtils.savePaternSettings(user.email(),self.request.get('p'),'Berish_Endulfing',1)
      else:
       DbUtils.savePaternSettings(user.email(),self.request.get('p'),'Berish_Endulfing',0)
       
    
    if self.request.get('Bulish_Harami') != self.request.get('hBulish_Harami'):
      #logging.info('Return from checkbox [' + self.request.get('p') + '] Bulish_Harami ')
     #logging.info('Return from checkbox [' + self.request.get('GBPUSD') + '] hCheckBox [' + self.request.get('hGBPUSD') + ']')
      if len(self.request.get('Bulish_Harami')) > 0:
       #logging.info('Calling savePaternSettings ...... Selected ...')
       DbUtils.savePaternSettings(user.email(),self.request.get('p'),'Bulish_Harami',1)
      else:
       #logging.info('Calling savePaternSettings ...... NOT Selected ...')  
       DbUtils.savePaternSettings(user.email(),self.request.get('p'),'Bulish_Harami',0)
       
     
    if self.request.get('Berish_Harami') != self.request.get('hBerish_Harami'):
      #logging.info('Return from checkbox [' + self.request.get('p') + '] Berish_Harami ')
     #logging.info('Return from checkbox [' + self.request.get('GBPUSD') + '] hCheckBox [' + self.request.get('hGBPUSD') + ']')
      if len(self.request.get('Berish_Harami')) > 0:
     # logging.info('Calling saveUserSettings ......')
       DbUtils.savePaternSettings(user.email(),self.request.get('p'),'Berish_Harami',1)
      else:
       DbUtils.savePaternSettings(user.email(),self.request.get('p'),'Berish_Harami',0)
       
    self.redirect(self.request.uri)



app = webapp2.WSGIApplication([
  ('/.*', MainHandler),
], debug=True)