# Machine Translation Vocabulary Stealing

Code accompanying the report [Stolen Subwords: Importance of Vocabularies for Machine Translation Model Stealing](https://vilda.net/papers/stolen_subwords.pdf).

Abstract:

> In learning-based functionality stealing, the attacker is trying to build a local model based on the victim's outputs.
> The attacker has to make choices regarding the local model's architecture, optimization method and, specifically for NLP models, subword vocabulary, such as BPE.
> On the machine translation task, we explore (1) whether the choice of the vocabulary plays a role in model stealing scenarios and (2) if it is possible to extract the victim's vocabulary.
> We find that the vocabulary itself does not have a large effect on the local model's performance.
> Given gray-box model access, it is possible to collect the victim's vocabulary by collecting the outputs (detokenized subwords on the output).
> The results of the minimum effect of vocabulary choice are important more broadly for black-box knowledge distillation.

<img width="500em" src="https://github.com/zouharvi/stolen-subwords/assets/7661193/ae84d0a5-8a1b-442d-9b3e-688fd8b61c54">
