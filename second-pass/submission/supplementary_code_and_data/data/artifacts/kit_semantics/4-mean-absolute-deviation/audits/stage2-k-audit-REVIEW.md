# Independent adversarial review: 4-mean-absolute-deviation

This audit used the required `using-kit` then `validating-proof` workflow. It
did not rely on the candidate's compiled definitions, `#Top` logs,
`PROOF.md`, trace, or final report. All executable reconstruction occurred
below `/tmp/audit-work/reconstruct`; reviewer-authored artifacts and bounded
logs are below `/audit-output/evidence`.

The reconstructed reachability proof is legitimate for arbitrary finite
all-`Float` `ValSeq` inputs under the supplied MPY semantics, and it pins the
actual submitted program. I assign `CONCERNS`, rather than `PASS`, because a
pair of proof-local dynamic-sort dispatch equations accelerate fixed semantic
function evaluation without a separately closing bridge-free universal K
connection claim, and because the Python/canonical boundary has two documented
scope discrepancies. I found no false-rule witness, substituted program,
bounded unrolling, vacuity, or non-result-constraining theorem.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- `record_layout`: `pipeline-v3`;
- `condition`: `kit-semantics`;
- `semantics_mode`: `SUPPLIED_SEMANTICS`;
- `mount_reference_semantics`: `true`;
- problem `4-mean-absolute-deviation`.

The mode and mounts agree: `/reference/reference-semantics` is present as a
real directory. There is no infrastructure contradiction and no reason to
emit `AUDIT_ERROR`.

I checked every pipeline-v3-required record as a real regular file and parsed
the launcher records:

- `/run.json`, `/task.json`, `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`,
  `runtime-metrics.json`, `usage.json`, `codex-last.txt`,
  `codex-output.log`, and `prompt.txt`;
- the JSONL trace below `/generation-evidence/codex-trace`.

All launcher-recorded single-file SHA-256 values match the mounted bytes. The
campaign object in `/audit-input.json` equals
`/audit-campaign-lock.json` exactly, and the lock file independently hashes to
the recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
All launcher inputs are mounted read-only.

The candidate prompt and translator are byte-identical to
`/reference/prompt.py` and `/reference/py2mpy.py`. A recursive path/type/byte
comparison of `/candidate/reference-semantics` against
`/reference/reference-semantics` found no missing, additional, changed,
mistyped, or linked entries. Both independently have pipeline-v3 tree digest
`4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`.
The complete candidate tree independently has pipeline-v3 digest
`875628de06d02e3e2a63813bb4c80eec8cf1c89960042f69c6d6506498816798`,
matching the output workspace digest in both the invocation and generation
result.

The one trace file hashes to the value in the invocation/result. Its complete
338-line JSONL stream parses without error; its tree digest matches
`usage.json`. The 33,781-line generation output was inspected as untrusted
construction evidence. The records claim success, `#Top`, 267 differential
cases, and expected mutation failures; none of those claims was accepted
without reconstruction.

Evidence:

- `/audit-output/evidence/integrity_check.py`
- `/audit-output/evidence/stage1-integrity.log`
- `/audit-output/evidence/stage1-readonly-mounts.log`
- `/audit-output/evidence/generation_trace_summary.py`
- `/audit-output/evidence/stage1-generation-trace-summary.log`
- `/audit-output/evidence/stage1-generation-output-summary.log`
- `/audit-output/evidence/toolchain-versions.log`

Observed audit toolchain: K 7.1.293 and Python 3.10.12.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt asks
`mean_absolute_deviation(numbers: List[float]) -> float` to calculate the
average absolute difference of each element from the arithmetic mean. Its
documented example is:

```python
mean_absolute_deviation([1.0, 2.0, 3.0, 4.0]) == 1.0
```

The trusted canonical computes `mean = sum(numbers) / len(numbers)` and then
`sum(abs(x - mean) for x in numbers) / len(numbers)`.

The generated `solution.py` computes the same operation order using two
explicit loops. It additionally returns `0.0` when `len(numbers) == 0`. Its
initial `number = 0.0` is semantically inert for nonempty iterations and makes
the loop variable defined on the empty path.

Regeneration with the trusted translator:

```text
python3 /reference/py2mpy.py /candidate/solution.py
```

exited 0 and was byte-identical to `/candidate/solution.mpy`; both translation
artifacts hash to
`a0c4dd8f00832c5527f0b078793cb5545efc3c79fd855ab06b062499ca5ea1a0`.

The independent differential script imports the trusted canonical and
generated entry points directly. It checks the prompt example, the empty and
singleton branch boundary, equal/opposite/mixed values, signed zero,
subnormal/minimum-normal/maximum finite floats, infinity, NaN, integer and
mixed numeric runtime boundaries, and 264 seeded random lists across lengths
1 through 64. Of 280 cases, there were zero nonempty-finite mismatches and one
total mismatch:

```text
input=[]
canonical=ZeroDivisionError
generated=0.0
```

Thus the candidate is faithful on the nonempty annotated float domain, while
the empty behavior is an explicit generated-program extension, not canonical
behavior. The mathematical MAD of an empty dataset and the prompt's exception
behavior are unspecified; the canonical strongly suggests an implicit
nonempty domain. I treat the extra return as a documented fidelity concern,
not a false result on the canonical nonempty domain.

Both Python functions also accept integer/mixed lists at runtime, while the K
theorem requires every K element to have sort `Float`. Under the literal
`List[float]` annotation this is not a material narrowing; it remains an
important excluded runtime extension. If “input numbers” were interpreted to
include arbitrary K `Int` elements despite the annotation, that would instead
be a material domain restriction.

Evidence:

- `/audit-output/evidence/stage2-translation-identity.log`
- `/audit-output/evidence/differential_test.py`
- `/audit-output/evidence/stage2-differential.log`

## 3. Clean proof reconstruction

I copied only source artifacts into `/tmp/audit-work/reconstruct`, using the
trusted reference-semantics tree. I did not copy or use the candidate's
`runtime-kompiled`, `verification-kompiled`, binary caches, or parsed/compiled
outputs.

Fresh concrete build:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-audit-kompiled
```

Exit 0. A reviewer-authored module containing the exact generated function
body and assertions for empty, singleton, prompt-example, opposite-sign, and
mixed-sign inputs translated with the trusted translator. `krun` exited 0 and
ended with `.K`, an empty call stack, `noRet`, `NoExc`, and exit code 0.

Fresh proof build:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-audit-kompiled
```

Exit 0. The following independent positive proof commands all exited 0 and
printed `#Top`:

```text
kprove spec.k --definition verification-audit-kompiled \
  --spec-module SPEC --claims SPEC.sum-loop

kprove spec.k --definition verification-audit-kompiled \
  --spec-module SPEC --claims SPEC.deviation-loop

kprove spec.k --definition verification-audit-kompiled \
  --spec-module SPEC
```

The last command contains both circularities and the entry claim; it is the
complete target-proof execution. The compiler warnings are confined to
pre-existing supplied-semantics unused-variable/non-exhaustiveness warnings
and unused framed claim variables.

Evidence:

- `/audit-output/evidence/stage3-llvm-build.log`
- `/audit-output/evidence/stage3-concrete-smoke.log`
- `/audit-output/evidence/stage3-haskell-build.log`
- `/audit-output/evidence/stage3-kprove-sum-loop.log`
- `/audit-output/evidence/stage3-kprove-deviation-loop.log`
- `/audit-output/evidence/stage3-kprove-full-spec.log`

## 4. Adequacy and real-program pinning

### Plain-language claims

`SPEC.sum-loop` says: with an arbitrary finite remaining list suffix `VS`
whose elements are floats, executing the actual first `for` loop terminates
the loop region and changes `total` from an arbitrary float accumulator `ACC`
to the exact left fold `sumFloatVS(VS, ACC)`. It uses the real callee
environment, scopes, body, target variable, builtin scope, heap, stack,
return, exception, and exit-code cells.

`SPEC.deviation-loop` analogously says: executing the actual second loop
changes `deviation` from `ACC` to the left fold that adds
`absF(subF(element, MEAN))` for every remaining float, while preserving the
same `MEAN` and caller state.

`SPEC.mean-absolute-deviation` says: for every finite `ValSeq VS` satisfying
`allFloatVS(VS)`, load the submitted module, bind its exact function body,
look up and call it with `list(VS)`, execute the body, and return:

- `0.0` if `VS` is empty;
- otherwise the exact structural term obtained by dividing the first
  left-fold sum by the length, accumulating absolute deviations around that
  mean, and dividing the second fold by the same length.

This postcondition is equality to `madResult(VS)`, not a free result variable,
tautology, or one-way implication.

### Mechanical program identity

I parsed the submitted `solution.mpy` and a claim-side module containing
`madBody` with the fresh proof definition and `kast --expand-macros`. Their
expanded KORE files are byte-identical, both hashing to
`3cbc4861392f2c3bd8c81361e33e6af3cc7e78615233c900f351ed73e8214b26`.
This is a constructor-level demonstration that the entry claim loads the
submitted function binding and body, including the typing-only import.

The candidate body mutation changes the actual `Return(Float(0.0))` constructor
to `Return(Float(1.0))`. Under the fresh definition, that changed program term
reached `1.0` against expected `0.0`, produced `WarnStuckClaimState`, and
exited 1. It therefore tests theorem sensitivity to the executed body rather
than changing an external source file only.

### Satisfiability and concrete substitution

`VS = vCons(1.0, vCons(2.0, vCons(3.0, vCons(4.0, .ValSeq))))` is a concrete
entry witness; `allFloatVS(VS)` reduces to `true`, and all initial cells in the
claim are realizable.

Reviewer evaluation of the claim's exact fold definitions on four nonempty
ground witnesses agrees exactly with both trusted canonical and generated
Python, including the prompt result `1.0`. The fresh LLVM execution supplies
the corresponding concrete fixed-semantics bridge.

A diagnostic attempt to force the Haskell proof backend to numerically reduce
the ground prompt example stopped at its documented missing `FLOAT.add` hook.
This is not a failed target claim: the supplied proof semantics deliberately
keeps `addF`, `subF`, `absF`, and `divFloatIntV` opaque, and the successful
target theorem constrains their exact structural composition. Numerical
ground evidence comes from LLVM and Python.

Evidence:

- `/audit-output/evidence/stage4-constructor-pinning.log`
- `/audit-output/evidence/stage4-submitted-program-expanded.kore`
- `/audit-output/evidence/stage4-claim-program-expanded.kore`
- `/audit-output/evidence/stage4-body-sensitivity.log`
- `/audit-output/evidence/postcondition_substitution.py`
- `/audit-output/evidence/stage4-postcondition-substitutions.log`
- `/audit-output/evidence/stage4-ground-substitutions.log`

## 5. Rule-by-rule static soundness review

The mechanical inventory covers every declaration/rule in the 24 supplied K
files plus `verification.k` and `spec.k`: 233 syntax records, 710 rule records,
five contexts, one configuration, and three claims. The exhaustive statements,
guards, priorities, and attributes are in
`/audit-output/evidence/stage5-k-rule-inventory.log`.

Because this is `SUPPLIED_SEMANTICS`, every rule in those 24 fixed-semantics
files is classified as the launcher-selected semantics trust boundary after
recursive byte/type identity was established. I separately traced every
construct actually used by `solution.mpy`: module loading and sequencing,
typing import, function binding/call/frame lifecycle, name and builtin lookup,
left-to-right arguments/operators, assignment, length, integer equality,
branching, list iteration and target binding, float literals,
addition/subtraction/division/absolute value, return, frame pop, and all active
configuration cells. The exact declaration/rule mapping is in
`/audit-output/evidence/stage5-static-review.md`.

The complete proof-local decisions are:

| Local extension | Decision |
|---|---|
| `madBody` macro | Sound, semantically inert, mechanically identical after macro expansion to the submitted body. |
| `allFloatVS` | Sound total domain predicate; empty/cons equations are exhaustive and disjoint and recurse on the tail. |
| `projectFloat` declaration | A total opaque float outside `isFloat`; underspecified there, but no target use is outside the guard. This is a local opaque boundary that candidate `PROOF.md` did not acknowledge. |
| Cast `#Ceil` characterization and concrete/symbolic orientations | Sound guarded sort-projection equations. Mode-specific orientations do not form a runtime cycle; `projectFloat(F) => F` fixes actual floats. |
| Guarded `applyBin("+", A:Float, V:Val)` | Sound sort-refined form of the supplied `Float,Float` equation. On its overlap, `projectFloat(V)` collapses to `V`, so RHS values agree. |
| Guarded `applyBin("-", V:Val, M:Float)` | Same decision for subtraction. |
| `sumFloatVS` | Sound, exhaustive, descending left fold matching the first loop's exact order. |
| `deviationFloatVS` | Sound, exhaustive, descending fold matching the second loop's exact subtraction/absolute/addition order. |
| `madResult` | Sound result definition. Zero/nonzero length guards are disjoint and exhaustive for `vsLen`; the equations match the empty return and nonempty body. |
| Two loop claims | Sound circularities over arbitrary remaining finite suffixes. They execute the real `#loop` control flow and preserve/frame every material cell. |
| Entry claim | Sound, result-constraining execution of the real module/function/body over arbitrary finite all-float inputs. |

There is no rule that encodes an unrelated task answer, bypasses module
binding, replaces a loop with an oracle, invents state, or discards control.
The summaries name results, while the two loop claims establish their
execution connection.

The projection witness `projectFloat(1.0) => 1.0` closes; the opposite
interpretation `projectFloat(1.0) => 2.0` fails with a residual `1.0`, so this
result-bearing helper does not admit that false value.

The guarded `applyBin` simplifications behaviorally accelerate fixed semantic
function dispatch and therefore deserve Kit's operational-bridge scrutiny. I
built a separate definition importing only fixed semantics and attempted
universal guarded connection claims. The Haskell backend left the claim stuck
at the expected `isFloat(V)`-to-sort-projection implication. This is a missing
machine-checked bridge-free universal connection, but not an unsoundness
witness: the local equations are exactly the fixed typed rules after an
identity projection; guards and overlaps are disjoint/agreeing; and no
opposite ground value is admitted. In accordance with the benchmark
instruction, I record the narrower evidence gap and do not label the rules
unsound without a false conclusion witness.

Evidence:

- `/audit-output/evidence/k_inventory.py`
- `/audit-output/evidence/stage5-k-rule-inventory.log`
- `/audit-output/evidence/stage5-static-review.md`
- `/audit-output/evidence/stage5-projection-witnesses.log`
- `/audit-output/evidence/stage5-bridge-free-connections.log`
- `/audit-output/evidence/stage5-bridge-free-connections-v2.log`

## 6. Fresh non-vacuity test

I did not rely on the candidate's `spec-vacuity.k`. The fresh
`/tmp/audit-work/reconstruct/auditor-vacuity.k` starts from the complete
submitted module constructor and satisfying empty input, but changes the
result obligation from actual `0.0` to false `42.0`.

The mutation dry run exited 0, proving the artifact parsed and built. The
actual proof then reached a residual `<k> 0.0 ~> .K </k>`, emitted
`WarnStuckClaimState`, and exited 1 because the destination required `42.0`.
This is the intended unmet result obligation, not a parser error, missing
import, timeout, unrelated crash, or unreachable mutation. The positive proof
is therefore discriminating and non-vacuous.

Evidence:

- `/tmp/audit-work/reconstruct/auditor-vacuity.k`
- `/audit-output/evidence/stage6-fresh-nonvacuity.log`

## 7. Proven versus assumed accounting

### Formally established

Under the fresh Haskell definition consisting of the supplied MPY semantics
and the reviewed proof-local equations/claims, the proof establishes partial
correctness of the actual submitted generated program:

- for an arbitrary finite `ValSeq` containing only K `Float` values;
- from the claim's realizable initial module configuration;
- if execution reaches the function return;
- the result is exactly `madResult(VS)`, namely the generated program's
  left-to-right floating-point fold expression for mean absolute deviation,
  with explicit `0.0` on empty input;
- module loading, name/builtin lookup, argument evaluation, function
  allocation/binding, both loops, assignments, return, frame restoration,
  heap, stack, exception, and exit-code behavior all execute or are explicitly
  preserved by the claims.

This is unbounded in list length. It is not finitely many examples or a
bounded unrolling.

### Assumptions and empirical bridges

| Boundary | Influence | Accounting |
|---|---|---|
| Trusted `py2mpy.py` | Source-to-`solution.mpy` identity | Outside the theorem. Trusted regeneration is byte-identical; constructor-level pinning then connects `solution.mpy` to the entry claim. |
| Supplied MPY semantics | All language execution | Launcher-selected fixed trust boundary; candidate copy is recursively identical. |
| `addF`, `subF`, `absF`, `divFloatIntV` | Every nonempty numerical result | Opaque to Haskell by supplied design, with concrete LLVM equations. The theorem proves their exact composition, conditional on those primitives representing Python float operations. Reviewer LLVM execution and direct canonical differential tests are finite evidence. |
| Guarded `projectFloat`/dispatch lemmas | Symbolic float element projection and two loop arithmetic steps | Sound by sort/overlap review and ground opposite-value rejection; bridge-free universal K connection did not close, so this remains the principal nonfatal proof-evidence limitation. |
| K frontend/backend/toolchain | Compilation and reachability closure | Standard trusted checker boundary; observed version 7.1.293. |
| Fold expression means human-facing MAD | Intent interpretation | Direct mathematical/source-level correspondence for nonempty inputs; no separate real-analysis theorem is needed to see the formula, but IEEE primitive behavior remains conditional as above. |
| Python differential testing | Program/canonical runtime agreement | 280 finite cases, zero nonempty-finite mismatches, one explicit empty divergence. It supports but does not replace the K proof. |

The proof does not establish total correctness, a universal CPython-versus-MPY
semantics theorem, independent correctness of the translator/K backend/fixed
semantics, or a canonical return value on an empty dataset. It also does not
cover K `Int` elements, although the dynamic Python programs accept them.

### Decision

The proof closes cleanly, is non-vacuous and result-constraining, covers
arbitrary finite lengths over the literal `List[float]` domain, and
mechanically pins the exact generated module and body. No materially unsound
rule or false conclusion witness was found. Therefore this is a legitimate
partial-correctness proof, not `FAIL / NOT_LEGIT`.

The missing bridge-free universal closure for the guarded dispatch
simplifications, the unacknowledged outside-guard opacity of `projectFloat`,
the canonical empty-input divergence, and the excluded dynamic integer
extension prevent an unqualified `PASS`. They are documented trust/scope
limitations that do not make a false conclusion provable on the formal
all-float domain.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
