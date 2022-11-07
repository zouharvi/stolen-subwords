#!/usr/bin/bash

./src/vocab_mismatch/convert_to_vocab.py -i data_vocab/All.de-en/teacher.tok.en -o data_vocab/All.de-en/teacher.tok.en.uniq --no-debpe
./src/vocab_mismatch/convert_to_vocab.py -i data_vocab/All.de-en/teacher.tok.de -o data_vocab/All.de-en/teacher.tok.de.uniq --no-debpe

./src/vocab_mismatch/convert_to_vocab.py -i data_vocab/All.de-en/orig.tok.en -o data_vocab/All.de-en/orig.tok.en.uniq --no-debpe
./src/vocab_mismatch/convert_to_vocab.py -i data_vocab/All.de-en/orig.tok.de -o data_vocab/All.de-en/orig.tok.de.uniq --no-debpe

sbatch --time=0-4 --ntasks=50 --mem-per-cpu=1500M \
    --job-name="minimize vocab de uniq small" \
    --output="logs/minimize_de_uniq_small" \
    --wrap="./src/vocab_mismatch/minimize_vocab.py -i data_vocab/All.de-en/orig.tok.de.uniq -o data_vocab/All.de-en/orig.tok.de.uniq_small"
sbatch --time=0-4 --ntasks=50 --mem-per-cpu=1500M \
    --job-name="minimize vocab en uniq small" \
    --output="logs/minimize_en_uniq_small" \
    --wrap="./src/vocab_mismatch/minimize_vocab.py -i data_vocab/All.de-en/orig.tok.en.uniq -o data_vocab/All.de-en/orig.tok.en.uniq_small"

sbatch --time=0-4 --ntasks=50 --mem-per-cpu=1500M \
    --job-name="minimize vocab de uniq small lower" \
    --output="logs/minimize_de_uniq_small_lower" \
    --wrap="./src/vocab_mismatch/minimize_vocab.py -i data_vocab/All.de-en/orig.tok.de.uniq -o data_vocab/All.de-en/orig.tok.de.uniq_small_lower --lower"
sbatch --time=0-4 --ntasks=50 --mem-per-cpu=1500M \
    --job-name="minimize vocab en uniq small lower" \
    --output="logs/minimize_en_uniq_small_lower" \
    --wrap="./src/vocab_mismatch/minimize_vocab.py -i data_vocab/All.de-en/orig.tok.en.uniq -o data_vocab/All.de-en/orig.tok.en.uniq_small_lower --lower"