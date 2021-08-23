import env
import json
import os
import sys

from count_exclamation import count_exclamation
from count_hashtags import count_hashtags
from count_uppercase_words import count_uppercase_words
from toxicity_threat_insult import toxicity_threat_insult
from LIWC_metrics import LIWC_metrics
import text_metrics
from sentiment_analysis import sample_analyze_sentiment as SentimentAnalyzer
from scraper.title_scraper import get_title


def run_titles(args):
    with open(os.environ.get("FAKE_NEWS_URL_FILE"),'r') as f:
        for line in f:
            dic = json.loads(line)
            print(dic['fonte'].upper())
            L = []
            for url in dic['urls']:
                data = {}
                data['url'] = url
                data['fonte'] = dic['fonte']
                try:
                    data['Titulo'] = get_title(url)
                    print(url+'\n',data['Titulo'])
                except Exception as E:
                    data['Problema'] = E
                    print("!!@ ",data, "@!!")
                L.append(data)
                

            with open('../dados/titles_file.txt','a') as f:
                for l in L:
                    f.write(json.dumps(l,ensure_ascii=False)+'\n')

                    


def run_features(args):
    # Inicializando estruturas de dados
    metrics = {'fake': {}, 'true': {}}
    titles = {}

    # Lendo os arquivos com os títulos
    with open(os.environ.get("FAKE_NEWS_FILE")) as f:
        titles['fake'] = f.readlines()
    with open(os.environ.get("TRUE_NEWS_FILE")) as f:
        titles['true'] = f.readlines()

    # Gerando as features para cadaa título
    for news_type in ['fake', 'true']:
        for title in titles[news_type]:
            aux = {}
            toxicity = toxicity_threat_insult(title)
            aux.update(toxicity)
            sentiment = SentimentAnalyzer(title)
            exclamation = count_exclamation(title)
            aux.update(exclamation)
            uppercase = count_uppercase_words(title)
            aux.update(uppercase)
            hashtags = count_hashtags(title)
            aux.update(hashtags)
            text = text_metrics.run(title)
            aux.update(text)
            LIWC = LIWC_metrics(title)
            aux.update(LIWC)
            metrics[news_type][title.strip()] = aux

    # Salvando dados gerados
    with open(os.environ.get('METRICS'), 'w') as f:
        json_string = json.dumps(
            metrics,
            sort_keys=False,
            indent=4,
            ensure_ascii=False)
        f.write(json_string)


if __name__ == "__main__":
    args = sys.argv[1:]
    function = args[0]
    if function == 'features':
        run_features(args[1:])
    elif function == 'titles':
        run_titles(args[1:])
    else:
        print("Por favor selecione qual metodo quer usar")
