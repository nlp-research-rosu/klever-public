#!/usr/bin/env bash
set -u

work=/tmp/audit-work/126-is-sorted/candidate-src
translator=/tmp/audit-work/126-is-sorted/trusted/py2mpy.py

cd "$work" || exit 2
echo "COMMAND: python3 $translator solution.py | sha256sum"
python3 "$translator" solution.py | sha256sum
pipe_status=("${PIPESTATUS[@]}")
translator_exit=${pipe_status[0]}
hash_exit=${pipe_status[1]}
echo "TRANSLATOR_EXIT=$translator_exit"
echo "HASH_EXIT=$hash_exit"

echo "COMMAND: cmp -l solution.mpy <(python3 $translator solution.py)"
cmp -l solution.mpy <(python3 "$translator" solution.py)
cmp_exit=$?
echo "CMP_EXIT=$cmp_exit"

if (( translator_exit != 0 || hash_exit != 0 || cmp_exit != 0 )); then
    exit 1
fi
