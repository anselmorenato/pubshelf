import wx
import sys, os
from model_comment import Comment

ID_SUBMIT_BUTTON = 4000
ID_DELETE_BUTTON = 4001
ID_CLOSE_BUTTON = 4002

DIALOG_SIZE = (400,400)
TEXTBODY_SIZE = (300,200)
class PubShelfCommentDialog(wx.Frame):
  def __init__(self, parent, id):
    wx.Frame.__init__(self, parent, id, 'PubItem', size=DIALOG_SIZE)
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
    mainSizer.Add(headSizer, 0, wx.ALL, 10)

    titleLabel = wx.StaticText(panel, -1, 'Title', style=wx.ALIGN_CENTER)
    self.forms['title'] = wx.TextCtrl(panel, -1, '')
    authorLabel = wx.StaticText(panel, -1, 'Author', style=wx.ALIGN_CENTER)
    self.forms['author'] = wx.TextCtrl(panel, -1, '')
    textbodyLabel = wx.StaticText(panel, -1, 'Text', style=wx.ALIGN_CENTER)
    self.forms['textbody'] = wx.TextCtrl(panel, -1, '', size=TEXTBODY_SIZE,
                                      style=wx.TE_MULTILINE)
    
    formSizer = wx.FlexGridSizer(cols=2, hgap=10)
    formSizer.AddGrowableCol(1)
    formSizer.AddGrowableRow(2)
    formSizer.SetFlexibleDirection(wx.BOTH)
    formSizer.Add(titleLabel, 0, wx.ALIGN_CENTER)
    formSizer.Add(self.forms['title'], 0, wx.EXPAND|wx.ALL, 5)
    formSizer.Add(authorLabel, 0, wx.ALIGN_CENTER)
    formSizer.Add(self.forms['author'], 0, wx.EXPAND|wx.ALL, 5)
    formSizer.Add(textbodyLabel, 0, wx.ALIGN_CENTER)
    formSizer.Add(self.forms['textbody'], 1, wx.EXPAND|wx.ALL, 5)
    mainSizer.Add(formSizer, 0, wx.EXPAND|wx.ALL, 10)

    ## Buttons
    submitButton = wx.Button(panel, ID_SUBMIT_BUTTON, 'Submit')
    deleteButton = wx.Button(panel, ID_DELETE_BUTTON, 'Delete')
    closeButton = wx.Button(panel, ID_CLOSE_BUTTON, 'Close')
    self.Bind(wx.EVT_BUTTON, self.OnSubmit, id=ID_SUBMIT_BUTTON)
    self.Bind(wx.EVT_BUTTON, self.OnDelete, id=ID_DELETE_BUTTON)
    self.Bind(wx.EVT_BUTTON, self.OnClose, id=ID_CLOSE_BUTTON)
    
    buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
    buttonSizer.Add( (10,10), wx.EXPAND|wx.ALL, 10 )
    buttonSizer.Add( submitButton, wx.EXPAND|wx.ALL, 10 )
    buttonSizer.Add( deleteButton, wx.EXPAND|wx.ALL, 10 )
    buttonSizer.Add( closeButton, wx.EXPAND|wx.ALL, 10 )
    buttonSizer.Add( (10,10), wx.EXPAND|wx.ALL, 10 )
    mainSizer.Add(buttonSizer,0, wx.EXPAND|wx.ALL, 10)

    panel.SetSizer(mainSizer)
    self.Centre()
  
  def OnClose(self, event):
    self.Close()

  def OnSubmit(self, event):
    c = Comment()
    c.id = self.forms['id'].GetLabel()
    c.pubitem_id = self.forms['pubitem_id'].GetLabel()
    c.title = self.forms['title'].GetValue()
    c.author = self.forms['author'].GetValue()
    c.textbody = self.forms['textbody'].GetValue()

    if( self.forms['title'].GetValue() and self.forms['textbody'].GetValue()):
      if( c.id != '' and c.id != '0' ):   
        c.update()
      else:
        c.insert()
      self.GetParent().pubitem.set_comments()
      self.GetParent().SetPubItem( self.GetParent().pubitem )
      self.Close()
  
  def OnDelete(self, event):
    msg_box = wx.MessageDialog(self, "Do you really want to delete?", "Warning", wx.YES_NO | wx.NO_DEFAULT | wx.CENTRE | wx.ICON_EXCLAMATION )
    result = msg_box.ShowModal()
    if( result == wx.ID_YES ):
      c = Comment()
      c.id = self.forms['id'].GetLabel()
      if( c.id != '0' ): c.delete()
      self.GetParent().pubitem.set_comments()
      self.GetParent().SetPubItem( self.GetParent().pubitem )
      self.Close()

  def SetComment(self, comment):
    self.forms['id'].SetLabel("%d" % comment.id )
    self.forms['pubitem_id'].SetLabel("%d" % comment.pubitem_id)
    self.forms['title'].SetValue(comment.title)
    self.forms['author'].SetValue(comment.author)
    self.forms['textbody'].SetValue(comment.textbody)
