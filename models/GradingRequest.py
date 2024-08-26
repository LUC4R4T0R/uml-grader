from pydantic import BaseModel
from typing import List, Union
from models.Submission import Submission
from models.MarkingScheme import MarkingScheme


class GradingRequest(BaseModel):
    marking_scheme: MarkingScheme
    mod_solution: str
    submissions: List[Submission]
    max_points: Union[int, float]
