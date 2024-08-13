from fastapi import FastAPI

from models.GradingRequest import GradingRequest

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "world"}


@app.post("/gradeSubmissions")
def perform_grading(grading_request: GradingRequest):
    return grading_request
