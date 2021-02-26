# FLMT
File-Level Mutation Testing

## Usage
0. Install dependencies:
```
pip install -r requirements.txt
```
1. Current version: only works with projects written in Python and tested by pytest.
2. Get dependency matrix:
```
python src/mutation.py PATH_TO_THE_PROJECT
```
Dependency matrx will be in the [output/](https://github.com/hil-se/FLMT/tree/main/output) folder.
