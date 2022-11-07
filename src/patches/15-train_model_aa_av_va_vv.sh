#!/usr/bin/bash


DATASET1="wmt19m";
DATASET2="CCAligned";

# for LANGS in "en-de" "de-en"; do
for LANGS in "en-de"; do
    IFS='-' read -r -a LANGS <<< "${LANGS}";
    LANG1="${LANGS[0]}"
    LANG2="${LANGS[1]}"
    for PREFIX1 in "orig" "teacher"; do
    for PREFIX2 in "orig" "teacher"; do

        SIGNATURE="${DATASET2}.de-en.bpe_${DATASET1}.${PREFIX1}-${PREFIX2}.${LANG1}-${LANG2}";
        TEXT_DIR="data_bin/${SIGNATURE}/";

        sbatch --time=07-00 --ntasks=8 --mem-per-cpu=4G --gpus=1 \
            --job-name="train_student_${SIGNATURE}" \
            --output="logs/train_student_${SIGNATURE}.log" \
            --wrap="CUDA_VISIBLE_DEVICES=0 fairseq-train \
                $TEXT_DIR \
                --arch transformer_iwslt_de_en --share-decoder-input-output-embed \
                --optimizer adam --adam-betas '(0.9, 0.98)' --clip-norm 0.5 \
                --lr 5e-4 --lr-scheduler inverse_sqrt --warmup-updates 4000 \
                --dropout 0.3 --weight-decay 0.0001 \
                --criterion label_smoothed_cross_entropy --label-smoothing 0.1 \
                --max-tokens 4096 \
                --eval-bleu \
                --save-dir \"$TEXT_DIR/checkpoints\" \
                --eval-bleu-args '{\"beam\": 5, \"max_len_a\": 1.2, \"max_len_b\": 10}' \
                --eval-bleu-detok moses \
                --eval-bleu-remove-bpe \
                --bpe fastbpe \
                --eval-bleu-print-samples \
                --best-checkpoint-metric bleu --maximize-best-checkpoint-metric \
                --fp16 \
            "
    done;
    done;
done;

# TODO: batch-size?

# TEXT_DIR="data_bin/CCAligned.de-en.bpe_wmt19m.orig-orig.en-de";
# fairseq-train \
#     $TEXT_DIR \
#     --arch transformer_iwslt_de_en --share-decoder-input-output-embed \
#     --optimizer adam --adam-betas '(0.9, 0.98)' --clip-norm 0.5 \
#     --lr 5e-4 --lr-scheduler inverse_sqrt --warmup-updates 4000 \
#     --dropout 0.3 --weight-decay 0.0001 \
#     --criterion label_smoothed_cross_entropy --label-smoothing 0.1 \
#     --max-tokens 4096 \
#     --eval-bleu \
#     --save-dir $TEXT_DIR/checkpoints \
#     --eval-bleu-args '{"beam": 5, "max_len_a": 1.2, "max_len_b": 10}' \
#     --eval-bleu-detok moses \
#     --eval-bleu-remove-bpe \
#     --bpe fastbpe \
#     --eval-bleu-print-samples \
#     --best-checkpoint-metric bleu --maximize-best-checkpoint-metric \
#     --fp16