#!/usr/bin/env python2.5
import os

pubshelf_dir = os.getcwd()
current_db_dir = os.getcwd()+'/db'
current_db_name = 'pubshelf.db'
current_author_name = os.getenv('LOGNAME')
current_os_type = os.uname()[0]
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
