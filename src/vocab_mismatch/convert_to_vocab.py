#!/usr/bin/env python3

import argparse
import tqdm

args = argparse.ArgumentParser()
args.add_argument("-i", "--input", default="data_vocab/wmt19m.de-en.bpecodes")
args.add_argument("-o", "--output", default="data_vocab/tmp.vocab")
args = args.parse_args()

is_bpe = args.input.endswith("bpecodes")


def load_bpe(f):
    with open(f, "r") as f:
        data_raw = list(f.readlines())
        assert all([len(l.split(" ")) == 3 for l in data_raw])
        data = [l.split(" ")[:2] for l in data_raw]
    # this is incorrect and gives overconfident results
    vocab = set([l[0] + l[1] for l in data])
    return vocab


def load_simple(f):
    print("Loading")
    out = set()
    with open(f, "r") as f:
        for l in tqdm.tqdm(f):
            l = l.rstrip("\n")
            # we should add </w> to word ending tokens
            for w in l.split(" "):
                if w.endswith("@@"):
                    out.add(w.replace("@@", ""))
                else:
                    out.add(w.replace("@@", "") + "</w>")
    return out


if is_bpe:
    data = load_bpe(args.input)
else:
    data = load_simple(args.input)

print("Loaded", len(data), "items")

with open(args.output, "w") as f:
    for v in data:
        f.write(v + "\n")
