#!/usr/bin/bash

# for SUFFIX in "uniq_small_lower" "uniq_small" "uniq" "small_sent"; do
for SUFFIX in "small_sent"; do
    echo "Submitting ${SUFFIX}";
    sbatch --time=0-4 --ntasks=40 --mem-per-cpu=2G \
        --output="logs/precompute_vocab_budget_${SUFFIX}.log" \
        --job-name="precompute_vocab_budget_${SUFFIX}" \
        --wrap="python3 ./src/figures/precompute_vocab_budget.py \
            --orig data_vocab/All.de-en/orig.tok.en.${SUFFIX}.bpe \
            --teacher data_vocab/All.de-en/orig.tok.en.${SUFFIX}.teacher.bpe \
            --output computed/overlap/wmt19m.teacher-teacher.de-en.${SUFFIX}.jsonl \
        ";
done;

echo "Submitting all"
sbatch --time=0-24 --ntasks=40 --mem-per-cpu=5G \
    --output="logs/precompute_vocab_budget_all.log" \
    --job-name="precompute_vocab_budget_all" \
    --wrap="python3 ./src/figures/precompute_vocab_budget.py \
        --orig data_vocab/All.de-en/orig.bpe.wmt19m.en \
        --teacher data_vocab/All.de-en/teacher.bpe.wmt19m.en \
        --output computed/overlap/wmt19m.teacher-teacher.de-en.all.jsonl \
    ";