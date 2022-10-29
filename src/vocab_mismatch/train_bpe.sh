#!/usr/bin/bash

FASTBPE_BIN="/home/vilda/bin/fastBPE/fast"

# train BPE
for DATASET in "EuroPath" "EUbookshop" "ParaCrawl"; do
    # $FASTBPE_BIN getvocab data_vocab/${DATASET}.de-en.tok.en data_vocab/${DATASET}.de-en.tok.de > data_vocab/${DATASET}.dict
    $FASTBPE_BIN learnbpe 30000 data_vocab/${DATASET}.de-en.tok.en data_vocab/${DATASET}.de-en.tok.de > data_vocab/${DATASET}.bpecodes
done