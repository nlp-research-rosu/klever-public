#!/usr/bin/env bash
set -euo pipefail
set -x

export PATH="$HOME/.nix-profile/bin:$PATH"
export PYTHONDONTWRITEBYTECODE=1
cd /tmp/audit-work/35-max-element

python3 - <<'PY'
import ast
import importlib.util

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.max_element

prompt_tree = ast.parse(open("/reference/prompt.py", encoding="utf-8").read())
function = next(node for node in prompt_tree.body if isinstance(node, ast.FunctionDef))
print(f"PROMPT_PARAMETER_ANNOTATION={ast.unparse(function.args.args[0].annotation)}")
print(f"PROMPT_RETURN_ANNOTATION={function.returns}")

canonical = load("domain_canonical", "/reference/canonical.py")
candidate = load("domain_candidate", "/tmp/audit-work/35-max-element/solution.py")
for witness in ([1.5, -2.0, 1.5001], ["alpha", "zeta", "mu"]):
    print(f"SOURCE_DOMAIN_WITNESS={witness!r}")
    print(f"CANONICAL_RESULT={canonical(list(witness))!r}")
    print(f"CANDIDATE_RESULT={candidate(list(witness))!r}")
PY

set +e
krun solution.mpy \
  --definition audit-semantic-kompiled \
  --color off \
  -cARGS='[1.5, -2.0, 1.5001]' \
  > /audit-output/evidence/stage7-float-domain.raw.log 2>&1
float_domain_status=$?
krun solution.mpy \
  --definition audit-semantic-kompiled \
  --color off \
  -cARGS='["alpha", "zeta", "mu"]' \
  > /audit-output/evidence/stage7-string-domain.raw.log 2>&1
string_domain_status=$?
set -e

echo "FLOAT_DOMAIN_KRUN_EXIT=$float_domain_status"
sed -n '1,100p' /audit-output/evidence/stage7-float-domain.raw.log
echo "STRING_DOMAIN_KRUN_EXIT=$string_domain_status"
sed -n '1,100p' /audit-output/evidence/stage7-string-domain.raw.log
test "$float_domain_status" -ne 0
test "$string_domain_status" -ne 0
