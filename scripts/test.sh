#!/bin/bash

set -e

poetry run python -m black --check obschartapp tests
poetry run python -m mypy obschartapp tests
pyright
