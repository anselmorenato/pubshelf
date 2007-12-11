import cookielib, urllib2, re
from string import atoi
from libpy.model_pubitem import PubItem

def parse_bibtex(raw):
  p = PubItem()
  if( re.search('title={{(.+)}}',raw) ):
    p.title = re.search('title={{(.+)}}', raw).group(1)
  if( re.search('author={(.+)}',raw) ):
    p.authors = re.search('author={(.+)}',raw).group(1)
    p.authors = p.authors.replace('.','')
    p.authors = p.authors.replace(' and ','; ')
  if( re.search('journal={(.+)}',raw) ):
    p.journal = re.search('journal={(.+)}',raw).group(1)
  if( re.search('volume={(.+)}',raw) ):
    p.volume = re.search('volume={(.+)}',raw).group(1) 
  if( re.search('pages={(.+)}',raw) ):
    p.page = re.search('pages={(.+)}',raw).group(1)
    p.page = p.page.replace('--','-')
  if( re.search('year={(.+)}',raw) ):
    p.pub_year = atoi(re.search('year={(.+)}',raw).group(1))

  return p
  
def google_search(term='', retmax=50):
  url_google_scholar = 'http://scholar.google.com/'
  term = re.compile('\s+').sub('+', term)
  term = re.compile('\&').sub('', term)
  cj = cookielib.CookieJar()
  opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
  opener.addheaders = [('User-agent', 'PubShelf')]
  url_search = url_google_scholar+'scholar?num='+retmax
  url_search += '&q='+term
  r_search = opener.open(url_search)

  rv = []
  for cookie in cj:  
    if( cookie.name == 'GSP' ): 
      gsp_cookie = cookie
      gsp_cookie.value = cookie.value + ':CF=4'
      cj.set_cookie(gsp_cookie)
  
  re_gs_id = 'related:([A-z0-9]+):scholar.google.com'

  for gs_id in re.compile(re_gs_id).findall(r_search.read()):
    gs_id = 'info:'+gs_id+':scholar.google.com'
    url_fetch = url_google_scholar+'scholar.bib?q='+gs_id+'&output=citation'
    r_fetch = opener.open(url_fetch)
    rv.append( parse_bibtex(r_fetch.read()) )

  return rv
