#!/usr/bin/env python2.5

import wx, yaml
import sys
sys.path.append('./libpy/')
from dbi import PubShelfDBI
from conf import PubShelfConf
sys.path.append('./gui/')
from frame import PubShelfFrame

class PubShelfGUI(wx.App):
  def OnInit(self):
    conf = PubShelfConf('./conf/pubshelf.yaml')
    dbi = PubShelfDBI(conf)
    frame = PubShelfFrame(None, -1, 'PubShelf', dbi, conf)
    frame.Show(True)
    self.SetTopWindow(frame)
    return True

app = PubShelfGUI(0)
app.MainLoop()
