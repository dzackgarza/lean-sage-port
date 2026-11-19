#!/usr/bin/env python3
"""Run the local gate from the commit hook.

The shared commit hook (`~/ai-review-ci/repo-hooks/pre-commit`) runs this file after its syntax
check, with `--mode staged` or `--mode push` and the changed paths on standard input. The commit
runs `just test`; the push repeats nothing, because each pushed commit already passed it.
"""

import argparse
import subprocess
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--mode", choices=["staged", "push"], required=True)
args = parser.parse_args()
sys.stdin.read()
if args.mode == "staged":
    sys.exit(subprocess.run(["just", "test"]).returncode)
