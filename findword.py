import config
from time import perf_counter
from record import record
from countpoints import CountPoints

print(f"Loading wordlist at '{config.wordlist_path}'...")

time_start = perf_counter() # Capture current time
file = open(config.wordlist_path, "r") # Loading word list to memory
words = []
for word in file:
	word = word.strip()
	words.append(word)
time_end = perf_counter() # Capture current time
time = time_end-time_start # Take times away from each other to get a total time taken
print(f"Wordlist loaded in {round(time, 3)} seconds, it is {len(words)} words long")
file.close()
record("timings/wordlistloadtime.txt", str(time) + "\n") # Record how long it took, for data collection


def FindWord(word, output=True):
	word = word.upper()
	length = len(word)
	if length <= 1:
		print("Word must be longer than 1")
		return False
	filt_words = words
	if output:
		print(f"Validating word: '{word}'...")
	time_start = perf_counter() 
	while True: # Using while True because it should only escape the loop by ending the function
		pointer = round((len(filt_words)-1)/2) # Point to middle of wordlist
		point_len = len(filt_words[pointer])
		
		if point_len == length:
			temp = pointer
			while len(filt_words[pointer]) == length: # Check up to left boundary
				pointer -= 1
				if filt_words[pointer] == word:
					summarise(time_start, False, word, output)
					return True
			pointer = temp

			while len(filt_words[pointer]) == length: # Check up to right boundary
				pointer += 1
				if filt_words[pointer] == word:
					summarise(time_start, False, word, output)
					return True
			summarise(time_start, False, word, output)
			return False
			
		elif point_len > length: # If the correct length words are to the left
			filt_words = filt_words[:pointer] 
		elif point_len < length: # If the correct length words are to the right
			filt_words = filt_words[pointer:] 

		
def summarise(time_start, found, word, output):
	if output:
		time_end = perf_counter()
		time = round(time_end-time_start,5)
		if found:
			print(f"Word found in {time} seconds")
		else:
			print(f"Word not found in {time} seconds")
	