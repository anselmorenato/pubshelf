class Tag:
  def __init__(self, id=0, category='', name='', created_at=''):
    self.id = id
    self.category = category
    self.name = name
    self.created_at = created_at
    self.articles = []
 
   def get_tags_by_pubitem(self, pubitem):
    rv = []
    sql = "SELECT t.id, t.category, t.name FROM tags AS t, tags_pubitems AS tp\
            WHERE tp.pubitem_id='%d' AND tp.tag_id=t.id" % (pubitem.id)
    for row in self.conn.execute(sql):
      rv.append( Tag(id=row[0], category=row[1], name=row[2]) )
    return rv 