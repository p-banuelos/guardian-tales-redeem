#!/bin/bash

if ! find . -name "*.pyc" | read
then
  python3.12 -m compileall . > /dev/null 2>&1
fi

python3.12 guardian_tales/main.py