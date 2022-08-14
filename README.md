## Purpose

The purpose is to achieve a uniform process to create taxonomies from different information sources.
To that end, we define an intermediate representation which all sources need to extract their relevant (to our interests) information to,
and then we convert it to our final ready to upload taxonomy JSON.


## SNOMED CT

SNOMED CT (Systematized Nomenclature of Medicine - Clinical Terms) is a standardized, multilingual vocabulary of clinical terminology.
In SNOMED there are Concepts and Relations.

### Concepts

Each concept may have multiple names, including "fully specified names" (names that uniquely identify the concept) and "synonyms" (other names, sometimes more in use). 
We each of these groups has a single preferred name.
SNOMED treats the **preferred synonym** as the canonical name and so do we. 
The rest are used as aliases resulting in 3 groups:
- **synonyms**: the names of the "synonyms" group (except the "preferred synonym")
- **preferred fully specified name**
- **fully specified names**:  the names of the "fully specified names" group (except the "preferred synonym")

We filter out concepts that are not marked as active. 

### Relations

There are many kinds of relations between concepts, we chose to adopt the "is a" relation which SNOMED itself uses to define the taxonomy hierarchy.

In the "is a" relation hierarchy, concepts may have more than one father, so we performed the following heuristic priority to linearize the graph (force each concept to have one father at most):

```
Choose the father of a concept according to the following priority:
(1) a descendant of a disease 
(2) a descendant of clinical findings
(3) the number of his children
```

## RxNorm

RxNorm provides normalized names for clinical drugs.

We want to produce a taxonomy of clinical drugs, for this purpose we used the active ingredients (IN) found in RxNorm as canonical names (split to RxNorm-normalized and non-normalized - adding another level of hierarchy to our taxonomy).

In rxnorm, each IN is related to a precise ingredient (PIN) and a few possible brand names (BN). Each of IN/PIN/BN may have different names from different sources which rxnorm treat as synonyms,
and are represented as adjacent lines in the concepts file and by sharing the same concept-id. We use all of these as aliases, resulting in 5 groups:
- **ingredient synonyms** - we use the rest of the active-ingredient's related synonyms as aliases.
- **precise ingredient** - stems from a link that exists between the ingredient and a more specific version of the ingredient.
- **brand name** - derives from the relationship between the ingredient and the commercial brand name of the drug containing the same ingredient.
- **precise ingredient synonyms** - we use the rest of the precise-ingredient's related synonyms as aliases.
- **brand name synonyms** - we use the rest of the brand-name's related synonyms as aliases.

In addition, we chose to keep only INs that have at least one synonym whose source is DRUGBANK - which cleaned up the taxonomy from concepts that are not necessarily drugs.
