## Purpose

The purpose is to achieve uniformity to create taxonomies from different information sources 
and extract data that is relevant to our format and at the end create from them JSON in our format.

## SNOMED CT
SNOMED CT (Systematized Nomenclature of Medicine - Clinical Terms) is a standardized, multilingual vocabulary of clinical terminology.
<br> We get all active concepts from concepts and description file, the canonical name of each concept will be the preferred synonym.
<br> We extracted the hierarchy from the relationship file, the relationship we were interested in is 'is a', we noticed that a certain concept can have more than one father, 
so we performed some heuristic operations in order for each concept to have at most one father:
<br> Choose the father of a concept according to the following priority:
<br>- a descendant of a disease 
<br>- a descendant of clinical findings
<br>- the number of his children


## RxNorm
RxNorm provides normalized names for clinical drugs.
<br> We want to produce a taxonomy of clinical drugs, for this purpose we extracted from RxNorme as
concepts the active ingredients (including those that are rxnorm meaning that they have undergone
a certain normalization and those that have not) and this was chosen to be the canonical name of the concept,
<br> We divided the aliases of the active ingredient into 5 groups which We populated through the relationship between them and the active ingredient:
<br> 'ingredient synonyms' - the lines of the same concept that is an ingredient are its aliases
<br> 'precise ingredient' - stems from a link that exists between the ingredient and a more specific version of the ingredient
<br> 'brand name' - derives from the relationship between the ingredient and the commercial brand name of the drug containing the same ingredient
<br> 'precise ingredient synonyms' - the lines of the same concept that is precise ingredient are its aliases
<br> 'brand name synonyms' - the lines of the same concept that is brand name are its aliases

In addition, we chose to only take concepts that have at least one line whose source is DRUGBANK - used to clear ingredients that are not necessarily drugs.
<br> Because we received a flat hierarchy (active ingredients and their names) we chose to add a level to the hierarchy and divide the ingredients into those that are rxnorm and those that are not (other).