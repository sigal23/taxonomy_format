# RXNORM

RxNorm provides normalized names for clinical drugs and links its names to many of the drug vocabularies commonly used in pharmacy management and drug interaction software, including those of First Databank, Micromedex, and Gold Standard Drug Database. By providing links between these vocabularies, RxNorm can mediate messages between systems not using the same software and vocabulary.

## The goal

Extract data from RXNORM that is relevant to our format.

## Download relevant files

We chose to use RxNorm full edition which should be most updated and full.
Navigate to https://www.nlm.nih.gov/research/umls/rxnorm/docs/rxnormfiles.html. 

Under the title "RxNorm Full Monthly Release" download the file by clicking on "RxNorm_full_08012022.zip" (The number here may not be the same as what you see, and that's okay).

**Please note** - in order to be able to download the file you need a "UMLS Metathesaurus License", if you don't have a license, you must register (it's free - follow the instructions on the website).

After the download is complete, extract the following relevant files:

1.  The file: **"RXNCONSO.RRF"** from RxNorm_full_07052022/rff
2.  The file: **"RXNREL.RRF"** from RxNorm_full_07052022/rff

The files should be placed in a folder called "rxnorm".

## Explanation of the files

1. **Concept file** - "RXNCONSO.RRF" the file contains several lines for each concept, each concept has a unique identifier and also each line (atoms), you can see a full explanation of the fields in the following link:
    https://www.nlm.nih.gov/research/umls/rxnorm/docs/techdoc.html#rel:~:text=12.4%20Concept%20Names%20and%20Sources%20(File%20%3D%20RXNCONSO.RRF)


2. **Relationships file** - "RXNREL.RRF" the file contains connections between concepts and also between atoms, we are only interested in connections between 'ingredient' (IN), 'precise ingredient' (PIN), 'brand name' (BN). In our case the relations represent synonyms of a certain ingredient and not a hierarchy, you can see a full explanation of the fields in the following link:
   https://www.nlm.nih.gov/research/umls/rxnorm/docs/techdoc.html#rel:~:text=12.7%20Related%20Concepts%20(File%20%3D%20RXNREL.RRF)
