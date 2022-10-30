#!/usr/bin/bash

mkdir -p data_vocab/translated

for DATASET1 in "EuroPat" "EUbookshop" "ParaCrawl"; do
        mkdir -p "data_vocab/$DATASET1.de-en";
        mv "data_vocab/${DATASET1}.de-en.de" "data_vocab/$DATASET1.de-en/orig.de";
        mv "data_vocab/${DATASET1}.de-en.en" "data_vocab/$DATASET1.de-en/orig.en";
        mv "data_vocab/${DATASET1}.de-en.tok.de" "data_vocab/$DATASET1.de-en/tok.de";
        mv "data_vocab/${DATASET1}.de-en.tok.en" "data_vocab/$DATASET1.de-en/tok.en";
        mv "data_vocab/${DATASET1}.de-en.bpecodes" "data_vocab/$DATASET1.de-en/self.bpecodes";

    for DATASET2 in "wmt19m" "EuroPat" "EUbookshop" "ParaCrawl"; do
        mv "data_vocab/${DATASET1}.de-en.bpe.${DATASET2}.de" "data_vocab/$DATASET1.de-en/bpe.${DATASET2}.de";
        mv "data_vocab/${DATASET1}.de-en.bpe.${DATASET2}.en" "data_vocab/$DATASET1.de-en/bpe.${DATASET2}.en";
    done;
done;