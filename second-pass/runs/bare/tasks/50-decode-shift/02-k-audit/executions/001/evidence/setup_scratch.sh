#!/usr/bin/env bash
set -euo pipefail

scratch=/tmp/audit-work/50-decode-shift
candidate_src="$scratch/candidate-src"
trusted_src="$scratch/trusted"

if [[ -e "$scratch" ]]; then
  echo "refusing to reuse existing scratch directory: $scratch" >&2
  exit 65
fi

mkdir -p "$candidate_src" "$trusted_src"
cp -- /candidate/solution.py /candidate/solution.mpy /candidate/semantic.k \
  /candidate/spec.k /candidate/verification.k "$candidate_src/"
cp -- /reference/canonical.py /reference/prompt.py /reference/py2mpy.py \
  "$trusted_src/"

find "$scratch" -type f -printf '%P\t%s bytes\n' | sort
