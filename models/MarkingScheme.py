from pydantic import BaseModel
from typing import List


class MarkingScheme(BaseModel):
    name: str
    nClasses: int
    nAssoc: int
    expectedClasses: List[List[str]]
    expectedAttributes: List[str]
