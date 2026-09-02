# Independent adversarial review: 99-closest-integer

## Executive decision

The candidate contains a legitimate, result-constraining partial-correctness
proof of the submitted translated program under the supplied semantics. Fresh
reconstruction closes all four unbounded claims, the claim body is
constructor-identical to the trusted regeneration, and independent false-result
and body mutations are rejected for the expected obligations.

The result is not an unqualified `PASS`. The Haskell proof is
interpretation-parametric in seven result-bearing supplied float primitives,
and the supplied decimal parser cannot represent every spelling accepted by
CPython. The candidate documents that fixed-model gap and gives the concrete
`"1e2"` divergence; this audit independently reproduced K/model result 632
versus submitted CPython result 100. The theorem covers every `IntSeq` the fixed
model represents without a candidate-added restriction, and the submitted
Python is faithful on the gap. Campaign amendment v2 exception 1 therefore
requires `CONCERNS / LEGIT`, not `FAIL / NOT_LEGIT`.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout: pipeline-v3`,
`semantics_mode: SUPPLIED_SEMANTICS`, and the expected
`kit-semantics`/`99-closest-integer` task. The supplied semantics mount exists,
so the rendered mode and trusted mounts do not conflict.

I read and inspected:

- `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
  `/task.json`, and `/generation-result.json`;
- all required pipeline-v3 records in `/generation-evidence`, including
  `invocation.json`, `metrics.json`, `runtime-metrics.json`, `usage.json`,
  `codex-last.txt`, `codex-output.log`, and `prompt.txt`;
- the complete structured trace. It contains 241 valid JSONL records, zero
  malformed records, and matching declared hash
  `1f6030e71abaffa491a53ad5bb4020bc750ca36f2eab043ed690c9c20e0d7cbc`.

The generation records were treated only as untrusted claims. The trace
inventory and all 43 recorded tool calls are summarized in
`evidence/stage1/trace-summary.log`.

Independent integrity results are in
`evidence/stage1/integrity-v2.{cmd,log,status}`:

- the campaign object equals the embedded `/audit-input.json` campaign block;
- the lock SHA-256 is
  `053ed73cba6d14969a1268433f910c65d5a2c1f365fd324fb469fa1e51dadd01`,
  exactly the declared value;
- every required record and provenance mount is readable and has the expected
  regular-file/directory type;
- every declared per-file hash checked by the script matches;
- candidate `prompt.py` and `py2mpy.py` are byte-identical to the trusted
  mounts;
- recursive path/type/content comparison of
  `/candidate/reference-semantics` and
  `/reference/reference-semantics` reports zero differences;
- there are no symlinks in the candidate, trusted reference, or generation
  evidence trees.

The required candidate source artifacts are present. Candidate
`runtime-kompiled` and `verification-kompiled` were ignored. All executable
source was copied to `/tmp/audit-work`, and every definition below was rebuilt
there.

An initial reviewer integrity script run failed on an auditor-authored
`Path.lexists` typo; the corrected script is the `integrity-v2` run above. This
was not an input or candidate failure.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The trusted docstring requires `closest_integer(value: str)` to return the
closest integer to the represented number, choosing the farther-from-zero
integer on exact ties. It fixes examples `"10" -> 10`, `"15.3" -> 15`,
`"14.5" -> 15`, and `"-14.5" -> -15`. It does not specify invalid strings,
NaN/infinity, errors, or how arbitrarily fine decimal spellings should interact
with CPython binary-float conversion.

The submitted program parses with CPython `float`, computes `floor` and `ceil`,
chooses the nearer endpoint with strict `< 0.5` tests, and chooses `ceil` for
positive ties and `floor` for nonpositive ties. This satisfies the determined
docstring behavior for finite parsed numbers.

### Trusted regeneration

The exact command is recorded in
`evidence/stage2/translation.{cmd,log,status}`. It runs:

```text
python3 /reference/py2mpy.py /candidate/solution.py > /tmp/audit-work/regenerated-solution.mpy
cmp -s /tmp/audit-work/regenerated-solution.mpy /candidate/solution.mpy
```

Exit status is 0. Both files have SHA-256
`bc37bac6c33fc5c8a66542f92622a83aeefdbd1d243ff4243d094930dc92ca3b`.

### Independent differential

`evidence/stage2/independent_differential.py` independently imports the trusted
canonical entry point and submitted entry point. Its complete 1,284 inputs are
preserved in `differential-inputs.json`, results in
`differential-results.json`, and command/output/status in
`differential.{cmd,log,status}`.

Coverage includes all examples, zero and signed zero, both sign branches,
values below/at/above every half boundary, alternate number spellings,
scientific notation, whitespace, binary-representation boundaries, large and
subnormal values, invalid/non-finite observations, an exhaustive small grid,
and 750 seeded six-decimal random inputs.

Results:

- documented-example failures: 0;
- ordinary generated exact-decimal mismatches: 0 across 1,236 cases;
- candidate-versus-canonical mismatches: 9;
- candidate-versus-exact-Decimal mismatches: 8, all deliberately selected
  numeric-representation boundaries;
- script exit status: 0.

Five canonical mismatches are evidence for the candidate, not against it:
`"145e-1"`, `"-145e-1"`, `"1.45e1"`, `"-1.45e1"`, and `" 14.5 "`.
They denote exact ties; the candidate returns away from zero while canonical
uses banker's `round` because the spelling does not end in `.5`. The docstring,
not canonical equality, controls.

The remaining mismatches concern values such as
`"0.49999999999999999"` and `"9007199254740992.5"` whose exact decimal value
and CPython binary float differ at a rounding boundary. Campaign amendment v3
expressly treats numeric-representation subtleties as underdetermined. The
candidate consistently rounds the CPython parsed float, a defensible reading.
No mismatch demonstrates a violation of docstring-determined behavior.

## 3. Clean proof reconstruction

The live toolchain is K v7.1.293. Exact version/help output is in
`evidence/stage3/toolchain.log`.

### Fresh concrete definition and execution

The trusted semantics was freshly compiled:

```text
kompile /tmp/audit-work/reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/auditor-runtime-kompiled
```

`evidence/stage3/kompile-llvm.status` is 0. The independent 15-assert program
`/tmp/audit-work/auditor_concrete_probe.py` was translated with the trusted
translator and run using:

```text
krun /tmp/audit-work/auditor_concrete_probe.mpy \
  --definition /tmp/audit-work/auditor-runtime-kompiled
```

`evidence/stage3/krun-concrete.status` is 0. The final configuration contains
`.K`, `NoExc`, exit code 0, empty heap/stack, and the expected exact translated
closure.

### Fresh proof definition and all positive targets

The Haskell definition was freshly built:

```text
kompile /tmp/audit-work/verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/auditor-verification-kompiled
```

`evidence/stage3/kompile-haskell.status` is 0. The complete target command:

```text
kprove /tmp/audit-work/spec.k \
  --definition /tmp/audit-work/auditor-verification-kompiled \
  --spec-module SPEC
```

prints `#Top` and exits 0
(`evidence/stage3/kprove-all.{cmd,log,status}`). Each claim was also selected
and run independently with its full CLI label:

| Claim | Evidence | Result |
|---|---|---|
| `SPEC.closest-positive-lower` | `stage3/kprove-positive-lower.*` | `#Top`, 0 |
| `SPEC.closest-positive-upper` | `stage3/kprove-positive-upper.*` | `#Top`, 0 |
| `SPEC.closest-nonpositive-upper` | `stage3/kprove-nonpositive-upper.*` | `#Top`, 0 |
| `SPEC.closest-nonpositive-lower` | `stage3/kprove-nonpositive-lower-rerun.*` | `#Top`, 0 |

One earlier concurrent four-prover launch caused the last backend process to be
killed (`stage3/kprove-nonpositive-lower.status` 113, reporting backend code
137). The all-claims proof had already succeeded, and the same selected claim
immediately closed alone. This is a reviewer parallel-resource artifact, not a
candidate or infrastructure verdict.

## 4. Adequacy and real-program pinning

The four claims state:

| Claim | Plain precondition | Postcondition |
|---|---|---|
| positive-lower | parsed value positive; distance to floor strictly below 0.5 | return floor |
| positive-upper | parsed value positive; distance to floor at least 0.5 | return ceil |
| nonpositive-upper | parsed value nonpositive; distance from ceil strictly below 0.5 | return ceil |
| nonpositive-lower | parsed value nonpositive; distance from ceil at least 0.5 | return floor |

There is no RHS-only/free result variable, implication-only weakening, helper
claim, or tautology. Each claim consumes the call and constrains the returned
integer plus every modeled state cell.

`evidence/stage4/pinning_and_witnesses.py` performs a mechanical balanced-term
comparison. After only removing whitespace and the explicit/implicit
`.Stmts` list unit, the trusted-regenerated `FuncDef` body and all four
`closureVal` bodies have the same SHA-256:

```text
5c8f3421af7bcaba8fb081cd1366da9aa52061f26a90b374a3becccb46812877
```

It also verifies four exact entry calls and four copies of every pinned
environment, scope allocator, heap, heap allocator, stack, return, exception,
and exit-code cell. The claim begins at the function-call boundary rather than
module load. This is valid under the fixed semantics: `Import("math")` is a
fixed no-op, module loading creates precisely this closure, and the fixed
`math.floor`/`math.ceil` intercepts execute every material expression and
control effect in the body.

Concrete satisfying witnesses and substitutions, preserved in
`evidence/stage4/pinning-witnesses.log`, are:

| Claim | Witness | Substituted result | Candidate | Canonical |
|---|---:|---:|---:|---:|
| positive-lower | `"15.3"` | 15 | 15 | 15 |
| positive-upper | `"14.5"` | 15 | 15 | 15 |
| nonpositive-upper | `"-14.3"` | -14 | -14 | -14 |
| nonpositive-lower | `"-14.5"` | -15 | -15 | -15 |

The guards are two Boolean choices and their negations. Because the fixed
symbols are typed total Boolean functions, the four claims cover every
symbolic `CS:IntSeq`; there is no fixed length, finite list of inputs, bounded
unrolling, or candidate-added well-formedness narrowing.

## 5. Rule-by-rule static soundness review

The exhaustive source-derived inventory is
`evidence/stage5/rule-inventory.log`, produced by the preserved
`inventory_k.py`. It covers every supplied K file, `verification.k`, and
`spec.k`:

```text
syntax declarations: 244
configuration declarations: 1
contexts: 5
rules: 764
claims: 4
simplification rules: 0
```

The complete module-by-module disposition and exact candidate execution map
are in `evidence/stage5/used_path_and_module_review.md`. Important findings:

- `verification.k` imports fixed `MPY` and adds no syntax, function,
  totality/functional declaration, opaque symbol, priority, ordinary rule, or
  simplification;
- `spec.k` adds only the four reachability claims;
- every submitted constructor maps to fixed syntax and an execution rule;
- lookup, callee-before-argument evaluation, positional binding, assignments,
  nested branches, abrupt return, frame pop, and all cell restoration are
  preserved;
- all used priority overlaps are either guard-disjoint or select the intended
  candidate path; the duplicated mixed float arithmetic rules have identical
  right-hand sides;
- there is no candidate answer-encoding rule, program bypass, oracle,
  fabricated result, or unmodeled used construct.

### Fixed operational bridges and opaque values

The fixed `math.floor`/`math.ceil` rules are syntactic priority bridges. They
skip ordinary lookup, but on this candidate's exact one-argument calls the
module imports `math`, never rebinds it, and the bridge preserves argument
evaluation, returned integer, continuation, frame, and all observable modeled
cells. Its broader behavior under a hypothetical shadowed `math` name is not
reachable from this submitted program.

The result-bearing proof primitives are:

```text
decStrToF, floorFI, ceilF, intToF, subF, ltIF, floatLt
```

They are fixed, supplied operations intentionally opaque to Haskell and
concrete through LLVM float hooks. They are not program-defined bodies and
were not added by the candidate. The K theorem is interpretation-parametric in
them; the nearest-integer interpretation is conditional on their ordinary
finite-binary-float contracts. This is a real trust boundary, not a universal
connection theorem.

### Supplied-model gaps and witnesses

The used `decStrToF` concrete parser models digits, an optional dot, and an
optional leading minus, but not all CPython spellings. This audit independently
translated and ran `auditor_model_gap_probe.py`:

```text
krun /tmp/audit-work/auditor_model_gap_probe.mpy \
  --definition /tmp/audit-work/auditor-runtime-kompiled
```

The K assertion that the submitted algorithm returns 632 for `"1e2"` passes
with `.K`, `NoExc`, and exit 0
(`evidence/stage5/model-gap-krun.*`). Independently,
`evidence/stage5/cpython_model_gap_probe.py` imports the unchanged submission,
prints 100, asserts it, and exits 0. Thus the concrete divergence is:

```text
supplied model: closest_integer("1e2") = 632
submitted CPython: closest_integer("1e2") = 100
```

The candidate's trust ledger explicitly reports this witness and also records
plus-sign, whitespace, exponent, and ASCII boundaries. This satisfies all four
campaign-exception conditions: fixed supplied origin, no additional theorem
narrowing, explicit ledger/witness, and faithful submitted CPython behavior.

The exhaustive review also found CPython-inexact behavior in unused supplied
subset modules. Examples with concrete false conclusions are proof-mode
structural sequence equality (`[True] == [1]` is true in CPython but structural
K equality distinguishes the elements) and the string-count empty-pattern
fold (`"abc".count("")` is 4 in CPython, while the supplied fold returns 0).
Opaque `sortVS`, `sortKeyVS`, `md5hexCodes`, and total out-of-bounds indexing
also lack universal in-K connection theorems. None of these symbols, rules, or
terms occurs in the submitted body, a precondition, a guard, or a
postcondition. They are term-disjoint and cannot enable a false conclusion
about this program. They are recorded as narrower fixed-subset evidence gaps,
not mislabeled as candidate unsoundness.

## 6. Fresh non-vacuity test

The candidate's own `spec-vacuity.k` and log were inspected only as untrusted
evidence. This audit created a distinct mutation,
`evidence/stage6/auditor-false-spec.k`, changing the real positive-near result
from `floor(F)` to the false `floor(F)+1`.

The dry run in `stage6/dry-run.*` parses/builds successfully and exits 0. The
actual command in `stage6/kprove-false.cmd` exits 1 with
`WarnStuckClaimState`. Its residual is exactly:

```text
floorFI(decStrToF(CS)) +Int 1 #Equals floorFI(decStrToF(CS))
```

The precondition is satisfiable: `"15.3"` takes this branch, the real result is
15, and the mutation demands 16. This is a semantic failure, not a parser
error, crash, timeout, or unreachable mutation.

For independent body sensitivity, `auditor-body-mutation-spec.k` changes the
executed closure's positive far/tie `return upper` to `return lower`, while
retaining the original `ceilF(F)` destination. It dry-runs successfully and
then exits 1 with a residual requiring `floorFI(F) == ceilF(F)`. Witness
`"14.5"` gives mutated 14 versus required 15. Evidence is in
`stage6/body-dry-run.*` and `stage6/kprove-body-mutation.*`.

## 7. Proven versus assumed accounting

### Formally established

Under the freshly compiled supplied Haskell definition, for every
`CS:IntSeq` satisfying each respective guard, the exact submitted function
body:

1. calls the fixed string-to-float operation;
2. computes the fixed floor and ceil values;
3. follows the sign and strict half-distance branch represented in the guard;
4. returns the stated endpoint; and
5. restores all modeled environment, scope, allocator, heap, stack, return,
   exception, and exit-code cells.

The four guards cover all fixed-model Boolean outcomes. The theorem is
unbounded and body-sensitive. It is a partial-correctness theorem; it does not
promise a normal integer result for invalid strings or non-finite values where
the source description does not determine one.

### Trust ledger

| Boundary | Effect and dependents | Assessment/evidence |
|---|---|---|
| Trusted `py2mpy.py` | Connects submitted Python AST to the executed constructor body | Byte-identical regeneration plus constructor-level comparison; accepted trusted input |
| K toolchain/backends | Parses, compiles, executes, and proves the fixed theory | Fresh K v7.1.293 builds and runs; ordinary machine-checking trust |
| Fixed call/frame/control rules | Binding, evaluation order, return, and modeled state | Exact used-rule trace; concrete execution; both result/body mutations |
| `decStrToF` | Determines all numeric values, branches, and results | Supplied external primitive; LLVM/differential evidence; explicit `"1e2"` gap |
| `floorFI`, `ceilF` | Determine endpoints and returned integers | Supplied primitives; concrete branch/boundary probes |
| `intToF`, `subF` | Determine endpoint distances and branches | Supplied primitives; concrete near/at/far half probes |
| `ltIF`, `floatLt` | Determine sign and strict-distance branches | Supplied Boolean primitives; complementary formal guards and concrete witnesses |
| Fixed math-call intercept/import model | Skips general module binding/attribute lookup | Faithful for this unshadowed candidate; model-level limitation, not candidate extension |
| Nearest-endpoint mathematics | Connects floor/ceil distance cases to the docstring phrase “closest integer” | Straightforward informal argument; tie strictness checked at both signs |
| Finite differential/concrete evidence | Supports CPython/model and intent bridges only on tested cases | 1,284 Python differentials, 15 fresh LLVM assertions, explicit gap; not substituted for K proof |

### Gate and benchmark mapping

- Gate A (real-program soundness): PASS.
- Gate B (intent adequacy): PASS for all docstring-determined finite-number
  behavior, with a documented supplied-model representation gap.
- Gate C (trust/evidence auditability): PASS; assumptions and finite evidence
  are explicit and reproducible.

The candidate's `VALIDATED` headline is stronger than the benchmark's final
mapping. The documented supplied-model gap triggers campaign amendment v2
exception 1, so the appropriate completed-audit result is `CONCERNS / LEGIT`.
There is no candidate-caused domain narrowing, failed proof, vacuity,
substituted body, or reachable unsound rule that would justify `FAIL`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
