#!/bin/bash

# Build and publish:
# poetry build
# bash publish.sh

set -eo pipefail
poetry publish
git tag v$(poetry version -s)
git push --tags
