import wx
from menu import PubShelfMenuBar
from dialog_pubitem import PubShelfPubItemDialog
from dialog_search import PubShelfSearchDialog
from main_tree import PubShelfTagTree
from main_list import PubShelfItemList
from main_content import PubShelfItemContent

windowSize = wx.Size(800,600)
treePaneWidth = 200
minTreePaneWidth = 100
itemListHeight = 300
minItemPaneHeight = 100

class PubShelfFrame(wx.Frame):
  def __init__(self, parent, id, title):
    wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, windowSize)

    ## MenuBar
    self.SetMenuBar( PubShelfMenuBar() )
    
    ## StatusBar
    self.statusbar = self.CreateStatusBar();

    ## ToolBar
    toolbar = self.CreateToolBar();
    tool_image_new = wx.Bitmap("./icon/new.bmp", wx.BITMAP_TYPE_BMP)
    tool_image_search = wx.Bitmap("./icon/search.bmp", wx.BITMAP_TYPE_BMP)
    toolbar.AddSimpleTool(1, tool_image_new, "New")
    toolbar.AddSimpleTool(2, tool_image_search, "Search")
    toolbar.AddSeparator()
    toolbar.Realize()
    self.Bind(wx.EVT_TOOL, self.PubItemDialog, id=1)
    self.Bind(wx.EVT_TOOL, self.SearchDialog, id=2)

    ## Splitter 
    self.treeSplitter = wx.SplitterWindow(self, -1, 
                                          style=wx.SP_BORDER)
    self.treeSplitter.SetMinimumPaneSize(minTreePaneWidth)
    self.itemSplitter = wx.SplitterWindow(self.treeSplitter, -1,
                                          style=wx.SP_BORDER)
    self.itemSplitter.SetMinimumPaneSize(minItemPaneHeight)

    ## TagTree
    self.tree = PubShelfTagTree(self.treeSplitter, -1)

    ## ItemList
    self.itemList = PubShelfItemList(self.itemSplitter, -1)

    ## ItemContent
    self.itemContent = PubShelfItemContent(self.itemSplitter, -1)
    
    ## Wrap Up
    self.itemSplitter.SplitHorizontally(self.itemList, self.itemContent,
                                      itemListHeight)
    self.treeSplitter.SplitVertically(self.tree, self.itemSplitter, 
                                      treePaneWidth)
    self.Bind(wx.EVT_SIZE, self.OnResize)

  def Refresh(self):
    self.tree.Refresh()
    self.itemList.Refresh()
    self.itemContent.Refresh()

  def PubItemDialog(self, event):
    self.new_dialog = PubShelfPubItemDialog(self, -1)
    self.new_dialog.ShowModal()
    self.new_dialog.Destroy()
  
  def SearchDialog(self, event):
    self.search_dialog = PubShelfSearchDialog(self, -1)
    self.search_dialog.ShowModal()
    self.search_dialog.Destroy()
  
  def OnResize(self, event):
    self.itemList.OnResize()
    event.Skip()

