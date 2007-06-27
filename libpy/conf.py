import os
import yaml

class PubShelfConf:
  def __init__(self):
    file_path1 = os.path.join('..','config','pubshelf.yaml')
    file_path2 = os.path.join('.','config','pubshelf.yaml')
    file_path = ''
    if( os.access(file_path1, os.F_OK) ): file_path = file_path1
    elif( os.access(file_path2, os.F_OK) ): file_path = file_path2

    try:
      self.item = yaml.load( file(file_path,'r') )
    except:
      print "Error to open yaml files under config"
