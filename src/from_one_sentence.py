#!/usr/bin/env python3

import argparse
import random
import sys
import torch
import fairseq
import pickle
import fastBPE
import copy

args = argparse.ArgumentParser()
args.add_argument(
    "--vocab-out", default='computed/from_single_sentence/sent_0.pkl',
)
args.add_argument(
    "--start-sent",
    default='In model functionality stealing, we aim to replicate the victim model MV functionality to which we have either completely blackbox or grey-box (logits).',
)
args = args.parse_args()
random.seed(0)

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
bpe = fastBPE.fastBPE("data_vocab/wmt19m.de-en.bpecodes")

model_a.eval()
model_a.to("cuda")
model_b.eval()
model_b.to("cuda")


def get_translation(model, vocab_freq):
    # keep how many times a word was sampled from a vocab and set selection weight to 1/k
    # sent_src = " ".join(random.choices(list(vocab), k=20))
    sent_src = []
    vocab_population = [(x_i, x[0]) for x_i, x in enumerate(vocab_freq)]
    vocab_weights = [1 / x[1] for x in vocab_freq]
    for _ in range(20):
        w_i, w = random.choices(
            vocab_population, vocab_weights, k=1
        )[0]
        # add +1 used frequency
        vocab_freq[w_i][1] += 1
        sent_src.append(w)

    sent_src = " ".join(sent_src)
    # how much are we paying for this budget-wise?
    sent_src_bpe = bpe.apply([sent_src])[0].split(" ")
    sent_tgt = model.translate(sent_src)
    sent_tgt_bpe = bpe.apply([sent_tgt])[0].split(" ")
    return sent_src_bpe, sent_tgt_bpe, sent_tgt,


output = {"a": {}, "a_bpe": {}, "b": {}, "b_bpe": {}}


def dump_vocab():
    with open(args.vocab_out, "wb") as f:
        pickle.dump(output, f)


def add_to_vocab(vocab, vocab_freq, sent):
    extended = False
    sent = set(sent.split())
    for w in sent:
        # sanitize words
        # w = ''.join(c for c in w.lower() if c.isalnum())
        if len(w) > 30:
            continue
        if w not in vocab:
            extended = True
            vocab.add(w)
            vocab_freq.append([w, 1])
    return extended


def add_to_vocab_bpe(vocab, sent_bpe):
    extended = False
    for w in sent_bpe:
        if w not in vocab:
            extended = True
            vocab.add(w)
    return extended


vocab_a = set(args.start_sent.split())
vocab_a_freq = [[w, 1] for w in vocab_a]
vocab_bpe_a = set()
vocab_b = set()
vocab_b_freq = []
vocab_bpe_b = set()

PATIENCE_MAX = 5
patience = PATIENCE_MAX

save_checkpoints = [
    1000, 5000,
    10000, 50000,
    100000,
] + [
    x * 10**6
    for x in [0.5, 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]
]
budget = 0
i = 0

while True:
    i += 1
    if i < 10 or i % 10 == 0:
        print(f"{i:>5}, budget: {budget:>9}, EN-full: {len(vocab_a):>6}, DE-full: {len(vocab_b):>6}, EN-bpe: {len(vocab_bpe_a):>6}, DE-bpe: {len(vocab_bpe_b):>6}")
        if i % 100 == 0:
            sys.stdout.flush()
        if budget >= save_checkpoints[0]:
            save_checkpoints.pop(0)
            output["a"][budget] = copy.deepcopy(vocab_a)
            output["b"][budget] = copy.deepcopy(vocab_b)
            output["a_bpe"][budget] = copy.deepcopy(vocab_bpe_a)
            output["b_bpe"][budget] = copy.deepcopy(vocab_bpe_b)
            dump_vocab()

    # extend B
    sent_bpe_a, sent_bpe_b, sent_b = get_translation(model_a, vocab_a_freq)
    extended_b = add_to_vocab(vocab_b, vocab_b_freq, sent_b)
    extended_b_bpe = add_to_vocab_bpe(vocab_bpe_b, sent_bpe_b)
    budget += len(sent_bpe_a)

    # extend A
    sent_bpe_b, sent_bpe_a, sent_a = get_translation(model_b, vocab_b_freq)
    extended_a = add_to_vocab(vocab_a, vocab_a_freq, sent_a)
    extended_a_bpe = add_to_vocab_bpe(vocab_bpe_a, sent_bpe_a)
    budget += len(sent_bpe_b)

    if (not extended_a) and (not extended_b) and (not extended_a_bpe) and (not extended_b_bpe):
        patience -= 1
        print("Decreasing patience to", patience)
    else:
        patience = PATIENCE_MAX

    if patience == 0 or len(save_checkpoints) == 0:
        break

# TODO: not present in the live version
output["a"][budget] = copy.deepcopy(vocab_a)
output["b"][budget] = copy.deepcopy(vocab_b)
output["a_bpe"][budget] = copy.deepcopy(vocab_bpe_a)
output["b_bpe"][budget] = copy.deepcopy(vocab_bpe_b)
dump_vocab()