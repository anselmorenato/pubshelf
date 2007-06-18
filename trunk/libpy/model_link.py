from model import PubShelfModel

class Link(PubShelfModel):
  def __init__(self, id=0, pubitem_id=0, uri='', created_at=''):
    self.id = id
    self.pubitem_id = pubitem_id
    self.uri = uri
    self.created_at = created_at

  def find_by_pubitem(self, pubitem):
    rv = []
    cur = self.get_dbi().conn.cursor()
    sql = "SELECT id, uri, created_at FROM links WHERE pubitem_id=?"
    for row in cur.execute(sql, str(pubitem.id)):
      rv.append( Link(id=row[0], uri=row[1], created_at=row[2]) )
    return rv
