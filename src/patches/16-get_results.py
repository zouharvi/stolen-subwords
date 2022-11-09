#!/usr/bin/env python3

import argparse
import re

args = argparse.ArgumentParser()
args.add_argument("logfile")
args = args.parse_args()


logfile1 = args.logfile
if "en-de.log" in logfile1:
    logfile2 = logfile1.replace("en-de.log", "de-en.log")
elif "de-en.log" in logfile1:
    logfile2 = logfile1.replace("de-en.log", "en-de.log")
else:
    raise Exception(f"Sibling logfile not found to '{logfile1}'")

re_epoch = re.compile(r" epoch (\d+)")
re_best_bleu = re.compile(r" best_bleu (\d+\.?\d*)")
re_bleu = re.compile(r" bleu (\d+\.?\d*)")


def load_data(f):
    with open(f, "r") as f:
        data = [x.strip() for x in f.readlines()]
    data = [x for x in data if "best_bleu" in x]
    data = [
        (
            int(re_epoch.search(x).group(1)),
            float(re_best_bleu.search(x).group(1)),
            float(re_bleu.search(x).group(1)),
        )
        for x in data
    ]
    return data


data1 = load_data(logfile1)
data2 = load_data(logfile2)

max_epoch1 = max([x[0] for x in data1])
max_epoch2 = max([x[0] for x in data2])


max_epoch = min(max_epoch1, max_epoch2)
bleu1 = [x[1] for x in data1 if x[0] == max_epoch][0]
bleu2 = [x[1] for x in data2 if x[0] == max_epoch][0]
bleu_avg = (bleu1+bleu2)/2

occurence_best1 = max([x[0] for x in data1 if x[2] == bleu1])
occurence_best2 = max([x[0] for x in data2 if x[2] == bleu2])

print(f"On epoch {max_epoch} ({occurence_best1}/{max_epoch1}, {occurence_best2}/{max_epoch2}) best_bleu avg {bleu_avg:.2f}")
