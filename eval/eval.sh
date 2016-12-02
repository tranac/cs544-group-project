#!/bin/bash
# Script to run evaluations for a given model
# Will be tweaked as full models come in

# Potential Parameters:
# Correct transcription
# Model directory
# Label MLF file
# FInished monophones file

# Working commands
# HVite -C config2 -H hmm9/macros -H hmm9/hmmdefs -l '*' -S test.scp -I mat_words.mlf -i recout.mlf dict monophones1
# HResults -I mat_words.mlf monophones1 recout.mlf

test_data=$1
rec_out=$2
res_out=$3

HVite -C config2 -H hmm9/macros -H hmm9/hmmdefs -l '*' -S $test_data -I mat_words.mlf -i $rec_out dict monophones1

HResults -I mat_words.mlf monophones1 $rec_out > $res_out

python3 word_errors.py prompts $rec_out >> $res_out