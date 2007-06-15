import wx

ID_OPEN = 1000

class PubShelfMenuBar(wx.MenuBar):
  def __init__(self):
    super(PubShelfMenuBar, self).__init__()
    self.Append( self.FileMenu(), '&File' )

  def FileMenu(menubar):
    file = wx.Menu()
    file.Append(ID_OPEN, '&Open', 'Open new file')
    return file
