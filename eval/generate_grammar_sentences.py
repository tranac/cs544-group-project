artcs = set()
adjcs = set()
advbs = set()
nouns = set()
posss = set()
prons = set()
preps = set()
verbs = set()

# Multi-word nouns are in a different file so we can
# read the entire line
def get_multi_nouns():
	with open("mult-noun-def","r") as input:
		for line in input:
			for token in line.split()[1:]:
				nouns.add(token)
	input.closed

# Get all of the words labels with [label] for easy 
# exporting to the grammar
def get_labels():
	with open("gram-def","r") as input:
		for line in input:
			tokens = line.split()
			if tokens[1].upper() == "ARTC":
				artcs.add(tokens[0])
			if tokens[1].upper() == "ADJC":
				adjcs.add(tokens[0])
			if tokens[1].upper() == "ADVB":
				advbs.add(tokens[0])
			if tokens[1].upper() == "NOUN":
				nouns.add(tokens[0])
			if tokens[1].upper() == "POSS":
				posss.add(tokens[0])
			if tokens[1].upper() == "PRON":
				prons.add(tokens[0])
			if tokens[1].upper() == "PREP":
				preps.add(tokens[0])
			if tokens[1].upper() == "VERB":
				verbs.add(tokens[0])
	input.closed

get_labels()
get_multi_nouns()

sentences = set()
with open("transcription_output.txt","r") as input:
	for line in input:
		tokens = line.split()[1:]
		sentence = ""
		for token in tokens:
			if token in artcs:
				sentence += "$artc "
			elif token in adjcs:
				sentence += "$adjc "
			elif token in advbs:
				sentence += "$advb "
			elif token in nouns:
				sentence += "$noun "
			elif token in posss:
				sentence += "$poss "
			elif token in prons:
				sentence += "$pron "
			elif token in preps:
				sentence += "$prep "
			elif token in verbs:
				sentence += "$verb "
		sentences.add(sentence)
input.closed

i = 0
with open("gram-sent", "w") as output:
	for sentence in sentences:
		if i == 25:
			break
		output.write("| " + sentence + "\n")
		i += 1
output.closed