#!/usr/bin/env python3

import json
import collections

with open("data_vocab/compute_bpe_all.out", "r") as f:
    data = [json.loads(x) for x in f.readlines()]


out = r"""
\begin{tabular}{lccc}
\toprule
& \multicolumn{3}{c}{\textbf{Target dataset}} \\
"""
out += r"$\downarrow$ \textbf{BPE trained on}"

data_new = collections.defaultdict(dict)

for line in data:
    data_new[
        line["bpe_dataset"].lstrip("data_vocab/").rstrip(".txt")
    ][
        line["target_dataset"].lstrip("data_vocab/").rstrip(".txt")
    ] = line["subword_count"]

datasets = list(data_new["wmt19"].keys())

PRETTY_NAME = {
    "wmt19m": "Victim",
    "wmt19": "WMT19",
    "para_crawl": "Paracrawl",
    "europarl": "Europarl",
}

for target_dataset in datasets:
    out += f" & {PRETTY_NAME[target_dataset]}"

out += "\\\\ \n"
out += r"\midrule"
out += "\n"

print(data_new)

for bpe_dataset, data_new_local in data_new.items():
    out += f"{PRETTY_NAME[bpe_dataset]}"
    for target_dataset in datasets:
        star = r"$\star$" if bpe_dataset == target_dataset else r"\hspace{1.8mm}"
        self_perf = data_new[target_dataset][target_dataset]
        out += f" & {data_new_local[target_dataset]/self_perf:.2f} {star}"
    out += " \\\\ \n"

out = out.rstrip()
out += r"""
\bottomrule
\end{tabular}
"""

print(out)
