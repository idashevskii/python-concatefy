#!/bin/bash
set -e
cd "$(dirname "${BASH_SOURCE[0]}")/"

# source .venv/bin/activate

echo $@

python -m python_concatefy.main $@
