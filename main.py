import json
from tqdm import tqdm


if __name__ == '__main__':

    aliasesFields = {'synonym': '900000000000013009', 'fully specified name': '900000000000003001'}

    with open('sct2_Concept_Snapshot_US1000124_20220301.txt') as con:
        concept_dict = {}
        for line in tqdm(con):
            row = line.strip().split('\t')
            if row[2] == '1':
                concept_dict[row[0]] = {'name': '', 'preferred synonym': [], 'synonyms': [],
                                        'preferred fully specified name': [], 'fully specified names': []}

    with open('der2_cRefset_LanguageSnapshot-en_US1000124_20220301.txt') as lang:
        prefer_terms = []
        for line in tqdm(lang):
            row = line.strip().split('\t')
            if row[2] == '1' and row[4] == '900000000000509007' and row[6] == '900000000000548007':
                prefer_terms.append(row[5])

    with open('sct2_Description_Snapshot-en_US1000124_20220301.txt') as desc:
        for line in tqdm(desc):
            row = line.strip().split('\t')
            if row[2] == '1' and row[5] == 'en' and row[4] in concept_dict:
                if row[6] == aliasesFields['synonym']:
                    if row[0] in prefer_terms:
                        concept_dict[row[4]]['preferred synonym'].append(row[7])
                        concept_dict[row[4]]['name'] = row[7]
                    else:
                        concept_dict[row[4]]['synonyms'].append(row[7])
                elif row[6] == aliasesFields['fully specified name']:
                    if row[0] in prefer_terms:
                        concept_dict[row[4]]['preferred fully specified name'].append(row[7])
                    else:
                        concept_dict[row[4]]['fully specified names'].append(row[7])

    with open('sct2_Relationship_Snapshot_US1000124_20220301.txt') as relation:
        is_a_dict = {}
        concept_without_father = list(concept_dict.keys())
        for line in tqdm(relation):
            row = line.strip().split('\t')
            if row[2] == '1' and row[7] == '116680003' and row[4] in concept_dict and row[5] in concept_dict:
                if row[5] in is_a_dict:
                    is_a_dict[row[5]].append(row[4])
                else:
                    is_a_dict[row[5]] = [row[4]]
                if row[4] in concept_without_father:
                    concept_without_father.remove(row[4])

    # for k in concept_dict.keys():
    #     print(str(k) + ' ' + str(concept_dict[k]))
    # print('\n')
    # for k in is_a_dict.keys():
    #     print(str(k) + ' ' + str(is_a_dict[k]))
    # print('\n')
    # print(concept_without_father)

    with open("concepts.json", 'w') as f:
        json.dump(concept_dict, f)

    with open("is_a.json", 'w') as f:
        json.dump(is_a_dict, f)

    with open("concept_without_father.json", 'w') as f:
        json.dump(concept_without_father, f)

    # loaded_json = json.load(f)
