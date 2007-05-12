import wx

class PubShelfItemList(wx.ListCtrl):
  def __init__(self, parent, id, conf):
    window_style = wx.html.HW_SCROLLBAR_AUTO
    super(PubShelfItemContent, self).__init__(parent, id, style=window_style)
    self.conf = conf

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
