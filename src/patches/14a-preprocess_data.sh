#!/usr/bin/bash


# scp euler:/cluster/work/sachan/vilem/vocab-stealing/data_vocab/CCAligned.de-en/{teacher,orig}.bpe.wmt19m.{en,de} data_vocab/CCAligned.de-en/

for DATASET2 in "EuroPat"; do
for DATASET1 in "All" "wmt19m" "CCAligned" "ParaCrawl" "EuroPat"; do
    for PREFIXES in "orig-teacher" "orig-orig"; do
        IFS='-' read -r -a PREFIXES <<< "${PREFIXES}";
        PREFIX1="${PREFIXES[0]}"
        PREFIX2="${PREFIXES[1]}"

        for LANGS in "en-de" "de-en"; do
            IFS='-' read -r -a LANGS <<< "${LANGS}";
            LANG1="${LANGS[0]}"
            LANG2="${LANGS[1]}"

            echo "Creating ${DATASET2} (BPE'd by ${DATASET1}) ${PREFIX1}-${PREFIX2} ${LANG1}-${LANG2}";
            TEXT_DIR="data_bin/${DATASET2}.de-en.bpe_${DATASET1}.${PREFIX1}-${PREFIX2}.${LANG1}-${LANG2}/";
            mkdir -p ${TEXT_DIR};
            TEXT_SRC="data_vocab/${DATASET2}.de-en/${PREFIX1}.bpe.${DATASET1}.${LANG1}";
            TEXT_TGT="data_vocab/${DATASET2}.de-en/${PREFIX2}.bpe.${DATASET1}.${LANG2}";
            TEXT_SRC_ORIG="data_vocab/${DATASET2}.de-en/orig.bpe.${DATASET1}.${LANG1}";
            TEXT_TGT_ORIG="data_vocab/${DATASET2}.de-en/orig.bpe.${DATASET1}.${LANG2}";

            # TODO: accidentially removed one zero
            head -n 960000 ${TEXT_SRC} > "${TEXT_DIR}/train.${LANG1}";
            tail -n 40000 ${TEXT_SRC_ORIG} | head -n 20000 > "${TEXT_DIR}/dev.${LANG1}";
            tail -n 20000 ${TEXT_SRC_ORIG} > "${TEXT_DIR}/test.${LANG1}";

            head -n 960000 ${TEXT_TGT} > "${TEXT_DIR}/train.${LANG2}";
            tail -n 40000 ${TEXT_TGT_ORIG} | head -n 20000 > "${TEXT_DIR}/dev.${LANG2}";
            tail -n 20000 ${TEXT_TGT_ORIG} > "${TEXT_DIR}/test.${LANG2}";
        done;
    done;
done;
done;

for DATASET2 in "EuroPat"; do
for DATASET1 in "All" "wmt19m" "CCAligned" "ParaCrawl" "EuroPat"; do
    for PREFIXES in "orig-teacher" "orig-orig"; do
        IFS='-' read -r -a PREFIXES <<< "${PREFIXES}";
        PREFIX1="${PREFIXES[0]}"
        PREFIX2="${PREFIXES[1]}"

        for LANGS in "en-de" "de-en"; do
            IFS='-' read -r -a LANGS <<< "${LANGS}";
            LANG1="${LANGS[0]}"
            LANG2="${LANGS[1]}"

            echo "Preprocessing ${DATASET2} (BPE'd by ${DATASET1}) ${PREFIX1}-${PREFIX2} ${LANG1}-${LANG2}";
            TEXT_DIR="data_bin/${DATASET2}.de-en.bpe_${DATASET1}.${PREFIX1}-${PREFIX2}.${LANG1}-${LANG2}/";

            sbatch --time=0-1 --ntasks=40 --mem-per-cpu=1G \
                --job-name="preprocess_${DATASET2}.de-en.bpe_${DATASET1}.${PREFIX1}-${PREFIX2}.${LANG1}-${LANG2}" \
                --output="logs/preprocess_${DATASET2}.de-en.bpe_${DATASET1}.${PREFIX1}-${PREFIX2}.${LANG1}-${LANG2}" \
                --wrap="fairseq-preprocess --source-lang $LANG1 --target-lang $LANG2 \
                --trainpref $TEXT_DIR/train --validpref $TEXT_DIR/dev --testpref $TEXT_DIR/test  \
                --destdir $TEXT_DIR \
                --bpe fastbpe \
                --joined-dictionary \
                --tokenizer moses \
                --workers 40 \
            "
        done;
    done;
done;
done;