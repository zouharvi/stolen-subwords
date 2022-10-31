#!/usr/bin/env python3

import argparse

import tqdm

# python3 ./src/vocab_mismatch/bilen_cleaner.py \
#     -i1 ./data_vocab/EUbookshop.de-en.en \
#     -i2 ./data_vocab/EUbookshop.de-en.de \
#     -o1 ./data_vocab/EUbookshop.de-en/orig.en \
#     -o2 ./data_vocab/EUbookshop.de-en/orig.de;

args = argparse.ArgumentParser()
args.add_argument(
    "-i1", "--input-1", default=None,
)
args.add_argument(
    "-i2", "--input-2", default=None,
)
args.add_argument(
    "-o1", "--output-1", default=None,
)
args.add_argument(
    "-o2", "--output-2", default=None,
)
args = args.parse_args()

fin1 = open(args.input_1, "r")
fin2 = open(args.input_2, "r")
fou1 = open(args.output_1, "w")
fou2 = open(args.output_2, "w")

lens_a = []
lens_b = []
for a, b in tqdm.tqdm(zip(fin1, fin2)):
    a = a.rstrip()
    b = b.rstrip()
    # a = a.replace("."*10, ".")
    # b = b.replace("."*10, ".")
    # a = a.replace(". "*5, ".")
    # b = b.replace(". "*5, ".")
    if len(a) >= 1000 or len(b) >= 1000:
        continue
        print(a)
        print("==")
        print(b)
    fou1.write(a + "\n")
    fou2.write(b + "\n")
    lens_a.append(len(a))
    lens_b.append(len(b))

print(max(lens_a), max(lens_b))

