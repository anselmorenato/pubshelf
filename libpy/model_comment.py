from model import PubShelfModel

class Comment(PubShelfModel):
  def __init__(self, id=0, pubitem_id=0, title='', author='Anonymous', 
                    textbody='', created_at=''):
    self.id = id
    self.pubitem_id = pubitem_id
    self.author = author
    self.title = title
    self.textbody = textbody
    self.created_at = created_at

  def insert(self, cursor):
    sql = "INSERT INTO comments (pubitem_id,title,author,textbody) \
            VALUES (?,?,?,?)"
    cursor.execute(sql, (self.pubitem_id,self.title,self.author,self.textbody))

  def delete(self):
    sql = "DELETE FROM comments WHERE id=?"
    cursor = self.get_dbi().conn.cursor()
    cursor.execute(sql, self.id)

  def find_by_pubitem(self, pubitem):
    rv = []
    cur = self.get_dbi().conn.cursor()
    sql = "SELECT id,title,author,textbody,created_at FROM comments \
            WHERE pubitem_id=?"
    for row in cur.execute(sql, str(pubitem.id)):
      rv.append( Comment(id=row[0], title=row[1], author=row[2],
                          textbody=row[3], created_at=row[4]) )
    return rv

  def find(self):
    rv = []
    cur = self.get_dbi().conn.cursor()
    sql = "SELECT id,title,author,textbody,created_at FROM comments \
            WHERE id =?"
    for row in cur.execute(sql, str(self.id)):
      rv.append( Comment(id=row[0], title=row[1], author=row[2],
                          textbody=row[3],created_at=row[4]) )
    return rv

