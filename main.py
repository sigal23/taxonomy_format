import json
import argparse
from snomed.snomed_extract import snomed_extract
from create_our_format import create_our_format
from rxnorm.rxnorm_extract import rxnorm_extract
from common import ConceptDict, IsADict, ConceptWithoutFather
from typing import List

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
    concept_dict: ConceptDict = {}
    is_a_dict: IsADict = {}
    concept_without_father: ConceptWithoutFather = []
    aliases_fields: List[str] = []
    folder_name: str = ''

    # If the taxonomy we want to produce is of 'snomed'
    if taxonomy_name.lower() == "snomed":
        folder_name = "snomed"
        aliases_fields = ['synonyms', 'preferred fully specified name', 'fully specified names']
        if extract:
            concept_dict, is_a_dict, concept_without_father = snomed_extract()
        else:
            with open('snomed/concepts.json') as f:
                concept_dict = json.load(f)
            with open('snomed/is_a.json') as f:
                is_a_dict = json.load(f)
            with open('snomed/concept_without_father.json') as f:
                concept_without_father = json.load(f)

    # If the taxonomy we want to produce is of 'rxnorm'
    if taxonomy_name.lower() == "rxnorm":
        folder_name = "rxnorm"
        aliases_fields = ['ingredient synonyms', 'precise ingredient', 'brand name', 'precise ingredient synonyms', 'brand name synonyms']
        if extract:
            concept_dict, is_a_dict, concept_without_father = rxnorm_extract()
        else:
            with open('rxnorm/concepts.json') as f:
                concept_dict = json.load(f)
            with open('rxnorm/is_a.json') as f:
                is_a_dict = json.load(f)
            with open('rxnorm/concept_without_father.json') as f:
                concept_without_father = json.load(f)

    # create our format from the taxonomy
    create_our_format(concept_dict, is_a_dict, concept_without_father, aliases_fields, folder_name)
