#!/usr/bin/bash

rsync -azP --filter=":- .gitignore" --exclude .git/ . euler:/cluster/work/sachan/vilem/vocab-stealing/


# scp euler:/cluster/work/sachan/vilem/vocab-stealing/data_vocab/*.bpecodes data_vocab/
# scp euler:/cluster/work/sachan/vilem/vocab-stealing/data_vocab/All.de-en/{orig,teacher}.bpecodes data_vocab/All.de-en/
# scp euler:/cluster/work/sachan/vilem/vocab-stealing/data_vocab/All.de-en/teacher.tok.bpe.wmt19m.{en,de}} data_vocab/All.de-en/
# scp euler:/cluster/work/sachan/vilem/vocab-stealing/data_vocab/All.de-en/teacher.tok.{en,de} data_vocab/All.de-en/
# scp euler:/cluster/work/sachan/vilem/vocab-stealing/data_vocab/All.de-en/orig.tok.*{en,de} data_vocab/All.de-en/
# scp data_vocab/All.de-en/orig.tok.de.uniq euler:/cluster/work/sachan/vilem/vocab-stealing/data_vocab/All.de-en/
# scp euler:/cluster/work/sachan/vilem/vocab-stealing/data_vocab/All.de-en/orig.tok.de.uniq_small data_vocab/All.de-en/
# scp euler:/cluster/work/sachan/vilem/vocab-stealing/data_vocab/All.de-en/*teacher.bpe* data_vocab/All.de-en/
# scp euler:/cluster/work/sachan/vilem/vocab-stealing/data_vocab/All.de-en/teacher.{en,de} data_vocab/All.de-en/
# scp data_vocab/CCAligned.de-en/orig.{en,de} euler:/cluster/work/sachan/vilem/vocab-stealing/data_vocab/CCAligned.de-en/