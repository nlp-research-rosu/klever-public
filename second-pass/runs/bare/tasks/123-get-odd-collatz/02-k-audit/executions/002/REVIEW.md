# Independent adversarial audit: 123-get-odd-collatz

The candidate cleanly reconstructs and its local generated semantics is sound
for every construct used by the submitted program. Its claims are
result-constraining, non-vacuous, and mechanically pinned to the trusted-
regenerated program AST. However, it proves the end-to-end result only for
eight fixed inputs. The two symbolic claims prove one parity branch step, not a
loop invariant or a universal entry theorem. The HumanEval contract covers
arbitrary positive integers. This is therefore materially
`SOUND-BUT-LIMITED` in Kit terminology and, under the benchmark's explicit
mapping, `FAIL / NOT_LEGIT`.

## 1. Input and provenance integrity

I first read `/audit-input.json` and used its `container_paths` rather than the
host provenance paths. It declares:

- problem `123-get-odd-collatz`, condition `bare`;
- `record_layout = legacy-selected-stage1`;
- `semantics_mode = GENERATED_SEMANTICS`;
- complete input provenance.

All required launcher and generation records for that layout are present,
readable real files/directories, and not symlinks: `/audit-input.json`,
`/audit-campaign-lock.json`, `/run.json`, `/task.json`,
`/generation-result.json`, `/generation-evidence/invocation.json`,
`metrics.json`, `codex-last.txt`, `codex-output.log`, `prompt.txt`, and the
structured trace. The optional present `usage.json` was also inspected.
Historical `runtime-metrics.json` is absent but is not required by this legacy
layout.

`/audit-campaign-lock.json` is JSON-equal to the `audit_campaign` block and its
independent SHA-256 is the recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
All recorded leaf-file hashes checked by the reviewer match. Candidate
`prompt.py` and `py2mpy.py` are byte-identical to their trusted mounted
versions.

For independent aggregate verification, the reviewer recomputed the pipeline
tree hash directly from entry names, types, sizes, and bytes. The candidate
tree is
`d6a27bfb92fd82332b1b3d059def1dea773843d3fa1f5cdf192006dd6a322a64`,
matching both the invocation's retained workspace hash and
`generation-result.json`. The trace tree is
`b7f10377d4b0abe0ae0254046fb2bed0f7304dc45b4a72d174e676a6cf405bc4`,
matching `usage.json`; its one 313-line JSONL file also matches the recorded
leaf hash and every line parses. The launcher-owned alternate aggregate digest
fields are recorded in the same log and were not confused with this specified
pipeline-tree encoding.

The generated-semantics boundary is intact:
`/reference/reference-semantics` does not exist. There are no candidate or
generation-evidence symlinks. The candidate contains all proof source
artifacts needed below. I found no infrastructure breach.

Evidence:

- `evidence/scripts/stage1_integrity.py`
- `evidence/logs/stage1-integrity.log`
- `evidence/logs/toolchain-versions.log`

Generation records were treated only as provenance claims. No candidate log,
prior result marker, or trace was used as proof evidence.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

From trusted `/reference/prompt.py` and `/reference/canonical.py`: for a
positive integer `n`, follow the Collatz trajectory (`n/2` if even, `3n+1` if
odd) until `1`, collect the odd terms, and return them sorted increasingly.
The minimum case is `Collatz(1) = [1]`; the documented example is
`get_odd_collatz(5) == [1, 5]`. There is no valid “empty input” because the
contract's input is a positive integer; `n=1` is the boundary/minimal-output
case.

The candidate's `solution.py` uses exact integer `//` rather than the
canonical implementation's `/`, accumulates each odd term before its odd
transition, and appends `1` at return. On the intended positive-integer domain
this is the same algorithmic result when the trajectory reaches 1. Inputs
`n <= 0` are outside the source contract and were not used to widen or narrow
the audit.

Trusted regeneration:

```text
python3 /tmp/audit-work/reference/py2mpy.py solution.py > regenerated-solution.mpy
cmp -s regenerated-solution.mpy solution.mpy
```

exited 0. Both files have SHA-256
`66f5221c16c9b6d2b31815ba5c856f965d2c2ca1142b4152277aa3720cbb18e6`.

The independent differential script imports the trusted canonical function and
candidate function as separate modules. It checks:

- named boundaries and representatives
  `1,2,3,4,5,6,7,19,27,97,871,6171`;
- every input `1..1000`;
- 200 seeded generated integers in `1..10000`.

There were 1,179 unique inputs and zero mismatches. This is finite fidelity
evidence, not a universal proof.

Evidence:

- `evidence/logs/stage2-regenerate-mpy.log`
- `evidence/scripts/differential.py`
- `evidence/logs/stage2-differential.log`

## 3. Clean proof reconstruction

I copied only candidate source artifacts to `/tmp/audit-work/candidate-src`.
No candidate-compiled definition or cache was copied or reused. K was
v7.1.293.

### Generated semantics

Fresh LLVM build:

```text
kompile semantic.k --main-module SEMANTIC --syntax-module MPY-SYNTAX \
  --backend llvm --output-definition semantic-audit-kompiled
```

exited 0 (`evidence/logs/stage3-kompile-llvm.log`). Fresh `krun` executions for
`n = 1,2,3,5,6,27` all exited 0 and terminated with empty `<k>`, cleared local
maps, and the expected exact list. A reviewer script parsed the K result and
compared it with both Python implementations; all six were equal. This covers
the loop-skipping boundary, first even and odd branches, the prompt example,
and a 112-transition trajectory.

Evidence:

- `evidence/scripts/compare_krun_python.py`
- `evidence/logs/stage3-krun-python-compare.log`
- `evidence/logs/stage3-krun-n1.log` through
  `evidence/logs/stage3-krun-n27.log`

### Proof definition and every positive claim

Fresh Haskell build:

```text
kompile verification.k --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX --backend haskell \
  --output-definition verification-audit-kompiled
```

exited 0 (`evidence/logs/stage3-kompile-haskell.log`).

The reviewer mechanically split `spec.k` into 12 one-claim modules, changing
only module names/import boilerplate. Each was run separately:

```text
kprove individual-claims/spec-claim-NN.k -I . \
  --definition verification-audit-kompiled \
  --spec-module SPEC-CLAIM-NN --output pretty
```

Every one exited 0 and printed exactly `#Top`. The original aggregate

```text
kprove spec.k --definition verification-audit-kompiled \
  --spec-module SPEC --output pretty
```

also exited 0 with `#Top`.

Evidence:

- `evidence/scripts/split_k_claims.py`
- `evidence/claims/spec-claim-01.k` through `spec-claim-12.k`
- `evidence/logs/stage3-kprove-claim-01.log` through
  `stage3-kprove-claim-12.log`
- `evidence/logs/stage3-kprove-all.log`

Thus clean reconstruction passes. What these successful claims mean is audited
next; `#Top` alone does not establish contract adequacy.

## 4. Adequacy and real-program pinning

### Plain-language claim inventory

The first eight claims have no symbolic precondition. Each fixes the complete
initial state to `run(solutionProgram)`, empty function/environment maps,
`noResult`, and exactly one input:

| Input | Required terminal list |
|---:|---|
| 1 | `[1]` |
| 2 | `[1]` |
| 3 | `[1,3,5]` |
| 5 | `[1,5]` |
| 6 | `[1,3,5]` |
| 7 | `[1,5,7,11,13,17]` |
| 19 | `[1,5,11,13,17,19,29]` |
| 27 | the exact 42-element list shown at `spec.k:85-90` |

These preconditions are plainly satisfiable: the displayed ground initial
configuration is a witness for each. Their result cells are exact, not free
variables, implications, or tautologies. The differential log substitutes all
eight inputs and confirms the required result against both Python functions.

Claim 9 (`even-step`) says that, for arbitrary `M > 0` and arbitrary integer
list `OS`, executing the actual branch with
`n = 2*M, odds = OS` terminates with `n = M, odds = OS`. A concrete satisfying
witness is `M=1, OS=.Ints`.

Claim 10 (`odd-step`) says that, for arbitrary `M > 0` and `OS`, executing the
actual branch with `n = 2*M+1` terminates with `n = 6*M+4` and appends the
original odd value to `OS`. A concrete witness is `M=1, OS=.Ints`, producing
`n=10, odds=[3]`. Excluding `M=0` here does not omit a reachable loop branch:
the loop guard is false at `n=1`.

Claims 11 and 12 execute observer wrappers on the fixed list
`[17,1,7,5,13,11]`; one proves sorting that list yields a sorted list and the
other proves its elements are odd. They neither consume the program's result
nor quantify over outputs.

### Program pinning

`solutionProgram`, `collatzLoop`, and `collatzBranch` are nullary
definitional AST constants, not execution shortcuts. For a mechanical
constructor comparison, I rebuilt an LLVM definition whose parser exposes
`VERIFICATION`, ran trusted-regenerated `solution.mpy` and the text
`solutionProgram` for one semantics step, and compared their KORE
configurations. Both KORE lines are byte-identical with SHA-256
`b2983dc149bdafdb86909e6382f885448668800109ab7da5c9dc0778ada5d93d`.
At that point both `<k>` cells contain the same expanded function binding/body
under `load(...) ~> start`; explicit `.Ids`, `.Exprs`, and `.CmpOps` in
`verification.k` are just the list terminators elided by concrete syntax in
`solution.mpy`.

Evidence:

- `evidence/pinning/solutionProgram.term`
- `evidence/logs/stage4-kompile-pinning.log`
- `evidence/logs/stage4-pin-source-depth1-kore.log`
- `evidence/logs/stage4-pin-helper-depth1-kore.log`
- `evidence/logs/stage4-pin-kore-compare.log`

A body-sensitivity test changed the AST actually expanded by
`collatzBranch`, replacing `3*n+1` with `n+1`. The mutated definition built
successfully. The `n=5` entry claim then exited 1 with
`WarnStuckClaimState`; its concrete terminal result was `[1,3,5]`, not
`[1,5]`. This confirms the finite entry theorem depends on the submitted body.

Evidence:

- `evidence/mutations/verification-body-mutated.k`
- `evidence/logs/stage4-body-mutation-create.log`
- `evidence/logs/stage4-body-mutation-build.log`
- `evidence/logs/stage4-body-mutation-proof.log`

### Material adequacy failure

There is no entry claim with symbolic `N` and precondition `N > 0`; no loop
invariant; no recursive trajectory summary; and no postcondition connecting a
general output to all odd terms in the Collatz trajectory. The parity claims
prove only one branch execution and are not composed into a loop theorem. The
observer claims are two unrelated ground examples.

Partial correctness does not require proving the Collatz conjecture or
termination. It does require a theorem applying to every intended positive
input for which execution terminates. Eight fixed end-to-end executions cannot
supply that theorem. This is a material narrowing from all positive integers to
`{1,2,3,5,6,7,19,27}`.

## 5. Rule-by-rule static soundness review

The exhaustive inventory is
`evidence/rule-inventory.md`; source extraction is preserved in
`evidence/logs/stage5-static-extraction.log`. It enumerates every local syntax
production, configuration cell, function/`total` declaration, and all 44 rules
in `semantic.k` plus all 10 rules in `verification.k`. There are no local
`functional`, priority, simplification, anywhere, macro, symbolic, opaque/fresh,
or owise declarations.

Every submitted constructor is covered:

- module/function loading and the fixed entry binding;
- assignment and local map updates;
- `while`, `if`, and top-level return control;
- left-to-right evaluation of literals, names, singleton/empty lists, binary
  operations, comparisons, and `sorted`;
- the exact used operations `+`, `*`, `%`, `//`, `==`, and `!=`;
- immutable append and insertion sort.

The configuration models precisely the observable state used here:
computation, input, functions, local bindings, and result. Heap/allocation
identity can be abstracted because lists are local immutable values in this
program and no alias is observed. K integers are unbounded, agreeing with the
submitted Python integer operations over the positive reachable domain.
`%Int` and `/Int` are guarded so that every used case (nonnegative dividend,
positive divisor) matches Python `%` and `//`. Comparator guards and insertion
guards are pairwise disjoint and exhaustive. Every `[total]` recursive function
has constructor-complete base/step equations and structural descent.

The semantics deliberately does not cover unused multi-element literal syntax,
chained comparisons, arbitrary calls, arbitrary signed floor division, or a
return buried under an unmatched continuation. Under the
`GENERATED_SEMANTICS` boundary, this is acceptable minimality: no such term is
used by `solution.mpy`, and unsupported terms stop rather than fabricate
results.

`collatzBranch`, `collatzLoop`, and `solutionProgram` only expand to AST; fixed
semantics still executes every loop test, branch, arithmetic operation,
collection operation, and return. `isSorted` and `allOdd` are truthful,
terminating observer definitions. Their wrappers are separate commands used
only by ground observer claims; they do not bridge or replace program
execution. No rule encodes a Collatz answer, introduces an unconstrained oracle,
or bypasses a property-bearing computation.

I found no local unsound rule. Accordingly there is no claimed unsoundness for
which a false-conclusion witness is owed. The defect is theorem scope, not a
false semantic equation.

## 6. Fresh non-vacuity test

There is no candidate `spec-vacuity.k`. I created a fresh mutation of the
satisfiable `n=5` entry claim, changing only its result obligation from
`[1,5]` to the demonstrably false `[1,7]`.

The spec build/dry run:

```text
kprove spec-vacuity.k -I /tmp/audit-work/candidate-src \
  --definition /tmp/audit-work/candidate-src/verification-audit-kompiled \
  --spec-module SPEC-CLAIM-04 --dry-run
```

exited 0, so this is not parser/import/build failure. The actual proof command
without `--dry-run` exited 1 and emitted `WarnStuckClaimState`. Its residual is
a fully terminated concrete configuration with actual
`result(vl(1 :: 5 :: .Ints))`, which cannot unify with the mutated destination
`[1,7]`. This is the expected unmet result obligation.

Evidence:

- `evidence/mutations/spec-vacuity.k`
- `evidence/logs/stage6-mutation-create.log`
- `evidence/logs/stage6-mutation-dry-run.log`
- `evidence/logs/stage6-mutation-proof.log`

The limited ground theorem is therefore discriminating and non-vacuous.

## 7. Proven versus assumed accounting

### Precisely proven

Under the generated semantics and K builtins, the machine-checked proof
establishes:

1. exact full-program termination/results for the eight fixed inputs listed in
   stage 4;
2. the exact state transition of one even branch for all `M>0` and arbitrary
   `OS`;
3. the exact state transition of one odd branch for all `M>0` and arbitrary
   `OS`;
4. two ground facts about separate sorted/odd observer commands.

It does **not** establish the HumanEval result for an arbitrary positive input,
even conditionally on termination. It also does not establish a universal
sortedness or all-odd property of returned results.

### Trust ledger

| Boundary | Influence | Assessment |
|---|---|---|
| K v7.1.293 compiler, Haskell/LLVM backends, reachability prover | All parsing, execution, and proof closure | Necessary low-level trust boundary; fresh builds and exact exit/output evidence recorded. |
| Imported `INT`, `BOOL`, `STRING`, `MAP`, K sequencing/list machinery | Arithmetic, conditions, bindings, generated list syntax | Acceptable ordinary K primitive boundary. Used arithmetic guards stay in the Python-agreeing positive domain. |
| Trusted `/reference/py2mpy.py` | Python-to-constructor bridge | Acceptable benchmark-trusted input; byte-identical regeneration pins submitted `solution.mpy`. |
| `solutionProgram` AST constants | Program identity | Formally reduced and mechanically KORE-equal to the regenerated source term; body mutation is proof-sensitive. No oracle. |
| Generated `semantic.k` | Entire modeled execution | Individually generated and therefore not externally blessed. It passed construct-complete static review and fresh concrete boundary tests; every used operation executes. No task answer is assumed. |
| Direct `start` rule and `sorted` builtin rule | Entry binding/control and returned order | Acceptable modeling primitives for this single fixed module. Exact binding is matched; insertion sort is exhaustively and truthfully defined over `Ints`. |
| Python differential testing | Implementation-to-canonical fidelity on 1,179 inputs | Finite empirical bridge only. It cannot replace a universal K claim and is not treated as one. |
| Collatz termination | Whether arbitrary executions finish | Not proven or assumed by the finite claims. A legitimate partial-correctness theorem could remain conditional on termination, but no universal conditional theorem exists here. |

### Gate/status accounting and decision

- Gate A (real-program soundness of the claims actually stated): **PASS**.
  The theory is sound for used constructs, pins the actual AST, constrains
  results, is body-sensitive, and rejects a false result.
- Gate B (intent adequacy): **FAIL**. The formal entry domain is eight fixed
  inputs rather than arbitrary positive integers.
- Gate C (auditability of the limited theorem): **PASS**. Commands, artifacts,
  witnesses, finite evidence scope, and trust boundaries are reproducible and
  explicitly separated.

Generic Kit status would be `SOUND-BUT-LIMITED`. The benchmark expressly maps a
material narrowing of the HumanEval source-contract domain to
`FAIL / NOT_LEGIT`, not to `CONCERNS`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
