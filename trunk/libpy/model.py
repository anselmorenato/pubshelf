from libpy.conf import PubShelfConf
from libpy.dbi import PubShelfDBI

class PubShelfModel:
  def __init__(self):
    psconf = PubShelfConf()
    self.conf = psconf.item
    self.sql  = psconf.sql

  def get_dbi(self):
    try: 
      return self.dbi
    except:
      self.dbi = PubShelfDBI()
      return self.dbi
  
  def get_sql(self, keyword):
    try:
      return self.sql[keyword]
    except:
      psconf = PubShelfConf()
      self.sql = psconf.sql
      return self.sql[keyword]
