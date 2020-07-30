# UML Class Diagram Automated ML Grader

## Authors

[Younes Boubekeur](https://github.com/YounesB-McGill),
[Gunter Mussbacher](https://github.com/gmussbacher/),
[Shane McIntosh](https://github.com/smcintosh)

## About

This application grades student [UML class diagrams](https://www.omg.org/spec/UML/About-UML/) based on a model (ideal) solution.
It uses a heuristic and machine learning techniques to classify student submissions into higher or lower quality or predict their letter grade (A-F).

A research paper covering this tool was submitted to the [MODELS 2020 Conference](https://conf.researchr.org/home/models-2020).

## System components

The following image shows the grading process used for this project.

<div style="text-align:center;"><img src="figures/documentation/system_design.png"><br></div>

In this repository, we provide the following information:

1. Example student [assignment](data/assignment_sample_data) and
[final exam](data/final_exam_sample_data) submissions. We are unable to make 
the entire datasets public due to copyright and ethics considerations.
1. Data representing the [human grades](data/LG_grading_a2_final.csv), _i.e._,
the ground truth, for the assignment and final exam.
1. The [code](clean.py) used to extract and clean the raw data.
1. The [heuristic algorithm](heuristic_grader.py).
1. The [machine learning predictors](predictor.py).
1. The Ecore to TouchCore class diagram model transformation [code](ecore2cdm.py).
1. The TouchCore model compare [automation script](tc_controller.sh).
1. The [utility scripts](utils.py) used to compute and visualize results.

## Running the code

Below we provide instructions to run the different parts of the experiment.
We also provide intermediate artifacts to aid persons seeking to replicate
part of the study. Since all three parts have Python dependencies,
configure a virtual environment on your local machine according to
[Pipenv instructions](https://pipenv-fork.readthedocs.io/en/latest/install.html).

### Grading with the heuristic

To grade an Umple model using the simple heuristic, it must first be
[cleaned](clean.py):

```bash
$ ./clean.py ${UMPLE_FILE}
```

Then, run this command to obtain the heuristic grades on standard out as demonstrated below:

```bash
$ ${HEURISTIC_GRADER} ${MARKING_SCHEME} ${UMPLE_FILES_DIR} [showExtras]

# Example 1: First pass for assignment. Run from this folder.
$ ./heuristic_grader.py data/assignment/marking_scheme.json data/assignment/ showExtras

0,6,12,13,13
12,4,12,9,5
{}  # Empty since not enough samples
{}

# Example 2: Second pass for final exam question
$ ./heuristic_grader.py data/final_exam/marking_scheme.json data/final_exam/

0,18,15,25,25
6,13,8,13,8
```

The column order is as follows:

```
SubmissionId,Classes,Attributes,Associations,Multiplicities
```

If `showExtras` were run on a sufficiently large dataset, it would yield 
results resembling what we obtained for extra classes and attributes, respectively:

```json
{
  "Precondition": 50,
  "Action": 48,
  "InfrastructureMap": 41,
  "Alert": 25,
  "Owner": 21,
  "Command": 20,
  ...
}
{
  "address": 78,
  "measuredValue": 52,
  "timeStamp": 47,
  "Time": 46,
  "Completed": 46,
  "Failed": 45,
  ...
}
```

### Grading with machine learning classifiers

This can be done with the `predictor.py` file. More details coming soon.

### Grading Umple models in TouchCore

To grade Umple models in TouchCore, they must first be [cleaned](clean.py)
(see above), 
transformed to Eclipse Ecore format and then to TouchCore's internal format. 
To convert to Ecore:

```bash
$ ${UMPLE} --generate Ecore ${FILENAME}
```

where `${UMPLE}` is the Umple compiler executable and `${FILENAME}` is the
Umple file to be converted. The output is an `*.ecore` file.

It is possible to convert `*.ecore` files to `.cdm` using our
[`ecore2cdm.py`](ecore2cdm.py) model transformation:

```bash
$ ./ecore2cdm.py ${ECORE_DIR} ${CDM_DIR}
```

The last step requires importing the ideal solution and student solution 
`*.cdm` files into a TouchCore project according to the
[user guide](https://bitbucket.org/mcgillram/touchram/wiki/touchcore-user-guide).
At the time of writing, the student grade can be obtained while on the 
[`comparing-model`](https://bitbucket.org/mcgillram/touchram/branch/comparing-model)
branch in the touchram repository (see below for exact version used in the experiement).
This can be done manually for a small number of files.
Alternatively, it is possible to run our model compare [automation script](tc_controller.sh) in batch mode,
although it will require modifying its file paths and the
[Python helper file](tc_gui_grader.py).

We provide `*.ecore` and `.cdm` files for the ideal solutions and sample 
student submissions.


## Dependency versions

Umple version: `445d1d99b542c85c9a694ef78a6dad5c7794b0b2`

TouchCore CORE version: `e66b47c444a04ded0a4d4aed1f23d40207de177e`

TouchCore RAM version: `5a067eab574c2dbd90af656d1bbfc7c34da1e7e0`

Versions of Python packages are shown in the `requirements.txt` file.
