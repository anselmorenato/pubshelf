from pysqlite2 import dbapi2 as sqlite
from data import PubItem, Link, Comment, Tag;

class PubShelfDBI:
  def __init__(self, conf):
    db_file = conf['dbpath']+conf['dbname'];
    self.conn = sqlite.connect(db_file);
    #self.conn = sqlite3.connect(db_file);

  def get_tags(self):
    rv = dict();
    for row in self.conn.execute('SELECT t.id, t.category, t.name, \
                                    t.created_at, tp.pubitem_id\
                                  FROM tags AS t, tags_pubitems AS tp\
                                  WHERE t.id=tp.tag_id'):
      tag = Tag(id=row[0], category=row[1], name=row[2], created_at=row[3]);
      if( not rv.has_key(tag.id) ):
        rv[tag.id] = tag
    
    return rv.values()
  
  def get_pubitems_by_tag(self, tag_category, tag_name):
    rv = [];
    sql = "SELECT DISTINCT p.id, p.nickname, p.pub_type, p.title, p.authors, \
            p.journal, p.publisher, p.volume, p.page, p.pub_year, p.created_at\
            FROM pubitems AS p, tags_pubitems AS tp, tags AS t \
            WHERE p.id=tp.pubitem_id AND tp.tag_id=t.id \
              AND t.category='%s' AND t.name='%s' ORDER BY p.pub_year DESC" \
              % (tag_category, tag_name)

    for row in self.conn.execute(sql):
      pubitem = PubItem(id=row[0], nickname=row[1], pub_type=row[2], \
                  title=row[3], authors=row[4], journal=row[5], \
                  publisher=row[6], volume=row[7], page=row[8], \
                  pub_year=row[9], created_at=row[10])
      rv.append(pubitem)

    return rv
  
  def get_pubitem_by_nickname(self, nickname):
    sql = "SELECT DISTINCT p.id, p.nickname, p.pub_type, p.title, p.authors,\
            p.journal, p.publisher, p.volume, p.page, p.pub_year, p.created_at\
            FROM pubitems AS p WHERE p.nickname='%s'" % (nickname)
    
    for row in self.conn.execute(sql):
      pubitem = PubItem(id=row[0], nickname=row[1], pub_type=row[2], \
                  title=row[3], authors=row[4], journal=row[5], \
                  publisher=row[6], volume=row[7], page=row[8], \
                  pub_year=row[9], created_at=row[10])
      pubitem.set_links( self.get_links_by_pubitem(pubitem) )
      pubitem.set_tags( self.get_tags_by_pubitem(pubitem) )
      pubitem.set_comments( self.get_comments_by_pubitem(pubitem) )
      return pubitem
  
  def get_comments_by_pubitem(self, pubitem):
    rv = []
    sql = "SELECT title, textbody FROM comments WHERE pubitem_id='%d'"\
          % (pubitem.id)
    for row in self.conn.execute(sql):
      rv.append( Comment(title=row[0], textbody=row[1]) )
    return rv

  def get_links_by_pubitem(self, pubitem):
    rv = []
    sql = "SELECT name, uri, uri_type FROM links WHERE pubitem_id='%d'"\
          % (pubitem.id)
    for row in self.conn.execute(sql):
      rv.append( Link(name=row[0], uri=row[1], uri_type=row[2]) )
    return rv

  def get_tags_by_pubitem(self, pubitem):
    rv = []
    sql = "SELECT t.id, t.category, t.name FROM tags AS t, tags_pubitems AS tp\
            WHERE tp.pubitem_id='%d' AND tp.tag_id=t.id" % (pubitem.id)
    for row in self.conn.execute(sql):
      rv.append( Tag(id=row[0], category=row[1], name=row[2]) )
    return rv

  def get_pubitems_by_tag_category(self, tag_category):
    rv = [];
    sql = "SELECT DISTINCT p.id, p.nickname, p.pub_type, p.title, p.authors,\
            p.journal, p.publisher, p.volume, p.page, p.pub_year, p.created_at\
            FROM pubitems AS p, tags_pubitems AS tp, tags AS t\
            WHERE p.id=tp.pubitem_id AND tp.tag_id=t.id\
              AND t.category='%s' ORDER BY p.pub_year DESC" % tag_category
    for row in self.conn.execute(sql):
      pubitem = PubItem(id=row[0], nickname=row[1], pub_type=row[2], 
                  title=row[3], authors=row[4], journal=row[5], 
                  publisher=row[6], volume=row[7], page=row[8], 
                  pub_year=row[9], created_at=row[10])
      rv.append(pubitem)
    return rv
