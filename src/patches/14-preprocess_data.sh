#!/usr/bin/bash


# scp euler:/cluster/work/sachan/vilem/vocab-stealing/data_vocab/CCAligned.de-en/{teacher,orig}.bpe.wmt19m.{en,de} data_vocab/CCAligned.de-en/

# for DATASET2 in "ParaCrawl" "EuroPat" "CCAligned"; do
for DATASET2 in "CCAligned"; do
    DATASET1=wmt19m;
    for PREFIX1 in "orig" "teacher"; do
    for PREFIX2 in "orig" "teacher"; do
        for LANGS in "en-de" "de-en"; do
            IFS='-' read -r -a LANGS <<< "${LANGS}";
            LANG1="${LANGS[0]}"
            LANG2="${LANGS[1]}"

            echo "Creating ${DATASET2} (BPE'd by ${DATASET1}) ${PREFIX1}-${PREFIX2} ${LANG1}-${LANG2}";
            TEXT_DIR="data_bin/${DATASET2}.de-en.bpe_${DATASET1}.${PREFIX1}-${PREFIX2}.${LANG1}-${LANG2}/";
            mkdir -p ${TEXT_DIR};
            TEXT_SRC="data_vocab/${DATASET2}.de-en/${PREFIX1}.bpe.${DATASET1}.${LANG1}";
            TEXT_TGT="data_vocab/${DATASET2}.de-en/${PREFIX2}.bpe.${DATASET1}.${LANG2}";

            head -n 950000 ${TEXT_SRC} > "${TEXT_DIR}/train.${LANG1}";
            tail -n 50000 ${TEXT_SRC} | head -n 25000 > "${TEXT_DIR}/dev.${LANG1}";
            tail -n 25000 ${TEXT_SRC} > "${TEXT_DIR}/test.${LANG1}";

            head -n 950000 ${TEXT_TGT} > "${TEXT_DIR}/train.${LANG2}";
            tail -n 50000 ${TEXT_TGT} | head -n 25000 > "${TEXT_DIR}/dev.${LANG2}";
            tail -n 25000 ${TEXT_TGT} > "${TEXT_DIR}/test.${LANG2}";
        done;
    done;
    done;
done;

for DATASET2 in "ParaCrawl" "EuroPat" "CCAligned"; do
    DATASET1=wmt19m;
    for PREFIX1 in "orig" "teacher"; do
    for PREFIX2 in "orig" "teacher"; do
        for LANGS in "en-de" "de-en"; do
            IFS='-' read -r -a LANGS <<< "${LANGS}";
            LANG1="${LANGS[0]}"
            LANG2="${LANGS[1]}"

            echo "Preprocessing ${DATASET2} (BPE'd by ${DATASET1}) ${PREFIX1}-${PREFIX2} ${LANG1}-${LANG2}";
            TEXT_DIR="data_bin/${DATASET2}.de-en.bpe_${DATASET1}.${PREFIX1}-${PREFIX2}.${LANG1}-${LANG2}/";

            fairseq-preprocess --source-lang $LANG1 --target-lang $LANG2 \
                --trainpref $TEXT_DIR/train --validpref $TEXT_DIR/dev --testpref $TEXT_DIR/test  \
                --destdir $TEXT_DIR \
                --bpe fastbpe \
                --joined-dictionary \
                --tokenizer moses \
                --workers 40;
        done;
    done;
    done &
done;

wait