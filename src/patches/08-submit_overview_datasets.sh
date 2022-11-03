#!/usr/bin/bash

for DATASET in "ParaCrawl" "EuroPat" "CCAligned"; do
for DATASET in "All"; do
    echo "Submitting overview of ${DATASET}";
    sbatch --time=0-4 --ntasks=40 --mem-per-cpu=2G \
        --output="logs/overview_${DATASET}.log" \
        --job-name="overview_${DATASET}" \
        --wrap="python3 ./src/vocab_mismatch/dataset_overview.py \
            -i1 data_vocab/${DATASET}.de-en/orig.en \
            -i2 data_vocab/${DATASET}.de-en/orig.de";
done;

DATASET="All"
for SUFFIX in "orig" "teacher"; do
    echo "Submitting overview of ${DATASET}_${SUFFIX}";
    sbatch --time=0-4 --ntasks=40 --mem-per-cpu=2G \
        --output="logs/overview_${DATASET}.${SUFFIX}.log" \
        --job-name="overview_${DATASET}_${SUFFIX}" \
        --wrap="python3 ./src/vocab_mismatch/dataset_overview.py \
            -i1 data_vocab/${DATASET}.de-en/${SUFFIX}.en \
            -i2 data_vocab/${DATASET}.de-en/${SUFFIX}.de";
done;