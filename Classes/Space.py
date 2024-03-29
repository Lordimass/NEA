import config
from .Indicator import Indicator
import tkinter as tk

class Space():
	def __init__(self,
				 coordinate,
				 multiplier,
				 tileSize,
				 win_buffer,
				 callback,
				 indicator_callback):
		self.coordinate 		= coordinate
		self.multiplier 		= multiplier
		self.winBuffer  		= win_buffer
		self.__size     		= tileSize
		self.tile     		    = None
		self.button     		= self.Render()
		self.indicators 		= None
		self.__colour   		= self.__GetColour()
		self.callback   		= callback
		self.indicator_callback = indicator_callback

		self.UpdateButton()

	def Render(self):
		self.__scrnPos = self.GetScrnPos()
		button = tk.Button(
			text    = None,
			font    = config.font,
			command = lambda: self.SelectSpace(True),
			bg      = None)
		
		button.place(
			x       = self.__scrnPos[0],
			y       = self.__scrnPos[1],
			width   = self.__size,
			height  = self.__size)
		
		return button

	def UpdateButton(self):
		self.__scrnPos = self.GetScrnPos()
		
		if self.tile == None:
			if not(self.multiplier == None):
				txt = self.multiplier 
			else: # To account for deletion of tiles and their text not being removed if text attribute set to None
				txt = ""
		else:
			txt = f"{self.tile.GetLetter()}{str(self.tile.GetValue()).translate(config.subscript)}"
		
		self.__colour = self.__GetColour()
		
		self.button.config(
			text = txt,
			bg   = self.__colour
		)

	def GetScrnPos(self):
		x = self.winBuffer[0] + int(self.coordinate[0])*self.__size
		y = self.winBuffer[1] + int(self.coordinate[1])*self.__size
		return (x,y)
		
	def __GetColour(self, colours = config.colours):
		if self.tile == None:
			return colours[self.multiplier]
		else:
			return colours["Tile"]

	def SelectSpace(self, manual = False):
		self.callback(self.coordinate, manual) # Update selected_space in main.py
		right = Indicator(True, self.__scrnPos, self.__size, self.indicator_callback) # Make new indicators
		down  = Indicator(False, self.__scrnPos, self.__size, self.indicator_callback)
		self.indicators = (right, down)

	def PlayTile(self, tile):
		self.tile     = tile
		tile.position = self.coordinate
		self.UpdateButton()
