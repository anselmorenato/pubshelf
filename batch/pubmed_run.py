#!/usr/bin/python 
import sys
sys.path.append('../libpy/')
from pubmed import *

term = 'elegans AND 2006[dp]';
retmax = '50';

pm = do_search(term, retmax);
for article in pm.articles:
  print article.authors,article.title;
