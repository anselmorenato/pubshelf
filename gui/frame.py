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
  def __init__(self, parent, id, title, dbi, conf):
    wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, windowSize)
    self.dbi = dbi
    self.conf = conf

    ## MenuBar
    self.SetMenuBar( PubShelfMenuBar() )
    
    ## StatusBar
    self.statusbar = self.CreateStatusBar();

    ## ToolBar
    toolbar = self.CreateToolBar();
    toolbar.AddSimpleTool(1, 
        wx.Image('../icon/new.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap()) 
    toolbar.AddSimpleTool(2,
        wx.Image('../icon/search.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap())
    toolbar.AddSeparator()
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
    self.tree = PubShelfTagTree(self.treeSplitter, -1, self.dbi, self.conf)

    ## ItemList
    self.itemList = PubShelfItemList(self.itemSplitter, -1, self.dbi, self.conf)

    ## ItemContent
    self.itemContent = PubShelfItemContent(self.itemSplitter, -1, self.conf)
    
    ## Wrap Up
    self.itemSplitter.SplitHorizontally(self.itemList, self.itemContent,
                                      itemListHeight)
    self.itemSplitter.SetSashPosition(itemListHeight)
    self.treeSplitter.SplitVertically(self.tree, self.itemSplitter, 
                                      treePaneWidth)

  def PubItemDialog(self, event):
    self.new_dialog = PubShelfPubItemDialog(None, -1)
    self.new_dialog.ShowModal()
    self.new_dialog.Destroy()
  
  def SearchDialog(self, event):
    self.search_dialog = PubShelfSearchDialog(None, -1)
    self.search_dialog.ShowModal()
    self.search_dialog.Destroy()
