import tkinter as tk
import config
import saveload

class Infobox():
	def __init__(self, player1, player2, bag, scrnPos, size):
		self.player1   = player1
		self.player2   = player2
		self.bag	   = bag
		self.p1Turn    = True
		self.text      = tk.StringVar()
		self.__scrnPos = scrnPos
		self.__size    = size
		self.__label   = self.__GetLabel()
		self.UpdateText()

	def __GetLabel(self):
		label = tk.Label(
			bg           = config.info_box_colour,
			textvariable = self.text,
			wraplength   = self.__size[0],
		    font         = config.font,
			justify      = tk.LEFT,
			anchor       = "nw",
		    relief       = tk.RAISED)
			
		label.place(
			x            = self.__scrnPos[0],
			y            = self.__scrnPos[1],
			width        = self.__size[0],
			height       = self.__size[1])

	def __GetRackAsString(self, rack):
		output = ""
		for tile in rack:
			output += tile.GetLetter() + str(tile.GetValue()).translate(config.subscript) + " "
		return output

	def UpdateText(self):
		p1_score = f"Player 1 Score: {self.player1.GetPoints()}"
		p2_score = f"Player 2 Score: {self.player2.GetPoints()}"

		if self.p1Turn:
			rack = self.__GetRackAsString(self.player1.GetRack())
			turn = "1"
		else:
			rack = self.__GetRackAsString(self.player2.GetRack())
			turn = "2"

		self.text.set(f'''{p1_score}
{p2_score} \n
{rack} \n
There are {len(self.bag)} letters remaining in the bag and it is Player {turn}'s turn''')

	def SwapTurn(self, board, save = True):
		if self.p1Turn:
			self.player1.DrawLetters(self.bag)
			print("---------------------- PLAYER 2's TURN ----------------------")
		else:
			self.player2.DrawLetters(self.bag)
			print("---------------------- PLAYER 1's TURN ----------------------")

		self.p1Turn = not(self.p1Turn)
		self.UpdateText()
		if save:
			saveload.saveGame(board, self)

		
		
