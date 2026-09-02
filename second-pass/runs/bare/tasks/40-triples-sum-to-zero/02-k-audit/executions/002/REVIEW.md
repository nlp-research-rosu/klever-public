# Independent adversarial review: 40-triples-sum-to-zero

The reconstructed K proof closes and is internally result-constraining, but it
does not establish the full HumanEval source contract for the real submitted
Python program. A valid 1,001-element integer-list input makes the trusted
canonical implementation return `True` while `solution.py` raises
`RecursionError`; the candidate's generated K semantics instead returns
`True`. This is a material, reachable source-to-semantics gap on the
unrestricted contract domain. Under the benchmark-specific decision boundary,
the otherwise sound-but-limited theorem is `FAIL / NOT_LEGIT`, not
`CONCERNS / LEGIT`.

## 1. Input and provenance integrity

The launcher declares `record_layout = legacy-selected-stage1`,
`condition = bare`, and `semantics_mode = GENERATED_SEMANTICS`. I used the
launcher `container_paths`, not the host provenance paths.

All records required for this layout are readable real files, not symlinks:
`/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`, `/task.json`,
`/generation-result.json`, `invocation.json`, `metrics.json`,
`codex-last.txt`, `codex-output.log`, `prompt.txt`, and the structured trace.
The optional `usage.json` is present and was also inspected. Historical
runtime metrics are not required for this legacy layout.

The campaign lock is structurally equal to the `audit_campaign` block and its
SHA-256 equals the recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
Every launcher-recorded regular-file hash checked in
[provenance-check-complete.log](/audit-output/evidence/provenance-check-complete.log)
matches: run, task, result, invocation, canonical, prompt, translator,
metrics, usage, generation prompt, Codex final text, and Codex output.

The structured trace contains one regular JSONL file. Its content digest
matches the invocation/result records; all 183 lines parse, with one
`task_started` and one `task_complete` event. Its independently reconstructed
pipeline tree digest matches `usage.json`. The independently reconstructed
candidate pipeline-tree digest is
`fd2f20f017877ef8044dc75517b6fcee2083f29831f901c1280de84fe166c0b8`,
matching both the invocation and generation-result workspace digests. The
launcher also records separate launcher-level tree-digest fields
(`f7c197...` and `d57fcc...`); the prompt does not specify that digest
encoding, so I recorded those values without conflating them with the
pipeline-tree algorithm.

Candidate `prompt.py` and `py2mpy.py` are byte-identical to the trusted
mounted copies. There are no symlinks under `/candidate`, `/reference`, or
`/generation-evidence`. As required for `GENERATED_SEMANTICS`,
`/reference/reference-semantics` is absent. Thus there is no infrastructure
breach and no hidden reference semantics was sought or used.

The generation trace and prior `KPROVE_PASSED` marker were treated only as
untrusted claims. Candidate `.kbuild`, `.kprove`, and `__pycache__` content was
not reused.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The trusted prompt and canonical define:

> For any list of integers, return `True` iff there are three distinct list
> positions whose values sum to zero; otherwise return `False`.

The duplicate-value positive example `[1, 3, -2, 1]` confirms that
“distinct” means distinct positions, not three pairwise-distinct values.
There is no list-length bound.

The candidate uses an extensionally sensible recursive decomposition:
`_has_pair_sum(first, rest)` scans successive second positions and searches
only the later suffix for the third value; the entry point scans successive
first positions. This preserves distinct indices.

### Translator identity

Running the trusted translator on the scratch copy of `solution.py` regenerated
`solution.mpy` byte-for-byte. Both files hash to
`b863637652ba42e8c3117b599f9a96abaa4ccfbd8cac616807adf0b2a54593c3`;
see
[translator-regeneration.log](/audit-output/evidence/translator-regeneration.log).

### Independent differential evidence

[differential_test.py](/audit-output/evidence/differential_test.py) imports the
trusted canonical and candidate through separate explicit paths. It covers:

- all five documented examples;
- empty, lengths one/two/three, duplicate, zero, hit/miss, late-hit, and
  arbitrary-precision-integer boundaries;
- all lists of lengths 0 through 6 over values `-3..3` (137,257 cases); and
- 2,000 deterministic generated lists of lengths 0 through 18.

Those 139,275 ordinary cases have zero mismatches. The same test then uses the
valid contract input

```python
[10**9, 1, -1, 0] + [2] * 997
```

of length 1,001. The canonical returns `True` from positions `(1, 2, 3)`.
Before the candidate advances beyond its first element,
`_has_pair_sum` exceeds CPython's recursion limit and raises
`RecursionError: maximum recursion depth exceeded in comparison`. The
differential command therefore correctly exits 1; see
[differential-test.log](/audit-output/evidence/differential-test.log).

This is a material behavior divergence on the stated domain, not a different
but equivalent algorithm. Raising the process recursion limit only moves the
finite boundary; the contract itself is unrestricted.

## 3. Clean proof reconstruction

I copied only source artifacts into `/tmp/audit-work/candidate-src`. Fresh
output directories were used; candidate compiled definitions and caches were
ignored.

The available toolchain is K `v7.1.293` and Python `3.10.12`; see
[tool-versions.log](/audit-output/evidence/tool-versions.log).

Fresh builds both exit 0:

- LLVM semantics:
  [kompile-semantics-llvm.log](/audit-output/evidence/kompile-semantics-llvm.log)
- Haskell verification definition:
  [kompile-verification-haskell.log](/audit-output/evidence/kompile-verification-haskell.log)

The three positive claims are circularity-dependent, so they were tested in
dependency-preserving layers:

1. `pair-correct` alone: exit 0 and `#Top` in
   [kprove-pair-correct.log](/audit-output/evidence/kprove-pair-correct.log).
2. `pair-correct` plus `triples-correct`, excluding only `program-correct`:
   exit 0 and `#Top` in
   [kprove-pair-and-triples.log](/audit-output/evidence/kprove-pair-and-triples.log).
3. All three claims, including the target program claim: exit 0 and `#Top` in
   [kprove-all-positive.log](/audit-output/evidence/kprove-all-positive.log).

Exploratory `--claims` commands that removed needed earlier circularities were
not used as proof evidence; they are identified in
[invalid-filter-diagnostic-note.md](/audit-output/evidence/invalid-filter-diagnostic-note.md).

The freshly compiled LLVM semantics agrees with both Python implementations on
14 normal and boundary cases, including empty lists, all prompt examples,
duplicate values, large integers, and late hits; see
[concrete-semantics-test-fixed.log](/audit-output/evidence/concrete-semantics-test-fixed.log).
An initial reviewer regex error is preserved separately in
`concrete-semantics-test.log` and has no evidentiary value.

At the length-1,001 witness, however, fresh K execution exits 0 with `true`,
matching the canonical while the submitted Python raises `RecursionError`;
see
[stress-semantics-test.log](/audit-output/evidence/stress-semantics-test.log).
This directly locates the material divergence in the Python-to-generated-
semantics bridge.

## 4. Adequacy and real-program pinning

### Claims in plain language

- `pair-correct` has no explicit precondition. For every mathematical integer
  `FIRST`, finite `Ints` suffix `IS`, arbitrary continuation `RESTK`, and
  arbitrary unchanged auxiliary cells, invoking the exact `_has_pair_sum`
  binding returns `hasPairWith(FIRST, IS)` and preserves `RESTK`.
- `triples-correct` likewise has no explicit precondition. Invoking the exact
  entry binding on any finite `Ints` list returns `hasZeroTriple(IS)` and
  preserves the arbitrary continuation and other cells.
- `program-correct` starts from the quoted `solutionProgram`, empty function
  and environment maps, input `VList(IS)`, and `noResult`. It requires the
  computation to be consumed, installs exactly `solutionFunctions`, and
  constrains the final result to
  `result(VBool(hasZeroTriple(IS)))`.

Every precondition is satisfiable. Examples are `IS = .Ints` and
`IS = 1 ; 3 ; -2 ; 1 ; .Ints`, with `RESTK = .K` for helper claims and any
well-sorted values for the framed cells.

### Exact term and result constraint

The trusted-regenerated `solution.mpy` constructor has the same two function
bindings and bodies as `solutionProgram`. The reviewer-authored
[pinning-spec.k](/audit-output/evidence/pinning-spec.k) places the full
trusted-translator constructor on the right of `solutionProgram`; it closes
with `#Top` in
[kprove-pinning-fixed.log](/audit-output/evidence/kprove-pinning-fixed.log).
The `WarnTrivialClaim` is expected here: K's function simplifier normalized
the quoted constant and the full constructor to the same term. A first attempt
at a cell-free functional claim was rejected as unsupported and is preserved
in `kprove-pinning.log`; it is not evidence.

The claim does not merely mention an external file: `solutionProgram` expands
inside the `<k>` term that is actually executed. `solutionFunctions` contains
the same bodies used by the helper circularities. A material mutation of the
executed `pairBody` success branch from `True` to `False` builds successfully
but makes the proof fail on the pair obligation with a meaningful residual;
see
[body-mutation-diff.log](/audit-output/evidence/body-mutation-diff.log),
[kompile-body-mutation.log](/audit-output/evidence/kompile-body-mutation.log),
and
[kprove-body-mutation.log](/audit-output/evidence/kprove-body-mutation.log).

The returned value is not free or tautological. Ground substitutions for
empty, positive-example, and negative-example inputs reduce respectively to
`false`, `true`, and `false` in
[kprove-ground-summaries.log](/audit-output/evidence/kprove-ground-summaries.log),
matching both Python implementations on those inputs.

Thus the immutable K theorem pins the regenerated constructor and constrains
its K result. Its inadequacy is instead that the generated semantics does not
preserve an actual exceptional behavior of the Python program on part of the
source-contract domain.

## 5. Rule-by-rule static soundness review

### Complete local declaration inventory

`semantic.k` has 17 local syntax sentences:

1. Source constructors: `Program`, `Stmts`, `Stmt` (`FuncDef`, `If`,
   `Return`), `Params`, `Ids`, `Exprs`, `CmpOps`, `Expr` (`Bool`, `Int`,
   `Name`, `UnaryOp`, `BinOp`, `Subscript`, `Slice`, `Compare`, `Call`),
   `CmpOp`, and `Bound`.
2. Runtime constructors: `Ints`, `PyVal` (`VInt`, `VBool`, `VList`),
   `Result`, `Fun`, the `Value` extension of `Expr`, and `KItem`.
   The `KItem` productions are `load`, `start`, `eval`, `unaryK`,
   `binLeftK`, `binRightK`, `subscriptLeftK`, `subscriptRightK`,
   `compareLeftK`, `compareRightK`, `call1K`, `call2LeftK`,
   `call2RightK`, `invoke1`, `invoke2`, `exec`, `ifK`, and `finish`.
3. One local total function declaration:
   `memberInt(Int, Ints) [function, total]`.

`verification.k` has four syntax sentences: the nullary functions `pairBody`,
`tripleBody`, `solutionProgram`, and `solutionFunctions`, plus total functions
`hasPairWith(Int, Ints)` and `hasZeroTriple(Ints)`.

There are no local `functional`, `simplification`, `concrete`, priority, or
opaque result-bearing declarations. Free data/continuation constructors are
ordinary syntax, not oracles. There are no generated helper K files beyond
`semantic.k`, `verification.k`, and `spec.k`. The lexical inventory with exact
line locations is in
[local-declaration-inventory.log](/audit-output/evidence/local-declaration-inventory.log).

The configuration has exactly the material state modeled here: `<k>`,
`<funs>`, `<env>`, `<input>`, and `<result>`. The program has no assignment,
heap mutation, I/O, or user-visible allocation. What is missing materially is
an exception/recursion-budget component.

### All 39 semantic rules

The following identifiers account for every ordinary rule in `semantic.k`:

| Rules | Source lines | Role and finding |
|---|---:|---|
| S1–S5 | 81–93 | Module loading, function-map installation, hard-coded entry start, and final-result capture. They preserve all material cells and are correct for the exact two-definition module. |
| S6–S9 | 95–98 | Runtime value/literal evaluation and environment lookup. Correct for the bound names reached by the submitted term; a missing binding visibly gets stuck rather than being fabricated. |
| S10–S13 | 100–103 | Left-to-right unary evaluation and `not` on empty/nonempty lists or Booleans. Correct for every unary operand reached by the program. |
| S14–S17 | 105–110 | Left-to-right binary evaluation, integer subtraction, and integer addition. Only subtraction is used; both arithmetic equations are ordinary unbounded-integer mathematics. |
| S18–S22 | 112–118 | Left-to-right subscript evaluation, index 0, the exact `[1:]` slice, and suffix construction. Correct on the submitted AST, but globally over-broad as detailed below. |
| S23–S27 | 120–130 | Left-to-right comparison, integer-list membership, and the two exhaustive `memberInt` equations. The empty/cons guards are disjoint, cover all `Ints`, and recursive descent is structural. |
| S28–S34 | 132–147 | One/two-argument call evaluation, named function lookup, parameter binding, and invocation. Argument order, binding, caller continuation, and environments are preserved for the exact program. These rules permit unbounded recursive invocation and omit CPython's reachable `RecursionError`, which is the material used-path gap. |
| S35–S39 | 149–159 | Return, `if` evaluation, true-return branch, false fall-through, and an empty-body default. S35–S38 exactly cover both `If(... Return(...), empty else)` shapes in the program and preserve return control. S39 is unreachable from the submitted translated functions; as a general Python model its `false` default would not represent implicit `None`, but no valid submitted path relies on it. |

All constructs actually used by `solution.mpy` map to rules: `Module` and
`FuncDef` to S1–S3; function entry/finish to S4–S5; literals/names to S6–S9;
`not` to S10–S13; subtraction to S14–S16; index 0 and slice `[1:]` to
S18–S22; `in` to S23–S27; one/two-argument calls to S28–S34; and
`Return`/`If` to S35–S38. No used constructor is silently fabricated or
left unmodeled.

S21–S22 encode the slice as the same intermediate `VInt(1)` used by a literal
integer index. Consequently the valid translated expression `l[1]` is
misinterpreted as `l[1:]`. The concrete false-conclusion witness
[subscript-one.py](/audit-output/evidence/subscript-one.py) is translated
byte-for-byte to
[subscript-one.mpy](/audit-output/evidence/subscript-one.mpy); on `[10,20,30]`
Python returns integer `20`, while this semantics returns
`VList(20 ; 30 ; .Ints)`. Exact commands and results are in
[subscript-overbreadth-witness.log](/audit-output/evidence/subscript-overbreadth-witness.log).
This proves the reusable generated semantics is not sound for all syntax it
admits. It does not by itself falsify the target theorem because the
mechanically pinned submitted term contains integer index `0` and slice
`[1:]`, never integer index `1`.

The used-path semantics gap has a target-program witness: S28–S34 keep
invoking recursively on the length-1,001 valid input until K returns `true`,
whereas the actual submitted Python terminates exceptionally. This is not
attributed to a globally false arithmetic equation; it is the narrower,
concrete omission of a reachable exceptional control effect.

### All eight verification rules and three claims

| Rules | Source lines | Class and finding |
|---|---:|---|
| V1–V4 | 13–68 | Definitional summaries expanding `pairBody`, `tripleBody`, `solutionProgram`, and `solutionFunctions`. They quote, rather than bypass, the exact executed constructor. Each nullary function has one unguarded defining equation and no overlap. |
| V5–V6 | 74–76 | `hasPairWith`: empty is false; on `J ; IS`, check whether `-I-J` occurs strictly later, then recurse on the shorter suffix. Guards are structural, exhaustive, disjoint, and descending. |
| V7–V8 | 78–80 | `hasZeroTriple`: empty is false; on `I ; IS`, check a later pair and recurse on the shorter suffix. Again exhaustive, disjoint, and descending. |

The equations V5–V8 follow the ordinary index decomposition
`i < j < k`; they do not encode a candidate-specific answer. The only
result-bearing summaries are fully defined total functions. There is no
fresh/opaque symbol, oracle, operational bridge, priority preemption,
simplification lemma, or overlapping equation.

The three `spec.k` claims are reachability circularities, not semantic rewrite
rules. Helper LHS terms match exact invocation/binding/body states,
quantify over and preserve `RESTK`, and include every configuration cell.
The program claim executes the exact module and constrains `.K`, function
installation, and final result. The body-sensitivity and false-result probes
show that these claims are exercised.

## 6. Fresh non-vacuity test

The reviewer-authored
[spec-vacuity.k](/audit-output/evidence/spec-vacuity.k) preserves both helper
circularities but changes the program's result obligation to the opposite
Boolean:

```k
result(VBool(notBool hasZeroTriple(IS)))
```

The empty list satisfies the unchanged entry precondition. Real K execution
returns `false`, while the mutation demands `true`.

The mutation front-end builds successfully with exit 0 under `--dry-run`; see
[spec-vacuity-dry-run.log](/audit-output/evidence/spec-vacuity-dry-run.log).
The actual proof exits 1 with `WarnStuckClaimState` and the expected unmet
condition equating `hasZeroTriple(IS)` with its negation; see
[kprove-spec-vacuity.log](/audit-output/evidence/kprove-spec-vacuity.log).
This is a reachable failed result obligation, not a parser error, timeout, or
unrelated crash.

## 7. Proven versus assumed accounting

### What K proves

Conditional on the freshly compiled K definition, the successful reachability
proof establishes:

1. `_has_pair_sum(FIRST, IS)` returns exactly the recursive mathematical
   predicate `hasPairWith(FIRST, IS)`.
2. `triples_sum_to_zero(IS)` returns exactly `hasZeroTriple(IS)`.
3. Executing the exact regenerated constructor from the fresh K configuration
   consumes the computation and leaves
   `result(VBool(hasZeroTriple(IS)))` for every finite `Ints` term.
4. By the exhaustive suffix equations, `hasZeroTriple(IS)` is true exactly
   when three strictly increasing positions have values summing to zero.

No candidate prose, prior trace, differential test, or prior `#Top` substitutes
for these K reachability results.

### Trust and limitation ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K 7.1.293 compiler, Haskell/LLVM backends, and reachability implementation | All machine-checked results | Standard unavoidable tool trust; versions and fresh builds recorded. |
| Imported `BOOL`, `INT`, `STRING`, `MAP`, and `LIST` domain operations | Arithmetic, maps, Booleans, and membership | Acceptable low-level mathematical primitives; no task property is hidden in them. |
| Trusted `py2mpy.py` as the CPython-AST-to-constructor bridge | Program identity | Byte regeneration and source inspection support the exact constructor mapping, but translator correctness is not itself formally proved. |
| Equations `memberInt`, `hasPairWith`, `hasZeroTriple` | Final Boolean | Fully transparent, exhaustive structural definitions; accepted by rule review, not opaque assumptions. |
| Generated semantics as a Python behavior model | Meaning of the K theorem as a theorem about `solution.py` | **Materially inadequate on a used path.** It omits the reachable recursion exception and returns a Boolean on a valid input where real CPython raises. |
| S21–S22 subscript marker encoding | Reusability outside this exact AST | Empirically false for valid translated `l[1]`; off the submitted path, but an additional semantics-quality limitation. |
| Finite differential and concrete testing | Source/semantics empirical bridge only | Zero ordinary mismatches support tested cases; they do not prove universal equivalence. The stress mismatch positively refutes universal equivalence. |

Partial correctness does not require proving termination, but this finding is
not merely absence of a termination proof. At the witness, the actual Python
execution has a concrete exceptional outcome while the generated semantics
continues to a normal Boolean and the formal theorem describes that normal
result. Silently excluding that reachable exceptional behavior materially
narrows the HumanEval contract/real-program bridge.

### Gate and verdict accounting

- Kit Gate A, internal K theory: pass for the exact constructor; no proof-local
  oracle or execution bypass was found, body sensitivity holds, and the result
  mutation is rejected.
- Kit Gate B, HumanEval/source adequacy: fail. The source contract has no
  length bound, but the submitted implementation and generated semantics
  diverge materially at a valid finite input.
- Kit Gate C, auditability: the trust boundaries and all reviewer evidence are
  explicit and reproducible. This cannot repair Gate B.

Generic Kit terminology would describe the internally sound K theorem as
sound-but-limited. The benchmark prompt explicitly maps a material narrowing
of the HumanEval source-contract domain to `FAIL / NOT_LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
