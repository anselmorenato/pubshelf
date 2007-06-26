import wx
import sys, os
from conf import PubShelfConf
from model_tag import Tag
from model_pubitem import PubItem

ID_EXPORT_BUTTON = 5000
ID_CLOSE_BUTTON = 5001
ID_FILENAME_FORM = 5002

DIALOG_SIZE = (400,150)
class PubShelfExportDialog(wx.Dialog):
  def __init__(self, parent, id):
    wx.Dialog.__init__(self, parent, id, 'PubItem', size=DIALOG_SIZE)
    self.forms = dict()
    psconf = PubShelfConf()

    tag_list = []
    t = Tag()
    for tag in t.find_all():
      tag_list.append( tag.category+'/'+tag.name )

    panel = wx.Panel(self, -1)
    mainSizer = wx.BoxSizer(wx.VERTICAL)

    ## Form
    tagLabel = wx.StaticText(panel,-1,'Tag to export', style=wx.ALIGN_CENTER)
    self.forms['tag_list'] = wx.ComboBox(panel, -1, choices=tag_list,
                                        style=wx.CB_READONLY)
    fileLabel = wx.StaticText(panel, -1, 'Export file', style=wx.ALIGN_CENTER)
    default_file = psconf.item['dir_file']+'pubshelf_export.txt'
    self.forms['file_export'] = wx.TextCtrl(panel, ID_FILENAME_FORM, 
                                  default_file, 
                                  style=wx.TE_LEFT|wx.TE_PROCESS_ENTER)

    formSizer = wx.FlexGridSizer(cols=2, hgap=10)
    formSizer.AddGrowableCol(1)
    formSizer.Add(tagLabel, 0, wx.ALIGN_CENTER)
    formSizer.Add(self.forms['tag_list'], 0, wx.EXPAND)
    formSizer.Add(fileLabel, 0, wx.ALIGN_CENTER)
    formSizer.Add(self.forms['file_export'], 0, wx.EXPAND)
    mainSizer.Add(formSizer, 0, wx.EXPAND|wx.ALL, 10)
    
    ## Buttons
    exportButton = wx.Button(panel, ID_EXPORT_BUTTON, 'Export')
    closeButton = wx.Button(panel, ID_CLOSE_BUTTON, 'Close')
    self.Bind(wx.EVT_BUTTON, self.OnExport, id=ID_EXPORT_BUTTON)
    self.Bind(wx.EVT_BUTTON, self.OnClose, id=ID_CLOSE_BUTTON)
    
    buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
    buttonSizer.Add( (10,10), wx.EXPAND|wx.ALL, 10 )
    buttonSizer.Add( exportButton, wx.EXPAND|wx.ALL, 10 )
    buttonSizer.Add( closeButton, wx.EXPAND|wx.ALL, 10 )
    buttonSizer.Add( (10,10), wx.EXPAND|wx.ALL, 10 )
    mainSizer.Add(buttonSizer,0, wx.EXPAND|wx.ALL, 10)

    panel.SetSizer(mainSizer)
    self.Centre()
  
  def OnClose(self, event):
    self.Close()

  def OnExport(self, event):
    (tag_category, tag_name) = self.forms['tag_list'].GetValue().split('/')
    filename_export = self.forms['file_export'].GetValue()
    file_export = open(filename_export,'w')
    pi = PubItem()
    for pubitem in pi.find_by_tag_category_and_name(tag_category, tag_name):
      citation = pubitem.get_export_citation()
      file_export.write(citation)
    file_export.close()
    self.Close()
    #file_export = open(filename_export, 'w')
    pass
