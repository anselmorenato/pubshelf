#!/usr/bin/python 
import sys
sys.path.append('../libpy/')
from pubmed import *

term = 'ahringer AND 2007[dp]'
retmax = '50'

articles = pubmed_search(term, retmax)
for article in articles:
  print (article.get_citation()).encode("latin1")
  #print (article.authors).encode("latin1")
