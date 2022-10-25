#!/usr/bin/env python3

import datasets
import tqdm

data = datasets.load.load_dataset("wmt14", "de-en")["train"]

def get_vocab(data, lang):
    data = [x[lang].lower().split() for x in data[:500]["translation"]]
    data = [w for s in data for w in s]
    vocab = set()
    for w in tqdm.tqdm(data):
        # sanitize words
        w = ''.join(c for c in w.lower() if c.isalnum())
        if len(w) > 30:
            continue
        vocab.add(w)
    return vocab

vocab_wmt_en = get_vocab(data, "en")
vocab_wmt_de = get_vocab(data, "de")


with open("data/vocab_en.txt", "r") as f:
    vocab_mt_en = set([w.rstrip() for w in f.readlines()])
with open("data/vocab_de.txt", "r") as f:
    vocab_mt_de = set([w.rstrip() for w in f.readlines()])

print(" MT EN len", len(vocab_mt_en))
print(" MT DE len", len(vocab_mt_de))
print("WMT EN len", len(vocab_wmt_en))
print("WMT DE len", len(vocab_wmt_de))

print("MT coverage of WMT (EN)", f"{len(vocab_mt_en & vocab_wmt_en)/len(vocab_wmt_en):.2%}")
print("MT coverage of WMT (DE)", f"{len(vocab_mt_de & vocab_wmt_de)/len(vocab_wmt_de):.2%}")
