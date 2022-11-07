#!/usr/bin/env python3

import argparse
import tqdm

args = argparse.ArgumentParser()
args.add_argument("-i", "--input", default="data_vocab/wmt19m.de-en.bpecodes")
args.add_argument("-o", "--output", default=None)
args.add_argument("--no-debpe", action="store_true")
args = args.parse_args()

is_bpe = args.input.endswith("bpecodes")


def load_bpe(f):
    with open(f, "r") as f:
        data_raw = list(f.readlines())
        assert all([len(l.split(" ")) == 3 for l in data_raw])
        data = [l.split(" ")[:2] for l in data_raw]
    # this is incorrect and gives overconfident results
    vocab = set([l[0] + l[1] for l in data])
    return vocab

def process_line(l):
    if l.endswith("\n"):
        l = l[:-1]
    if args.no_debpe:
        return set(l.split(" "))
    else:
        out = set()
        for w in l.split(" "):
            if w.endswith("@@"):
                out.add(w[:-2])
            else:
                out.add(w + "</w>")
        return out

def load_simple(f):
    import multiprocess
    pool = multiprocess.Pool()
    BATCH_SIZE=1_000_000
    print("Counting number of lines")
    num_lines = sum(1 for _ in open(f, "r"))
    print("Loading")
    out = set()
    with open(f, "r") as f:
        batch = []
        for _ in tqdm.tqdm(list(range(num_lines//BATCH_SIZE))):
            for _ in range(1_000_000):
                batch.append(f.readline())
            vocab_local = list(pool.map(process_line, batch))
            vocab_local = {w for vocab in vocab_local for w in vocab}
            out |= vocab_local
            print("Current vocab:", len(out))
            batch = []
    return out

if is_bpe:
    data = load_bpe(args.input)
else:
    data = load_simple(args.input)

print("Saved", len(data), "items")

if args.output is None:
    args.output = args.input.replace(".bpecodes", ".vocab").replace(".all", ".vocab")

with open(args.output, "w") as f:
    for v in data:
        f.write(v + "\n")

