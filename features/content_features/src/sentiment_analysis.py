import os
import sys

from google.cloud import language_v1
from google.oauth2 import service_account

def get_cred():
	key_path = os.environ.get('SENTIMENT_ANALYSIS_API_KEY')
	credentials = service_account.Credentials.from_service_account_file(key_path)
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


#GOOGLE SAMPLE (https://cloud.google.com/natural-language/docs/samples/language-sentiment-text?hl=pt-br):
def sample_analyze_sentiment(text_content):
	"""
	Analyzing Sentiment in a String

	Args:
	  text_content The text content to analyze
	"""
	client = language_v1.LanguageServiceClient(credentials=get_cred())


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
	infos = {'sentiment_score':'',
			'sentiment_magnitude':'',
			'sentiment':''}
	infos['sentiment_score'] = score
	infos['sentiment_magnitude'] = magnitude
	infos['sentiment'] = analyze_score(score,magnitude)

	return infos
