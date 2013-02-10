import wx 
import os 
ID_BUTTON1=110 
class MainWindow(wx.Frame): 
   def __init__(self,parent,id,title): 
      self.dirname='' 
      wx.Frame.__init__(self,parent,wx.ID_ANY, title) 
      self.control = wx.TextCtrl(self, 1, style=wx.TE_MULTILINE) 
      wx.EVT_MENU(self, -1, self.OnAbout) 
      wx.EVT_MENU(self, ID_EXIT, self.OnExit) 
      wx.EVT_MENU(self, ID_OPEN, self.OnOpen) 
      self.sizer2 = wx.BoxSizer(wx.HORIZONTAL) 
      self.buttons=[] 
      for i in range(0,5): 
         self.SetFont(wx.Font(2+2*i,wx.FONTFAMILY_MODERN,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL, faceName="Courier New")) 
         self.buttons.append(wx.Button(self, ID_BUTTON1+i, "Button &"+str(i+1))) 
         self.sizer2.Add(self.buttons[i],1,wx.EXPAND) 
      ## Use some sizers to see layout options 
      sizer=wx.BoxSizer(wx.VERTICAL) 
      sizer.Add(self.control,1,wx.EXPAND) ## the control (editor) aspect ratio changes with frame size 
      #self.sizer.Add(self.control,1,wx.SHAPED) ## the control aspect ratio is set, and will not change 
      sizer.Add(self.sizer2,0,wx.EXPAND)  ## Likewise, for the buttons 
      #self.sizer.Add(self.sizer2,0,wx.SHAPED) 
      ##Layout sizers 
      self.SetSizer(sizer) 
      self.SetAutoLayout(1) 
      sizer.Fit(self) 
      self.Show(1) 
app = wx.PySimpleApp() 
frame = MainWindow(None, -1, "Sample editor") 
app.MainLoop() 
