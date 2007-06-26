import wx
from dialog_pubitem import PubShelfPubItemDialog
from model_pubitem import PubItem

WIDTH_NICKNAME = 130
WIDTH_YEAR = 70
WIDTH_TITLE = 400

class PubShelfItemList(wx.ListCtrl):
  def __init__(self, parent, id):
    window_style = wx.LC_REPORT
    super(PubShelfItemList, self).__init__(parent, id, style=window_style)
    
    self.InsertColumn(0, 'NickName', width=WIDTH_NICKNAME)
    self.InsertColumn(1, 'Year', width=WIDTH_YEAR)
    self.InsertColumn(2, 'Title', width=WIDTH_TITLE)

    #self.Bind(wx.EVT_SIZE, self.OnItemListSizeChanged)
    self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnListItemSelected)
    self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnPubItemActivated)

  def SetItemList(self, pubitems):
    self.DeleteAllItems()
    for pubitem in pubitems:
      self.Append([pubitem.nickname, pubitem.pub_year, pubitem.title])

  def OnResize(self):
    if( self.GetSize().x > 0 ):
      WIDTH_TITLE = self.GetSize().x - WIDTH_NICKNAME - WIDTH_YEAR
      self.SetColumnWidth(2, width=WIDTH_TITLE)

  def OnListItemSelected(self, event):
    nickname = event.GetItem().GetText()
    pi = PubItem()
    pubitem = pi.find_by_nickname(nickname)
    item_content = self.GetParent().GetParent().GetParent().itemContent
    item_content.SetPubItem( pubitem )
    event.Skip()

  def OnPubItemActivated(self, event):
    nickname = event.GetItem().GetText()
    pi = PubItem()
    pubitem = pi.find_by_nickname(nickname)
    dialog = PubShelfPubItemDialog(None, -1)
    dialog.SetPubItem(pubitem)
    dialog.ShowModal()
    dialog.Destroy()
