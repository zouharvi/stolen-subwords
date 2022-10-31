#!/usr/bin/bash

FASTBPE_BIN="fastBPE/fast"

# train BPE
for DATASET in "EuroPat" "EUbookshop" "ParaCrawl"; do
    # $FASTBPE_BIN getvocab data_vocab/${DATASET}.de-en.tok.en data_vocab/${DATASET}.de-en.tok.de > data_vocab/${DATASET}.dict
    $FASTBPE_BIN learnbpe 30000 data_vocab/${DATASET}.de-en.tok.en data_vocab/${DATASET}.de-en.tok.de > data_vocab/${DATASET}.de-en.bpecodes
done