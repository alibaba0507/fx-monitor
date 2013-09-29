import json
from google.appengine.api import memcache
import logging
from google.appengine.api import users
import urllib
import DbUtils


def getCachedPairData(pair):
  if pair == 'gbpusd':
    return memcache.get('h_gbp')
  elif pair == 'eurusd':
    return memcache.get('h_eur')
  elif pair == 'usdchf':
    return memcache.get('h_chf')
  elif pair == 'usdcad':
    return memcache.get('h_cad')
  elif pair == 'audusd':
   return memcache.get('h_aud')
  elif pair == 'eurgbp':
    return memcache.get('h_eurgbp')
  elif pair == 'eurjpy':
    return memcache.get('h_eurjpy')
  elif pair == 'gbpjpy':
    return memcache.get('h_gbpjpy')
    
    
def constTemplateValues(userInfo,patternList):
  user = users.get_current_user()
  if user:
    template_values = {
     'pair_html' : getPairsAsLinks(),
     'html_table' : patternList,
     'url' : userInfo[0],
     'url_text' : userInfo[1],
     'user' : userInfo[2],
     'GBPUSD' : DbUtils.getUserPatternSettings(user.email(),'GBPUSD'),
     'EURUSD' : DbUtils.getUserPatternSettings(user.email(),'EURUSD'),
     'USDCHF' : DbUtils.getUserPatternSettings(user.email(),'USDCHF'),
     'USDCAD' : DbUtils.getUserPatternSettings(user.email(),'USDCAD'),
     'AUDUSD' : DbUtils.getUserPatternSettings(user.email(),'AUDUSD'),
     'EURGBP' : DbUtils.getUserPatternSettings(user.email(),'EURGBP'),
     'GBPJPY' : DbUtils.getUserPatternSettings(user.email(),'GBPJPY'),
     'EURJPY' : DbUtils.getUserPatternSettings(user.email(),'EURJPY'),
     'USDJPY' : DbUtils.getUserPatternSettings(user.email(),'USDJPY')
     }
  else:
    template_values = {
        'pair_html' : getPairsAsLinks(),
        'html_table' : patternList,
        'url' : userInfo[0],
        'url_text' : userInfo[1],
        'user' : userInfo[2]
            
      }
  return template_values
#this will get json and will
#parse it to list
def constPatternList(ls,pair):
  big_f = []
  cnt = 0
  for elem in ls:
   f = []
   cnt += 1
   if cnt > 20: break # only 20 rows to collect for now.later must implement some filter
   i = 0
   b_found = 0
   for e in elem:
    s = urllib.unquote(e).decode("utf-8") 
    if i == 0 and (pair is None or (pair and pair.upper() == s.upper())):
     b_found = 1
    if i == 2: # fromat time
     l = s.split('T')
     if len(l) > 0:
      s = '&nbsp;' + l[0] + '&nbsp;'
    if b_found == 1:
     f.append(s )
    i += 1
   big_f.append(f)
  return big_f
  
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

def getPairsAsLinks():
  pair_html = '<p> For price distribution price check ... <br /> '
  pair_html += '<a href="/?pair=gbpusd">GBPUSD</a>, '
  pair_html += '<a href="/?pair=eurusd">EURUSD</a>, '
  pair_html += '<a href="/?pair=usdchf">USDCHF</a>, '
  pair_html += '<a href="/?pair=usdcad">USDCAD</a>, '
  pair_html += '<a href="/?pair=audusd">AUDUSD</a>, '
  pair_html += '<a href="/?pair=eurgbp">EURGBP</a>, '
  pair_html += '<a href="/?pair=gbpjpy">GBPJPY</a>, '
  pair_html += '<a href="/?pair=eurjpy">EURJPY</a>'
  return pair_html
  

def loadPatternHistory(uri):
  