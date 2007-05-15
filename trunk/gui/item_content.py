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
    rv = "<TABLE><TR><TD>%s,<b>%s</b>,<i>%s</i>,<b><i>%s</i></b></TD></TR>" \
        % (pubitem.authors, pubitem.pub_year, pubitem.title, pubitem.journal)

    rv += "<TR><TD>Tags : "
    for tag in pubitem.tags:
      rv += "%s:%s " % (tag.category, tag.name)
    rv += "</TD></TR>"
      
    for comment in pubitem.comments:
      rv += "<TR><TD>%s</TD></TR><TR><TD>%s</TD></TR>"\
            % (comment.title, comment.textbody)

    for link in pubitem.links:
      rv += "<TR><TD><A HREF='%s'>%s</A></TD></TR>" % (link.uri, link.name)
    rv += "</TABLE>"
    self.SetPage( rv )

  def OnLinkClicked(self, link):
    uri = link.GetHref()
    print uri
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
