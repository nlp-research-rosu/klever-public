#!/usr/bin/env bash
set -u

run_shell() {
  local command_text="$1"
  printf 'COMMAND: %s\n' "$command_text"
  bash -o pipefail -c "$command_text"
  local status=$?
  printf 'EXIT_STATUS: %s\n\n' "$status"
  return 0
}

run_shell "test ! -e /reference/reference-semantics"
run_shell "find /reference -maxdepth 2 -printf '%y %p\n' | sort"
run_shell "find /candidate -maxdepth 3 -printf '%y %p\n' | sort"
run_shell "find /candidate/codex-trace -printf '%y %p\n' | sort"
run_shell "find /candidate -type l -print"
run_shell "find /candidate -maxdepth 1 -type f -name '*.k' -printf '%f\n' | sort"
run_shell "stat -c '%F %n' /candidate/run-input.json /candidate/metrics.json /candidate/codex-last.txt /candidate/codex-output.log /candidate/prompt.py /candidate/py2mpy.py /candidate/solution.py /candidate/solution.mpy /candidate/semantic.k /candidate/spec.k /candidate/verification.k /candidate/prove.sh"
run_shell "sha256sum /candidate/prompt.py /reference/prompt.py /candidate/py2mpy.py /reference/py2mpy.py"
run_shell "cmp --silent /candidate/prompt.py /reference/prompt.py"
run_shell "cmp --silent /candidate/py2mpy.py /reference/py2mpy.py"
run_shell "python3 -m json.tool /candidate/run-input.json"
run_shell "python3 -m json.tool /candidate/metrics.json"
run_shell "sed -n '1,80p' /candidate/codex-last.txt"
run_shell "wc -lc /candidate/codex-output.log /candidate/codex-trace/2026/07/22/*.jsonl"
run_shell "rg -n 'kprove|#Top|WarnStuck|reference cross-check|RESULT:' /candidate/codex-output.log | tail -80"
run_shell "python3 /audit-output/evidence/stage1/trace_summary.py"
