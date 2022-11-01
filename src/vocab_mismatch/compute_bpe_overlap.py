#!/usr/bin/env python3

import argparse
import fastBPE

args = argparse.ArgumentParser()
args.add_argument("--bpe-1", default="data_vocab/wmt19m.de-en.bpecodes")
args.add_argument("--bpe-2", default="data_vocab/All.de-en/self.bpecodes")
args = args.parse_args()

def load(f):
    m = fastBPE.fastBPE(f)
    with open(f, "r") as f:
        data_raw = list(f.readlines())
        assert all([len(l.split(" ")) == 3 for l in data_raw])
        data = [l.split(" ")[:2] for l in data_raw]
    vocab = set([l[0]+l[1] for l in data])
    return m, vocab

def overlap(v1, v2):
    return 2*len(v1 & v2) / (len(v1)+len(v2))

m1, vocab1 = load(args.bpe_1)
m2, vocab2 = load(args.bpe_2)

print(f"Overalp is: {overlap(vocab1, vocab2):.1%}")