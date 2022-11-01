#!/usr/bin/bash

cd data_vocab

for lang in "en" "de"; do
    cat EuroPat.de-en/orig.${lang} | sacremoses -j 30 -l de tokenize > EuroPat.de-en/tok.${lang};
    cat EUbookshop.de-en/orig.${lang} | sacremoses -j 30 -l de tokenize > EUbookshop.de-en/tok.${lang};
    cat ParaCrawl.de-en/orig.${lang} | sacremoses -j 30 -l de tokenize > ParaCrawl.de-en/tok.${lang};
    cat All.de-en/teacher_small.${lang} | sacremoses -j 30 -l de tokenize > All.de-en/teacher_small.tok.${lang};
done

cd ..