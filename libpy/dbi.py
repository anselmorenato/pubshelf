import os
import sqlite3
#from pysqlite2 import dbapi2 as sqlite
from conf import PubShelfConf

class PubShelfDBI:
  def __init__(self):
    conf = PubShelfConf()
    db_file = os.path.join(conf.item['dir_db'],conf.item['db_name'])

    try:
      #self.conn = sqlite.connect(db_file)
      self.conn = sqlite3.connect(db_file)
    except:
      print "Database error : check %s" % db_file
