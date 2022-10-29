#!/usr/bin/bash

cd data_vocab

wget https://object.pouta.csc.fi/OPUS-EuroPat/v3/moses/de-en.txt.zip
unzip de-en.txt.zip

rm EuroPat.de-en.xml README LICENSE de-en.txt.zip

wget https://object.pouta.csc.fi/OPUS-EUbookshop/v2/moses/de-en.txt.zip
unzip de-en.txt.zip
rm EUbookshop.de-en.ids README LICENSE de-en.txt.zip

wget https://object.pouta.csc.fi/OPUS-ParaCrawl/v8/moses/de-en.txt.zip
unzip de-en.txt.zip
rm ParaCrawl.de-en.xml README LICENSE de-en.txt.zip

cd ..