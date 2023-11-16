#!/bin/bash

cd ../backend

source venv/bin/activate

pip install -r requirements.txt --quiet

pylint --fail-under 8 pingurl/ 

pytest .