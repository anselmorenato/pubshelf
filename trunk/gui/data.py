class PubItem:
  def __init__(self, id=0, nickname='', title='', authors='', journal=''\
               , publisher='', volume='', page='', pub_year='', pub_type=''\
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
    rv = "%s, %d, %s, %s" \
          % (self.authors, self.pub_year, self.title, self.journal)
    if( self.volume ):
      rv += ", %s" % self.volume
    
    if( self.page ):
      rv += ", %s" % self.page

    return rv
  
class Link:
  def __init__(self, id=0, pubitem_id=0, name='', uri='', uri_type=''\
                , created_at=''):
    self.id = id
    self.pubitem_id = pubitem_id
    self.name = name
    self.uri = uri
    self.uri_type = uri_type
    self.created_at = created_at

class Comment:
  def __init__(self, id=0, pubitem_id=0, title='', textbody='', created_at=''):
    self.id = id
    self.pubitem_id = pubitem_id
    self.title = title
    self.textbody = textbody
    self.created_at = created_at

class Tag:
  def __init__(self, id=0, category='', name='', created_at=''):
    self.id = id
    self.category = category
    self.name = name
    self.created_at = created_at
    self.articles = []
