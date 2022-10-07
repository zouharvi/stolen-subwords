import random


def dataset_wrapper(lang):
    import datasets
    if lang == "en":
        return datasets.load.load_dataset("wmt14", f"cs-en")
    elif lang in {"cs", "de"}:
        return datasets.load.load_dataset("wmt14", f"{lang}-en")
    else:
        raise Exception(f"Dataset for {lang} not yet covered")

# we still have to load the whole model even if we just want to use the tokenizer
# we can speed it up by not loading the whole ensemble


def bpe_model_wrapper(model):
    import torch
    if model in {'transformer.wmt19.en-de', 'transformer.wmt19.de-en'}:
        return torch.hub.load(
            'pytorch/fairseq', model,
            checkpoint_file='model1.pt',
            tokenizer='moses', bpe='fastbpe'
        )
    else:
        raise Exception(f"Model {model} not yet covered")


class NGramModel():
    import collections

    def get_ngrams(self, sent):
        return list(zip(*[sent[i:] for i in range(self.n)]))

    def __init__(self, seed, n, sequences, post_treatment=None):
        self.n = n
        self.random = random.Random(seed)
        self.post_treatment = post_treatment

        if type(sequences[0][0]) is str and len(sequences[0][0]) == 1:
            self.start_token = "|"
        else:
            self.start_token = "| "

        len_counter = self.collections.Counter([len(s) - n for s in sequences])
        self.lens_weights = list(len_counter.values())
        self.lens = list(len_counter.keys())

        self.freqs = self.collections.defaultdict(self.collections.Counter)
        for sequence in sequences:
            ngrams = self.get_ngrams(sequence)
            for ngram in ngrams:
                ngram_cont = ngram[-1:][0]
                ngram_start = "".join(ngram[:-1])
                self.freqs[ngram_start][ngram_cont] += 1
                # unigram back-off distribution
                self.freqs[None][ngram_cont] += 1

        self.freqs = {
            k: (list(x.keys()), list(x.values()))
            for k, x in self.freqs.items()
        }

    def __next__(self):
        while True:
            length = self.random.choices(
                self.lens, k=1, weights=self.lens_weights
            )[0]
            sent = self.start_token * self.n
            for i in range(length):
                ngram_start = sent[-self.n + 1:]
                if not ngram_start in self.freqs:
                    # unigram back-off distribution
                    ngram_start = None
                ngram_cont = self.random.choices(
                    self.freqs[ngram_start][0], k=1, weights=self.freqs[ngram_start][1]
                )[0]
                sent += ngram_cont

            # remove start character
            sent = "".join(sent.split(self.start_token))
            if self.post_treatment is not None:
                sent = self.post_treatment(sent)
            return sent


class CharZerogram():
    import string

    def __init__(self, seed, spaces_count=1):
        self.random = random.Random(seed)
        self.alphabet = self.string.ascii_letters + " " * spaces_count

    def __next__(self):
        while True:
            length = self.random.randint(10, 100)
            return "".join(self.random.choices(self.alphabet, k=length))


class CharNgram(NGramModel):
    def __init__(self, seed, lang, n):
        self.random = random.Random(seed)

        dataset = dataset_wrapper(lang)
        # use | for sentence start
        dataset = [
            "|" * n + x[lang]
            for x in dataset["train"][:1000]["translation"]
        ]

        super().__init__(seed, n, dataset)


class WordNgram(NGramModel):
    import nltk.tokenize

    def __init__(self, seed, lang, n):
        self.random = random.Random(seed)

        dataset = dataset_wrapper(lang)
        # use | for sentence start
        dataset = [
            "| " * n + x[lang]
            for x in dataset["train"][:10000]["translation"]
        ]
        dataset = [
            [w + " " for w in self.nltk.tokenize.word_tokenize(sent)]
            for sent in dataset
        ]

        super().__init__(seed, n, dataset)


class SubwordNgram(NGramModel):
    def __init__(self, seed, lang, n, bpe_model):
        self.random = random.Random(seed)

        dataset = dataset_wrapper(lang)
        model = bpe_model_wrapper(bpe_model)
        # use | for sentence start
        dataset = [
            "| " * n + x[lang]
            for x in dataset["train"][:10000]["translation"]
        ]

        # remove @@ control characters
        dataset = [
            [
                w + " "
                for w in model.bpe.encode(sent).split()
            ]
            for sent in dataset
        ]

        def post_treatment(sent):
            return model.bpe.decode(sent)

        super().__init__(seed, n, dataset, post_treatment=post_treatment)


def get_generator(name, args):
    if name.startswith("char_zerogram_"):
        spaces_count = int(name[len("char_zerogram_"):])
        return CharZerogram(args.seed, spaces_count)
    elif name.startswith("char_ngram_"):
        lang = name[len("char_ngram_"):]
        return CharNgram(args.seed, lang, args.ngram)
    elif name.startswith("word_ngram_"):
        lang = name[len("word_ngram_"):]
        return WordNgram(args.seed, lang, args.ngram)
    elif name.startswith("subword_ngram_"):
        lang = name[len("subword_ngram_"):]
        return SubwordNgram(args.seed, lang, args.ngram, args.bpe_model)
    else:
        raise Exception(f"Unknown generator {name}")
