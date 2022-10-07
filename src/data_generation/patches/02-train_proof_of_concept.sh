#!/usr/bin/bash

# generate source data (parallel)
for ((i=0; i < 10; i++)); do 
    ./src/data_generation/main.py \
        -n 100 -g word_ngram_en \
        --ngram 3 -o data/word_3gram_en.${i}.txt \
        --seed $i 2> /dev/null &
done

# TODO sync before here
cat data/word_3gram_en.*.txt > data/word_3gram_en.txt

# eval data
sacrebleu --download wmt21 --language-pair en-de
cat ~/.sacrebleu/wmt21/wmt21.en-de.src

# teacher translate
for ((i=0; i < 10; i++)); do 
    ./src/teacher_translate.py
        -i data/word_3gram_en.${i}.txt -o data/word_3gram_ende.${i}.txt &
done