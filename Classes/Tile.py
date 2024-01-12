class Tile():
	def __init__(self,
				 letter,
				 value):
		self.position = "B"
		self.__letter = letter
		self.__value  = value

	def GetLetter(self):
		return self.__letter

	def GetValue(self):
		return self.__value

