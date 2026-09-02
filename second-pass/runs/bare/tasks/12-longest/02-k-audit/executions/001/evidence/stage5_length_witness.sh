#!/usr/bin/env bash
set -euo pipefail
cd /tmp/audit-work/12-longest-audit

cp /audit-output/evidence/length-witness.k length-witness.k
cp /audit-output/evidence/showlen-ascii.mpy showlen-ascii.mpy
cp /audit-output/evidence/showlen-bmp.mpy showlen-bmp.mpy
cp /audit-output/evidence/showlen-nonbmp.mpy showlen-nonbmp.mpy

echo '$ compile direct K lengthString witness'
kompile length-witness.k \
  --backend llvm \
  --enable-search \
  --main-module LENGTH-WITNESS \
  --syntax-module LENGTH-WITNESS \
  --output-definition length-witness-kompiled \
  --warnings none

for file in showlen-ascii.mpy showlen-bmp.mpy showlen-nonbmp.mpy; do
  echo "$ krun $file --pattern '<out> RESULT:Value </out>'"
  krun "$file" \
    --definition length-witness-kompiled \
    -cARGS='noneVal' \
    --pattern '<out> RESULT:Value </out>' \
    --output pretty
  echo "KRUN_EXIT_STATUS=$?"
done

echo 'SCRIPT_EXIT_STATUS=0'
