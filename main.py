import json

from snomed.snomed_extract import snomed_extract
from create_our_format import create_our_format

if __name__ == '__main__':

    EXTRACT = False
    TAXONOMY_NAME = "SNOMED"

    concept_dict = {}
    is_a_dict = {}
    concept_without_father = []
    aliases_fields = []

    if TAXONOMY_NAME == "SNOMED":
        aliases_fields = ['preferred synonym', 'synonyms', 'preferred fully specified name', 'fully specified names']
        if EXTRACT:
            concept_dict, is_a_dict, concept_without_father = snomed_extract()
        else:
            with open('snomed/concepts.json') as f:
                concept_dict = json.load(f)
            with open('snomed/is_a.json') as f:
                is_a_dict = json.load(f)
            with open('snomed/concept_without_father.json') as f:
                concept_without_father = json.load(f)

    create_our_format(concept_dict, is_a_dict, concept_without_father, aliases_fields)
