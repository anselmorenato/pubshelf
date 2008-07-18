#!/usr/bin/python
import yaml
import sys
sys.path.append('../libpy/')
from model_link import Link
from model_pubitem import PubItem

p = PubItem(id=1)
l = Link()

for link in l.find_by_pubitem(p):
  print link.uri
