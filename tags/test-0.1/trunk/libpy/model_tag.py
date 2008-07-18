from libpy.model import PubShelfModel

class Tag(PubShelfModel):
  def __init__(self, id=0, category='', name='', created_at=''):
    self.id = id
    self.category = category
    self.name = name
    self.created_at = created_at
    self.articles = []

  def clean_with_cursor(self, cursor):
    sql = "DELETE FROM tags WHERE id NOT IN \
            (SELECT DISTINCT tag_id FROM tags_pubitems)"
    cursor.execute(sql)

  def delete_with_cursor_and_pubitem(self, cursor, pubitem):
    sql = "DELETE FROM tags_pubitems WHERE pubitem_id=?"
    cursor.execute(sql, (pubitem.id,))

  def insert_with_cursor(self, cursor):
    sql = "INSERT INTO tags (category, name) VALUES (?,?)"
    cursor.execute(sql, (self.category, self.name))
    return cursor.lastrowid
    
  def insert_with_cursor_and_pubitem(self, cursor, pubitem):
    tag_id = self.is_available(cursor)
    if( tag_id < 0 ): tag_id = self.insert_with_cursor(cursor)

    sql = "INSERT INTO tags_pubitems (pubitem_id, tag_id) VALUES (?,?)"
    cursor.execute(sql, (pubitem.id, tag_id))

  def find_all(self):
    rv = []
    sql = "SELECT id, category, name FROM tags ORDER BY category, name"
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
    sql = "SELECT t.id, t.category, t.name \
            FROM tags AS t, tags_pubitems AS tp\
            WHERE tp.pubitem_id=? AND tp.tag_id=t.id"
    cur = self.get_dbi().conn.cursor()
    for row in cur.execute(sql, ( str(pubitem.id), )):
      rv.append( Tag(id=row[0], category=row[1], name=row[2]) )

    return rv 
