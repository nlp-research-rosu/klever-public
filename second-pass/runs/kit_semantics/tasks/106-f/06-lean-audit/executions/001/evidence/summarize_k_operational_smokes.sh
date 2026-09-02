#!/usr/bin/env bash
set -u

raw=/audit-output/evidence/17_fresh_k_operational_smokes.txt
clean=/tmp/audit-work/17_fresh_k_operational_smokes.clean.txt

echo '$ sed ANSI-control-codes from 17_fresh_k_operational_smokes.txt, then extract commands, exits, and heap result entries'
sed -E 's/\x1B\[[0-9;]*[mK]//g; s/\x1B\[[0-9;?]*[[:alpha:]]//g' "$raw" > "$clean"
rg '^\$ (kompile|krun)|^(kompile|krun)_exit=|    0 \|-> list' "$clean"
