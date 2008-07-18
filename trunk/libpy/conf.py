import os
import sys

class PubShelfConf:
  def __init__(self):
    self.item = dict()
    file_path1 = os.path.join('..','config','pubshelf.yaml')
    file_path2 = os.path.join('.','config','pubshelf.yaml')
    file_path = ''

    if( os.access(file_path1, os.F_OK) ): file_path = file_path1
    elif( os.access(file_path2, os.F_OK) ): file_path = file_path2

    try:
      st = open(file_path, 'r')
      for line in st:
        line = line.rstrip()
        (key, value) = line.split(":")
        key = key.lstrip().rstrip()
        value = value.lstrip().rstrip()
        self.item[key] = value
    except:
      print "Error to open config file : "+file_path
      sys.exit()
