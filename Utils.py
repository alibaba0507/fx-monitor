from google.appengine.api import users
from google.appengine.ext import ndb

class Pair(ndb.Model):
  name = ndb.StringProperty()
  value = ndb.IntegerProperty()
  email = ndb.StringProperty()

class ActiveUser(ndb.Model):
  name = ndb.StringProperty()
  emial = ndb.StringProperty()
  lastModified = ndb.DateTimeProperty(auto_now_add=True)
