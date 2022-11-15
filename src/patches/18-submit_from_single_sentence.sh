#!/usr/bin/bash


I=0
for SENT in \
    "Stolen subwords: importance of vocabularies for machine translation model stealing" \
    "NLP models are a key intelectual property, many of which are deployed online." \
    "We present the Eyetracked Multi-Modal Translation (EMMT) corpus, a dataset containing monocular eye movement recordings, audio and 4-electrode electroencephalogram (EEG) data of 43 participants." \
    "Two roads diverged in a wood, and I- I took the one less traveled by, And that has made all the difference." \
    "One morning, when Gregor Samsa woke from troubled dreams, he found himself transformed in his bed into a horrible vermin."; \
do
    echo "Submitting ${I} \"$SENT\""
    sbatch --time=07-00 --ntasks=8 --mem-per-cpu=5G --gpus=1 \
        --output="logs/from_single_sentence_${I}.log" \
        --job-name="from_single_sentence_${I}" \
        --wrap="python3 ./src/from_one_sentence.py \
            --start-sent \"${SENT}\" \
            --vocab-out computed/from_single_sentence/sent_${I}.pkl \
        ";

    # increment counter
    I=$((I+1));
done;