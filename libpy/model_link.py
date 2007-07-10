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

  def update_uri(self):
    cursor = self.get_dbi().conn.cursor()
    sql = "UPDATE links SET uri=? WHERE id=?"
    cursor.execute(sql, (self.uri, self.id))
    self.get_dbi().conn.commit()
    
  def delete_with_cursor_and_pubitem(self, cursor, pubitem):
    sql = "DELETE FROM links WHERE pubitem_id=?"
    cursor.execute("DELETE FROM links WHERE pubitem_id=?",[pubitem.id])
    
  def insert_with_cursor_and_pubitem(self, cursor, pubitem):
    sql = "INSERT INTO links (pubitem_id, name, uri) VALUES (?,?,?)"
    conf = PubShelfConf()
    nickname = pubitem.nickname
    if( os.path.isfile(self.uri) ):
      pub_year = str(pubitem.pub_year)
      file_dir = os.path.join(conf.item['dir_db'], pub_year)
      if( not os.path.isdir(file_dir) ): os.mkdir(file_dir)

      file_suffix = re.search(r'\.([a-z]+)$', self.uri).group(1)
      filename = "%s_%s.%s" % (nickname, self.name, file_suffix)
      file_path = os.path.join(file_dir, filename)
      
      if( self.uri != file_path ):
        shutil.copyfile(self.uri, file_path)
        self.uri = os.path.join(pub_year, filename)

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
    for row in cur.execute(sql, (str(pubitem.id),)):
      rv.append( Link(id=row[0], name=row[1], uri=row[2], created_at=row[3]) )
    return rv
