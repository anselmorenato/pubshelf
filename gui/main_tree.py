import wx
import sys
from model_tag import Tag
from model_pubitem import PubItem

class PubShelfTagTree(wx.TreeCtrl):
  def __init__(self, parent, id):
    window_style = wx.TR_HIDE_ROOT|wx.TR_HAS_BUTTONS|wx.TR_LINES_AT_ROOT
    #window_style = wx.TR_HAS_BUTTONS
    super(PubShelfTagTree, self).__init__(parent, id, style=window_style) 
    self.Refresh()
    self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnTreeSelChanged)
    
  def Refresh(self):
    self.DeleteAllItems()
    self.root = self.AddRoot('Local')
    self.categories = dict()
    self.categories['All'] = self.AppendItem(self.root, 'All')
    self.categories['No Category'] = self.AppendItem(self.root, 'No Category')
    
    t = Tag()
    for tag in t.find_all():
      if(not self.categories.has_key(tag.category)):
        self.categories[tag.category] = self.AppendItem(self.root, tag.category)
      self.AppendItem(self.categories[tag.category], tag.name)
    
  def OnTreeSelChanged(self, event):
    selected_item = event.GetItem()
    selected_text = self.GetItemText(selected_item)

    pi = PubItem()
    pubitems = []
    if( self.categories.has_key(selected_text) ):
      if( selected_text == 'All' ):
        pubitems = pi.find_all()
      elif( selected_text == 'No Category' ):
        pubitems = pi.find_by_tag_category('')
      else:
        pubitems = pi.find_by_tag_category(selected_text)
    else:
      parent_item = self.GetItemParent(selected_item)
      tag_category = self.GetItemText(parent_item)
      pubitems = pi.find_by_tag_category_and_name(tag_category, selected_text)
	
    item_list = self.GetParent().GetParent().itemList
    item_list.SetItemList(pubitems)
