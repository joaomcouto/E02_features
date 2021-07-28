import subprocess

def text_metrics(text):

    text = text.strip() # Retira espaços e quebra de linha no final

    # Adicionando char de parada para exeutavel style
    final_chars = ['.', '!', '?', ':', ' ']
    for i in range(len(text)-1, -1, -1):
        if text[i] in [' ', '\n']:
            continue
        elif text[i] in final_chars:
            break
        else:
            text += '.'
            break


    metrics = subprocess.run(["./executaveis/text_metrics.x", "-L", "pt"], input=text, text=True).stdout

    if metrics == "No sentences found.\n":
        pass
        # TRATAR

"""
readability grades:
        Kincaid: -1,8
        ARI: 3,7
        Coleman-Liau: 6,5
        Flesch Index: 117,2/100
        Fog Index: 2,0
        Lix: 5,0 = below school year 5
        SMOG-Grading: 3,0
sentence info:
        24 characters
        5 words, average length 4,80 characters = 1,00 syllables
        1 sentences, average length 5,0 words
        0% (0) short sentences (at most 1 words)
        0% (0) long sentences (at least 15 words)
        1 paragraphs, average length 1,0 sentences
        0% (0) questions
        0% (0) passive sentences
        longest sent 5 wds at sent 1; shortest sent 5 wds at sent 1
word usage:
        verb types:
        to be (0) auxiliary (0)
        types as % of total:
        conjunctions 0% (0) pronouns 0% (0) prepositions 0% (0)
        nominalizations 0% (0)
sentence beginnings:
        pronoun (0) interrogative pronoun (0) article (0)
        subordinating conjunction (0) conjunction (0) preposition (0)
"""
    print(metrics)

text_metrics("ÚLTIMO MINUTO: Washington Post confirma a origem do paciente zero do coronavírus \n   ")
