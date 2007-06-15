import wx
import wx.html
import os
import re

class PubShelfItemContent(wx.html.HtmlWindow):
  def __init__(self, parent, id, conf):
    window_style = wx.html.HW_SCROLLBAR_AUTO
    super(PubShelfItemContent, self).__init__(parent, id, style=window_style)
    self.conf = conf
    if 'gtk2' in wx.PlatformInfo:
      self.SetStandardFonts()

  def set_pubitem(self, pubitem):
    rv = "<TABLE><TR><TD BGCOLOR='blue'>"
    rv += "<FONT COLOR='white'><B>Citation</B></FONT></TD></TR>"
    rv += "<TR><TD>"+pubitem.get_html_citation()+"</TD></TR>"

    rv += "<TR><TD BGCOLOR='blue'><font color='white'><b>Links</b></font>"
    rv += "</TD></TR><TR><TD><UL>"
    for link in pubitem.links:
      rv += "<LI><A HREF='%s'>%s</A>" % (link.uri, link.name)
    rv += "</UL></TD></TR>"

    rv += "<TR><TD BGCOLOR='blue'><FONT color='white'><b>Tags</b></FONT>"
    rv += "</TD></TR><TR><TD><UL>"
    for tag in pubitem.tags:
      rv += "<LI> %s:%s " % (tag.category, tag.name)
    rv += "</UL></TD></TR>"
      
    #rv += "<TR><TD BGCOLOR='blue'><font color='white'><b>Comments</b></font>"
    #rv += "</TD></TR><TR><TD>"
    #for comment in pubitem.comments:
    #  rv += "<B>%s</B><BR>" % comment.title
    #  rv += "%s<BR><BR>" % comment.textbody
    #rv += "</TD></TR>"

    rv += "</TABLE>"

    self.SetPage( rv )

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
