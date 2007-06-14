import wx

class PubShelfNewItemDialog(wx.Dialog):
  def __init__(self, parent, id):
    wx.Dialog.__init__(self, parent, id, 'New PubItem')
