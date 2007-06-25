import re, os, shutil
from model import PubShelfModel
from conf import PubShelfConf

class Link(PubShelfModel):
  def __init__(self, id=0, pubitem_id=0, name='', uri='', created_at=''):
    self.id = id
    self.pubitem_id = pubitem_id
    self.name = name
    self.uri = uri
    self.created_at = created_at

  def insert(self, cursor, pubitem):
    sql = "INSERT INTO links (pubitem_id, name, uri) VALUES (?,?,?)"
    conf = PubShelfConf()
    nickname = pubitem.nickname
    if( self.uri.startswith('/') ):
      target_suffix = re.search(r'\.([a-z]+)$', self.uri).group(1)

      target_dir1 = conf.item['dir_home']+conf.item['dir_db']
      target_dir2 = "%s%s/" % (target_dir1,str(pubitem.pub_year))
      if( not os.path.isdir(target_dir2) ): os.mkdir(target_dir2)

      target_filename = "%s_%s.%s" % (nickname, self.name, target_suffix)
      target_uri = "%s%s" % (target_dir2, target_filename)
      
      shutil.copyfile(self.uri, target_uri)
      self.uri = target_uri

    cursor.execute(sql, (self.pubitem_id, self.name, self.uri))

  def find_all(self):
    rv = []
    cursor = self.get_dbi().conn.cursor()
    sql = "SELECT id, name, uri, created_at FROM links"
    for row in cursor.execute(sql):
      rv.append( Link(id=row[0], name=row[1], uri=row[2], created_at=row[3]) )
    return rv

  def find_by_pubitem(self, pubitem):
    rv = []
    cur = self.get_dbi().conn.cursor()
    sql = "SELECT id, name, uri, created_at FROM links WHERE pubitem_id=?"
    for row in cur.execute(sql, str(pubitem.id)):
      rv.append( Link(id=row[0], name=row[1], uri=row[2], created_at=row[3]) )
    return rv
