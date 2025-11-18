#!/bin/bash

# Use venv python if available, otherwise fall back to system python3
if [ -f "venv/bin/python3" ]; then
    venv/bin/python3 cmoney.py "$@"
else
    python3 cmoney.py "$@"
fi