import wx, wx.html
import sys, os
from conf import PubShelfConf
from model_pubitem import PubItem
from model_tag import Tag
from model_link import Link

ID_SUBMIT_BUTTON = 2000
ID_CLOSE_BUTTON = 2001
ID_FILE_SELECT_BUTTON = 2010
ID_URI_ADD_BUTTON = 2011
ID_URI_DELETE_BUTTON = 2012
ID_URI_FORM = 2013
ID_TAG_ADD_BUTTON  = 2020
ID_TAG_DELETE_BUTTON  = 2021
ID_TAG_FORM = 2022

DIALOG_SIZE = wx.Size(600,600)
AVAILABLE_PUB_TYPES = ['paper','book']

class PubShelfPubItemDialog(wx.Dialog):
  def __init__(self, parent, id):
    wx.Dialog.__init__(self, parent, id, 'PubItem', size=DIALOG_SIZE)
    panel = wx.Panel(self, -1)

    psconf = PubShelfConf()
    self.conf = psconf.item
    self.tag_list = []
    self.uri_list = []
    self.forms = dict()

    mainSizer = wx.BoxSizer(wx.VERTICAL)

    ## ID, Nickname, PubType
    IDLabel = wx.StaticText(panel, -1, 'ID', style=wx.ALIGN_RIGHT)
    self.forms['ID'] = wx.StaticText(panel, -1, '', style=wx.ALIGN_CENTER)
    nicknameLabel = wx.StaticText(panel, -1,'Nickname', style=wx.ALIGN_RIGHT)
    self.forms['Nickname'] = wx.StaticText(panel,-1,'', style=wx.ALIGN_CENTER)
    pubtypeLabel = wx.StaticText(panel,-1,'Pub. type', style=wx.ALIGN_RIGHT)
    self.forms['PubType'] = wx.ComboBox(panel,-1,choices=AVAILABLE_PUB_TYPES)
    self.forms['PubType'].SetValue(AVAILABLE_PUB_TYPES[0])
    
    headSizer = wx.BoxSizer(wx.HORIZONTAL)
    headSizer.Add(IDLabel, wx.SHAPED, 10)
    headSizer.Add(self.forms['ID'], wx.SHAPED)
    headSizer.Add(nicknameLabel, wx.SHAPED, 10)
    headSizer.Add(self.forms['Nickname'], wx.SHAPED)
    headSizer.Add(pubtypeLabel, wx.SHAPED, 10)
    headSizer.Add(self.forms['PubType'], wx.SHAPED, 10)
    mainSizer.Add(headSizer, 0, wx.EXPAND|wx.ALL, 10)

    ## Title, Authors, Journal, Publisher
    titleLabel = wx.StaticText(panel, -1, 'Title', style=wx.ALIGN_CENTER)
    self.forms['Title'] = wx.TextCtrl(panel, -1, '')
    authorsLabel = wx.StaticText(panel, -1, 'Authors', style=wx.ALIGN_CENTER)
    self.forms['Authors'] = wx.TextCtrl(panel, -1, '')
    journalLabel = wx.StaticText(panel, -1, 'Journal', style=wx.ALIGN_CENTER)
    self.forms['Journal'] = wx.TextCtrl(panel, -1, '')
    publisherLabel= wx.StaticText(panel, -1, 'Publisher', style=wx.ALIGN_CENTER)
    self.forms['Publisher'] = wx.TextCtrl(panel, -1, '')
    
    titleSizer = wx.FlexGridSizer(cols=2, hgap=10)
    titleSizer.AddGrowableCol(1)
    titleSizer.Add(titleLabel, 0, wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL)
    titleSizer.Add(self.forms['Title'], 0, wx.EXPAND)
    titleSizer.Add(authorsLabel, 0, wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL)
    titleSizer.Add(self.forms['Authors'], 0, wx.EXPAND)
    titleSizer.Add(journalLabel, 0, wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL)
    titleSizer.Add(self.forms['Journal'], 0, wx.EXPAND)
    titleSizer.Add(publisherLabel, 0, wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL)
    titleSizer.Add(self.forms['Publisher'], 0, wx.EXPAND)
    mainSizer.Add(titleSizer,0, wx.EXPAND|wx.ALL, 10)

    ## Volume, Page, PubYear
    volumeLabel = wx.StaticText(panel, -1, 'Volume', style=wx.ALIGN_CENTER)
    self.forms['Volume'] = wx.TextCtrl(panel, -1, '')
    pageLabel = wx.StaticText(panel, -1,'Page', style=wx.ALIGN_CENTER)
    self.forms['Page'] = wx.TextCtrl(panel,-1,'')
    pubyearLabel = wx.StaticText(panel,-1,'Pub. year', style=wx.ALIGN_CENTER)
    self.forms['PubYear'] = wx.TextCtrl(panel,-1,'')
    
    volumeSizer = wx.BoxSizer(wx.HORIZONTAL)
    volumeSizer.Add(volumeLabel, wx.SHAPED)
    volumeSizer.Add(self.forms['Volume'], wx.SHAPED)
    volumeSizer.Add(pageLabel, wx.SHAPED)
    volumeSizer.Add(self.forms['Page'], wx.SHAPED)
    volumeSizer.Add(pubyearLabel, wx.SHAPED)
    volumeSizer.Add(self.forms['PubYear'], wx.SHAPED)
    mainSizer.Add(volumeSizer, 0, wx.EXPAND|wx.ALL, 10)

    tagLabel = wx.StaticText(panel, -1, 'Tags', style=wx.ALIGN_CENTER)
    self.forms['Tag'] = wx.TextCtrl(panel, ID_TAG_FORM, '', 
                                  style=wx.TE_LEFT|wx.TE_PROCESS_ENTER)
    tagAddButton = wx.Button(panel, ID_TAG_ADD_BUTTON, 'Add')
    #self.Bind(wx.EVT_BUTTON, self.AddTag, id=ID_TAG_ADD_BUTTON)
    #self.Bind(wx.EVT_TEXT_ENTER, self.AddTag, id=ID_TAG_FORM)
    self.forms['TagList'] = wx.ListCtrl(panel, -1, style=wx.LC_LIST)
    tagDeleteButton = wx.Button(panel, ID_TAG_DELETE_BUTTON, 'Delete')
    #self.Bind(wx.EVT_BUTTON, self.DeleteTag, id=ID_TAG_DETELE_BUTTON)

    listSizer = wx.FlexGridSizer(cols=3, hgap=10, vgap=10)
    listSizer.AddGrowableCol(1)
    listSizer.Add(tagLabel, 0, wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL)
    listSizer.Add(self.forms['Tag'], 0, wx.EXPAND)
    listSizer.Add(tagAddButton, 0, wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL)
    listSizer.Add((10,10))
    listSizer.Add(self.forms['TagList'], 0, wx.EXPAND)
    listSizer.Add(tagDeleteButton, 0, wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL)
    mainSizer.Add(listSizer, 0, wx.EXPAND|wx.ALL, 10)

    ## Buttons
    submit_button = wx.Button(panel, ID_SUBMIT_BUTTON, 'Submit')
    close_button = wx.Button(panel, ID_CLOSE_BUTTON, 'Close')
    self.Bind(wx.EVT_BUTTON, self.OnSubmit, id=ID_SUBMIT_BUTTON)
    self.Bind(wx.EVT_BUTTON, self.OnClose, id=ID_CLOSE_BUTTON)
    
    buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
    buttonSizer.Add((10,10))
    buttonSizer.Add(submit_button)
    buttonSizer.Add(closeButton)
    buttonSizer.Add((10,10))
    mainSizer.Add(buttonSizer, 0, wx.EXPAND|wx.ALL, 10)
    
    panel.SetSizer(mainSizer)
    self.Centre()

'''
    ## URI
    pubItemYPos += pubItemYPosStep
    wx.StaticText(panel, -1, 'URIs', size=pubItemLabelSize, 
                  pos = (pubItemLabelXPos, pubItemYPos))
    self.uri_form = wx.TextCtrl(panel, ID_URI_FORM, '', 
                  size=pubItemMediumFormSize,
                  pos=(pubItemFormXPos, pubItemYPos),
                  style=wx.TE_LEFT|wx.TE_PROCESS_ENTER )
    wx.Button(panel, ID_FILE_SELECT_BUTTON, 'File', 
                  style=wx.BU_EXACTFIT, size=pubItemSmallButtonSize, 
                  pos=(pubItemButton1XPos, pubItemYPos))
    self.Bind(wx.EVT_BUTTON, self.OpenFile, id=ID_FILE_SELECT_BUTTON)
    wx.Button(panel, ID_URI_ADD_BUTTON, 'Add', 
                  style=wx.BU_EXACTFIT, size=pubItemSmallButtonSize, 
                  pos=(pubItemButton2XPos, pubItemYPos))
    self.Bind(wx.EVT_BUTTON, self.AddURI, id=ID_URI_ADD_BUTTON)
    self.Bind(wx.EVT_TEXT_ENTER, self.AddURI, id=ID_URI_FORM)
    
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
''' 
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
      self.uri_list.append("%s::%s" % (link.name, link.uri))
    
    self.RefreshList(self.tag_list, self.tag_list_form)
    self.RefreshList(self.uri_list, self.uri_list_form)

  def OnClose(self, event):
    self.Close()

  def OnSubmit(self, event):
    pubitem = PubItem()
    pubitem.id = self.forms['ID'].GetLabel()
    pubitem.nickname = self.forms['Nickname'].GetLabel()
    pubitem.pub_type = self.forms['Pub type'].GetValue()
    pubitem.title = self.forms['Title'].GetValue()
    pubitem.authors = self.forms['Authors'].GetValue()
    pubitem.journal = self.forms['Journal'].GetValue()
    pubitem.publisher = self.forms['Publisher'].GetValue()
    pubitem.volume = self.forms['Volume'].GetValue()
    pubitem.page = self.forms['Page'].GetValue()
    pubitem.pub_year = self.forms['Pub Year'].GetValue()
    if(pubitem.pub_year): pubitem.pub_year = int(pubitem.pub_year)

    for tag_raw in self.tag_list:
      (category, name) = tag_raw.split('::')
      pubitem.tags.append( Tag(category=category,name=name) )

    for link_raw in self.uri_list:
      (name, uri) = link_raw.split('::')
      pubitem.links.append( Link(name=name, uri=uri) )

    if( pubitem.title ):
      pubitem.insert()
      self.GetParent().Refresh()
    self.Close()
 
  def AddTag(self, event):
    if(self.tag_list.count(self.tag_form.GetValue()) == 0):
      self.tag_list.append(self.tag_form.GetValue())
    self.tag_form.SetValue('')
    self.RefreshList(self.tag_list, self.tag_list_form)
  
  def DeleteTag(self, event):
    for selected_tag in self.SelectedItemText(self.tag_list_form):
      self.tag_list.remove(selected_tag)
    self.RefreshList(self.tag_list, self.tag_list_form)

  def AddURI(self, event):
    if(self.uri_list.count(self.uri_form.GetValue()) == 0):
      self.uri_list.append(self.uri_form.GetValue())
    self.uri_form.SetValue('')
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
