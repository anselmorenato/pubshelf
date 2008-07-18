#!/usr/bin/env python
import wx
import yaml
import sys
sys.path.append('libwx')
sys.path.append('libpy')

from dialog_pubitem import PubShelfPubItemDialog
from dialog_search import PubShelfSearchDialog
from dialog_export import PubShelfExportDialog
from dialog_comment import PubShelfCommentDialog

app = wx.App(0)

#dia = PubShelfExportDialog(None, -1)
#dia = PubShelfSearchDialog(None, -1)
#dia = PubShelfPubItemDialog(None, -1)
dia = PubShelfCommentDialog(None,-1)
dia.Show()

app.MainLoop()
