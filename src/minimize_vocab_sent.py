#!/usr/bin/env python3

import argparse
import tqdm

args = argparse.ArgumentParser()
args.add_argument(
    "-i", "--input", default="data_vocab/All.de-en/orig.tok.en"
)
args.add_argument(
    "-o", "--output", default="data_vocab/All.de-en/orig.tok.small_sent.en"
)
args = args.parse_args()

vocab_seen = set()

fin = open(args.input, "r")
fout = open(args.output, "w")
vocab_new = set()
vocab_old_size = 0

for line in tqdm.tqdm(fin):
    line = line.rstrip("\n").split(" ")
    vocab_old_size += len(line)
    line_new = [w for w in line if w not in vocab_new]
    vocab_new |= set(line_new)

    if len(line_new) != 0:
        fout.write(" ".join(line_new) + "\n")

print("Old length:", vocab_old_size)
print("New length:", len(vocab_new))