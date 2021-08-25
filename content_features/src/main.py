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
from scraper.title_scraper import execute


def run_titles(args):
	with open(os.environ.get("FAKE_NEWS_URL_PROBLEM_FILE"),'r') as f:
		for line in f:
			dic = json.loads(line)
			L = [{'Titulo': ''}]
			#for url in dic['url']:
			data = {}
			data['url'] = dic['url'].strip() #url.strip()
			data['fonte'] = dic['fonte']	
			data['Titulo'] = str(execute(data['fonte'],data['url'])).strip()
			if data['Titulo'] == 'NULL' or data['Titulo'] == None or data['Titulo'] == L[-1]['Titulo']:
				with(open('../dados/titles_exeptions.txt','a')) as file:
					file.write(json.dumps(data,ensure_ascii=False)+'\n')
			else:
				L.append(data)
			with open('../dados/top10_fake_titles.txt','a') as f:
				for l in L[1:]:
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
