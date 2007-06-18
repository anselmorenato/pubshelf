from model import PubShelfModel

class Tag(PubShelfModel):
  def __init__(self, id=0, category='', name='', created_at=''):
    self.id = id
    self.category = category
    self.name = name
    self.created_at = created_at
    self.articles = []

  def insert(self, cursor):
    sql = "INSERT INTO tags (category, name) VALUES (?,?)"
    cursor.execute(sql, (self.category, self.name))
    return cursor.lastrowid
    
  def insert_with_pubitem_id(self, cursor, pubitem_id):
    tag_id = self.is_available(cursor)
    if( tag_id < 0 ):
      tag_id = self.insert(cursor)

    sql = "INSERT INTO tags_pubitems (pubitem_id, tag_id) VALUES (?,?)"
    cursor.execute(sql, (pubitem_id, tag_id))

  def find_all(self):
    rv = []
    sql = "SELECT id, category, name FROM tags"
    for row in self.get_dbi().conn.execute(sql):
      rv.append( Tag(id=row[0], category=row[1], name=row[2]) )
    return rv

  def is_available(self,cursor):
    sql = "SELECT id FROM tags where category=? AND name=?"
    cursor.execute(sql, (self.category, self.name))
    try:
      return cursor.fetchone()[0]
    except:
      return -1

  def find_by_pubitem(self, pubitem):
    rv = []

  #def find_by_name_and_category(self, cur, name, category):
  #  sql = "SELECT id FROM tags where category=? AND name=?"
  #  cur.execute(sql, (category, name))
  #  tag_id = 0
  #  
  #  try:
  #    tag_id = cur.fetchone()[0]
  #  except:
  #    sql = "INSERT INTO tags (category, name) VALUES (?,?)"
  #    cur.execute(sql, (self.category, self.name))
  #    tag_id = cur.lastrowid
  # 
  #  return Tag(id=tag_id, name=name, category=category)

  def find_by_pubitem(self, pubitem):
    rv = []
    sql = "SELECT t.id, t.category, t.name \
            FROM tags AS t, tags_pubitems AS tp\
            WHERE tp.pubitem_id=? AND tp.tag_id=t.id"
    cur = self.get_dbi().conn.cursor()
    for row in cur.execute(sql, str(pubitem.id)):
      rv.append( Tag(id=row[0], category=row[1], name=row[2]) )

    return rv 
