from pydantic import BaseModel
from typing import List
from typing_extensions import TypedDict


class MarkingScheme(TypedDict):
    name: str
    nClasses: int
    nAssoc: int
    expectedClasses: List[List[str]]
    expectedAttributes: List[str]
