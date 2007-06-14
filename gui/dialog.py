#!/usr/bin/env python
import wx
import yaml
from dialog_pubitem import PubShelfPubItemDialog

conf = yaml.load( file('../etc/pubshelf.yaml','r') )
app = wx.App(0)

dia = PubShelfPubItemDialog(None, -1, conf)
dia.ShowModal()
dia.Destroy()

app.MainLoop()
