from fastapi import FastAPI
from clean import remove_comments
from models.MarkingScheme import MarkingScheme
from models.Submission import Submission
from typing import List
from heuristic_grader import get_association_multiplicities, grade_submission
import numpy as np

from models.GradingRequest import GradingRequest

from predictor import classifiers, train_model

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "world"}


@app.post("/gradeSubmissions")
def perform_grading(grading_request: GradingRequest):
    for submission in grading_request.submissions:
        submission.model = clean_diagram(submission.model)
    grading_request.mod_solution = clean_diagram(grading_request.mod_solution)

    heuristic_results = grade_all_using_heuristic(grading_request.marking_scheme, grading_request.submissions, grading_request.mod_solution, grading_request.max_points)

    '''
    classifiers = [
        LogisticRegression(C=1e5, max_iter=2000),
        GaussianNB(var_smoothing=0.1),
        RandomForestClassifier(),
        # Also gives same results for 3, 5, 7, 12
        KNeighborsClassifier(n_neighbors=2),
        DecisionTreeClassifier()
    ]
    '''

    models = train_models(classifiers, heuristic_results)
    grading_results = ml_grading(models, heuristic_results)

    print(grading_results)
    return grading_results

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


def grade_all_using_heuristic(marking_scheme: MarkingScheme, submissions: List[Submission], model_solution: str, max_points: float):
    global IDEAL_ASSOC_MULTS
    result = []

    IDEAL_ASSOC_MULTS = get_association_multiplicities(model_solution, bidirectional=True)
    print(IDEAL_ASSOC_MULTS)

    for index, submission in enumerate(submissions):
        result.append({'id': submission.submissionId, 'heuristic': grade_submission((str(index+1), submission.model), marking_scheme), 'points': submission.points})

    result.sort(key=lambda x: x['heuristic'][0])
    result.insert(0, {'id': None, 'heuristic': grade_submission((str(0), model_solution), marking_scheme), 'points': max_points})
    result.insert(0, {'id': None, 'heuristic': [-1, 0, 0, 0, 0], 'points': 0})

    for r in result:
        print(",".join(map(str, r['heuristic'])))

    return result


def train_models(models, heuristic_results):
    training_data = [x for x in heuristic_results if isinstance(x['points'], int) or isinstance(x['points'], float)]
    if len(training_data) < 1:
        raise RuntimeError('no training data')

    x_train = []
    y_train = []
    for dataset in training_data:
        x_train.append(get_heuristic_values(dataset))
        y_train.append(dataset['points'])

    return [train_model(model, x_train, y_train) for model in models]

def ml_grading(models, heuristic_results):
    input_data = np.array([get_heuristic_values(dataset) for dataset in heuristic_results]).astype(float)
    results_by_model = [predict_grades(model, input_data) for model in models]
    results_by_submission = np.rot90(results_by_model, 3)

    return [{'id': dataset['id'], 'model_results': results_by_submission[index].tolist()} for index, dataset in enumerate(heuristic_results)]

def predict_grades(model, input_data):
    return model.predict(input_data)

def get_heuristic_values(dataset):
    return dataset['heuristic'][1:4]
