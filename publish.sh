#!/bin/bash

# Build and publish:
# poetry build
# bash publish.sh

set -eo pipefail
poetry publish || echo "ERROR publish"
git tag v$(poetry version -s) || echo "ERROR tag"
git push --tags || echo "ERROR push tags"
