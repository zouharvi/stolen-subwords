#!/usr/bin/bash

mkdir -p data_vocab/translated

# for DATASET in "EuroPat" "EUbookshop" "ParaCrawl"; do
for DATASET in "EuroPat"; do
    mkdir -p "data_vocab/$DATASET.de-en";
    mv "data_vocab/${DATASET}.de-en.de" "data_vocab/$DATASET.de-en/orig.de";
    mv "data_vocab/${DATASET}.de-en.en" "data_vocab/$DATASET.de-en/orig.en";
    mv "data_vocab/${DATASET}.de-en.tok.de" "data_vocab/$DATASET.de-en/tok.de";
    mv "data_vocab/${DATASET}.de-en.tok.en" "data_vocab/$DATASET.de-en/tok.en";
    mv "data_vocab/${DATASET}.de-en.bpe.wmt19m.de" "data_vocab/$DATASET.de-en/bpe.wmt19m.de";
    mv "data_vocab/${DATASET}.de-en.bpe.wmt19m.en" "data_vocab/$DATASET.de-en/bpe.wmt19m.en";
    
    mkdir -p "data_vocab/$DATASET.de-en/bin";

    fairseq-preprocess \
        --source-lang en --target-lang de \
        --trainpref "data_vocab/$DATASET.de-en/bpe.wmt19m" \
        --destdir "data_vocab/${DATASET}.de-en/bin" \
        --thresholdtgt 0 --thresholdsrc 0 \
        --bpe fastbpe \
        --joined-dictionary \
        --workers 20
done;