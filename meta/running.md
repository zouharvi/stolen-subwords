|date|status|nickname|comment|command|
|-|-|-|-|-|
|07-10-2022|running||teacher translate word_3gram en->de|`bsub -W 20:00 -n 4 -R "rusage[mem=4096,ngpus_excl_p=1]" ./src/teacher_translate.py -i data/word_3gram_en.${i}.txt -o data/word_3gram_ende.${i}.txt`|
|07-10-2022|running||teacher translate wmt21 en->de|`bsub -W 20:00 -n 4 -R "rusage[mem=4096,ngpus_excl_p=1]" ./src/teacher_translate.py -i /cluster/home/vzouhar/.sacrebleu/wmt21/wmt21.en-de.src -o data/wmt21.en-de.teacher-tgt`|