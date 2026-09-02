# Reviewer command ledger

All source/build commands ran from `/tmp/audit-work/source` unless another
working directory is stated. `script --quiet --return --command CMD LOG`
captured each bounded transcript and its `COMMAND_EXIT_CODE`.

| Evidence | Exact inner command | Exit |
|---|---|---:|
| `00-toolchain.log` | `kompile --version && kprove --version && krun --version && python3 --version` | 0 |
| `01-provenance.log` (cwd `/audit-output`) | `python3 /audit-output/evidence/provenance_check.py` | 0 |
| `01-generation-record-summary.log` (cwd `/audit-output`) | `python3 /audit-output/evidence/generation_record_summary.py` | 0 |
| `02-translator-byte-identity.log` | `python3 /tmp/audit-work/reference/py2mpy.py /tmp/audit-work/source/solution.py \| cmp - /tmp/audit-work/source/solution.mpy` | 0 |
| `02-python-differential.log` (cwd `/audit-output`) | `python3 /audit-output/evidence/differential_test.py` | 0 |
| `03-kompile-concrete.log` | `kompile /tmp/audit-work/source/semantic.k --backend llvm --main-module SEMANTIC --syntax-module MPY-SYNTAX --output-definition /tmp/audit-work/build/semantic-kompiled` | 0 |
| `03-kompile-proof.log` | `kompile /tmp/audit-work/source/verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition /tmp/audit-work/build/verification-kompiled` | 0 |
| `03-positive-claims-list.log` | `rg -n "^  claim" /tmp/audit-work/source/spec.k` | 0 |
| `03-kprove-positive.log` | `kprove /tmp/audit-work/source/spec.k --definition /tmp/audit-work/build/verification-kompiled --spec-module SPEC` | 0, `#Top` |
| `03-krun-concrete.log` | `for s in '"xyzXYZ"' '"Jerry"' '""' '"AaBb!"' '"Ää"' '"Αα"'; do printf 'INPUT=%s\n' "$s"; krun /tmp/audit-work/source/solution.mpy --definition /tmp/audit-work/build/semantic-kompiled -cINPUT="$s"; done` | 0 |
| `04-program-term-identity-v2.log` | `bash -lc 'set -o pipefail; kast /tmp/audit-work/source/solution.mpy --definition /tmp/audit-work/build/verification-kompiled --input program --output json \| sha256sum; python3 /audit-output/evidence/extract_claim_program.py \| kast /dev/stdin --definition /tmp/audit-work/build/verification-kompiled --input program --output json \| sha256sum; cmp <(kast /tmp/audit-work/source/solution.mpy --definition /tmp/audit-work/build/verification-kompiled --input program --output json) <(python3 /audit-output/evidence/extract_claim_program.py \| kast /dev/stdin --definition /tmp/audit-work/build/verification-kompiled --input program --output json)'` | 0 |
| `04-body-sensitivity.log` | `kprove /audit-output/evidence/spec-body-mutation.k --definition /tmp/audit-work/build/verification-kompiled --spec-module SPEC-BODY-MUTATION` | 1, expected stuck claim |
| `05-unicode-false-conclusion-kprove-v2.log` | `kprove /audit-output/evidence/spec-unicode-witness.k --definition /tmp/audit-work/build/verification-kompiled --spec-module SPEC-UNICODE-WITNESS` | 0, `#Top` |
| `05-unicode-python-oracles.log` | `python3 -c 'from importlib.util import spec_from_file_location,module_from_spec; p=spec_from_file_location("c","/tmp/audit-work/reference/canonical.py"); c=module_from_spec(p); p.loader.exec_module(c); p=spec_from_file_location("s","/tmp/audit-work/source/solution.py"); s=module_from_spec(p); p.loader.exec_module(s); print("input=Ää canonical=",c.count_distinct_characters("Ää")," candidate_python=",s.count_distinct_characters("Ää"),sep="")'` | 0 |
| `06-false-postcondition.log` | `kprove /audit-output/evidence/spec-vacuity.k --definition /tmp/audit-work/build/verification-kompiled --spec-module SPEC-VACUITY` | 1, expected stuck claim |

Two retained diagnostic logs are not proof evidence:
`04-program-term-identity.log` exited 1 because `.Exprs` is K-claim notation,
not concrete `.mpy` notation; `extract_claim_program.py` performed the
documented unit normalization and the corrected comparison exited 0.
`05-unicode-false-conclusion-kprove.log` exited 113 because the first witness
used a relative `requires`; the corrected absolute source requirement built
and proved in the `-v2` log.
