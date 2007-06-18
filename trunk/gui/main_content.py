import wx
import wx.html
import os, re
from conf import PubShelfConf

LabelSize = (100,15)
initXPos = 10

class PubShelfItemContent(wx.Panel):
  def __init__(self, parent, id):
    super(PubShelfItemContent, self).__init__(parent, id)
    psconf = PubShelfConf()
    self.conf = psconf.item

  def set_pubitem(self, pubitem):
    currentYPos = 10
    currentPos = (initXPos, currentYPos)
    label_citation = wx.StaticText(self, -1, 'Citation', 
                                size=LabelSize, pos=currentPos)
    
    currentYPos += label_citation.GetSize().y
    currentPos = (initXPos, currentYPos)
    textctrl_citation = wx.TextCtrl(self,-1,pubitem.get_citation(), 
                  size=(self.GetSize().x-initXPos*2,-1), 
                  pos=currentPos, style=wx.TE_READONLY|wx.TE_MULTILINE)
    
    currentYPos += textctrl_citation.GetSize().y
    currentPos = (initXPos, currentYPos)
    label_link = wx.StaticText(self, -1, 'Links', size=LabelSize,pos=currentPos)

    link_list = []
    for link in pubitem.links:
      link_list.append(link.uri)

    currentYPos += label_link.GetSize().y
    currentPos = (initXPos, currentYPos)
    listbox_link = wx.ListBox(self, -1, choices=link_list,
                      size=(self.GetSize().x-initXPos*2, -1), pos=currentPos)

    currentYPos += listbox_link.GetSize().y
    currentPos = (initXPos, currentYPos)
    label_tag = wx.StaticText(self, -1, 'Tags', size=LabelSize,pos=currentPos)

    tag_list = []
    for tag in pubitem.tags:
      tag_list.append( tag.category+'::'+tag.name )
    
    currentYPos += label_tag.GetSize().y
    currentPos = (initXPos, currentYPos)
    listctrl_tag = wx.ListCtrl(self, -1, style=wx.LC_LIST, 
                      size=(self.GetSize().x-initXPos*2, -1), pos=currentPos)
    self.RefreshListCtrl(tag_list, listctrl_tag)

  def Refresh(self):
    pass

  def RefreshListCtrl(self, list, list_form):
    list_form.DeleteAllItems()
    idx = 0
    for item in list:
      list_form.InsertStringItem(idx, item)
      idx += 1

  def OnLinkClicked(self, link):
    uri = link.GetHref()
    re_filepath = re.compile('^file://')
    re_filetype = re.compile('.([a-z]+)$')
    if( re_filepath.match(uri) ):
      file_type = re_filetype.search(uri).group(1)
      file_path = re_filepath.sub('', uri)
      if( file_type == 'pdf' ):
        os.system(self.conf['apps']['pdf']+' '+file_path)
      else:
        os.system(self.conf['apps']['html']+' '+uri)
    else:
      os.system(self.conf['apps']['html']+' '+uri)
