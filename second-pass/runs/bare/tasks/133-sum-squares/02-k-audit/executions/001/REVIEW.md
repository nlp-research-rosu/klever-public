# Independent adversarial audit: 133-sum-squares

## Outcome

The candidate contains a legitimate, result-constraining partial-correctness
proof of the exact submitted `solution.mpy` under its generated exact-rational
semantics. I assign `CONCERNS / LEGIT`, rather than `PASS / LEGIT`, because the
connection from that deliberately small semantics to all behavior of CPython
`math.ceil` and Python numeric objects is informal and finitely tested, not a
machine-checked refinement theorem. The limitation does not let a false result
be proved for the submitted program on the formal input domain.

The decisive positive facts are:

- the submitted MPY is reproduced byte-for-byte by the trusted translator;
- the program term in every entry claim parses to the same K term as that MPY;
- fresh LLVM and Haskell definitions compile from source without using
  candidate caches;
- every claim closes, both in isolated runs and in the untouched aggregate
  spec, with exit status 0 and `#Top`;
- the program-defined body executes under the operational rules and is not
  replaced by `sumSquares` or another oracle;
- all proof-local summaries are transparent, terminating equations;
- a fresh, buildable `+ 1` result mutation is rejected with the expected unmet
  implication.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `GENERATED_SEMANTICS`. `/reference/reference-semantics`
does not exist and is not a symlink. The trusted reference contains exactly the
three expected regular files: `prompt.py`, `canonical.py`, and `py2mpy.py`.
There is no trusted-mount contradiction and therefore no infrastructure breach.
See
[00_environment_and_integrity.log](evidence/00_environment_and_integrity.log).

### Candidate artifacts

All required artifacts are present as regular, non-symlink files:
`run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`,
`prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`, `semantic.k`,
`verification.k`, `spec.k`, and `prove.sh`. There are no candidate helper K
files beyond those three K sources. No required artifact is missing, mistyped,
or symlinked.

The candidate also contains `semantic-kompiled/` and
`verification-kompiled/`. Those are extra generated build outputs, not source
integrity failures. They were treated as untrusted evidence and never copied
or executed. No candidate `PROOF.md` or `spec-vacuity.k` exists; neither was a
required bare-generation deliverable.

The candidate prompt is byte-identical to `/reference/prompt.py`, with SHA-256
`c3e8935467740bb6def5ca00e35116e04dc22c240cc22df0f0efee1e5a493d57`.
The candidate translator is byte-identical to `/reference/py2mpy.py`, with
SHA-256
`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.

`run-input.json`, `metrics.json`, `codex-last.txt`, the 859,224-byte generation
log, and the 331-record structured trace were reviewed only as untrusted
claims. They report a bare run, eventual `#Top`, and several intermediate
failed or stuck construction attempts. None of those reports was used as proof
evidence. Bounded extracts and the trace command inventory are in
[01b_untrusted_claims.log](evidence/01b_untrusted_claims.log) and
[01_trace_summary.log](evidence/01_trace_summary.log).

### Isolation

Only source inputs were copied to
`/tmp/audit-work/133-sum-squares`; trusted files were copied into its separate
`trusted/` directory. Checksums of the scratch sources are recorded in
[02_source_copy.log](evidence/02_source_copy.log). All compilation,
mutation, and execution below occurred in that scratch directory.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For a list of numbers `lst`, the required result is

`sum(math.ceil(x) ** 2 for x in lst)`.

Ceiling is applied to each element before squaring. The documented results are
14 for `[1,2,3]`, 98 for `[1,4,9]`, 84 for `[1,3,5,7]`, 29 for
`[1.4,4.2,0]`, and 6 for `[-2.4,1,1]`. The empty-list result is 0.

The trusted canonical implementation initializes an accumulator, iterates over
the input list, adds `math.ceil(i) ** 2`, and returns the accumulator. The
candidate uses the same algorithm with `from math import ceil`, an explicit
`rounded` local, and multiplication in place of exponentiation. Those changes
preserve the result.

### Translation identity

The trusted command

```text
python3 trusted/py2mpy.py solution.py > regenerated-solution.mpy
```

exited 0. `cmp` and `diff` found no difference from submitted `solution.mpy`;
both have SHA-256
`c321881aab59c156ade6fe479b0f35b0e3818daeeceb94c1af8dfbe9e8b1854c`.
See [03_program_fidelity.log](evidence/03_program_fidelity.log).

### Independent differential test

[03_differential_test.py](evidence/03_differential_test.py) separately imports
the trusted canonical entry point and the scratch candidate entry point. Its
scope was:

- all five documented examples;
- 15 empty, singleton, exact-integer, immediately-above/below-integer,
  Boolean, fraction, and large-integer boundary cases;
- all 2,955 lists of lengths 0 through 3 over a 14-value pool spanning
  negative, zero, and positive ceiling boundaries;
- 500 deterministic generated lists of lengths 0 through 20 containing
  integers and independently constructed `Fraction` values.

All 3,475 comparisons matched; exit status was 0. This establishes strong
finite evidence of implementation equivalence on the tested ordinary numeric
domain. It is not treated as a universal proof.

## 3. Clean proof reconstruction

### Toolchain and fresh builds

The live toolchain was independently available as K v7.1.293 and Python
3.10.12. The following source-only builds both exited 0:

```text
kompile semantic.k --backend llvm --syntax-module MPY-SYNTAX \
  --main-module MPY --output-definition audit-semantic-kompiled

kompile verification.k --backend haskell --syntax-module MPY-SYNTAX \
  --main-module VERIFICATION \
  --output-definition audit-verification-kompiled
```

The output directories did not exist before these commands. Build evidence is
in [04_fresh_build_and_proofs.log](evidence/04_fresh_build_and_proofs.log).

### Positive proof claims

Each target was copied into a separate scratch spec and run against the fresh
Haskell definition. The universal theorem was supplied its exact
`loop-invariant` circularity dependency; the loop claim was also proved alone.

| Target | Formal result | Exit | Output |
|---|---:|---:|---|
| ground `[1,2,3]` entry claim | `intVal(14)` | 0 | `#Top` |
| `all-numeric-lists` plus its loop dependency | `intVal(sumSquares(L))` | 0 | `#Top` |
| `loop-invariant` alone | `intVal(sumSquaresFrom(A,L))` | 0 | `#Top` |
| ground `[1.4,4.2,0]` exact-rational claim | `intVal(29)` | 0 | `#Top` |
| ground `[-2.4,1,1]` exact-rational claim | `intVal(6)` | 0 | `#Top` |
| untouched `spec.k`, all five claims | all above | 0 | `#Top` |

Exact commands and complete bounded outputs are in
[04b_individual_proofs.log](evidence/04b_individual_proofs.log).

An initial reviewer harness attempted the universal claim without its loop
circularity and was manually interrupted while it unrolled indefinitely. That
diagnostic is preserved in `04_fresh_build_and_proofs.log`; it is neither a
candidate proof command nor a candidate failure. The corrected isolated
harness above uses the dependency actually present in `spec.k`.

### Fresh concrete execution

The fresh LLVM semantics executed the actual `solution.mpy` on 19 cases:
empty; all five examples; zero and signed integers; rational values just above,
below, and at 0, 1, and -1; a denominator encoded through `next(next(one))`;
and large integers. Every `krun` exited 0, terminated with
`<k> intVal(N) ~> .K </k>`, and matched both Python implementations. See
[05_concrete_semantics_crosscheck.py](evidence/05_concrete_semantics_crosscheck.py)
and
[05_concrete_semantics_crosscheck.log](evidence/05_concrete_semantics_crosscheck.log).

## 4. Adequacy and real-program pinning

### Claims in plain language

1. `spec.k:6-23` starts with exactly the submitted module, an empty function
   map and environment, and the list `[1,2,3]`; it requires termination at the
   concrete result 14.
2. `spec.k:25-41` starts with the same exact module and empty state for any
   well-formed `PList`; it requires the result
   `intVal(sumSquares(L))`.
3. `spec.k:43-56` is the loop circularity. Given the exact real loop body,
   the exact following `return total` continuation, any remaining list `L`,
   and an environment whose newest `total` binding is `intVal(A)`, it requires
   the result `intVal(sumSquaresFrom(A,L))`. The functions cell is preserved.
4. `spec.k:58-75` is the exact-rational encoding of `[1.4,4.2,0]` and requires
   29.
5. `spec.k:77-94` is the exact-rational encoding of `[-2.4,1,1]` and requires
   6.

There are no textual `requires` conditions, but each claim's source
configuration is itself a precondition: the entry claims require empty initial
cells and the exact module; the helper requires the stated loop head and top
accumulator binding. All are satisfiable.

### Program identity and execution sensitivity

The program term extracted from the entry claims and the actual
`solution.mpy` were independently parsed with `kast`. Their normalized outputs
are byte-identical, with SHA-256
`ae71a37fa2935747287b0794b525f45ab93d174226d7a39583a0ce875130cb65`.
See
[06b_corrected_program_pinning.log](evidence/06b_corrected_program_pinning.log).
An earlier standalone-parser probe incorrectly included K's internal
`.PyStmts` terminator and failed to parse; that reviewer harness error is
preserved in
[06_adequacy_and_pinning.log](evidence/06_adequacy_and_pinning.log) and was
corrected before drawing the identity conclusion.

The operational path loads the submitted `FuncDef` body into `<functions>`,
selects that stored body in `callEntry`, and executes its assignments, loop,
and return. `sumSquares` appears only in the destination theorem and never
replaces operational execution. Changing the executed multiplication to
addition changed the concrete `[1,2,3]` result from 14 to 12, demonstrating
body sensitivity; see
[07_static_inventory_and_sensitivity.log](evidence/07_static_inventory_and_sensitivity.log).

### Satisfying witnesses and result constraint

Concrete witnesses are:

- the four ground entry states written in `spec.k`;
- the universal state with `L = nil`, which returns 0;
- the universal state with
  `L = [ratVal(14,ten), ratVal(-24,ten)]`, which returns 8;
- the loop state with `A = 5`, that same `L`, functions `.Map`, and
  `env = binding("total",intVal(5)) .Env`, which returns 13.

The ground loop claim closed with `#Top`. All six substituted results matched
both Python implementations (with the accumulator added for the loop helper).
See [06_adequacy_witnesses.py](evidence/06_adequacy_witnesses.py) and
`06_adequacy_and_pinning.log`.

Every destination constrains the returned `<k>` value. The existential
destination variables for final function/environment cells do not occur in
the result and cannot choose it. There is no implication-only or free-result
postcondition.

## 5. Rule-by-rule static soundness review

The exhaustive source listing and attribute searches are in
[07_static_inventory_and_sensitivity.log](evidence/07_static_inventory_and_sensitivity.log)
and
[07b_corrected_attribute_inventory.log](evidence/07b_corrected_attribute_inventory.log).
Two malformed reviewer `rg` expressions in the first log exited 2; the
corrected searches are preserved in the latter and do not change the source
inventory.

### Local syntax, configuration, and attributes

| Source | Complete local declaration inventory |
|---|---|
| `semantic.k:5-19` | `PyModule(Module)`; statement-list syntax; `ImportFrom`, `FuncDef/Params`, `Assign`, `AugAssign`, `For`, `Return`; `Name`, `Int`, `Call`, `BinOp` |
| `semantic.k:27-46` | `PosNat` constructors `one`, `next`, `ten`; `posInt [function,total]`; `NumValue` constructors `intVal`, `ratVal`; `PList` constructors `nil`, `cons`; `PValue` injection and `listVal`; `ceilInt [function]` |
| `semantic.k:59-67` | stored `function`; environment constructors `.Env` and `binding`; functions `evalExpr`, `lookupValue`, `ceilValue`, `addValue`, `mulValue` |
| `semantic.k:84-89` | control terms `load`, `loadStmt`, `callEntry`, `exec`, `loop`, `bind` |
| `semantic.k:91-96` | `<python>` configuration containing `<k>`, `<functions>`, and `<env>`; initialization is actual program followed by `callEntry($ARGS)` |
| `verification.k:6-8` | `squareCeil [function]`, `sumSquares [function,total]`, `sumSquaresFrom [function,total]` |

All `[symbol(...)]` occurrences name constructors; they are not opaque
result-bearing symbols. There are no local `[functional]`, `[simplification]`,
`[concrete]`, `[priority]`, `[owise]`, or opaque declarations. There are no
priority rules or proof-local operational bridges.

`posInt` is genuinely total on `PosNat`: `one`, `next(P)`, and `ten` are
disjoint and exhaustive, and the only recursive case descends to `P`.
`sumSquares` immediately dispatches to `sumSquaresFrom`;
`sumSquaresFrom` has disjoint, exhaustive `nil` and `cons` cases and descends
on the tail. The remaining functions intentionally lack `[total]` and stop
when used outside their modeled subset.

### Domain and expression rules

| Rule | Review decision |
|---|---|
| `semantic.k:33 posInt(one) => 1` | True constructor equation. |
| `semantic.k:34 posInt(next(P))` | True successor equation; structurally descending. |
| `semantic.k:35 posInt(ten) => 10` | True special-constructor equation; no overlap with `one` or `next`. |
| `semantic.k:48 ceilInt(intVal(I)) => I` | Integer ceiling is itself. |
| `semantic.k:49-50 ceilInt(ratVal(N,D))` | With `posInt(D)>0`, `-((-N) divInt d)` is exactly `ceil(N/d)` because K `divInt` is Euclidean division. |
| `semantic.k:69 evalExpr(Int(I),_)` | Exact integer-literal evaluation. |
| `semantic.k:70 lookupValue(binding(X,V) _,X)` | Correct newest-binding lookup. |
| `semantic.k:71-72 lookupValue` miss | Guard is the disjoint complement of the hit case; recursion descends through the environment. |
| `semantic.k:73 evalExpr(Name(X),RHO)` | Delegates to the correct shadowing lookup; an unbound name visibly remains unsupported. |
| `semantic.k:74 Call(Name("ceil"),E)` | Computes the modeled ceiling transparently. It is intentionally specialized to the exact imported function; general Python binding/rebinding is outside scope. |
| `semantic.k:75-76 BinOp("*",...)` | Correct pure integer multiplication for the used rounded values. |
| `semantic.k:77-78 BinOp("+",...)` | Correct pure integer addition; not used in submitted `solution.mpy`. |
| `semantic.k:80 ceilValue(NumValue)` | Transparent wrapper around the reviewed `ceilInt`; no oracle. |
| `semantic.k:81 addValue(intVal,intVal)` | Correct unbounded integer addition. |
| `semantic.k:82 mulValue(intVal,intVal)` | Correct unbounded integer multiplication. |

The lookup rules do not overlap because of the string-inequality guard.
Expression constructor and operator-string patterns are pairwise disjoint.
There is no catch-all that fabricates a value: a syntactically accepted `"-"`
operator stopped with residual `evalExpr(BinOp("-",...))` and exit 113, as
recorded in `07_static_inventory_and_sensitivity.log`.

### Operational rules

| Rule | Review decision |
|---|---|
| `semantic.k:98 Module(SS)` | Begins left-to-right loading of the real statement list. |
| `semantic.k:100 load(.PyStmts)` | Correct list-load base case. |
| `semantic.k:101 load(S SS)` | Sequences the head before the tail. |
| `semantic.k:103 loadStmt(ImportFrom(_, _))` | Ignores imports broadly. Coupled with the specialized `ceil` call rule, it is sound for the exact `from math import ceil` source with no rebinding, but not a general import semantics. |
| `semantic.k:104-105 loadStmt(FuncDef(...))` | Stores the exact parameter and body under the declared name. |
| `semantic.k:107-109 callEntry(V)` | Selects the stored `"sum_squares"` body, binds its actual parameter, and resets the local environment. This is exact for the required entry point. |
| `semantic.k:111 exec(.PyStmts)` | Correct statement-list base case. |
| `semantic.k:113-114 Assign` | Evaluates the pure modeled RHS in the old environment and pushes a shadowing binding. Observationally equivalent to assignment for this subset. |
| `semantic.k:116-117 AugAssign "+"` | Reads the newest old value and pure RHS, adds them, and pushes the result. This preserves the actual program's order and value. |
| `semantic.k:119-120 For` | Evaluates the iterable and schedules the loop before the following statements, preserving list order. |
| `semantic.k:122-123 Return` | Evaluates the return expression and discards the remaining statements in that `exec`. It is exact in the submitted post-loop context; arbitrary nested abrupt-return contexts are not modeled. |
| `semantic.k:125 loop(...,nil,...)` | Correct zero-iteration base case. |
| `semantic.k:126-127 loop(...,cons(V,VS),BODY)` | Binds the current element, executes the exact body, then recurs on the tail. |
| `semantic.k:129-130 bind` | Pushes the loop-variable binding before body execution. |

The `load`, `exec`, and `loop` cases are disjoint by list/statement
constructors. State changes are confined to the function map and shadowing
environment. There is no heap, output, exception, allocation, or external
state in the modeled program. The function body has no side-effecting
expression, list mutation, nested call, or return inside the loop, so atomic
expression evaluation and the stated control contexts preserve every
observable component used by this program.

The import rule, hard-coded `ceil` binding, and return rule accept broader
syntactic contexts than were validated. I do not label them unsound for this
theorem: no such broader context is reachable by varying an intended input to
the fixed submitted program, so there is no false-conclusion witness on the
intended domain. They are instead recorded as scope/evidence gaps and are part
of the `CONCERNS` judgment.

### Verification equations

| Rule | Review decision |
|---|---|
| `verification.k:10 squareCeil(V)` | Definitionally equals the square of the reviewed ceiling. |
| `verification.k:12 sumSquares(VS)` | Initializes the accumulator to zero without replacing program execution. |
| `verification.k:13 sumSquaresFrom(A,nil)` | Correct accumulator base case. |
| `verification.k:14-15 sumSquaresFrom(A,cons(V,VS))` | Adds exactly one squared ceiling and structurally descends on `VS`. |

These equations are truthful, terminating, and non-overlapping. They occur in
postconditions and the loop circularity, not as rewrites that bypass
`callEntry`, `exec`, or `loop`. There is no shared opaque symbol between
execution and the postcondition.

### Used-construct coverage

| Submitted MPY construct | Declaration and executing rules |
|---|---|
| `Module` and statement lists | `semantic.k:5,7,98,100-101` |
| `ImportFrom("math","ceil")` | `semantic.k:9,103`, with `ceil` evaluation at 74 and 80 |
| `FuncDef/Params` | `semantic.k:10,59,104-109` |
| `Assign` | `semantic.k:11,113-114` |
| `For` | `semantic.k:13,119-120,125-130` |
| `AugAssign "+"` | `semantic.k:12,116-117` |
| `Return` | `semantic.k:14,122-123` |
| `Name` and shadowing lookup | `semantic.k:16,70-73` |
| `Int` | `semantic.k:17,69` |
| `Call(Name("ceil"),...)` | `semantic.k:18,74,80` |
| `BinOp("*",...)` | `semantic.k:19,75-76,82` |

Normal and empty concrete runs exercise both loop branches, statement-list
base and recursive cases, lookup hit and miss, integer and rational ceiling,
and `one`, `next`, and `ten` denominator constructors. There is no used
construct without a rule.

## 6. Fresh non-vacuity test

The reviewer-authored mutation is
[spec-vacuity-audit.k](evidence/spec-vacuity-audit.k). It changes the universal
destination from

```text
intVal(sumSquares(L))
```

to the deliberately false

```text
intVal(sumSquares(L) +Int 1)
```

while retaining the exact real program and genuine loop dependency. The
satisfying witness `L = nil` returns 0 but the mutation requires 1.

`kprove --dry-run` exited 0, establishing that the mutation parsed and built.
The real proof command exited 1 and emitted `WarnStuckClaimState`; its residual
explicitly compared `sumSquaresFrom(0,L) +Int 1` with
`sumSquaresFrom(0,L)`, followed by the expected “cannot be rewritten further”
error. This is a reached, result-bearing obligation, not a parser error,
missing import, crash, or timeout. Exact commands and bounded output are in
[08_fresh_non_vacuity.log](evidence/08_fresh_non_vacuity.log).

## 7. Proven versus assumed accounting

### What the K proof establishes

Under the fresh generated semantics, for every finite `PList` whose elements
are either arbitrary K integers or exact rationals with a positive
`PosNat` denominator, execution of the exact submitted module from empty
function/environment cells, followed by the required
`sum_squares` entry call, reaches

```text
intVal(sumSquares(L))
```

where `sumSquares` is transparently defined as the left-accumulated sum of the
squares of the mathematical ceilings of all elements. The loop circularity
establishes the corresponding statement for any integer accumulator and
remaining list. The four concrete claims establish the stated ground results.
This is a partial-correctness reachability result; no candidate prose or finite
test substitutes for it.

### Trust ledger

| Boundary | Role and dependents | Assessment |
|---|---|---|
| K v7.1.293 parser, compiler, LLVM/Haskell backends, and `kprove` | All builds, executions, and reachability closure | Necessary low-level tool trust; independently rebuilt and mutation-tested. |
| K `Int`, `divInt`, `Map`, and `String` built-ins | Integer arithmetic, exact ceiling formula, function map, string guards | Acceptable fixed primitives. `divInt`'s Euclidean contract makes the ceiling equation mathematically valid for positive denominators. |
| Trusted `/reference/py2mpy.py` | Source-to-MPY syntax bridge | Trusted input by audit authority; byte identity of submitted MPY was independently checked. |
| Generated MPY operational semantics | Meaning of the submitted constructors | Audited rule by rule. It executes the real body and has no result oracle or proof-only operational shortcut. |
| Exact rational representation `ratVal(N,D)` | Formal numeric input model and `ceilInt` | Transparent and mathematically sound. |
| Mapping ordinary CPython finite numeric inputs to `intVal`/`ratVal` | Bridge from the formal input model to actual Python objects | Informal, not machine-checked. Every finite float has an exact rational value and ceiling is compatible with that value, but the candidate supplies no formal encoder/refinement theorem. This is the principal concern. |
| Python import/binding behavior | Justifies treating the exact imported name `ceil` as mathematical ceiling | Sound for the fixed source (`from math import ceil`, no rebinding), but generalized import and dynamic binding behavior are not modeled. |
| Differential tests | Candidate-vs-canonical bridge on 3,475 inputs; K-vs-both-Python bridge on 19 inputs | Reproducible finite evidence only, not a universal theorem. |
| Natural-language domain | Lists of ordinary numbers | The formal theorem excludes NaN, infinities, non-lists, complex numbers, exceptional/custom numeric protocols, and Python side effects. Those are not exercised by the prompt examples and remain outside the proof. |

There are no opaque proof-local symbols, trusted program-defined helpers,
empirical operational bridges, simplification axioms, or answer-encoding
semantic rules. The generated semantics is deliberately not a general Python
semantics; its broader unused import/return contexts should not be reused
without extension and revalidation.

### Decision

Real-program soundness passes: the exact body executes, the loop helper matches
real control flow and state, all summaries are transparent, the result is
constrained, and the false result is rejected. Intent adequacy is sufficient
for the ordinary finite numeric-list task, but has the documented formal-model
bridge limitation. Evidence is reproducible and honestly finite.

Accordingly, the proof is legitimate but merits concerns rather than an
unqualified pass.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
