#!/usr/bin/bash

# clean up log file
# rm -f data_vocab/compute_bpe_all.out

for DATASET1 in "wmt19m" "ParaCrawl" "EuroPat" "CCAligned" "All"; do
    for DATASET2 in "ParaCrawl" "EuroPat" "CCAligned"; do
        echo "Computing for BPE trained on $DATASET1 on data from $DATASET2:";
        ./src/vocab_mismatch/compute_bpe_len.py \
            --dataset "data_vocab/${DATASET2}.de-en/orig.bpe.${DATASET1}.en" \
            --dataset "data_vocab/${DATASET2}.de-en/orig.bpe.${DATASET1}.de" \
            --target-dataset ${DATASET2} \
            --bpe-dataset $DATASET1 \
            >> data_vocab/compute_bpe_all.out;
    done;
done