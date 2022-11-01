#!/usr/bin/bash

rsync -azP --filter=":- .gitignore" --exclude .git/ . euler:/cluster/work/sachan/vilem/nonsense-to-nonsense/


scp euler:/cluster/work/sachan/vilem/nonsense-to-nonsense/data_vocab/All.de-en/self.bpecodes data_vocab/All.de-en/