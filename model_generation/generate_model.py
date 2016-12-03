#Imports

from subprocess import call
import sys
import os

#Classes

#Functions

#Generates words.mlf file
def prompts2mlf (generationDirectory, corpusDirectory, modelDirectory):
	os.system("perl " + generationDirectory + "/prompts2mlf " + modelDirectory + "/words.mlf " + corpusDirectory + "/transcription_output.txt")

#Generates wlist file
def prompts2wlist (generationDirectory, corpusDirectory, modelDirectory):
	os.system("perl " + generationDirectory + "/prompts2wlist " + corpusDirectory + "/transcription_output.txt " + modelDirectory + "/wlist")

#This generates the phones, mkphones, and words files
def HLed (generationDirectory, modelDirectory, phones):
	os.system("HLed -A -D -T 1 -l '*' -d " + generationDirectory + "/dict.txt -i " + modelDirectory + "/phones" + str(phones) + ".mlf " + generationDirectory + "/mkphones" + str(phones) + ".led " + modelDirectory + "/words.mlf")

#This generates the dictionary and monophones files
def HDMan (generationDirectory, modelDirectory):
	os.system("HDMan -A -D -T 1 -m -w " + modelDirectory + "/wlist -n " + modelDirectory + "/monophones -i -l " + modelDirectory + "/dlog " + modelDirectory + "/dict " + generationDirectory + "/dict.txt")

#This generates the .mfc files for the .wav files
def HCopy (generationDirectory, modelDirectory):
	os.system("HCopy -A -D -T 1 -C " + generationDirectory + "/config -S " + modelDirectory + "/codetr.scp")

#This generates the initial HMM
def HCompV (generationDirectory, modelDirectory):
	os.system("HCompV -A -D -T 1 -C " + generationDirectory + "/config2 -f 0.01 -m -S " + modelDirectory + "/train.scp -M " + modelDirectory + "/hmm0 " + generationDirectory +"/proto")

#This does the learning (0-1, 1-2, 2-3, 5-6, 6-7, 7-8, 8-9)
def HERest (generationDirectory, modelDirectory, hmm, phones, mlf):
	os.system("HERest -A -D -T 1 -C " + generationDirectory + "/config2 -I " + modelDirectory + "/" + mlf + ".mlf -t 250.0 150.0 1000.0 -S " + modelDirectory + "/train.scp -H " + modelDirectory + "/hmm" + str(hmm) + "/macros -H " + modelDirectory + "/hmm" + str(hmm) + "/hmmdefs -M " + modelDirectory + "/hmm" + str(hmm+1) + " " + modelDirectory + "/monophones" + str(phones))

#This fixes silence models (hmm4 to hmm5)
def HHEd (generationDirectory, modelDirectory, hmm):
	os.system("HHEd -A -D -T 1 -H " + modelDirectory + "/hmm" + str(hmm) + "/macros -H " + modelDirectory + "/hmm" + str(hmm) + "/hmmdefs -M " + modelDirectory + "/hmm" + str(hmm+1) + " " + generationDirectory + "/sil.hed " + modelDirectory + "/monophones1")

#This realigns the transcriptions (hmm7)
def HVite (generationDirectory, modelDirectory, hmm):
	os.system("HVite -A -D -T 1 -l '*' -o SWT -C " + generationDirectory + "/config2 -H " + modelDirectory + "/hmm" + str(hmm) + "/macros -H " + modelDirectory + "/hmm" + str(hmm) + "/hmmdefs -i " + modelDirectory + "/aligned.mlf -m -t 250.0 150.0 1000.0 -y lab -a -I " + modelDirectory + "/wordsFix.mlf -S " + modelDirectory + "/train.scp " + modelDirectory + "/dict " + modelDirectory + "/monophones1> " + modelDirectory + "/HVite_log")

#This fixes words.mlf to have * in the path name
def FixWords (modelDirectory):
	words = open(modelDirectory + "/words.mlf", "r")
	wordsFix = open(modelDirectory + "/wordsFix.mlf", "w")
	for line in words:
		if ".lab" in line:
			path = "\"*/"
			path += line[1:]
			wordsFix.write(path)
		else:
			wordsFix.write(line)

#This fixes dict, adding silence [silence] for adaptation at later stages
def FixDict (modelDirectory):
	dictionary = open(modelDirectory + "/dict", "r")
	holderDictionary = open(modelDirectory + "/holderdict", "w")
	holderDictionary.write(dictionary.read())

	dictionary = open(modelDirectory + "/dict", "w")
	holderDictionary = open(modelDirectory + "/holderdict", "r")
	for line in holderDictionary:
		dictionary.write(line)
		if "[SHOWS]" in line:
			dictionary.write("sil             [sil]\n")

#Creates the .scp files that detail what .wav files are used for training and testing with randomness
def GenerateDataSplit (generationDirectory, corpusDirectory, modelDirectory, trainingPercentage):
	os.system("python " + generationDirectory + "/generate_data_split.py " + corpusDirectory + " " + trainingPercentage + " " + modelDirectory)

#Generates the Monophone1 file (removes sp from monophones1)
def GenerateMonophones (modelDirectory):
	monophones1 = open(modelDirectory + "/monophones1", "w")
	monophones = open(modelDirectory + "/monophones", "r")
	monophones0 = open(modelDirectory + "/monophones0", "w")
	monophones1.write(monophones.read())
	monophones1.write("sp\n")
	monophones1.write("sil\n")
	monophones.seek(0)
	monophones0.write(monophones.read())
	monophones0.write("sil\n")

#Builds the hmmdefs file from the generated proto file and the monophones0 file
def GenerateHmmDefs (modelDirectory):
	hmmdefs = open(modelDirectory + "/hmm0/hmmdefs", "w")
	proto = open(modelDirectory + "/hmm0/proto", "r")
	monophones0 = open(modelDirectory + "/monophones0")
	
	protoHolder = ""
	write = False;
	for line in proto:
		if "BEGIN" in line:
			write = True
		if write:
			protoHolder += line

	for line in monophones0:
		line = line.strip()
		hmmdefs.write("~h \"" + line + "\"\n")
		hmmdefs.write(protoHolder)

#Generates the macros file from proto and vFloors
def GenerateMacro (modelDirectory):
	proto = open(modelDirectory + "/hmm0/proto", "r")
	vFloors = open(modelDirectory + "/hmm0/vFloors", "r")
	macros = open(modelDirectory + "/hmm0/macros", "w")
	for i in range(3):
		macros.write(proto.readline())
	macros.write(vFloors.read())

#Generates fixed hmm for silence models
def FixSilence (modelDirectory):
	hmm3defs = open(modelDirectory + "/hmm3/hmmdefs", "r")
	hmm3macros = open(modelDirectory + "/hmm3/macros", "r")
	hmm4defs = open(modelDirectory + "/hmm4/hmmdefs", "w")
	hmm4macros = open(modelDirectory + "/hmm4/macros", "w")

	hmm4macros.write(hmm3macros.read())

	hmm4defs.write(hmm3defs.read())

	hmm4defs.write("~h \"sp\"\n")
	hmm4defs.write("<BEGINHMM>\n")
	hmm4defs.write("<NUMSTATES> 3\n")
	hmm4defs.write("<STATE> 2\n")

	hmm3defs.seek(0)

	write = False
	sp = False
	defHolder = ""
	for line in hmm3defs:
		if "<STATE> 4" in line:
			write = False
		if write and sil:
			hmm4defs.write(line)
		if "~h" in line:
			if "sil" in line:
				sil = True
			else:
				sil = False
		if "<STATE> 3" in line:
			write = True

	hmm4defs.write("<TRANSP> 3\n")
	hmm4defs.write(" 0.0 1.0 0.0\n")
	hmm4defs.write(" 0.0 0.9 0.1\n")
	hmm4defs.write(" 0.0 0.0 0.0\n")
	hmm4defs.write("<ENDHMM>\n")

#Main
modelDirectory = "Models/" + sys.argv[3]
generationDirectory = sys.argv[1]
corpusDirectory = sys.argv[2]
trainingPercentage = sys.argv[4]

prompts = corpusDirectory + "/transcription_output.txt"
promts2wlist = generationDirectory + "/prompts2wlist"

#Create the directory structure needed for the new model
for i in range(10):
	if not os.path.exists(modelDirectory + "/hmm" + str(i)):
		os.makedirs(modelDirectory + "/hmm" + str(i))

prompts2wlist(generationDirectory, corpusDirectory, modelDirectory)
prompts2mlf(generationDirectory, corpusDirectory, modelDirectory)

HLed(generationDirectory, modelDirectory, 0)
HLed(generationDirectory, modelDirectory, 1)

FixWords(modelDirectory)

GenerateDataSplit(generationDirectory, corpusDirectory, modelDirectory, trainingPercentage)

HDMan(generationDirectory, modelDirectory)

FixDict(modelDirectory)

GenerateMonophones(modelDirectory)

HCopy(generationDirectory, modelDirectory)

HCompV(generationDirectory, modelDirectory)

GenerateHmmDefs(modelDirectory)
GenerateMacro(modelDirectory)

for i in range(3):
	HERest(generationDirectory, modelDirectory, i, 0, "phones0")

FixSilence(modelDirectory)
HHEd(generationDirectory, modelDirectory, 4)

for i in range(5, 7):
	HERest(generationDirectory, modelDirectory, i, 1, "phones1")

HVite(generationDirectory, modelDirectory, 7)

for i in range(7, 9):
	HERest(generationDirectory, modelDirectory, i, 1, "aligned")
