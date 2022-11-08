#!/usr/bin/env python3

import argparse
import numpy as np
import sacremoses
import tqdm
import multiprocessing
pool = multiprocessing.Pool()

args = argparse.ArgumentParser()
args.add_argument(
    "-i1", "--input-1", default=None,
)
args.add_argument(
    "-i2", "--input-2", default=None,
)
args = args.parse_args()

tokenizer_en = sacremoses.MosesTokenizer("en")
tokenizer_de = sacremoses.MosesTokenizer("de")

print("Loading lines")
with open(args.input_1, "r") as f:
    data1 = list(f.readlines()[:10_000_000])
with open(args.input_2, "r") as f:
    data2 = list(f.readlines()[:10_000_000])

print("Computing chars")
chars1 = set()
for l in tqdm.tqdm(data1):
    chars1 |= set(l)
chars2 = set()
for l in tqdm.tqdm(data2):
    chars2 |= set(l)

print("Computing unique characters...")
print("Unique English characters:", len(chars1))
print("Unique German characters:", len(chars2))
print("Unique combined characters:", len(chars1 | chars2))

# free memory
del chars1
del chars2

print("Computing line lengths")
avg_line_chars_en = np.average([len(l) for l in data1])
avg_line_chars_de = np.average([len(l) for l in data2])
avg_line_chars = np.average([len(l) for l in data1 + data2])
print(f"Each line has on average {avg_line_chars:.1f} chars (combined)")
print(f"Each line has on average {avg_line_chars_en:.1f} chars (English)")
print(f"Each line has on average {avg_line_chars_de:.1f} chars (German)")

print("Tokenizing 1")
tokenized1 = list(pool.map(tokenizer_en.tokenize, tqdm.tqdm(data1)))
print("Tokenizing 2")
tokenized2 = list(pool.map(tokenizer_de.tokenize, tqdm.tqdm(data2)))

# avoid allocation
avg_line_words = np.average(
    [len(l) for l in tokenized1] + [len(l) for l in tokenized2])
avg_line_words_en = np.average([len(l) for l in tokenized1])
avg_line_words_de = np.average([len(l) for l in tokenized2])
print(f"Each line has on average {avg_line_words:.1f} words (combined)")
print(f"Each line has on average {avg_line_words_en:.1f} words (English)")
print(f"Each line has on average {avg_line_words_de:.1f} words (German)")

print("Computing unique words...")
words1 = [w.lower() for l in tokenized1 for w in l]
words2 = [w.lower() for l in tokenized2 for w in l]

# free memory
del tokenized1
del tokenized2

words1 = set(words1)
words2 = set(words2)

print("Unique English words:", len(words1))
print("Unique German words:", len(words2))
print("Unique combined words:", len(words1 | words2))
