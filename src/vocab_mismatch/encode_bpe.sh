#!/usr/bin/bash

FASTBPE_BIN="fastBPE/fast"

# copy victim's vocab
# WMT19_PATH="/home/vilda/.cache/torch/pytorch_fairseq/0695ef328ddefcb8cbcfabc3196182f59c0e41e0468b10cc0db2ae9c91881fcc.bb1be17de4233e13870bd7d6065bfdb03fca0a51dd0f5d0b7edf5c188eda71f1"
# cp "${WMT19_PATH}/bpecodes" data_vocab/wmt19m.de-en.bpecodes

# run BPE in parallel
for DATASET1 in "wmt19m" "EuroPat" "EUbookshop" "ParaCrawl"; do
    for DATASET2 in "EuroPat" "EUbookshop" "ParaCrawl"; do
        echo "Running BPE trained on $DATASET1 on data from $DATASET2:";
        $FASTBPE_BIN applybpe_stream data_vocab/${DATASET1}.de-en.bpecodes < data_vocab/${DATASET2}.de-en.tok.en > data_vocab/${DATASET2}.de-en.bpe.en &
        echo "Running BPE trained on $DATASET1 on data from $DATASET2:";
        $FASTBPE_BIN applybpe_stream data_vocab/${DATASET1}.de-en.bpecodes < data_vocab/${DATASET2}.de-en.tok.de > data_vocab/${DATASET2}.de-en.bpe.de &
    done;
done

for DATASET1 in "wmt19m" "EuroPat" "EUbookshop" "ParaCrawl"; do
    for DATASET2 in "EuroPat" "EUbookshop" "ParaCrawl"; do
        echo "Computing for BPE trained on $DATASET1 on data from $DATASET2:";
        ./src/vocab_mismatch/compute_bpe_len.py \
            --dataset "data_vocab/${DATASET2}.de-en.bpe.en" \
            --dataset "data_vocab/${DATASET2}.de-en.bpe.de" \
            --target-dataset ${DATASET2} \
            --bpe-dataset $DATASET1 \
            >> data_vocab/compute_bpe_all.out;
    done;
done