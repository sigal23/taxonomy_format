import json
from tqdm import tqdm
import csv

# Relevant IDs
ACTIVE = '1'
SYNONYM = '900000000000013009'
FULLY_SPECIFIED_NAME = '900000000000003001'
EN_USA = '900000000000509007'
PREFERRED = '900000000000548007'
IS_A = '116680003'
LANGUAGE_CODE = 'en'
# Relevant file names
CONCEPT = 'snomed/sct2_Concept_Snapshot_US1000124_20220301.txt'
LANGUAGE = 'snomed/der2_cRefset_LanguageSnapshot-en_US1000124_20220301.txt'
DESCRIPTION = 'snomed/sct2_Description_Snapshot-en_US1000124_20220301.txt'
RELATIONSHIP = 'snomed/sct2_Relationship_Snapshot_US1000124_20220301.txt'


# A function that extracts from the snomed files the content we need to create our taxonomy format
def snomed_extract():
    # Save all active concepts in a dictionary called 'concept_dict',
    # where the key is the ID of the concept and the value is a dictionary that contains for each concept:
    # 'name', 'preferred synonym', 'synonyms', 'preferred fully specified name' and 'fully specified names'
    with open(CONCEPT) as con:
        concept_dict = {}
        row_iter = csv.DictReader(con, delimiter='\t')
        for row in tqdm(row_iter):
            if row['active'] == ACTIVE:
                concept_dict[row['id']] = {'name': '', 'preferred synonym': [], 'synonyms': [],
                                           'preferred fully specified name': [], 'fully specified names': []}

    # Save the ID of the preferred descriptions in an array called 'prefer_terms'
    with open(LANGUAGE) as lang:
        prefer_terms = []
        row_iter = csv.DictReader(lang, delimiter='\t')
        for row in tqdm(row_iter):
            if row['active'] == ACTIVE and row['refsetId'] == EN_USA and row['acceptabilityId'] == PREFERRED:
                prefer_terms.append(row['referencedComponentId'])

    # Fill in the 'concept_dict' dictionary values with the appropriate descriptions for each concept
    with open(DESCRIPTION) as desc:
        row_iter = csv.DictReader(desc, delimiter='\t')
        for row in tqdm(row_iter):
            if row['active'] == ACTIVE and row['languageCode'] == LANGUAGE_CODE and row['conceptId'] in concept_dict:
                if row['typeId'] == SYNONYM:
                    if row['id'] in prefer_terms:
                        concept_dict[row['conceptId']]['preferred synonym'].append(row['term'])
                        # The canonical name of each concept will be the preferred synonym
                        concept_dict[row['conceptId']]['name'] = row['term']
                    else:
                        concept_dict[row['conceptId']]['synonyms'].append(row['term'])
                elif row['typeId'] == FULLY_SPECIFIED_NAME:
                    if row['id'] in prefer_terms:
                        concept_dict[row['conceptId']]['preferred fully specified name'].append(row['term'])
                    else:
                        concept_dict[row['conceptId']]['fully specified names'].append(row['term'])

    # Create a dictionary called 'is_a_dict' that contains the relationship between the concepts according to their ID
    # The key is the father and the value is an array of all his children
    with open(RELATIONSHIP) as relation:
        is_a_dict = {}
        concept_without_father = list(concept_dict.keys())
        row_iter = csv.DictReader(relation, delimiter='\t')
        for row in tqdm(row_iter):
            if row['active'] == ACTIVE and row['typeId'] == IS_A and row['sourceId'] in concept_dict and row[
                'destinationId'] in concept_dict:
                if row['destinationId'] in is_a_dict:
                    is_a_dict[row['destinationId']].append(row['sourceId'])
                else:
                    is_a_dict[row['destinationId']] = [row['sourceId']]
                # Saving the concepts that don't have a parent - will be used for building the hierarchy
                if row['sourceId'] in concept_without_father:
                    concept_without_father.remove(row['sourceId'])

    # If we have one root then get all his children instead
    if len(concept_without_father) == 1:
        concept_without_father = is_a_dict[concept_without_father[0]]

    # Turning the graph into a tree
    is_a_dict = snomed_is_a_single_father(is_a_dict)

    # Saving the relevant data we extracted to json files
    with open("snomed/concepts.json", 'w') as f:
        json.dump(concept_dict, f)

    with open("snomed/is_a.json", 'w') as f:
        json.dump(is_a_dict, f)

    with open("snomed/concept_without_father.json", 'w') as f:
        json.dump(concept_without_father, f)

    return concept_dict, is_a_dict, concept_without_father


# A function that receives a dictionary of fathers and their children
# according to their concept id, and returns a dictionary in the same structure
# but each concept can have only one father (tree)
def snomed_is_a_single_father(is_a_dict):
    # Get descendants by concept id
    def get_descendants(conc_id):
        descendants = [conc_id]
        for child in is_a_dict.get(conc_id, []):
            descendants += get_descendants(child)
        return descendants

    child_to_father = {}
    is_a_single_father = {}
    disease_descendants = set(get_descendants("404684003"))
    clinic_find_descendants = set(get_descendants("64572001"))

    # Creating an inverted dictionary - the key is the child and the value is an array of his fathers
    for f in is_a_dict.keys():
        for c in is_a_dict[f]:
            if c in child_to_father and f not in child_to_father[c]:
                child_to_father[c].append(f)
            elif c not in child_to_father:
                child_to_father[c] = [f]

    # Choose the father of a concept according to the following priority - a descendant of a disease,
    # a descendant of clinical findings, the number of his children
    # child_to_father will contain child as key and the chosen father as value
    for c in child_to_father.keys():
        father_arr = child_to_father[c]
        if len(father_arr) > 1:
            father_arr = sorted(father_arr, key=lambda x: (x not in disease_descendants, x not in clinic_find_descendants,
                                                           -len(is_a_dict[x])))
        child_to_father[c] = father_arr[0]

    # Create a dictionary of fathers and their children where each concept can have only one father
    for c, f in child_to_father.items():
        if f in is_a_single_father and c not in is_a_single_father[f]:
            is_a_single_father[f].append(c)
        elif f not in is_a_single_father:
            is_a_single_father[f] = [c]

    return is_a_single_father
