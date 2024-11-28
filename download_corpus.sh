#!/bin/bash

# Download the corpus from Rondhuit
# https://www.rondhuit.com/download/ldcc-20140209.tar.gz

export CORPUS_URL="https://www.rondhuit.com/download/ldcc-20140209.tar.gz"

# create data directory if not exists
mkdir -p data

# download the corpus into data directory
curl -L $CORPUS_URL -o data/ldcc-20140209.tar.gz

# extract the corpus
tar -zxvf data/ldcc-20140209.tar.gz -C data