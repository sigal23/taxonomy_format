import json

aliasesFields = ['preferred synonym', 'synonyms', 'preferred fully specified name', 'fully specified names']
f = open('snomed/concepts.json')
concept_dict = json.load(f)
f = open('snomed/is_a.json')
is_a_dict = json.load(f)
f = open('snomed/concept_without_father.json')
concept_without_father = json.load(f)
id = 1


def create_hierarchy(conc_id):
    global id
    id = id + 1
    if conc_id not in is_a_dict:
        aliases = {}
        for alias in aliasesFields:
            if len(concept_dict[conc_id][alias]) > 0:
                aliases[alias] = concept_dict[conc_id][alias]
        concept_leaf = {"name": concept_dict[conc_id]["name"], "id": id, "state": {"aliases": aliases}, "children": []}
        return concept_leaf

    aliases = {}
    for alias in aliasesFields:
        if len(concept_dict[conc_id][alias]) > 0:
            aliases[alias] = concept_dict[conc_id][alias]
    concept = {"name": concept_dict[conc_id]["name"], "id": id, "state": {"aliases": aliases}, "children": []}

    children = is_a_dict[conc_id]
    for c in children:
        concept["children"].append(create_hierarchy(c))

    return concept


def create_our_format():

    root = {"name": "root", "id": 1, "state": {"aliases": {aliasesFields[0]: ["all"]}}, "children": []}

    if len(concept_without_father) == 1:
        global id
        id = 0
        hierarchy = create_hierarchy(concept_without_father[0])
        root["children"] = hierarchy["children"]
    else:
        root["children"] = [create_hierarchy(c) for c in concept_without_father]

    with open("snomed/snomed_our_format.json", "w") as fi:
        json.dump({"nodes": [root], "aliasesFields": aliasesFields}, fi)
