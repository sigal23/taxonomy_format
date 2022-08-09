# RXNORM

RxNorm provides normalized names for clinical drugs and links its names to many of the drug vocabularies commonly used in pharmacy management and drug interaction software, including those of First Databank, Micromedex, and Gold Standard Drug Database. By providing links between these vocabularies, RxNorm can mediate messages between systems not using the same software and vocabulary.

## The goal

Extract data from RXNORM that is relevant to create a drug taxonomy (and concept list). This will give us a resource with higher coverage and which is easier to update/maintain than the one we mined manually.

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

1. **Concept file** - - "RXNCONSO.RRF" is a pipe-separated file. The file contains information about the RxNorm Concepts which are represented by several lines (a.k.a atoms).
    <br> We care about the following concept types (TTY column): 
    <br>- IN: stands for active ingridient and is singular per concept does have at least one line that is RXNORM and if the concept does not have a line that is RXNORM and there is IN we will choose the first one we see.
    <br>- BN: Brand name, could be several that are related to the same IN (through the relations file).
    <br>- PIN: precise ingredient, a more specific variation of the IN. 
    <br> For a better understanding of the file format (the columns) in the following link:
    https://www.nlm.nih.gov/research/umls/rxnorm/docs/techdoc.html#rel:~:text=12.4%20Concept%20Names%20and%20Sources%20(File%20%3D%20RXNCONSO.RRF)


2. **Relationships file** - "RXNREL.RRF" the file contains connections/relations between concepts and also between atoms. 
    <br> Since we treat the relations between the different BNs/PINs to IN as synonyms we use this file to find the relations between the concepts we already filtered from the concepts-file, 
    and create the mapping from canonical name (IN) to its aliases (BNs/PINs). 
    <br> For a better understanding of the file format (the columns) in the following link:
    https://www.nlm.nih.gov/research/umls/rxnorm/docs/techdoc.html#rel:~:text=12.7%20Related%20Concepts%20(File%20%3D%20RXNREL.RRF)
