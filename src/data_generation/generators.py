import random
from typing import Counter

from matplotlib import collections

def dataset_wrapper(lang):
    import datasets
    if lang == "en":
        return datasets.load.load_dataset("wmt14", f"cs-en")
    elif lang in {"cs", "de"}:
        return datasets.load.load_dataset("wmt14", f"{lang}-en")
    else:
        raise Exception(f"Dataset for {lang} not yet covered")


class CharZerogram():
    import string
    def __init__(self, seed, spaces_count=1):
        self.random = random.Random(seed)
        self.alphabet = self.string.ascii_letters + " " * spaces_count
        
    def __next__(self):
        while True:
            length = self.random.randint(10, 100)
            return "".join(self.random.choices(self.alphabet, k = length))

class CharUnigram():
    import collections

    def __init__(self, seed, lang):
        self.random = random.Random(seed)

        dataset = dataset_wrapper(lang)
        dataset = [x[lang] for x in dataset["train"][:1000]["translation"]]

        len_counter = self.collections.Counter([len(s) for s in dataset])
        self.lens_weights = list(len_counter.values())
        self.lens = list(len_counter.keys())

        # merge all sentences together
        dataset = [c for sent in dataset for c in sent]
        alphabet_counter = self.collections.Counter(dataset)

        self.alphabet = list(alphabet_counter.keys())
        self.alphabet_weights = list(alphabet_counter.values())
        
    def __next__(self):
        while True:
            length = self.random.choices(self.lens, k= 1, weights=self.lens_weights)[0]
            return "".join(self.random.choices(self.alphabet, k = length, weights=self.alphabet_weights))


class CharNgram():
    import collections

    def get_ngrams(self, sent):
        return list(zip(*[sent[i:] for i in range(self.n)]))

    def __init__(self, seed, lang, n):
        self.n = n
        self.random = random.Random(seed)

        dataset = dataset_wrapper(lang)
        # use | for sentence start
        dataset = ["|" * n + x[lang] for x in dataset["train"][:1000]["translation"]]

        len_counter = self.collections.Counter([len(s)-n for s in dataset])
        self.lens_weights = list(len_counter.values())
        self.lens = list(len_counter.keys())

        self.freqs = self.collections.defaultdict(self.collections.Counter)
        # merge all sentences together
        for sent in dataset:
            ngrams = self.get_ngrams(sent)
            for ngram in ngrams:
                ngram_cont = ngram[-1:][0]
                ngram_start = "".join(ngram[:-1])
                self.freqs[ngram_start][ngram_cont] += 1
                self.freqs[None][ngram_cont] += 1

        self.freqs = {k:(list(x.keys()), list(x.values())) for k,x  in self.freqs.items()}

    def __next__(self):
        while True:
            length = self.random.choices(self.lens, k= 1, weights=self.lens_weights)[0]
            sent = "|" * self.n
            for i in range(length):
                ngram_start = sent[-self.n+1:]
                if not ngram_start in self.freqs:
                    # unigram back-off distribution
                    ngram_start = None
                ngram_cont = self.random.choices(self.freqs[ngram_start][0], k=1, weights=self.freqs[ngram_start][1])[0]
                sent += ngram_cont
            
            # remove start character
            sent = sent[self.n:]
            return sent

def get_generator(name, args):
    if name.startswith("char_zerogram_"):
        spaces_count = int(name[len("char_zerogram_"):])
        return CharZerogram(args.seed, spaces_count)
    elif name.startswith("char_unigram_"):
        lang = name[len("char_unigram_"):]
        return CharUnigram(args.seed, lang)
    elif name.startswith("char_2gram_"):
        lang = name[len("char_2gram_"):]
        return CharNgram(args.seed, lang, 2)
    elif name.startswith("char_3gram_"):
        lang = name[len("char_3gram_"):]
        return CharNgram(args.seed, lang, 3)
    elif name.startswith("char_4gram_"):
        lang = name[len("char_4gram_"):]
        return CharNgram(args.seed, lang, 4)
    else:
        raise Exception(f"Unknown generator {name}")



