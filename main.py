
if __name__ == '__main__':

    aliasesFields = {'synonym': '900000000000013009', 'fully specified name': '900000000000003001'}

    with open('concepts.txt') as con:
        concept_dict = {}
        for line in con:
            row = line.strip().split('\t')
            if row[2] == '1':
                concept_dict[row[0]] = {'name': '', 'preferred synonym': [], 'synonyms': [],
                                        'preferred fully specified name': [], 'fully specified names': []}

    with open('language.txt') as lang:
        prefer_terms = []
        for line in lang:
            row = line.strip().split('\t')
            if row[2] == '1' and row[4] == '900000000000509007' and row[6] == '900000000000548007':
                prefer_terms.append(row[5])

    with open('description.txt') as desc:
        for line in desc:
            row = line.strip().split('\t')
            if row[2] == '1' and row[5] == 'en':
                if row[6] == aliasesFields['synonym'] and row[0] in prefer_terms:
                    concept_dict[row[4]]['preferred synonym'].append(row[7])
                    concept_dict[row[4]]['name'] = row[7]
                elif row[6] == aliasesFields['fully specified name'] and row[0] in prefer_terms:
                    concept_dict[row[4]]['preferred fully specified name'].append(row[7])
                elif row[6] == aliasesFields['synonym']:
                    concept_dict[row[4]]['synonyms'].append(row[7])
                elif row[6] == aliasesFields['fully specified name']:
                    concept_dict[row[4]]['fully specified names'].append(row[7])

    for k in concept_dict.keys():
        print(str(k) + ' ' + str(concept_dict[k]))
    print('\n')

    with open('relationships.txt') as relation:
        is_a_dict = {}
        for line in relation:
            row = line.strip().split('\t')
            if row[2] == '1' and row[7] == '116680003':
                if row[5] in is_a_dict:
                    is_a_dict[row[5]].append(row[4])
                else:
                    is_a_dict[row[5]] = [row[4]]

    for k in is_a_dict.keys():
        print(str(k) + ' ' + str(is_a_dict[k]))
