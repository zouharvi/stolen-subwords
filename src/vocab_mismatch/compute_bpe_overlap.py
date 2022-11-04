#!/usr/bin/env python3

import argparse
import tqdm

args = argparse.ArgumentParser()
args.add_argument("-v1", "--vocab-1", default="data_vocab/wmt19m.de-en.vocab")
args.add_argument("-v2", "--vocab-2", default="data_vocab/All.de-en/orig.vocab")
args = args.parse_args()

def load(f):
    with open(f, "r") as f:
        data = [x.rstrip("\n") for x in f.readlines()]
    return set(data)

vocab1 = load(args.vocab_1)
vocab2 = load(args.vocab_2)

def overlap(a, b):
    return 2*len(a & b)/(len(a) + len(b))

print(f"Overlap is: {overlap(vocab1, vocab2):.1%}")