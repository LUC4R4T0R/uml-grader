from pydantic import BaseModel
from typing import Dict, List
from models.Submission import Submission
from models.MarkingScheme import MarkingScheme


class GradingRequest(BaseModel):
    markingScheme: MarkingScheme
    submissions: List[Submission]
