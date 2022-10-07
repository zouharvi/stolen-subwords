#!/usr/bin/env python3

import argparse
import tqdm

args = argparse.ArgumentParser()
args.add_argument(
    "--model", default='transformer.wmt19.en-de',
    help="Name of the translation model to use"
)
args.add_argument(
    "-o", "--output", default="data/tmp.txt",
    help="Where to store the data"
)
args.add_argument(
    "-i", "--input", default=None,
)
args = args.parse_args()

fin = open(args.input, "r")
fout = open(args.output, "w")

def model_wrapper(model):
    import torch
    import fairseq
    if model in {'transformer.wmt19.en-de', 'transformer.wmt19.de-en'}:
        return torch.hub.load(
            'pytorch/fairseq', model,
            checkpoint_file='model1.pt',
            tokenizer='moses', bpe='fastbpe'
        )
    else:
        raise Exception(f"Model {model} not yet covered")

model = model_wrapper(args.model)
model.eval()
model.to("cuda")

for line_in in tqdm.tqdm(fin):
    line_in = line_in.rstrip("\n")
    line_out = model.translate(line_in)
    fout.write(line_out + "\n")
