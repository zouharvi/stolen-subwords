#!/usr/bin/bash
# Run me from the top-level directory

DATA_SIZE_K=1000
mkdir -p data

# generate 1mil sentences for chars
./src/data_generation/main.py -n $DATA_SIZE_K -g char_zerogram_8 -o data/char_zerogram_8_en.txt
./src/data_generation/main.py -n $DATA_SIZE_K -g char_ngram_en --ngram 1 -o data/char_1gram_en.txt
./src/data_generation/main.py -n $DATA_SIZE_K -g char_ngram_en --ngram 2 -o data/char_2gram_en.txt
./src/data_generation/main.py -n $DATA_SIZE_K -g char_ngram_en --ngram 3 -o data/char_3gram_en.txt

# generate 1mil sentences for words
./src/data_generation/main.py -n $DATA_SIZE_K -g word_ngram_en --ngram 1 -o data/word_1gram_en.txt
./src/data_generation/main.py -n $DATA_SIZE_K -g word_ngram_en --ngram 2 -o data/word_2gram_en.txt
./src/data_generation/main.py -n $DATA_SIZE_K -g word_ngram_en --ngram 3 -o data/word_3gram_en.txt

# generate 1mil sentences for subwords
./src/data_generation/main.py -n $DATA_SIZE_K -g subword_ngram_en --ngram 1 --bpe-model transformer.wmt19.en-de -o data/subword_1gram_en.txt
./src/data_generation/main.py -n $DATA_SIZE_K -g subword_ngram_en --ngram 2 --bpe-model transformer.wmt19.en-de -o data/subword_2gram_en.txt
./src/data_generation/main.py -n $DATA_SIZE_K -g subword_ngram_en --ngram 3 --bpe-model transformer.wmt19.en-de -o data/subword_3gram_en.txt