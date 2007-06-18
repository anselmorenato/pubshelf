import cookielib, urllib2, re;
from model_pubitem import PubItem

def parse_bibtex(raw):
  title = re.search('title={{.+}}', raw).group()
  #title.replace('title={{','')
  #title.replace('}}$','')
  print title

  rv = PubItem()
  return rv
  
  
def google_scholar_search(term='', retmax=50):
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
  
  print r_search.read()
  re_gs_id = 'related:([A-z0-9]+):scholar.google.com'

  for gs_id in re.compile(re_gs_id).findall(r_search.read()):
    gs_id = 'info:'+gs_id+':scholar.google.com'
    url_fetch = url_google_scholar+'scholar.bib?q='+gs_id+'&output=citation'
    r_fetch = opener.open(url_fetch)
    rv.append( parse_bibtex(r_fetch.read()) )

  return rv
