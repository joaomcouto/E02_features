import env
import json
import os
import sys

from count_exclamation import count_exclamation
from count_hashtags import count_hashtags
from count_uppercase_words import count_uppercase_words
# from toxicity_threat_insult import toxicity_threat_insult
import text_metrics
from sentiment_analysis.py import sample_analyze_sentiment as SentimentAnalyzer


def main(args):
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
            # toxicity = toxicity_threat_insult(title)
            # aux.update(toxicity)
            sentiment = SentimentAnalyzer(title)
            exclamation = count_exclamation(title)
            aux.update(exclamation)
            uppercase = count_uppercase_words(title)
            aux.update(uppercase)
            hashtags = count_hashtags(title)
            aux.update(hashtags)
            text = text_metrics.run(title)
            aux.update(text)
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
    main(sys.argv[1:])
