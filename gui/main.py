#!/usr/bin/env python2.5

import wx, yaml
from frame import PubShelfFrame
import sys
sys.path.append('../libpy/')
from dbi import PubShelfDBI

class PubShelfGUI(wx.App):
  def OnInit(self):
    conf = yaml.load( file('../etc/pubshelf.yaml','r') )
    dbi = PubShelfDBI(conf)
    frame = PubShelfFrame(None, -1, 'PubShelf', dbi, conf)
    frame.Show(True)
    self.SetTopWindow(frame)
    return True

app = PubShelfGUI(0)
app.MainLoop()
