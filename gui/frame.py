import wx
from menu import PubShelfMenuBar
from tag_tree import PubShelfTagTree
from item_list import PubShelfItemList
from item_content import PubShelfItemContent

#windowSize = wx.Size(800,600)
windowSize = wx.Size(600,400)
treePaneWidth = 200
minTreePaneWidth = 100
itemListHeight = 200
minItemPaneHeight = 100

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
    self.itemList = PubShelfItemList(self.itemSplitter, -1, self.dbi, self.conf)

    ## ItemContent
    self.itemContent = PubShelfItemContent(self.itemSplitter, -1, conf)
    
    ## Wrap Up
    self.itemSplitter.SplitHorizontally(self.itemList, self.itemContent)
    self.treeSplitter.SplitVertically(self.tree, self.itemSplitter)
    self.treeSplitter.SetSashPosition(treePaneWidth)
    self.Centre()

  #def OnListItemSelected(self, event):
  #  nickname = event.GetItem().GetText()
  #  pubitem = self.dbi.get_pubitem_by_nickname( nickname )
  #  self.itemContent.SetPage(
  #    'Here is some <b>formatted</b> <font color="red">text</font>'
  #    'Here is some <b>formatted</b> <font color="red">text</font>'
  #    'Here is some <b>formatted</b> <font color="red">text</font>'
  #    '<a href="file:///home/linusben/Desktop/forcjn.pdf">PDF</a>'
  #    '<a href="file:///usr/share/doc/python2.5-doc/html/tut/tut.html">HTML</A>'
  #    )
  #  event.Skip()
