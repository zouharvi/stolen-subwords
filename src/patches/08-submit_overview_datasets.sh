#!/usr/bin/bash

for DATASET in "EuroPat" "EUbookshop" "ParaCrawl"; do
    echo "Submitting overview of $DATASET";
    sbatch --time=0-4 --ntasks=10 --mem-per-cpu=6G \
        --output="logs/overview_${DATASET}.log" \
        --job-name="overview_${DATASET}" \
        --wrap="python3 ./src/vocab_mismatch/dataset_overview.py \
            -i1 data_vocab/${DATASET}.de-en/orig.en \
            -i2 data_vocab/${DATASET}.de-en/orig.de";
done;
