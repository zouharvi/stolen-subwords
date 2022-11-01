#!/usr/bin/bash

rsync -azP --filter=":- .gitignore" --exclude .git/ . euler:/cluster/work/sachan/vilem/nonsense-to-nonsense/


# scp euler:/cluster/work/sachan/vilem/nonsense-to-nonsense/data_vocab/*.bpecodes data_vocab/
# scp euler:/cluster/work/sachan/vilem/nonsense-to-nonsense/data_vocab/All.de-en/self.bpecodes data_vocab/All.de-en/
# scp euler:/cluster/work/sachan/vilem/nonsense-to-nonsense/data_vocab/All.de-en/teacher_small.bpecodes data_vocab/All.de-en/
# scp euler:/cluster/work/sachan/vilem/nonsense-to-nonsense/data_vocab/All.de-en/teacher_small.tok.bpe.wmt19m.* data_vocab/All.de-en/