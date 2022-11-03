#!/usr/bin/bash

FASTBPE_BIN="fastBPE/fast"

for DATASET in "ParaCrawl" "EuroPat" "CCAligned" "All"; do
    for PREFIX in "orig" "teacher"; do
        # $FASTBPE_BIN getvocab data_vocab/${DATASET}.de-en.tok/en data_vocab/${DATASET}.de-en/tok.de > data_vocab/${DATASET}.dict
        echo "Submitting for $DATASET"
        sbatch --time=0-4 --ntasks=25 --mem-per-cpu=2G \
        --job-name="train bpe ${DATASET} ${PREFIX}" \
        --output="logs/train_bpe_${DATASET}_${PREFIX}.log" \
        --wrap="\
            $FASTBPE_BIN learnbpe 30000 \
                data_vocab/${DATASET}.de-en/${PREFIX}.tok.en data_vocab/${DATASET}.de-en/${PREFIX}.tok.de \
                > data_vocab/${DATASET}.de-en/${PREFIX}.bpecodes
        ";
    done;
done