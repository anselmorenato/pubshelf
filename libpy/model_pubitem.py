#from data import Tag, Link, Comment
import sys,re
from dbi import PubShelfDBI
from model import PubShelfModel
from model_tag import Tag
from model_comment import Comment
from model_link import Link

class PubItem(PubShelfModel):
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
    
  def get_citation(self):
    rv = "%s, %s, %s" % (self.authors,self.title,self.journal)
    rv += self.get_volume_page() + " (%d)" % self.pub_year
    return rv
  
  def get_html_citation(self):
    rv = "%s, <b>%s</b>, <i>%s</i>" % (self.authors,self.title,self.journal)
    rv += self.get_volume_page() + " (%d)" % self.pub_year
    return rv

  def get_export_citation(self):
    ## bibtex
    bibtex_authors = self.authors.replace('; ',' and ')
    bibtex_page = self.page.replace('-','--')
    bibtex = "@article{%s,\n  title={{%s}},\n  author={%s},\n  journal={%s},\n  volume={%s},\n  pages={%s},\n  year={%d}\n}\n\n" 
    return bibtex % (self.nickname, self.title, bibtex_authors, self.journal, 
                    self.volume, bibtex_page, self.pub_year)

  def get_volume_page(self):
    rv = ''
    if( self.volume ): rv += ", %s" % self.volume
    if( self.page ): rv += ":%s" % self.page
    return rv

  def get_nickname_base(self):
    first_author = self.authors.split(',')[0]
    first_author_surname  = re.sub(r'[A-Z\-]+$','',first_author)
    first_author_surname  = re.sub(r'\s+','',first_author_surname)
    return "%s%d" % (first_author_surname, self.pub_year)

  def set_nickname(self):
    cur = self.get_dbi().conn.cursor()
    sql = "SELECT count(id) FROM pubitems WHERE nickname LIKE '%s'"
    nickname_base = self.get_nickname_base() + '%'
    cur.execute(sql % nickname_base)
    self.nickname = "%s.%d" % (self.get_nickname_base(), cur.fetchone()[0]+1)

  def delete(self):
    try:
      cursor = self.get_dbi().conn.cursor()
      sql = "DELETE FROM pubitems WHERE id=?"
      cursor.execute(sql,(str(self.id),))
      
      l = Link()
      l.delete_with_cursor_and_pubitem(cursor, self)
        
      c = Comment()
      c.delete_with_cursor_and_pubitem(cursor, self)

      t = Tag()
      t.delete_with_cursor_and_pubitem(cursor, self)
      t.clean_with_cursor(cursor)

      self.get_dbi().conn.commit()
    except:
      print "Error in delete PubItem"
      raise

  def update(self):
    try:
      cursor = self.get_dbi().conn.cursor()
      cursor.execute("UPDATE pubitems SET pub_type=?, title=?, authors=?,\
                      journal=?,publisher=?,volume=?,page=?,pub_year=?\
                      WHERE id=?", 
                      (self.pub_type, self.title, self.authors, self.journal, 
                       self. publisher, self.volume, self.page, self.pub_year,
                       str(self.id)))
      
      l = Link()
      l.delete_with_cursor_and_pubitem(cursor, self)
      if( len(self.links) ):
        for link in self.links:
          link.pubitem_id = self.id
          link.insert_with_cursor_and_pubitem(cursor, self)
        
      #c = Comment()
      #c.delete_with_cursor_and_pubitem(cursor, self)
      #if( len(self.comments) ):
      #  for comment in self.comments:
      #    comment.pubitem_id = self.id
      #    comment.insert_with_cursor(cursor)
      self.set_comments()
      
      t = Tag()
      t.delete_with_cursor_and_pubitem(cursor, self)
      if( len(self.tags) ):
        for tag in self.tags:
          tag.insert_with_cursor_and_pubitem(cursor, self)
      t.clean_with_cursor(cursor)

      self.get_dbi().conn.commit()

    except:
      print "Error in update PubItem"
      raise

  def insert(self):
    if( self.nickname == '' ): self.set_nickname()
    try:
      cur = self.get_dbi().conn.cursor()
      cur.execute("INSERT INTO pubitems\
              (nickname, pub_type, title, authors, journal, publisher,\
              volume, page, pub_year) VALUES (?,?,?,?,?,?,?,?,?)",
              (self.nickname, self.pub_type, self.title,
              self.authors, self.journal, self.publisher,
              self.volume, self.page, self.pub_year))
      self.id = cur.lastrowid

      for link in self.links:
        link.pubitem_id = self.id
        link.insert_with_cursor_and_pubitem(cur, self)

      for comment in self.comments:
        comment.pubitem_id = self.id
        comment.insert_with_cursor(cur)
      
      for tag in self.tags:
        tag.insert_with_cursor_and_pubitem(cur, self)

      self.get_dbi().conn.commit()
    except:
      print "Error in insert PubItem"
      raise

  def set_links(self):
    cur = self.get_dbi().conn.cursor()
    l = Link()
    self.links = l.find_by_pubitem(self)

  def set_tags(self):
    cur = self.get_dbi().conn.cursor()
    t = Tag()
    self.tags = t.find_by_pubitem(self)

  def set_comments(self):
    cur = self.get_dbi().conn.cursor()
    c = Comment()
    self.comments = c.find_by_pubitem(self)

  def find(self):
    sql = "SELECT id,nickname,pub_type,title,authors,journal,publisher,\
            volume,page,pub_year,created_at FROM pubitems WHERE id=?"
    cursor = self.get_dbi().conn.cursor()
    for row in cur.execute(sql, (str(self.id),)):
      self.id = row[0]
      self.nickname = row[1]
      self.pub_type = row[2]
      self.title = row[3]
      self.authors = row[4]
      self.journal = row[5]
      self.pulisher = row[6]
      self.volume = row[7]
      self.page = row[8]
      self.pub_year = row[9]
      self.created_at = row[10]
      self.set_links()
      self.set_tags()
      self.set_comments()
    return self
      
  def find_all(self):
    rv = []
    sql = "SELECT id,nickname,pub_type,title,authors,journal,publisher,\
            volume,page,pub_year,created_at FROM pubitems"
    cur = self.get_dbi().conn.cursor()
    for row in cur.execute(sql):
      pubitem = PubItem(id=row[0], nickname=row[1], pub_type=row[2], \
                  title=row[3], authors=row[4], journal=row[5], \
                  publisher=row[6], volume=row[7], page=row[8], \
                  pub_year=row[9], created_at=row[10])
      #pubitem.set_links()
      pubitem.set_tags()
      #pubitem.set_comments()
      rv.append(pubitem)
    return rv


  def find_by_tag_category_and_name(self, tag_category, tag_name):
    rv = []
    sql = "SELECT DISTINCT p.id, p.nickname, p.pub_type, p.title, p.authors, \
            p.journal, p.publisher, p.volume, p.page, p.pub_year, p.created_at\
            FROM pubitems AS p, tags_pubitems AS tp, tags AS t \
            WHERE p.id=tp.pubitem_id AND tp.tag_id=t.id \
              AND t.category=? AND t.name=? ORDER BY p.pub_year DESC" 

    cur = self.get_dbi().conn.cursor()
    for row in cur.execute(sql, (tag_category, tag_name)):
      pubitem = PubItem(id=row[0], nickname=row[1], pub_type=row[2], \
                  title=row[3], authors=row[4], journal=row[5], \
                  publisher=row[6], volume=row[7], page=row[8], \
                  pub_year=row[9], created_at=row[10])
      pubitem.set_links()
      pubitem.set_tags()
      pubitem.set_comments()
      rv.append(pubitem)
    return rv

  def find_by_nickname(self, nickname):
    sql = "SELECT DISTINCT p.id, p.nickname, p.pub_type, p.title, p.authors,\
            p.journal, p.publisher, p.volume, p.page, p.pub_year, p.created_at\
            FROM pubitems AS p WHERE p.nickname='%s'" % nickname

    cur = self.get_dbi().conn.cursor()
    for row in cur.execute(sql):
      pubitem = PubItem(id=row[0], nickname=row[1], pub_type=row[2], \
                  title=row[3], authors=row[4], journal=row[5], \
                  publisher=row[6], volume=row[7], page=row[8], \
                  pub_year=row[9], created_at=row[10])
      pubitem.set_links()
      pubitem.set_tags()
      pubitem.set_comments()
      return pubitem

  def find_by_tag_category(self, tag_category):
    rv = []
    sql = "SELECT DISTINCT p.id, p.nickname, p.pub_type, p.title, p.authors,\
            p.journal, p.publisher, p.volume, p.page, p.pub_year, p.created_at\
            FROM pubitems AS p, tags_pubitems AS tp, tags AS t\
            WHERE p.id=tp.pubitem_id AND tp.tag_id=t.id\
              AND t.category='%s' ORDER BY p.pub_year DESC" % tag_category

    cur = self.get_dbi().conn.cursor()
    for row in cur.execute(sql):
      pubitem = PubItem(id=row[0], nickname=row[1], pub_type=row[2],
                  title=row[3], authors=row[4], journal=row[5],
                  publisher=row[6], volume=row[7], page=row[8],
                  pub_year=row[9], created_at=row[10])
      pubitem.set_links()
      pubitem.set_tags()
      pubitem.set_comments()
      rv.append(pubitem)

    return rv
