import wx
import sys
from model_tag import Tag
from model_pubitem import PubItem

class PubShelfTagTree(wx.TreeCtrl):
  def __init__(self, parent, id):
    window_style = wx.TR_HIDE_ROOT|wx.TR_HAS_BUTTONS
    super(PubShelfTagTree, self).__init__(parent, id, style=window_style) 
    self.Refresh()
    self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnTreeSelChanged)
    
  def Refresh(self):
    self.DeleteAllItems()
    root = self.AddRoot('Root')
    self.AppendItem(root,'All')
    self.AppendItem(root,'No Category')
    
    category = dict()
    t = Tag()
    for tag in t.find_all():
      if(not category.has_key(tag.category)):
        category[tag.category] = self.AppendItem(root, tag.category)
      self.AppendItem(category[tag.category], tag.name)
    
  def OnTreeSelChanged(self, event):
    item = event.GetItem()
    tag_name = self.GetItemText(item)
    parent_item = self.GetItemParent(item)
    tag_category = self.GetItemText(parent_item)

    pi = PubItem()
    pubitems = []
    if( tag_category == 'Root' ):
      if( tag_name == 'All' ):
        pubitems = pi.find_all()
      elif( tag_name == 'No Category' ):
        pubitems = pi.find_by_tag_category('')
      else:
        pubitems = pi.find_by_tag_category(tag_name)
    else:
      pubitems = pi.find_by_tag_category_and_name(tag_category, tag_name)

    item_list = self.GetParent().GetParent().itemList
    item_list.SetItemList(pubitems)
