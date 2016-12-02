#!/bin/python3
# Compares the output of the HTK recognizer
# on a word-by-word basis and counts the
# num_error rate for each word. An num_error counts as:
#	Word was misidentified
# Input Arguments:
#	[prompt list of correct transcripts] [recognized transcript]

import sys
from operator import itemgetter
from collections import defaultdict

num_error = defaultdict(int)	# Number of num_errors per word
num_words = defaultdict(int)	# Number of appearances

# Create dictonaries of correct transcripts to check against 
correct_transcripts = defaultdict(list)

with open(sys.argv[1],"r") as prompt_list:
	for prompt in prompt_list:
		tokens = prompt.split()
		sent = tokens[0]
		correct_transcripts[sent] = tokens[1:]
		for token in correct_transcripts[sent]:
			num_words[token] += 1

# Parse recognized transcript and compare against the correct one
with open(sys.argv[2],"r") as rec_output:
	rec_output.readline()
	sent = rec_output.readline()[3:-6]
	sentence_ind = 0
	for lines in rec_output:
		if lines == ".\n":
			sent = rec_output.readline()[3:-6]
			sentence_ind = 0
		else:
			word = lines.split()[2]
			if sentence_ind < len(correct_transcripts[sent]):
				if correct_transcripts[sent][sentence_ind] != word:
					print("wrong word " + word)
					num_error[correct_transcripts[sent][sentence_ind]] += 1
				sentence_ind += 1

# Get error percentages and print the percentages of any incorrect words
err_perc = defaultdict(float)
for word in num_words:
		err_perc[word] = 1 - (float(num_words[word] - num_error[word]) / float(num_words[word]))

print("Specific Word Error Percentages: ")
sorted_perc = sorted(err_perc.items(), key=itemgetter(1))
for word in sorted_perc:
	if word[1]:
		print("%.4f " % round(word[1],4) + word[0])
