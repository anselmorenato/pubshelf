import os
from pysqlite2 import dbapi2 as sqlite
from conf import PubShelfConf

class PubShelfDBI:
  def __init__(self):
    conf = PubShelfConf()
    db_file1 = '../'+conf.item['dbpath']+conf.item['dbname'];
    db_file2 = './'+conf.item['dbpath']+conf.item['dbname'];
    
    db_file = ''
    if( os.access(db_file1, os.F_OK) ): db_file = db_file1
    elif( os.access(db_file2, os.F_OK) ): db_file = db_file2

    try:
      self.conn = sqlite.connect(db_file);
    except:
      print "Database error : check %s" % db_file
