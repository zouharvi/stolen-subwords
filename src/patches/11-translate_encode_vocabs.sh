#!/usr/bin/bash

FASTBPE_BIN="fastBPE/fast"

for SUFFIX in "uniq" "uniq_small"; do
    echo "Submitting translation of ALL_${SUFFIX}";
    # Into German
    sbatch --time=1-00 --ntasks=8 --mem-per-cpu=3G --gpus=1 \
        --job-name="translate_teacher_${SUFFIX}.de" \
        --output="logs/translate_teacher_${SUFFIX}.de.log" \
        --wrap="\
            python3 src/teacher_translate.py \
                --model transformer.wmt19.en-de \
                -i data_vocab/${DATASET}.de-en/orig.tok.en.${SUFFIX} \
                -o data_vocab/${DATASET}.de-en/orig.tok.en.${SUFFIX}.teacher;\
            $FASTBPE_BIN applybpe \
                data_vocab/${DATASET}.de-en/orig.tok.en.${SUFFIX}.teacher.bpe \
                data_vocab/${DATASET}.de-en/orig.tok.en.${SUFFIX}.teacher \
                data_vocab/wmt19m.de-en.bpecodes;
            ";
    # Into English
    sbatch --time=1-00 --ntasks=8 --mem-per-cpu=3G --gpus=1 \
        --job-name="translate_teacher_${SUFFIX}.en" \
        --output="logs/translate_teacher_${SUFFIX}.en.log" \
        --wrap="\
            python3 src/teacher_translate.py \
                --model transformer.wmt19.en-de \
                -i data_vocab/${DATASET}.de-en/orig.tok.de.${SUFFIX} \
                -o data_vocab/${DATASET}.de-en/orig.tok.de.${SUFFIX}.teacher;\
            $FASTBPE_BIN applybpe \
                data_vocab/${DATASET}.de-en/orig.tok.de.${SUFFIX}.teacher.bpe \
                data_vocab/${DATASET}.de-en/orig.tok.de.${SUFFIX}.teacher \
                data_vocab/wmt19m.de-en.bpecodes;
            ";
done;