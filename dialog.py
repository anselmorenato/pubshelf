#!/usr/bin/env python
import wx
import yaml
import sys
sys.path.append('./gui/')
sys.path.append('./libpy/')
from dialog_pubitem import PubShelfPubItemDialog
from dialog_search import PubShelfSearchDialog

conf = yaml.load( file('./conf/pubshelf.yaml','r') )
app = wx.App(0)

#dia = PubShelfSearchDialog(None, -1)
dia = PubShelfPubItemDialog(None, -1)
dia.ShowModal()
dia.Destroy()

app.MainLoop()
