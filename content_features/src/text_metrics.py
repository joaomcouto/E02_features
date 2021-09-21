import subprocess
import json

"""
readability grades:
        Kincaid: 6,0
        ARI: 5,7
        Coleman-Liau: 9,5
        Flesch Index: 63,6/100 (plain English)
        Fog Index: 11,8
        Lix: 37,3 = school year 5
        SMOG-Grading: 9,7
sentence info:
        66 characters
        13 words, average length 5,08 characters = 1,62 syllables
        2 sentences, average length 6,5 words
        50% (1) short sentences (at most 2 words)
        0% (0) long sentences (at least 17 words)
        1 paragraphs, average length 2,0 sentences
        0% (0) questions
        0% (0) passive sentences
        longest sent 11 wds at sent 2; shortest sent 2 wds at sent 1
word usage:
        verb types:
        to be (0) auxiliary (0)
        types as % of total:
        conjunctions 0% (0) pronouns 0% (0) prepositions 15% (2)
        nominalizations 0% (0)
sentence beginnings:
        pronoun (0) interrogative pronoun (0) article (0)
        subordinating conjunction (0) conjunction (0) preposition (0)

"""

def get_int(text, idx,parentheses = False,sep = ' '):
    if parentheses:
        return int(text.split(str(sep))[idx].replace('(',"")[:-1])
    return int(text.split(str(sep))[idx])

def get_float(text,idx,sep = ' '):
    return float(text.split(str(sep))[idx].replace(',','.'))

def extract_values(out):

    if out == 'No sentences found.':
        raise NoSenteceException

    metric_list = out.split('\n')

    #Dados de Legibilidade
    readability = metric_list[1:8]
    read_dict = {}
    for value in readability:
        value = value.strip().split(':')

        if '/100' or '=' in value[1]:
            aux = value[1].split('/') if ('/100' in value[1]) else value[1].split('=')
            value[1] = aux[0]

        read_dict[value[0]] = float(value[1].replace(',','.').strip())

    #Dados da Frase:
    sent_dict = {}
    sentence = [i.strip() for i in metric_list[9:18]]
    sent_dict['n_characters'] = get_int(sentence[0],0)
    sent_dict['n_words'] = get_int(sentence[1],0)
    sent_dict['word_avg_lenght'] = get_float(sentence[1],4)
    sent_dict['n_sentences'] = get_int(sentence[2],0)
    sent_dict['sentence_avg_length'] = get_float(sentence[2],4)
    sent_dict['n_short_sentence'] = get_int(sentence[3], 1,True)
    sent_dict['n_long_sentence'] = get_int(sentence[4],1,True)
    sent_dict['n_paragraphs'] = get_int(sentence[5],0)
    sent_dict['paragraph_avg_length'] = get_float(sentence[5],4)
    sent_dict['n_questions'] = get_int(sentence[6],1,True)
    sent_dict['n_passive_sentence'] = get_int(sentence[7],1,True)
    sent_dict['longest_sentence'] = get_int(sentence[8],2)
    sent_dict['shortest_sentence'] = get_int(sentence[8],9)

    #Dados de Palavras
    word_dict = {}
    word = [i.strip() for i in metric_list[20:24]]
    word_dict['n_verbs_to_be'] = get_int(word[0],2,True)
    word_dict['n_verbs_auxiliary'] = get_int(word[0],4,True)
    word_dict['n_conjunctions'] = get_int(word[2],2,True)
    word_dict['%_conjunctions']  = float(get_int(word[2],1,True)/100)
    word_dict['n_pronouns'] = get_int(word[2],5,True)
    word_dict['%_pronouns']  = float(get_int(word[2],4,True)/100)
    word_dict['n_prepositions'] = get_int(word[2],8,True)
    word_dict['%_prepositions']  = float(get_int(word[2],7,True)/100)
    word_dict['n_nomilizations'] = get_int(word[3],2,True)
    word_dict['%_nomilizations']  = float(get_int(word[3],1,True)/100)

    return read_dict,sent_dict,word_dict


def text_metrics(text):

    text = text.strip() # Retira espaços e quebra de linha no final

    # Adicionando char de parada para executavel style
    final_chars = ['.', '!', '?', ':', ' ']
    for i in range(len(text)-1, -1, -1):
        if text[i] in [' ', '\n']:
            continue
        elif text[i] in final_chars:
            break
        else:
            text += '.'
            break
    # Torna primeira letra uppercase e não altera as restantes
    text = text[0].upper() + text[1:]
    metrics = subprocess.run(["./../executaveis/text_metrics.x", "-L", "pt"], input=text, text=True, capture_output=True).stdout
    return metrics

#file_name: indicar o nome para identificar na pasta de resultados
def metrics_from_file(file_path, file_name):
    with open(file_path, 'r') as file:
        for line in file:
            run(line, file_name)


def run(text):
    D = {} #Dicionarios com as metricas
    readability ,sentence ,word = extract_values(text_metrics(text))
    D.update(readability)
    D.update(sentence)
    D.update(word)
    return D
