import random
import json

from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import \
    Features, ConceptsOptions, EntitiesOptions, KeywordsOptions, CategoriesOptions, \
    EmotionOptions, MetadataOptions, SemanticRolesOptions, RelationsOptions, \
    SentimentOptions

nlu = NaturalLanguageUnderstandingV1(version="2018-03-16", url="https://gateway.watsonplatform.net/natural-language-understanding/api",
                                     username="41797b9f-ea86-4d19-aa5c-e4eafe40f27b", password="5TlLVSbt8U0e")

text = "They were idiots. The car had problems and they were unable to fix them or provide a replacement without a lot of hassle."

features = Features(categories=CategoriesOptions(), entities=EntitiesOptions(
    emotion=True, sentiment=True), keywords=KeywordsOptions(emotion=True, sentiment=True))

response = nlu.analyze(text=text, features=features)

print(response)
print(type(response))

neg_count = 0
pos_count = 0
neut_count = 0

for kw in response['keywords']:
    if kw['sentiment']['label'] == 'positive':
        pos_count += 1
    elif kw['sentiment']['label'] == 'negative':
        neg_count += 1
    else:
        neut_count += 1

def get_sentiment():
    if pos_count > neg_count and pos_count > neut_count:
        return ['positive']
    elif neg_count > pos_count and neg_count > neut_count:
        return ['negative']
    elif neut_count > pos_count and neut_count > neg_count:
        return ['neutral']
    elif neut_count == pos_count and neut_count > neg_count:
        return ['neutral']
    elif neg_count == pos_count and neg_count > neut_count:
        return ['neutral']
    elif neut_count == neg_count and neut_count > pos_count:
        return ['neutral']
    elif neut_count == pos_count and neut_count == neg_count:
        return ['neutral']


print(get_sentiment())
