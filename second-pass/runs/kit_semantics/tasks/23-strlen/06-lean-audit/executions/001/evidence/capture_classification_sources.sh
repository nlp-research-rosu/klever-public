#!/bin/sh
set -eu

nl -ba /reference/k-proof/verification.k
nl -ba /reference/k-proof/solution.py
nl -ba /reference/k-proof/spec.k
rg -n -C 3 \
  'builtinsScope|applyBuiltin\("len"|seqLen\(str|syntax Int ::= isLen|rule isLen|#applyK\(toCall\(builtinV\(BN' \
  /reference/k-proof/reference-semantics/semantics/core.k \
  /reference/k-proof/reference-semantics/semantics/builtins.k \
  /reference/k-proof/reference-semantics/semantics/call.k
python -m json.tool /reference/lemma-discovery.json
python -m json.tool /reference/klean-generation/input-manifest.json
python -m json.tool /reference/klean-generation/generator-manifest.json
python -m json.tool /reference/klean-generation/generated/obligation-map.json
python -m json.tool /reference/klean-generation/export-result.json
python -m json.tool /reference/generation-tools/source-manifest.json
sha256sum \
  /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py \
  /reference/generation-tools/source-manifest.json \
  /reference/lemma-discovery.json \
  /reference/k-proof/verification.k \
  /reference/klean-generation/generated/obligation-map.json
PYTHONPATH=/reference python -c \
  'import json; from pathlib import Path; from tools.k_rule_inventory import inventory_verification; print(json.dumps(inventory_verification(Path("/reference/k-proof")), indent=2, sort_keys=True))'
PYTHONPATH=/reference python -c \
  'import json; from pathlib import Path; from tools.lemma_discovery_contract import validate_trust_boundary; print(json.dumps(validate_trust_boundary(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json")), indent=2, sort_keys=True))'
