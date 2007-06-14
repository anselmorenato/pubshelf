import wx

ID_SEARCH_BUTTON = 3000
searchDialogSize = (600,600)
siteComboSize = (150,-1)
class PubShelfSearchDialog(wx.Dialog):
  def __init__(self, parent, id):
    wx.Dialog.__init__(self, parent, id, 'Search', size=searchDialogSize)
    available_sites = ['pubmed','google scholar']

    panel = wx.Panel(self, -1)
    vbox = wx.BoxSizer(wx.VERTICAL)
    hbox = wx.BoxSizer(wx.HORIZONTAL)
    self.site = wx.ComboBox(panel, -1, size=siteComboSize, 
                          choices=available_sites, style=wx.CB_READONLY)
    self.site.SetValue(available_sites[0])
    self.search_form = wx.TextCtrl(panel, -1, '', style=wx.TE_CENTER)
    self.search_results = wx.ListCtrl(panel, -1, style=wx.LC_REPORT)
    search_button = wx.Button(panel, ID_SEARCH_BUTTON, 'Search!')
    hbox.Add(self.site, 1)
    hbox.Add(self.search_form, 1, flag=wx.EXPAND)
    hbox.Add(search_button, 1)

    vbox.Add(hbox)
    vbox.Add(self.search_results, flag=wx.EXPAND)
    panel.SetSizer(vbox)
    self.Bind(wx.EVT_BUTTON, self.DoSearch, id=ID_SEARCH_BUTTON)
    self.Centre()

  def DoSearch(self, event):
    print self.site.GetValue()
    print self.search_form.GetValue()
