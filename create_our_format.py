import json

# numbering the concepts in the hierarchy
hierarchy_id = 1


# A function that creates a json file of taxonomy with our format
def create_our_format(concept_dict, is_a_dict, concept_without_father, aliases_fields, folder_name):
    # A recursive function that creates the hierarchy of concepts
    def create_hierarchy(conc_id):
        global hierarchy_id
        hierarchy_id = hierarchy_id + 1
        aliases = {}
        for alias in aliases_fields:
            # Only if the concept has aliases of a certain type will we add,
            # if empty we will not add to the concept the alias title
            if len(concept_dict[conc_id][alias]) > 0:
                aliases[alias] = concept_dict[conc_id][alias]
        # Stop conditions when we reached the leaf - a concept that has no children and
        # in this case "is_a_dict.get (conc_id, [])" will return an empty array and the recursion will start to go back
        concept = {"name": concept_dict[conc_id]["name"], "id": hierarchy_id, "state": {"aliases": aliases},
                   "children": [create_hierarchy(c) for c in is_a_dict.get(conc_id, [])]}
        return concept

    # Creating a fictitious root whose children are all concepts that have no parents
    root = {"name": "root", "id": 1, "state": {"aliases": {aliases_fields[0]: ["all"]}},
            "children": [create_hierarchy(c) for c in concept_without_father]}

    # Save the taxonomy in our format
    with open(folder_name + "/taxonomy_our_format.json", "w") as fi:
        json.dump({"nodes": [root], "aliasesFields": aliases_fields}, fi)
