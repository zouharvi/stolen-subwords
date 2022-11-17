|start date|status|nickname|comment|command|
|-|-|-|-|-|
|17-11-2022|ok||preprocess EuroPat|`./src/patches/14a-preprocess_data.sh`|
|17-11-2022|failed, running||train students on EuroPat (orig-teacher -*, orig-orig -EuroPat)|`./src/patches/15-students_base.sh`|
|17-11-2022|running||train students on ParaCrawl (orig-teacher -*, orig-orig -ParaCrawl)|`./src/patches/15-students_base.sh`|
|17-11-2022|ok||preprocess ParaCrawl & EuroPat|`./src/patches/14a-preprocess_data.sh`|
|17-11-2022|ok||apply bpe (ParaCrawl EuroPat)|`./src/patches/06-apply_bpe.sh`|
|16-11-2022|ok||precompute vocab budget|`./src/patches/17-submit_precompute_vocab_budget.sh`|
|16-11-2022|ok||translate & encode vocab (small_sent)|`./src/patches/11-translate_encode_vocabs.sh`|
|16-11-2022|ok||apply bpe single|`./src/patches/06-apply_bpe.sh`|
|14-11-2022|running||from single sentence (0..4)|`./src/patches/18-submit_from_single_sentence.sh`|
|10-11-2022|ok||train students on CCAligned (-All, -ParaCrawl, -EuroPat)|`./src/patches/15-students_base.sh`|
|08-11-2022|ok||train students on CCAligned (-wmt19m, -CCAligned)|`./src/patches/15-students_base.sh`|
|08-11-2022|ok||preprocessing data CCAligned-CCAligned|`./src/patches/14-preprocess_data.sh`|
|07-11-2022|ok||preprocessing data|`sbatch --time=01-00 --ntasks=100 --mem-per-cpu=1GB --output="logs/preprocess_table_2" ./src/patches/14-preprocess_data.sh`|
|07-11-2022|ok||translate & encode vocab|`./src/patches/11-translate_encode_vocabs.sh`|
|07-11-2022|ok||apply BPE CC teacher|`./src/patches/06-apply_bpe.sh`|
|07-11-2022|ok||train BPE CC teacher|`./src/patches/05-train_bpe.sh`|
|07-11-2022|ok||minimize vocab|`sbatch --time=0-4 --ntasks=50 --mem-per-cpu=1500M --job-name="minimize vocab" ./src/patches/13-minimize_vocab.sh`|
|07-11-2022|ok||apply bpe (All.teacher)|`./src/apply_bpe.sh`|
|04-11-2022|ok||dataset overview (All)|`./src/patches/08-submit_overview_datasets.sh`|
|04-11-2022|ok||tokenize (CCAligned.teacher)|`./src/patches/04-tokenize_data.sh`|
|04-11-2022|ok||train bpe (All.teacher)|`./src/patches/05-train_bpe.sh`|
|03-11-2022|ok||encode bpe (to/from CCAligned, from All)|`./src/patches/06-apply_bpe.sh`|
|03-11-2022|ok||train bpe (All, CCAligned)|`./src/patches/05-train_bpe.sh`|
|03-11-2022|ok||translate CCAligned (fast micro)|`./src/patches/03-submit_translate_datasets.sh`|
|03-11-2022|ok||tokenize CCAligned|`./src/patches/04-tokenize_data.sh`|
|03-11-2022|ok, ok||dataset overview (All, CCAligned)|`./src/patches/08-submit_overview_datasets.sh`|
|02-11-2022|ok||translate & encode vocab|`./src/patches/11-translate_encode_vocabs.sh"`|
|02-11-2022|ok||minimize data data|`sbatch --time=0-4 --ntasks=10 --mem-per-cpu=8G --wrap="python3 ./src/minimize_vocab.py -i data_vocab/All.de-en/orig.tok.de.uniq"`|
|02-11-2022|ok||tokenize data|`./src/patches/04-tokenize_data.sh`|
|01-11-2022|ok, ok||encode bpe (All)|`./src/patches/06-apply_bpe.sh`|
|01-11-2022|ok, ok||train bpe|`./src/patches/05-train_bpe.sh`|
|01-11-2022|ok||tokenize data|`sbatch --time=0-4 --ntasks=32 --mem-per-cpu=1G ./src/patches/04-tokenize_data.sh`|
|01-11-2022|ok||dataset overview|`./src/patches/08-submit_overview_datasets.sh`|
|30-10-2022|ok||translate datasets|`./src/patches/03-submit_translate_datasets.sh`|
|29-10-2022|ok||compute BPE efficiency|`sbatch --time=0-4 --ntasks=6 --mem-per-cpu=6G ./src/compute_bpe_len.sh`|
|29-10-2022|ok||apply bpe|`./src/apply_bpe.sh`|
|29-10-2022|ok||tokenize data|`sbatch --time=0-4 --ntasks=15 --mem-per-cpu=2G ./src/train_bpe.sh`|
|29-10-2022|ok||tokenize data|`sbatch --time=0-4 --ntasks=15 --mem-per-cpu=3G ./src/tokenize_data.sh`|
|07-10-2022|ok||teacher translate word_3gram en->de|`bsub -W 20:00 -n 4 -R "rusage[mem=4096,ngpus_excl_p=1]" ./src/teacher_translate.py -i data/word_3gram_en.${i}.txt -o data/word_3gram_ende.${i}.txt`|
|07-10-2022|ok||teacher translate wmt21 en->de|`bsub -W 20:00 -n 4 -R "rusage[mem=4096,ngpus_excl_p=1]" ./src/teacher_translate.py -i /cluster/home/vzouhar/.sacrebleu/wmt21/wmt21.en-de.src -o data/wmt21.en-de.teacher-tgt`|