import json

# numbering the concepts in the hierarchy
hierarchy_id = 1


# A function that creates a json file of taxonomy with our format
def create_our_format(concept_dict, is_a_dict, concept_without_father, aliases_fields):
    def create_hierarchy(conc_id):
        global hierarchy_id
        hierarchy_id = hierarchy_id + 1
        aliases = {}
        for alias in aliases_fields:
            if len(concept_dict[conc_id][alias]) > 0:
                aliases[alias] = concept_dict[conc_id][alias]
        concept = {"name": concept_dict[conc_id]["name"], "id": hierarchy_id, "state": {"aliases": aliases},
                   "children": [create_hierarchy(c) for c in is_a_dict.get(conc_id, [])]}
        return concept

    root = {"name": "root", "id": 1, "state": {"aliases": {aliases_fields[0]: ["all"]}},
            "children": [create_hierarchy(c) for c in concept_without_father]}

    with open("snomed/snomed_our_format.json", "w") as fi:
        json.dump({"nodes": [root], "aliasesFields": aliases_fields}, fi)
