import webapp2
#import jinja2
import urllib2
import urllib
import json
import os
import unicodedata
from google.appengine.ext.webapp import template
from google.appengine.api import urlfetch
import cachedJson
from google.appengine.api import memcache
import logging
from google.appengine.api import mail
#from Utils import LoginInfo
from google.appengine.api import users
import News

'''
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])
'''

class MainHandler(webapp2.RequestHandler):
  
  def get(self):
    userInfo = getLoginInfo(self.request.uri)
    if slef.request.get('news'):
      resp = News.search(slef.request.get('q'),slef.request.get('p'))
      self.response.out.write(resp)
    if self.request.get('clear'):
      cachedJson.clearData()
    elif self.request.get('email'):
      email = self.request.get('email')
      msg = '<p>Test for Html message <br/><ul> Some list <li> List 1</li><li>List 2</li></ul>'
      message = mail.EmailMessage(sender="fx2go4u@gmail.com",
                            subject="SR Level broken ...")
      message.to = email
      message.body = """
      Dear Ali baba:
      """
      message.html = msg
      message.send()
      #logging.debug('Email has been send to [' + email + ']')
    # geting history table of the patterns as json format
    elif self.request.get('c'):
      msg = cachedJson.checkSRLevels()
      if msg and len(msg) > 0:
        message = mail.EmailMessage(sender="Fx-Monitor Support <fx2go4u@gmail.com>",
                            subject="SR Level broken ...")
        message.to = "Ali baba <fx2go4u@gmail.com>"
        message.body = """
        Dear Ali baba:
        
        """ 
        
        message.html = msg
        message.send()
    elif self.request.get('sendEmailForPatternAlert'):
      cachedJson.sendEmailForPatternAlert() #cron to send emails to user
    elif self.request.get('checkPatterns'):
      cachedJson.chekEmailPatterns() # cron run once a day and record patterns
    elif self.request.get('cron'):
      cachedJson.loadData()
    elif self.request.get('pair'):
      #cachedJson.clearData()
      pair = self.request.get('pair')
      cachedJson.loadData()
      if pair == 'gbpusd':
        hist_json = memcache.get('h_gbp')
      elif pair == 'eurusd':
        hist_json = memcache.get('h_eur')
      elif pair == 'usdchf':
        hist_json = memcache.get('h_chf')
      elif pair == 'usdcad':
        hist_json = memcache.get('h_cad')
      elif pair == 'audusd':
        hist_json = memcache.get('h_aud')
      elif pair == 'eurgbp':
        hist_json = memcache.get('h_eurgbp')
      elif pair == 'eurjpy':
        hist_json = memcache.get('h_eurjpy')
      elif pair == 'gbpjpy':
        hist_json = memcache.get('h_gbpjpy')
    
      big_f = []
      if hist_json is not None and len(hist_json):
        cnt = 0
        resultJSON = json.loads(hist_json)
        for elem in resultJSON['hist']:
          f = []
          cnt += 1
          if cnt > 20: break # only 20 rows to collect for now.later must implement some filter
          i = 0
          for e in elem:
           s = urllib.unquote(e).decode("utf-8")
           if i == 2: # fromat time
            l = s.split('T')
            if len(l) > 0:
             s = '&nbsp;' + l[0] + '&nbsp;'
           f.append(s )
           i += 1
          
          big_f.append(f)
        
        pair_html = '<p> For price distribution price check ... <br /> '
        pair_html += '<a href="/?pair=gbpusd">GBPUSD</a>, '
        pair_html += '<a href="/?pair=eurusd">EURUSD</a>, '
        pair_html += '<a href="/?pair=usdchf">USDCHF</a>, '
        pair_html += '<a href="/?pair=usdcad">USDCAD</a>, '
        pair_html += '<a href="/?pair=audusd">AUDUSD</a>, '
        pair_html += '<a href="/?pair=eurgbp">EURGBP</a>, '
        pair_html += '<a href="/?pair=gbpjpy">GBPJPY</a>, '
        pair_html += '<a href="/?pair=eurjpy">EURJPY</a>'
        
        if resultJSON['chart'] and len(resultJSON['chart']) != 0:
          user = users.get_current_user()
          if user is None:
           template_values = {
             'pair_html' : pair_html,
             'chart' : resultJSON['chart'] ,
             'pair' : self.request.get('pair'),
             'html_table' : big_f,
             'url' : userInfo[0],
             'url_text' : userInfo[1],
             'user' : userInfo[2]
           }
          else:
             template_values = {
             'pair_html' : pair_html,
             'chart' : resultJSON['chart'] ,
             'pair' : self.request.get('pair'),
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
        else:
          user = users.get_current_user()
          if user is None:
           template_values = {
            'pair_html' : pair_html,
            'pair' : self.request.get('pair'),
            'html_table' : big_f,
            'url' : userInfo[0],
            'url_text' : userInfo[1],
            'user' : userInfo[2]
           }
          else:
           template_values = {
            'pair_html' : pair_html,
            'pair' : self.request.get('pair'),
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
    elif self.request.get('r'):
      cachedJson.loadData()
      #url_link = "https://script.google.com/macros/s/AKfycbzFDj3RD57LI-W8ppcyHVhNq_3-_MQ-WUP9sttWZoO8ocvhF-Dh/exec?r=1"
      pair = None
      if self.request.get('p'):
        pair = self.request.get('p')
        #url_link += "&p=" + self.request.get('p')
      #urlfetch.set_default_fetch_deadline(45)
      #result = urlfetch.fetch(url_link)
      #logging.debug(url_link)
      #resultJSON = json.loads(result.content)
      resultJSON = json.loads(memcache.get('sr_lines'))
      #logging.debug(urllib.unquote(resultJSON['0']).decode("utf-8"))
      table = '<table border = 1><tr><td>Pair</td><td>price</td><td>time</td></tr>'
      j = 0
      for e in resultJSON:
        table += '<tr>'
        if pair is None or (pair and pair.upper() == resultJSON[str(j)]['name'].upper()):
          table += '<td>' + resultJSON[str(j)]['name'] + '</td><td>' + str(resultJSON[str(j)]['price']) + '</td><td>' + resultJSON[str(j)]['time'] + '</td>'
        #logging.debug(resultJSON[str(j)]['time'])
        j += 1
      '''
        #table += '<tr>'
        #table += '<td>' + e['name'] + '</td><td>' + e['price'] + '</td><td>' + e['time']  + '</td>'
        #table += '</tr>'
      '''
      table += '</table>'
      
      pair_html = '<p> For price distribution price check ... <br /> '
      pair_html += '<a href="/?r=1&p=gbpusd">GBPUSD</a>, '
      pair_html += '<a href="/?r=1&p=eurusd">EURUSD</a>, '
      pair_html += '<a href="/?r=1&p=usdchf">USDCHF</a>, '
      pair_html += '<a href="/?r=1&p=usdcad">USDCAD</a>, '
      pair_html += '<a href="/?r=1&p=audusd">AUDUSD</a>, '
      pair_html += '<a href="/?r=1&p=eurgbp">EURGBP</a>, '
      pair_html += '<a href="/?r=1&p=gbpjpy">GBPJPY</a>, '
      pair_html += '<a href="/?r=1&p=eurjpy">EURJPY</a>'
      
      if self.request.get('p'):
        user = users.get_current_user()
        if user is None:
         template_values = {
          'pair_html' : pair_html,
          'pair' : self.request.get('p'),
          'table' : table,
          'url' : userInfo[0],
          'url_text' : userInfo[1],
          'user' : userInfo[2]
         }
        else:
         template_values = {
          'pair_html' : pair_html,
          'pair' : self.request.get('p'),
          'table' : table,
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
      else:
        user = users.get_current_user()
        if user is None:
         template_values = {
           'pair_html' : pair_html,
          'table' : table,
          'url' : userInfo[0],
          'url_text' : userInfo[1],
          'user' : userInfo[2]
         }
        else:
         template_values = {
          'pair_html' : pair_html,
          'pair' : self.request.get('p'),
          'table' : table,
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
    elif self.request.get('pv'):
      #cachedJson.clearData()
      cachedJson.loadData()
      hist_json = memcache.get('pv')
      logging.debug('Pass PV param')
      pair = None
      if self.request.get('p'):
        pair = self.request.get('p')
      big_f = []
      if hist_json is not None and len(hist_json):
        resultJSON = json.loads(hist_json)
        cnt = 0;
        for elem in resultJSON['hist']:
          f = []
          if cnt > 20: break
          #self.response.write("<tr>")
          i = 0
          b_found = 0
          for e in elem:
            if e.strip() == '': 
             break            
            if i == 0 and (pair is None or (pair and pair.upper() == e.upper())):
             f.append(urllib.unquote(e).decode("utf-8") )
             b_found = 1
            elif i != 0 and b_found == 1:
              s = urllib.unquote(e).decode("utf-8")
              if i == 2: # fromat time
                l = s.split('T')
                if len(l) > 0:
                  s = ' &nbsp; ' + l[0] + '&nbsp; ' 
              f.append( s)
            i += 1
          if b_found == 1:
            cnt += 1
            #self.response.write("<td>" + urllib.unquote(e).decode("utf-8") + "</td>")
          big_f.append(f)
       
        pair_html = '<p> For price distribution price check ... <br /> '
        pair_html += '<a  href="/?pv=1&p=gbpusd">GBPUSD</a>, '
        pair_html += '<a  href="/?pv=1&p=eurusd">EURUSD</a>, '
        pair_html += '<a  href="/?pv=1&p=usdchf">USDCHF</a>, '
        pair_html += '<a  href="/?pv=1&p=usdcad">USDCAD</a>, '
        pair_html += '<a  href="/?pv=1&p=audusd">AUDUSD</a>, '
        pair_html += '<a  href="/?pv=1&p=eurgbp">EURGBP</a>, '
        pair_html += '<a  href="/?pv=1&p=gbpjpy">GBPJPY</a>, '
        pair_html += '<a  href="/?pv=1&p=eurjpy">EURJPY</a>'
       
        user = users.get_current_user()
        if user is None:
          template_values = {
            'pair_html' : pair_html,
            'html_table' : big_f,
            'url' : userInfo[0],
            'url_text' : userInfo[1],
            'user' : userInfo[2]
          }
        else:
           template_values = {
            'pair_html' : pair_html,
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
    else:
      cachedJson.loadData()
      #cachedJson.checkSRLevels()
      hist_json = memcache.get('hist')
      cn = 0
      big_f = []
      if hist_json is not None and len(hist_json):
        resultJSON = json.loads(hist_json)
        cnt = 0
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
            #self.response.write("<td>" + urllib.unquote(e).decode("utf-8") + "</td>")
          big_f.append(f)
       
        pair_html = '<p> For price distribution price check ... <br /> '
        pair_html += '<a href="/?pair=gbpusd">GBPUSD</a>, '
        pair_html += '<a href="/?pair=eurusd">EURUSD</a>, '
        pair_html += '<a href="/?pair=usdchf">USDCHF</a>, '
        pair_html += '<a href="/?pair=usdcad">USDCAD</a>, '
        pair_html += '<a href="/?pair=audusd">AUDUSD</a>, '
        pair_html += '<a href="/?pair=eurgbp">EURGBP</a>, '
        pair_html += '<a href="/?pair=gbpjpy">GBPJPY</a>, '
        pair_html += '<a href="/?pair=eurjpy">EURJPY</a>'
       
        user = users.get_current_user()
        if user is None:
          template_values = {
            'pair_html' : pair_html,
            'html_table' : big_f,
            'url' : userInfo[0],
            'url_text' : userInfo[1],
            'user' : userInfo[2]
            
          }
        else:
          template_values = {
            'pair_html' : pair_html,
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
          #self.response.write("</tr>")   
        #self.response.write("</table")
      #template = JINJA_ENVIRONMENT.get_template('index.html')
      #self.response.write(template.render(template_values))
      
  def post(self):
    user = users.get_current_user()
    l = []
    #logging.debug('Strong_Pearcing [' + self.request.get('Strong_Pearcing') + '][' + self.request.get('hStrong_Pearcing') + '][' + self.request.get('p') + ']')
    if self.request.get('Strong_Pearcing') != self.request.get('hStrong_Pearcing'):
     #logging.info('Return from checkbox [' + self.request.get('p') + '] Strong_Pearcing ')
     if len(self.request.get('Strong_Pearcing')) > 0:
     # logging.info('Calling saveUserSettings ......')
      cachedJson.savePaternSettings(user.email(),self.request.get('p'),'Strong_Pearcing',1)
     else:
       cachedJson.savePaternSettings(user.email(),self.request.get('p'),'Strong_Pearcing',0)
    
    if self.request.get('Strong_Dark_cloud') != self.request.get('hStrong_Dark_cloud'):
     #logging.info('Return from checkbox [' + self.request.get('p') + '] Strong_Dark_cloud ')
     if len(self.request.get('Strong_Dark_cloud')) > 0:
     # logging.info('Calling saveUserSettings ......')
      cachedJson.savePaternSettings(user.email(),self.request.get('p'),'Strong_Dark_cloud',1)
     else:
       cachedJson.savePaternSettings(user.email(),self.request.get('p'),'Strong_Dark_cloud',0)
       
    
     if self.request.get('Pearcing') != self.request.get('hPearcing'):
      #logging.info('Return from checkbox [' + self.request.get('p') + '] Pearcing ')
      if len(self.request.get('Pearcing')) > 0:
     # logging.info('Calling saveUserSettings ......')
       cachedJson.savePaternSettings(user.email(),self.request.get('p'),'Pearcing',1)
      else:
       cachedJson.savePaternSettings(user.email(),self.request.get('p'),'Pearcing',0)
    
     logging.debug('Dark_cloud [' + self.request.get('Dark_cloud') + '][' + self.request.get('hDark_cloud') + '][' + self.request.get('p') + ']')
   
    if self.request.get('Dark_cloud') != self.request.get('hDark_cloud'):
      #logging.info('Return from checkbox [' + self.request.get('p') + '] Dark_cloud ')
     #logging.info('Return from checkbox [' + self.request.get('GBPUSD') + '] hCheckBox [' + self.request.get('hGBPUSD') + ']')
      if len(self.request.get('Dark_cloud')) > 0:
     # logging.info('Calling saveUserSettings ......')
       cachedJson.savePaternSettings(user.email(),self.request.get('p'),'Dark_cloud',1)
      else:
       cachedJson.savePaternSettings(user.email(),self.request.get('p'),'Dark_cloud',0)
    
    if self.request.get('Bulish_Endulfing') != self.request.get('hBulish_Endulfing'):
     # logging.info('Return from checkbox [' + self.request.get('p') + '] Bulish_Endulfing ')
     #logging.info('Return from checkbox [' + self.request.get('GBPUSD') + '] hCheckBox [' + self.request.get('hGBPUSD') + ']')
      if len(self.request.get('Bulish_Endulfing')) > 0:
     # logging.info('Calling saveUserSettings ......')
       cachedJson.savePaternSettings(user.email(),self.request.get('p'),'Bulish_Endulfing',1)
      else:
       cachedJson.savePaternSettings(user.email(),self.request.get('p'),'Bulish_Endulfing',0)
       
    if self.request.get('Berish_Endulfing') != self.request.get('hBerish_Endulfing'):
    #logging.info('Return from checkbox [' + self.request.get('p') + '] Berish_Endulfing ')
     #logging.info('Return from checkbox [' + self.request.get('GBPUSD') + '] hCheckBox [' + self.request.get('hGBPUSD') + ']')
      if len(self.request.get('Berish_Endulfing')) > 0:
     # logging.info('Calling saveUserSettings ......')
       cachedJson.savePaternSettings(user.email(),self.request.get('p'),'Berish_Endulfing',1)
      else:
       cachedJson.savePaternSettings(user.email(),self.request.get('p'),'Berish_Endulfing',0)
       
    
    if self.request.get('Bulish_Harami') != self.request.get('hBulish_Harami'):
      #logging.info('Return from checkbox [' + self.request.get('p') + '] Bulish_Harami ')
     #logging.info('Return from checkbox [' + self.request.get('GBPUSD') + '] hCheckBox [' + self.request.get('hGBPUSD') + ']')
      if len(self.request.get('Bulish_Harami')) > 0:
       #logging.info('Calling savePaternSettings ...... Selected ...')
       cachedJson.savePaternSettings(user.email(),self.request.get('p'),'Bulish_Harami',1)
      else:
       #logging.info('Calling savePaternSettings ...... NOT Selected ...')  
       cachedJson.savePaternSettings(user.email(),self.request.get('p'),'Bulish_Harami',0)
       
     
    if self.request.get('Berish_Harami') != self.request.get('hBerish_Harami'):
      #logging.info('Return from checkbox [' + self.request.get('p') + '] Berish_Harami ')
     #logging.info('Return from checkbox [' + self.request.get('GBPUSD') + '] hCheckBox [' + self.request.get('hGBPUSD') + ']')
      if len(self.request.get('Berish_Harami')) > 0:
     # logging.info('Calling saveUserSettings ......')
       cachedJson.savePaternSettings(user.email(),self.request.get('p'),'Berish_Harami',1)
      else:
       cachedJson.savePaternSettings(user.email(),self.request.get('p'),'Berish_Harami',0)
       
    self.redirect(self.request.uri)

    #path = os.path.join(os.path.dirname(__file__), 'index1.html')
    #self.response.out.write(template.render(path,template_values))
app = webapp2.WSGIApplication([
  ('/.*', MainHandler),
], debug=True)