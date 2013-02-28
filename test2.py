import wx
class AbstractButton(wx.Window):

   def __init__(self,parent,id=-1,label=wx.EmptyString,pos=wx.DefaultPosition,
                size=wx.DefaultSize, style=0,
                validator=wx.DefaultValidator,name=wx.ButtonNameStr):

      wx.Window.__init__(self,  parent, id,pos,size,style,name)
      self._label=label
      self.width,self.height=self.ComputerBestSize()
      self.SetSize(wx.Size(self.width,self.height))
      self.SetTransparent(0)
      self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
      self._onFouce=self._keyDown=self._mouseIn=self._mouseDown=False
      self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
      self.Bind(wx.EVT_LEFT_UP,self.OnMouseUp)

      self.Bind(wx.EVT_LEAVE_WINDOW,self.OnMouseLeave)
      self.Bind(wx.EVT_ENTER_WINDOW,self.OnMouseEnter)
      self.Bind(wx.EVT_ERASE_BACKGROUND,lambda evt:evt.Skip())
      self.Bind(wx.EVT_PAINT,self.OnPaint)
      self.Bind(wx.EVT_SET_FOCUS,self.OnFouce)
      self.Bind(wx.EVT_KILL_FOCUS,self.OnLoseFocue)

      self.Bind(wx.EVT_BUTTON,self.OnPress)

      self.mouseInBmp=None
      self.mouseDownBmp=None
      self.mouseOutBmp=None
      self.onFouceBmp=None

   def SetDefault(self):
      def OnKey(evt):
         if evt.GetKeyCode() in (wx.WXK_RETURN,wx.WXK_NUMPAD_ENTER):
            self.SendButtonCmd()
         else:
            evt.Skip()
      self.GetParent().Bind(wx.EVT_CHAR_HOOK,OnKey)


   def SetLabel(self,label):
      self._label=label

   def GetLabel(self):
      return self._label

   def OnPress(self,event):
      self._keyDown=True
      self.Refresh()
      self._keyDown=False
      event.Skip()

   def OnFouce(self,event):
      self._onFouce=True
      self.Refresh()
      event.Skip()

   def OnLoseFocue(self,event):
      self._onFouce=False
      self.Refresh()
      event.Skip()


   def ComputerBestSize(self):
      label=self.GetLabel()
      #return default
      if not label:return 24,21
      #computer best size
      fontLen=len(label)
      width,height=65,26
      if fontLen>2:width+=5*(fontLen-2)
      return width,height


   def OnMouseEnter(self,event):
      self._mouseIn = True
      self.Refresh()
      event.Skip()

   def OnMouseLeave(self,event):
      self._mouseIn = False
      self.Refresh()
      event.Skip()

   def OnMouseDown(self,event):
      self._mouseDown = True
      self.Refresh()
      event.Skip()

   def OnMouseUp(self,event):
      self._mouseDown = False
      self.Refresh()
      event.Skip()
      self.SendButtonCmd()

   def DrawButtion(self,dc):
      if self._mouseDown or self._keyDown:
         dc.DrawBitmap(self.mouseDownBmp,0,0)
      elif self._mouseIn:
         dc.DrawBitmap(self.mouseInBmp,0,0)
      elif self._onFouce:
         dc.DrawBitmap(self.onFouceBmp,0,0)
      else:
         dc.DrawBitmap(self.mouseOutBmp,0,0)



   def OnKeyDown(self,event):
      self._keyDown=True
      self.Refresh()
      event.Skip()

   def OnKeyUp(self,event):
      if self._keyDown:
         self._keyDown=False
         self.Refresh()
         event.Skip()
         self.SendButtonCmd()
      else:
         event.Skip()


   def DrawCenterText(self,dc):
      labelText=self.GetLabel()
      if not labelText:return
      w,h=self.GetTextExtent(labelText)
      w2,h2=self.GetClientSizeTuple()
      x,y=(w2-w)/2,(h2-h)/2
      dc.DrawText(labelText,x,y)

   def SendButtonCmd(self):
      event = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, self.GetId())
      event.SetInt(0)
      event.SetEventObject(self)
      self.GetEventHandler().ProcessEvent(event)
      event.Skip()

class SkinCloseButton(AbstractButton):

   def __init__(self,parent):
      AbstractButton.__init__(self,parent,style=wx.NO_BORDER)
      self.mouseInBmp=ImageCenter.WCloseInBmp.GetBitmap()
      self.mouseDownBmp=ImageCenter.WCloesOutBmp.GetBitmap()
      self.onFouceBmp=self.mouseOutBmp=ImageCenter.WCloesOutBmp.GetBitmap()


   def BindClose(self,frame):
      frame.Bind(wx.EVT_BUTTON,
         lambda evt:win32gui.SendMessage(frame.GetHandle(),
            win32con.WM_CLOSE,0,0),self)



   def OnPaint(self, event):
      dc = wx.BufferedPaintDC(self)
      self.DrawButtion(dc)
#####################################################
class SkinMaxSizeButton(AbstractButton):
   def __init__(self,parent):
      AbstractButton.__init__(self,parent,style=wx.NO_BORDER)
      self.mouseInBmp=ImageCenter.WMaxInBmp.GetBitmap()
      self.mouseDownBmp=ImageCenter.WMaxOutBmp.GetBitmap()
      self.onFouceBmp=self.mouseOutBmp=ImageCenter.WMaxDownBmp.GetBitmap()


   def BindMaxSize(self,frame):
      frame.Bind(wx.EVT_BUTTON,
         lambda evt:win32gui.SendMessage(frame.GetHandle(),
            win32con.WM_SYSCOMMAND,
            win32con.SC_MAXIMIZE,0),self)




   def OnPaint(self, event):
      dc = wx.BufferedPaintDC(self)
      self.DrawButtion(dc)
#####################################################
class SkinMinSizeButton(AbstractButton):
   def __init__(self,parent):
      AbstractButton.__init__(self,parent,style=wx.NO_BORDER)
      self.mouseInBmp=ImageCenter.WMinInBmp.GetBitmap()
      self.mouseDownBmp=ImageCenter.WMinOutBmp.GetBitmap()
      self.onFouceBmp=self.mouseOutBmp=ImageCenter.WMinDownBmp.GetBitmap()


   def BindMinSize(self,frame):
      frame.Bind(wx.EVT_BUTTON,
         lambda evt:
         win32gui.SendMessage(frame.GetHandle(),
            win32con.WM_SYSCOMMAND,
            win32con.SC_MINIMIZE,0),self)



   def OnPaint(self, event):
      dc = wx.BufferedPaintDC(self)
      self.DrawButtion(dc)

