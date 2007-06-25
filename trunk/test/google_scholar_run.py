#!/usr/bin/python 
import sys
sys.path.append('../libpy/')
from google import *

term = 'synmuv'
retmax = '50'

articles = google_scholar_search(term=term, retmax=retmax)
#for article in articles:
  #print (article.get_citation()).encode("latin1")
  #print (article.authors).encode("latin1")
