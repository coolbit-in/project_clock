import   wx
#---------------------------------------------------------------------------
text="Popmenu"
class MyFrame(wx.Frame):
     def __init__(
             self, parent, ID, title, pos=wx.DefaultPosition,
             size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE
             ):
         wx.Frame.__init__(self, parent, ID, title, pos, size, style)
         panel = TestPanel(self, -1)
        
         self.CreateStatusBar()

class TestPanel(wx.Panel):
     def __init__(self, parent, log):
         wx.Panel.__init__(self, parent, -1)
         box = wx.BoxSizer(wx.VERTICAL)
         # Make and layout the controls
         fs = self.GetFont().GetPointSize()
         bf = wx.Font(fs+4, wx.SWISS, wx.NORMAL, wx.BOLD)
         nf = wx.Font(fs+2, wx.SWISS, wx.NORMAL, wx.NORMAL)
         t = wx.StaticText(self, -1, text)
         t.SetFont(nf)
         box.Add(t, 0, wx.CENTER|wx.ALL, 5)
         t.Bind(wx.EVT_CONTEXT_MENU, self.OnContextMenu)
         self.SetSizer(box)
         self.Bind(wx.EVT_CONTEXT_MENU, self.OnContextMenu)

     def OnContextMenu(self, event):
         #print ("OnContextMenu\n")
         # only do this part the first time so the events are only bound once
         #
         # Yet another anternate way to do IDs. Some prefer them up top to
         # avoid clutter, some prefer them close to the object of interest
         # for clarity. 
         if not hasattr(self, "popupID1"):
             self.popupID1 = wx.NewId()
             self.popupID2 = wx.NewId()
             self.popupID3 = wx.NewId()
             self.popupID4 = wx.NewId()
             self.popupID5 = wx.NewId()
             self.popupID6 = wx.NewId()
             self.popupID7 = wx.NewId()
             self.popupID8 = wx.NewId()
             self.popupID9 = wx.NewId()
             self.Bind(wx.EVT_MENU, self.OnPopupNine, id=self.popupID9)
         # make a menu
         menu = wx.Menu()
         # Show how to put an icon in the menu
         item = wx.MenuItem(menu, self.popupID1,"One")

         menu.AppendItem(item)
         # add some other items
         menu.Append(self.popupID2, "Two")
         menu.Append(self.popupID3, "Three")
         menu.Append(self.popupID4, "Four")
         menu.Append(self.popupID5, "Five")
         menu.Append(self.popupID6, "Six")
         # make a submenu
         sm = wx.Menu()
         sm.Append(self.popupID8, "sub item 1")
         sm.Append(self.popupID9, "sub item 1")
         menu.AppendMenu(self.popupID7, "Test Submenu", sm)

         # Popup the menu.   If an item is selected then its handler
         # will be called before PopupMenu returns.
         self.PopupMenu(menu)
         menu.Destroy()
     def OnPopupNine(self, event):
         print ("Popup nine\n")

if __name__ == '__main__':
     app=wx.App()
     f=MyFrame(None,-1,'hello')
     f.SetIcon(wx.Icon('smile.ico', wx.BITMAP_TYPE_ICO))
     f.Show()
     app.MainLoop()