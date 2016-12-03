#!/bin/bash

dir=~/cs544-group-project/Models/All_${1-10}_${2-1}
echo $dir

cp -r $dir/hmm9 hmm9_$1_$2