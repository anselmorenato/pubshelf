#!/usr/bin/env python2.5

import wx, yaml
import sys
sys.path.append('libpy')
sys.path.append('gui')
from main_frame import PubShelfFrame

class PubShelfGUI(wx.App):
  def OnInit(self):
    frame = PubShelfFrame(None, -1, 'PubShelf')
    frame.Show(True)
    self.SetTopWindow(frame)
    return True

app = PubShelfGUI(0)
app.MainLoop()
