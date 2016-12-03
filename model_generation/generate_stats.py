#Imports

from subprocess import call
import sys
import os

#Functions

def HERest (generationDirectory, modelDirectory, hmm, phones, mlf):
	os.system("HERest -A -D -T 1 -C " + generationDirectory + "/config2 -I " + modelDirectory + "/" + mlf + ".mlf -s " + modelDirectory + "/hmm" + str(hmm+1) + "/stats -t 250.0 150.0 1000.0 -S " + modelDirectory + "/train.scp -H " + modelDirectory + "/hmm" + str(hmm) + "/macros -H " + modelDirectory + "/hmm" + str(hmm) + "/hmmdefs -M " + modelDirectory + "/hmm" + str(hmm+1) + " " + modelDirectory + "/monophones" + str(phones))

#Main
modelDirectory = "Models/" + sys.argv[2]
generationDirectory = sys.argv[1]

HERest(generationDirectory, modelDirectory, 8, 1, "aligned")