#!/usr/bin/python
import sys
sys.path.append('../libpy/')
from model_pubitem import PubItem

pm = PubItem(authors='Harris HS,Kim SK', pub_year=2004, page='2-4')
print pm.get_nickname_base()
