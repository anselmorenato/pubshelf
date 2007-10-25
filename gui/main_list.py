import wx
from dialog_pubitem import PubShelfPubItemDialog
from model_pubitem import PubItem
from niftylist import NiftyVirtualList, NiftyListItem

WIDTH_NICKNAME = 130
WIDTH_YEAR = 70
WIDTH_TITLE = 400

#http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/426407

class PubShelfItemList(NiftyVirtualList):
#class PubShelfItemList(wx.ListCtrl):
  def __init__(self, parent, id):
    window_style = wx.LC_REPORT
    super(PubShelfItemList, self).__init__(parent, id, style=window_style | wx.LC_VIRTUAL )
#    super(PubShelfItemList, self).__init__(parent, id, style=window_style )
    
    self.InsertColumn(0, 'NickName', width=WIDTH_NICKNAME)
    self.InsertColumn(1, 'Year', width=WIDTH_YEAR)
    self.InsertColumn(2, 'Title', width=WIDTH_TITLE)
    
    self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnListItemSelected)
    self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnPubItemActivated)
    self.Bind(wx.EVT_LIST_COL_CLICK, self.OnColClick)

#    self.pubid_to_idx_map = {} # dictionary
    self.colsort = [0, 0, 0] # 0=ascending ready, 1=descending ready
    self.colsortfunc = [
                        lambda x, y: cmp(x.nickname, y.nickname), 
                        lambda x, y: cmp(x.pub_year, y.pub_year),
                        lambda x, y: cmp(x.title, y.title),
                        lambda x, y: cmp(y.nickname, x.nickname),
                        lambda x, y: cmp(y.pub_year, x.pub_year),
                        lambda x, y: cmp(y.title, x.title)
                       ]

  def SetItemList(self, pubitems):
    self.DeleteAllItems()
    self.SetSort(lambda x, y: cmp(x.id, y.id)) # default sorting

    for pubitem in pubitems:
      item = self.InsertItem(data = pubitem)
      item.SetText(pubitem.nickname, 0)
      item.SetText(str(pubitem.pub_year), 1)
      item.SetText(pubitem.title, 2)
#      self.pubid_to_idx_map[pubitem.id] = item
  
  def remove_by_pubitem_id(self, id):
    self.SetFilter(lambda x: x.id == id)
    self.DeleteItem(0)
    self.SetFilter(lambda x: True)
#    self.DeleteItem(pubid_to_idx_map[id])

  def OnColClick(self, event):
    col = event.m_col
    self.SetSort(self.colsortfunc[self.colsort[col]*3+col])
    self.colsort[col] = 1 - self.colsort[col]
    
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
    frame = self.GetParent().GetParent().GetParent()
    dialog = PubShelfPubItemDialog(frame, -1)
    dialog.SetPubItem(pubitem)
    dialog.Show()
