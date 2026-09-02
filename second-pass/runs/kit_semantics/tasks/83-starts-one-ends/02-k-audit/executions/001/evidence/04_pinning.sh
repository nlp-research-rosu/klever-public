#!/usr/bin/env bash
set -uo pipefail

scratch_path=$(sed -n '1p' /audit-output/evidence/scratch-path.txt)
log_path=/audit-output/evidence/04_pinning.log
exec >"$log_path" 2>&1

run() {
    printf '\n$'
    printf ' %q' "$@"
    printf '\n'
    "$@"
    local status=$?
    printf '[exit %d]\n' "$status"
    return 0
}

printf 'Claim adequacy and program pinning (UTC): '
date -u +%Y-%m-%dT%H:%M:%SZ

run python3 /audit-output/evidence/04_constructor_pinning.py \
    "$scratch_path/solution.mpy" \
    "$scratch_path/spec.k" \
    "$scratch_path/trusted-canonical.py" \
    "$scratch_path/solution.py"

run sed -n 123,215p "$scratch_path/reference-semantics/semantics/core.k"
run sed -n 62,95p "$scratch_path/reference-semantics/semantics/functions.k"
run sed -n 15,24p "$scratch_path/reference-semantics/semantics/call.k"
run sed -n 69,75p "$scratch_path/reference-semantics/semantics/call.k"
run sed -n 50,61p "$scratch_path/reference-semantics/semantics/controls.k"
run sed -n 10,18p "$scratch_path/reference-semantics/semantics/operators.k"
run sed -n 7,27p "$scratch_path/reference-semantics/semantics/int.k"

module_log="$scratch_path/reviewer-module-load.raw.log"
printf '\n$ cd %q && krun solution.mpy --definition reviewer-runtime-kompiled --output pretty\n' "$scratch_path"
(
    cd "$scratch_path" &&
    krun solution.mpy --definition reviewer-runtime-kompiled --output pretty
) >"$module_log" 2>&1
module_status=$?
printf '[exit %d]\n' "$module_status"
printf '[raw output: %s; ' "$module_log"
wc -c <"$module_log" | tr -d '\n'
printf ' bytes]\n'
sed -n '1,240p' "$module_log"

printf '\nScript exit: 0 (individual command statuses above)\n'
