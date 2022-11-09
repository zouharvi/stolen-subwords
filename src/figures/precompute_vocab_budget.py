#!/usr/bin/env python3

import argparse
import numpy as np
import tqdm
import json

args = argparse.ArgumentParser()
args.add_argument(
    "--orig", default="data_vocab/All.de-en/orig.tok.en.uniq_small_lower.bpe")
args.add_argument(
    "--teacher", default="data_vocab/All.de-en/orig.tok.en.uniq_small_lower.teacher.bpe")
args.add_argument("-v", "--vocab", default="data_vocab/wmt19m.de-en.vocab")
args.add_argument(
    "-o", "--output",
    default="computed/overlap/wmt19m.teacher-teacher.de-en.uniq_small_lower.jsonl"
)
args = args.parse_args()

f_o1 = args.orig
f_t1 = args.teacher

def load_vocab(f):
    with open(f, "r") as f:
        data = [x.rstrip("\n") for x in f.readlines()]
    return set(data)

def invert_direction(f1):
    if ".en." in f1 + ".":
        f2 = (f1 + ".").replace(".en.", ".de.").rstrip(".")
    elif ".de." in f1 + ".":
        f2 = (f1 + ".").replace(".de.", ".en.").rstrip(".")
    else:
        raise Exception(f"Unknown sibling to '{f1}'")
    return f2

def load_bpe_data(f):
    print("Loading", f)
    out = []
    with open(f, "r") as f:
        for i, l in tqdm.tqdm(enumerate(f)):
            # if i >= 500:
            #     break
            if l.endswith("\n"):
                l = l[:-1]
            out_local = []
            for w in l.split(" "):
                if w.endswith("@@"):
                    out_local.append(w[:-2])
                else:
                    out_local.append(w + "</w>")
            out.append(out_local)
    return out


def precompute_cost(d_o):
    cost = []
    sum = 0
    for l in d_o:
        sum += len(l)
        cost.append(sum)
    return cost


def find_max_index_within_budget(cost_o, budget):
    last_ok = 0
    last_sum = 0
    for i, sum in enumerate(cost_o):
        if sum < budget:
            last_ok = i
            last_sum = sum
        else:
            break
    return last_ok, last_sum


def get_vocab_from_index(index, d_t):
    d_t = d_t[:index]
    return {x for l in d_t for x in l}


def compute_overlap(a, b):
    return 2 * len(a & b) / (len(a) + len(b))


f_o2 = invert_direction(f_o1)
f_t2 = invert_direction(f_t1)

d_o1 = load_bpe_data(f_o1)
d_o2 = load_bpe_data(f_o2)
cost_o1 = precompute_cost(d_o1)
cost_o2 = precompute_cost(d_o2)
del d_o1, d_o2
final_cost = min(cost_o1[-1], cost_o2[-1])

d_t2 = load_bpe_data(f_t2)
d_t1 = load_bpe_data(f_t1)

vocab = load_vocab(args.vocab)

weight1 = cost_o1[-1]/cost_o2[-1]
weight2 = cost_o2[-1]/cost_o1[-1]

outfile = open(args.output, "w")

MILLION = 10**6
for budget in [x * MILLION for x in [0.5, 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]]:
    # give each direction proportional budget
    ok_index_1, budget_real_1 = find_max_index_within_budget(cost_o1, weight1/(weight1+weight2)*budget)
    ok_index_2, budget_real_2 = find_max_index_within_budget(cost_o2, weight2/(weight1+weight2)*budget)

    vocab_1 = get_vocab_from_index(ok_index_1, d_t2)
    vocab_2 = get_vocab_from_index(ok_index_2, d_t1)
    vocab_hyp = vocab_1 | vocab_2

    overlap = compute_overlap(vocab, vocab_hyp)
    print(f"{(budget)//MILLION}M: {overlap:.1%}")

    outfile.write(
        json.dumps({
            "budget": budget, "overlap": overlap,
            "v1_len": len(vocab_1), "v2_len": len(vocab_2),
            "vhyp_len": len(vocab_hyp), "vwmt_len": len(vocab),
            "budget_real": budget_real_1+budget_real_2
        }) + "\n"
    )
