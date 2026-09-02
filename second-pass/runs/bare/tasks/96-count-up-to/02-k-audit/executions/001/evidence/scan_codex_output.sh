#!/usr/bin/env bash
set -uo pipefail

log=/candidate/codex-output.log

printf 'file=%s bytes=%s lines=%s sha256=%s\n' \
  "$log" "$(stat -c %s "$log")" "$(wc -l < "$log")" \
  "$(sha256sum "$log" | cut -d' ' -f1)"

printf '\nStatus-bearing lines (untrusted)\n'
rg -n -i \
  'kprove|kompile|krun|#Top|WarnStuckClaimState|error|failed|succeeded|exit|differential|byte-for-byte|mismatch|RESULT:' \
  "$log"

printf '\nComplete-file line classification counts\n'
awk '
  { total += 1 }
  /^exec$/ { exec_markers += 1 }
  /succeeded in/ { succeeded += 1 }
  /exited [0-9]+/ { explicit_exits += 1 }
  /#Top/ { tops += 1 }
  /WarnStuckClaimState/ { stuck += 1 }
  /RESULT:/ { result_markers += 1 }
  END {
    printf "total_lines=%d\n", total
    printf "exec_markers=%d\n", exec_markers
    printf "succeeded_lines=%d\n", succeeded
    printf "explicit_exit_lines=%d\n", explicit_exits
    printf "top_lines=%d\n", tops
    printf "stuck_lines=%d\n", stuck
    printf "result_marker_lines=%d\n", result_markers
  }
' "$log"
