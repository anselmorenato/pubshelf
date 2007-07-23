import wx
import sys, os
from conf import PubShelfConf
from model_pubitem import PubItem
from model_tag import Tag
from model_link import Link

ID_SUBMIT_BUTTON = 2000
ID_DELETE_BUTTON = 2001
ID_CLOSE_BUTTON = 2002
ID_FILE_SELECT_BUTTON = 2010
ID_LINK_ADD_BUTTON = 2011
ID_LINK_DELETE_BUTTON = 2012
ID_LINK_TITLE_FORM = 2013
ID_LINK_URI_FORM = 2014
ID_LINK_LIST_CTRL = 2015
ID_TAG_ADD_BUTTON  = 2020
ID_TAG_DELETE_BUTTON  = 2021
ID_TAG_FORM = 2022

DIALOG_SIZE = wx.Size(600,600)
linkTitleWidth = 130
linkURIWidth = 310
AVAILABLE_PUB_TYPES = ['paper','book']

class PubShelfPubItemDialog(wx.Frame):
  def __init__(self, parent, id):
    wx.Frame.__init__(self, parent, id, 'PubItem', size=DIALOG_SIZE)
    panel = wx.Panel(self, -1)

    psconf = PubShelfConf()
    self.conf = psconf.item
    self.tag_list = []
    self.link_list = dict()
    self.forms = dict()

    mainSizer = wx.BoxSizer(wx.VERTICAL)

    ## ID, Nickname, PubType
    IDLabel = wx.StaticText(panel, -1, 'ID', style=wx.ALIGN_CENTER)
    self.forms['id'] = wx.StaticText(panel, -1, '', size=(30,-1), 
                                      style=wx.ALIGN_LEFT)
    nicknameLabel = wx.StaticText(panel, -1,'Nickname', style=wx.ALIGN_CENTER)
    self.forms['nickname'] = wx.StaticText(panel,-1,'', style=wx.ALIGN_LEFT)
    pubtypeLabel = wx.StaticText(panel,-1,'Pub. type', style=wx.ALIGN_CENTER)
    self.forms['pub_type'] = wx.ComboBox(panel,-1,choices=AVAILABLE_PUB_TYPES)
    self.forms['pub_type'].SetValue(AVAILABLE_PUB_TYPES[0])
    self.forms['id'].SetBackgroundColour('#aaaaaa')
    self.forms['nickname'].SetBackgroundColour('#aaaaaa')
    
    headSizer = wx.BoxSizer(wx.HORIZONTAL)
    headSizer.Add(IDLabel)
    headSizer.Add(self.forms['id'])
    headSizer.Add(nicknameLabel, wx.EXPAND)
    headSizer.Add(self.forms['nickname'], wx.EXPAND)
    headSizer.Add(pubtypeLabel, wx.EXPAND)
    headSizer.Add(self.forms['pub_type'], wx.EXPAND)
    mainSizer.Add(headSizer, 0, wx.EXPAND|wx.ALL, 10)

    ## Title, Authors, Journal, Publisher
    titleLabel = wx.StaticText(panel, -1, 'Title', style=wx.ALIGN_CENTER)
    self.forms['title'] = wx.TextCtrl(panel, -1, '')
    authorsLabel = wx.StaticText(panel, -1, 'Authors', style=wx.ALIGN_CENTER)
    self.forms['authors'] = wx.TextCtrl(panel, -1, '')
    journalLabel = wx.StaticText(panel, -1, 'Journal', style=wx.ALIGN_CENTER)
    self.forms['journal'] = wx.TextCtrl(panel, -1, '')
    publisherLabel= wx.StaticText(panel, -1, 'Publisher', style=wx.ALIGN_CENTER)
    self.forms['publisher'] = wx.TextCtrl(panel, -1, '')
    
    titleSizer = wx.FlexGridSizer(cols=2, hgap=10)
    titleSizer.AddGrowableCol(1)
    titleSizer.Add(titleLabel, 0, wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL)
    titleSizer.Add(self.forms['title'], 0, wx.EXPAND)
    titleSizer.Add(authorsLabel, 0, wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL)
    titleSizer.Add(self.forms['authors'], 0, wx.EXPAND)
    titleSizer.Add(journalLabel, 0, wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL)
    titleSizer.Add(self.forms['journal'], 0, wx.EXPAND)
    titleSizer.Add(publisherLabel, 0, wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL)
    titleSizer.Add(self.forms['publisher'], 0, wx.EXPAND)
    mainSizer.Add(titleSizer,0, wx.EXPAND|wx.ALL, 10)

    ## Volume, Page, PubYear
    volumeLabel = wx.StaticText(panel, -1, 'Volume', style=wx.ALIGN_CENTER)
    self.forms['volume'] = wx.TextCtrl(panel, -1, '')
    pageLabel = wx.StaticText(panel, -1,'Page', style=wx.ALIGN_CENTER)
    self.forms['page'] = wx.TextCtrl(panel,-1,'')
    pubyearLabel = wx.StaticText(panel,-1,'Pub. year', style=wx.ALIGN_CENTER)
    self.forms['pub_year'] = wx.TextCtrl(panel,-1,'')
    
    volumeSizer = wx.BoxSizer(wx.HORIZONTAL)
    volumeSizer.Add(volumeLabel, wx.SHAPED)
    volumeSizer.Add(self.forms['volume'], wx.SHAPED)
    volumeSizer.Add(pageLabel, wx.SHAPED)
    volumeSizer.Add(self.forms['page'], wx.SHAPED)
    volumeSizer.Add(pubyearLabel, wx.SHAPED)
    volumeSizer.Add(self.forms['pub_year'], wx.SHAPED)
    mainSizer.Add(volumeSizer, 0, wx.EXPAND|wx.ALL, 10)

    ## Tags
    tagLabel = wx.StaticText(panel, -1, 'Tags', style=wx.ALIGN_CENTER)
    self.forms['tag'] = wx.TextCtrl(panel, ID_TAG_FORM, '', 
                                  style=wx.TE_LEFT|wx.TE_PROCESS_ENTER)
    tagAddButton = wx.Button(panel, ID_TAG_ADD_BUTTON, 'Add')
    self.forms['tag_list'] = wx.ListCtrl(panel, -1, style=wx.LC_LIST)
    tagDeleteButton = wx.Button(panel, ID_TAG_DELETE_BUTTON, 'Delete')

    self.Bind(wx.EVT_BUTTON, self.AddTag, id=ID_TAG_ADD_BUTTON)
    self.Bind(wx.EVT_TEXT_ENTER, self.AddTag, id=ID_TAG_FORM)
    self.Bind(wx.EVT_BUTTON, self.DeleteTag, id=ID_TAG_DELETE_BUTTON)

    tagButtonSizer = wx.BoxSizer(wx.VERTICAL)
    tagButtonSizer.Add(tagAddButton, wx.EXPAND)
    tagButtonSizer.Add(tagDeleteButton, wx.EXPAND)

    tagSizer = wx.FlexGridSizer(cols=3, hgap=10, vgap=10)
    tagSizer.AddGrowableCol(1)
    tagSizer.Add(tagLabel, 0, wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL)
    tagSizer.Add(self.forms['tag'], 0, wx.EXPAND)
    tagSizer.Add((10,10))
    tagSizer.Add((10,10))
    tagSizer.Add(self.forms['tag_list'], 0, wx.EXPAND)
    tagSizer.Add(tagButtonSizer, 0, wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL)
    mainSizer.Add(tagSizer, 0, wx.EXPAND|wx.ALL, 10)

    ## Links
    linkLabel = wx.StaticText(panel, -1, 'Links', style=wx.ALIGN_CENTER)
    self.forms['link_title'] = wx.TextCtrl(panel, ID_LINK_TITLE_FORM, '',
                                size=(linkTitleWidth,-1),style=wx.TE_LEFT)
    self.forms['link_uri'] = wx.TextCtrl(panel, ID_LINK_URI_FORM, '', 
                                size=(linkURIWidth,-1),
                                style=wx.TE_LEFT|wx.TE_PROCESS_ENTER)
    fileBrowseButton = wx.Button(panel, ID_FILE_SELECT_BUTTON, 'File')
    linkAddButton = wx.Button(panel, ID_LINK_ADD_BUTTON, 'Add')
    self.forms['link_list'] = wx.ListCtrl(panel, ID_LINK_LIST_CTRL, style=wx.LC_REPORT)
    self.forms['link_list'].InsertColumn(0,'Title', width=linkTitleWidth)
    self.forms['link_list'].InsertColumn(1,'URI', width=linkURIWidth)
    linkDeleteButton = wx.Button(panel, ID_LINK_DELETE_BUTTON, 'Delete')
    
    self.forms['link_list'].Bind(wx.EVT_LEFT_DCLICK, self.OnDoubleClick, id=ID_LINK_LIST_CTRL )

    self.Bind(wx.EVT_BUTTON, self.OpenFile, id=ID_FILE_SELECT_BUTTON)
    self.Bind(wx.EVT_BUTTON, self.AddLink, id=ID_LINK_ADD_BUTTON)
    self.Bind(wx.EVT_TEXT_ENTER, self.AddLink, id=ID_LINK_URI_FORM)
    self.Bind(wx.EVT_BUTTON, self.DeleteLink, id=ID_LINK_DELETE_BUTTON)

    linkButtonSizer = wx.BoxSizer(wx.VERTICAL)
    linkButtonSizer.Add(linkAddButton, wx.EXPAND)
    linkButtonSizer.Add(linkDeleteButton, wx.EXPAND)

    linkFormSizer = wx.BoxSizer(wx.HORIZONTAL)
    linkFormSizer.Add(self.forms['link_title'])
    linkFormSizer.Add(self.forms['link_uri'])

    linkSizer = wx.FlexGridSizer(cols=3, hgap=10, vgap=10)
    linkSizer.AddGrowableCol(1)
    linkSizer.Add(linkLabel, 0, wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL)
    linkSizer.Add(linkFormSizer, 0, wx.EXPAND)
    linkSizer.Add(fileBrowseButton, 0, wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL)
    linkSizer.Add((10,10))
    linkSizer.Add(self.forms['link_list'], 0, wx.EXPAND)
    linkSizer.Add(linkButtonSizer, 0, wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL)
    mainSizer.Add(linkSizer, 0, wx.EXPAND|wx.ALL, 10)

    ## Buttons
    submitButton = wx.Button(panel, ID_SUBMIT_BUTTON, 'Submit')
    deleteButton = wx.Button(panel, ID_DELETE_BUTTON, 'Delete')
    closeButton = wx.Button(panel, ID_CLOSE_BUTTON, 'Close')
    self.Bind(wx.EVT_BUTTON, self.OnSubmit, id=ID_SUBMIT_BUTTON)
    self.Bind(wx.EVT_BUTTON, self.OnDelete, id=ID_DELETE_BUTTON)
    self.Bind(wx.EVT_BUTTON, self.OnClose, id=ID_CLOSE_BUTTON)
    
    buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
    buttonSizer.Add((10,10), wx.EXPAND)
    buttonSizer.Add(submitButton, wx.EXPAND)
    buttonSizer.Add(deleteButton, wx.EXPAND)
    buttonSizer.Add(closeButton, wx.EXPAND)
    buttonSizer.Add((10,10), wx.EXPAND)
    mainSizer.Add(buttonSizer, 0, wx.EXPAND|wx.ALL, 10)
    
    panel.SetSizer(mainSizer)
    self.Centre()

  def SetPubItem(self, pubitem):
    self.forms['id'].SetLabel( "%d" % pubitem.id )
    self.forms['nickname'].SetLabel( pubitem.nickname )
    self.forms['title'].SetValue( pubitem.title )
    self.forms['authors'].SetValue( pubitem.authors )
    self.forms['journal'].SetValue( pubitem.journal )
    self.forms['publisher'].SetValue( pubitem.publisher )
    self.forms['volume'].SetValue( pubitem.volume )
    self.forms['page'].SetValue( pubitem.page )
    self.forms['pub_year'].SetValue( "%d" % pubitem.pub_year )

    for tag in pubitem.tags:
      self.tag_list.append("%s/%s" % (tag.category, tag.name))

    for link in pubitem.links:
      self.link_list[link.name] = link.uri
    
    self.RefreshTagList()
    self.RefreshLinkList()

  def OnClose(self, event):
    self.Close()

  def OnDelete(self, event):
    pubitem = PubItem()
    pubitem.id = int(self.forms['id'].GetLabel())
    if( pubitem.id ): 
      pubitem.id = int(pubitem.id)
      pubitem.delete()
      self.GetParent().itemList.remove_by_pubitem_id(pubitem.id)
      self.GetParent().itemList.Refresh()
      self.GetParent().itemContent.SetBlank()
      self.GetParent().tree.Refresh()
      self.Close()
    
  def OnSubmit(self, event):
    pubitem = PubItem()
    pubitem.id = self.forms['id'].GetLabel()
    if( pubitem.id ): pubitem.id = int(pubitem.id)
    pubitem.nickname = self.forms['nickname'].GetLabel()
    pubitem.pub_type = self.forms['pub_type'].GetValue()
    pubitem.title = self.forms['title'].GetValue()
    pubitem.authors = self.forms['authors'].GetValue()
    pubitem.journal = self.forms['journal'].GetValue()
    pubitem.publisher = self.forms['publisher'].GetValue()
    pubitem.volume = self.forms['volume'].GetValue()
    pubitem.page = self.forms['page'].GetValue()
    pubitem.pub_year = self.forms['pub_year'].GetValue()
    if(pubitem.pub_year): pubitem.pub_year = int(pubitem.pub_year)

    for tag_raw in self.tag_list:
      (category, name) = tag_raw.split('/',1)
      pubitem.tags.append( Tag(category=category,name=name) )

    for name, uri in self.link_list.iteritems():
      pubitem.links.append( Link(name=name, uri=uri) )

    if( pubitem.id and pubitem.nickname):
      pubitem.update()
    else:
      pubitem.insert()
    
    self.GetParent().itemContent.SetPubItem(pubitem)
    self.GetParent().tree.Refresh()
    self.Close()
 
  def AddTag(self, event):
    tag_raw = self.forms['tag'].GetValue()
    if( tag_raw.find('/') < 0 ): tag_raw = '/'+tag_raw
    if(self.tag_list.count(tag_raw) == 0):
      self.tag_list.append(tag_raw)
    self.forms['tag'].SetValue('')
    self.RefreshTagList()
  
  def DeleteTag(self, event):
    for selected_tag in self.SelectedItemText(self.forms['tag_list']):
      self.tag_list.remove(selected_tag)
    self.RefreshTagList()

  def AddLink(self, event):
    linkTitle = self.forms['link_title'].GetValue()
    linkURI = self.forms['link_uri'].GetValue()
    if( linkTitle != '' and linkURI != '' ):
      if( not self.link_list.has_key(linkTitle) ):
        self.link_list[linkTitle] = linkURI
        self.forms['link_title'].SetValue('')
        self.forms['link_uri'].SetValue('')
        self.forms['link_list'].Append( [linkTitle, linkURI] )

  def OnDoubleClick(self, event):
    listctrl = self.forms['link_list']
    selected_idx = listctrl.GetFocusedItem()

    self.forms['link_title'].SetValue(listctrl.GetItem(selected_idx,0).GetText())
    self.forms['link_uri'].SetValue(listctrl.GetItem(selected_idx,1).GetText())

  def DeleteLink(self, event):
    for selected_link in self.SelectedItemText(self.forms['link_list']):
      del self.link_list[selected_link]
    self.RefreshLinkList()

  def RefreshTagList(self):
    self.forms['tag_list'].DeleteAllItems()
    idx = 0
    for item in self.tag_list:
      self.forms['tag_list'].InsertStringItem(idx,item)
      idx += 1
  
  def RefreshLinkList(self):
    self.forms['link_list'].DeleteAllItems()
    for title, uri in self.link_list.iteritems():
      self.forms['link_list'].Append( [title, uri] )

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
    file_dialog = wx.FileDialog(self, "Shooze a file", self.conf['dir_file'],
                        "", "*.*", wx.OPEN)
    if( file_dialog.ShowModal() == wx.ID_OK ):
      file_path = file_dialog.GetPath()
      self.forms['link_uri'].SetValue(file_path)
    file_dialog.Destroy()
