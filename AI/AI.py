import AI.PossibleMoves as PossibleMoves
from Classes.Title import Title
import time

def FindMove(spaces, infobox, root):
	title = Title("Player two is choosing their move...", root)
	PossibleMoves.PossibleMoves(spaces, infobox, root)
	title.Delete()