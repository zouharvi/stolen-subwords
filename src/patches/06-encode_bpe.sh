#!/usr/bin/bash

FASTBPE_BIN="fastBPE/fast"

# copy victim's vocab
# WMT19_PATH="/home/vilda/.cache/torch/pytorch_fairseq/0695ef328ddefcb8cbcfabc3196182f59c0e41e0468b10cc0db2ae9c91881fcc.bb1be17de4233e13870bd7d6065bfdb03fca0a51dd0f5d0b7edf5c188eda71f1"
# cp "${WMT19_PATH}/bpecodes" data_vocab/wmt19m.de-en.bpecodes

# run BPE in parallel
for DATASET1 in "wmt19m" "EuroPat" "EUbookshop" "ParaCrawl"; do
    for DATASET2 in "EuroPat" "EUbookshop" "ParaCrawl"; do
        for LANG in "en" "de"; do
            echo "Submitting BPE trained on $DATASET1 (${LANG}) on data from $DATASET2:";
            sbatch --time=0-12 --ntasks=10 --mem-per-cpu=6G \
                --output="logs/applybpe_${DATASET1}_${LANG}_${DATASET2}.log" \
                --job-name="applybpe_${DATASET1}_${LANG}_${DATASET2}" \
                --wrap="$FASTBPE_BIN applybpe \
                    data_vocab/${DATASET2}.de-en.bpe.${DATASET1}.${LANG} \
                    data_vocab/${DATASET2}.de-en.tok.${LANG} \
                    data_vocab/${DATASET1}.de-en.bpecodes
                ";
        done;
    done;
done

DATASET1="All"
for LANG in "en" "de"; do
    sbatch --time=0-4 --ntasks=10 --mem-per-cpu=6G \
        --output="logs/applybpe_${DATASET1}_${LANG}.log" \
        --job-name="applybpe_${DATASET1}_${LANG}" \
        --wrap="\
        $FASTBPE_BIN applybpe \
            data_vocab/${DATASET1}.de-en/teacher_small.tok.bpe.wmt19m.${LANG} \
            data_vocab/${DATASET1}.de-en/teacher_small.tok.${LANG} \
            data_vocab/wmt19m.de-en.bpecodes;
        ";
done;