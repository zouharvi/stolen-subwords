#!/usr/bin/env python3

import argparse
import random
import torch

args = argparse.ArgumentParser()
args.add_argument(
    "--model", default='transformer.wmt19.en-de',
    help="Name of the translation model to use"
)
args.add_argument(
    "--vocab-a", default='data/vocab_en.txt',
)
args.add_argument(
    "--vocab-b", default='data/vocab_de.txt',
)
args = args.parse_args()


model_a = torch.hub.load(
    'pytorch/fairseq', 'transformer.wmt19.en-de',
    checkpoint_file='model1.pt',
    tokenizer='moses', bpe='fastbpe'
)
model_b = torch.hub.load(
    'pytorch/fairseq', 'transformer.wmt19.de-en',
    checkpoint_file='model1.pt',
    tokenizer='moses', bpe='fastbpe'
)

model_a.eval()
model_a.to("cuda")
model_b.eval()
model_b.to("cuda")

def get_translation(model, vocab_freq):
    # keep how many times a word was sampled from a vocab and set selection weight to 1/k
    # sent_src = " ".join(random.choices(list(vocab), k=20))
    sent_src = []
    vocab_population = [(x_i, x[0]) for x_i, x in enumerate(vocab_freq)]
    vocab_weights = [1/x[1] for x in vocab_freq]
    for _ in range(20):
        w_i, w = random.choices(
            vocab_population, vocab_weights, k =1
        )[0]
        vocab_freq[w_i][1] += 1
        sent_src.append(w)
    sent_src = " ".join(sent_src)
    sent_tgt = model.translate(sent_src)
    return sent_tgt

def dump_vocab(path, vocab):
    with open(path, "w") as f:
        f.write("\n".join(vocab))

def add_to_vocab(vocab, vocab_freq, sent):
    extended = False
    sent = set(sent.split())
    for w in sent:
        # sanitize words
        w = ''.join(c for c in w.lower() if c.isalnum())
        if len(w) > 30:
            continue
        if w not in vocab:
            extended = True
            vocab.add(w)
            vocab_freq.append([w, 1])
    return extended


SENT_A = "In model functionality stealing, we aim to replicate the victim model MV functionality to which we have either completely blackbox or grey-box (logits)."
vocab_a = set(SENT_A.split())
vocab_a_freq = [[w, 1] for w in vocab_a]
vocab_b = set()
vocab_b_freq = []

PATIENCE_MAX = 3
patience = PATIENCE_MAX
for i in range(10000):
    if i < 10 or i % 10 == 0:
        print(f"{i:>5}, EN: {len(vocab_a):>5}, DE: {len(vocab_b):>5}")
        dump_vocab(args.vocab_a, vocab_a)
        dump_vocab(args.vocab_b, vocab_b)

    # extend B
    sent_b = get_translation(model_a, vocab_a_freq)
    extended_b = add_to_vocab(vocab_b, vocab_b_freq, sent_b)

    # extend A
    sent_a = get_translation(model_b, vocab_b_freq)
    extended_a = add_to_vocab(vocab_a, vocab_a_freq, sent_a)

    if (not extended_a) and (not extended_b):
        patience -= 1
        print("DECREASING PATIENCE TO", patience)
    else:
        patience = PATIENCE_MAX

    if patience == 0:
        break