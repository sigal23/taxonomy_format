from typing import List, Union, Dict, Set

# common types
AliasObject = Union[str, List[str], Set[str]]
ConceptDict = Dict[str, Dict[str, AliasObject]]
IsADict = Dict[str, List[str]]
ConceptWithoutFather = List[str]
