#!/usr/bin/env bash
set +e
cd /tmp/audit-work/68-pluck || exit 90

run_bounded() {
  local label=$1
  shift
  local raw="/tmp/audit-work/68-pluck/${label}.raw.log"
  echo "\$ $*"
  "$@" >"$raw" 2>&1
  local rc=$?
  local lines
  lines=$(wc -l <"$raw")
  echo "exit=$rc lines=$lines"
  if (( lines <= 120 )); then
    sed -n '1,120p' "$raw"
  else
    sed -n '1,60p' "$raw"
    echo "... [bounded log: middle omitted] ..."
    tail -60 "$raw"
  fi
  return "$rc"
}

echo '$ rm -rf /tmp/audit-work/68-pluck/fixed-audit-kompiled'
rm -rf /tmp/audit-work/68-pluck/fixed-audit-kompiled
echo "exit=$?"

run_bounded 05a_kompile_fixed \
  kompile fixed-audit.k \
    --backend haskell \
    --main-module FIXED-AUDIT \
    --syntax-module MPY-SYNTAX \
    --output-definition fixed-audit-kompiled
build_rc=$?

if (( build_rc == 0 )); then
  run_bounded 05b_kprove_iter_connection \
    kprove iter-bridge-connection.k \
      --definition fixed-audit-kompiled \
      --spec-module ITER-BRIDGE-CONNECTION \
      --output pretty
  proof_rc=$?
else
  proof_rc=99
fi

echo "SUMMARY build=$build_rc proof=$proof_rc"
if (( build_rc != 0 || proof_rc != 0 )); then
  exit 1
fi
