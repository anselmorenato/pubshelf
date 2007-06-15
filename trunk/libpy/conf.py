import os
import yaml

class PubShelfConf:
  def __init__(self):
    file_path1 = '../conf/pubshelf.yaml'
    file_path2 = './conf/pubshelf.yaml'
    file_path = ''
    if( os.access(file_path1, os.F_OK) ): file_path = file_path1
    elif( os.access(file_path2, os.F_OK) ): file_path = file_path2

    try:
      self.item = yaml.load( file(file_path,'r') )
    except:
      print "Error to open config file pubshelf.yaml"
