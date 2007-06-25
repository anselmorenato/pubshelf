import os
from pysqlite2 import dbapi2 as sqlite
from conf import PubShelfConf

class PubShelfDBI:
  def __init__(self):
    conf = PubShelfConf()
    db_file = conf.item['dir_home']+conf.item['dir_db']+conf.item['db_name']

    try:
      self.conn = sqlite.connect(db_file);
    except:
      print "Database error : check %s" % db_file
