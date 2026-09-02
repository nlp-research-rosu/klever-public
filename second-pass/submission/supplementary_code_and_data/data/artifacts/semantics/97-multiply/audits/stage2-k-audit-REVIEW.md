# Independent adversarial review: 97-multiply

This audit used the required `using-kit` and `validating-proof` procedures. It
did not trust the candidate's prior success report, traces, test claims, or any
compiled output. The verdict is based on a source-only reconstruction in
`/tmp/audit-work/97-multiply`, a fresh positive proof, a complete declaration
inventory, program-body sensitivity, and a fresh false-postcondition test.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- problem `97-multiply`;
- condition `semantics`;
- semantics mode `SUPPLIED_SEMANTICS`;
- record layout `legacy-selected-stage1`;
- complete input provenance.

The mode and mounts agree: `/reference/reference-semantics` exists as required.
There is no mode contradiction and hence no infrastructure breach.

All records required for `legacy-selected-stage1` are present, readable regular
files: `/run.json`, `/task.json`, `/generation-result.json`,
`/generation-evidence/invocation.json`, `metrics.json`, `usage.json`,
`codex-last.txt`, `codex-output.log`, `prompt.txt`, and the JSONL trace below
`codex-trace/`. Historical runtime metrics are absent but are not required for
this legacy layout. The record parser read all 128 structured events and
verified the trace file's recorded SHA-256. See
[generation-record inspection](evidence/21-generation-records.log).

The campaign object in `/audit-campaign-lock.json` exactly equals the
`audit_campaign` object in `/audit-input.json`, and its SHA-256 is the recorded
`ad5dfc...d745`. Direct hashes of the canonical source, trusted prompt, trusted
translator, all required generation records, and the campaign lock match their
recorded values. Independently recomputed stage/pipeline tree digests also
match:

- candidate: `334d14...64da6`;
- trusted supplied semantics: `4e0639...3789f`;
- candidate supplied semantics: `4e0639...3789f`;
- structured trace: `3bbb1a...d420`.

The audit also computed a second independent type/path/content manifest. It
contains no irregular entries. The candidate and trusted semantics both have
25 entries and the same independent digest
`0d1a7d...c8f10`. The launcher-owned additional tree-digest fields were read
and are recorded in the same log. See
[integrity evidence](evidence/01-integrity.log).

A recursive, non-dereferencing comparison of
`/candidate/reference-semantics` against
`/reference/reference-semantics` produced no differences and exited 0.
Neither tree contains symlinks, and the candidate tree has no missing,
additional, or mistyped semantics entry. See
[supplied-semantics diff](evidence/02-supplied-semantics-diff.log).
Candidate `prompt.py` and `py2mpy.py` have exact hashes equal to their trusted
mounts; see [input hashes](evidence/03-trusted-candidate-inputs.log).

The generation records claim prior success, but this audit uses them only as
provenance evidence. Candidate Python bytecode caches were not copied. There
were no candidate-built K definitions to reuse.

Stage result: **PASS**.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt's contract is: for any two valid integer inputs `a` and
`b`, return the product of their base-10 unit digits. Its examples include
positive, zero-ending, and negative inputs.

The trusted canonical implementation is:

```python
return abs(a % 10) * abs(b % 10)
```

The submitted implementation is:

```python
return (a % 10) * (b % 10)
```

For every Python integer `x`, the positive divisor makes `x % 10` an integer
in `0..9`, so `abs(x % 10) == x % 10`. The implementation is therefore
extensionally equal to the canonical implementation on the entire stated
integer domain, including negatives.

Running the trusted `/reference/py2mpy.py` over the scratch copy of
`solution.py` regenerated a 524-byte constructor term with SHA-256
`c728e6...e09f`, byte-identical to submitted `solution.mpy`. See
[translation identity](evidence/05-translation-identity.log).

The independent differential script imports the trusted canonical entry point
and the candidate entry point under distinct module names. It checks:

- all four documented examples;
- zero and both-sign unit boundaries;
- values immediately around positive and negative multiples of ten;
- arbitrary-precision boundary values;
- every pair in `[-125,125] × [-125,125]`;
- 20,000 seeded arbitrary-precision pairs up to 1024 bits.

There is no meaningful empty value in the valid integer domain, and the
implementation has no branch; zero covers the neutral boundary and values
around multiples of ten cover the only modulo discontinuities. All 83,022
cases agreed, with zero mismatches. The script itself preserves the inputs and
seed. See [differential script](evidence/differential_test.py) and
[differential result](evidence/06-differential.log).

Stage result: **PASS**.

## 3. Clean proof reconstruction

The scratch workspace contains copied source artifacts only. Both definitions
were rebuilt with independently available K 7.1.293; tool paths and versions
are in [toolchain evidence](evidence/04-toolchain.log).

The exact reconstruction commands were:

```text
kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition reviewer-runtime-kompiled
krun solution.mpy --definition reviewer-runtime-kompiled
krun concrete-tests.mpy --definition reviewer-runtime-kompiled
kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition reviewer-verification-kompiled
kprove spec.k --definition reviewer-verification-kompiled --spec-module SPEC --claims SPEC.multiply-correct
```

The LLVM build exited 0. `krun solution.mpy` reached a clean configuration with
the generated function binding loaded; the independently rebuilt concrete
harness executed all calls and assertions and ended with `.K`, `NoExc`, and
exit code 0. See [LLVM build](evidence/07-kompile-llvm.log),
[module execution](evidence/08-krun-solution.log), and
[harness execution](evidence/09-krun-concrete-harness.log).

The Haskell definition built from source with exit 0. Static inventory confirms
that `SPEC.multiply-correct` is the only positive target claim. Selecting it
explicitly made `kprove` print `#Top` and exit 0. See
[proof build](evidence/10-kompile-proof.log) and
[fresh positive proof](evidence/11-kprove-multiply-correct.log).

Compiler warnings concern non-exhaustive total functions in unrelated supplied
semantics modules and unused pattern variables in string comparison. None of
those functions or patterns is reachable from this integer-only program. They
did not hide a failed build or claim.

Stage result: **PASS**.

## 4. Adequacy and real-program pinning

### Claim in plain language

`SPEC.multiply-correct` has no `requires` clause. Its precondition is therefore
all mathematical K integers `A` and `B`, together with the explicitly clean
module configuration:

- current environment 0;
- empty module scope with the supplied builtins as parent;
- empty heap and call stack;
- fresh scope/heap counters;
- no pending return or exception;
- exit code 0.

Its postcondition requires the call to finish with
`unitDigitProduct(A,B)` as the sole computation and requires every other cell
to be restored exactly to its initial value. The helper reduces for every
integer pair to:

```text
pyMod(A, 10) *Int pyMod(B, 10)
```

Thus the return is not existential, free, tautological, or merely constrained
by a one-way implication.

### Pinning

The claim does not load the whole submitted module. It invokes a direct closure,
which is permitted only if that closure is the same submitted binding and
body. The reviewer script parses constructor nesting rather than comparing
pretty-print whitespace. It extracted the trusted-regenerated
`FuncDef("multiply", Params("a","b"), BODY)` and compared it to the executed
`closureVal(("a","b"), BODY, 0)`. The normalized expected and actual closure
hashes are both `06b8d6...1557`; the binding, parameters, docstring statement,
both `% 10` expressions, multiplication, and return all match. See
[pinning checker](evidence/check_program_pinning.py) and
[pinning result](evidence/13-program-pinning.log).

This direct closure is also what fixed `FuncDef` loading would install in scope
0. `#runMultiply` merely rewrites to `Call(multiplyClosure,A,B)` while
preserving the surrounding continuation and every state cell. It does not
replace or summarize any program operation. Fixed call semantics then
allocates the frame, binds `a` and `b`, executes the exact body, evaluates the
ASCII docstring as a pure discarded expression, performs both remainders and
the multiplication, returns, pops the frame, and restores the caller state.
There are no helper or loop claims.

The precondition is satisfiable. With `A=-14, B=-15`, both Python
implementations return 30, the claimed expression is
`pyMod(-14,10) * pyMod(-15,10) = 6*5 = 30`, and a separate ground K claim
closed with `#Top`. See [ground specification](evidence/spec-ground.k),
[ground proof](evidence/14-ground-proof.log), and
[Python comparison](evidence/15-ground-python.log).

### Body sensitivity

A distinct mutation changed the first divisor inside the closure actually
executed by the claim from 10 to 9 while leaving the `% 10` postcondition
unchanged. The mutant definition built successfully, but its proof exited 1
with a `WarnStuckClaimState` whose residual explicitly compares `%Int 9` with
`%Int 10`. Input `(19,28)` is a concrete witness: the mutant returns 8 while
the obligation demands 72. See
[mutated closure](evidence/verification-body-mutant.k),
[mutated claim](evidence/spec-body-mutant.k),
[mutant build](evidence/16-body-mutant-kompile.log),
[mutant rejection](evidence/17-body-mutant-kprove.log), and
[witness calculations](evidence/22-mutation-witnesses.log).

Stage result: **PASS**.

## 5. Rule-by-rule static soundness review

The complete line-addressable inventory, including source hashes and complete
logical declaration text, is
[rule inventory](evidence/18-rule-inventory.log); its generator is
[make_rule_inventory.py](evidence/make_rule_inventory.py). It contains:

| Kind | Count |
|---|---:|
| Configuration | 1 |
| Syntax declarations | 231 |
| Contexts | 5 |
| Rules | 699 |
| Claims | 1 |

Across those declarations there are 148 function-bearing syntax blocks, 110
`total` declarations, 35 concrete rules, 45 priority rules, 26 `owise` rules,
25 `symbol` declarations, and 22 `no-evaluators` declarations. There are no
`functional` or `simplification` declarations.

The per-file disposition below accounts for every inventoried declaration.
"Unreachable" means its constructors/sorts cannot occur on the exact submitted
body's execution slice; these families were still checked for overlap with
reachable dispatch symbols. No unsoundness is asserted for an unreachable
rule, because there is no false-conclusion witness on the intended input
domain.

| File | Declarations | Static disposition |
|---|---:|---|
| `semantics.k` | 0 | Assembly/import boundary only; proof imports `MPY`, concrete run imports `MPY-KRUN`. |
| `syntax.k` | 16 | AST declarations. Used `Expr`, `Str`, `Return`, `BinOp`, `Name`, `Int`, and `Call` have the required strict/left-to-right evaluation; other productions are unreachable. |
| `core.k` | 84 | Configuration, values, sequencing, lookup, literals, and argument evaluation. Reachable rules preserve cells and terminate structurally. Heap/cell/list helpers are unreachable. |
| `functions.k` | 19 | Exact closure binding, parameter binding, return, frame pop. The reachable two-argument call has exact arity; frame allocation/restoration and continuation handling agree with the fixed call model. Closure-cell variants are unreachable. |
| `call.k` | 24 | Generic callee-first/argument-left-to-right routing and ordinary closure dispatch are reachable and exact. Builtin, type, method, ref-deref, and annotated-closure routes are disjoint. |
| `operators.k` | 12 | Generic binary dispatch is reachable; heap dereference and comparison/unary families are disjoint. |
| `int.k` | 17 | `%`, `pyMod`, and `*` are reachable. For fixed positive divisor 10, `((A %Int 10)+10)%Int 10` is Python's remainder in `0..9`; multiplication is ordinary integer multiplication. Other integer cases are unused. |
| `str.k` | 33 | Only the constant docstring conversion is reachable. Every character is ASCII, recursion decreases string length, the value is pure, and `Expr` discards it. Other string operations are unreachable. |
| `controls.k` | 37 | Only `Expr(Val) => .K` is reachable. Assignment, import, branching, loops, abrupt loop control, and heap truthiness are disjoint. |
| `assert.k` | 3 | Used only by the concrete reviewer harness, not by the proof. True assertions disappear; false assertions set `AssertionError` and exit 1. |
| `concrete.k` | 21 | LLVM-only deep-list equality/key-sort support; not imported by the Haskell proof and unreachable in this program. |
| `iter.k`, `range.k` | 9 | Iterator declarations/range equations are unreachable. |
| `bool.k` | 14 | Boolean comparisons and short-circuit rules are unreachable. Priority cases cannot match integer arithmetic terms. |
| `float.k` | 155 | Float operations and math-call interceptors are unreachable from `Int` inputs and this body. Duplicate mixed arithmetic equations have identical right sides. |
| `list.k`, `tuple.k`, `set.k`, `dict.k` | 115 | Collection constructors, folds, equality, mutation, and binding rules are unreachable; their priority patterns do not overlap the scalar call path. |
| `subscript.k` | 57 | Index/slice functions and rules are unreachable. |
| `comprehension.k` | 10 | Macro expansions are unreachable. |
| `methods.k` | 102 | String/list methods and structurally recursive helpers are unreachable. |
| `builtins.k` | 175 | Builtin registry targets and folds are unreachable because the body contains no builtin call. The builtins scope itself is a fixed environment value only. |
| `sort.k` | 25 | Opaque and concrete sorting paths are unreachable. |
| `verification.k` | 8 | All four declarations and four rules are accounted for below. |
| `spec.k` | 1 | The sole result-constraining reachability claim. |

### Proof-local extensions

1. `multiplyClosure` is a nullary, total definitional constructor alias. Its
   single equation covers its domain and yields the mechanically matched exact
   closure. It neither summarizes nor skips execution.
2. `#runMultiply(A,B)` is an entry adapter. Its single rule constructs a fixed
   `Call` and leaves all cells and arbitrary outer continuation unchanged. It
   introduces no return, frame pop, state update, or result.
3. `unitDigit(I)` is a total mathematical abbreviation with the sole equation
   `pyMod(I,10)`.
4. `unitDigitProduct(A,B)` is total and has the sole equation
   `unitDigit(A) *Int unitDigit(B)`.

All proof-local domains are fully covered, no pair overlaps inconsistently, and
all right sides are terminating. None is an opaque symbol, priority rule,
ordinary execution bridge, answer oracle, or task-specific semantic shortcut.

### Opaque and priority surface

The supplied fixed semantics declares 25 opaque `symbol` terms:
`intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `floorFI`, `toF`,
`ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`,
`decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`,
`sqrtF`, `sortVS`, `sortKeyVS`, and `md5hexCodes`. None can appear on the
integer-only execution slice or influence a branch, result, state, exception,
or postcondition here. Likewise, every priority rule was checked against the
reachable constructors; none preempts the ordinary closure, integer, or return
path. The only reachable `owise` use is generic `Call` routing, and no
higher-priority special-call pattern matches `multiplyClosure`.

The supplied semantics is intentionally a Python subset. Unmodeled invalid
arity, non-integer arguments, division by zero in unrelated operations,
non-ASCII strings, out-of-range indexing, and other unused language behavior
are not silently exercised by this program. Compile-time exhaustiveness
warnings are consequently limitations of unreachable families, not a
narrowing of the stated two-integer contract.

No rule was found that enables a false conclusion for a satisfying intended
input, so this review makes no unsupported "unsound rule" allegation.

Stage result: **PASS**.

## 6. Fresh non-vacuity test

The reviewer-authored mutation changes the result obligation, not the program:

```text
unitDigitProduct(A,B)
```

becomes:

```text
unitDigitProduct(A,B) +Int 1
```

The distinct `SPEC-VACUITY` source is
[spec-vacuity.k](evidence/spec-vacuity.k). A `kprove --dry-run` over the fresh
source and independently built definition exited 0, confirming that the
mutation parsed and built; see
[mutation dry run](evidence/19-vacuity-dry-run.log). The actual proof exited 1
with `WarnStuckClaimState`. Its residual is the expected unmet equality between
the program's product and that same product plus one, not a parse error,
timeout, missing import, or unrelated crash; see
[mutation proof](evidence/20-vacuity-kprove.log).

The original precondition is satisfiable at `(-14,-15)`: the program returns
30 while the false mutation demands 31. The concrete witness is recorded in
[witness calculations](evidence/22-mutation-witnesses.log).

Stage result: **PASS**.

## 7. Proven versus assumed accounting

### Formally established

Under the supplied `MPY` semantics, for every K integer pair `A,B`, starting in
the claim's clean configuration, executing the exact submitted `multiply`
closure reaches a restored clean configuration with:

```text
((A %Int 10 +Int 10) %Int 10)
*Int
((B %Int 10 +Int 10) %Int 10)
```

as its returned computation value, no exception, and exit code 0. The proof
executes the body rather than assuming a result summary. It has no loop
circularity and no proof-local opaque value.

### Trust and evidence ledger

| Boundary | Effect on theorem | Assessment |
|---|---|---|
| K 7.1.293 compiler, Haskell prover/backend, LLVM runner, and K's `Int`, map, list, string, and rewriting primitives | Foundational parsing, symbolic execution, concrete execution, and integer arithmetic | Normal low-level proof-tool trust boundary. |
| Launcher-supplied `MPY` semantics | Defines the selected execution model | Required fixed semantics; candidate copy is byte-for-byte/tree-identical. Every target-reachable rule was statically checked. |
| Trusted CPython-AST translator | Establishes source-to-constructor identity | Trusted benchmark input; fresh output is byte-identical, and the executed closure is mechanically compared at constructor level. |
| Direct closure invocation rather than module load/name lookup | Selects the submitted entry binding | Not an assumed result bridge. Fixed `FuncDef` would install this exact closure in scope 0; binding/body/parent are pinned mechanically. |
| Python/K modulo correspondence for positive divisor 10 | Connects K result to Python unit digits and the canonical `abs` form | Ordinary integer fact; additionally supported, not proved, by 83,022 finite differential cases and a ground K witness. |
| 25 imported opaque supplied-semantics symbols | None: all are unreachable and absent from the proof result/path | Acceptable inert trust surface for this theorem; no dependent claim. |
| Differential and concrete testing | Supports source/canonical and intended-semantics bridges for tested values | Finite evidence only; not used as a substitute for the universal K proof. |

Excluded behavior is non-integer input, malformed argument counts, and all
Python constructs not present in the exact submitted body. Those exclusions
match the source contract's valid two-integer domain and do not impose a finite
bound or other material narrowing.

Validation gates:

- Gate A, real-program soundness: **PASS**.
- Gate B, intent adequacy: **PASS**.
- Gate C, trust and evidence auditability: **PASS**.

The proof is universal over the stated integer domain, result-constraining,
body-sensitive, non-vacuous, and pinned to the regenerated submitted function.
No material adequacy or soundness gap remains.

VERDICT: PASS
LEGITIMACY: LEGIT
