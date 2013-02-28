#!/usr/bin/python
# -*- coding:utf=8 -*-
import wx, time, datetime
from wx.lib.stattext import GenStaticText as StaticText 
from wx.lib.buttons import GenButton as Button 
class SuspendedFrame(wx.Frame):
	def __init__(self, parent):
		wx.Frame.__init__(self, parent, -1, "SuspendedFrame", size = (150, 30),
			pos = (480, 180), style = wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR | wx.SIMPLE_BORDER)
		self.panel = wx.Panel(self)
		self.mainPad = Button(self.panel, -1,
			label = "00:00:00", pos = (0, 0), size = (150, 30), style = wx.ALIGN_CENTER)
		self.menu = wx.Menu()
		self.clockExit = self.menu.Append(-1, "Exit")

		#timer
		self.timer = wx.Timer(self)
		self.timer.Start(998)
		#bind
		#self.Bind(wx.wx.EVT_LEFT_DCLICK, self.OnPass, self.mainPad)
		self.Bind(wx.EVT_MENU, self.OnClockExit, self.clockExit)
		self.panel.Bind(wx.EVT_CONTEXT_MENU, self.OnShowMenu)
		self.mainPad.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
		#self.panel.Bind(wx.EVT_LEFT_DOWN, self.test)
		self.mainPad.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
		self.mainPad.Bind(wx.EVT_MOTION, self.OnMouseMove)
		self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
		#var
		self.IsMove = 0

	def OnLeftDown(self, event):
		mousePos = self.ClientToScreen(event.GetPosition())
		framePos = self.GetPosition()
		self.delta = wx.Point(mousePos.x - framePos.x, mousePos.y - framePos.y)

	def OnMouseMove(self, event):
		if event.Dragging() and event.LeftIsDown():
			mousePos = self.ClientToScreen(event.GetPosition())
			newPos = (mousePos.x - self.delta.x, mousePos.y - self.delta.y)
			self.Move(newPos)
			self.IsMove = 1

	def OnLeftUp(self, event):
		if self.IsMove == 0:
			self.OnOpenMainFrame()
		else:
			self.IsMove = 0
	
	def OnPass(self, event):
		pass

	def OnOpenMainFrame(self):
		mainFrame = self.GetChildren()[1]
		mainFrame.SetPosition((self.GetPositionTuple()[0] - 120, self.GetPositionTuple()[1] - 300));
		mainFrame.Show()
	
	def OnTimer(self, event):
		self.CopyMainFrameLabel()
		self.Refresh()
			
	def CopyMainFrameLabel(self):
		mainFrame = self.GetChildren()[1]
		self.mainPad.SetLabel(mainFrame.GetClockPadLabel())

	def OnClockExit(self, event):
		self.Destroy()

	def OnShowMenu(self, event):
		pos = event.GetPosition()
		pos = self.ScreenToClient(pos)
		self.PopupMenu(self.menu, pos)
		event.Skip()


class ClockFrame(wx.Frame):
	def __init__(self, parent):
		wx.Frame.__init__(self, parent, -1, "Clock", size = (320, 240), 
			pos = (480,180), 
			style = wx.CLOSE_BOX | wx.CAPTION | wx.FRAME_NO_TASKBAR)

		#panel and clockPad
		self.panel = wx.Panel(self)
		self.clockPad = StaticText(self.panel, -1, 
			label = "00:00:00", pos = (0, 50), size = (320, -1), style = wx.ALIGN_CENTER)
		self.clockPad.SetBackgroundColour("black")
		self.clockPad.SetForegroundColour("white")
		self.clockFont = wx.Font(43, wx.SCRIPT, wx.NORMAL, wx.BOLD)
		self.clockPad.SetFont(self.clockFont)
		self.clockPadLabel = ""
		#buttons
		self.selectButton = wx.ToggleButton(parent = self.panel, label = "进入倒计时模式",
			pos = (90, 5), size = (140, 45))
		self.startButton = wx.Button(parent = self.panel, label = "开始",
			pos = (30, 150), size = (100, 60))
		self.clearButton = wx.Button(parent = self.panel, label = "清零",
			pos = (190, 150), size = (100, 60))
		
		#timer
		self.timer = wx.Timer(self)
		
		#bind
		self.Bind(wx.EVT_CLOSE, self.OnHide)
		self.Bind(wx.EVT_BUTTON, self.OnStartButton, self.startButton)
		self.Bind(wx.EVT_BUTTON, self.OnClearButton, self.clearButton)
		self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
		self.Bind(wx.EVT_TOGGLEBUTTON, self.OnSelectButton, self.selectButton)

	def OnStartButton(self, event):
		self.startTime = time.time()
		self.timer.Start(998)

	def OnTimer(self, event):
		self.nowTime = time.time()
		self.showTime = self.nowTime - self.startTime
		self.clockPadLabel = "%02d:%02d:%02d" % self.InitTimePrint(self.showTime)
		self.clockPad.SetLabel(self.clockPadLabel)

	def GetClockPadLabel(self):
		return self.clockPadLabel

	def InitTimePrint(self, tmp):
		tmp = round(tmp)
		tmp_hour = int(tmp / 3600)
		tmp_min = int((tmp - 3600 * tmp_hour) / 60)
		tmp_sec = int (tmp % 60)
		return (tmp_hour, tmp_min, tmp_sec)

	def OnClearButton(self, event):
		self.timer.Stop()
		self.clockPad.SetLabel("00:00:00")
			
	def OnHide(self, event):
		self.Hide()
		if self.GetParent().IsShown() == False:
			self.GetParent().Show()

	def OnSelectButton(self, event):
		if self.selectButton.GetValue() == True:
			self.selectButton.SetLabel("返回计时模式")
			selectTimeFrame = SelectTimeFrame(parent = self)
			selectTimeFrame.Show()
		else:
			self.selectButton.SetLabel("进入倒计时模式")

class SelectTimeFrame(wx.Frame):

	def __init__(self, parent):
		wx.Frame.__init__(self, parent, -1, "", size = (240, 180), 
			pos = (480,180), 
			style = wx.CLOSE_BOX | wx.CAPTION | wx.FRAME_NO_TASKBAR)
		self.panel = wx.Panel(self)
		self.selectHour = wx.SpinCtrl(parent = self, pos = (1,1), size = (50,20), min = 0, max = 23, initial = 0)
		self.selectMinute = wx.SpinCtrl(parent = self, pos = (1, 70), size = (50, 20), min = 0, max = 59, initial = 0)
		self.selectSecond = wx.SpinCtrl(parent = self, pos = (1, 140), size = (50, 20), min = 0, max = 59, initial = 0)








if __name__ == '__main__':
	app = wx.PySimpleApp()
	suspendedFrame = SuspendedFrame(parent = None)
	mainFrame = ClockFrame(parent = suspendedFrame)
	mainFrame.Show()
	app.MainLoop()
