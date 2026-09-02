# Independent adversarial audit: 157-right-angle-triangle

## Outcome

The candidate's seven reachability claims all reconstruct to `#Top`, and a fresh
false-result mutation is rejected correctly. The proof is nevertheless not a
legitimate proof of the submitted program artifact. `verification.k` never
loads or refers to `solution.mpy`; it calls a closure whose body is handwritten
again inside `verification.k`. A clean body-sensitivity experiment replaced
both `solution.py` and its translator-identical `solution.mpy` with an
always-`False` program, rebuilt the proof definition, and the positive
Pythagorean claim still proved `#Top`. Thus the theorem is about a duplicated K
term, not the real generated program selected by the submitted artifact.

This is the decision boundary's substituted-program case. The failure is not an
infrastructure failure, a timeout, or an inference from a candidate report.

## 1. Input and provenance integrity

Semantics mode is `SUPPLIED_SEMANTICS`. The trusted mount is consistent with
that mode: `/reference/reference-semantics` exists.

The no-follow integrity checker in
[`evidence/check_integrity.py`](evidence/check_integrity.py) compared path sets,
entry types, and SHA-256 content:

- Candidate `prompt.py` is byte-identical to `/reference/prompt.py`.
- Candidate `py2mpy.py` is byte-identical to `/reference/py2mpy.py`.
- Candidate `reference-semantics/` has exactly the same 25 entries as the
  trusted tree. Every entry has the same type and bytes. There are no missing,
  additional, changed, mistyped, or symlinked semantics entries.
- `solution.py`, `solution.mpy`, `spec.k`, `verification.k`, and `prove.sh` are
  regular files, not symlinks.

Exact results are in
[`stage1_prompt_integrity.log`](evidence/stage1_prompt_integrity.log),
[`stage1_translator_integrity.log`](evidence/stage1_translator_integrity.log),
and
[`stage1_semantics_integrity.log`](evidence/stage1_semantics_integrity.log).
The complete candidate/reference type inventory is in
[`stage1_inventory.log`](evidence/stage1_inventory.log).

The following requested provenance artifacts are absent:
`run-input.json`, `metrics.json`, `codex-last.txt`, and `codex-output.log`.
No structured generation trace under a recognizable `generation-trace.*` or
`trace.*` name is present. `PROOF.md` is also absent. The candidate contains
ancillary concrete tests and Python bytecode, but none was trusted or reused.
These omissions reduce provenance/audit evidence; they do not contradict the
rendered semantics mode and therefore are not an infrastructure breach.

All execution inputs were freshly copied to `/tmp/audit-work`; the semantics
copy came from `/reference`, not from a candidate-built definition. Source
hashes and the scratch manifest are recorded in
[`scratch_manifest.log`](evidence/scratch_manifest.log). No candidate cache or
compiled definition was copied.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementations

The trusted prompt says that, given three triangle side lengths, the function
returns `True` exactly when the sides form a right-angled triangle. The trusted
canonical function tests the three permutations of the Pythagorean equality:

`a² = b² + c²`, or `b² = a² + c²`, or `c² = a² + b²`.

The candidate first rejects any non-positive input, then tests the same three
equalities in the order “`c` is hypotenuse, `b` is hypotenuse, `a` is
hypotenuse.” For positive numeric side lengths the implementations are
equivalent. For non-positive numbers they can differ because the canonical
implementation does not enforce the ordinary meaning of “length.”

### Translation identity

The trusted translator was run from scratch:

```text
python3 /tmp/audit-work/py2mpy.py /tmp/audit-work/solution.py > /tmp/audit-work/regenerated-solution.mpy
```

The regenerated and submitted `solution.mpy` files both have SHA-256
`703f3585497535059c241e012e8e977109876df7bf20c9821a17b359c1061ad7`
and are byte-identical. See
[`stage2_translate.log`](evidence/stage2_translate.log).

### Independent differential execution

[`evidence/differential_test.py`](evidence/differential_test.py) independently
imports the clean copy of `/reference/canonical.py` and the candidate
`solution.py`. It covers:

- both documented examples;
- empty, one-argument, and two-argument calls;
- every guard/equality/final-return branch boundary;
- all 27,000 positive integer triples in `[1,30]^3`;
- 5,000 deterministic random positive integer triples in `[1,10000]^3`;
- all 9,261 triples in `[-10,10]^3`;
- four representative positive float triples.

The command exited 0. There were zero mismatches in 32,006 categorized
positive-domain evaluations (some suites intentionally overlap). Both
implementations raised `TypeError` for each arity case. There were 205
mismatches in the non-positive grid; for example, canonical returns `True` for
`(-10,-8,-6)` while the candidate returns `False`. Two zero-valued guard
boundary cases also differ. Full counts and first witnesses are in
[`stage2_differential.log`](evidence/stage2_differential.log).

I treat strictly positive side lengths as the natural intended geometric
domain, so no differential mismatch was found on that domain. The prompt has
no type annotations, while the formal proof covers only K `Int`; positive
floats work in the two Python implementations but are outside the theorem.
That is an intent-scope limitation independent of the decisive pinning failure.

## 3. Clean proof reconstruction

The live toolchain was available: K `v7.1.337` and Python `3.10.12`; see
[`environment_versions.log`](evidence/environment_versions.log).

### Concrete definition

The trusted supplied semantics was freshly compiled:

```text
timeout 300 kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

Compilation exited 0. It emitted fixed-semantics warnings about several
`[total]` functions whose equations are not compiler-detected as exhaustive.
The exact warnings are preserved in
[`stage3_kompile_concrete.log`](evidence/stage3_kompile_concrete.log).

The reviewer-authored
[`concrete_audit.py`](evidence/concrete_audit.py) was translated with the
trusted translator and executed with:

```text
timeout 120 krun concrete-audit.mpy --definition runtime-kompiled
```

It exercises all three Pythagorean positions, an ordinary false case, all three
zero guard positions, and a negative guard case. `krun` exited 0 with `.K`,
`NoExc`, and exit code 0. See
[`stage3_prepare_concrete.log`](evidence/stage3_prepare_concrete.log) and
[`stage3_krun_concrete.log`](evidence/stage3_krun_concrete.log).

### Proof definition and all positive target claims

The proof definition was freshly compiled:

```text
timeout 300 kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

This exited 0; see
[`stage3_kompile_proof.log`](evidence/stage3_kompile_proof.log).

The unmodified candidate spec was then proved as a whole:

```text
timeout 300 kprove spec-original.k \
  --definition verification-kompiled --spec-module SPEC
```

It exited 0 and printed `#Top`; see
[`stage3_kprove_all_original.log`](evidence/stage3_kprove_all_original.log).

For independent selection, I added labels only (no semantic change) to the
scratch spec and ran all seven claims separately. Each exited 0 and printed
exactly one `#Top`:

| Claim label | Result |
|---|---|
| `SPEC.pythagorean-c` | `#Top`, exit 0 |
| `SPEC.pythagorean-b` | `#Top`, exit 0 |
| `SPEC.pythagorean-a` | `#Top`, exit 0 |
| `SPEC.nonpositive-a` | `#Top`, exit 0 |
| `SPEC.nonpositive-b` | `#Top`, exit 0 |
| `SPEC.nonpositive-c` | `#Top`, exit 0 |
| `SPEC.positive-none` | `#Top`, exit 0 |

The per-claim exact commands and outputs are the seven
`evidence/stage3_kprove_*.log` files; the compact check is
[`stage3_proof_status_summary.log`](evidence/stage3_proof_status_summary.log).
There are no helper or loop claims.

Stage 3 therefore passes as verification under the candidate's submitted
theory. A fresh `#Top` does not resolve what program that theory executes.

## 4. Adequacy and real-program pinning

### Claim meanings, satisfiability, and result constraint

Every claim starts from the full pristine MPY configuration: module environment
0, empty module map with the fixed builtins parent, next scope 1, empty heap,
empty stack, `noRet`, `NoExc`, and exit code 0. Every destination fixes the
`<k>` result to a literal `true` or `false`; there is no free result variable,
tautological `ensures`, or one-way implication.

| Claim | Plain-language precondition | Postcondition | Satisfying witness |
|---|---|---|---|
| `pythagorean-c` | all positive and `a²+b²=c²` | returns `true` | `(3,4,5)` |
| `pythagorean-b` | all positive and `a²+c²=b²` | returns `true` | `(3,5,4)` |
| `pythagorean-a` | all positive and `b²+c²=a²` | returns `true` | `(5,3,4)` |
| `nonpositive-a` | `a <= 0` | returns `false` | `(0,4,5)` |
| `nonpositive-b` | `a > 0` and `b <= 0` | returns `false` | `(3,0,5)` |
| `nonpositive-c` | `a > 0`, `b > 0`, and `c <= 0` | returns `false` | `(3,4,0)` |
| `positive-none` | all positive and no equality holds | returns `false` | `(1,2,3)` |

[`precondition_witnesses.py`](evidence/precondition_witnesses.py) checks every
precondition and substitutes the witness into both Python implementations. All
seven agree with the claimed literal; see
[`stage4_precondition_witnesses.log`](evidence/stage4_precondition_witnesses.log).
The three short-circuit non-positive cases plus the four positive cases cover
all integer triples. The positive equality cases cannot overlap for strictly
positive integers.

### Decisive failure: the submitted program is not in the claim execution

`verification.k` requires only `reference-semantics/semantics.k`. Neither it
nor `spec.k` requires, parses, loads, or otherwise refers to `solution.mpy`.
The only `solution.mpy` match is prose in a comment. Instead:

1. `#rightAngleTriangleBody` is equated to a handwritten `Stmts` term.
2. `#rightAngleTriangleClosure` constructs a closure over that term.
3. `#runRightAngleTriangle` rewrites directly to a call of that closure.

Consequently the claim never executes the submitted
`Module(FuncDef(...))`, never uses the fixed `#loadAll` rule on the submitted
module, and never obtains the function binding through the submitted
`FuncDef`. The dependency search and hashes are in
[`stage4_dependency_check.log`](evidence/stage4_dependency_check.log).

The handwritten body happens to mirror the current submitted body, but there
is no bridge-free connection claim and no generated dependency tying that K
term to `solution.mpy`.

I tested body sensitivity in a separate clean scratch directory:

- Replaced `solution.py` with `right_angle_triangle(...): return False`.
- Regenerated `solution.mpy` with the trusted translator; it was byte-identical
  to the stored mutant. See
  [`stage4_pinning_mutant_translation.log`](evidence/stage4_pinning_mutant_translation.log).
- Confirmed mutant Python returns `False` on `(3,4,5)`.
- Left the submitted `verification.k` unchanged and freshly compiled it
  against a fresh trusted-semantics copy; compilation exited 0.
- Proved `SPEC.pythagorean-c` in that fresh definition. It still exited 0 and
  printed `#Top`, asserting `true` for the Pythagorean case.

The preparation, build, and proof records are
[`stage4_pinning_mutant_prepare.log`](evidence/stage4_pinning_mutant_prepare.log),
[`stage4_pinning_mutant_build.log`](evidence/stage4_pinning_mutant_build.log),
and
[`stage4_pinning_mutant_proof.log`](evidence/stage4_pinning_mutant_proof.log).
The concrete false-conclusion witness for attributing this theorem to the real
artifact is `(3,4,5)`: the translator-identical mutant program returns
`False`, while the unchanged proof concludes `true`.

This establishes body insensitivity to the real generated program. Stage 4
fails even though the current handwritten duplicate is extensionally
consistent with the current artifact.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[`k_rule_inventory.py`](evidence/k_rule_inventory.py) scanned every trusted
semantics K file plus `verification.k` and `spec.k`, retaining source locations,
attributes, a normalized declaration, and a declaration hash. The exhaustive
941-record ledger is
[`stage5_exhaustive_inventory.log`](evidence/stage5_exhaustive_inventory.log).
It comprises 928 fixed supplied-semantics declarations/rules, six local
verification declarations/rules, and seven claims.

Compact per-file counts are:

| File/module | Syntax | Rules | Context/config/claims |
|---|---:|---:|---:|
| `assert.k` | 0 | 3 | 0 |
| `bool.k` | 0 | 13 | 1 context |
| `builtins.k` | 38 | 137 | 0 |
| `call.k` | 3 | 21 | 0 |
| `comprehension.k` | 3 | 7 | 0 |
| `concrete.k` | 5 | 16 | 0 |
| `controls.k` | 3 | 34 | 0 |
| `core.k` | 37 | 46 | 1 configuration |
| `dict.k` | 12 | 28 | 0 |
| `float.k` | 34 | 121 | 0 |
| `functions.k` | 4 | 15 | 0 |
| `int.k` | 1 | 16 | 0 |
| `iter.k` | 1 | 0 | 0 |
| `list.k` | 5 | 27 | 0 |
| `methods.k` | 27 | 75 | 0 |
| `operators.k` | 0 | 10 | 2 contexts |
| `range.k` | 2 | 6 | 0 |
| `set.k` | 6 | 12 | 0 |
| `sort.k` | 6 | 19 | 0 |
| `str.k` | 5 | 28 | 0 |
| `subscript.k` | 15 | 40 | 2 contexts |
| `syntax.k` | 16 | 0 | 0 |
| `tuple.k` | 4 | 21 | 0 |
| `verification.k` | 3 | 3 | 0 |
| `spec.k` | 0 | 0 | 7 claims |

`semantics.k` itself is the module/import assembly and has no local operational
rule. The ledger enumerates all `[function]`, `[total]`, `[concrete]`,
`[owise]`, priority, symbol/no-evaluator, strictness, and ordinary-rule records.
There are no local or fixed `[simplification]` rules and no `[functional]`
declarations. A focused source listing of all special attributes and the used
construct rules is in
[`stage5_special_attributes.log`](evidence/stage5_special_attributes.log).

### Construct-to-semantics map and execution review

The actual `solution.mpy` uses `Module`, `FuncDef`, `Params`, `If`, `Compare`,
`CmpOp`, `Name`, `Int`, `Return`, `Bool`, and integer `BinOp`.

- `Module` is declared in `syntax.k`; `core.k` configuration starts with
  `#loadAll($PGM)`, and rules expand `Module(SS)` and sequence statements.
- `FuncDef` and `Params` are declared in `syntax.k`; `functions.k` installs a
  `closureVal` in the current scope.
- `Name` lookup walks the current scope and parent chain via `#look`.
- `Int` and `Bool` literals cool to K `Int` and `Bool`.
- `BinOp` is left-to-right by `[seqstrict(2,3)]`; `operators.k` dispatches to
  the `int.k` equations. The used `+Int` and `*Int` rules are exact unbounded
  integer arithmetic.
- `Compare` evaluates left then right through its two contexts and dispatches
  `<=` and `==` to the exact K integer predicates.
- `If` evaluates only its condition and dispatches through `truthy`; K booleans
  have their ordinary truth values.
- `Call` evaluates callee then arguments left-to-right, creates a new scope,
  binds `a,b,c`, pushes a frame, executes the body, and restores the caller on
  `#pop`.
- `Return` evaluates its expression, discards the remaining function-body
  continuation, records the return, and pops precisely the call frame. For this
  straight-line function there is no heap allocation, mutation, exception,
  output, loop, or helper claim.

The claims pin all visible cells at entry and destination, so the call must
restore environment, scopes, scope allocator, heap, heap allocator, stack,
return state, exception, and exit code.

The important mismatch is that the proof path starts at
`#runRightAngleTriangle`, not at `#loadAll(solution.mpy)`. Therefore the
otherwise applicable `Module` and `FuncDef` rules for the real artifact are
bypassed.

### Local proof extensions

The six local inventory entries are K0929–K0934 in the exhaustive ledger:

1. `#rightAngleTriangleBody : Stmts` is a nullary `[function]` with one exact
   equation to a fixed AST. As an equation about the newly introduced constant
   it is deterministic, terminating, and non-overlapping. It is a definitional
   duplicate, not a proved connection to the submitted program.
2. `#rightAngleTriangleClosure : Val` is a nullary `[function]` with one exact
   equation constructing parameter names, the duplicate body, and defining
   environment 0. It is deterministic and non-overlapping.
3. `#runRightAngleTriangle(A,B,C)` has one ordinary rule expanding in place to
   `Call(#rightAngleTriangleClosure,A,B,C)`. It preserves any surrounding
   continuation and does not itself fabricate a return, mutate state, or skip
   the fixed call semantics.

There are no proof-local totality, priority, simplification, opaque, oracle, or
answer-encoding rules. I found no concrete witness making any of these three
equations false as equations over their newly introduced symbols, so I do not
label them logically unsound. The narrower and decisive defect is the absent
connection to the real artifact. The mutant witness above proves that the
candidate's attribution of the resulting theorem to `solution.mpy` is false.

### Fixed-semantics trust and unused rules

All 928 fixed entries are byte-for-byte the mandated trusted supplied
semantics. I reviewed their inventory for overlaps, priorities, state-changing
rules, totality markers, and opaque terms. The used integer/call/control path
has guarded, sort-specific equations with no conflicting right-hand sides.
Priorities on reference dereference/cell rules do not match the integer-only,
heap-empty path.

The fixed opaque/symbol boundary consists of the float primitives
`intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `floorFI`, `toF`,
`ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`,
`divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`, and `sqrtF`, plus
`sortVS`, `sortKeyVS`, and `md5hexCodes`. Their concrete legs or external
interpretations are part of the supplied semantics trust boundary. No submitted
program term, branch, result, or claim reaches any of them. The many unused
collection/string/builtin rules likewise cannot match the concrete syntactic
sorts on this program's path. I found no false-conclusion witness involving a
fixed rule on the intended path and therefore do not assert a semantics
unsoundness.

## 6. Fresh non-vacuity test

No candidate `spec-vacuity.k` was present. I authored
[`evidence/spec-vacuity.k`](evidence/spec-vacuity.k), changing the
`pythagorean-c` destination from `true` to `false` while keeping its satisfiable
precondition. `(3,4,5)` satisfies the precondition, and both Python
implementations return `True`.

First:

```text
timeout 120 kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY --dry-run
```

exited 0 and emitted the backend command, establishing that the mutation
parsed and built. See
[`stage6_vacuity_dry_run.log`](evidence/stage6_vacuity_dry_run.log).

Then:

```text
timeout 180 kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

exited 1 with `WarnStuckClaimState`. The residual has `true ~> .K` in the
`<k>` cell while the destination requires `false`; the positive/equality
constraints remain visible. This is the expected unmet result obligation, not
a parser error, timeout, unrelated crash, or unreachable mutation. See
[`stage6_vacuity_proof.log`](evidence/stage6_vacuity_proof.log).

Stage 6 passes: the proof discriminates true from false for its handwritten
duplicate program. Non-vacuity does not repair Stage 4's missing artifact
connection.

## 7. Proven versus assumed accounting

### What the successful K proof establishes

Conditional on K v7.1.337 and the trusted supplied MPY semantics, starting from
the specified pristine cells, calling the proof-local closure whose body is
`#rightAngleTriangleBody`:

- returns `true` for each positive integer Pythagorean permutation;
- returns `false` in the three ordered non-positive cases;
- returns `false` for positive integers satisfying none of the equalities; and
- restores every framed state cell in the claim.

The false mutation shows these returned literals are genuinely constrained.

### Assumptions and boundaries

| Boundary | Dependents | Assessment |
|---|---|---|
| K compiler, Haskell/LLVM backends, solver, and K integer primitives | all reconstructed runs | Normal machine-checking trust boundary; versions and outputs recorded |
| `/reference/reference-semantics` | all concrete and symbolic MPY execution | Mandated fixed semantics for this mode; candidate copy has exact integrity |
| Trusted `py2mpy.py` | link from current `solution.py` to current `solution.mpy` | Deterministic byte identity established for both original and pinning mutant |
| Handwritten `#rightAngleTriangleBody` equals the submitted artifact's body | every target claim | Illegitimate theorem bridge: no import, parsing dependency, or K connection theorem; real-artifact mutant leaves proof unchanged |
| Fixed float/sort/MD5 opaque symbols | only programs that reach those operations | Explicit supplied-semantics boundary; irrelevant to this integer-only proof |
| Differential comparison to canonical | implementation-to-reference evidence | Finite evidence only; zero positive-domain mismatches, non-positive divergences recorded |
| Pythagorean characterization of a positive right triangle | natural-language interpretation | Ordinary mathematical intent bridge, not a K geometry theorem |
| Integer-only formal domain | formal theorem scope | Narrower than untyped numeric Python behavior; floats are not proved |
| Partial-correctness interpretation | theorem wording | The reachability proof is not a general Python totality theorem, although this modeled straight-line call closes on all seven integer partitions |

Candidate prose, absent traces, concrete tests, and differential testing are not
used as substitutes for the K proof. The decisive issue is also not a missing
empirical test: it is that the successful reachability proof has the wrong
program identity. Under the required decision boundary, a sound,
result-constraining proof of a separately encoded program is still
`FAIL / NOT_LEGIT`.

The command logger, reviewer-authored scripts, exact statuses, bounded proof
outputs, and SHA-256 evidence index are preserved under
[`evidence/`](evidence/), with the index in
[`evidence_manifest.log`](evidence/evidence_manifest.log).

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
