#!/usr/bin/env python3

import matplotlib.pyplot as plt
import fig_utils
import argparse
import json

# scp euler:/cluster/work/sachan/vilem/vocab-stealing/computed/overlap/*all*.jsonl computed/overlap/

args = argparse.ArgumentParser()
args.add_argument(
    "--logs", default="computed/from_single_sentence/precomputed.jsonl"
)
args = args.parse_args()

PRETTY_NAME = {
    "self_overlap_bpe": "Self BPE overlap",
    "self_overlap_word": "Self word overlap",
    "victim_overlap_bpe": "Victim BPE overlap",
    "bpe_count": "BPE count",
    "word_count": "Word count",
}

with open(args.logs, "r") as f:
    data = json.loads(f.read())


# plot
plt.figure(figsize=(4.8, 3.5))
xticks_main = []
ax1 = plt.gca()
ax2 = plt.twinx()

for k_i, k in enumerate(["self_overlap_bpe", "self_overlap_word", "victim_overlap_bpe"]):
    v = data[k + "_avg"]
    xticks_main = [int(x) for x in v.keys()]

    xticks = range(len(v.keys()))
    ax1.plot(
        range(len(v.keys())),
        list(v.values()),
        marker=".",
        markersize=12,
        alpha=1,
        color=fig_utils.COLORS[k_i],
        label=PRETTY_NAME[k],
    )

    ax1.errorbar(
        xticks,
        y=list(v.values()),
        yerr=(
            [100 for m, a in zip(data[k + "_max"].values(), v.values())],
            [m - a for m, a in zip(data[k + "_max"].values(), v.values())],
        ),
        color=fig_utils.COLORS[k_i],
        elinewidth=0,
        linewidth=0,
        capsize=3,
        capthick=1.5,
        barsabove=True,
    )
    ax1.errorbar(
        xticks,
        y=list(v.values()),
        yerr=(
            [0 for m, a in zip(data[k + "_max"].values(), v.values())],
            [m - a for m, a in zip(data[k + "_max"].values(), v.values())],
        ),
        color=fig_utils.COLORS[k_i],
        elinewidth=1,
        linewidth=0,
        barsabove=True,
    )

for k_i, k in enumerate(["word_count"]):
    v = data[k + "_avg"]
    ax2.plot(
        range(len(v.keys())),
        list(v.values()),
        marker=".",
        markersize=12,
        alpha=1,
        color=fig_utils.COLORS[k_i+3],
        label=PRETTY_NAME[k],
    )

ax1.set_xticks(
    [i for i in range(len(xticks_main)) if (i + 1) % 2],
    [
        f"{x/1000000:}M".replace(".0M", "M")
        for i, x in enumerate(xticks_main) if (i + 1) % 2
    ],
)

yticks1 = [0, 0.2, 0.4, 0.6, 0.8]
ax1.set_yticks(
    yticks1,
    [f"{x:.0%}" for x in yticks1],
)
yticks2 = [0, 100, 200, 300, 400, 500, 600, 700]
ax2.set_yticks(
    [x*1000 for x in yticks2],
    [f"{x}k" for x in yticks2],
)

# plt.xlim(-2)
ax1.set_ylim(-0.05, 0.9)
ax1.set_ylabel("Vocabulary overlap")
ax2.set_ylabel("Vocabulary count")
plt.xlabel("Subword translation budget (millions, logscaled).")

h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
# lns = lns1+lns2+lns3
# labs = [l.get_label() for l in lns]
# ax.legend(lns, labs, loc=0)

plt.legend(
    h1+h2,
    l1+l2,
    ncol=2,
    bbox_to_anchor=(-0.13, 1, 1.13, 0), loc="lower left", mode="expand"
)
plt.tight_layout(pad=0.1)
plt.savefig("computed/figures/cycle_budget.pdf")
plt.show()
