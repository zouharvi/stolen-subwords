#!/usr/bin/bash

# generate source data (parallel)
# bsub 
for ((i=0; i < 10; i++)); do 
    ./src/data_generation/main.py \
        -n 100 -g word_ngram_en \
        --ngram 3 -o data/word_3gram_en.${i}.txt \
        --seed $i 2> /dev/null &
done

# TODO sync before here
cat data/word_3gram_en.*.txt > data/word_3gram_en.txt

# eval data
# /cluster/home/vzouhar/.sacrebleu/wmt21/wmt21.en-de.src
sacrebleu --download wmt21 --language-pair en-de
cat ~/.sacrebleu/wmt21/wmt21.en-de.src

# teacher translate
for ((i=0; i < 10; i++)); do 
    bsub -W 20:00 -n 4 -R "rusage[mem=4096,ngpus_excl_p=1]" \
        ./src/teacher_translate.py \
        -i data/word_3gram_en.${i}.txt -o data/word_3gram_ende.${i}.txt ;
done

# translate WMT21 test set 
bsub -W 4:00 -n 4 -R "rusage[mem=4096,ngpus_excl_p=1]" \
    ./src/teacher_translate.py \
    -i /cluster/home/vzouhar/.sacrebleu/wmt21/wmt21.en-de.src -o data/wmt21.en-de.teacher-tgt