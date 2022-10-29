#!/usr/bin/bash

cd data_vocab

wget https://object.pouta.csc.fi/OPUS-EuroPat/v3/moses/de-en.txt.zip
unzip de-en.txt.zip
rm EuroPat.de-en.xml README LICENSE de-en.txt.zip


wget https://object.pouta.csc.fi/OPUS-EUbookshop/v2/moses/de-en.txt.zip
unzip de-en.txt.zip
rm EUbookshop.de-en.ids README LICENSE de-en.txt.zip

wget https://object.pouta.csc.fi/OPUS-Europarl/v3/moses/de-en.txt.zip
unzip de-en.txt.zip
rm Europarl.de-en.ids README LICENSE de-en.txt.zip

# join to EUbookshop
cat Europarl.de-en.de >> EUbookshop.de-en.de
cat Europarl.de-en.en >> EUbookshop.de-en.en

wget https://object.pouta.csc.fi/OPUS-ParaCrawl/v8/moses/de-en.txt.zip
unzip de-en.txt.zip
rm ParaCrawl.de-en.xml README LICENSE de-en.txt.zip

cd ..