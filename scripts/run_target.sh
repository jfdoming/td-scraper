#!/bin/bash
set -euo pipefail

export PROJECT_ROOT="$1"
export PROJECT_SOURCES_FILE="$PROJECT_ROOT/.sources"
export BUILD_ROOT="$PROJECT_ROOT/../chromium-python-lambda"

if [ -f .env ]; then
    source .env
fi

cd "$BUILD_ROOT"
make "$2"
