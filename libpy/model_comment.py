class Comment:
  def __init__(self, id=0, pubitem_id=0, title='', textbody='', created_at=''):
    self.id = id
    self.pubitem_id = pubitem_id
    self.title = title
    self.textbody = textbody
    self.created_at = created_at
  def get_comments_by_pubitem(self, pubitem):
    rv = []
    sql = "SELECT title, textbody FROM comments WHERE pubitem_id='%d'"\
          % (pubitem.id)
    for row in self.conn.execute(sql):
      rv.append( Comment(title=row[0], textbody=row[1]) )
    return rv

