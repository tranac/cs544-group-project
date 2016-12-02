#!/bin/python3
# Chooses a given percentage of files
# from each speaker for training
# Inputs:
#	[directory] [percentage for training]

import sys
import os
from random import shuffle

corpus_dict = sys.argv[1]
train_perc	= float(sys.argv[2])/100.0

print (train_perc)

ang_files = []
mat_files = []
max_files = []

# Get list of all .wav audio files
for dirName, subDirs, files in os.walk(corpus_dict):
	for file in files:
		if ".wav" in file:
			if "angelica" in dirName:
				ang_files.append(dirName + "/" + file)
			elif "mathew" in dirName:
				mat_files.append(dirName + "/" + file)
			else:
				max_files.append(dirName + "/" + file)

# 150 sentences each
amt_files = len(ang_files)
# Shuffle lists to get a random order and get amount of training files
shuffle(ang_files)
shuffle(mat_files)
shuffle(max_files)
train_amt = amt_files * train_perc

# Split files into training and testing data
train_files = []
test_files = []

num_train = amt_files * train_perc
for i in range(0, amt_files):
	if i < train_amt:
		train_files.append(ang_files[i])
		train_files.append(mat_files[i])
		train_files.append(max_files[i])
	else:
		test_files.append(ang_files[i])
		test_files.append(mat_files[i])
		test_files.append(max_files[i])

# Generate codetr.scp, train.scp, and test.scp
with open("codetr.scp", "w") as codetr:
	for file in train_files:
		codetr.write(file + " ")
		codetr.write(file[:-4] + ".mfc\n")
	for file in test_files:
		codetr.write(file + " ")
		codetr.write(file[:-4] + ".mfc\n")

with open("train.scp", "w") as train:
	for file in train_files:
		train.write(file[:-4] + ".mfc\n")

with open("test.scp", "w") as test:
	for file in test_files:
		test.write(file[:-4] + ".mfc\n")