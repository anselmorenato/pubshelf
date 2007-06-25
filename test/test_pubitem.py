#!/usr/bin/python
import yaml
import sys
sys.path.append('../libpy/')
from model_pubitem import PubItem
from model_tag import Tag
from model_link import Link
from model_comment import Comment

data1 = yaml.load( file('./pubitem_example1.yaml','r') )
pm1 = PubItem(title=data1['title'], authors=data1['authors'],
              journal=data1['journal'], volume=data1['volume'],
              page=data1['page'], pub_year=data1['pub_year'],
              pub_type=data1['pub_type'])

for tag_raw in data1['tags']:
  (tag_category, tag_name) = tag_raw.split('/')
  pm1.tags.append( Tag(category=tag_category, name=tag_name) )

for link_raw in data1['links']:
  (link_name, link_uri) = link_raw.split('/')
  pm1.links.append( Link(name=link_name, uri=link_uri) )

for comment_raw in data1['comments']:
  pm1.comments.append( Comment(title=comment_raw['title'], 
                               textbody=comment_raw['textbody']) )

pm1.insert()
print pm1.nickname
#pm = PubItem(authors='Harris HS,Kim SK', pub_year=2004, page='2-4')
#print pm.get_nickname_base()
