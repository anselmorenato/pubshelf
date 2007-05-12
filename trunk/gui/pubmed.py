#!/usr/bin/python 
from lib.pubmed import *;

term = 'elegans AND 2006[dp]';
retmax = '50';

pm = pubmed_search(term, retmax);
for article in pm.articles:
  print article.authors,article.title;
