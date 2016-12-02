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
def HLed (generationDirectory, modelDirectory):
	os.system("HLed -d " + generationDirectory + "/dict.txt -i " + modelDirectory + "/phones0.mlf " + generationDirectory + "/mkphones0.led " + modelDirectory + "/words.mlf")

#This generates the dictionary and monophones files
def HDMan (generationDirectory, modelDirectory):
	call("HDMan -A -D -T 1 -m -w " + modelDirectory + "/wlist -n " + modelDirectory + "/monophones1 -i -l " + modelDirectory + "/dlog " + modelDirectory + "/dict " + generationDirectory + "/dict.txt")

#This generates the .mfc files for the .wav files
def HCopy (generationDirectory, modelDirectory):
	call("HCopy -A -D -T 1 -C " + generationDirectory + "/config -S " + modelDirectory + "/codetr.scp")

#This does the learning (0-1, 1-2, 2-3, 5-6, 6-7, 7-8, 8-9)
def HERest (generationDirectory, modelDirectory, hmm, monophones):
	call("HERest -A -D -T 1 -C " + generationDirectory + "/config2 -I " + modelDirectory + "/phones0.mlf -t 250.0 150.0 1000.0 -S " + modelDirectory + "/train.scp -H " + modelDirectory + "/hmm" + str(hmm) + "/macros -H " + modelDirectory + "/hmm" + str(hmm) + "/hmmdefs -M " + modelDirectory + "/hmm" + str(hmm+1) + " " + modelDirectory + "/monophones" + str(monophones))

#This fixes silence models (hmm4 to hmm5)
def HHEd (generationDirectory, modelDirectory, hmm):
	call("HHEd -A -D -T 1 -H " + modelDirectory + "/hmm" + str(hmm) + "/macros -H " + modelDirectory + "/hmm" + str(hmm) + "/hmmdefs -M " + modelDirectory + "/hmm" + str(hmm+1) + " " + generationDirectory + "/sil.hed " + modelDirectory + "/monophones1")

#This realigns the transcriptions (hmm7)
def HVite (generationDirectory, modelDirectory, hmm, monophones):
	call("HVite -A -D -T 1 -l '*' -o SWT -C " + generationDirectory + "/config2 -H " + modelDirectory + "/hmm" + str(hmm) + "/macros -H " + modelDirectory + "/hmm" + str(hmm) + "/hmmdefs -i " + modelDirectory + "/aligned.mlf -m -t 250.0 150.0 1000.0 -y lab -a -I " + modelDirectory + "/words.mlf -S " + modelDirectory + "/train.scp " + modelDirectory + "/dict " + modelDirectory + "/monophones1> HVite_log")

#Main
modelDirectory = "Models/" + sys.argv[1]
generationDirectory = sys.argv[2]
corpusDirectory = sys.argv[3]

prompts = corpusDirectory + "/transcription_output.txt"
promts2wlist = generationDirectory + "/prompts2wlist"

#Create the directory structure needed for the new model
for i in range(10):
	if not os.path.exists(modelDirectory + "/hmm" + str(i)):
		os.makedirs(modelDirectory + "/hmm" + str(i))

#Get the file paths to all the .wav files
audio = []
for dirName, subDirs, files in os.walk(corpusDirectory):
	for file in files:
		if ".wav" in file:
			audio.append(dirName + "/" + file)

prompts2wlist(generationDirectory, corpusDirectory, modelDirectory)
prompts2mlf(generationDirectory, corpusDirectory, modelDirectory)
HLed(generationDirectory, modelDirectory)