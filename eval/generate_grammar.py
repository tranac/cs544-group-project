# Multi-word nouns are in a different file so we can
# read the entire line
def get_multi_nouns():
	with open("gram-mult-noun", "w") as output:
		with open("mult-noun-def","r") as input:
			for line in input:
				output.write(" | " + line.rstrip())
		input.closed
	output.closed

# Get all of the words labels with [label] for easy 
# exporting to the grammar
def get_labels(label):
	with open("gram-out", "w") as output:
		with open("gram-def","r") as input:
			for line in input:
				tokens = line.split()
				if tokens[1].upper() == label:
					output.write(" | " + tokens[0])
		input.closed
	output.closed

get_labels("NOUN")
get_multi_nouns()