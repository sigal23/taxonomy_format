import json
from tqdm import tqdm
import csv

# Relevant file names
CONCEPT = 'rxnorm/RXNCONSO.RRF'
RELATIONSHIP = 'rxnorm/RXNREL.RRF'


def rxnorm_extract():
    with open(CONCEPT) as con:
        row_iter = csv.DictReader(con, delimiter='|', fieldnames=["RXCUI", "LAT", "TS", "LUI", "STT", "SUI", "ISPREF",
                                                                  "RXAUI", "SAUI", "SCUI", "SDUI", "SAB", "TTY", "CODE",
                                                                  "STR", "SRL", "SUPPRESS", "CVF"])
        concept_dict = {}
        concept_dict_pin = {}
        concept_dict_bn = {}
        last_cid = 'initialize'
        bn_in_pin = ''
        had_rxnorm = False
        concept_syn = set()
        name = ''

        for row in tqdm(row_iter):
            current_cid = row['RXCUI']

            if last_cid == 'initialize':
                last_cid = row['RXCUI']

            if current_cid != last_cid:
                if had_rxnorm:
                    if bn_in_pin == 'IN':
                        concept_dict[last_cid] = {'name': name, 'ingredient': [name],
                                                    'precise ingredient': [], 'brand name': [], 'synonyms': concept_syn}
                    elif bn_in_pin == 'PIN':
                        concept_dict_pin[last_cid] = [name, concept_syn]

                    elif bn_in_pin == 'BN':
                        concept_dict_bn[last_cid] = [name, concept_syn]
                bn_in_pin = ''
                had_rxnorm = False
                name = ''
                last_cid = current_cid
                concept_syn = set()

            concept_syn.add(row['STR'])
            if row['SAB'] == 'RXNORM' and row['TTY'] in ('BN', 'IN', 'PIN'):
                bn_in_pin = row['TTY']
                had_rxnorm = True
                name = row['STR']

    with open(RELATIONSHIP) as rel:
        row_iter = csv.DictReader(rel, delimiter='|', fieldnames=["RXCUI1", "RXAUI1", "STYPE1", "REL", "RXCUI2", "RXAUI2", "STYPE2",
                                                                  "RELA", "RUI", "SRUI", "SAB", "SL", "RG", "DIR",
                                                                  "SUPPRESS", "CVF"])
        for row in tqdm(row_iter):
            if row['SAB'] == 'RXNORM' and row['STYPE1'] == 'CUI' and row['STYPE2'] == 'CUI' and row['RXCUI2'] in concept_dict:
                if row['RELA'] == 'has_form' and row['RXCUI1'] in concept_dict_pin:
                    concept_dict[row['RXCUI2']]['precise ingredient'].append(concept_dict_pin[row['RXCUI1']][0])
                    concept_dict[row['RXCUI2']]['synonyms'].update(concept_dict_pin[row['RXCUI1']][1])
                elif row['RELA'] == 'has_tradename' and row['RXCUI1'] in concept_dict_bn:
                    concept_dict[row['RXCUI2']]['brand name'].append(concept_dict_bn[row['RXCUI1']][0])
                    concept_dict[row['RXCUI2']]['synonyms'].update(concept_dict_bn[row['RXCUI1']][1])

    #print(concept_dict['296'])

    for k in tqdm(concept_dict.keys()):
        concept_dict[k]['synonyms'] = list(concept_dict[k]['synonyms'])

    # flat hierarchy
    concept_without_father = list(concept_dict.keys())
    is_a_dict = {}

    # Saving the relevant data we extracted to json files
    with open("rxnorm/concepts.json", 'w') as f:
        json.dump(concept_dict, f)

    with open("rxnorm/is_a.json", 'w') as f:
        json.dump(is_a_dict, f)

    with open("rxnorm/concept_without_father.json", 'w') as f:
        json.dump(concept_without_father, f)

    return concept_dict, is_a_dict, concept_without_father




    # -----------------------------------------------------------------------------------------------
    # rxnorm_bn_in_pin = set()
    # bn_in_pin = set()
    # not_bn_in_pin = set()
    # drugs = set()
    #
    # count_rxnorm_bn_in_pin = 0
    # count_bn_in_pin = 0
    # count_not_bn_in_pin = 0
    #
    # with open("rxnorm/FDA_DRUGS_YS1.txt") as drugs:
    #     drugs = set(line.strip().lower() for line in drugs)
    #
    # with open("rxnorm/RXNCONSO.RRF") as con:
    #     row_iter = csv.reader(con, delimiter='|')
    #     last_cid = 'initialize'
    #     had_bn_in_pin = False
    #     had_rxnorm_bn_in_pin = False
    #     concepts_list_rx = set()
    #
    #     for row in tqdm(row_iter):
    #         if last_cid == 'initialize':
    #             last_cid = row[0]
    #             concept_str = []
    #
    #         current_cid = row[0]
    #         if current_cid != last_cid:
    #             if had_bn_in_pin:
    #                 if had_rxnorm_bn_in_pin:
    #                     count_rxnorm_bn_in_pin += 1
    #                     rxnorm_bn_in_pin.update(concept_str)
    #                 else:
    #                     count_bn_in_pin += 1
    #                     bn_in_pin.update(concept_str)
    #             else:
    #                 count_not_bn_in_pin += 1
    #                 not_bn_in_pin.update(concept_str)
    #             had_bn_in_pin = False
    #             had_rxnorm_bn_in_pin = False
    #             last_cid = current_cid
    #             concept_str = []
    #
    #         concept_str.append(row[14].lower())
    #         if row[12] in ('BN', 'IN', 'PIN'):
    #             had_bn_in_pin = True
    #             if row[11] == 'RXNORM':
    #                 had_rxnorm_bn_in_pin = True
    #                 concepts_list_rx.add(row[14].lower())
    #
    #     # for the last row
    #     if had_bn_in_pin:
    #         if had_rxnorm_bn_in_pin:
    #             count_rxnorm_bn_in_pin += 1
    #             rxnorm_bn_in_pin.update(concept_str)
    #         else:
    #             count_bn_in_pin += 1
    #             bn_in_pin.update(concept_str)
    #     else:
    #         count_not_bn_in_pin += 1
    #         not_bn_in_pin.update(concept_str)
    #
    # print('count_rxnorm_bn_in_pin - ' + str(count_rxnorm_bn_in_pin))
    # print('count_bn_in_pin - ' + str(count_bn_in_pin))
    # print('count_not_bn_in_pin - ' + str(count_not_bn_in_pin))
    #
    # print('rxnorm_bn_in_pin - ' + str(len(rxnorm_bn_in_pin & drugs)))
    # print('bn_in_pin - ' + str(len(bn_in_pin & drugs)))
    # print('not_bn_in_pin - ' + str(len(not_bn_in_pin & drugs)))
    # print('concepts_list_rx - ' + str(len(concepts_list_rx & drugs)))

    # print('xxxx - ' + str(len(drugs - (rxnorm_bn_in_pin | bn_in_pin))))
    # print(drugs - (rxnorm_bn_in_pin | bn_in_pin))
    # print('xxxx - ' + str((drugs - (rxnorm_bn_in_pin | bn_in_pin)) - (drugs - (rxnorm_bn_in_pin | bn_in_pin | not_bn_in_pin))))
