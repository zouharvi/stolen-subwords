#!/usr/bin/bash

WMT19_ENDE="/home/vilda/.cache/torch/pytorch_fairseq/0695ef328ddefcb8cbcfabc3196182f59c0e41e0468b10cc0db2ae9c91881fcc.bb1be17de4233e13870bd7d6065bfdb03fca0a51dd0f5d0b7edf5c188eda71f1"
WMT19_DEEN="/home/vilda/.cache/torch/pytorch_fairseq/4055d1c0156ceff4279bd3fadfcf7d44ad3005887c16edc7ebc7e36db5559e99.3838a6fe86bebad87be65f7945fd8a8891d2601571ca4fd815f514974eac0dbc"

# for DATASET in "EuroPat" "EUbookshop" "ParaCrawl"; do
for DATASET in "EuroPat"; do
    fairseq-generate data_vocab/${DATASET}.de-en/bin \
        --path "${WMT19_ENDE}/model1.pt" \
        --beam 5 --remove-bpe \
        --bpe fastbpe \
        --encoder-embed-dim 28904 \
        --source-lang "en" --target-lang "de"
        # --dict "${WMT19_PATH}/bpecodes"

    # --batch-size 
done;