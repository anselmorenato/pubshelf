import wx
import wx.html
import os, re
from conf import PubShelfConf

LabelSize = (100,15)

class PubShelfItemContent(wx.html.HtmlWindow):
  def __init__(self, parent, id):
    window_style = wx.html.HW_SCROLLBAR_AUTO
    super(PubShelfItemContent, self).__init__(parent, id, 
                                              style=window_style)
    psconf = PubShelfConf()
    self.conf = psconf.item
    if 'gtk2' in wx.PlatformInfo:
      self.SetStandardFonts()

  def set_pubitem(self, pubitem):
    rv = "<TABLE><TR><TD BGCOLOR='blue'>"
    rv += "<FONT COLOR='white'><B>Citation</B></FONT></TD></TR>"
    rv += "<TR><TD>"+pubitem.get_html_citation()+"</TD></TR>"

    rv += "<TR><TD BGCOLOR='blue'><FONT color='white'><b>Tags</b></FONT>"
    rv += "</TD></TR><TR><TD>"
    for tag in pubitem.tags:
      rv += "%s/%s," % (tag.category, tag.name)
    rv += "</TD></TR>"

    rv += "<TR><TD BGCOLOR='blue'><font color='white'><b>Links</b></font>"
    rv += "</TD></TR><TR><TD><UL>"
    for link in pubitem.links:
      rv += "<LI><A HREF='%s'>%s</A>" % (link.uri, link.name)
    rv += "</UL></TD></TR>"
    
    rv += "</TABLE>"
    self.SetPage(rv)

  #def RefreshListCtrl(self, list, list_form):
  #  list_form.DeleteAllItems()
  #  idx = 0
  #  for item in list:
  #    list_form.InsertStringItem(idx, item)
  #    idx += 1

  def OnLinkClicked(self, link):
    uri = link.GetHref()
    if( uri.startswith('/') ):
      if( uri.endswith('pdf') ):
        os.system(self.conf['apps']['pdf']+' '+uri)
      else:
        os.system(self.conf['apps']['html']+' '+uri)
    else:
      uri = uri.replace('&','\&')
      os.system(self.conf['apps']['html']+' '+uri)
