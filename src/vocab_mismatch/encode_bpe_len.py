#!/usr/bin/env python3

import sys
import fastBPE
import argparse
import json

args = argparse.ArgumentParser()
args.add_argument("--bpecodes")
args.add_argument("--dataset", nargs="+")
args.add_argument("--target-dataset")
args.add_argument("--bpe-dataset")
args = args.parse_args()

print("Loading BPE", file=sys.stderr)
bpe_model = fastBPE.fastBPE(args.bpecodes)

print("Loading dataset", file=sys.stderr)


# debug print
# print("\n".join(data_encoded[:20]))
encoded_len = 0
for f in args.dataset:
    with open(f, "r") as f:
        data = [x.rstrip() for x in f.readlines()]
    print("Encoding dataset", file=sys.stderr)
    data_encoded = bpe_model.apply(data)
    encoded_len += sum([x.count(" ")+1 for x in data_encoded])

print(json.dumps(
    {
        "bpe_dataset": args.bpe_dataset,
        "target_dataset": args.target_dataset,
        "subword_count": encoded_len
    },
    ensure_ascii=False
))
