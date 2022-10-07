#!/usr/bin/env python3

import argparse
from generators import get_generator
import tqdm

args = argparse.ArgumentParser()
args.add_argument(
    "-n", default=10, type=int,
    help="How many source sentences to generate (in thousands)"
)
args.add_argument(
    "-s", "--seed", default=0, type=int,
)
args.add_argument(
    "--ngram", default=None, type=int,
    help="For ngram language models, which n to use"
)
args.add_argument(
    "--bpe-model", default=None,
    help="For subword ngram language models, name of the translation model from which to copy the vocab"
)
args.add_argument(
    "-g", "--generator", default="char_zerogram_10",
    help="Which generator to use"
)
args.add_argument(
    "-o", "--output", default="data/tmp.txt",
    help="Where to store the data"
)
args = args.parse_args()


model = get_generator(args.generator, args)

fout = open(args.output, "w")

# make sure that the system can batch the calls so that at no point is the whole dataset in memory
for i in tqdm.tqdm(range(args.n * 1000), total=args.n * 1000):
    sent = next(model)
    fout.write(sent + "\n")
