#!/usr/bin/bash

for DATASET in "EuroPat" "EUbookshop" "ParaCrawl"; do
    for m0 in $(seq 0 9); do
        m1=$(($m0 + 1));

        echo "Submitting translation of $DATASET ($m0-$m1)";
        # Into German
        sbatch --time=1-00 --ntasks=8 --mem-per-cpu=3G --gpus=1 \
            --job-name="translate_teacher_${DATASET}.${m0}.de" \
            --output="logs/translate_teacher_${DATASET}.${m0}.de.log" \
            --wrap="python3 src/teacher_translate.py \
                --model transformer.wmt19.en-de \
                -i data_vocab/${DATASET}.de-en/orig.en \
                -o data_vocab/${DATASET}.de-en/teacher.${m0}.de \
                -m0 $m0 -m1 $m1";
        echo "Submitting translation of $DATASET ($m0-$m1)";
        # Into English
        sbatch --time=1-00 --ntasks=8 --mem-per-cpu=3G --gpus=1 \
            --job-name="translate_teacher_${DATASET}.${m0}.en" \
            --output="logs/translate_teacher_${DATASET}.${m0}.en.log" \
            --wrap="python3 src/teacher_translate.py \
                --model transformer.wmt19.de-en \
                -i data_vocab/${DATASET}.de-en/orig.de \
                -o data_vocab/${DATASET}.de-en/teacher.${m0}.en \
                -m0 $m0 -m1 $m1";
    done;
done;