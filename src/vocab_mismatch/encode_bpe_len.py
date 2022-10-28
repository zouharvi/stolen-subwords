#!/usr/bin/env python3

import sys
import fastBPE
import argparse
import json

args = argparse.ArgumentParser()
args.add_argument("--bpecodes")
args.add_argument("--dict")
args.add_argument("--dataset")
args.add_argument("--bpe-dataset")
args = args.parse_args()

print("Loading BPE", file=sys.stderr)
bpe_model = fastBPE.fastBPE(args.bpecodes)

print("Loading dataset", file=sys.stderr)
with open(args.dataset, "r") as f:
    data = [x.rstrip() for x in f.readlines()]

print("Encoding dataset", file=sys.stderr)
data_encoded = bpe_model.apply(data)

# debug print
# print("\n".join(data_encoded[:20]))
encoded_len = sum([x.count(" ")+1 for x in data_encoded])
print(json.dumps(
    {
        "bpe_dataset": args.bpe_dataset,
        "target_dataset": args.dataset,
        "subword_count": encoded_len
    },
    ensure_ascii=False
))
