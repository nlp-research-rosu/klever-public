#!/usr/bin/env bash
set -u

python3 /audit-output/evidence/01_provenance.py
python_status=$?
printf 'python_provenance_exit=%s\n' "$python_status"

cmp -s /candidate/prompt.py /reference/prompt.py
printf 'candidate_prompt_cmp_exit=%s\n' "$?"
cmp -s /candidate/py2mpy.py /reference/py2mpy.py
printf 'candidate_translator_cmp_exit=%s\n' "$?"

diff -qr --no-dereference /candidate/reference-semantics /reference/reference-semantics
printf 'reference_semantics_recursive_diff_exit=%s\n' "$?"

find /candidate/reference-semantics -type l -print
printf 'candidate_reference_semantics_symlink_scan_exit=%s\n' "$?"
find /candidate/reference-semantics -mindepth 1 ! -type f ! -type d -print
printf 'candidate_reference_semantics_special_scan_exit=%s\n' "$?"

file /generation-evidence/codex-output.log
wc -l -c /generation-evidence/codex-output.log
sed -n '1,20p' /generation-evidence/codex-output.log
tail -n 30 /generation-evidence/codex-output.log
rg -n -i 'error|warning|#top|result:|blocked|partial|validated|sound-but-limited|formally-sound' /generation-evidence/codex-output.log | tail -n 160
printf 'generation_output_scan_exit=%s\n' "$?"

exit "$python_status"
