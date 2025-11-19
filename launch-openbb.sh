#!/bin/bash
# OpenBB CLI Launch Script
# This script activates the virtual environment and launches the OpenBB CLI

# Activate the virtual environment
source /Users/sdg223157/OPBB/openbb-env/bin/activate

# Launch OpenBB CLI with all arguments passed to this script
openbb "$@"
