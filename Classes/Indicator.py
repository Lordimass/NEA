import config
import tkinter as tk

class Indicator():
	def __init__(self, right, parentPos, parentSize, callback):
		self.right      = right
		self.parentPos  = parentPos
		self.parentSize = parentSize
		self.__scrnPos  = self.GetScrnPos()
		self.__size     = self.GetSize()
		self.button		= None
		self.callback   = callback
		self.Render()

	def Render(self):
		if self.right:
			txt = ">"
		else:
			txt = "v"

		button = tk.Button(
			text    = txt,
			font    = config.font,
		    command = lambda: self.callback(self.right),
			bg      = config.indicator_colour)
		
		button.place(
			x       = self.__scrnPos[0],
			y       = self.__scrnPos[1],
		    width   = self.__size[0],
			height  = self.__size[1])
		
		self.button = button

	def GetScrnPos(self):
		if self.right:
			x = self.parentPos[0]+(0.7*self.parentSize)
			y = self.parentPos[1]
			return (x,y)
		else:
			x = self.parentPos[0]
			y = self.parentPos[1]+(0.7*self.parentSize)
			return (x,y)
			
	def GetSize(self):
		x = 0.3*self.parentSize
		y = self.parentSize-(0.3*self.parentSize)
		if self.right:
			return (x,y)
		else:
			return (y,x)
	
