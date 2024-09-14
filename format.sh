#!/bin/bash
poetry run isort --profile black .
poetry run black .
