#!/usr/bin/bash

FASTBPE_BIN="fastBPE/fast"

for DATASET in "EuroPat" "EUbookshop" "ParaCrawl" "All"; do
    # $FASTBPE_BIN getvocab data_vocab/${DATASET}.de-en.tok/en data_vocab/${DATASET}.de-en/tok.de > data_vocab/${DATASET}.dict
    echo "Submitting for $DATASET"
    sbatch --time=0-4 --ntasks=25 --mem-per-cpu=1G \
    --job-name="train bpe ${DATASET}" \
    --output="logs/train_bpe_${DATASET}.log" \
    --wrap="\
        $FASTBPE_BIN learnbpe 30000 \
            data_vocab/${DATASET}.de-en/tok.en data_vocab/${DATASET}.de-en/tok.de \
            > data_vocab/${DATASET}.de-en/self.bpecodes
    ";
done


DATASET="All"
sbatch --time=0-4 --ntasks=25 --mem-per-cpu=1G \
    --job-name="train bpe ${DATASET}" \
    --output="logs/train_bpe_${DATASET}.log" \
    --wrap="\
        $FASTBPE_BIN learnbpe 30000 \
            data_vocab/${DATASET}.de-en/teacher_small.tok.en data_vocab/${DATASET}.de-en/teacher_small.tok.de \
            > data_vocab/${DATASET}.de-en/teacher_small.bpecodes
    ";