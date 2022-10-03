import json
from tqdm import tqdm
import csv
from typing import List, Dict, Tuple, Set
from common import AliasObject, ConceptDict, IsADict, ConceptWithoutFather

# Relevant file names
CONCEPT = 'rxnorm/RXNCONSO.RRF'
RELATIONSHIP = 'rxnorm/RXNREL.RRF'


# A function that extracts from the rxnorm files the content we need to create our taxonomy format
def rxnorm_extract() -> Tuple[ConceptDict, IsADict, ConceptWithoutFather]:
    with open(CONCEPT) as con:
        row_iter = csv.DictReader(con, delimiter='|', fieldnames=["RXCUI", "LAT", "TS", "LUI", "STT", "SUI", "ISPREF",
                                                                  "RXAUI", "SAUI", "SCUI", "SDUI", "SAB", "TTY", "CODE",
                                                                  "STR", "SRL", "SUPPRESS", "CVF"])
        con_row = [dict(x) for x in list(row_iter)]

    # Initialize the parameters for the first concept
    concept_dict: ConceptDict = {}
    concept_dict_pin: Dict[str, List[AliasObject]] = {}
    concept_dict_bn: Dict[str, List[AliasObject]] = {}
    last_cid: str = 'initialize'
    bn_in_pin: str = ''
    had_rxnorm: bool = False
    had_drugbank: bool = False
    concept_syn: Set[str] = set()
    name: str = ''
    concept_id_dict_key_rxn: Set[str] = set()
    con_no_rxnorm: Set[str] = get_con_no_rxnorm()
    concept_id_dict_key_no_rxn: Set[str] = set()

    # move over concepts rows
    for row in tqdm(con_row):
        # current concept id
        current_cid: str = row['RXCUI']

        # initialize for the first run
        if last_cid == 'initialize':
            last_cid = row['RXCUI']

        # If we have finished running through all the lines of a certain concept
        if current_cid != last_cid:
            # If the concept had a row that is RXNORM or is a concept that we defined from those that
            # are not RXNORM and put it in the appropriate data structure
            if had_rxnorm or last_cid in con_no_rxnorm:
                if bn_in_pin == 'IN' and had_drugbank:
                    concept_dict[last_cid] = {'name': name, 'ingredient synonyms': concept_syn, 'precise ingredient': [],
                                              'brand name': [], 'precise ingredient synonyms': set(), 'brand name synonyms': set()}
                    # Saving the dictionary keys (concept id) according to division hierarchy into rxnorm and those that are not
                    if had_rxnorm:
                        concept_id_dict_key_rxn.add(last_cid)
                    else:
                        concept_id_dict_key_no_rxn.add(last_cid)
                elif bn_in_pin == 'PIN':
                    concept_dict_pin[last_cid] = [name, concept_syn]

                elif bn_in_pin == 'BN':
                    concept_dict_bn[last_cid] = [name, concept_syn]

            # Initialize the parameters from the following concept
            bn_in_pin = ''
            had_rxnorm = False
            had_drugbank = False
            name = ''
            last_cid = current_cid
            concept_syn = set()
        # Saving all the names of the rows (atoms) of the same concept that are its synonyms
        concept_syn.add(row['STR'])
        # If the concept has a line that is RXNORM with a desired TTY (IN\BN\PIN) we will place the parameters according to this line
        if row['SAB'] == 'RXNORM' and row['TTY'] in ('BN', 'IN', 'PIN'):
            bn_in_pin = row['TTY']
            had_rxnorm = True
            name = row['STR']
        # If the concept does not have a line that is RXNORM with a desired TTY (IN\BN\PIN) we will place the parameters according to the
        # following priority: if there is IN we will choose the first one we see, if there is no IN we will choose BN
        # and if there is no IN\BN we will choose PIN
        elif current_cid in con_no_rxnorm:
            if row['TTY'] == 'IN' and bn_in_pin != 'IN':
                bn_in_pin = row['TTY']
                name = row['STR']
            elif row['TTY'] == 'BN' and bn_in_pin != 'IN':
                bn_in_pin = row['TTY']
                name = row['STR']
            elif row['TTY'] == 'PIN' and bn_in_pin not in ('IN', 'BN'):
                bn_in_pin = row['TTY']
                name = row['STR']

        # If there is one row that is with SAB=DRUGBANK we would like this concept (used to clear INs that are not necessarily drugs)
        if row['SAB'] == 'DRUGBANK':
            had_drugbank = True

    with open(RELATIONSHIP) as rel:
        row_iter = csv.DictReader(rel, delimiter='|', fieldnames=["RXCUI1", "RXAUI1", "STYPE1", "REL", "RXCUI2", "RXAUI2", "STYPE2",
                                                                  "RELA", "RUI", "SRUI", "SAB", "SL", "RG", "DIR",
                                                                  "SUPPRESS", "CVF"])
        # move over relationship rows
        for row in tqdm(row_iter):
            # Linking the synonyms to the INs we saved which are RXNORM\NO RXNORM and adding them to the appropriate alias group
            if row['STYPE1'] == 'CUI' and row['STYPE2'] == 'CUI' and ((row['RXCUI2'] in concept_id_dict_key_rxn and row['SAB'] == 'RXNORM') or (row['RXCUI2'] in concept_id_dict_key_no_rxn)):
                if row['RELA'] == 'has_form' and row['RXCUI1'] in concept_dict_pin:
                    concept_dict[row['RXCUI2']]['precise ingredient'].append(concept_dict_pin[row['RXCUI1']][0])
                    concept_dict[row['RXCUI2']]['precise ingredient synonyms'].update(concept_dict_pin[row['RXCUI1']][1])
                elif row['RELA'] == 'has_tradename' and row['RXCUI1'] in concept_dict_bn:
                    concept_dict[row['RXCUI2']]['brand name'].append(concept_dict_bn[row['RXCUI1']][0])
                    concept_dict[row['RXCUI2']]['brand name synonyms'].update(concept_dict_bn[row['RXCUI1']][1])

    # Convert the set to a list so we can write the concepts to a file
    for k in tqdm(concept_dict.keys()):
        concept_dict[k]['ingredient synonyms'] = list(concept_dict[k]['ingredient synonyms'])
        concept_dict[k]['precise ingredient synonyms'] = list(concept_dict[k]['precise ingredient synonyms'])
        concept_dict[k]['brand name synonyms'] = list(concept_dict[k]['brand name synonyms'])

    # Deletion of duplicate synonyms between concept alias lists
    concept_dict = del_dup_syn(concept_dict)

    # Creating two levels of nesting - one for concepts that are RXNORM and one for the others
    concept_dict['rxnorm'] = {'name': 'RxNorm', 'ingredient synonyms': [], 'precise ingredient': [],
                              'brand name': [], 'precise ingredient synonyms': [], 'brand name synonyms': []}
    concept_dict['others'] = {'name': 'Others', 'ingredient synonyms': [], 'precise ingredient': [],
                              'brand name': [], 'precise ingredient synonyms': [], 'brand name synonyms': []}
    concept_without_father: ConceptWithoutFather = ['rxnorm', 'others']
    is_a_dict: IsADict = {'rxnorm': list(concept_id_dict_key_rxn), 'others': list(concept_id_dict_key_no_rxn)}

    # Saving the relevant data we extracted to json files
    with open("rxnorm/concepts.json", 'w') as f:
        json.dump(concept_dict, f)

    with open("rxnorm/is_a.json", 'w') as f:
        json.dump(is_a_dict, f)

    with open("rxnorm/concept_without_father.json", 'w') as f:
        json.dump(concept_without_father, f)

    return concept_dict, is_a_dict, concept_without_father


# A function that removes duplicate synonyms between concept alias lists and returns concept dict in the same format it received
def del_dup_syn(concept_dict: ConceptDict) -> ConceptDict:
    fix_concept_dict = {}
    prior_list = ['precise ingredient synonyms', 'brand name synonyms', 'ingredient synonyms', 'precise ingredient',
                  'brand name', 'name']
    # For each concept we create a dictionary of priorities and then rebuild the concept using the dictionary
    # without duplication between aliases groups
    for cid, v in concept_dict.items():
        # Creating a dictionary where the key is concept name and the value is the alias group the name belongs to
        prior_dict = {}
        for al in prior_list:
            if al == 'name':
                prior_dict[v[al]] = al
            else:
                for n in v[al]:
                    prior_dict[n] = al
        # Turning the dictionary we created into a concept without duplication
        fix_concept = {'name': '', 'ingredient synonyms': [], 'precise ingredient': [],
                       'brand name': [], 'precise ingredient synonyms': [], 'brand name synonyms': []}
        for n, al in prior_dict.items():
            if al == 'name':
                fix_concept[al] = n
            else:
                fix_concept[al].append(n)
        fix_concept_dict[cid] = fix_concept
    return fix_concept_dict


# A function that returns a set of the concepts id that don't have a line containing RXNORM and also have lines whose TTY is IN\BN\PIN
def get_con_no_rxnorm() -> Set[str]:
    with open(CONCEPT) as con:
        row_iter = csv.DictReader(con, delimiter='|', fieldnames=["RXCUI", "LAT", "TS", "LUI", "STT", "SUI", "ISPREF",
                                                                  "RXAUI", "SAUI", "SCUI", "SDUI", "SAB", "TTY", "CODE",
                                                                  "STR", "SRL", "SUPPRESS", "CVF"])

        con_row = [dict(x) for x in list(row_iter)]

    rxnorm_con: Set[str] = set()
    con_id_bn_in_pin: Set[str] = set()

    for row in con_row:
        if row['TTY'] in ('BN', 'IN', 'PIN') and row['SAB'] == 'RXNORM':
            rxnorm_con.add(row['RXCUI'])

    for row in con_row:
        if row['TTY'] in ('BN', 'IN', 'PIN') and row['RXCUI'] not in rxnorm_con:
            con_id_bn_in_pin.add(row['RXCUI'])

    return con_id_bn_in_pin
