#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy

python3 -m py_compile solution.py concrete_tests.py
python3 - <<'PY'
import ast
from pathlib import Path

solution = ast.parse(Path("solution.py").read_text())
tests = ast.parse(Path("concrete_tests.py").read_text())
assert ast.dump(solution) == ast.dump(ast.Module(body=tests.body[:2], type_ignores=[]))
PY

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun concrete_tests.mpy \
  --definition runtime-kompiled \
  --output pretty \
  | tee concrete_tests.out

python3 - <<'PY'
from pathlib import Path

out = Path("concrete_tests.out").read_text()
assert "<k>\n    .K\n  </k>" in out
assert "<exc>\n    NoExc\n  </exc>" in out
assert "<exit-code>\n    0\n  </exit-code>" in out
PY

kompile verification.k \
  --backend haskell \
  --main-module STRONGEST-EXTENSION-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled \
  -I .

kprove spec.k \
  --definition verification-kompiled \
  --spec-module STRONGEST-EXTENSION-SPEC \
  --claims character-loop-correct \
  --output pretty \
  | tee proof-character-loop.out
rg -x '#Top' proof-character-loop.out

kompile verification.k \
  --backend haskell \
  --main-module STRONGEST-EXTENSION-WITH-CHAR-LOOP-LEMMA \
  --syntax-module MPY-SYNTAX \
  --output-definition char-loop-lemma-kompiled \
  -I .

kprove spec.k \
  --definition char-loop-lemma-kompiled \
  --spec-module STRONGEST-EXTENSION-SPEC \
  --claims extension-strength-correct \
  --output pretty \
  | tee proof-extension-strength.out
rg -x '#Top' proof-extension-strength.out

kompile verification.k \
  --backend haskell \
  --main-module STRONGEST-EXTENSION-WITH-STRENGTH-LEMMA \
  --syntax-module MPY-SYNTAX \
  --output-definition strength-lemma-kompiled \
  -I .

kprove spec.k \
  --definition strength-lemma-kompiled \
  --spec-module STRONGEST-EXTENSION-SPEC \
  --claims selection-loop-correct \
  --output pretty \
  | tee proof-selection-loop.out
rg -x '#Top' proof-selection-loop.out

kompile verification.k \
  --backend haskell \
  --main-module STRONGEST-EXTENSION-WITH-LOOP-LEMMAS \
  --syntax-module MPY-SYNTAX \
  --output-definition loop-lemmas-kompiled \
  -I .

kprove spec.k \
  --definition loop-lemmas-kompiled \
  --spec-module STRONGEST-EXTENSION-SPEC \
  --claims strongest-extension-correct \
  --output pretty \
  | tee proof-strongest-extension.out
rg -x '#Top' proof-strongest-extension.out
