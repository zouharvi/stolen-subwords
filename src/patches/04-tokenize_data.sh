#!/usr/bin/bash

# for DATASET in "ParaCrawl" "EuroPat" "CCAligned"; do
for DATASET in "EuroPat"; do
    for PREFIX in "orig" "teacher"; do
        for LANG in "en" "de"; do
            sbatch --time=0-4 --ntasks=40 --mem-per-cpu=1G \
                --output="logs/tokenize_${DATASET}.${LANG}_${PREFIX}.log" \
                --job-name="tokenize_${DATASET}.${LANG}_${PREFIX}" \
                --wrap="cat \"data_vocab/${DATASET}.de-en/${PREFIX}.${LANG}\" \
                    | sacremoses -j 40 -l ${LANG} tokenize \
                    > \"data_vocab/${DATASET}.de-en/${PREFIX}.tok.${LANG}\"\
                ";
        done;
    done;
done;


# join all in All
for DATASET in "ParaCrawl" "EuroPat" "CCAligned"; do
    for PREFIX in "orig" "teacher"; do
        for LANG in "en" "de"; do
            echo "Joining ${DATASET}.${PREFIX}.${LANG}"; 
            cat "data_vocab/${DATASET}.de-en/${PREFIX}.tok.${LANG}" >> "data_vocab/All.de-en/${PREFIX}.tok.${LANG}";
        done;
    done;
done;