#!/usr/bin/env python3

import fastBPE

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

model = model_wrapper("transformer.wmt19.en-de")
bpe = fastBPE.fastBPE("data_vocab/wmt19m.de-en.bpecodes")

def translate_boxes(text):
    print(text)
    translation = model.translate(text)
    print(translation)
    gtranslation = bpe.apply([translation])[0]
    gtranslation = gtranslation.replace("@@", "\\bpeatsymbol")
    print(gtranslation)
    print()

# translate_boxes("Stolen Subwords: Importance of Vocabularies for Machine Translation Model Stealing")
# translate_boxes("huge errors in their own understanding of reality")
# translate_boxes("Avoid misunderstanding and reduce error propabilities")
# translate_boxes("avoid errors and unpleasant misunderstandings")

translate_boxes("The washing machine is broken.")
translate_boxes("I broke the milling machine.")
