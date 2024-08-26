from pydantic import BaseModel
from typing import Union


class Submission(BaseModel):
    submissionId: str
    submissionEntryId: str
    model: str
    points: Union[int, float, None]
