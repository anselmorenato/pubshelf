#!/usr/bin/env python2.5
import cookielib, urllib2, re;

url_gs = 'http://scholar.google.com/';
term = 'alternative splicing evolution';
retmax = '50';

term = re.compile('\s+').sub('+', term);
term = re.compile('\&').sub('', term);
cj = cookielib.CookieJar();
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj));
opener.addheaders = [('User-agent', 'Bawi')];
url_search = url_gs+'scholar?num='+retmax;
url_search += '&q='+term;r_search = opener.open(url_search);

for cookie in cj:  if( cookie.name == 'GSP' ):    
  gsp_cookie = cookie;    
  gsp_cookie.value = cookie.value + ':CF=4';      
  cj.set_cookie(gsp_cookie);re_gs_id = 'related:([A-z0-9]+):scholar.google.com';

for gs_id in re.compile(re_gs_id).findall(r_search.read()):
  gs_id = 'info:'+gs_id+':scholar.google.com';
  url_fetch = url_gs+'scholar.bib?q='+gs_id+'&output=citation';
  r_fetch = opener.open(url_fetch);
  print r_fetch.read();
