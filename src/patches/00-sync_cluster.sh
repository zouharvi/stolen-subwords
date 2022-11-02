#!/usr/bin/bash

rsync -azP --filter=":- .gitignore" --exclude .git/ . euler:/cluster/work/sachan/vilem/nonsense-to-nonsense/


# scp euler:/cluster/work/sachan/vilem/vocab-stealing/data_vocab/*.bpecodes data_vocab/
# scp euler:/cluster/work/sachan/vilem/vocab-stealing/data_vocab/All.de-en/{orig,teacher}.bpecodes data_vocab/All.de-en/
# scp euler:/cluster/work/sachan/vilem/vocab-stealing/data_vocab/All.de-en/teacher.tok.bpe.wmt19m.* data_vocab/All.de-en/