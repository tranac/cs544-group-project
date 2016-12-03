import csv

num_max = 1
num_mat = 1
num_ang = 1

with open("gram-out", "w") as output:
	with open("gram-def","r") as input:
		for line in input:
			tokens = line.split()
			print(tokens)
			# # Sentence
			# sentence = entry["Sentence"]
			# sentence = sentence.upper()[:-1]
			# output.write(sentence + '\n')
	input.closed
output.closed