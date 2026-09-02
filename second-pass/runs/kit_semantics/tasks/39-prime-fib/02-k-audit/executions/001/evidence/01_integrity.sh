#!/usr/bin/env bash
set -eu
set -o pipefail

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  rc=$?
  printf '[exit %d]\n' "$rc"
  return "$rc"
}

echo "Declared layout and semantics mode"
run python3 -c 'import json; d=json.load(open("/audit-input.json")); print(d["record_layout"], d["semantics_mode"], d["problem_id"], d["condition"], sep="\n")'

echo "Campaign lock must equal the campaign block"
run python3 -c 'import json; a=json.load(open("/audit-input.json"))["audit_campaign"]; b=json.load(open("/audit-campaign-lock.json")); assert a == b; print("MATCH")'

echo "Required pipeline-v3 records and trusted mounts must be regular readable files/directories"
required_paths=(
  /audit-input.json
  /audit-campaign-lock.json
  /candidate
  /reference/canonical.py
  /reference/prompt.py
  /reference/py2mpy.py
  /reference/reference-semantics
  /run.json
  /task.json
  /generation-result.json
  /generation-evidence/invocation.json
  /generation-evidence/metrics.json
  /generation-evidence/runtime-metrics.json
  /generation-evidence/usage.json
  /generation-evidence/codex-last.txt
  /generation-evidence/codex-output.log
  /generation-evidence/prompt.txt
  /generation-evidence/codex-trace
)
for path in "${required_paths[@]}"; do
  if [[ -r "$path" && ! -L "$path" && ( -f "$path" || -d "$path" ) ]]; then
    stat -c 'OK %F %A %s %n' "$path"
  else
    stat -c 'BAD %F %A %s %n' "$path" 2>&1 || true
  fi
done

echo "No symlinks or non-regular entries in source/provenance trees"
printf '$ find /candidate /reference /generation-evidence -type l -print\n'
symlinks="$(find /candidate /reference /generation-evidence -type l -print)"
printf '%s' "$symlinks"
test -z "$symlinks"
printf '[exit %d]\n' "$?"
printf '$ find /candidate/reference-semantics /reference/reference-semantics -not -type d -not -type f -printf %%y\\ %%p\\\\n\n'
specials="$(find /candidate/reference-semantics /reference/reference-semantics -not -type d -not -type f -printf '%y %p\n')"
printf '%s' "$specials"
test -z "$specials"
printf '[exit %d]\n' "$?"

echo "Recorded direct hashes"
hash_checks=(
  'ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745  /audit-campaign-lock.json'
  '50b253880fb3cd8cb47012ef1084eb96307d76e235bc1fbefad3262e1092f9cd  /reference/canonical.py'
  '6dde5c311a83caad26ca80e7e914c596b9cb6e8467630530600e21c98d547c5a  /reference/prompt.py'
  '406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16  /reference/py2mpy.py'
  '6dde5c311a83caad26ca80e7e914c596b9cb6e8467630530600e21c98d547c5a  /candidate/prompt.py'
  '406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16  /candidate/py2mpy.py'
  '3b99df09203880c9a59a6dcfed87c41b60e6057ebf8720421e156f1e7517bd73  /run.json'
  '44eea73ad7ce55339268b5ceb288bae33dd9c5dd35d4cf9b947d45abe42eb495  /task.json'
  '57d76b81ca44856eb457ae94ee5f6bb36c8a3624d99d8efbd6e1b75eb177ab08  /generation-result.json'
  '29584eabe2e322f7361b08b970f25afbf4420a4316288e79661ff96d191f16cd  /generation-evidence/invocation.json'
  'a2ec55e4a065bbf18d99e536e482394759bb5a4fc3e6313e51368765ed011b0d  /generation-evidence/metrics.json'
  '52cd40d55b13ae9dab0202fc9e60d034280e23f3db72779eecc5edbf87efeef8  /generation-evidence/runtime-metrics.json'
  '326a95050ae6a507e867993598077aa5d9089bd579cacaf3c654ea771d5eca1b  /generation-evidence/usage.json'
  'fa9afe583b5584d6ab9280241bcd01c7c117a4dced02308677f2ea45035d6b39  /generation-evidence/codex-last.txt'
  'b07c42c8d7449beb415254599bb29854c06c4135228446ad47f08ae853cabcd9  /generation-evidence/codex-output.log'
  'c5f7af5f994f1d98d2cb3ab967f88f74a437a6548277cceaf24481aba1cf31e5  /generation-evidence/prompt.txt'
)
for check in "${hash_checks[@]}"; do
  printf '%s\n' "$check" | sha256sum -c -
  printf '[exit %d]\n' "$?"
done

echo "Candidate prompt and translator byte-compare with trusted mounts"
run cmp -s /candidate/prompt.py /reference/prompt.py
run cmp -s /candidate/py2mpy.py /reference/py2mpy.py

echo "SUPPLIED_SEMANTICS recursive integrity comparison"
run diff -r --no-dereference /candidate/reference-semantics /reference/reference-semantics
printf '$ (cd /reference/reference-semantics && find . -type f -print0 | sort -z | xargs -0 sha256sum) | sha256sum\n'
(cd /reference/reference-semantics && find . -type f -print0 | sort -z | xargs -0 sha256sum) | sha256sum
printf '[exit %d]\n' "${PIPESTATUS[0]}"
printf '$ (cd /candidate/reference-semantics && find . -type f -print0 | sort -z | xargs -0 sha256sum) | sha256sum\n'
(cd /candidate/reference-semantics && find . -type f -print0 | sort -z | xargs -0 sha256sum) | sha256sum
printf '[exit %d]\n' "${PIPESTATUS[0]}"

echo "Structured trace inventory and JSONL validity"
run find /generation-evidence/codex-trace -type f -printf '%P %s bytes\n'
run python3 -c 'import json; p="/generation-evidence/codex-trace/2026/07/25/rollout-2026-07-25T00-04-10-019f97a8-cf37-7dd3-8884-fef0cf5c5bbc.jsonl"; n=0; [json.loads(line) for line in open(p) if (n := n + 1)]; print(f"valid JSONL: {n} records")'
run sha256sum /generation-evidence/codex-trace/2026/07/25/rollout-2026-07-25T00-04-10-019f97a8-cf37-7dd3-8884-fef0cf5c5bbc.jsonl

echo "Pipeline-v3 canonical tree hashes"
run env PYTHONPATH=/opt/humaneval/tools python3 -c 'from pathlib import Path; from pipeline_contract import sha256_tree; expected={"/candidate":"a0bd2a6606735c8bd4df4a4e0f4c9736b4fc09e4f69d2bb267e33eb9408672c6","/candidate/reference-semantics":"4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f","/reference/reference-semantics":"4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f","/generation-evidence/codex-trace":"32ace908740763406d4220502d135a61dcb8f68b450752617f10bfa53911e927"}; [(print(sha256_tree(Path(p)),p), (_ for _ in ()).throw(AssertionError(p)) if sha256_tree(Path(p)) != h else None) for p,h in expected.items()]'
