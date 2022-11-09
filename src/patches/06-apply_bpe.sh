#!/usr/bin/bash

FASTBPE_BIN="fastBPE/fast"

# copy victim's vocab
# WMT19_PATH="/home/vilda/.cache/torch/pytorch_fairseq/0695ef328ddefcb8cbcfabc3196182f59c0e41e0468b10cc0db2ae9c91881fcc.bb1be17de4233e13870bd7d6065bfdb03fca0a51dd0f5d0b7edf5c188eda71f1"
# cp "${WMT19_PATH}/bpecodes" data_vocab/wmt19m.de-en.bpecodes

# for DATASET1 in "EuroPat"; do
#     for DATASET2 in "CCAligned"; do
for DATASET1 in "ParaCrawl" "EuroPat" "CCAligned"; do
    for DATASET2 in "ParaCrawl" "EuroPat" "CCAligned"; do
        for LANG in "en" "de"; do
            echo "Submitting BPE trained on $DATASET1 (${LANG}) on data from $DATASET2:";
            sbatch --time=0-4 --ntasks=40 --mem-per-cpu=1G \
                --output="logs/applybpe_${DATASET1}_${LANG}_${DATASET2}.log" \
                --job-name="applybpe_${DATASET1}_${LANG}_${DATASET2}" \
                --wrap="$FASTBPE_BIN applybpe \
                    data_vocab/${DATASET2}.de-en/teacher.bpe.${DATASET1}.${LANG} \
                    data_vocab/${DATASET2}.de-en/teacher.tok.${LANG} \
                    data_vocab/${DATASET1}.de-en/orig.bpecodes
                ";
        done;
    done;
done


for DATASET1 in "wmt19m"; do
    # for DATASET2 in "ParaCrawl" "EuroPat" "CCAligned"; do
    for DATASET2 in "EuroPat"; do
        for LANG in "en" "de"; do
            echo "Submitting BPE trained on $DATASET1 (${LANG}) on data from $DATASET2:";
            sbatch --time=0-4 --ntasks=40 --mem-per-cpu=1G \
                --output="logs/applybpe_${DATASET1}_${LANG}_${DATASET2}.log" \
                --job-name="applybpe_${DATASET1}_${LANG}_${DATASET2}" \
                --wrap="$FASTBPE_BIN applybpe \
                    data_vocab/${DATASET2}.de-en/orig.bpe.${DATASET1}.${LANG} \
                    data_vocab/${DATASET2}.de-en/orig.tok.${LANG} \
                    data_vocab/${DATASET1}.de-en.bpecodes
                ";
        done;
    done;
done


DATASET2="All"
# for DATASET2 in "ParaCrawl" "EuroPat" "CCAligned"; do
for SUFFIX in "uniq_small_lower" "uniq_small" "uniq"; do
    for LANG in "en" "de"; do
        echo "Submitting BPE trained on $DATASET1 (${LANG}) on data from $DATASET2:";
        wc -l "data_vocab/${DATASET2}.de-en/orig.tok.${LANG}.${SUFFIX}";
        sbatch --time=0-4 --ntasks=40 --mem-per-cpu=1G \
            --output="logs/applybpe_${DATASET1}_${LANG}_${DATASET2}_${SUFFIX}.log" \
            --job-name="applybpe_${DATASET1}_${LANG}_${DATASET2}_${SUFFIX}" \
            --wrap="$FASTBPE_BIN applybpe \
                data_vocab/${DATASET2}.de-en/orig.tok.${LANG}.${SUFFIX}.bpe \
                data_vocab/${DATASET2}.de-en/orig.tok.${LANG}.${SUFFIX} \
                data_vocab/wmt19m.de-en.bpecodes
            ";
    done;
done;