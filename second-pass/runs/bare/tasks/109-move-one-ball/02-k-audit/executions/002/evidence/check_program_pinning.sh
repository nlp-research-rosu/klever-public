#!/usr/bin/env bash
set -euo pipefail

workdir=${1:?scratch source directory required}
definition=${2:?compiled definition required}

cd "$workdir"

rule_text=$(
  awk '
    /rule theSolution =>/ { capture=1; sub(/^[[:space:]]*rule[[:space:]]*/, ""); print; next }
    capture && /^[[:space:]]*endmodule/ { exit }
    capture { print }
  ' mpy-syntax.k
)

printf '%s\n' 'EXTRACTED RULE:'
printf '%s\n' "$rule_text"
printf '%s\n' 'COMMAND: kast solution.mpy --output json'
kast solution.mpy \
  --definition "$definition" \
  --module HUMAN-EVAL-SYNTAX \
  --sort Pgm \
  --output json > program-source.json
printf '%s\n' 'COMMAND: kast extracted-theSolution-rule --input rule --output json'
kast \
  --definition "$definition" \
  --module HUMAN-EVAL-SYNTAX \
  --input rule \
  --output json \
  --expression "$rule_text" > program-rule.json

python3 - program-source.json program-rule.json <<'PY'
import hashlib
import json
import sys

source_doc = json.load(open(sys.argv[1], encoding="utf-8"))
rule_doc = json.load(open(sys.argv[2], encoding="utf-8"))
source_term = source_doc["term"]
rule_term = rule_doc["term"]
assert rule_term["node"] == "KRewrite", rule_term["node"]
rule_rhs = rule_term["rhs"]

def digest(value):
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()

print("source_constructor_sha256=", digest(source_term))
print("theSolution_rhs_constructor_sha256=", digest(rule_rhs))
print("constructor_terms_equal=", source_term == rule_rhs)
raise SystemExit(0 if source_term == rule_rhs else 1)
PY
