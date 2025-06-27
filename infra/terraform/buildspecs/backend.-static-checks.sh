#!/bin/bash

pip install -r backend/requirements-dev.txt

pip install -r backend/requirements.txt

ruff check backend/*.py --fix

ruff format backend/*.py

mypy --config-file backend/pyproject.toml backend/