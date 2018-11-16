# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import codecs
import os

def main(inputText):
    if inputText == "":
        return []
    dirpath = os.path.dirname(os.path.realpath(__file__))
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=dirpath + "/credentials.json"
    # Instantiates a client
    client = language.LanguageServiceClient()

    # Instantiates a plain text document.
    document = types.Document(
        content=inputText,
        type=enums.Document.Type.PLAIN_TEXT)

    # Detects entities in the document. You can also analyze HTML with:
    #   document.type == enums.Document.Type.HTML

    entities = client.analyze_entities(document).entities

    # entity types from enums.Entity.Type
    entity_type = ('UNKNOWN', 'PERSON', 'LOCATION', 'ORGANIZATION',
                   'EVENT', 'WORK_OF_ART', 'CONSUMER_GOOD', 'OTHER')
    result = []
    maxItems = 10
    for i in range(min(maxItems,len(entities))):
        entity = entities[i]
        result.append({'name': entity.name, 'type': entity_type[entity.type], 'salience': entity.salience})
    return result
    # for entity in entities:
    #     print('=' * 20)
    #     print(u'{:<16}: {}'.format('name', entity.name))
    #     print(u'{:<16}: {}'.format('type', entity_type[entity.type]))
    #     print(u'{:<16}: {}'.format('metadata', entity.metadata))
    #     print(u'{:<16}: {}'.format('salience', entity.salience))
    #     print(u'{:<16}: {}'.format('wikipedia_url',
    #           entity.metadata.get('wikipedia_url', '-')))
