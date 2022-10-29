#!/usr/bin/env python3

import sys
import argparse
import json
import tqdm

args = argparse.ArgumentParser()
args.add_argument("--dataset", nargs="+")
args.add_argument("--target-dataset")
args.add_argument("--bpe-dataset")
args = args.parse_args()

# debug print
# print("\n".join(data_encoded[:20]))
encoded_len = 0
for f in args.dataset:
    print("Loading dataset", file=sys.stderr)
    with open(f, "r") as f:
        data = [x.rstrip() for x in tqdm.tqdm(f.readlines())]
    print("Computing encoded len", file=sys.stderr)
    encoded_len += sum([x.count(" ")+1 for x in tqdm.tqdm(data)])

print(json.dumps(
    {
        "bpe_dataset": args.bpe_dataset,
        "target_dataset": args.target_dataset,
        "subword_count": encoded_len
    },
    ensure_ascii=False
))
