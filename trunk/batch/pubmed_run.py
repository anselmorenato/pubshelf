#!/usr/bin/python 
import sys
sys.path.append('../libpy/')
from pubmed import *

term = 'elegans AND 2006[dp]';
retmax = '50';

articles = pubmed_search(term, retmax);
for article in articles:
  print article.get_citation()
  #print article.authors,article.title;
