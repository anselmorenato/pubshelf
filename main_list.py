import wx
from dialog_pubitem import PubShelfPubItemDialog

WIDTH_NICKNAME = 130
WIDTH_YEAR = 70
WIDTH_TITLE = 200

class PubShelfItemList(wx.ListCtrl):
  def __init__(self, parent, id, dbi, conf):
    window_style = wx.LC_REPORT
    super(PubShelfItemList, self).__init__(parent, id, style=window_style)
    self.dbi = dbi
    self.conf = conf
    
    self.InsertColumn(0, 'NickName', width=WIDTH_NICKNAME)
    self.InsertColumn(1, 'Year', width=WIDTH_YEAR)
    self.InsertColumn(2, 'Title', width=WIDTH_TITLE)

    self.Bind(wx.EVT_SIZE, self.OnItemListSizeChanged)
    self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnListItemSelected)
    self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnPubItemActivated)

  def OnItemListSizeChanged(self, event):
    if( self.GetSize().x > 0 ):
      WIDTH_TITLE = self.GetSize().x - WIDTH_NICKNAME - WIDTH_YEAR
      self.SetColumnWidth(2, width=WIDTH_TITLE)
    event.Skip()

  def OnListItemSelected(self, event):
    nickname = event.GetItem().GetText()
    pubitem = self.dbi.get_pubitem_by_nickname( nickname )
    item_content = self.GetParent().GetParent().GetParent().itemContent
    item_content.set_pubitem( pubitem )
    event.Skip()

  def OnPubItemActivated(self, event):
    nickname = event.GetItem().GetText()
    pubitem = self.dbi.get_pubitem_by_nickname( nickname )
    dialog = PubShelfPubItemDialog(None, -1, self.conf)
    dialog.SetPubItem(pubitem)
    dialog.ShowModal()
    dialog.Destroy()
