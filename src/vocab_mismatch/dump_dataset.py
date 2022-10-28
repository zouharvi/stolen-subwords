#!/usr/bin/env python3

import sys
sys.path.append("src")
import utils
import argparse
import mosestokenizer

args = argparse.ArgumentParser()
args.add_argument("--output")
args.add_argument("--dataset")
args = args.parse_args()

print("Loading dataset")
data_en, data_de = utils.get_dataset(args.dataset)

tokenizer_en = mosestokenizer.MosesTokenizer("en")
tokenizer_de = mosestokenizer.MosesTokenizer("de")

with open(args.output, "w") as f:
    for l in data_en:
        f.write(" ".join(tokenizer_en(l)) + "\n")
    for l in data_de:
        f.write(" ".join(tokenizer_de(l)) + "\n")