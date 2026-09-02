#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

python3 py2mpy.py solution.py > solution.mpy

python3 -c 'from solution import how_many_times; cases = [("", "a", 0), ("aaa", "a", 3), ("aaaa", "aa", 3), ("", "", 1), ("abc", "", 4), ("abababa", "aba", 3), ("abc", "z", 0)]; assert all(how_many_times(s, t) == n for s, t, n in cases)'

kompile semantic.k --main-module SEMANTIC --syntax-module MPY-SYNTAX --backend llvm
krun solution.mpy --definition semantic-kompiled
run_output="$(krun run-example.mpy --definition semantic-kompiled)"
printf '%s\n' "$run_output"
grep -q 'intVal ( 3 )' <<<"$run_output"

kompile verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX --backend haskell
kprove spec.k --definition verification-kompiled
