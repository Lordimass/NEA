from random import randint
import config
import AI.AI as AI

class Player():
	def __init__(self, isPlayer1, isAI = False):
		self.__rack    = []
		self.__points  = 0
		self.__isPlayer1 = isPlayer1
		self.__isAI      = isAI

		if isAI:
			self.FindMove = AI.FindMove

	def GetPlayer(self):
		return self.__issPlayer1

	def GetAI(self):
		return self.__isAI

	def GetPoints(self):
		return self.__points

	def AddPoints(self, points):
		self.__points += points

	def SetPoints(self, points):
		self.__points = points

	def GetRack(self):
		return self.__rack

	def AddLetter(self, tile):
		self.__rack.append(tile)

	def ClearRack(self):
		self.__rack = []

	def RemoveLetter(self, letter):
		for tile in self.__rack:
			if tile.GetLetter() == letter:
				self.__rack.pop(self.__rack.index(tile))
				return True

		if self.__isPlayer1:
			player = 1
		else:
			player = 2
		print(f"ERROR: Requested removal of nonexistant letter ('{letter}') from rack of Player {player}")
		return False

	def DrawLetters(self, bag):
		count = config.rack_size - len(self.__rack)
		
		if self.__isPlayer1:
			player = "1"
		else:
			player = "2"
			
		for letter in range(count):
			if len(bag) != 0:
				tile = bag[randint(0, len(bag)-1)]
				tile.position = player
				self.AddLetter(tile)
				bag.pop(bag.index(tile))