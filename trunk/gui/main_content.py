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
    
    rv += "<TR><TD BGCOLOR='blue'><font color='white'>"
    rv += "<b>Comments</b></font></TD></TR>"
    rv += "<TR><TD BGCOLOR='#ccccff' ALIGN=RIGHT><font color='blue'>"
    rv += "<A HREF='AddComment'>Add Comment</A></font></TD></TR>"
    for comment in pubitem.comments:
      rv += "<TR><TD><b>%s</b> by <i>%s</i> (%s)</TD></TR>" \
              % (comment.title, comment.author, comment.created_at)
      rv += "<TR><TD>%s</TD></TR>" % comment.textbody
      rv += "<TR><TD BGCOLOR='#ccccff' ALIGN=RIGHT><font color='blue'>"
      rv += "<A HREF='EditComment/%d'>Edit</A></font/></TD></TR> " % comment.id
    rv += "</TABLE>"
    self.SetPage(rv)

  def OnLinkClicked(self, link):
    uri = link.GetHref()
    if( uri == 'AddComment' ):
      dialogComment = PubShelfCommentDialog(None,-1,self.pubitem)
      dialogComment.ShowModal()
      dialogComment.Destroy()
    elif( uri.startswith('EditComment') ):
      comment_id = atoi(uri.replace('EditComment/',''))
      c = Comment(id=comment_id)
      comment = c.find( )[0]
      dialogComment = PubShelfCommentDialog(None,-1,self.pubitem)
      dialogComment.SetComment(comment)
      dialogComment.ShowModal()
      dialogComment.Destroy()
    elif( uri.startswith('/') ):
      if( uri.endswith('pdf') ):
        os.system(self.conf['apps']['pdf']+' '+uri)
      else:
        os.system(self.conf['apps']['html']+' '+uri)
    else:
      uri = uri.replace('&','\&')
      os.system(self.conf['apps']['html']+' '+uri)
