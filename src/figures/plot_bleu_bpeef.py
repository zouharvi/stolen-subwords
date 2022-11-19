#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import fig_utils
from scipy.stats import spearmanr, pearsonr

# strict order: Victim, All, PCrawl, CCrawl, EuroPat

data_bpeef = {
    "PCrawl": [1.08, 1.04, 1.00, 1.04, 1.29],
    "CCrawl": [1.10, 1.04, 1.03, 1.00, 1.31],
    "EuroPat": [1.30, 1.05, 1.26, 1.28, 1.00],
}

data_bleu = {
    "PCrawl": [34.73, 34.91, 34.95, 34.86, 34.54],
    "CCrawl": [36.38, 36.05, 35.74, 36.25, 35.82],
    "EuroPat": [34.16, 34.36, 34.23, 34.19, 34.41],
}

domains = list(data_bpeef.keys())

data_corr_x = []
data_corr_y = []

for domain in domains:
    data_local = list(zip(data_bpeef[domain], data_bleu[domain]))
    data_local.sort(key=lambda x: x[0])
    plt.plot(
        [x[0] for x in data_local],
        [x[1] for x in data_local],
        label=domain,
        marker=".",
    )

    data_corr_x += data_bpeef[domain]
    bleu_avg = np.average(data_bleu[domain])
    data_corr_y += [x - bleu_avg for x in data_bleu[domain]]


print(f"BPE-ef - BLEU corr (Spearman): {spearmanr(data_corr_x, data_corr_y)[0]:.2%} {spearmanr(data_corr_x, data_corr_y)[1]:.3f}")
print(f"BPE-ef - BLEU corr (Pearson): {pearsonr(data_corr_x, data_corr_y)[0]:.2%} {pearsonr(data_corr_x, data_corr_y)[1]:.3f}")

plt.legend()
plt.tight_layout()
plt.show()
