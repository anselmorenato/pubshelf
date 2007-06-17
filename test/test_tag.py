#!/usr/bin/python
import yaml
import sys
sys.path.append('../libpy/')
from model_tag import Tag

t = Tag()
for tag in t.get_tags():
  print tag.name, tag.category
#pm = PubItem(authors='Harris HS,Kim SK', pub_year=2004, page='2-4')
#print pm.get_nickname_base()
