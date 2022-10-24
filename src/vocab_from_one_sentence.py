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


# def cycle_translate(sentA):
#     print()
#     for i in range(1, 10):
#         print(f"{i}a ###", sentA)
#         sentB = model_a.translate(sentA)
#         print(f"{i}b ###", sentB)
#         sentA = model_b.translate(sentB)

# # char zerogram 8
# cycle_translate("TzpEyVsCJ EqTLp  W sR PCgAK  CZpWGaRxXOaD ot lIo WAetE gHQG")
# # char unigram en
# cycle_translate(
#     "P eniirmatugh)whe snd)we.eamIhvtrar)ostov dtiscehesArre  Sc5itodp tnol iect0o s1himEtm) or ia een 1oeu cno. n .rrs")
# # word unigram en
# cycle_translate("alof will achefficient At failure massive as . such to issufootfutviolence satorganisations within important inappropriate ails lyof first meare across eit the ) them")
# # word bigram en
# cycle_translate(
#     "in as in following dossier violent annum the . When impact are can gender ( of application for Action encouraging report the")

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
    return set(sent_tgt.split())

def dump_vocab(path, vocab):
    with open(path, "w") as f:
        f.write("\n".join(vocab))

SENT_A = "In model functionality stealing, we aim to replicate the victim model MV functionality to which we have either completely blackbox or grey-box (logits)."
vocab_a = set(SENT_A.split())
vocab_a_freq = [[w, 1] for w in vocab_a]
vocab_b = set()
vocab_b_freq = []

for i in range(10000):
    if i < 10 or i % 10 == 0:
        print(f"{i:>5}, EN: {len(vocab_a):>5}, DE: {len(vocab_b):>5}")
        dump_vocab(args.vocab_a, vocab_a)
        dump_vocab(args.vocab_b, vocab_b)

    # extend B
    vocab_b_ext = get_translation(model_a, vocab_a_freq)
    extended_b = False
    for w in vocab_b_ext:
        if w not in vocab_b:
            extended_b = True
            vocab_b.add(w)
            vocab_b_freq.append([w, 1])

    # extend A
    vocab_a_ext = get_translation(model_b, vocab_b_freq)
    extended_a = False
    for w in vocab_a_ext:
        if w not in vocab_a:
            extended_a = True
            vocab_a.add(w)
            vocab_a_freq.append([w, 1])

    if (not extended_a) and (not extended_b):
        break
