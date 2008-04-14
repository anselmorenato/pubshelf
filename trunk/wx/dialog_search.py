import wx
from string import atoi
import sys
#sys.path.append('../libpy/')
from libpy.pubmed import *
from libpy.google import *
from dialog_pubitem import PubShelfPubItemDialog

ID_SEARCH_BUTTON = 3000
ID_CLOSE_BUTTON = 3001
ID_SEARCH_FORM  = 3002

DIALOG_SIZE = (600,600)
authorWidth = 100
titleWidth = 410
yearWidth = 50
logSize = (580,-1)
resultsListSize = (580,430)

AVAILABLE_SITES = ['pubmed','google scholar']
PUBMED_RETMAX = '50'

class PubShelfSearchDialog(wx.Frame):
  def __init__(self, parent, id):
    wx.Frame.__init__(self, parent, id, 'Search', size=DIALOG_SIZE)
    self.parent = parent

    panel = wx.Panel(self, -1)
    mainSizer = wx.BoxSizer(wx.VERTICAL)

    ## Selecting site for searching
    self.site = wx.ComboBox(panel, -1, choices=AVAILABLE_SITES,
                            style=wx.CB_READONLY)
    self.site.SetValue(AVAILABLE_SITES[0])

    ## Terms for searching
    self.search_form = wx.TextCtrl(panel, ID_SEARCH_FORM, '', 
                          style=wx.TE_LEFT|wx.TE_PROCESS_ENTER)
    self.Bind(wx.EVT_TEXT_ENTER, self.DoSearch, id=ID_SEARCH_FORM)

    ## Do Search!
    search_button = wx.Button(panel, ID_SEARCH_BUTTON, 'Search!')
    self.Bind(wx.EVT_BUTTON, self.DoSearch, id=ID_SEARCH_BUTTON)

    headSizer = wx.FlexGridSizer(cols=3,vgap=30,hgap=10)
    headSizer.AddGrowableCol(1)
    headSizer.Add(self.site, 0, wx.ALIGN_CENTER)
    headSizer.Add(self.search_form, 0, wx.EXPAND)
    headSizer.Add(search_button, 0, wx.ALIGN_CENTER)
    mainSizer.Add(headSizer, 0, wx.EXPAND|wx.ALL, 10)

    ## Detailed result
    self.search_log = wx.StaticText(panel, -1, '', size=logSize)
    mainSizer.Add(self.search_log, 0, wx.EXPAND|wx.ALL, 10)

    self.search_results = wx.ListCtrl(panel, -1, size=resultsListSize,
                            style=wx.LC_REPORT|wx.LC_HRULES|wx.LC_VRULES )
    self.search_results.InsertColumn(0, 'Authors', width=authorWidth)
    self.search_results.InsertColumn(1, 'Title', width=titleWidth)
    self.search_results.InsertColumn(2, 'Year', width=yearWidth)
    self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.LaunchPubItemDialog)
    mainSizer.Add(self.search_results, 0, wx.EXPAND|wx.ALL, 10)
   
    ## Closing window
    close_button = wx.Button(panel, ID_CLOSE_BUTTON, 'Close')
    self.Bind(wx.EVT_BUTTON, self.OnClose, id=ID_CLOSE_BUTTON)

    buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
    buttonSizer.Add( (10,10), 1 )
    buttonSizer.Add( close_button )
    buttonSizer.Add( (10,10), 1 )
    mainSizer.Add(buttonSizer, 0, wx.EXPAND|wx.BOTTOM, 10)
    
    panel.SetSizer(mainSizer)
    self.Centre()

  def OnClose(self, event):
    self.Close()

  def DoSearch(self, event):
    log_text = "'%s'@%s" % (self.search_form.GetValue(), self.site.GetValue())
    self.search_log.SetLabel("Searching..."+log_text)

    if( self.site.GetValue() == AVAILABLE_SITES[0] ):
      articles = pubmed_search(self.search_form.GetValue(), PUBMED_RETMAX)
    elif( self.site.GetValue() == AVAILABLE_SITES[1] ):
      articles = google_search(self.search_form.GetValue(), PUBMED_RETMAX)
   
    log_text += ": %d records are found" % len(articles)
    if( len(articles) == atoi(PUBMED_RETMAX) ):
      log_text += '(MAX)'

    self.search_log.SetLabel(log_text)
    self.search_results.DeleteAllItems()
    self.pubitem_list = []
    for pubitem in articles:
      entry = [pubitem.authors, pubitem.title, pubitem.pub_year]
      self.search_results.Append(entry)
      self.pubitem_list.append( pubitem )
    
  def LaunchPubItemDialog(self, event):
    idx = event.GetIndex()
    dialog = PubShelfPubItemDialog(self.parent, -1)
    dialog.SetPubItem(self.pubitem_list[idx])
    dialog.Show()
