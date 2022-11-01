#!/usr/bin/env python3

import argparse
import tqdm

args = argparse.ArgumentParser()
args.add_argument("--bpe-1", default="data_vocab/wmt19m.de-en.bpecodes")
args.add_argument("--bpe-2", default="data_vocab/All.de-en/self.bpecodes")
args.add_argument("--bpe-2-simple", action="store_true")
args = args.parse_args()

def load(f):
    with open(f, "r") as f:
        data_raw = list(f.readlines())
        assert all([len(l.split(" ")) == 3 for l in data_raw])
        data = [l.split(" ")[:2] for l in data_raw]
    # this is incorrect and gives overconfident results
    vocab = set([l[0].replace("</w>", "") +l[1].replace("</w>", "")  for l in data])
    print("Loaded", len(vocab))
    return vocab

def load_simple(f):
    with open(f, "r") as f:
        data = list(f.readlines())
    print("stripping")
    data = [l.rstrip("\n") for l in data]
    print("splitting")
    out = set()
    for l in tqdm.tqdm(data):
        # we should add </w> to word ending tokens
        l = [w.replace("@@", "") for w in l.split(" ")]
        out |= set(l)
    return out
    

def overlap(v1, v2):
    return 2*len(v1 & v2) / (len(v1)+len(v2))

vocab1 = load(args.bpe_1)
if args.bpe_2_simple:
    vocab2 = load_simple(args.bpe_2)
else:
    vocab2 = load(args.bpe_2)

print(f"Overlap is: {overlap(vocab1, vocab2):.1%}")