from googleapiclient import discovery
import json
import env
import os
import time


def toxicity_threat_insult(text):
    """
    Limit: 60 calls for minute.

    All attirbutes below are Production attributes have been tested across
    multiple domains and trained on significant amounts of human-annotated
    comments.
    All of them support pt language.

    Receives a text and returns:

    Metrics:
        - THREAT: Describes an intention to inflict pain,
        injury, or violence against an individual or group.

        - INSULT:  Insulting, inflammatory, or negative
        comment towards a person or a group of people.

        - TOXICITY: A rude, disrespectful, or unreasonable
        comment that is likely to make people leave a discussion.

        - IDENTITY_ATTACK: Negative or hateful comments
        targeting someone because of their identity. (NOT IN USE)

        - PROFANITY: Swear words, curse words, or other
        obscene or profane language. (NOT IN USE)
    """
    API_KEY = os.environ.get('PERSPECTIVE_API_KEY')

    client = discovery.build(
      "commentanalyzer",
      "v1alpha1",
      developerKey=API_KEY,
      discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
      static_discovery=False,
    )

    analyze_request = {
      'comment': {'text': text},
      'requestedAttributes': {'TOXICITY': {}, 'INSULT': {}, 'THREAT': {}},
      'languages': ['pt'],
      'doNotStore': False
    }

    time.sleep(1.1)
    response = client.comments().analyze(body=analyze_request).execute()
    results = {'Toxicity': '', 'Threat': '', 'Insult': ''}
    results['Toxicity'] = response['attributeScores']['TOXICITY']['summaryScore']['value']
    results['Threat'] = response['attributeScores']['THREAT']['summaryScore']['value']
    results['Insult'] = response['attributeScores']['INSULT']['summaryScore']['value']

    return results


print(toxicity_threat_insult("Alemanha confirma 1º caso de coronavírus em Starnberg"))
