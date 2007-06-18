import wx
import sys
from model_tag import Tag
from model_pubitem import PubItem

class PubShelfTagTree(wx.TreeCtrl):
  def __init__(self, parent, id):
    window_style = wx.TR_HIDE_ROOT|wx.TR_HAS_BUTTONS
    super(PubShelfTagTree, self).__init__(parent, id, style=window_style) 

    root = self.AddRoot('Root')
    category = dict()
    t = Tag()
    for tag in t.find_all():
      if(not category.has_key(tag.category)):
        category[tag.category] = self.AppendItem(root, tag.category)
      self.AppendItem(category[tag.category], tag.name)
    
    self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnTreeSelChanged)

  def OnTreeSelChanged(self, event):
    item = event.GetItem()
    tag_name = self.GetItemText(item)
    parent_item = self.GetItemParent(item)
    tag_category = self.GetItemText(parent_item)

    pi = PubItem()
    pubitems = []
    if( tag_category == 'Root' ):
      pubitems = pi.find_by_tag_category(tag_name)
    else:
      pubitems = pi.find_by_tag_category_and_name(tag_category, tag_name)

    item_list = self.GetParent().GetParent().itemList
    item_list.DeleteAllItems()
    for pubitem in pubitems:
      entry = [pubitem.nickname, pubitem.pub_year, pubitem.title]
      item_list.Append(entry)
