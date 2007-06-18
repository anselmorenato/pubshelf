#from data import Tag, Link, Comment
import sys,re
from dbi import PubShelfDBI

class PubItem:
  def __init__(self, id=0, nickname='', title='', authors='', journal=''\
               , publisher='', volume='', page='', pub_year=0, pub_type=''\
               , created_at=''):
    self.id = id
    self.nickname = nickname
    self.title = title
    self.authors = authors
    self.journal = journal
    self.publisher = publisher
    self.volume = volume
    self.page = page
    self.pub_year = pub_year
    self.pub_type = pub_type
    self.created_at = created_at

    self.tags = []
    self.comments = []
    self.links = []
    
  def get_dbi(self):
    try:
      return self.dbi
    except:
      self.dbi = PubShelfDBI()
      return self.dbi

  def set_tags(self,tags):
    self.tags = tags
  
  def set_links(self,links):
    self.links = links

  def set_comments(self,comments):
    self.comments = comments

  def get_citation(self):
    rv = "%s, %s, %s" % (self.authors,self.title,self.journal)
    rv += self.get_volume_page() + " (%d)" % self.pub_year
    return rv
  
  def get_html_citation(self):
    rv = "%s, <b>%s</b>, <i>%s</i>" % (self.authors,self.title,self.journal)
    rv += self.get_volume_page() + " (%d)" % self.pub_year
    return rv

  def get_volume_page(self):
    rv = ''
    if( self.volume ): rv += ", %s" % self.volume
    if( self.page ): rv += ":%s" % self.page
    return rv

  def get_nickname_base(self):
    first_author = self.authors.split(',')[0]
    first_author_surname  = re.sub(r'[A-Z\-]+$','',first_author)
    first_author_surname  = re.sub(r'\s+','',first_author_surname)
    return "%s%d" % (first_author_surname,self.pub_year)

  def set_nickname(self):
    cur = self.get_dbi().conn.cursor()
    sql = "SELECT count(id) FROM pubitems WHERE nickname like '"
    sql += self.get_nickname_base()+"%'"
    cur.execute(sql)
    self.nickname = "%s.%d" % (self.get_nickname_base(), cur.fetchone()[0]+1)

  def insert(self):
    cur = self.get_dbi().conn.cursor()
    if( self.nickname == '' ): self.set_nickname()
    try:
      cur.execute("INSERT INTO pubitems\
              (nickname, pub_type, title, authors, journal, publisher,\
              volume, page, pub_year) VALUES (?,?,?,?,?,?,?,?,?)",
              (self.nickname, self.pub_type, self.title,
              self.authors, self.journal, self.publisher,
              self.volume, self.page, self.pub_year))
      pubitem_id = cur.lastrowid
      for tag in self.tags:
        cur.execute("INSERT INTO tags (category, name) VALUES (?,?)",
              (tag.category, tag.name))
      self.get_dbi().conn.commit()
    except:
      print "Error in insert PubItem"

      
    #for link in self.links:
    #  self.dbi.conn.execute('INSERT INTO links (pubitem_id, uri) VALUES (?,?)',
    #          (self_id, link.uri))

"""
  def find_by_tag(self, category, name):
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
"""
