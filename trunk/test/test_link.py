#!/usr/bin/python
import yaml
import sys
sys.path.append('../libpy/')
from model_link import Link

l = Link()
for link in l.find_all():
  print link.name, link.uri
