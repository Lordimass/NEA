def record(path, text):
	file = open(path, "a")
	file.write(text)
	file.close()

