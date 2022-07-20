# SNOMED CT

SNOMED CT (Systematized Nomenclature of Medicine - Clinical Terms) is a standardized, multilingual vocabulary of clinical terminology that is used by physicians and other health care providers for the electronic exchange of clinical health information.

## The goal

Extract data from SNOMED that is relevant to our format.

## Download relevant files

We chose to use US edition as it extends over the official international edition and should be most updated and full.
Navigate to https://www.nlm.nih.gov/healthit/snomedct/us_edition.html. 

Under the title "Current US Edition Release" download the file by clicking the button "Download Now!".

**Please note** - in order to be able to download the file you need a "UMLS Metathesaurus License", if you don't have a license, you must register (it's free - follow the instructions on the website).

After the download is complete, extract the following relevant files:

1.  The file: **"sct2_Concept_Snapshot_US1000124_20220301.txt"** from SnomedCT_USEditionRF2_PRODUCTION_20220301T120000Z/Snapshot/Terminology/
2.  The file: **"sct2_Description_Snapshot-en_US1000124_20220301.txt"** from SnomedCT_USEditionRF2_PRODUCTION_20220301T120000Z/Snapshot/Terminology/
3.  The file: **"sct2_Relationship_Snapshot_US1000124_20220301.txt"** from SnomedCT_USEditionRF2_PRODUCTION_20220301T120000Z/Snapshot/Terminology/
4.  The file: **"der2_cRefset_LanguageSnapshot-en_US1000124_20220301.txt"** from SnomedCT_USEditionRF2_PRODUCTION_20220301T120000Z/Snapshot/Refset/Language/

The files should be placed in a folder called "snomed".

## Explanation of the files

1. **Concept file** - contains the clinical concepts found in SNOMED CT.
    <u><br> The fields that are relevant to us from the file: <br> </u>
    - Id - unique ID of the concept.
    - Active - indicates whether the concept is active or inactive.


2. **Description file** - contains descriptions for SNOMED CT concepts. <br> a description is used to give meaning to a 
   concept and to provide structured and standard ways of relating to a concept. each concept can have more than one description.
   <br><u> The fields that are relevant to us from the file: <br> </u>
    - Id - unique ID of the description.
    - Active - indicates whether the description is active or inactive.
    - ConceptId - identifies the concept to which this description refers.
    - LanguageCode - Specifies the language of the description text.
    - typeId - Description of the type of description: definition (900000000000550004), synonym (900000000000013009), fully specified name (900000000000003001).
    - Term - the text of the description.


3. **Relationship file** - Contains one connection between concepts in each line. each relationship is of a certain type, for the purpose of the hierarchy we are interested in a relationship of the type "is_a" only.
   <u><br> The fields that are relevant to us from the file: <br> </u>
    - Id - unique ID of the relationship
    - Active - indicates whether the relationship is active or inactive
    - sorceId - ID of the source concept
    - destinationId - ID of the destination concept
    - typeId - the type of relationship between the concepts (we will refer to the "is a" relationship identified by 116680003)


4. **Language file** - A reference set used to specify the descriptions that are preferred or acceptable for use in a particular language context. 
using this table we find the preferred concept in the English language to display among all aliases of concept.
    <u><br> The fields that are relevant to us from the file: <br> </u>
    - referencedComponentId - refers to the identifier of a description.
    - acceptabilityId - with the code 900000000000548007 representing "Preferred".
    - refsetId - with code 9000000000000509007 representing "us_en".

