#!/usr/bin/bash

mkdir -p data_vocab
FASTBPE_BIN="/home/vilda/bin/fastBPE/fast"

# copy victim's vocab
WMT19_PATH="/home/vilda/.cache/torch/pytorch_fairseq/0695ef328ddefcb8cbcfabc3196182f59c0e41e0468b10cc0db2ae9c91881fcc.bb1be17de4233e13870bd7d6065bfdb03fca0a51dd0f5d0b7edf5c188eda71f1"
cp "${WMT19_PATH}/bpecodes" data_vocab/wmt19m_bpecodes.txt

# extract data
# echo "EXTRACTING DATA"
# for DATASET in "wmt19" "para_crawl" "europarl"; do
#     python3 ./src/vocab_mismatch/dump_dataset.py --output data_vocab/${DATASET}.txt --dataset $DATASET
# done

# train BPE
echo "TRAINING BPE";
for DATASET in "EuroPath" "EUbookshop" "ParaCrawl"; do
    # $FASTBPE_BIN getvocab data_vocab/${DATASET}.de-en.en data_vocab/${DATASET}.de-en.de > data_vocab/${DATASET}_dict.txt
    $FASTBPE_BIN learnbpe 30000 data_vocab/${DATASET}.de-en.en data_vocab/${DATASET}.de-en.de > data_vocab/${DATASET}.bpecodes
done

# clean up log file
rm -f data_vocab/compute_bpe_all.out

# run BPE (in 4 parallel threads - inner loop)
for DATASET1 in "wmt19m" "wmt19" "para_crawl" "europarl"; do
    for DATASET2 in "wmt19" "para_crawl" "europarl"; do
        echo "Running BPE trained on $DATASET1 on data from $DATASET2:";
        ./src/vocab_mismatch/encode_bpe_len.py \
            --bpecodes data_vocab/${DATASET1}.bpecodes \
            --dataset "data_vocab/${DATASET2}.de-en.en" \
            --dataset "data_vocab/${DATASET2}.de-en.de" \
            --target-dataset ${DATASET2} \
            --bpe-dataset $DATASET1 \
            >> data_vocab/compute_bpe_all.out;
    done &
done