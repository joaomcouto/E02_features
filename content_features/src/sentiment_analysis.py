import os
import sys

from google.cloud import language_v1
from google.oauth2 import service_account

def get_cred():
	credentials = service_account.Credentials.from_service_account_file("api_auth/ic-analise-de-sentimentos-7ee361a878de.json")
	return credentials

def analyze_score(val,mag):
	if val > 0.25 and mag > 0.0:
		return 'Positive'
	elif val > -0.25 and val < 0.25:
		if(val == 0.0 and mag > 0.0):
			return 'Mixed'
		else:
			return 'Neutral'
	elif val < -0.25:
		return 'Negative'
	else:
		return 'Out of range'


#GOOGLE SAMPLE(https://cloud.google.com/natural-language/docs/samples/language-sentiment-text?hl=pt-br):
def sample_analyze_sentiment(text_content):
	"""
	Analyzing Sentiment in a String

	Args:
	  text_content The text content to analyze
	"""
	client = language_v1.LanguageServiceClient(credentials=get_cred())

	# text_content = 'I am so happy and joyful.'

	# Available types: PLAIN_TEXT, HTML
	type_ = language_v1.Document.Type.PLAIN_TEXT

	# Optional. If not specified, the language is automatically detected.
	# For list of supported languages:
	# https://cloud.google.com/natural-language/docs/languages
	language = "pt-br"
	document = {"content": text_content, "type_": type_, "language": language}

	# Available values: NONE, UTF8, UTF16, UTF32
	encoding_type = language_v1.EncodingType.UTF8

	response = client.analyze_sentiment(request = {'document': document, 'encoding_type': encoding_type})
	score = response.document_sentiment.score
	magnitude = response.document_sentiment.magnitude
	infos = {'string':'',
			'sentiment_score':'',
			'sentiment_magnitude':'',
			'sentiment':''}
	infos['string'] = text_content
	infos['sentiment_score'] = score
	infos['sentiment_magnitude'] = magnitude
	infos['sentiment'] = analyze_score(score,magnitude)
	"""

	# Get overall sentiment of the input document
	print(u"Document sentiment score: {}".format(score))
	print(u"Document sentiment magnitude: {}".format(magnitude))
	
	
	# Get sentiment for all sentences in the document
	for sentence in response.sentences:
		print(u"Sentence text: {}".format(sentence.text.content))
		print(u"Sentence sentiment score: {}".format(sentence.sentiment.score))
		print(u"Sentence sentiment magnitude: {}".format(sentence.sentiment.magnitude))

	# Get the language of the text, which will be the same as
	# the language specified in the request or, if not specified,
	# the automatically-detected language.
	print(u"Language of the text: {}".format(response.language))

	"""
	return infos

def main(argv):
	if (argv[0] == '-true'):
		r_file_path = 'true_news.txt'
		w_file_path = 'true_news_sentiment_analysis.txt'
	elif(argv[0] == '-fake'):
		r_file_path = 'fake_news.txt'
		w_file_path = 'fake_news_sentiment_analysis.txt'
	else:
		print("Argumento não definido.\n")
		return
		
	with open(r_file_path , 'r') as read_file:
		with open(w_file_path, 'a') as write_file:
			for line in read_file:
				D = sample_analyze_sentiment(line.strip())
				write_file.write(str(D) + '\n')

if __name__ == "__main__":
    main(sys.argv[1:])