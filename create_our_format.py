import json

# numbering the concepts in the hierarchy
hierarchy_id = 1


# A function that creates a json file of taxonomy with our format
# parameters:
# concept_dict - a dictionary where the key is the concept ID and the value is a dictionary like: {'name': 'canonical name', 'alias_group_name1': [], 'alias_group_name2': [] ,etc...}
# is_a_dict - a dictionary that contain the hierarchy of the taxonamy, the key is the concepts ID of the 'father' and the value is an array of all his children's concept ID
# concept_without_father - an array that contains the concepts ID that doesn't have a father - to know where to start building the hierarchy
# aliases_fields - an array that contains alias group names
# folder_name - folder name (str) where we want to save the taxonomy in our format
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
