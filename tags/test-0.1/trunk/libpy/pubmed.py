#!/usr/bin/python 
import urllib, re, xml.sax
from string import atoi
from libpy.model_pubitem import PubItem
from libpy.model_link import Link

class PubmedSearchHandler(xml.sax.ContentHandler):
  element_array = []
  count = ''
  query_key = ''
  web_env = ''

  def startElement(self, name, attrs):
    self.element_array.append(name)

  def endElement(self, name):
    self.element_array.pop()

  def characters(self, content):
    if(self.element_array[0] == 'eSearchResult'):
      if( len(self.element_array) > 1) :
        if(self.element_array[1] == 'Count'):
          self.count = content
        elif self.element_array[1] == 'QueryKey' :
          self.query_key = content
        elif self.element_array[1] == 'WebEnv' :
          self.web_env = content

class Author:
  last_name = ''
  first_name = ''
  initial_name = ''

class PubmedFetchHandler(xml.sax.ContentHandler):
  element_array = []
  articles = []
  #author = Author()
  
  pubmed_article_tag = ['PubmedArticleSet','PubmedArticle']
  medline_citation_tag = pubmed_article_tag+['MedlineCitation']
  pubmed_id_tag = medline_citation_tag+['PMID']
  journal_title_tag = medline_citation_tag\
                      + ['MedlineJournalInfo','MedlineTA']
  article_tag = medline_citation_tag+['Article']
  article_title_tag = article_tag+['ArticleTitle']
  journal_issue_tag = article_tag+['Journal','JournalIssue']
  volume_tag = journal_issue_tag + ['Volume']
  issue_tag = journal_issue_tag + ['Issue']
  page_tag = article_tag + ['Pagination','MedlinePgn']
  pub_year_tag = journal_issue_tag + ['PubDate','Year']
  abstract_tag = article_tag + ['Abstract']
  author_tag = article_tag + ['AuthorList','Author']
  author_last_name_tag = author_tag + ['LastName']
  author_first_name_tag = author_tag + ['FirstName']
  author_fore_name_tag = author_tag + ['ForeName']
  author_initial_name_tag = author_tag + ['Initials']

  def __init__(self):
    self.articles = []

  def startElement(self, name, attrs):
    self.element_array.append(name)
    if(self.element_array == self.pubmed_article_tag):
      self.article = PubItem()
      self.authors = []
    elif(self.element_array == self.author_tag):
      self.author = Author()

  def endElement(self, name):
    if( self.element_array == self.pubmed_article_tag ):
      self.article.authors = '; '.join(self.authors)
      self.articles.append(self.article)
    elif( self.element_array == self.author_tag and self.author.last_name ):
      if( self.author.initial_name ):
        self.authors.append(self.author.last_name+','+self.author.initial_name)
      elif( self.author.first_name ):
        initial_name = re.compile('[a-z ]').sub('',self.author.first_name)
        self.authors.append(self.author.last_name+','+initial_name)
      else:
        self.authors.append(self.author.last_name)
    
    self.element_array.pop()

  def characters(self, content):
    pubmed_link_uri = 'http://www.ncbi.nlm.nih.gov/sites/entrez?Db=pubmed&Cmd=ShowDetailView&TermToSearch=%s'
    if( self.element_array == self.pubmed_id_tag ):
      pubmed_uri = pubmed_link_uri % content
      self.article.links.append( Link(name='PubMed', uri=pubmed_uri) )
    elif( self.element_array == self.journal_title_tag ):
      self.article.journal = content
    elif( self.element_array == self.article_title_tag ):
      self.article.title = content
    elif( self.element_array == self.volume_tag ):
      self.article.volume = content
    elif( self.element_array == self.issue_tag ):
      self.article.volume += '('+content+')'
    elif( self.element_array == self.page_tag ):
      self.article.page = content
    elif( self.element_array == self.pub_year_tag ):
      self.article.pub_year = atoi(content)
    elif( self.element_array == self.author_last_name_tag ):
      self.author.last_name = content
    elif( self.element_array == self.author_first_name_tag ):
      self.author.first_name = content
    elif( self.element_array == self.author_fore_name_tag ):
      self.author.first_name = content
    elif( self.element_array == self.author_initial_name_tag ):
      self.author.initial_name = content

def pubmed_search(term='', retmax=50):
  url_eutil = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils'
  url_search = url_eutil+'/esearch.fcgi?db=pubmed&usehistory=y'
  url_search += '&retmax='+retmax
  term = term.replace(' ','+')
  url_search += '&term='+term

  response = urllib.urlopen(url_search).read()
  search_parser = PubmedSearchHandler()
  xml.sax.parseString(response, search_parser)

  url_fetch = url_eutil+'/efetch.fcgi?db=pubmed&retmode=xml'
  url_fetch += '&retmax='+retmax
  url_fetch += '&query_key='+search_parser.query_key
  url_fetch += '&WebEnv='+search_parser.web_env

  response = urllib.urlopen(url_fetch).read()
  fetch_parser = PubmedFetchHandler()
  xml.sax.parseString(response, fetch_parser)

  return fetch_parser.articles
