#!/usr/bin/bash

# generate source data (parallel)
# bsub 
for ((i=0; i < 10; i++)); do 
    ./src/data_generation/main.py \
        -n 100 -g word_ngram_en \
        --ngram 3 -o data/word_3gram_en.${i}.txt \
        --seed $i 2> /dev/null &
done

# TODO sync before here
cat data/word_3gram_en.*.txt > data/word_3gram_en.txt

# eval data
# /cluster/home/vzouhar/.sacrebleu/wmt21/wmt21.en-de.src
sacrebleu --download wmt21 --language-pair en-de
cat ~/.sacrebleu/wmt21/wmt21.en-de.src

# teacher translate
for ((i=0; i < 10; i++)); do 
    bsub -W 20:00 -n 4 -R "rusage[mem=4096,ngpus_excl_p=1]" \
        ./src/teacher_translate.py \
        -i data/word_3gram_en.${i}.txt -o data/word_3gram_ende.${i}.txt ;
done

# translate WMT21 test set 
bsub -W 4:00 -n 4 -R "rusage[mem=4096,ngpus_excl_p=1]" \
    ./src/teacher_translate.py \
    -i /cluster/home/vzouhar/.sacrebleu/wmt21/wmt21.en-de.src -o data/wmt21.en-de.teacher-tgt

# evaluate teacher
sacrebleu -t wmt21 -l en-de < data/wmt21.en-de.teacher-tgt

# train & apply sentencepiece to train data
./src/apply_bpe.py --train \
    --i "data/proof_of_concept/word_3gram.de" \
    --i "data/proof_of_concept/word_3gram.en" \
    --o "data/proof_of_concept/word_3gram_bpe.de" \
    --o "data/proof_of_concept/word_3gram_bpe.en"
    
# apply sentencepiece to valid data
./src/apply_bpe.py \
    --i "data/proof_of_concept/wmt21.de" \
    --i "data/proof_of_concept/wmt21.en" \
    --o "data/proof_of_concept/wmt21_bpe.de" \
    --o "data/proof_of_concept/wmt21_bpe.en"

# train a student model
# /home/vilda/.cache/torch/pytorch_fairseq/0695ef328ddefcb8cbcfabc3196182f59c0e41e0468b10cc0db2ae9c91881fcc.bb1be17de4233e13870bd7d6065bfdb03fca0a51dd0f5d0b7edf5c188eda71f1/
TEXT=data/proof_of_concept
fairseq-preprocess --source-lang en --target-lang de \
    --trainpref $TEXT/word_3gram_bpe --validpref $TEXT/wmt21_bpe  \
    --destdir $TEXT \
    --bpe sentencepiece \
    --joined-dictionary \
    --tokenizer moses \
    --workers 12

CUDA_VISIBLE_DEVICES=0 fairseq-train \
    $TEXT \
    --arch transformer_iwslt_de_en --share-decoder-input-output-embed \
    --optimizer adam --adam-betas '(0.9, 0.98)' --clip-norm 0.5 \
    --lr 5e-4 --lr-scheduler inverse_sqrt --warmup-updates 4000 \
    --dropout 0.3 --weight-decay 0.0001 \
    --criterion label_smoothed_cross_entropy --label-smoothing 0.1 \
    --max-tokens 4096 \
    --eval-bleu \
    --eval-bleu-args '{"beam": 5, "max_len_a": 1.2, "max_len_b": 10}' \
    --eval-bleu-detok moses \
    --eval-bleu-remove-bpe sentencepiece \
    --eval-bleu-print-samples \
    --best-checkpoint-metric bleu --maximize-best-checkpoint-metric \
    --fp16