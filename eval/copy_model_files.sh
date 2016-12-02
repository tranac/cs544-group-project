#!/bin/bash

dir=~/cs544-group-project/Models/All_${1-10}_${2-1}

# Keep just in case
cp -r ./hmm9 hmm9-old
cp ./test.scp ./test-old.scp

cp -r $dir/hmm9 hmm9
cp $dir/test.scp ./test.scp