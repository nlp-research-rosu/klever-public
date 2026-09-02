#!/usr/bin/env bash
set -euo pipefail
cd /tmp/audit-work/12-longest-audit

export PATH="/home/agent/.nix-profile/bin:$PATH"

echo '$ compare fully macro-expanded submitted solution.mpy and longestProgram'
kast solution.mpy \
  --definition verification-fresh-kompiled \
  --module VERIFICATION \
  --sort Stmt \
  --expand-macros \
  --output kore \
  --output-file /audit-output/evidence/kast-solution.kore
kast \
  --expression longestProgram \
  --definition verification-fresh-kompiled \
  --module VERIFICATION \
  --sort Stmt \
  --expand-macros \
  --output kore \
  --output-file /audit-output/evidence/kast-longestProgram.kore
cmp /audit-output/evidence/kast-solution.kore \
    /audit-output/evidence/kast-longestProgram.kore
echo "EXPANDED_PROGRAM_CMP_EXIT=$?"
sha256sum /audit-output/evidence/kast-solution.kore \
          /audit-output/evidence/kast-longestProgram.kore

echo '$ install reviewer ground interpretation in scratch'
cp /audit-output/evidence/ground-witness.k ground-witness.k

echo '$ kompile ground-witness.k --backend llvm --enable-search --main-module GROUND-WITNESS --syntax-module MPY-SYNTAX --output-definition ground-witness-kompiled'
kompile ground-witness.k \
  --backend llvm \
  --enable-search \
  --main-module GROUND-WITNESS \
  --syntax-module MPY-SYNTAX \
  --output-definition ground-witness-kompiled \
  --warnings none

echo '$ empty entry witness: ID="empty", I=0, N=0'
krun solution.mpy \
  --definition ground-witness-kompiled \
  -cARGS='seqVal("empty",0,0)' \
  --pattern '<out> noneVal </out>' \
  --output pretty

echo '$ nonempty entry witness: ID="growth", I=0, N=3'
echo '$ substitution: firstInSeq(stringAt("growth",0),"growth",0,3) = "ccc"'
echo '$ Python canonical and candidate on ["a","bb","ccc"] both return "ccc" (stage2_fidelity.log)'
krun solution.mpy \
  --definition ground-witness-kompiled \
  -cARGS='seqVal("growth",0,3)' \
  --pattern '<out> strVal("ccc") </out>' \
  --output pretty

echo 'SCRIPT_EXIT_STATUS=0'
