import wx
import sys
sys.path.append('../libpy/')
from model_tag import Tag

class PubShelfTagTree(wx.TreeCtrl):
  def __init__(self, parent, id, dbi, conf):
    window_style = wx.TR_HIDE_ROOT|wx.TR_HAS_BUTTONS
    super(PubShelfTagTree, self).__init__(parent, id, style=window_style) 
    self.conf = conf
    self.dbi = dbi

    root = self.AddRoot('Root')
    category = dict()
    t = Tag()
    for tag in t.get_tags():
      if(not category.has_key(tag.category)):
        category[tag.category] = self.AppendItem(root, tag.category)
      self.AppendItem(category[tag.category], tag.name)
    
    self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnTreeSelChanged)

  def OnTreeSelChanged(self, event):
    item = event.GetItem()
    tag_name = self.GetItemText(item)
    parent_item = self.GetItemParent(item)
    tag_category = self.GetItemText(parent_item)

    pubitems = []
    if( tag_category == 'Root' ):
      pubitems = self.dbi.get_pubitems_by_tag_category(tag_name)
    else:
      pubitems = self.dbi.get_pubitems_by_tag(tag_category, tag_name)

    item_list = self.GetParent().GetParent().itemList
    item_list.DeleteAllItems()
    for pubitem in pubitems:
      entry = [pubitem.nickname, pubitem.pub_year, pubitem.title]
      item_list.Append(entry)
