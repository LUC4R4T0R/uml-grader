from pydantic import BaseModel


class Submission(BaseModel):
    submissionId: str
    submissionEntryId: str
    model: str
