#!/usr/bin/env python3

import argparse
import tqdm

args = argparse.ArgumentParser()
args.add_argument(
    "-i", "--input", default="data_vocab/wmt19m.de-en.tok.en.uniq")
args.add_argument("-o", "--output", default=None)
args = args.parse_args()

with open(args.input, "r") as f:
    vocab_orig = [x.strip() for x in f.readlines()]

# sort by length
vocab_orig.sort(key=lambda x: len(x), reverse=True)
existing = set()

print("Original length:", len(vocab_orig))

for i in range(1):
    vocab_new = set()
    for w in tqdm.tqdm(vocab_orig):
        if w not in existing:
            vocab_new.add(w)

            # prefix & suffix
            # for i in range(1, len(w)):
            #     existing.add(w[:i])
            # for i in range(1, len(w) - 1):
            #     existing.add(w[i:])

            # all substring
            for i in range(len(w) - 1):
                for j in range(i + 1, len(w)):
                    existing.add(w[i:j])

print("New length:", len(vocab_new))

if args.output is None:
    args.output = args.input.replace(".uniq", ".uniq_small")

with open(args.output, "w") as f:
    for v in vocab_new:
        f.write(v + "\n")
