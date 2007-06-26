import wx
import sys, os
from model_comment import Comment

DIALOG_SIZE = (400,600)
class PubShelfCommentDialog(wx.Dialog):
  def __init__(self, parent, id, pubitem):
    wx.Dialog.__init__(self, parent, id, 'PubItem', size=DIALOG_SIZE)
    self.forms = dict()
    panel = wx.Panel(self, -1)

    mainSizer = wx.BoxSizer(wx.VERTICAL)

    IDLabel = wx.StaticText(panel, -1, 'Comment ID', style=wx.ALIGN_CENTER)
    self.forms['id'] = wx.StaticText(panel, -1, '', style=wx.ALIGN_CENTER)
    pubitemIDLabel = wx.StaticText(panel, -1, 'PubItem ID', 
                                    style=wx.ALIGN_CENTER)
    self.forms['pubitem_id'] = wx.StaticText(panel, -1, '', 
                                             style=wx.ALIGN_CENTER)
    
    headSizer = wx.BoxSizer(wx.HORIZONTAL)
    headSizer.Add(IDLabel, wx.SHAPED, 10)
    headSizer.Add(self.forms['id'], wx.SHAPED)
    headSizer.Add(pubitemIDLabel, wx.SHAPED, 10)
    headSizer.Add(self.forms['pubitem_id'], wx.SHAPED)
    mainSizer.Add(headSizer, 0, wx.EXPAND|wx.ALL, 10)

    titleLabel = wx.StaticText(panel, -1, 'Title', style=wx.ALIGN_CENTER)
    self.forms['title'] = wx.TextCtrl(panel, -1, '')
    authorLabel = wx.StaticText(panel, -1, 'Author', style=wx.ALIGN_CENTER)
    self.forms['author'] = wx.TextCtrl(panel, -1, '')
    textbodyLabel = wx.StaticText(panel, -1, 'Text', style=wx.ALIGN_CENTER)
    self.forms['textbody'] = wx.TextCtrl(panel, -1, '')
    
    formSizer = wx.FlexGridSizer(cols=2, hgap=10)
    formSizer.AddGrowableCol(1)
    formSizer.Add(titleLabel, 0, wx.ALIGN_CENTER)
    formSizer.Add(self.forms['title'], 0, wx.EXPAND)
    formSizer.Add(authorLabel, 0, wx.ALIGN_CENTER)
    formSizer.Add(self.forms['author'], 0, wx.EXPAND)
    formSizer.Add(textbodyLabel, 0, wx.ALIGN_CENTER)
    formSizer.Add(self.forms['textbody'], 0, wx.EXPAND)
    mainSizer.Add(formSizer, 0, wx.EXPAND|wx.ALL, 10)

    panel.SetSizer(mainSizer)
    self.Centre()


  def SetComment(self, comment):
    self.forms['id'].SetLabel("%d" % comment.id )
    self.forms['pubitem_id'].SetLabel("%d" % comment.pubitem_id)
    self.forms['title'].SetValue(comment.title)
    self.forms['author'].SetValue(comment.author)
    self.forms['textbody'].SetValue(comment.textbody)
