#!/usr/bin/env bash
set +e
cd /tmp/audit-work/68-pluck || exit 90
raw=/tmp/audit-work/68-pluck/03g_kprove_correct.raw.log

echo '$ timeout 300s kprove spec.k --definition proof-audit-kompiled --spec-module PLUCK-SPEC --claims PLUCK-SPEC.pluck-correct,PLUCK-SPEC.pluck-loop --trusted PLUCK-SPEC.pluck-loop --output pretty'
timeout 300s kprove spec.k \
  --definition proof-audit-kompiled \
  --spec-module PLUCK-SPEC \
  --claims PLUCK-SPEC.pluck-correct,PLUCK-SPEC.pluck-loop \
  --trusted PLUCK-SPEC.pluck-loop \
  --output pretty >"$raw" 2>&1
rc=$?
lines=$(wc -l <"$raw")
echo "exit=$rc lines=$lines"
if (( lines <= 160 )); then
  sed -n '1,160p' "$raw"
else
  sed -n '1,80p' "$raw"
  echo "... [bounded log: middle omitted] ..."
  tail -80 "$raw"
fi
exit "$rc"
