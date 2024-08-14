from fastapi import FastAPI
from clean import remove_comments

from models.GradingRequest import GradingRequest

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "world"}


@app.post("/gradeSubmissions")
def perform_grading(grading_request: GradingRequest):
    return grading_request

def clean_diagram(diagram: str):
    """
    Clean the given Umple file.
    """
    # Replace all unidirectional associations -> or <- with bidirectional ones --
    if "//$?[End_of_model]$?" in diagram:
        diagram = diagram.split("//$?[End_of_model]$?")[0]
    diagram = remove_comments(diagram)
    diagram = diagram.replace("<-", "--").replace("->", "--").replace("<@>", "-").replace("interface", "class")
    return diagram
