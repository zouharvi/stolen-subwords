#!/usr/bin/bash

for DATASET in "EuroPat" "EUbookshop" "ParaCrawl"; do
    for LANG in "en" "de"; do
        sbatch --time=0-4 --ntasks=20 --mem-per-cpu=3G \
            --output="logs/tokenize_${DATASET}.${LANG}_orig.log" \
            --job-name="tokenize_${DATASET}.${LANG}_orig" \
            --wrap="cat \"data_vocab/${DATASET}.de-en/orig.${LANG}\" | sacremoses -j 20 -l ${LANG} tokenize > \"data_vocab/${DATASET}.de-en/orig.tok.${LANG}\"";

        sbatch --time=0-4 --ntasks=20 --mem-per-cpu=3G \
            --output="logs/tokenize_${DATASET}.${LANG}_teacher.log" \
            --job-name="tokenize_${DATASET}.${LANG}_teacher" \
            --wrap="cat \"data_vocab/${DATASET}.de-en/teacher.${LANG}\" | sacremoses -j 20 -l ${LANG} tokenize > \"data_vocab/${DATASET}.de-en/teacher.tok.${LANG}\"";
    done;
done;


# join all in All
for DATASET in "EuroPat" "EUbookshop" "ParaCrawl"; do
    for PREFIX in "orig" "teacher"; do
        for LANG in "en" "de"; do
            echo "Joining ${DATASET}.${LANG}"; 
            cat "data_vocab/${DATASET}.de-en/${PREFIX}.tok.${LANG}" >> "data_vocab/All.de-en/${PREFIX}.tok.${LANG}";
        done;
    done;
done;

# cat All.de-en/teacher.${lang} | sacremoses -j 30 -l de tokenize > All.de-en/teacher.tok.${lang};