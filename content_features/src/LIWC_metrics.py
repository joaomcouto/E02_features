from pyliwc.core import LIWC


def LIWC_metrics(text):
    """
    Metrics:
        funct
        pronoun
        ppron
        i
        we
        you
        shehe
        they
        ipron
        article
        verb
        auxverb
        past
        present
        future
        adverb
        preps
        conj
        negate
        quant
        number
        swear
        social
        family
        friend
        humans
        affect
        posemo
        negemo
        anx
        anger
        sad
        cogmech
        insight
        cause
        discrep
        tentat
        certain
        inhib
        incl
        excl
        percept
        see
        hear
        feel
        bio
        body
        health
        sexual
        ingest
        relativ
        motion
        space
        time
        work
        achieve
        leisure
        home
        money
        relig
        death
        assent
        nonfl
        filler
    """
    liwc = LIWC("./../dados/Brazilian_Portuguese_LIWC2007_Dictionary.dic")
    liwc_scores = liwc.process_text(text)
    print(liwc_scores)

print(LIWC_metrics("Alemanha confirma 1º caso de coronavírus em Starnberg"))
