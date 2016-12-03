#!/bin/bash
# Script to run evaluations for a given model
# Will be tweaked as full models come in

# Potential Parameters:
# Correct transcription
# Model directory
# Label MLF file
# FInished monophones file

# rec_out=${1-recout.mlf}
# res_out=${2-results.out}
rec_out=adapt_recout_$1_$2.mlf
res_out=adapt_results_$1_$2.out
start=`date +%s`
echo Testing adapted model $1_$2

#HVite -C config2 -H hmm9_$1_$2/macros -H hmm9_$1_$2/hmmdefs -l '*' -S eval-test.scp -w wdnet -i $rec_out -p 0.0 -s 5.0 dict monophones1
HVite -C config2 -H adapt_$1_$2/macros -H adapt_$1_$2/hmmdefs -l '*' -S eval-test.scp -w wdnet -i $rec_out -p 0.0 -s 5.0 dict monophones1

end=`date +%s`
runtime=$((end-start))

echo $runtime

HResults -I wordsFix.mlf monophones1 $rec_out > $res_out

python3 word_errors.py prompts $rec_out >> $res_out

