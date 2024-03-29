import csv

####################################
# Loading point values
scores = {}
score_file = open("standardletterdistribtion.csv", "r")
reader = csv.reader(score_file)
for line in reader:
	scores[line[0]] = int(line[2])

####################################
# Can leave word_tiles parameter as None and just provide a string of letters (for crosswords since multipliers are irrelevant)
def CountPoints(word_tiles, spaces, word_letters = None):
	multiply = False
	if (word_tiles != None) and (word_letters != None):
		raise Exception("Cannot parse both word_tiles and word_letters to CountPoints, it only needs one of these")
	elif (word_tiles == None) and (word_letters == None):
		raise Exception("At least one parameter must be provided, either word_tiles or word_letters")
	elif (word_tiles != None) and (spaces == None):
		raise Exception("Full spaces list must be provided in order to count multipliers, if multipliers are not necessary, parse word_letters instead.")
	elif (word_letters != None) and (spaces != None):
		print("Spaces do not need to be provided when parsing word letters as multipliers are not counted, consider parsing None instead.")
	elif (word_tiles != None) and (word_letters == None):
		multiply = True
	elif (word_tiles == None) and (word_letters != None):
		multiply = False
	else:
		raise Exception("Unexpected input")
	score = 0
	multiplier = 1
	if word_tiles != None:
		for tile in word_tiles:
			if multiply:
				
				position = tile.position
				space = spaces[int(position[1])][int(position[0])]
				
				if space.multiplier == "TW":
					multiplier *= 3
				elif space.multiplier == "DW":
					multiplier *= 2
		
				if space.multiplier == "TL":
					space_mult = 3
				elif space.multiplier == "DL":
					space_mult = 2
				else:
					space_mult = 1
	
			score += tile.GetValue()*space_mult
	else:
		for letter in word_letters:
			score += scores[letter.upper()]
		
	score *= multiplier
	return score