import wx
import sys
from libpy.model_tag import Tag
from libpy.model_pubitem import PubItem

class PubShelfTagTree(wx.TreeCtrl):
  def __init__(self, parent, id):
    window_style = wx.TR_HIDE_ROOT|wx.TR_HAS_BUTTONS|wx.TR_LINES_AT_ROOT
    #window_style = wx.TR_HAS_BUTTONS
    super(PubShelfTagTree, self).__init__(parent, id, style=window_style) 
    self.Refresh()
    self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnTreeSelChanged)

  def GetSelTag(self):
    if (self.GetSelection()):
      selected = self.GetSelection()
      sel_tag = self.GetItemText(selected)
      
      if (not self.ItemHasChildren(selected)):
        sel_category = self.GetItemText(self.GetItemParent(selected))
      else:
        sel_category = sel_tag
        sel_tag = ''
    else:
      sel_tag = 'All'
      sel_category = ''
    
    return (sel_category, sel_tag)
  def Refresh(self):
    (sel_category, sel_tag) = self.GetSelTag()
    
    self.DeleteAllItems()
    self.root = self.AddRoot('Local')
    self.categories = dict()
    self.tags = dict()
    self.categories['All'] = self.AppendItem(self.root, 'All')
    self.categories['No Category'] = self.AppendItem(self.root, 'No Category')
    
    if (sel_category == 'All' and sel_tag == ''):
      self.SelectItem(self.categories['All'])
    elif (sel_category == 'No Category' and sel_tag == ''):
      self.SelectItem(self.categories['No Category'])
    
    t = Tag()
    for tag in t.find_all():
      if(tag.category == ''):
        id = self.AppendItem(self.categories['No Category'], tag.name)
        self.tags['No Category'+'/'+tag.name] = id
        if (tag.name == sel_tag and sel_category == 'No Category'):
          self.SelectItem(id)
      else:
        if(not self.categories.has_key(tag.category)):
          self.categories[tag.category]=self.AppendItem(self.root, tag.category)
        id = self.AppendItem(self.categories[tag.category], tag.name)
        self.tags[tag.category+'/'+tag.name] = id
        if (tag.name == sel_tag and tag.category == sel_category):
          self.SelectItem(id)
    
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
      if( tag_category == 'No Category' ): tag_category = ''
      pubitems = pi.find_by_tag_category_and_name(tag_category, selected_text)
	
    item_list = self.GetParent().GetParent().itemList
    item_list.SetItemList(pubitems)

  def ChangeToAnItem(self, category_name, tag_name):
    # TODO : this is deadly dirty way to coding for non-category tags and not doing user-generated event
    pi = PubItem()
    pubitems = pi.find_by_tag_category_and_name(category_name, tag_name)

    if (category_name == ''): category_name = 'No Category'    
    self.SelectItem( self.tags[category_name+'/'+tag_name] )
  
    item_list = self.GetParent().GetParent().itemList
    item_list.SetItemList(pubitems)
    
