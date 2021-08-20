from pyliwc.core import LIWC


def LIWC_metrics(text):
    """
    Uses a portuguese LIWC version
    to calculate the text scores
    """
    liwc_scores = {
        'funct' : 0,
        'pronoun' : 0,
        'ppron' : 0,
        'i' : 0,
        'we' : 0,
        'you' : 0,
        'shehe' : 0,
        'they' : 0,
        'ipron' : 0,
        'article' : 0,
        'verb' : 0,
        'auxverb' : 0,
        'past' : 0,
        'present' : 0,
        'future' : 0,
        'adverb' : 0,
        'preps' : 0,
        'conj' : 0,
        'negate' : 0,
        'quant' : 0,
        'number' : 0,
        'swear' : 0,
        'social' : 0,
        'family' : 0,
        'friend' : 0,
        'humans' : 0,
        'affect' : 0,
        'posemo' : 0,
        'negemo' : 0,
        'anx' : 0,
        'anger' : 0,
        'sad' : 0,
        'cogmech' : 0,
        'insight' : 0,
        'cause' : 0,
        'discrep' : 0,
        'tentat' : 0,
        'certain' : 0,
        'inhib' : 0,
        'incl' : 0,
        'excl' : 0,
        'percept' : 0,
        'see' : 0,
        'hear' : 0,
        'feel' : 0,
        'bio' : 0,
        'body' : 0,
        'health' : 0,
        'sexual' : 0,
        'ingest' : 0,
        'relativ' : 0,
        'motion' : 0,
        'space' : 0,
        'time' : 0,
        'work' : 0,
        'achieve' : 0,
        'leisure' : 0,
        'home' : 0,
        'money' : 0,
        'relig' : 0,
        'death' : 0,
        'assent' : 0,
        'nonfl' : 0,
        'filler' : 0
    }
    liwc = LIWC("./../dados/Brazilian_Portuguese_LIWC2007_Dictionary.dic")
    liwc_calculated = liwc.process_text(text)
    for key, value in liwc_calculated.items():
        liwc_scores[key] = value
    return liwc_scores

#print(LIWC_metrics("Alemanha confirma 1º caso de coronavírus em Starnberg"))
