#!/usr/bin/env bash
# Fail before a benchmark stage can use a mixed Codex/K/Klean/Lean runtime.
set -euo pipefail

MODE="${1:-}"
EXPECTED_CODEX="codex-cli 0.144.6"
EXPECTED_K="v7.1.293"
EXPECTED_K_COMMIT="ff15baac9e66426612ec45ff912af7f14965b64a"
EXPECTED_PYK="7.1.293"
EXPECTED_LEAN="4.22.0"
EXPECTED_LEAN_COMMIT="ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05"
K_SOURCE_COMMIT="/opt/runtimeverification-k/.source-commit"

fail() {
  printf 'frozen toolchain mismatch: %s\n' "$*" >&2
  exit 70
}

[[ "$MODE" == "agent" || "$MODE" == "klean" ]] \
  || fail "mode must be agent or klean"

ACTUAL_K=""
for command in kompile kprove krun; do
  actual="$("$command" --version 2>/dev/null \
    | sed -n 's/^K version:[[:space:]]*//p' \
    | head -n 1)"
  [[ "$actual" == "$EXPECTED_K" ]] \
    || fail "$command is ${actual:-missing}; expected $EXPECTED_K"
  ACTUAL_K="$actual"
done

[[ -f "$K_SOURCE_COMMIT" && ! -L "$K_SOURCE_COMMIT" ]] \
  || fail "Klean source commit marker is missing"
ACTUAL_K_COMMIT="$(<"$K_SOURCE_COMMIT")"
[[ "$ACTUAL_K_COMMIT" == "$EXPECTED_K_COMMIT" ]] \
  || fail "Klean source is ${ACTUAL_K_COMMIT:-missing}; expected $EXPECTED_K_COMMIT"

ACTUAL_PYK="$(python3 - <<'PY'
from importlib.metadata import version
print(version("kframework"))
PY
)" || fail "cannot read the installed pyk/Klean version"
[[ "$ACTUAL_PYK" == "$EXPECTED_PYK" ]] \
  || fail "pyk/Klean is ${ACTUAL_PYK:-missing}; expected $EXPECTED_PYK"
python3 -c 'import pyk.klean' >/dev/null 2>&1 \
  || fail "pyk.klean cannot be imported"

ACTUAL_LEAN_OUTPUT="$(lean --version 2>/dev/null)" || fail "Lean is unavailable"
[[ "$ACTUAL_LEAN_OUTPUT" == *"version $EXPECTED_LEAN,"* ]] \
  || fail "Lean version differs from $EXPECTED_LEAN: $ACTUAL_LEAN_OUTPUT"
[[ "$ACTUAL_LEAN_OUTPUT" == *"commit $EXPECTED_LEAN_COMMIT,"* ]] \
  || fail "Lean commit differs from $EXPECTED_LEAN_COMMIT: $ACTUAL_LEAN_OUTPUT"
ACTUAL_LEAN="$(
  printf '%s\n' "$ACTUAL_LEAN_OUTPUT" \
    | sed -n 's/.*version \([^,]*\),.*/\1/p'
)"
[[ -n "$ACTUAL_LEAN" ]] || fail "cannot parse Lean version: $ACTUAL_LEAN_OUTPUT"
command -v lake >/dev/null 2>&1 || fail "Lake is unavailable"

if [[ "$MODE" == "agent" ]]; then
  ACTUAL_CODEX="$(codex --version 2>/dev/null)" || fail "Codex is unavailable"
  [[ "$ACTUAL_CODEX" == "$EXPECTED_CODEX" ]] \
    || fail "Codex is ${ACTUAL_CODEX:-missing}; expected $EXPECTED_CODEX"
fi

printf 'frozen toolchain OK: K %s, pyk/Klean %s, Lean %s' \
  "${ACTUAL_K#v}" "$ACTUAL_PYK" "$ACTUAL_LEAN"
if [[ "$MODE" == "agent" ]]; then
  printf ', Codex %s' "${ACTUAL_CODEX#codex-cli }"
fi
printf '\n'
