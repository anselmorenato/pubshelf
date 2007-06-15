class Link:
  def __init__(self, id=0, pubitem_id=0, uri='', created_at=''):
    self.id = id
    self.pubitem_id = pubitem_id
    self.uri = uri
    self.created_at = created_at
  def get_links_by_pubitem(self, pubitem):
    rv = []
    sql = "SELECT uri FROM links WHERE pubitem_id='%d'"\
          % (pubitem.id)
    for row in self.conn.execute(sql):
      rv.append( Link(uri=row[0]) )
    return rv
