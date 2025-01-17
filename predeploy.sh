#!/bin/bash

# Run Python build
poetry run python3 build.py

# Run Yarn build
yarn build
