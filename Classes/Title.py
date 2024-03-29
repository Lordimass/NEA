import config
import tkinter as tk

class Title():
	def __init__(self, text, root):
		self.text  = text
		self.label = self.GetLabel()
		self.root = root
		print(text)
		root.update()

	def GetLabel(self):
		label = tk.Label(
			text = self.text,
			font = config.font,
		)

		label.pack()
		return label

	def Delete(self):
		self.label.destroy()
		self.root.update()
		del self