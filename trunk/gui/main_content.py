import wx
import wx.html
import os, re
from string import atoi
from conf import PubShelfConf
from model_comment import Comment
from dialog_comment import PubShelfCommentDialog

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

  def SetPubItem(self, pubitem):
    self.pubitem = pubitem
    rv = "<TABLE><TR><TD BGCOLOR='blue'>"
    rv += "<FONT COLOR='white'><B>Citation</B></FONT></TD></TR>"
    rv += "<TR><TD>"+pubitem.get_html_citation()+"</TD></TR>"

    rv += "<TR><TD BGCOLOR='blue'><FONT color='white'><b>Tags</b></FONT>"
    rv += "</TD></TR><TR><TD BGCOLOR=#ccccff>"
    tags = []
    for tag in pubitem.tags:
      tags.append( tag.category+'/'+tag.name )
    rv += ', '.join(tags) 
    rv += "</TD></TR>"

    rv += "<TR><TD BGCOLOR='blue'><font color='white'><b>Links</b></font>"
    rv += "</TD></TR><TR><TD><UL>"
    for link in pubitem.links:
      rv += "<LI><A HREF='%s'>%s</A>" % (link.uri, link.name)
    rv += "</UL></TD></TR>"
    
    url_add = "<A HREF='AddComment'><font color='white'>Add</font></A>"
    rv += "<TR><TD BGCOLOR='blue'><font color='white'>"
    rv += "<b>Comments</b> %s </font></TD></TR>" % url_add
    for comment in pubitem.comments:
      url_edit = "<A HREF='EditComment/%d'>[Edit]</A>" % comment.id
      rv += "<TR><TD><b>%s</b> by <i>%s</i> (%s) %s</TD></TR>" \
              % (comment.title, comment.author, comment.created_at, url_edit)
      rv += "<TR><TD><PRE>%s</PRE></TD></TR>" % comment.textbody
    rv += "</TABLE>"
    self.SetPage(rv)
  
  def SetBlank(self):
    self.SetPage('')

  def OnLinkClicked(self, link):
    uri = link.GetHref()
    c = Comment(pubitem_id=self.pubitem.id, author=self.conf['author_name'])
    if( uri == 'AddComment' ):
      dialogComment = PubShelfCommentDialog(self,-1)
      dialogComment.SetComment(c)
      dialogComment.Show()
    elif( uri.startswith('EditComment') ):
      comment_id = atoi(uri.replace('EditComment/',''))
      c.id = comment_id
      comment = c.find()[0]
      dialogComment = PubShelfCommentDialog(self,-1)
      dialogComment.SetComment(comment)
      dialogComment.Show()
    elif( uri.startswith('/') ):
      if( uri.endswith('pdf') ):
        os.system(self.conf['apps']['pdf']+' "'+uri+'"')
      else:
        os.system(self.conf['apps']['html']+' "'+uri+'"')
    else:
      os.system(self.conf['apps']['html']+' "'+uri+'"')
