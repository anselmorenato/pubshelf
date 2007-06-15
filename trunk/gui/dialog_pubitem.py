import wx, wx.html
import sys, os
sys.path.append('../libpy/')
from data import *

ID_SUBMIT_BUTTON = 2000
ID_CLOSE_BUTTON = 2001
ID_FILE_SELECT_BUTTON = 2010
ID_URI_ADD_BUTTON = 2011
ID_URI_DELETE_BUTTON = 2012
ID_TAG_ADD_BUTTON  = 2020
ID_TAG_DELETE_BUTTON  = 2021
AVAILABLE_PUB_TYPES = ['paper','book']

pubItemDialogSize = (600,600)
pubItemLabelSize = (90,25)
pubItemLargeFormSize = (490,25)
pubItemSmallFormSize = (200,25)
pubItemMediumFormSize = (350,25)
pubItemListSize = (420,75)
pubItemLabelXPos = 10
pubItemFormXPos  = 100
pubItemButton1XPos = 460
pubItemButton2XPos = 530
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
    self.uri_list = []

    panel = wx.Panel(self, -1)

    ## Basic elements
    self.forms = dict()

    labels = ['ID','Nickname','Pub type','Title','Authors','Journal',
              'Publisher','Volume','Page','Pub Year']
    form_size = { 'ID':pubItemSmallFormSize, 
                  'Nickname':pubItemSmallFormSize,
                  'Pub type':pubItemSmallFormSize,
                  'Title':pubItemLargeFormSize,
                  'Authors':pubItemLargeFormSize,
                  'Journal':pubItemLargeFormSize,
                  'Publisher':pubItemLargeFormSize,
                  'Volume':pubItemSmallFormSize,
                  'Page':pubItemSmallFormSize,
                  'Pub Year':pubItemSmallFormSize
                  }
    form_type = { 'ID':'StaticText', 'Nickname':'StaticText', 
                  'Pub type':'ComboBox', 'Title':'TextCtrl',
                  'Authors':'TextCtrl', 'Journal':'TextCtrl',
                  'Publisher':'TextCtrl', 'Volume':'TextCtrl',
                  'Page':'TextCtrl', 'Pub Year':'TextCtrl'
                  }

    pubItemYPos = pubItemYPosInit
    for label in labels:
      wx.StaticText(panel, -1, label, size=pubItemLabelSize, 
                      pos = (pubItemLabelXPos, pubItemYPos))
      if(label == 'Pub type'):
        self.forms[label] = wx.ComboBox(panel, -1, choices=AVAILABLE_PUB_TYPES,
                              size=form_size[label], style=wx.CB_READONLY,
                              pos=(pubItemFormXPos, pubItemYPos))
        self.forms[label].SetValue(AVAILABLE_PUB_TYPES[0])
      elif(form_type[label] == 'StaticText'):
        self.forms[label] = wx.StaticText(panel, -1, '', 
                              size=form_size[label],
                              pos = (pubItemFormXPos, pubItemYPos))
      elif(form_type[label] == 'TextCtrl'):
        self.forms[label] = wx.TextCtrl(panel, -1, '', 
                              size=form_size[label],
                              pos=(pubItemFormXPos, pubItemYPos))
      pubItemYPos += pubItemYPosStep

    ## Tag
    wx.StaticText(panel, -1, 'Tags', size=pubItemLabelSize, 
                  pos = (pubItemLabelXPos, pubItemYPos))
    self.tag_form = wx.TextCtrl(panel, -1, '', size=pubItemMediumFormSize,
                      pos=(pubItemFormXPos, pubItemYPos))
    wx.Button(panel, ID_TAG_ADD_BUTTON, 'Add', 
                  style=wx.BU_EXACTFIT, size=pubItemSmallButtonSize, 
                  pos=(pubItemButton1XPos, pubItemYPos))
    self.Bind(wx.EVT_BUTTON, self.AddTag, id=ID_TAG_ADD_BUTTON)

    ## Tag List
    pubItemYPos += pubItemYPosStep
    self.tag_list_form = wx.ListCtrl(panel, -1,
                            style=wx.LC_LIST, size=pubItemListSize,
                            pos=(pubItemFormXPos, pubItemYPos))
    wx.Button(panel, ID_TAG_DELETE_BUTTON, 'Delete', 
                          style=wx.BU_EXACTFIT, size=pubItemSmallButtonSize, 
                          pos=(pubItemButton2XPos, pubItemYPos))
    self.Bind(wx.EVT_BUTTON, self.DeleteTag, id=ID_TAG_DELETE_BUTTON)
    pubItemYPos += pubItemYPosStep*2

    ## URI
    pubItemYPos += pubItemYPosStep
    wx.StaticText(panel, -1, 'URIs', size=pubItemLabelSize, 
                  pos = (pubItemLabelXPos, pubItemYPos))
    self.uri_form = wx.TextCtrl(panel, -1, '', size=pubItemMediumFormSize,
                  pos=(pubItemFormXPos, pubItemYPos))
    wx.Button(panel, ID_FILE_SELECT_BUTTON, 'File', 
                  style=wx.BU_EXACTFIT, size=pubItemSmallButtonSize, 
                  pos=(pubItemButton1XPos, pubItemYPos))
    self.Bind(wx.EVT_BUTTON, self.OpenFile, id=ID_FILE_SELECT_BUTTON)
    wx.Button(panel, ID_URI_ADD_BUTTON, 'Add', 
                  style=wx.BU_EXACTFIT, size=pubItemSmallButtonSize, 
                  pos=(pubItemButton2XPos, pubItemYPos))
    self.Bind(wx.EVT_BUTTON, self.AddURI, id=ID_URI_ADD_BUTTON)
    
    ## URI List
    pubItemYPos += pubItemYPosStep
    self.uri_list_form = wx.ListCtrl(panel, -1,
                            style=wx.LC_LIST, size=pubItemListSize,
                            pos=(pubItemFormXPos, pubItemYPos))
    wx.Button(panel, ID_URI_DELETE_BUTTON, 'Delete', 
                   style=wx.BU_EXACTFIT, size=pubItemSmallButtonSize, 
                   pos=(pubItemButton2XPos, pubItemYPos))
    self.Bind(wx.EVT_BUTTON, self.DeleteURI, id=ID_URI_DELETE_BUTTON)
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

  def SetPubItem(self, pubitem):
    self.forms['ID'].SetLabel( "%d" % pubitem.id )
    self.forms['Nickname'].SetLabel( pubitem.nickname )
    self.forms['Title'].SetValue( pubitem.title )
    self.forms['Authors'].SetValue( pubitem.authors )
    self.forms['Journal'].SetValue( pubitem.journal )
    self.forms['Publisher'].SetValue( pubitem.publisher )
    self.forms['Volume'].SetValue( pubitem.volume )
    self.forms['Page'].SetValue( pubitem.page )
    self.forms['Pub Year'].SetValue( "%d" % pubitem.pub_year )
    for tag in pubitem.tags:
      self.tag_list.append("%s::%s" % (tag.category, tag.name))
    for link in pubitem.links:
      self.uri_list.append("%s" % link.uri)
    
    self.RefreshList(self.tag_list, self.tag_list_form)
    self.RefreshList(self.uri_list, self.uri_list_form)

  def OnClose(self, event):
    self.Close()
 
  def AddTag(self, event):
    if(self.tag_list.count(self.tag_form.GetValue()) == 0):
      self.tag_list.append(self.tag_form.GetValue())
    self.RefreshList(self.tag_list, self.tag_list_form)
  
  def DeleteTag(self, event):
    for selected_tag in self.SelectedItemText(self.tag_list_form):
      self.tag_list.remove(selected_tag)
    self.RefreshList(self.tag_list, self.tag_list_form)

  def AddURI(self, event):
    if(self.uri_list.count(self.uri_form.GetValue()) == 0):
      self.uri_list.append(self.uri_form.GetValue())
    self.RefreshList(self.uri_list, self.uri_list_form)

  def DeleteURI(self, event):
    for selected_uri in self.SelectedItemText(self.uri_list_form):
      self.uri_list.remove(selected_uri)
    self.RefreshList(self.uri_list, self.uri_list_form)

  def RefreshList(self,list,list_form):
    list_form.DeleteAllItems()
    idx = 0
    for item in list:
      list_form.InsertStringItem(idx,item)
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
      rv.append( listctrl.GetItemText(selected_idx) )

    return rv

  def OpenFile(self, event):
    home_path = self.conf['home_path']
    file_dialog = wx.FileDialog(self, "Shooze a file", home_path, 
                        "", "*.*", wx.OPEN)
    if( file_dialog.ShowModal() == wx.ID_OK ):
      file_path = file_dialog.GetPath()
      self.uri_form.SetValue(file_path)

    file_dialog.Destroy()
    
