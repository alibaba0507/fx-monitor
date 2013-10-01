from google.appengine.ext import ndb
from google.appengine.api import memcache
import logging

#db table for pattern
class Pivots(ndb.Model):
  name = ndb.StringProperty()
  email = ndb.StringProperty()
  child_1 = ndb.StringProperty()
  child_2 = ndb.StringProperty()
  # This will change any time when pattern of the day is found
  sendEmail = ndb.IntegerProperty(default = 0)