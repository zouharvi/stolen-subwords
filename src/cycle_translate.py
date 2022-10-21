#!/usr/bin/env python3

import argparse
import random
import torch

args = argparse.ArgumentParser()
args.add_argument(
    "--model", default='transformer.wmt19.en-de',
    help="Name of the translation model to use"
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

def get_translation(model, vocab):
    sent_src = " ".join(random.choices(list(vocab), k=20))
    sent_tgt = model.translate(sent_src)
    return set(sent_tgt.split())

SENT_A = "In model functionality stealing, we aim to replicate the victim model MV functionality to which we have either completely blackbox or grey-box (logits)."
vocab_a = set(SENT_A.split())
vocab_b = set()

for i in range(10000):
    if i < 10 or i % 10 == 0:
        print(f"{i:>5}, EN: {len(vocab_a):>5}, DE: {len(vocab_b):>5}")
        print(vocab_a)

    vocab_b_ext = get_translation(model_a, vocab_a)
    vocab_b |= vocab_b_ext
    vocab_a_ext = get_translation(model_b, vocab_b)
    vocab_a |= vocab_a_ext
    if len(vocab_a_ext) == 0 and len(vocab_b_ext) == 0:
        break
