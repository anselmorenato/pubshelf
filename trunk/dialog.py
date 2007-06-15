#!/usr/bin/env python
import wx
import yaml
from dialog_pubitem import PubShelfPubItemDialog
from dialog_search import PubShelfSearchDialog

conf = yaml.load( file('../etc/pubshelf.yaml','r') )
app = wx.App(0)

dia = PubShelfSearchDialog(None, -1, conf)
#dia = PubShelfPubItemDialog(None, -1, conf)
dia.ShowModal()
dia.Destroy()

app.MainLoop()
