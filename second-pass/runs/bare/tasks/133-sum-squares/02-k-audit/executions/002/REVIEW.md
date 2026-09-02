# Independent adversarial review: 133-sum-squares

## Overall decision

The candidate contains a legitimate, result-constraining partial-correctness
proof of the submitted program over arbitrary finite lists of modeled numeric
values. The source was regenerated with the trusted translator, the generated
semantics and proof definition were rebuilt from source, the full spec and each
claim closed with fresh K 7.1.293 artifacts, and independent body, summary, and
postcondition mutations were rejected for the expected semantic reasons.

The verdict is `CONCERNS / LEGIT`, rather than an unqualified pass, because the
generated Mini-Python semantics hardwires the used `math.ceil` binding while
its generic import rule ignores import names, and because the bridge from
CPython finite numeric values to exact K rationals remains an audited
representation argument rather than a K theorem. These are non-fatal for this
immutable program and intended finite numeric-list domain. They do not bound
the list length, restrict the proof to examples, introduce an oracle, or enable
a false target conclusion.

Reviewer artifacts and exact command logs are indexed in
`/audit-output/evidence/README.md`.

## 1. Input and provenance integrity

### Launcher record and mode

`/audit-input.json` is readable and declares:

- problem `133-sum-squares`;
- condition `bare`;
- record layout `legacy-selected-stage1`;
- semantics mode `GENERATED_SEMANTICS`;
- `mount_reference_semantics: false`; and
- complete input provenance.

The object in `/audit-campaign-lock.json` is structurally identical to
`audit_input["audit_campaign"]`, and the lock's SHA-256 is the recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
The trusted `/reference/reference-semantics` tree is absent, as required in
generated-semantics mode. There is therefore no supplied or inferred hidden
semantics baseline.

For `legacy-selected-stage1`, I read and checked `/run.json`, `/task.json`,
`/generation-result.json`, `/generation-evidence/invocation.json`,
`metrics.json`, `codex-last.txt`, `codex-output.log`, `prompt.txt`, the complete
JSONL trace tree, and the present `usage.json`. The generation records were
treated only as historical claims. No current proof conclusion relies on their
reported `KPROVE_PASSED` marker or old `#Top`.

### File and tree checks

`/candidate`, `/generation-evidence`, and the trace tree are real directories.
All required records, trusted inputs, trace entries, and candidate artifacts
are real regular files; no candidate or evidence tree entry is a symlink or
unsupported node. Candidate proof artifacts present are:

`prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`, `semantic.k`,
`verification.k`, `spec.k`, and `prove.sh`.

The reviewer script `/audit-output/evidence/provenance_check.py` independently
recomputed every recorded flat-file digest. All matched, including:

- trusted canonical, prompt, and translator;
- candidate prompt and translator;
- run, task, result, and invocation manifests;
- generation metrics, usage, prompt, last message, and output log; and
- every evidence file named in `generation-result.json`, including the JSONL
  trace and both legacy records.

The candidate prompt is byte-identical to `/reference/prompt.py`; the candidate
translator is byte-identical to `/reference/py2mpy.py`.

The pipeline-native source-tree digest independently computed from the mounted
candidate is
`c55d53506754749ffbf456d12fe4bc4003d7174b03ab366dd7058330b802304f`,
matching both the stage invocation and stage result workspace digest. The
pipeline-native trace digest is
`5101d3c088699f384e476ba3b1ded41818bfd48785739284ee73e6cc8fff7c98`,
matching `usage.json`'s source-trace digest. The audit-input also contains
launcher-package aggregate fields `e044…` and `8a10…`; those are not the
pipeline tree encoding. I did not substitute one tree-hash encoding for the
other. Content identity is independently established by the complete
per-file chain and the generation-native aggregate chain.

Evidence: `evidence/logs/01-provenance.log` (exit 0).

**Stage 1 result: PASS.** No infrastructure breach or semantics-mode
contradiction was found.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

The trusted prompt requires `sum_squares(lst)` to take a list of numbers, round
each element upward with mathematical ceiling, square each rounded integer,
and return the sum. The trusted canonical implementation is:

```python
squared = 0
for i in lst:
    squared += math.ceil(i) ** 2
return squared
```

The submitted implementation imports `ceil`, initializes `total = 0`, stores
`ceil(number)` in `rounded`, adds `rounded * rounded`, and returns `total`.
The algorithm and order of operations agree with the canonical implementation.

### Trusted translation

In scratch, I ran:

```text
python3 /tmp/audit-work/reference/py2mpy.py solution.py > regenerated-solution.mpy
cmp -s regenerated-solution.mpy solution.mpy
```

The command exited 0. Thus the submitted `solution.mpy` is byte-identical to
trusted regeneration, not a hand-substituted K term.

Evidence: `evidence/logs/02-regenerate-mpy.log`.

### Independent differential test

`/audit-output/evidence/differential.py` independently imports the trusted
canonical and submitted entry points. It checks:

- all five documented examples;
- the empty list;
- zero and signed zero;
- negative and positive integer/ceiling boundaries;
- adjacent IEEE-754 values via `nextafter`;
- the smallest subnormal values;
- large integers around \(2^{53}\) and \(2^{100}\);
- booleans as Python integer subtypes; and
- 2,000 deterministic generated lists of length 0 through 12 containing
  finite integers and floats.

Result: 2,017 cases, 0 mismatches, exit 0.

Evidence: `evidence/logs/03-python-differential.log`.

**Stage 2 result: PASS.** No material divergence from the trusted implementation
was found.

## 3. Clean proof reconstruction

All builds and experiments used source-only copies under
`/tmp/audit-work/candidate`. No candidate-provided compiled definition or cache
was copied or used. `kup` is absent, but the independently installed live
toolchain is available; `kompile`, `krun`, and `kprove` all report K 7.1.293,
matching the campaign lock.

### Generated-semantics reconstruction and execution

Fresh concrete build:

```text
kompile semantic.k --backend llvm --syntax-module MPY-SYNTAX \
  --main-module MPY --output-definition semantic-fresh-kompiled
```

Exit 0; evidence: `evidence/logs/05-build-concrete.log`.

`/audit-output/evidence/concrete_cases.sh` then ran the trusted-regenerated
program through that definition and independently evaluated the same input with
the trusted Python canonical. All seven comparisons agreed:

| Case | Python | K `<k>` result |
|---|---:|---:|
| empty list | 0 | `intVal(0)` |
| `[1,2,3]` | 14 | `intVal(14)` |
| `[1.4,4.2,0]` | 29 | `intVal(29)` |
| `[-2.4,1,1]` | 6 | `intVal(6)` |
| `[-0.1,0.1,-1,1]` | 3 | `intVal(3)` |
| `[-1.1,-1.0,-0.9]` | 2 | `intVal(2)` |
| exact `[1/3,-1/3]` with a non-`ten` denominator | 1 | `intVal(1)` |

Evidence: `evidence/logs/06-concrete-cases.log` (exit 0).

### Proof-definition reconstruction

Fresh symbolic build:

```text
kompile verification.k --backend haskell --syntax-module MPY-SYNTAX \
  --main-module VERIFICATION \
  --output-definition verification-fresh-kompiled
```

Exit 0; evidence: `evidence/logs/07-build-proof.log`.

The original full proof command was:

```text
kprove spec.k --definition verification-fresh-kompiled --spec-module SPEC
```

It exited 0 and printed `#Top`; evidence:
`evidence/logs/08-kprove-all.log`.

I also copied each original claim verbatim into a labeled scratch spec so that
it could be run separately. The universal entry claim needs the exact loop
invariant as a circularity, so its isolated file contains only that companion;
the loop invariant is independently run alone.

| Claim run | Scope | Result |
|---|---|---|
| `09-kprove-claim-1` | ground `[1,2,3]` | exit 0, `#Top` |
| `10-kprove-claim-2` | universal entry + exact invariant companion | exit 0, `#Top` |
| `11-kprove-claim-3` | loop invariant alone | exit 0, `#Top` |
| `12-kprove-claim-4` | positive-fraction example | exit 0, `#Top` |
| `13-kprove-claim-5` | negative-fraction example | exit 0, `#Top` |

Evidence: corresponding numbered files in `evidence/logs/`.

**Stage 3 result: PASS.** Every positive claim closes in a clean,
source-reconstructed definition.

## 4. Adequacy and real-program pinning

### Claims in plain language

1. With empty initial function and environment cells, the exact submitted
   module called on `[1,2,3]` returns exactly `intVal(14)`.
2. With the same initial cells, for every finite `L:PList`, the exact module
   returns exactly `intVal(sumSquares(L))`.
3. If the active continuation is the real `number` loop followed by the real
   final `return total`, the current environment begins with
   `total = intVal(A)`, and the unprocessed values are `L`, then completing that
   control flow returns exactly `intVal(sumSquaresFrom(A,L))`.
4. The exact module returns `intVal(29)` on the encoded `[1.4,4.2,0]`.
5. It returns `intVal(6)` on the encoded `[-2.4,1,1]`.

There are no hidden `requires` clauses on the entry claims. Their preconditions
are satisfiable: the declared initial configuration with `.Map`, `.Env`, and,
for the universal claim, `L = nil`, is one witness. The loop precondition is
satisfied, for example, by `A = 0`, `L = nil`, `FUNS = .Map`, and
`REST = .Env`.

The postconditions constrain the observable `<k>` result to a concrete integer
or the fully defined `sumSquares` function. The right-hand variables for
`<functions>` and `<env>` intentionally existentially frame internal final
state; they do not free the return value. There is no implication-only
postcondition or tautology.

Concrete substitutions agree with both Python implementations and K execution:
`nil -> 0`, `[1,2,3] -> 14`, the two rational examples -> 29 and 6, and the
boundary witnesses in Stage 3 give the same results.

### Mechanical program identity

I parsed both `solution.mpy` and a surface rendering of the constructor body
from the entry claim with the fresh concrete definition:

```text
kast --definition semantic-fresh-kompiled --sort PyModule --output kore ...
```

Both normalized KORE files have SHA-256
`1266e7bdbbdeb740e00e15bea5823849dd7ad2b492a371dd62cff7f1c16fcb25`
and compare byte-identically. The explicit `.PyStmts` terminator in K claim
notation is the same list unit that the surface parser inserts.

Evidence: `evidence/logs/14-constructor-program-pinning.log`.

### Body sensitivity

I changed the multiplication in the *claim's executed program term* to
addition, retained input `[1,2,3]` and postcondition 14, and reran `kprove`.
The proof exited 1 with `WarnStuckClaimState`; the residual completed program
was `intVal(12)`. This is a direct body-sensitivity result, not a change to an
ignored external Python file.

Evidence: `evidence/logs/15-body-sensitivity.log`.

**Stage 4 result: PASS.** The theorem executes and is sensitive to the trusted-
regenerated submitted body.

## 5. Rule-by-rule static soundness review

### Construct and declaration inventory

Every source constructor in `solution.mpy` is represented:

| Submitted construct | Declaration | Execution path |
|---|---|---|
| module | `PyModule::Module` | `Module -> load` |
| `from math import ceil` | `PyStmt::ImportFrom` | used import is discharged; `ceil` is the named external primitive |
| function definition/parameter | `FuncDef`, `Params` | function stored in map, parameter bound by `callEntry` |
| assignment | `Assign` | RHS evaluated in old environment, new shadow binding |
| augmented `+=` | `AugAssign` | old target lookup plus integer RHS, new binding |
| `for` | `For` | list evaluation, constructor loop, per-element binding |
| return | `Return` | evaluates final expression |
| names and integer literal | `Name`, `Int` | environment lookup / `intVal` |
| function call | `Call` | used `Name("ceil")` case |
| multiplication | `BinOp("*",...)` | integer multiplication after ceiling |

All local syntax declarations are:

- `PyModule`: `Module(PyStmts)`;
- `PyStmts`: the empty-separated `PyStmt` list;
- `PyStmt`: `ImportFrom`, `FuncDef`, `Assign`, `AugAssign`, `For`, `Return`;
- `PyExpr`: `Name`, `Int`, `Call`, `BinOp`;
- `PosNat`: `one`, `next(PosNat)`, `ten`;
- `NumValue`: `intVal(Int)`, `ratVal(Int,PosNat)`;
- `PList`: `nil`, `cons(NumValue,PList)`;
- `PValue`: `NumValue`, `listVal(PList)`, plus the five function results below;
- `Function`: `function(String,PyStmts)`;
- `Env`: `.Env`, `binding(String,PValue) Env`;
- `KItem`: `load`, `loadStmt`, `callEntry`, `exec`, `loop`, `bind`; and
- verification-side `Int` functions `squareCeil`, `sumSquares`, and
  `sumSquaresFrom`.

Function declarations and attributes:

| Function | Attributes | Coverage/descent |
|---|---|---|
| `posInt` | `function,total` | disjoint `one`, `next`, `ten`; `next` structurally descends |
| `ceilInt` | `function` | disjoint and exhaustive `intVal`/`ratVal` |
| `evalExpr` | `function` | deliberately partial to modeled expression shapes; every used shape covered |
| `lookupValue` | `function` | head hit or guarded tail descent; actual lookups are bound |
| `ceilValue` | `function` | all `NumValue` inputs |
| `addValue` | `function` | modeled integer pair; all used operands are integers |
| `mulValue` | `function` | modeled integer pair; all used operands are integers |
| `squareCeil` | `function` | all `NumValue` inputs |
| `sumSquares` | `function,total` | every `PList` |
| `sumSquaresFrom` | `function,total` | disjoint `nil`/`cons`; structurally descends |

There are no local `[functional]`, `[simplification]`, `[concrete]`,
`[priority]`, `[owise]`, `[anywhere]`, `[opaque]`, macro, alias, or proof-local
operational rules. Constructor `[symbol]` declarations have no equations of
their own. The complete machine-generated scan is in
`evidence/logs/16-static-inventory.log`.

### Ordinary semantics rules

The following table decides every local rule:

| # | Rule(s) | Classification and review |
|---:|---|---|
| 1 | `posInt(one) => 1` | True constructor base. |
| 2 | `posInt(next(P)) => 1 + posInt(P)` | True positive-successor equation; strict structural descent. |
| 3 | `posInt(ten) => 10` | True named positive denominator. Cases 1–3 are disjoint and total. |
| 4 | `ceilInt(intVal(I)) => I` | Exact mathematical ceiling of an integer. |
| 5 | `ceilInt(ratVal(N,D)) => -((-N) divInt posInt(D))` | Exact ceiling identity because `posInt(D)>0` and K `divInt` is Euclidean division. Disjoint from rule 4. |
| 6 | `evalExpr(Int(I),_) => intVal(I)` | Faithful literal evaluation. |
| 7 | head `lookupValue(binding(X,V) _,X) => V` | Correct lexical value from the newest shadow binding. |
| 8 | guarded tail lookup when `X =/=String Y` | Correct, mutually exclusive with rule 7, structurally descends. |
| 9 | `evalExpr(Name(X),RHO)` | Delegates to the sound lookup rules. Used names are all bound. |
| 10 | `Call(Name("ceil"),E)` | Externally trusted primitive bridge; evaluates the used pure argument and applies the audited ceiling equation. It affects the result but is not opaque. |
| 11 | `BinOp("*",E1,E2)` | Correct multiplication of the used pure integer-valued operands. |
| 12 | `BinOp("+",E1,E2)` | Correct addition for the modeled pure operands; not needed by the submitted body but mathematically sound in its matched domain. |
| 13 | `ceilValue(V) => intVal(ceilInt(V))` | Correct wrapper; all modeled ceilings are integers. |
| 14 | `addValue(intVal(I1),intVal(I2))` | Exact unbounded integer addition. |
| 15 | `mulValue(intVal(I1),intVal(I2))` | Exact unbounded integer multiplication. |
| 16 | `Module(SS) => load(SS)` | Begins ordered module loading without changing state. |
| 17 | `load(.PyStmts) => .K` | Correct list base. |
| 18 | `load(S SS) => loadStmt(S) ~> load(SS)` | Preserves source statement order. |
| 19 | `loadStmt(ImportFrom(_,_)) => .K` | Over-broad as a reusable Python semantics, but the exact used import is `math.ceil`, whose binding is represented by rule 10. This is a documented concern, not a target-domain false rule. |
| 20 | `loadStmt(FuncDef(...))` map update | Stores the exact parameter and body under the exact function name. |
| 21 | `callEntry(V)` matching `"sum_squares"` | Selects the actual stored binding and binds its actual parameter. Resetting the local environment is correct at the only reachable top-level call site. |
| 22 | `exec(.PyStmts) => .K` | Correct statement-list base. |
| 23 | assignment rule | Evaluates RHS against the old environment, then shadows the target; correct for the used pure expressions. |
| 24 | augmented-add rule | Reads the current target and RHS from the old environment and installs their sum; correct for `total += rounded*rounded`. |
| 25 | `For` rule | Evaluates the iterable once, creates a loop over its list value, and preserves the exact suffix `exec(SS)`. |
| 26 | `Return` rule | Correct at the submitted final-return site: it discards trailing statements in the same `exec`, evaluates `total`, and has no call-frame state to unwind. It is not a complete general Python abrupt-control model. |
| 27 | empty-list loop | Consumes the loop and exposes the preserved suffix. |
| 28 | cons-list loop | Binds the head, executes the exact body, then recurs on the tail; gives one real semantic step before circularity reuse. |
| 29 | `bind` | Installs the per-iteration shadow binding; correct environment footprint. |

Evaluation order is adequate for the submitted pure expressions. The
configuration has exactly the needed state: `<k>`, function bindings, and local
environment. There is no heap, I/O, exception, output, or allocation behavior
used by the program. The environment shadow chain records assignments without
fabricating values. Function and loop control both preserve the actual
continuation.

### Verification-side equations

| # | Equation | Classification and review |
|---:|---|---|
| 30 | `squareCeil(V) => ceilInt(V) * ceilInt(V)` | Truthful mathematical definition; it does not replace execution. |
| 31 | `sumSquares(VS) => sumSquaresFrom(0,VS)` | Truthful initialization of the fold. |
| 32 | `sumSquaresFrom(A,nil) => A` | Truthful, disjoint base case. |
| 33 | `sumSquaresFrom(A,cons(V,VS)) => sumSquaresFrom(A+squareCeil(V),VS)` | Truthful fold step with structural descent. |

These four rules are definitional summaries, not operational bridges. The
program still executes module loading, the real function body, assignments,
every loop iteration symbolically through the invariant, the real
multiplication, and return. No rule rewrites the function call or loop directly
to a fresh answer.

I also rebuilt a separate definition with the opposite summary interpretation
`squareCeil(V) = ceil(V)^2 + 1`. The build succeeded, but the proof exited 1
with a semantic stuck state (the example summary became 17). Thus the summary
is execution-sensitive and not an arbitrary oracle.

Evidence: `evidence/logs/19-build-summary-mutation.log` and
`20-summary-opposite-interpretation.log`.

### Scope concerns, not target unsoundness

No reviewed rule has a false-conclusion witness for the immutable submitted
program on its intended finite numeric-list domain. Therefore I do not label
any rule materially unsound.

There are concrete *off-program* witnesses to the semantics' lack of general
Python reuse: an alternate module importing an unrelated function would still
have its import ignored, and a `Return` placed inside an alternate loop body
would not model Python call-frame unwinding. Neither pattern occurs in the
constructor-identical target body, and inputs cannot alter that body, function
map, or control continuation. These are the basis for `CONCERNS`, not a false
target theorem.

**Stage 5 result: PASS for target soundness, with documented non-fatal generated-
semantics scope concerns.**

## 6. Fresh non-vacuity test

I did not rely on a candidate-provided vacuity artifact. The reviewer-created
`/tmp/audit-work/candidate/spec-vacuity-audit.k` keeps:

- the original submitted constructor body;
- the satisfiable initial cells;
- input `[1,2,3]`; and
- a deliberately false result `intVal(15)` instead of `intVal(14)`.

First:

```text
kprove spec-vacuity-audit.k --definition verification-fresh-kompiled \
  --spec-module SPEC-VACUITY-AUDIT --dry-run
```

exited 0, establishing that the mutation parses and builds. The live proof then
exited 1 with `WarnStuckClaimState`. Its residual is the completed real program
at `intVal(14) ~> .K`, unable to match `intVal(15)`. This is the expected unmet
result obligation, not a parser error, timeout, unrelated crash, or unreachable
mutation.

Evidence: `evidence/logs/17-vacuity-dry-run.log` and
`18-vacuity-false-result.log`.

**Stage 6 result: PASS.**

## 7. Proven versus assumed accounting

### Precisely proven

Under the submitted generated semantics and K's reachability logic, for every
finite constructor list `L:PList` whose elements are either:

- `intVal(I)` for arbitrary K integers; or
- `ratVal(N,D)` for arbitrary integer numerator and structurally positive
  denominator,

executing the constructor-identical submitted module from empty initial
function/environment cells returns:

```text
intVal(sumSquares(L))
```

where `sumSquares` is the structurally recursive left fold of the square of
each exact mathematical ceiling. The loop claim establishes the stronger
accumulator invariant for arbitrary integer `A` and arbitrary remaining list
`L`. The theorem is unbounded in list length and integer magnitude; it is not a
finite unrolling or collection of examples.

This is a partial-correctness statement. It does not separately certify a
general CPython interpreter, exception behavior, or arbitrary modules.

### Trust ledger

| Boundary | Effect/dependents | Assessment and evidence |
|---|---|---|
| K 7.1.293 kernel, Haskell prover, LLVM runner, builtin `INT`, `MAP`, `STRING`, and K-list machinery | All rules and claims | Standard low-level trusted computing base; version recorded in `04-toolchain.log`, fresh builds in `05` and `07`. |
| Trusted `py2mpy.py` | Source-to-constructor identity | Launcher hash and byte identity checked; regenerated MPY and KORE constructor comparison both succeed (`02`, `14`). |
| Generated Mini-Python semantics | Meaning of the target constructor program | Audited rule by rule here; concrete Python/K boundary comparisons in `06`; no operational summary shortcut. |
| Standard binding of `from math import ceil` | Selects the result-bearing external primitive | Exact source import is pinned, but the semantics hardwires the name rather than building an import environment. Ordinary standard-library assumption; non-fatal concern. |
| `ceilInt` equation and positive-rational representation | Every element's rounded value and final result | Equation is the mathematical ceiling identity for positive denominators. Boundary checks in `06`; broader Python differential in `03`. |
| Finite CPython numeric value to exact K value bridge | Adequacy of the formal input domain | Every Python integer maps directly; every finite binary float has an exact rational representation with positive denominator. This is an informal representation bridge, not a K theorem. |
| `squareCeil`, `sumSquares`, `sumSquaresFrom` | Universal postcondition and invariant | Exhaustive truthful definitions; no opacity. The opposite `+1` interpretation is rejected (`19`, `20`). |
| Partial-correctness/normal-result scope | Excluded exception behavior | NaN, infinities, complex values, invalid lists, exotic numeric hooks, import failures, and exceptions are not modeled. The canonical function does not return the requested sum for such cases; their exclusion does not materially narrow the ordinary finite numeric-list source contract. |
| Finite differential tests | Empirical source and representation support | 2,017 Python comparisons and seven Python/K comparisons, zero mismatches. These support only the tested bridges and are not substituted for the K theorem. |

There are no fresh opaque values, unconstrained oracles, empirical axioms,
proof-local simplification lemmas, operational bridge rules, or hidden compiled
definitions in the proof.

### Gate accounting

- Gate A, real-program soundness: **PASS**. Exact program identity, actual
  control flow, summary sensitivity, body sensitivity, satisfiable
  preconditions, exact result constraints, and false-postcondition rejection
  are all established.
- Gate B, intent adequacy: **PASS**. Arbitrary finite integer/rational lists
  cover the intended arbitrary finite Python integer/finite-float value domain;
  the result is exactly the requested ceiling-square sum. There is no size
  bound.
- Gate C, trust and evidence auditability: **PASS**. All assumptions,
  dependents, scripts, commands, outputs, and expected-failure statuses are
  explicit and reproducible.

The remaining limitations are non-fatal generated-language scope and binding
concerns. They justify the benchmark's `CONCERNS / LEGIT` classification, not
`FAIL / NOT_LEGIT`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
