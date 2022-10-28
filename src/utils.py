
def get_dataset(dataset):
    import datasets
    if dataset == "wmt19":
        data = datasets.load.load_dataset("wmt19", "de-en")
        data = data["train"][:1000000]["translation"]
        return ([x["en"] for x in data],[x["de"] for x in data])
    elif dataset == "para_crawl":
        data = datasets.load.load_dataset("para_crawl", "ende")
        data = data["train"][:1000000]["translation"]
        return ([x["en"] for x in data],[x["de"] for x in data])
    elif dataset == "europarl":
        data = datasets.load.load_dataset("europarl_bilingual", lang1="de", lang2="en")
        data = data["train"][:1000000]["translation"]
        return ([x["en"] for x in data],[x["de"] for x in data])
    else:
        raise Exception("Unknown dataset " + dataset)