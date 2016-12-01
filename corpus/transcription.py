import csv

num_max = 1
num_mat = 1
num_ang = 1

with open("transcription_output.txt", "w") as output:
	with open("input.csv","r") as input:
		reader = csv.DictReader(input)
		for entry in reader:
			# File Tag
			if entry["Person"] == "MW":
				output.write("MAX_")
				if(num_max < 10):
					output.write("0")
				if(num_max < 100):
					output.write("0")
				output.write(str(num_max) + " ")
				num_max += 1
			elif entry["Person"] == "MS":
				output.write("MAT_")
				if(num_mat < 10):
					output.write("0")
				if(num_mat < 100):
					output.write("0")
				output.write(str(num_mat) + " ")
				num_mat += 1
			else:
				output.write("ANG_")
				if(num_ang < 10):
					output.write("0")
				if(num_ang < 100):
					output.write("0")
				output.write(str(num_ang) + " ")
				num_ang += 1
			# Sentence
			sentence = entry["Sentence"]
			sentence = sentence.upper()[:-1]
			output.write(sentence + '\n')
	input.closed
output.closed