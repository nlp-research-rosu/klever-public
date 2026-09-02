#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/0-has-close-elements
evidence=/audit-output/evidence
failures=0

run_bounded() {
  local label=$1
  shift
  local raw="$scratch/${label}.raw.log"
  local log="$evidence/${label}.log"

  {
    printf '$'
    printf ' %q' "$@"
    printf '\n'
  } > "$log"

  "$@" > "$raw" 2>&1
  local status=$?
  local lines bytes
  lines=$(wc -l < "$raw")
  bytes=$(wc -c < "$raw")
  {
    printf 'exit_status=%s\n' "$status"
    printf 'raw_output_lines=%s raw_output_bytes=%s\n' "$lines" "$bytes"
    if (( lines <= 320 )); then
      cat "$raw"
    else
      printf '%s\n' '--- first 140 lines ---'
      head -n 140 "$raw"
      printf '%s\n' '--- middle omitted from bounded reviewer log ---'
      printf '%s\n' '--- last 160 lines ---'
      tail -n 160 "$raw"
    fi
  } >> "$log"
  rm -f "$raw"
  printf '%s exit=%s lines=%s bytes=%s\n' "$label" "$status" "$lines" "$bytes"
  return "$status"
}

printf '%s\n' '$ find scratch for preexisting compiled definitions/caches'
find -P "$scratch" -maxdepth 2 \
  \( -iname '*kompiled*' -o -iname '*cache*' \) -print | sort
printf 'prebuild_find_exit=%s\n' "$?"

cd "$scratch" || exit 1
export PATH="$HOME/.nix-profile/bin:$PATH"

run_bounded stage3-build-llvm \
  kompile reference-semantics/semantics.k \
    --backend llvm \
    --main-module MPY-KRUN \
    --syntax-module MPY-SYNTAX \
    --output-definition audit-runtime-kompiled ||
  failures=$((failures + 1))

run_bounded stage3-build-verification-base \
  kompile --backend haskell verification.k \
    --main-module VERIFICATION-BASE \
    --syntax-module MPY-SYNTAX \
    --output-definition audit-verification-base-kompiled ||
  failures=$((failures + 1))

run_bounded stage3-prove-inner \
  kprove spec.k \
    --definition audit-verification-base-kompiled \
    --spec-module SPEC-INNER ||
  failures=$((failures + 1))
if ! grep -Fxq '#Top' "$evidence/stage3-prove-inner.log"; then
  printf '%s\n' 'missing_exact_top=1' >> "$evidence/stage3-prove-inner.log"
  failures=$((failures + 1))
else
  printf '%s\n' 'exact_top=1' >> "$evidence/stage3-prove-inner.log"
fi

run_bounded stage3-build-verification-inner \
  kompile --backend haskell verification.k \
    --main-module VERIFICATION-INNER \
    --syntax-module MPY-SYNTAX \
    --output-definition audit-verification-inner-kompiled ||
  failures=$((failures + 1))

run_bounded stage3-prove-outer-state \
  kprove spec.k \
    --definition audit-verification-inner-kompiled \
    --spec-module SPEC-OUTER-STATE ||
  failures=$((failures + 1))
if ! grep -Fxq '#Top' "$evidence/stage3-prove-outer-state.log"; then
  printf '%s\n' 'missing_exact_top=1' >> "$evidence/stage3-prove-outer-state.log"
  failures=$((failures + 1))
else
  printf '%s\n' 'exact_top=1' >> "$evidence/stage3-prove-outer-state.log"
fi

run_bounded stage3-prove-outer-control \
  kprove spec.k \
    --definition audit-verification-inner-kompiled \
    --spec-module SPEC-OUTER ||
  failures=$((failures + 1))
if ! grep -Fxq '#Top' "$evidence/stage3-prove-outer-control.log"; then
  printf '%s\n' 'missing_exact_top=1' >> "$evidence/stage3-prove-outer-control.log"
  failures=$((failures + 1))
else
  printf '%s\n' 'exact_top=1' >> "$evidence/stage3-prove-outer-control.log"
fi

run_bounded stage3-build-verification \
  kompile --backend haskell verification.k \
    --main-module VERIFICATION \
    --syntax-module MPY-SYNTAX \
    --output-definition audit-verification-kompiled ||
  failures=$((failures + 1))

run_bounded stage3-prove-target \
  kprove spec.k \
    --definition audit-verification-kompiled \
    --spec-module SPEC ||
  failures=$((failures + 1))
if ! grep -Fxq '#Top' "$evidence/stage3-prove-target.log"; then
  printf '%s\n' 'missing_exact_top=1' >> "$evidence/stage3-prove-target.log"
  failures=$((failures + 1))
else
  printf '%s\n' 'exact_top=1' >> "$evidence/stage3-prove-target.log"
fi

printf 'reconstruction_failures=%s\n' "$failures"
if (( failures != 0 )); then
  printf '%s\n' 'stage3_script_exit=1'
  exit 1
fi
printf '%s\n' 'stage3_script_exit=0'
