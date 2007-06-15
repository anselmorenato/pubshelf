#!/usr/bin/python
import yaml
import sys
sys.path.append('../libpy/')
from model_pubitem import PubItem

data1 = yaml.load( file('./pubitem_example1.yaml','r') )
pm1 = PubItem(title=data1['title'], authors=data1['authors'],
              journal=data1['journal'], volume=data1['volume'],
              page=data1['page'], pub_year=data1['pub_year'],
              pub_type=data1['pub_type'])

pm1.insert()
print pm1.nickname
#pm = PubItem(authors='Harris HS,Kim SK', pub_year=2004, page='2-4')
#print pm.get_nickname_base()
