import wx, wx.html
import sys, os
sys.path.append('../libpy/')
from data import *

ID_SUBMIT_BUTTON = 2000
ID_CLOSE_BUTTON = 2001
ID_FILE_SELECT_BUTTON = 2010
ID_FILE_ADD_BUTTON = 2011
ID_FILE_DELETE_BUTTON = 2012
ID_TAG_ADD_BUTTON  = 2020
ID_TAG_DELETE_BUTTON  = 2021

pubItemDialogSize = (600,600)
pubItemLabelSize = (90,25)
pubItemLargeFormSize = (490,25)
pubItemSmallFormSize = (200,25)
pubItemMediumFormSize = (350,25)
pubItemListSize = (420,75)
pubItemLabelXPos = 10
pubItemFormXPos  = 100
pubItemFileSelectButtonXPos = 460
pubItemFileAddButtonXPos = 530
pubItemYPosInit = 10
pubItemYPosStep = 30

pubItemButtonSize = (100,25)
pubItemSmallButtonSize = (60,25)
pubItemSubmitButtonPos = (190,560)
pubItemCloseButtonPos = (310,560)

class PubShelfPubItemDialog(wx.Dialog):
  def __init__(self, parent, id, conf):
    wx.Dialog.__init__(self, parent, id, 'PubItem', size=pubItemDialogSize)

    self.conf = conf
    self.tag_list = []
    self.file_list = []

    panel = wx.Panel(self, -1)

    ## Basic elements
    self.forms = dict()

    labels = ['ID','Nickname','Pub type']
    pubItemYPos = pubItemYPosInit
    for label in labels:
      wx.StaticText(panel, -1, label, size=pubItemLabelSize, 
                      pos = (pubItemLabelXPos, pubItemYPos))
      self.forms[label] = wx.StaticText(panel, -1, '', 
                            size=pubItemSmallFormSize,
                            pos = (pubItemFormXPos, pubItemYPos))
      pubItemYPos += pubItemYPosStep

    labels = ['Title','Authors','Journal','Publisher']
    for label in labels:
      wx.StaticText(panel, -1, label, size=pubItemLabelSize, 
                      pos = (pubItemLabelXPos, pubItemYPos))
      self.forms[label] = wx.TextCtrl(panel, -1, '', 
                            size=pubItemLargeFormSize,
                            pos = (pubItemFormXPos, pubItemYPos))
      pubItemYPos += pubItemYPosStep

    labels = ['Volume','Page','Pub Year']
    for label in labels:
      wx.StaticText(panel, -1, label, size=pubItemLabelSize, 
                      pos = (pubItemLabelXPos, pubItemYPos))
      self.forms[label] = wx.TextCtrl(panel, -1, '', 
                            size=pubItemSmallFormSize,
                            pos = (pubItemFormXPos, pubItemYPos))
      pubItemYPos += pubItemYPosStep
    
    ## Tag
    wx.StaticText(panel, -1, 'Tags', size=pubItemLabelSize, 
                  pos = (pubItemLabelXPos, pubItemYPos))
    self.tag_form = wx.TextCtrl(panel, -1, '', size=pubItemMediumFormSize,
                      pos = (pubItemFormXPos, pubItemYPos))
    tag_add_button = wx.Button(panel, ID_TAG_ADD_BUTTON, 'Add', 
                          style=wx.BU_EXACTFIT, size=pubItemSmallButtonSize, 
                          pos=(pubItemFileSelectButtonXPos, pubItemYPos))
    self.Bind(wx.EVT_BUTTON, self.AddTag, id=ID_TAG_ADD_BUTTON)

    ## Tag List
    pubItemYPos += pubItemYPosStep
    self.tag_list_form = wx.ListCtrl(panel, -1,
                            style=wx.LC_LIST, size=pubItemListSize,
                            pos=(pubItemFormXPos, pubItemYPos))
    tag_delete_button = wx.Button(panel, ID_TAG_DELETE_BUTTON, 'Delete', 
                          style=wx.BU_EXACTFIT, size=pubItemSmallButtonSize, 
                          pos=(pubItemFileAddButtonXPos, pubItemYPos))
    self.Bind(wx.EVT_BUTTON, self.DeleteTag, id=ID_TAG_DELETE_BUTTON)
    pubItemYPos += pubItemYPosStep*2

    ## File
    pubItemYPos += pubItemYPosStep
    wx.StaticText(panel, -1, 'Files', size=pubItemLabelSize, 
                  pos = (pubItemLabelXPos, pubItemYPos))
    self.file_form = wx.TextCtrl(panel, -1, '', size=pubItemMediumFormSize,
                  pos=(pubItemFormXPos, pubItemYPos))
    file_button = wx.Button(panel, ID_FILE_SELECT_BUTTON, 'Choose', 
                          style=wx.BU_EXACTFIT, size=pubItemSmallButtonSize, 
                          pos=(pubItemFileSelectButtonXPos, pubItemYPos))
    self.Bind(wx.EVT_BUTTON, self.OpenFile, id=ID_FILE_SELECT_BUTTON)
    add_file_button = wx.Button(panel, ID_FILE_ADD_BUTTON, 'Add', 
                          style=wx.BU_EXACTFIT, size=pubItemSmallButtonSize, 
                          pos=(pubItemFileAddButtonXPos, pubItemYPos))
    self.Bind(wx.EVT_BUTTON, self.AddFile, id=ID_FILE_ADD_BUTTON)
    
    ## File List
    pubItemYPos += pubItemYPosStep
    self.file_list_form = wx.ListCtrl(panel, -1,
                            style=wx.LC_LIST, size=pubItemListSize,
                            pos=(pubItemFormXPos, pubItemYPos))
    file_delete_button = wx.Button(panel, ID_FILE_DELETE_BUTTON, 'Delete', 
                          style=wx.BU_EXACTFIT, size=pubItemSmallButtonSize, 
                          pos=(pubItemFileAddButtonXPos, pubItemYPos))
    self.Bind(wx.EVT_BUTTON, self.DeleteFile, id=ID_FILE_DELETE_BUTTON)
    pubItemYPos += pubItemYPosStep*2
    
    ## Buttons
    submit_button = wx.Button(panel, ID_SUBMIT_BUTTON, 'Submit', 
                          style=wx.BU_EXACTFIT,
                          size=pubItemButtonSize, pos=pubItemSubmitButtonPos)
    close_button = wx.Button(panel, ID_CLOSE_BUTTON, 'Close', 
                          style=wx.BU_EXACTFIT,
                          size=pubItemButtonSize, pos=pubItemCloseButtonPos)
    self.Bind(wx.EVT_BUTTON, self.OnClose, id=ID_CLOSE_BUTTON)
    
    self.Centre()

  def OnClose(self, event):
    self.Close()
 
  def AddTag(self, event):
    if(self.tag_list.count(self.tag_form.GetValue()) == 0):
      self.tag_list.append(self.tag_form.GetValue())

    self.RefreshTagList()

  def AddFile(self, event):
    if(self.file_list.count(self.file_form.GetValue()) == 0):
      self.file_list.append(self.file_form.GetValue())

    self.RefreshFileList()

  def DeleteTag(self, event):
    for selected_tag in self.SelectedItemText(self.tag_list_form):
      self.tag_list.remove(selected_tag)
    
    self.RefreshTagList()

  def DeleteFile(self, event):
    for selected_file in self.SelectedItemText(self.file_list_form):
      self.file_list.remove(selected_file)
    
    self.RefreshFileList()

  def RefreshTagList(self):
    self.tag_list_form.DeleteAllItems()
    idx = 0
    for tag in self.tag_list:
      self.tag_list_form.InsertStringItem(idx,tag)
      idx += 1
    
  def RefreshFileList(self):
    self.file_list_form.DeleteAllItems()
    idx = 0
    for tag in self.file_list:
      self.file_list_form.InsertStringItem(idx,tag)
      idx += 1

  def SelectedItemText(self, listctrl):
    rv = []
    selected_idx = listctrl.GetFirstSelected()
    if( selected_idx < 0 ):
      return rv
    else:
      rv.append( listctrl.GetItemText(selected_idx) )
    
    while(1):
      selected_idx = listctrl.GetNextSelected(selected_idx)
      if( selected_idx < 0 ):
        break
      else:
        rv.append( listctrl.GetItemText(selected_idx) )

    return rv

  def OpenFile(self, event):
    home_path = self.conf['home_path']
    file_dialog = wx.FileDialog(self, "Shooze a file", home_path, 
                        "", "*.*", wx.OPEN)
    if( file_dialog.ShowModal() == wx.ID_OK ):
      file_path = file_dialog.GetPath()
      self.file_form.SetValue(file_path)

    file_dialog.Destroy()
    
