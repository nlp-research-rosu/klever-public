#!/usr/bin/env bash
set +e

work=/tmp/audit-work/68-pluck
cd "$work" || exit 90

run_bounded() {
  local label=$1
  shift
  local raw="$work/${label}.raw.log"
  echo "\$ $*"
  "$@" >"$raw" 2>&1
  local rc=$?
  local lines
  lines=$(wc -l <"$raw")
  echo "exit=$rc lines=$lines"
  if (( lines <= 160 )); then
    sed -n '1,160p' "$raw"
  else
    sed -n '1,80p' "$raw"
    echo "... [bounded log: middle omitted] ..."
    tail -80 "$raw"
  fi
  return "$rc"
}

echo '$ rm -rf /tmp/audit-work/68-pluck/runtime-audit-kompiled /tmp/audit-work/68-pluck/proof-audit-kompiled'
rm -rf \
  /tmp/audit-work/68-pluck/runtime-audit-kompiled \
  /tmp/audit-work/68-pluck/proof-audit-kompiled
echo "exit=$?"

run_bounded 03a_kompile_llvm \
  kompile reference-semantics/semantics.k \
    --backend llvm \
    --main-module MPY-KRUN \
    --syntax-module MPY-SYNTAX \
    --output-definition runtime-audit-kompiled
llvm_rc=$?

if (( llvm_rc == 0 )); then
  run_bounded 03b_krun_solution \
    krun solution.mpy --definition runtime-audit-kompiled
  krun_rc=$?
else
  krun_rc=99
fi

run_bounded 03c_kompile_haskell \
  kompile verification.k \
    --backend haskell \
    --main-module PLUCK-VERIFICATION \
    --syntax-module MPY-SYNTAX \
    --output-definition proof-audit-kompiled
haskell_rc=$?

if (( haskell_rc == 0 )); then
  run_bounded 03d_kprove_loop \
    kprove spec.k \
      --definition proof-audit-kompiled \
      --spec-module PLUCK-SPEC \
      --claims PLUCK-SPEC.pluck-loop \
      --output pretty
  loop_rc=$?

  run_bounded 03e_kprove_correct \
    kprove spec.k \
      --definition proof-audit-kompiled \
      --spec-module PLUCK-SPEC \
      --claims PLUCK-SPEC.pluck-correct,PLUCK-SPEC.pluck-loop \
      --trusted PLUCK-SPEC.pluck-loop \
      --output pretty
  correct_rc=$?
else
  loop_rc=99
  correct_rc=99
fi

echo "SUMMARY llvm=$llvm_rc krun=$krun_rc haskell=$haskell_rc loop=$loop_rc correct=$correct_rc"
if (( llvm_rc != 0 || krun_rc != 0 || haskell_rc != 0 || loop_rc != 0 || correct_rc != 0 )); then
  exit 1
fi
