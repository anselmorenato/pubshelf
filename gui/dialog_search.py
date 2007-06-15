import wx, wx.html
from string import atoi
import sys
sys.path.append('../libpy/')
from pubmed import *
from dialog_pubitem import PubShelfPubItemDialog

ID_SEARCH_BUTTON = 3000
ID_CLOSE_BUTTON = 3001
ID_SEARCH_FORM  = 3002

searchDialogSize = (600,600)
searchSiteComboSize = (150,28)
searchSiteComboPos = (10,10)
searchFormSize = (330,28)
searchFormPos = (170,10)
searchDoButtonSize = (80,28)
searchDoButtonPos = (510,10)
searchResultLogSize = (580,10)
searchResultLogPos = (10,40)
searchResultSize = (580,480)
searchResultPos = (10,60)
searchResultAuthorWidth = 100
searchResultTitleWidth = 410
searchResultPubYearWidth = 50
searchCloseButtonSize = (100,30)
searchCloseButtonPos = (250,550)

AVAILABLE_SITES = ['pubmed','google scholar']
PUBMED_RETMAX = '50'

class PubShelfSearchDialog(wx.Dialog):
  def __init__(self, parent, id, conf):
    wx.Dialog.__init__(self, parent, id, 'Search', size=searchDialogSize)
    self.conf = conf

    panel = wx.Panel(self, -1)

    ## Selecting site for searching
    self.site = wx.ComboBox(panel, -1, 
                          size=searchSiteComboSize, pos=searchSiteComboPos,
                          choices=AVAILABLE_SITES, style=wx.CB_READONLY)
    self.site.SetValue(AVAILABLE_SITES[0])

    ## Terms for searching
    self.search_form = wx.TextCtrl(panel, ID_SEARCH_FORM, '', 
                          size=searchFormSize, pos=searchFormPos,
                          style=wx.TE_LEFT|wx.TE_PROCESS_ENTER)
    self.Bind(wx.EVT_TEXT_ENTER, self.DoSearch, id=ID_SEARCH_FORM)

    ## Do Search!
    search_button = wx.Button(panel, ID_SEARCH_BUTTON, 'Search!', 
                          style=wx.BU_EXACTFIT,
                          size=searchDoButtonSize, pos=searchDoButtonPos)
    self.Bind(wx.EVT_BUTTON, self.DoSearch, id=ID_SEARCH_BUTTON)

    ## Detailed result
    self.search_log = wx.StaticText(panel, -1, '',
                        size=searchResultLogSize, pos=searchResultLogPos)
    self.search_results = wx.ListCtrl(panel, -1, 
                            style=wx.LC_REPORT|wx.LC_HRULES|wx.LC_VRULES,
                            size=searchResultSize, pos=searchResultPos)
    self.search_results.InsertColumn(0, 'Authors', 
                                    width=searchResultAuthorWidth)
    self.search_results.InsertColumn(1, 'Title',
                                    width=searchResultTitleWidth)
    self.search_results.InsertColumn(2, 'Year',
                                    width=searchResultPubYearWidth)
    self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.LaunchPubItemDialog)
   
    ## Closing window
    close_button = wx.Button(panel, ID_CLOSE_BUTTON, 'Close', 
                          style=wx.BU_EXACTFIT,
                          size=searchCloseButtonSize, pos=searchCloseButtonPos)
    self.Bind(wx.EVT_BUTTON, self.OnClose, id=ID_CLOSE_BUTTON)
    
    self.Centre()

  def OnClose(self, event):
    self.Close()

  def DoSearch(self, event):
    log_text = "'%s'@%s" % (self.search_form.GetValue(), self.site.GetValue())
    self.search_log.SetLabel("Searching..."+log_text)

    if( self.site.GetValue() == AVAILABLE_SITES[0] ):
      articles = pubmed_search(self.search_form.GetValue(), PUBMED_RETMAX)
   
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
    dialog = PubShelfPubItemDialog(None, -1, self.conf)
    dialog.SetPubItem(self.pubitem_list[idx])
    dialog.ShowModal()
    dialog.Destroy()
