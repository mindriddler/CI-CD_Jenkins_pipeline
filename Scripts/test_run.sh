#!/bin/bash

python3 -m venv ../venv

source ../venv/bin/activate

pip install -r ../backend/requirements.txt --quiet

pylint --fail-under 8 ../backend/pingurl/ 

pytest ../backend/