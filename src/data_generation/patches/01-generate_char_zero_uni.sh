#!/usr/bin/bash

# Run me from the top-level directory

mkdir -p data

# generate 1mil sentences
./src/data_generation/main.py -n 1000 -g char_unigram_en -o data/char_unigram_en.txt
./src/data_generation/main.py -n 1000 -g char_zerogram_8 -o data/char_zerogram_8.txt