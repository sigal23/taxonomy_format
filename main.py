import json
import argparse
from snomed.snomed_extract import snomed_extract
from create_our_format import create_our_format

if __name__ == '__main__':
    # Create the parser
    parser = argparse.ArgumentParser()
    # Add an arguments
    parser.add_argument('--extract', default=False, action='store_true')
    parser.add_argument('--taxonomy', type=str, required=True)
    # Parse the argument
    args = parser.parse_args()
    extract = args.extract
    taxonomy_name = args.taxonomy

    # The files required to create our taxonomy format
    concept_dict = {}
    is_a_dict = {}
    concept_without_father = []
    aliases_fields = []

    # If the taxonomy we want to produce is of 'snomed'
    if taxonomy_name in ["snomed", "Snomed", "SNOMED"]:
        aliases_fields = ['preferred synonym', 'synonyms', 'preferred fully specified name', 'fully specified names']
        if extract:
            concept_dict, is_a_dict, concept_without_father = snomed_extract()
        else:
            with open('snomed/concepts.json') as f:
                concept_dict = json.load(f)
            with open('snomed/is_a.json') as f:
                is_a_dict = json.load(f)
            with open('snomed/concept_without_father.json') as f:
                concept_without_father = json.load(f)

    # create our format from the taxonomy
    create_our_format(concept_dict, is_a_dict, concept_without_father, aliases_fields)
