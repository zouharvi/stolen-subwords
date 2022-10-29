|date|status|nickname|comment|command|
|-|-|-|-|-|
|20-10-2022|to run||compute BPE efficiency|`sbatch --time=0-4 --ntasks=6 --mem-per-cpu=6G ./src/vocab_mismatch/compute_bpe_len.sh`|
|20-10-2022|running||apply bpe|`./src/vocab_mismatch/encode_bpe.sh`|
|20-10-2022|ok||tokenize data|`sbatch --time=0-4 --ntasks=15 --mem-per-cpu=2G ./src/vocab_mismatch/train_bpe.sh`|
|20-10-2022|ok||tokenize data|`sbatch --time=0-4 --ntasks=15 --mem-per-cpu=3G ./src/vocab_mismatch/tokenize_data.sh`|
|07-10-2022|ok||teacher translate word_3gram en->de|`bsub -W 20:00 -n 4 -R "rusage[mem=4096,ngpus_excl_p=1]" ./src/teacher_translate.py -i data/word_3gram_en.${i}.txt -o data/word_3gram_ende.${i}.txt`|
|07-10-2022|ok||teacher translate wmt21 en->de|`bsub -W 20:00 -n 4 -R "rusage[mem=4096,ngpus_excl_p=1]" ./src/teacher_translate.py -i /cluster/home/vzouhar/.sacrebleu/wmt21/wmt21.en-de.src -o data/wmt21.en-de.teacher-tgt`|