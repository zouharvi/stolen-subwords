#!/usr/bin/bash

# merge
for DATASET in "EuroPat" "EUbookshop" "ParaCrawl"; do
    for LANG in "en" "de"; do
        echo "Merging ${DATASET}.${LANG}"; 
        SRC="data_vocab/${DATASET}.de-en/teacher."{0,1,2,3,4,5,6,7,8,9}".${LANG}";
        TGT="data_vocab/${DATASET}.de-en/teacher.${LANG}";
        sbatch --time=0-4 --ntasks=5 --mem-per-cpu=10G \
            --output="logs/merge_${DATASET}.${LANG}.log" \
            --job-name="merge_${DATASET}.${LANG}" \
            --wrap="cat $SRC > $TGT";
    done;
done;

# copy locally for backup
for DATASET in "EuroPat" "EUbookshop" "ParaCrawl"; do
    mkdir -p "data_backup/${DATASET}.de-en"
    echo "Merging ${DATASET}"; 
    scp \
        "euler:/cluster/work/sachan/vilem/vocab-stealing/data_vocab/$DATASET.de-en/teacher.*.{en,de}" \
        "data_backup/${DATASET}.de-en/";
done;


# remove temporary
for DATASET in "EuroPat" "EUbookshop" "ParaCrawl"; do
    echo "Removing ${DATASET}"; 
    rm "data_vocab/${DATASET}.de-en/teacher."{0,1,2,3,4,5,6,7,8,9}"."{en,de};
done;

# join all in All
for DATASET in "EuroPat" "EUbookshop" "ParaCrawl"; do
    for LANG in "en" "de"; do
        echo "Joining ${DATASET}.${LANG}"; 
        cat "data_vocab/${DATASET}.de-en/teacher.${LANG}" >> "data_vocab/All.de-en/teacher.${LANG}";
    done;
done;