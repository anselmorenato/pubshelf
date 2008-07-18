#!/usr/bin/python
import yaml
import sys
sys.path.append('../libpy/')
from model_tag import Tag

t = Tag()
for tag in t.find_all():
  print tag.name, tag.category
