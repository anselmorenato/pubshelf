import wx
from menu import PubShelfMenuBar
from item_content import PubShelfItemContent
from tag_tree import PubShelfTagTree

#windowSize = wx.Size(800,600)
windowSize = wx.Size(600,400)
treePaneWidth = 200
minTreePaneWidth = 100
itemListHeight = 200
minItemPaneHeight = 100
nicknameColumnWidth = 130
pubyearColumnWidth  = 70
citationColumnWidth = 200

class PubShelfFrame(wx.Frame):
  def __init__(self, parent, id, title, dbi, conf):
    wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, windowSize)
    self.dbi = dbi
    self.conf = conf

    ## MenuBar
    self.SetMenuBar( PubShelfMenuBar() )

    ## StatusBar
    self.CreateStatusBar();

    ## Splitter 
    self.treeSplitter = wx.SplitterWindow(self, -1, style=wx.SP_BORDER)
    self.treeSplitter.SetMinimumPaneSize(minTreePaneWidth)
    self.itemSplitter = wx.SplitterWindow(self.treeSplitter, -1,
                                          style=wx.SP_BORDER)

    ## TagTree
    self.tree = PubShelfTagTree(self.treeSplitter, -1, self.dbi, self.conf)

    ## ItemList
    self.itemList = wx.ListCtrl(self.itemSplitter, 26, style=wx.LC_REPORT)
    self.itemList.InsertColumn(0, 'Nickname', width=nicknameColumnWidth)
    self.itemList.InsertColumn(1, 'Year', width=pubyearColumnWidth)
    self.itemList.InsertColumn(2, 'Citation', width=citationColumnWidth)

    ## ItemContent
    self.itemContent = PubShelfItemContent(self.itemSplitter, -1, conf)
    
    ## Events
    self.itemList.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnListItemSelected)
    self.itemList.Bind(wx.EVT_SIZE, self.OnItemPaneSizeChanged)

    ## Wrap Up
    self.itemSplitter.SplitHorizontally(self.itemList, self.itemContent)
    self.treeSplitter.SplitVertically(self.tree, self.itemSplitter)
    self.treeSplitter.SetSashPosition(treePaneWidth)
    self.Centre()

  def OnListItemSelected(self, event):
    nickname = event.GetItem().GetText()
    pubitem = self.dbi.get_pubitem_by_nickname( nickname )
    self.itemContent.SetPage(
      'Here is some <b>formatted</b> <font color="red">text</font>'
      'Here is some <b>formatted</b> <font color="red">text</font>'
      'Here is some <b>formatted</b> <font color="red">text</font>'
      '<a href="file:///home/linusben/Desktop/forcjn.pdf">PDF</a>'
      '<a href="file:///usr/share/doc/python2.5-doc/html/tut/tut.html">HTML</A>'
      )
    event.Skip()

  def OnItemPaneSizeChanged(self, event):
    if( self.itemList.GetSize().x > 0 ):
      citationColumnWidth = self.itemList.GetSize().x - 200
      self.itemList.SetColumnWidth(2, width=citationColumnWidth)
    event.Skip()
