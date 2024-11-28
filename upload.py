# Read corpus from a file and upload it to the Elasticsearch server

import sys
import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch.helpers import streaming_bulk

load_dotenv()

ES_CLOUD_ID = os.getenv('ES_CLOUD_ID')
ES_API_KEY = os.getenv('ES_API_KEY')
es_client = Elasticsearch(
    cloud_id=ES_CLOUD_ID,
    api_key=ES_API_KEY,
    request_timeout=60,
)

BULK_SIZE = int(os.getenv('BULK_SIZE', 100))

# Read the corpus from the file
# Directory structure of the file:
# ./data/text/{corpus_name}/{id}.txt
#
# File structure:
# 1st line: URL
# 2nd line: Date in the format of ISO8601, such as 2010-05-22T14:30:00+0900
# 3rd line: Title
# After the 3rd line: Content
def read_corpus(corpus_name):
    corpus_path = f'data/text/{corpus_name}'
    corpus = []
    for filename in os.listdir(corpus_path):
        with open(f'{corpus_path}/{filename}', 'r') as file:
            url = file.readline().strip()
            date = file.readline().strip()
            title = file.readline().strip()
            content = file.read()
            corpus.append({
                'id': filename.split('.')[0],
                'url': url,
                'date': date,
                'title': title,
                'content': content
            })
    return corpus

def delete_index_if_exists(index_name):
    if es_client.indices.exists(index=index_name):
        es_client.indices.delete(index=index_name)

# Upload the corpus to the Elasticsearch server
# Index name should be livedoor_corpus_{corpus_name}
def upload_corpus(corpus_name, corpus):
    index_name = f'livedoor_corpus_{corpus_name}'
    delete_index_if_exists(index_name)
    def gendata():
        for doc in corpus:
            yield {
                '_index': index_name,
                '_id': doc['id'],
                '_source': doc
            }
    success_count = 0
    error_count = 0
    error_docs = []
    total = len(corpus)

    print(f'Uploading {total} documents to the Elasticsearch server')

    for success, info in streaming_bulk(
        es_client,
        gendata(),
        chunk_size=BULK_SIZE,
        raise_on_error=False
    ):
        if success:
            success_count += 1
            if success_count % BULK_SIZE == 0:
                print(f'{success_count} / {total} documents uploaded')
        else:
            error_count += 1
            error_docs.append(info['index']['_id'])
    print(f'{success_count} documents uploaded successfully')
    print(f'{error_count} documents failed to upload')
    print(f'Error documents: {error_docs}')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python upload.py {corpus_name}')
        sys.exit(1)
    corpus_name = sys.argv[1]
    corpus = read_corpus(corpus_name)
    upload_corpus(corpus_name, corpus)
    print(f'{len(corpus)} documents uploaded to the Elasticsearch server')