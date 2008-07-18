#!/usr/bin/python 
import sys
sys.path.append('../libpy/')
from google import *

term = 'Miska elegans'
retmax = '5'

articles = google_search(term=term, retmax=retmax)
for article in articles:
  print (article.get_citation()).encode("latin1")
