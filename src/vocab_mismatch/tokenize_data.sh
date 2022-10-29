#!/usr/bin/bash

cd data_vocab

for lang in "en" "de"; do
    # head -n 10000000 EuroPat.de-en.${lang} | sacremoses -j 10 -l de tokenize > EuroPat.de-en.tok.${lang};
    head -n 10000000 EUbookshop.de-en.${lang} | sacremoses -j 10 -l de tokenize > EUbookshop.de-en.tok.${lang};
    # head -n 10000000 ParaCrawl.de-en.${lang} | sacremoses -j 10 -l de tokenize > ParaCrawl.de-en.tok.${lang};
done

cd ..