#!/usr/bin/env bash
set -u

echo 'COMMAND: bash /audit-output/evidence/01_integrity.sh'
echo
echo '== Tool and mount readability =='
for path in \
  /audit-input.json \
  /audit-campaign-lock.json \
  /run.json \
  /task.json \
  /generation-result.json \
  /generation-evidence/invocation.json \
  /generation-evidence/metrics.json \
  /generation-evidence/runtime-metrics.json \
  /generation-evidence/usage.json \
  /generation-evidence/codex-last.txt \
  /generation-evidence/codex-output.log \
  /generation-evidence/prompt.txt \
  /generation-evidence/codex-trace \
  /candidate \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /reference/reference-semantics
do
  if test -r "$path"; then
    stat -c 'READABLE type=%F mode=%A path=%n' "$path"
  else
    echo "UNREADABLE path=$path"
  fi
done

echo
echo '== Required record and trusted-input SHA-256 values =='
sha256sum \
  /audit-campaign-lock.json \
  /run.json \
  /task.json \
  /generation-result.json \
  /generation-evidence/invocation.json \
  /generation-evidence/metrics.json \
  /generation-evidence/runtime-metrics.json \
  /generation-evidence/usage.json \
  /generation-evidence/codex-last.txt \
  /generation-evidence/codex-output.log \
  /generation-evidence/prompt.txt \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /candidate/prompt.py \
  /candidate/py2mpy.py
find /generation-evidence/codex-trace -type f -print0 |
  sort -z |
  xargs -0 sha256sum

echo
echo '== Recorded pipeline-v3 hash checks =='
check_hash() {
  expected="$1"
  file="$2"
  actual="$(sha256sum "$file" | cut -d' ' -f1)"
  if test "$actual" = "$expected"; then
    echo "HASH_OK $file $actual"
  else
    echo "HASH_MISMATCH $file expected=$expected actual=$actual"
  fi
}
check_hash ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745 /audit-campaign-lock.json
check_hash 3b99df09203880c9a59a6dcfed87c41b60e6057ebf8720421e156f1e7517bd73 /run.json
check_hash f8c9c3000c759f23078337e7e7c291bc1573546639ddc4550d1de55010c6657f /task.json
check_hash 4f90821c5eeb9775d35984a7bb08c4f3c0a52553f4b438e48302eba2c6beed16 /generation-result.json
check_hash 1c45431f02a790d145178aaed82741f5e7b047d50e10e45799296451f80326e5 /generation-evidence/invocation.json
check_hash 80fe369e04f10786e03741cafed07b051cb6a3111f476dde65028bcf3dec41c0 /generation-evidence/metrics.json
check_hash 2b987b82dfd4cb88929de942836733386d4516d8a2cffbdd3adc881d4462a5ea /generation-evidence/runtime-metrics.json
check_hash 0a6376bae40ac40b042d7fb8201e5d1efe31597fbc8fade94a354328e0e850e9 /generation-evidence/usage.json
check_hash 4b3ff0828b35e6a8924a05ba32b3481070d59e7a7da39508072712a2959cf8e5 /generation-evidence/codex-last.txt
check_hash 12440b5d02083139e3a0395396b0374217fa5a337c61f190b85094b98ba2bddf /generation-evidence/codex-output.log
check_hash c5f7af5f994f1d98d2cb3ab967f88f74a437a6548277cceaf24481aba1cf31e5 /generation-evidence/prompt.txt
check_hash 432b4a3a308e4f8147cc8a894ab4440c0807c0978646541933f77accd1bdba04 /generation-evidence/codex-trace/2026/07/24/rollout-2026-07-24T23-46-28-019f9798-992f-7472-abd1-9a38db7606fd.jsonl
check_hash fc85f43ca1c5626c69f0d5910740e8be8ec7483a0965e73a8a5da74f159c9f49 /reference/canonical.py
check_hash a173ce6b1e3767cabcf0ff73457d20e4eac07e0968b173b76afa0b35c0799646 /reference/prompt.py
check_hash 406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16 /reference/py2mpy.py
check_hash a173ce6b1e3767cabcf0ff73457d20e4eac07e0968b173b76afa0b35c0799646 /candidate/prompt.py
check_hash 406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16 /candidate/py2mpy.py

echo
echo '== Campaign lock exact structured comparison =='
python3 - <<'PY'
import json
with open('/audit-input.json', encoding='utf-8') as f:
    audit_input = json.load(f)
with open('/audit-campaign-lock.json', encoding='utf-8') as f:
    lock = json.load(f)
print('CAMPAIGN_BLOCK_MATCH', audit_input['audit_campaign'] == lock)
PY

echo
echo '== Candidate prompt and translator byte comparisons =='
cmp -s /candidate/prompt.py /reference/prompt.py
echo "prompt_cmp_exit=$?"
cmp -s /candidate/py2mpy.py /reference/py2mpy.py
echo "translator_cmp_exit=$?"

echo
echo '== Candidate/trusted supplied-semantics recursive integrity =='
find /candidate/reference-semantics /reference/reference-semantics -type l -printf 'SYMLINK %p -> %l\n'
candidate_list="$(mktemp)"
trusted_list="$(mktemp)"
(
  cd /candidate/reference-semantics
  find . -printf '%P\t%y\n' | sort
) > "$candidate_list"
(
  cd /reference/reference-semantics
  find . -printf '%P\t%y\n' | sort
) > "$trusted_list"
diff -u "$trusted_list" "$candidate_list"
echo "semantics_entry_type_diff_exit=$?"

semantics_fail=0
while IFS= read -r -d '' trusted; do
  rel="${trusted#/reference/reference-semantics/}"
  candidate="/candidate/reference-semantics/$rel"
  if ! test -f "$candidate"; then
    echo "SEMANTICS_MISSING_OR_MISTYPED $rel"
    semantics_fail=1
  elif ! cmp -s "$trusted" "$candidate"; then
    echo "SEMANTICS_CONTENT_MISMATCH $rel"
    semantics_fail=1
  else
    echo "SEMANTICS_FILE_OK $rel $(sha256sum "$trusted" | cut -d' ' -f1)"
  fi
done < <(find /reference/reference-semantics -type f -print0 | sort -z)
echo "semantics_recursive_compare_fail=$semantics_fail"

echo
echo '== Symlink scan of all mounted audit inputs =='
find \
  /candidate \
  /reference \
  /generation-evidence \
  /audit-input.json \
  /audit-campaign-lock.json \
  /run.json \
  /task.json \
  /generation-result.json \
  -type l -printf 'SYMLINK %p -> %l\n'

echo
echo 'SCRIPT_EXIT: 0'
