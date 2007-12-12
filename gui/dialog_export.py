import wx
import sys, os
from libpy.conf import PubShelfConf
from libpy.model_tag import Tag
from libpy.model_pubitem import PubItem

ID_EXPORT_BUTTON = 5000
ID_CLOSE_BUTTON = 5001
ID_FILENAME_FORM = 5002
ID_BIBTEXSTYLE_BUTTON = 5003
ID_WIKISTYLE_BUTTON = 5004

DIALOG_SIZE = (400,180)
class PubShelfExportDialog(wx.Frame):
  def __init__(self, parent, id):
    wx.Frame.__init__(self, parent, id, 'PubItem', size=DIALOG_SIZE)
    self.forms = dict()
    psconf = PubShelfConf()

    # Get the Tree selection
    (sel_category, sel_tag) = self.GetParent().tree.GetSelTag()
    if (sel_category == 'No Category'): sel_category = ''
    
    tag_list = []
    t = Tag()
    categories = dict()
    for tag in t.find_all():
      if(not categories.has_key(tag.category)):
        categories[tag.category] = 1
        tag_list.append( tag.category+'/' )
      tag_list.append( tag.category+'/'+tag.name )

    panel = wx.Panel(self, -1)
    mainSizer = wx.BoxSizer(wx.VERTICAL)

    ## Form
    tagLabel = wx.StaticText(panel,-1,'Tag to export', style=wx.ALIGN_CENTER)
    self.forms['tag_list'] = wx.ComboBox(panel, -1, value= sel_category + '/' + sel_tag, choices=tag_list,
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

    ## Style Buttons
    styleLabel = wx.StaticText(panel, -1, 'Style', style=wx.ALIGN_CENTER)
    self.bibtexstyleButton = wx.RadioButton(panel, ID_BIBTEXSTYLE_BUTTON, 'Bibtex', style = wx.RB_GROUP )
    self.wikistyleButton = wx.RadioButton(panel, ID_WIKISTYLE_BUTTON, 'Wiki')
    self.bibtexstyleButton.SetValue( True )
    
    styleSizer = wx.BoxSizer(wx.HORIZONTAL)
    styleSizer.Add( styleLabel, 0, wx.ALIGN_CENTER )
    styleSizer.Add( (10,10), wx.EXPAND|wx.ALL, 10 )
    styleSizer.Add( self.bibtexstyleButton, wx.EXPAND|wx.ALL, 10 )
    styleSizer.Add( self.wikistyleButton, wx.EXPAND|wx.ALL, 10 )
    styleSizer.Add( (10,10), wx.EXPAND|wx.ALL, 10 )
    mainSizer.Add(styleSizer, 0, wx.EXPAND|wx.ALL, 10)
    
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
    if (tag_name == ''): tag_name = '%' # wildcard SQL
    
    filename_export = self.forms['file_export'].GetValue()
    file_export = open(filename_export,'w')
    pi = PubItem()
    
    if (self.wikistyleButton.GetValue() == True ):
      ## wiki header
      file_export.write('= ' + tag_category + '/' + tag_name + ' =\n')
    
    for pubitem in pi.find_by_tag_category_and_name(tag_category, tag_name):
      if (self.wikistyleButton.GetValue() == True ):
        ## wiki style export
        wikidata = pubitem.get_export_wiki()
        file_export.write(wikidata.encode('utf-8'))
      else:
        ## bibtex style export
        citation = pubitem.get_export_citation()
        file_export.write(citation.encode('utf-8'))
    file_export.close()
    self.Close()
