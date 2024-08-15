from fastapi import FastAPI
from clean import remove_comments
from models.MarkingScheme import MarkingScheme
from models.Submission import Submission
from typing import List
from heuristic_grader import get_association_multiplicities, grade_submission

from models.GradingRequest import GradingRequest

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "world"}


@app.post("/gradeSubmissions")
def perform_grading(grading_request: GradingRequest):
    for submission in grading_request.submissions:
        submission.model = clean_diagram(submission.model)
    grading_request.mod_solution = clean_diagram(grading_request.mod_solution)

    return {"request": grading_request, "result": grade_all_using_heuristic(grading_request.marking_scheme, grading_request.submissions, grading_request.mod_solution)}

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

def grade_all_using_heuristic(marking_scheme: MarkingScheme, submissions: List[Submission], model_solution: str):
    global IDEAL_ASSOC_MULTS
    result = []

    IDEAL_ASSOC_MULTS = get_association_multiplicities(model_solution, bidirectional=True)
    print(IDEAL_ASSOC_MULTS)

    for index, submission in enumerate(submissions):
        result.append(grade_submission((str(index), submission.model), marking_scheme))

    result.sort(key=lambda x: x[0])

    for r in result:
        print(",".join(map(str, r)))

    return result
