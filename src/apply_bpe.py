#!/usr/bin/env python3

import argparse
import tqdm
import sentencepiece as spm

args = argparse.ArgumentParser()
args.add_argument(
    "-t", "--train", action="store_true",
)
args.add_argument(
    "-i", "--input", nargs="+",
    default=[
        "data/proof_of_concept/word_3gram.de",
        "data/proof_of_concept/word_3gram.en",
        "data/proof_of_concept/wmt21.de",
        "data/proof_of_concept/wmt21.en",
    ],
)
args.add_argument(
    "-o", "--output", nargs="+",
    default=[
        "data/proof_of_concept/word_3gram_bpe.de",
        "data/proof_of_concept/word_3gram_bpe.en",
        "data/proof_of_concept/wmt21_bpe.de",
        "data/proof_of_concept/wmt21_bpe.en",
    ],
)
args = args.parse_args()

if args.train:
    model_train = spm.SentencePieceTrainer.train(
        input=args.input,
        model_prefix='data/proof_of_concept/spm',
        vocab_size=15000,
        shuffle_input_sentence=True,
    )
# , user_defined_symbols=['foo', 'bar']


model = spm.SentencePieceProcessor(
    model_file='data/proof_of_concept/spm.model'
)

for fname_in, fname_out in zip(args.input, args.output):
    fout = open(fname_out, "w")
    with open(fname_in, "r") as fin:
        for sent in tqdm.tqdm(fin.readlines()):
            sent_out = model.encode(sent.strip(), out_type="str")
            sent_out = " ".join(sent_out)
            fout.write(sent_out + "\n")

