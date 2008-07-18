#!/usr/bin/python 
import sys
sys.path.append('../libpy/')
from conf import PubShelfConf
from model_link import Link

conf = PubShelfConf()
dir_db = conf.item['dir_db']

l = Link()
for link in l.find_all():
  if( link.uri.find(dir_db) == 0 ):
    old_uri = link.uri
    new_uri = old_uri.replace(dir_db,'')
    link.uri = new_uri
    link.update_uri()
    print "Update URI : %s -> %s" % (old_uri, new_uri)
