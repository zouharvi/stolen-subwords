#!/usr/bin/bash

rsync -azP --filter=":- .gitignore" --exclude .git/ . euler:/cluster/work/sachan/vilem/vocab-stealing/


# scp euler:/cluster/work/sachan/vilem/vocab-stealing/data_vocab/*.bpecodes data_vocab/
# scp euler:/cluster/work/sachan/vilem/vocab-stealing/data_vocab/All.de-en/teacher.bpecodes data_vocab/All.de-en/
# scp euler:/cluster/work/sachan/vilem/vocab-stealing/data_vocab/All.de-en/{teacher,orig}.tok.{en,de} data_vocab/All.de-en/
# scp data_vocab/All.de-en/orig.tok.{en,de}.{uniq,uniq_small} euler:/cluster/work/sachan/vilem/vocab-stealing/data_vocab/All.de-en/