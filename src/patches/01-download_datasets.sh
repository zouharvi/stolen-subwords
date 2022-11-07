#!/usr/bin/bash

cd data_vocab

wget https://object.pouta.csc.fi/OPUS-EuroPat/v3/moses/de-en.txt.zip
unzip de-en.txt.zip
rm EuroPat.de-en.xml README LICENSE de-en.txt.zip

wget https://object.pouta.csc.fi/OPUS-EUbookshop/v2/moses/de-en.txt.zip
unzip de-en.txt.zip
rm EUbookshop.de-en.ids README de-en.txt.zip

wget https://object.pouta.csc.fi/OPUS-CCAligned/v1/moses/de-en.txt.zip
unzip de-en.txt.zip
rm CCAligned.de-en.xml README LICENSE de-en.txt.zip

# wget https://object.pouta.csc.fi/OPUS-JRC-Acquis/v3.0/moses/de-en.txt.zip
# unzip de-en.txt.zip
# rm JRC-Acquis.de-en.xml README LICENSE de-en.txt.zip

# wget https://object.pouta.csc.fi/OPUS-Europarl/v3/moses/de-en.txt.zip
# unzip de-en.txt.zip
# rm Europarl.de-en.ids README LICENSE de-en.txt.zip

# join to EUbookshop
# cat Europarl.de-en.de >> EUbookshop.de-en.de
# cat Europarl.de-en.en >> EUbookshop.de-en.en
# rm Europarl.de-en.{de,en}

wget https://object.pouta.csc.fi/OPUS-ParaCrawl/v8/moses/de-en.txt.zip
unzip de-en.txt.zip
rm ParaCrawl.de-en.xml README LICENSE de-en.txt.zip

cd ..

# head -n 10000000 EuroPat.de-en.en > EuroPat.de-en/orig.en
# head -n 10000000 EuroPat.de-en.de > EuroPat.de-en/orig.de