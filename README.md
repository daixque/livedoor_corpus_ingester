# Livedoor corpus upload tool for Elasticsearch

A Utility tool to ingest the corpus data of Livedoor news articles which is published by Rondhuit. Refer to the URL below to know the details of the data:

https://www.rondhuit.com/download.html

For the search application development, it's important to have enough amount of corpus to verify the serach relevance. The Livedoor new corpus provides it in Japanese language. This tool enable you to download and ingest it to your Elasticsearch so that you can test your search application right away.

# Usage

## Download and extract the data

To download the data and extract it, execute `download_corpus.sh`.

```
$ ./download_corpus.sh
```

It will create a `data` directory and put the `ldc-20140209.tar.gz` file and extract it in the directory.

## Ingest the data into Elasticsearch

### API Key

Create an API key in your Elasticsearch. You can create it by API:

```
POST /_security/api_key
{
  "name": "livedoor-data-ingester"
}
```

Note down the newly created encoded API key.

### Set up Python

If you preferred, set up venv to keep your evnironment clean.

```
$ python -m venv .venv
$ . ./.venv/bin/activate
```

Then install dependant libraries:

```
$ pip install -r requirements.txt
```

### Set Elasticsearch connection information

Copy `env.sample` file to `.env` and set the `ES_CLOUD_ID` and `ES_API_KEY`.

### Upload the copurs

Run the `upload.py` with corpus name:

```
$ python upload.py {corpus_name}
```

Available corpus names are:

- dokujo-tsushin
- it-life-hack
- kaden-channel
- livedoor-homme
- movie-enter
- peachy
- smax
- sports-watch
- topic-news

# Data structure

The data is ingested into the index name as:

```
livedoor_corpus_{corpus_name}
```

Each document has following fields:

  - id: Document ID
  - url: URL of the article
  - date: Published date
  - title: Title of the article
  - content: Content of the article

You can find sample index template definition in the `index` directory of this repository.
