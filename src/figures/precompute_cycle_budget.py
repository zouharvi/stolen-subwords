#!/usr/bin/env python3

import argparse
import collections
import math
import numpy as np
import pickle
import json

# scp euler:/cluster/work/sachan/vilem/vocab-stealing/computed/from_single_sentence/* computed/from_single_sentence/

args = argparse.ArgumentParser()
args.add_argument(
    "--logs", nargs="+",
    default=[
        "computed/from_single_sentence/sent_0.pkl",
        "computed/from_single_sentence/sent_1.pkl",
        "computed/from_single_sentence/sent_2.pkl",
        "computed/from_single_sentence/sent_3.pkl",
    ]
)
args.add_argument(
    "-o", "--output",
    default="computed/computed/from_single_sentence/precomputed.jsonl"
)
args.add_argument(
    "--vocab-victim",
    default="data_vocab/wmt19m.de-en.vocab"
)
args = args.parse_args()


def load_logs(f):
    with open(f, "rb") as f:
        data = pickle.load(f)
    return data


data = [load_logs(x) for x in args.logs]


def load_vocab(f):
    with open(f, "r") as f:
        data = [x.rstrip("\n") for x in f.readlines()]
    return set(data)


vocab_victim = load_vocab(args.vocab_victim)


def overlap(a, b):
    return 2 * len(a & b) / (len(a) + len(b))


def debpe(v):
    out = set()
    for w in v:
        if w.endswith("@@"):
            out.add(w[:-2])
        else:
            out.add(w + "</w>")
    return v


output = {
    "self_overlap_bpe": collections.defaultdict(list),
    "self_overlap_word": collections.defaultdict(list),
    "victim_overlap_bpe": collections.defaultdict(list),
}

for d1_i, d1_local in enumerate(data):
    d1_bpe_keys = list(d1_local["a_bpe"].keys())
    for d1_key in d1_bpe_keys:
        d_key_round = int(str(d1_key)[0]) * 10**math.floor(math.log10(d1_key))
        vocab = debpe(d1_local["a_bpe"][d1_key] | d1_local["b_bpe"][d1_key])
        overlap_victim = overlap(vocab, vocab_victim)
        output["victim_overlap_bpe"][d_key_round].append(overlap_victim)

    for d2_i, d2_local in enumerate(data[d1_i + 1:]):
        d2_bpe_keys = list(d2_local["a_bpe"].keys())
        for d1_key, d2_key in zip(d1_bpe_keys, d2_bpe_keys):
            overlap_bpe_v = overlap(
                d1_local["a_bpe"][d1_key] | d1_local["b_bpe"][d1_key],
                d2_local["a_bpe"][d2_key] | d2_local["b_bpe"][d2_key],
            )
            overlap_word_v = overlap(
                d1_local["a"][d1_key] | d1_local["b"][d1_key],
                d2_local["a"][d2_key] | d2_local["b"][d2_key],
            )
            # this is an incredibly bad way of doing rounding
            d_key_round = int(str(d1_key)[0]) * \
                10**math.floor(math.log10(d1_key))
            output["self_overlap_bpe"][d_key_round].append(overlap_bpe_v)
            output["self_overlap_word"][d_key_round].append(overlap_word_v)


def average_keys(output_local):
    return {
        k: np.average(v)
        for k, v in output_local.items()
    }


def maximize_keys(output_local):
    return {
        k: np.max(v)
        for k, v in output_local.items()
    }


output = {
    k + "_avg": average_keys(v) for k, v in output.items()
} | {
    k + "_max": maximize_keys(v) for k, v in output.items()
}

for k, v in output["self_overlap_bpe_avg"].items():
    print(k, f"{v:.2%}")

print()

for k, v in output["self_overlap_bpe_max"].items():
    print(k, f"{v:.2%}")

print()

for k, v in output["self_overlap_word_avg"].items():
    print(k, f"{v:.2%}")
print()

for k, v in output["victim_overlap_bpe_max"].items():
    print(k, f"{v:.2%}")
