from model import PubShelfModel

class Comment(PubShelfModel):
  def __init__(self, id=0, pubitem_id=0, title='', textbody='', created_at=''):
    self.id = id
    self.pubitem_id = pubitem_id
    self.title = title
    self.textbody = textbody
    self.created_at = created_at

  def find_by_pubitem(self, pubitem):
    rv = []
    cur = self.get_dbi().conn.cursor()
    sql = "SELECT title, textbody FROM comments WHERE pubitem_id=?"
    for row in cur.execute(sql, str(pubitem.id)):
      rv.append( Comment(title=row[0], textbody=row[1]) )
    return rv

