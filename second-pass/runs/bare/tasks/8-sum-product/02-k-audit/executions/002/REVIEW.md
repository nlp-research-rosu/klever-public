# Independent adversarial review: 8-sum-product

## Overall finding

The candidate contains a legitimate, result-constraining partial-correctness
proof of the exact submitted generated program for arbitrary finite lists of
mathematical integers. A clean Haskell rebuild proves the sole positive claim
with `#Top`; a trusted regeneration pins the claim to `solution.py`; concrete K
execution agrees with both Python implementations; a body mutation and a false
postcondition mutation are both rejected for the expected result obligations.

The qualification is in the generated language semantics, not the theorem's
input domain. `semantic.k` erases every `ImportFrom` and resolves `sum` and
`prod` by textual name rather than modeled bindings. This specialization is
extensionally correct for the exact submitted module, whose `math.prod` import
is fixed and valid, but it is too broad as a reusable semantics. A preserved
witness proves the altered K program after changing the import to the invalid
`from typing import prod`, whereas Python raises `ImportError`. Because that
witness changes the submitted program and no allowed list input exposes a
wrong target result, I treat this as a non-fatal trust-boundary limitation and
not as a substituted-program or source-domain failure.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- problem `8-sum-product`, condition `bare`;
- `record_layout` `legacy-selected-stage1`;
- `semantics_mode` `GENERATED_SEMANTICS`;
- `mount_reference_semantics: false`; and
- complete input provenance.

All launcher-required files for that layout are present, readable real regular
files: `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
`/task.json`, `/generation-result.json`,
`/generation-evidence/invocation.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, and `prompt.txt`. The optional `usage.json` is present and
was inspected. The structured trace contains one real JSONL file; no required
mount or inspected tree contains a symlink. Historical
`runtime-metrics.json` is absent, as permitted for this legacy layout.
`legacy-metrics.json` and `legacy-run-input.json` were also inspected.

The audit campaign object is exactly equal to
`/audit-campaign-lock.json`. Its independently computed SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
the value recorded in `/audit-input.json`. The lock fixes K/pyk `7.1.293`,
the Kit commit and skill tree, audit image, prompt hash, and campaign ID.

The independently computed SHA-256 values for the run manifest, task manifest,
stage result, invocation, metrics, usage, generation prompt, Codex output, and
Codex final message all equal their recorded values. The sole trace file is
`39ecf7eae725daae0004a7e698818f89c69468e804c132ecbdf6179500bdbde5`,
matching both `invocation.json` and `generation-result.json`.

Using the repository's mounted `pipeline_contract.sha256_tree`, the candidate
tree is
`65461e9d38e144f5c6fb7e3d5b64c3b53d169b09bcbe625f8113e743f31b72a3`,
matching every `workspace_sha256` and `retained_workspace_sha256` in the
legacy generation records. The trace tree is
`cec680c8f28d47293343771d7935f29f656058f764b3616a2c3ad9bb588d76dd`,
matching `usage.json`'s `source_trace_sha256`. `audit-input.json` additionally
contains aggregate fields named `candidate_tree_sha256` and
`generation_codex_trace_sha256` computed by an undeclared second aggregation
procedure; those are not `pipeline_contract.sha256_tree` values. Since all
individual evidence hashes and the legacy layout's declared workspace/trace
digests match the mounted bytes, this is an auditability observation rather
than a missing, unreadable, or contradictory provenance mount.

`/candidate/prompt.py` is byte-identical to `/reference/prompt.py`, and
`/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`.
`/reference/reference-semantics` is absent and not a symlink, exactly as
required in generated-semantics mode. The candidate has every required proof
artifact: `solution.py`, `solution.mpy`, `semantic.k`, `verification.k`,
`spec.k`, and `prove.sh`.

The generation transcript and structured trace were treated only as untrusted
claims. They show the candidate authoring the submitted sources, encountering
and repairing parser errors, running three concrete examples, and reporting
one `#Top`. None of those prior build products or claims was reused.

Exact hashes, type checks, and commands are in
[`evidence/stage1-integrity.log`](evidence/stage1-integrity.log).
There is no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt's contract is: for a finite list of integers, return a
2-tuple containing the sum and product of every element. The empty list must
return `(0, 1)`.

The trusted canonical implementation initializes `sum_value = 0` and
`prod_value = 1`, traverses every element once, adds it to the sum, multiplies
it into the product, and returns the pair. The candidate instead returns
`(sum(numbers), math.prod(numbers))`. On lists of integers these standard
operations have the same identities and folds as the canonical loop, including
negative values, zero, and arbitrary-precision integers.

Running the trusted translator from the scratch copy on candidate
`solution.py` exits 0 and produces SHA-256
`d061e06bb15ef17ff9a7b6383328564ad6c802b1d3c8c027474caa9bb9bf3f1e`.
The submitted `solution.mpy` has the same hash and is byte-identical.

The independent differential script
[`evidence/differential_test.py`](evidence/differential_test.py) imports the
trusted canonical and generated entry points through separate module objects.
It checks the two documented examples, empty and singleton boundaries,
positive and negative identities, zero in the product, mixed signs, and a
large-integer case. It also exhaustively checks every list of length 0 through
5 over `[-3, -1, 0, 1, 2, 5]`, compares exceptions, and verifies neither
implementation mutates its input. All 9,340 cases agree with zero mismatches.
The exact deterministic scope is recorded in
[`evidence/differential-input-scope.md`](evidence/differential-input-scope.md);
commands and output are in
[`evidence/stage2-fidelity.log`](evidence/stage2-fidelity.log).

This finite test is supporting evidence, not the universal proof.

## 3. Clean proof reconstruction

All candidate source artifacts were copied to
`/tmp/audit-work/reconstruction-8-sum-product/candidate`. No candidate
`*-kompiled` definition or cache was copied or used.

The executable definition was freshly built with:

```text
kompile semantic.k --backend llvm --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/reconstruction-8-sum-product/concrete-kompiled
```

It exits 0. Fresh `krun` executions give:

| Input | K result |
|---|---|
| `[]` | `(0, 1)` |
| `[7]` | `(7, 7)` |
| `[-7]` | `(-7, -7)` |
| `[1,2,3,4]` | `(10, 24)` |
| `[-2,0,5]` | `(3, 0)` |
| `[10^12,-3,17]` | `(1000000000014, -51000000000000)` |

The trusted canonical and generated Python entry points return exactly the
same values for those inputs.

The proof definition was freshly built with:

```text
kompile verification.k --backend haskell --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/reconstruction-8-sum-product/proof-kompiled
```

It exits 0. `spec.k` contains one positive target claim. The independent run:

```text
kprove spec.k \
  --definition /tmp/audit-work/reconstruction-8-sum-product/proof-kompiled \
  --spec-module SUM-PRODUCT-SPEC
```

exits 0 and prints exactly `#Top`. Full bounded output is in
[`evidence/stage3-reconstruction.log`](evidence/stage3-reconstruction.log).

## 4. Adequacy and real-program pinning

There is one entry claim and no helper or loop claim.

Its precondition, stated plainly, is:

- `<k>` contains the exact submitted module constructor term;
- `<input>` is `PyList(IS)` for an arbitrary `IS:Ints`;
- `<functions>` is the empty map; and
- `<result>` is empty.

There is no `requires` clause and therefore no hidden length, sign, magnitude,
or non-emptiness restriction. `Ints` is the freely generated empty/cons
sequence of arbitrary K integers, so it covers every finite integer-list size,
not a bounded unrolling.

Its postcondition is:

- program execution consumes `<k>`;
- `<functions>` contains the exact registered `sum_product` closure;
- `<input>` is unchanged; and
- `<result>` is
  `PyTuple(PyInt(sumInts(IS)), PyInt(productInts(IS)))`.

The result is not fresh, existential, implied in only one direction, or
unconstrained. The recursive equations set empty sum/product to `0`/`1` and
nonempty sum/product to head plus/times the tail fold.

Satisfying initial states exist. For `IS = .Ints`, the claim predicts `(0,1)`,
which K and both Python implementations return. For
`IS = -2, 0, 5, .Ints`, it predicts `(3,0)`, again matching all three.

The reviewer script
[`evidence/pinning_check.py`](evidence/pinning_check.py):

1. regenerates `solution.mpy` with the trusted translator and checks byte
   identity;
2. extracts the initial `Module(...)` from the claim; and
3. parses the submitted and claim terms independently with
   `kast --sort Module --output json`.

Both constructor ASTs are identical. The claim therefore executes the actual
submitted function binding and body. The source term is manually embedded in
`spec.k` rather than generated automatically, which is a maintenance
observation only; identity is mechanically established for this immutable
candidate.

The separate body-sensitivity mutation changes the first executed component
from `sum(numbers)` to `prod(numbers)` and changes the destination closure in
parallel while retaining the intended result. `kprove` exits 1 with
`WarnStuckClaimState` and the unmet equality
`productInts(IS) = sumInts(IS)`. The concrete satisfying witness `[2,3]`
returns mutated `(6,6)` instead of required `(5,6)`. This confirms dependence
on the body actually executed by the claim, not merely on an external source
file. See [`evidence/stage4-adequacy.log`](evidence/stage4-adequacy.log).

## 5. Rule-by-rule static soundness review

The exhaustive local inventory is
[`evidence/rule-inventory.md`](evidence/rule-inventory.md). It enumerates every
sort and syntax production, configuration cell, function/total attribute, all
17 `MPY` rules, and the sole `VERIFICATION` function and equation. There are no
candidate-local opaque symbols, priorities, simplification rules, macros,
`functional` declarations, or helper K source files.

Construct coverage is complete:

- `Module` starts statement execution and the benchmark entry-point call.
- `ImportFrom` is consumed.
- `FuncDef`, `Params`, and the sole `Return` install the closure.
- `#invoke` selects that closure and evaluates its expression.
- `Name` uses the parameter map.
- `TupleExpr` constructs the pair.
- the two `Call` nodes select sum and product.
- `PyList`, `Ints`, and K `Int` represent the input and its elements.

The statement-list rules enforce left-to-right order. Function definition and
invocation preserve the active continuation and have the exact state footprint
needed by the target. Map lookup is valid on the single-parameter environment.
Tuple evaluation does not explicitly model Python's observable left-to-right
effect order, but the exact two calls are pure and total on the formal domain,
so no target behavior differs.

`sumInts` and `productInts` are total because their disjoint empty/cons rules
cover the complete `Ints` syntax and structurally descend. `sumValue` and
`productValue` convert those mathematical folds to `PyInt`. There are no
overlapping local equations. K arbitrary-precision `Int`, `+Int`, and `*Int`
match Python integer arithmetic on the source-contract domain.

`expectedSumProduct` is a definitional summary on the destination only. It
does not replace execution or introduce an oracle. Although the destination
and external-call semantics use the same folds, this is not circular: the
program body is independently executed through `FuncDef`, `#invoke`, `eval`,
and the two call rules, while the folds themselves have complete truthful
recursive equations that are precisely the mathematical meanings requested by
the contract.

The material limitation is binding and imports:

- `ImportFrom(_,_) => .K` accepts every module and imported-name list, checks
  neither import success nor binding, and updates no environment.
- `Call(Name("sum"),A)` and `Call(Name("prod"),A)` select external operations
  from textual spelling without checking the selected binding.

For a concrete false conclusion witness over those rules' full admitted syntax,
[`evidence/spec-import-binding-witness.k`](evidence/spec-import-binding-witness.k)
changes only the second import to `ImportFrom("typing","prod")`. K still proves
the universal result with `#Top`. The corresponding
[`evidence/python-import-binding-witness.py`](evidence/python-import-binding-witness.py)
exits 1 because `typing` has no `prod`. Exact commands and output are in
[`evidence/stage5-binding-witness.log`](evidence/stage5-binding-witness.log).

This witness establishes that `semantic.k` is not a faithful reusable semantics
for every source term its broad `ImportFrom` production admits. It does not
establish a false conclusion for the pinned real program: that program
contains the exact valid `from math import prod`, does not shadow either name,
and has no other import, state effect, exception, or control path. On this
fixed term, specializing the external bindings gives the same value and
control behavior for every intended input. I therefore record a generated-
semantics trust limitation rather than a material target-proof unsoundness.

## 6. Fresh non-vacuity test

The reviewer-authored
[`evidence/spec-vacuity-audit.k`](evidence/spec-vacuity-audit.k) preserves the
exact program, input domain, closure destination, and product result but
requires the returned sum to be `sumInts(IS) +Int 1`.

The empty list is a concrete satisfying witness: real execution returns
`(0,1)`, whereas the mutation requires `(1,1)`.

First, the mutation was passed through `kprove --dry-run`; it exits 0 and emits
the backend proof command, establishing that the distinct spec parses and
builds. The actual proof then exits 1 with `WarnStuckClaimState`. Its residual
is the expected unmet implication:

```text
sumInts(IS) +Int 1 #Equals sumInts(IS)
```

and its residual result cell contains the real
`(sumInts(IS), productInts(IS))`. The failure is not a parser error, missing
import, timeout, backend crash, or unreachable mutation. Exact evidence is in
[`evidence/stage6-nonvacuity.log`](evidence/stage6-nonvacuity.log).

## 7. Proven versus assumed accounting

### Formally established

Under the freshly built candidate definition, for every finite `IS:Ints`, the
exact regenerated module started with `PyList(IS)`, an empty function map, and
an empty result reaches a completed configuration whose result is:

```text
PyTuple(PyInt(sumInts(IS)), PyInt(productInts(IS)))
```

The closure installed in the function map is also constrained to the exact
submitted body. This is a universal reachability proof over arbitrary list
length and integer magnitude. It is a partial-correctness theorem; its formal
claim does not separately assert Python termination, though every local fold
equation structurally descends and all target operations terminate on finite
integer lists.

### Trust ledger

| Boundary | Effect and dependents | Assessment |
|---|---|---|
| K `7.1.293`, Haskell/LLVM backends, reachability engine | All compilation, execution, and proof closure | Standard accepted checker boundary; freshly rebuilt rather than candidate-provided |
| Imported K `INT`, `MAP`, collection syntax, `+Int`, `*Int` | Integer folds, environment update/lookup, all results | Accepted low-level mathematical/runtime primitives |
| Trusted `/reference/py2mpy.py` | Source-to-constructor identity | Launcher-trusted input; byte identity and constructor equality independently checked |
| `PyList(Ints)` versus Python `List[int]` | Formal input domain | Acceptable: all finite lists and arbitrary mathematical integers are covered; no material narrowing |
| Python built-in `sum` and `math.prod` contracts | Both returned components | Acceptable mathematical primitives on lists of integers; their candidate equations are exhaustive folds with correct identities |
| Exact import and name-binding specialization | Selection of `sum` and `math.prod` | Concerning but non-fatal for this immutable term: inspected exact source and Python execution support it; broad K rules fail the separate invalid-import witness |
| Candidate versus trusted canonical implementation | Alignment with HumanEval intent | Source inspection plus 9,340 differential cases; finite testing supports, but does not replace, the fold-based universal argument |
| Definition of “sum” and “product” by recursive folds | Human-facing postcondition | Ordinary mathematics, not an opaque or unconstrained oracle |

There are no opaque result symbols, empirical oracles inside the K proof,
proof-local operational bridges, auxiliary claims, or unproved simplification
lemmas. Candidate prose, prior `#Top`, generation traces, and differential
tests were not used as substitutes for the reconstructed K proof.

### Decision

The dynamic proof gate, real-program identity and body-sensitivity gate, intent
and unrestricted-domain gate, and non-vacuity gate pass. The result is
universally constrained and the candidate does not prove only examples,
bounded sizes, or a substituted body.

The generated semantics' import/name rules are broader than their valid
justification and make a false result claim possible for a different admitted
program term. Because the target claim mechanically fixes the valid real
module, no target input can reach that false binding case, and all material
target operations are otherwise modeled with truthful equations. This is a
documented non-fatal language-model/trust-boundary limitation, warranting
concerns while preserving legitimacy.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
