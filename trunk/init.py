#!/usr/bin/env python2.5
import os
import shutil

pubshelf_dir = os.getcwd()
config_filename = 'config/pubshelf.yaml'

current_db_dir = os.getcwd()+'/db'
current_db_name = 'pubshelf.db'
current_author_name = os.getenv('LOGNAME')
current_os_type = os.uname()[0]

app_pdf = dict()
app_pdf['Linux'] = '/usr/bin/acroread'
app_pdf['Darwin'] = 'open -a Preview'
app_pdf['Win'] = 'start'

app_html = dict()
app_html['Linux'] = '/usr/bin/firefox'
app_html['Darwin'] = 'open -a Firefix'
app_html['Win'] = 'explorer'

is_confirmed = 'unknown'

while( is_confirmed != 'yes' ):
  is_confirmed = 'unknown'

  ## DB directory
  pubshelf_db_dir = raw_input("PubShelf DB directory ["+current_db_dir+"] :")
  if( pubshelf_db_dir == '' ):
    pubshelf_db_dir = current_db_dir
  else:
    current_db_dir = pubshelf_db_dir

  ## DB name
  pubshelf_db_name = raw_input("DB name ["+current_db_name+"] :")
  if( pubshelf_db_name == '' ):
    pubshelf_db_name = current_db_name
  else:
    current_db_name = pubshelf_db_name

  ## Author Name
  pubshelf_author_name = raw_input("Author name ["+current_author_name+"] :")
  if( pubshelf_author_name == '' ):
    pubshelf_author_name = current_author_name
  else:
    current_author_name = pubshelf_author_name

  ## OS Type
  pubshelf_os_type = raw_input("OS type ["+current_os_type+"] :")
  if( pubshelf_os_type == '' ):
    pubshelf_os_type = current_os_type
  else:
    current_os_type = pubshelf_os_type
  
  print "PubShelf directory = " + pubshelf_dir
  print "PubShelf DB directory = " +pubshelf_db_dir
  print "PubShelf DB name = "+pubshelf_db_name
  print "Author name = "+pubshelf_author_name
  print "OS type = "+pubshelf_os_type

  while( is_confirmed != 'yes' and is_confirmed != 'no'):
    is_confirmed = raw_input("Are they correct? (yes/no) :")

## Execution
os.mkdir(current_db_dir,0755)
shutil.copy(pubshelf_dir+'/config/dummy.db', current_db_dir+'/'+current_db_name)

conf = open(config_filename,'w')
conf.write('dir_file: '+pubshelf_dir+"\n")
conf.write('dir_home: '+pubshelf_dir+"\n")
conf.write('dir_db: '+pubshelf_db_dir+"\n")
conf.write('db_name: '+pubshelf_db_name+"\n")
conf.write('author_name: '+pubshelf_author_name+"\n")
if( app_pdf.has_key(pubshelf_os_type) ):
  conf.write("pdf_app: "+app_pdf[pubshelf_os_type]+"\n")
  conf.write("html_app: "+app_html[pubshelf_os_type]+"\n")
else:
  conf.write("pdf_app: path for your pdf viewer\n")
  conf.write("html_app: path for your html viewer\n")

conf.close()
