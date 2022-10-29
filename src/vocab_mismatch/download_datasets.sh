#!/usr/bin/bash

cd vocab_mismatch

wget https://object.pouta.csc.fi/OPUS-EuroPat/v3/moses/de-en.txt.zip
unzip de-en.txt.zip

wget https://object.pouta.csc.fi/OPUS-EUbookshop/v2/moses/de-en.txt.zip
unzip de-en.txt.zip

rm EuroPat.de-en.xml README LICENSE

cd ..