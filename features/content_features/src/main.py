import env
import json
import os
import sys
import traceback

from count_exclamation import count_exclamation
from count_hashtags import count_hashtags
from count_uppercase_words import count_uppercase_words
from toxicity_threat_insult import toxicity_threat_insult
from LIWC_metrics import LIWC_metrics
import text_metrics
from sentiment_analysis import sample_analyze_sentiment as SentimentAnalyzer
from scraper.title_scraper import execute


def run_titles(args):
    arg = args[0]
    if arg == 'fake':
        with open(os.environ.get("FAKE_NEWS_URL_FILE"), 'r') as f:
            for line in f:
                dic = json.loads(line)
                L = [{'Titulo': ''}]
                for url in dic['url']:
                    data = {}
                    data['url'] = dic['url'].strip()  # url.strip()
                    data['fonte'] = dic['fonte']
                    data['Titulo'] = str(execute(data['fonte'], data['url'])).strip()
                    if data['Titulo'] == 'NULL' or data['Titulo'] == None or data['Titulo'] == L[-1]['Titulo']:
                        with(open(os.environ.get("FAKE_NEWS_EXCEPTION_FILE"),'a')) as file:
                            file.write(json.dumps(data, ensure_ascii=False)+'\n')
                    else:
                        L.append(data)
                with open('../dados/FakeNews_titles.txt', 'a') as f:
                    for l in L[1:]:
                        f.write(json.dumps(l, ensure_ascii=False)+'\n')
    elif arg == 'true':
        with open(os.environ.get("TRUE_NEWS_URL_FILE"),'r') as f:
            for url in f:
                d = {}
                d['url'] = url.strip()
                d['fonte'] = url.split('/')[2]
                d['Titulo'] = str(execute(d['fonte'],d['url'])).strip()
                print('URL = ',d['url'],'\nTITULO = ',d['Titulo'])
                if d['Titulo'] == 'NULL' or d['Titulo'] == None:
                    with(open(os.environ.get("TRUE_NEWS_EXCEPTION_FILE"),'a')) as file:
                        file.write(json.dumps(d, ensure_ascii=False)+'\n')
                else:
                    with open('../dados/TrueNews_titles.txt', 'a') as f:
                        f.write(json.dumps(d, ensure_ascii=False)+'\n')
    else:
        print("Argumento Inválido!")
        return
def run_features(title):
    aux = {}
    toxicity = toxicity_threat_insult(title)
    aux.update(toxicity)
    sentiment = SentimentAnalyzer(title)
    aux.update(sentiment)
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
    return aux


def run_fake(args):
    # Leitura dos titulos:
    dados_originais = []
    with open("./../dados/FakeNews_titles.txt", mode='r') as f:
        for line in f:
            dados_originais.append(json.loads(line.strip()))

    # Verifica se há títulos processados:
    resultados = []
    arquivo_resultado = "./../dados/resultado_fake_titles.txt"
    if os.stat(arquivo_resultado).st_size != 0:
        # Caso haja, carrega eles, para continuar de onde parou
        with open(arquivo_resultado, mode='r') as f:
            for line in f:
                resultados.append(json.loads(line.strip()))

    for i in range(len(resultados), len(dados_originais)):
        this_dados = dados_originais[i]
        try:
            features = run_features(this_dados["Titulo"])
            this_dados['features'] = features
        except Exception as e:
            # Salvando qual o erro que aconteceu
            this_dados['exception'] = traceback.format_exc()

        # Salvando dados coletados junto com dados do título (url e fonte)
        with open(arquivo_resultado, mode='a', encoding='utf-8') as f:
            f.write(json.dumps(this_dados, ensure_ascii=False) + '\n')


if __name__ == "__main__":
    args = sys.argv[1:]
    function = args[0]
    if function == 'features':
        run_features(args[1:])
    elif function == 'titles':
        run_titles(args[1:])
    elif function == 'fake_features':
        run_fake(args[1:])
    else:
        print("Por favor selecione qual metodo quer usar")
