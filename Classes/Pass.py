import config
import tkinter as tk

class Pass():
	def __init__(self, pass_pos, pass_size, infobox, spaces):
		self.__scrnPos = pass_pos
		self.__size    = pass_size
		self.__button  = self.GetButton()
		self.__infobox = infobox
		self.__spaces  = spaces

	def GetButton(self):
		button = tk.Button(
			text    = "PASS",
			font    = config.font,
			bg      = config.pass_colour,
			command = lambda: self.ButtonPress()
		)
		button.place(
			x      = self.__scrnPos[0],
			y      = self.__scrnPos[1],
			width  = self.__size[0],
			height = self.__size[1]
		)
		
		return button

	def ButtonPress(self):
		print("Passing turn")
		self.__infobox.SwapTurn(self.__spaces)
		
		