import wx, wx.html
import sys, os
from conf import PubShelfConf
from model_pubitem import PubItem
from model_tag import Tag
from model_link import Link

ID_SUBMIT_BUTTON = 2000
ID_CLOSE_BUTTON = 2001
ID_FILE_SELECT_BUTTON = 2010
ID_LINK_ADD_BUTTON = 2011
ID_LINK_DELETE_BUTTON = 2012
ID_LINK_TITLE_FORM = 2013
ID_LINK_URI_FORM = 2014
ID_TAG_ADD_BUTTON  = 2020
ID_TAG_DELETE_BUTTON  = 2021
ID_TAG_FORM = 2022

DIALOG_SIZE = wx.Size(600,600)
linkTitleWidth = 130
linkURIWidth = 310
AVAILABLE_PUB_TYPES = ['paper','book']

class PubShelfPubItemDialog(wx.Dialog):
  def __init__(self, parent, id):
    wx.Dialog.__init__(self, parent, id, 'PubItem', size=DIALOG_SIZE)
    panel = wx.Panel(self, -1)

    psconf = PubShelfConf()
    self.conf = psconf.item
    self.tag_list = []
    self.link_list = dict()
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

    ## Tags
    tagLabel = wx.StaticText(panel, -1, 'Tags', style=wx.ALIGN_CENTER)
    self.forms['Tag'] = wx.TextCtrl(panel, ID_TAG_FORM, '', 
                                  style=wx.TE_LEFT|wx.TE_PROCESS_ENTER)
    tagAddButton = wx.Button(panel, ID_TAG_ADD_BUTTON, 'Add')
    self.forms['TagList'] = wx.ListCtrl(panel, -1, style=wx.LC_LIST)
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
    tagSizer.Add(self.forms['Tag'], 0, wx.EXPAND)
    tagSizer.Add((10,10))
    tagSizer.Add((10,10))
    tagSizer.Add(self.forms['TagList'], 0, wx.EXPAND)
    tagSizer.Add(tagButtonSizer, 0, wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL)
    mainSizer.Add(tagSizer, 0, wx.EXPAND|wx.ALL, 10)

    ## Links
    linkLabel = wx.StaticText(panel, -1, 'Links', style=wx.ALIGN_CENTER)
    self.forms['LinkTitle'] = wx.TextCtrl(panel, ID_LINK_TITLE_FORM, '',
                                size=(linkTitleWidth,-1),style=wx.TE_LEFT)
    self.forms['LinkURI'] = wx.TextCtrl(panel, ID_LINK_URI_FORM, '', 
                                size=(linkURIWidth,-1),
                                style=wx.TE_LEFT|wx.TE_PROCESS_ENTER)
    fileBrowseButton = wx.Button(panel, ID_FILE_SELECT_BUTTON, 'File')
    linkAddButton = wx.Button(panel, ID_LINK_ADD_BUTTON, 'Add')
    self.forms['LinkList'] = wx.ListCtrl(panel, -1, style=wx.LC_REPORT)
    self.forms['LinkList'].InsertColumn(0,'Title', width=linkTitleWidth)
    self.forms['LinkList'].InsertColumn(1,'URI', width=linkURIWidth)
    linkDeleteButton = wx.Button(panel, ID_LINK_DELETE_BUTTON, 'Delete')

    self.Bind(wx.EVT_BUTTON, self.OpenFile, id=ID_FILE_SELECT_BUTTON)
    self.Bind(wx.EVT_BUTTON, self.AddLink, id=ID_LINK_ADD_BUTTON)
    self.Bind(wx.EVT_TEXT_ENTER, self.AddLink, id=ID_LINK_URI_FORM)
    self.Bind(wx.EVT_BUTTON, self.DeleteLink, id=ID_LINK_DELETE_BUTTON)

    linkButtonSizer = wx.BoxSizer(wx.VERTICAL)
    linkButtonSizer.Add(linkAddButton, wx.EXPAND)
    linkButtonSizer.Add(linkDeleteButton, wx.EXPAND)

    linkFormSizer = wx.BoxSizer(wx.HORIZONTAL)
    linkFormSizer.Add(self.forms['LinkTitle'])
    linkFormSizer.Add(self.forms['LinkURI'])

    linkSizer = wx.FlexGridSizer(cols=3, hgap=10, vgap=10)
    linkSizer.AddGrowableCol(1)
    linkSizer.Add(linkLabel, 0, wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL)
    linkSizer.Add(linkFormSizer, 0, wx.EXPAND)
    linkSizer.Add(fileBrowseButton, 0, wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL)
    linkSizer.Add((10,10))
    linkSizer.Add(self.forms['LinkList'], 0, wx.EXPAND)
    linkSizer.Add(linkButtonSizer, 0, wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL)
    mainSizer.Add(linkSizer, 0, wx.EXPAND|wx.ALL, 10)

    ## Buttons
    submitButton = wx.Button(panel, ID_SUBMIT_BUTTON, 'Submit')
    closeButton = wx.Button(panel, ID_CLOSE_BUTTON, 'Close')
    self.Bind(wx.EVT_BUTTON, self.OnSubmit, id=ID_SUBMIT_BUTTON)
    self.Bind(wx.EVT_BUTTON, self.OnClose, id=ID_CLOSE_BUTTON)
    
    buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
    buttonSizer.Add((10,10), wx.EXPAND)
    buttonSizer.Add(submitButton, wx.EXPAND)
    buttonSizer.Add(closeButton, wx.EXPAND)
    buttonSizer.Add((10,10), wx.EXPAND)
    mainSizer.Add(buttonSizer, 0, wx.EXPAND|wx.ALL, 10)
    
    panel.SetSizer(mainSizer)
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
    self.forms['PubYear'].SetValue( "%d" % pubitem.pub_year )

    for tag in pubitem.tags:
      self.tag_list.append("%s/%s" % (tag.category, tag.name))

    for link in pubitem.links:
      self.link_list[link.name] = link.uri
    
    self.RefreshTagList()
    self.RefreshLinkList()

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
    pubitem.pub_year = self.forms['PubYear'].GetValue()
    if(pubitem.pub_year): pubitem.pub_year = int(pubitem.pub_year)

    for tag_raw in self.tag_list:
      (category, name) = tag_raw.split('/')
      pubitem.tags.append( Tag(category=category,name=name) )

    for name, uri in self.link_list.iteritems():
      pubitem.links.append( Link(name=name, uri=uri) )

    if( pubitem.title ):
      pubitem.insert()
      self.GetParent().Refresh()
    self.Close()
 
  def AddTag(self, event):
    if(self.tag_list.count(self.forms['Tag'].GetValue()) == 0):
      self.tag_list.append(self.forms['Tag'].GetValue())
    self.forms['Tag'].SetValue('')
    self.RefreshTagList()
  
  def DeleteTag(self, event):
    for selected_tag in self.SelectedItemText(self.forms['TagList']):
      self.tag_list.remove(selected_tag)
    self.RefreshTagList()

  def AddLink(self, event):
    linkTitle = self.forms['LinkTitle'].GetValue()
    linkURI = self.forms['LinkURI'].GetValue()
    if( linkTitle != '' and linkURI != '' ):
      if( not self.link_list.has_key(linkTitle) ):
        self.link_list[linkTitle] = linkURI
        self.forms['LinkTitle'].SetValue('')
        self.forms['LinkURI'].SetValue('')
        self.forms['LinkList'].Append( [linkTitle, linkURI] )

  def DeleteLink(self, event):
    linkTitle = event.GetItem().GetText()
    del link_list[linkTitle]
    self.RefreshLinkList()

  def RefreshTagList(self):
    self.forms['TagList'].DeleteAllItems()
    idx = 0
    for item in self.tag_list:
      self.forms['TagList'].InsertStringItem(idx,item)
      idx += 1
  
  def RefreshLinkList(self):
    self.forms['LinkList'].DeleteAllItems()
    for title, uri in self.link_list.iteritems():
      self.forms['LinkList'].Append( [linkTitle,linkURI] )

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
      self.forms['LinkURI'].SetValue(file_path)
    file_dialog.Destroy()
