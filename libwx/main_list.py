import wx
from dialog_pubitem import PubShelfPubItemDialog
from libpy.model_pubitem import PubItem

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
    self.sort_type = 0 ## 0 : non-sort, 1: ascending, -1: descending
    
    self.pubitems = []

    self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnListItemSelected)
    self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnPubItemActivated)
    self.Bind(wx.EVT_LIST_COL_CLICK, self.OnColumnClicked)

  def SetItemList(self, pubitems):
    self.pubitems = []
    for pubitem in pubitems:
      self.pubitems.append( pubitem )
    self.Refresh()
  
  def remove_by_pubitem_id(self, id):
    idx = 0;
    for pubitem in self.pubitems:
      if(pubitem.id == id): 
        del self.pubitems[idx]
      idx += 1

  def Refresh(self):
    self.DeleteAllItems()
    for pubitem in self.pubitems:
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
    frame = self.GetParent().GetParent().GetParent()
    dialog = PubShelfPubItemDialog(frame, -1)
    dialog.SetPubItem(pubitem)
    dialog.Show()
  
  def OnColumnClicked(self, event):
    column = event.m_col
    if( self.sort_type == 1 ):
      self.sort_type = -1
      if( column == 1 ):
        self.pubitems.sort(lambda x, y: y.pub_year - x.pub_year)
      elif( column == 2 ):
        self.pubitems.sort(lambda x, y: cmp(y.title, x.title))
      else:
        self.pubitems.sort(lambda x, y: cmp(y.nickname, x.nickname))
    else:
      self.sort_type = 1
      if( column == 1 ):
        self.pubitems.sort(lambda x, y: x.pub_year - y.pub_year)
      elif( column == 2 ):
        self.pubitems.sort(lambda x, y: cmp(x.title, y.title))
      else:
        self.pubitems.sort(lambda x, y: cmp(x.nickname, y.nickname))

    self.Refresh()
