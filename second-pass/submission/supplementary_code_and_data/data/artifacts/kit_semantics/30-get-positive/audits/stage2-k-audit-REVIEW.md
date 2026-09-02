# Independent adversarial audit — 30-get-positive

The candidate contains a legitimate partial-correctness proof of the submitted
program under the supplied MPY semantics. I rebuilt every definition from
source, reran the connection and target claims, mechanically pinned the entry
claim to the trusted regeneration of `solution.mpy`, reviewed all proof-local
rules, and rejected a fresh false postcondition. Candidate-provided binaries,
logs, prose, and prior `#Top` results were not reused as proof evidence.

## 1. Input and provenance integrity

The declared record layout is `pipeline-v3` and the rendered semantics mode is
`SUPPLIED_SEMANTICS`. The trusted `/reference/reference-semantics` mount is
present, so the mounts do not contradict the rendered mode.

The reviewer-authored integrity checker
[`evidence/check_integrity.py`](evidence/check_integrity.py), run in
[`evidence/01-integrity-check.log`](evidence/01-integrity-check.log), established:

- `/audit-campaign-lock.json` has SHA-256
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  exactly the value recorded in `/audit-input.json`.
- The parsed campaign-lock object exactly equals the `audit_campaign` object in
  `/audit-input.json`.
- Every required `pipeline-v3` record is present, readable, and not a symlink:
  `/run.json`, `/task.json`, `/generation-result.json`, all four required JSON
  records under `/generation-evidence`, `codex-last.txt`,
  `codex-output.log`, `prompt.txt`, and the structured trace directory.
- Every launcher-recorded single-file hash checked by the script matches the
  mounted bytes, including the run, task, result, invocation, metrics, runtime
  metrics, usage, generation prompt/output/last report, trusted prompt,
  canonical implementation, translator, and their candidate copies.
- The one structured trace file has the hash recorded in
  `/generation-result.json`; all 490 JSONL records parse successfully. The
  full mechanical read and event inventory is in
  [`evidence/01-generation-summary.log`](evidence/01-generation-summary.log).
- A recursive type-and-content manifest has 25 entries for each supplied
  semantics tree. The candidate and trusted manifests are exactly equal; there
  are no missing, additional, changed, mistyped, special, or symlinked entries.
- The broader candidate and trace scans contain no symlink or special-file
  entries.

The raw launcher records and their hashes are preserved in
[`evidence/01-audit-input-readable.log`](evidence/01-audit-input-readable.log),
[`evidence/01-generation-records.log`](evidence/01-generation-records.log), and
the bounded recursive inventory
[`evidence/01-mounted-inventory.log`](evidence/01-mounted-inventory.log).
Required candidate proof artifacts (`solution.py`, `solution.mpy`,
`verification.k`, `spec.k`, `prove.sh`, and `PROOF.md`) are regular files.

The generation records claim success, but that claim was not used to decide
proof validity. There is no audit-infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

`/reference/prompt.py` requires `get_positive(l)` to return only the positive
numbers from the list. `/reference/canonical.py` implements the contract as
`[e for e in l if e > 0]`. Thus, on the material numeric domain, the result
must:

- contain exactly the elements whose numeric comparison with zero is true;
- preserve input order, values, and duplicates;
- exclude negative values, positive or negative zero, and NaN; and
- work for arbitrary finite list length, including the empty list.

The candidate implementation initializes an empty result, visits each element
once, appends it exactly when `x > 0.0`, and returns the result. For Python
integers and floats, comparison with `0.0` has the same sign-boundary behavior
as the canonical comparison with `0`.

### Trusted regeneration

From the scratch copy, the exact command

```text
python3 py2mpy.py solution.py > solution.regenerated.mpy
```

produced SHA-256
`b9455a2ae9ed9ff9ab9de9a7f6d2dd9f8e209e09c22be9105e260af224e85169`,
identical to the submitted `solution.mpy`; `cmp` exited 0. See
[`evidence/02-regeneration.log`](evidence/02-regeneration.log).

### Independent differential test

The reviewer-authored
[`evidence/differential_test.py`](evidence/differential_test.py) imports the
trusted and candidate Python entry points independently. It covers the two
documented examples, empty and singleton lists, every comparison boundary,
mixed signs, duplicates, extreme integers, subnormal floats, infinities, NaN,
and 1,000 deterministic generated lists of lengths 0 through 40. The exact
seed and fixed inputs are printed in
[`evidence/02-differential.log`](evidence/02-differential.log).

Result: 1,017 cases, zero mismatches, exit 0. This is finite bridge evidence,
not a substitute for the K proof.

## 3. Clean proof reconstruction

Only source files were copied to `/tmp/audit-work/proof`; the trusted semantics
tree was copied from `/reference`, and none of the candidate's
`*-kompiled` directories or caches was copied. The copied-source hashes are in
[`evidence/01-scratch-copy.log`](evidence/01-scratch-copy.log). The live tools
are K 7.1.293
([`evidence/03-toolchain.log`](evidence/03-toolchain.log)).

Fresh builds:

| Definition | Exact build | Result |
|---|---|---|
| Concrete | `kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition audit-runtime-kompiled` | exit 0; [`03-kompile-runtime.log`](evidence/03-kompile-runtime.log) |
| Bridge-free proof | `kompile --backend haskell verification.k --main-module VERIFICATION-BASE --syntax-module MPY-SYNTAX --output-definition audit-connection-kompiled` | exit 0; [`03-kompile-connection.log`](evidence/03-kompile-connection.log) |
| Target proof | `kompile --backend haskell verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition audit-verification-kompiled` | exit 0; [`03-kompile-verification.log`](evidence/03-kompile-verification.log) |

Each bridge-free connection claim was selected and run independently. Every
command exited 0 and printed `#Top`:

| Claim | Evidence |
|---|---|
| `compare-int-connection` | [`03-kprove-connection-compare-int.log`](evidence/03-kprove-connection-compare-int.log) |
| `compare-float-connection` | [`03-kprove-connection-compare-float.log`](evidence/03-kprove-connection-compare-float.log) |
| `applycmp-int-connection` | [`03-kprove-connection-applycmp-int.log`](evidence/03-kprove-connection-applycmp-int.log) |
| `applycmp-float-connection` | [`03-kprove-connection-applycmp-float.log`](evidence/03-kprove-connection-applycmp-float.log) |

The loop claim alone exited 0 and printed `#Top`
([`evidence/03-kprove-filter-loop.log`](evidence/03-kprove-filter-loop.log)).
The required complete target command

```text
kprove spec.k --definition audit-verification-kompiled --spec-module SPEC
```

ran both the invariant and entry claims together, exited 0, and printed
`#Top`; see
[`evidence/03-kprove-complete-spec.log`](evidence/03-kprove-complete-spec.log).

For completeness, selecting only `SPEC.get-positive` removes the
`SPEC.filter-loop` circularity and therefore unrolls an arbitrary-length list.
That diagnostic was interrupted; it is not the candidate's complete target
command and is documented in
[`evidence/03-isolated-entry-diagnostic.txt`](evidence/03-isolated-entry-diagnostic.txt).
The complete module run above is the authoritative entry-proof reconstruction.

The fresh LLVM definition also executed six reviewer assertions, covering the
examples, empty input, zero, mixed floats, the ground adequacy witness, and
100-digit signed integers. `krun` exited 0 with `<exc>NoExc</exc>` and
`<exit-code>0</exit-code>`; see
[`evidence/concrete_test.py`](evidence/concrete_test.py),
[`evidence/03-concrete-translate.log`](evidence/03-concrete-translate.log), and
[`evidence/03-krun-concrete.log`](evidence/03-krun-concrete.log).

The compiler warnings concern unused variables in the fixed `strLt` rules and
the supplied total abstraction for out-of-bounds `valSeqAt`; neither construct
is used by this program. No positive target emitted a stuck state or backend
error.

## 4. Adequacy and real-program pinning

### Claims in plain language

`SPEC.filter-loop` starts at the actual `#loop` for the submitted `for x in l`
body. Its precondition says that the remaining sequence `VS` is an arbitrary
finite sequence of MPY integers or floats. The current scope binds `positive`
to heap reference `H` and `x` to an arbitrary value; heap `H` contains the
already accumulated sequence `ACC`. If the loop terminates, the claim says
that the loop computation is consumed and heap `H` contains
`filterPositive(ACC, VS)`. The final `x` is intentionally unconstrained because
it is not observed after the loop. Other cells and unrelated map entries are
framed.

`SPEC.get-positive` starts from the exact function definition followed by a
call with symbolic `list(VS)`, where `numericVals(VS)` holds. It begins with the
module scope and builtins scope, empty heap, fresh heap location 0, empty
control stack, no return, no exception, and exit code 0. If execution
terminates, it must return `ref(0)`; heap location 0 must contain exactly
`list(filterPositive(.ValSeq, VS))`; heap allocation advances to 1; and the
stack, return, exception, and exit-code cells have their normal final values.
The return is therefore not a free variable, tautology, or one-way implication.

### Mechanical program identity

[`evidence/constructor_identity.py`](evidence/constructor_identity.py)
extracts balanced constructor terms rather than comparing prose. After
normalizing only the K parser's equivalent explicit/omitted empty list units:

- the trusted-regenerated `FuncDef` and the claim's executed `FuncDef` have the
  same SHA-256,
  `46d3239eef284f0a67f4c92b7549f7781772f17e2f57256f7aaf909ac76b52d9`;
- the function name and parameter are exactly `get_positive` and `l`;
- the executed function body exactly equals the body installed in
  `closureVal`;
- the closure is installed at module scope 0; and
- the continuation calls that installed binding with symbolic `list(VS)`.

All checks are true in
[`evidence/04-constructor-identity.log`](evidence/04-constructor-identity.log).
The outer submitted `Module(...)` is the only omitted wrapper:
the fixed rule `#loadAll(Module(SS)) => SS` removes it before executing the
same `FuncDef`. This is a demonstrated semantically inert normalization, not a
substituted program.

The real control-flow path is:

```text
Module/load → FuncDef binding → callee/argument evaluation → new frame
→ empty-list allocation → assignments → list iteration
→ comparison/branch → in-place append or skip → return/frame pop
```

Every material operation is executed by the fixed semantics. The helper claim
anchors exactly at the `#loop` reached by that path.

### Satisfiable state and concrete substitution

The ground sequence `[-1, 0, 2, 0.5, -3.25]` satisfies `numericVals`. Substituting
it for `VS` makes the claim's filter result `[2, 0.5]`; both trusted and
candidate Python implementations return `[2, 0.5]`. The exact K constructor
substitution and atom values are recorded by
[`evidence/ground_witness.py`](evidence/ground_witness.py) in
[`evidence/04-ground-witness.log`](evidence/04-ground-witness.log), and the
same input succeeds under the fresh LLVM semantics.

The candidate's body-sensitivity claim was also independently rebuilt and run
against the fresh definition. It changes the executed positive branch from
`append(x)` to `NoneVal` while retaining the original expected result. The
artifact built successfully, then `kprove` exited 1 with
`WarnStuckClaimState` and an empty actual result list:
[`evidence/04-body-mutation-build.log`](evidence/04-body-mutation-build.log) and
[`evidence/04-body-mutation-proof.log`](evidence/04-body-mutation-proof.log).
This changes the theorem's actual program term, not merely `solution.py`.

The formal domain is inductive `ValSeq`, not a bounded collection of examples
or fixed sizes. It covers arbitrary finite mixed lists of the MPY semantics'
material numeric values, integers and floats.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The reviewer-authored
[`evidence/k_rule_inventory.py`](evidence/k_rule_inventory.py) inventories every
`requires`, module/import, configuration, syntax declaration, context, rule,
attribute, and claim in the supplied tree, `verification.k`, `spec.k`, and
`spec-connection.k`. Its bounded output is
[`evidence/04-k-rule-inventory.log`](evidence/04-k-rule-inventory.log).

The supplied baseline contains 227 syntax declarations, five explicit
contexts, one configuration, and 695 rules. `verification.k` adds exactly four
syntax declarations and ten rules. The specs add two target claims and four
connection claims. There is no hidden proof-local helper file imported by the
target definition.

### Used-constructor mapping

| Submitted constructor | Declaration and material fixed rules |
|---|---|
| `Module`, statement sequence | `syntax.k`; `core.k` `#loadAll`, statement sequencing, and `.Stmts` rules |
| `FuncDef`, `Params` | `syntax.k`; `functions.k` installs the exact `closureVal` |
| `Call`, `Name` | `call.k` left-to-right callee/argument evaluation; `core.k` scope-chain lookup; `call.k` closure dispatch/frame push |
| `Expr(Str(...))` | `str.k` ASCII string literal rule; `controls.k` discards the evaluated expression value |
| `Assign` | strict RHS evaluation from `syntax.k`; `controls.k` writes the current scope |
| `ListExpr()` | `list.k` left-to-right element evaluation and `#alloc`; `core.k` heap/fresh-location update |
| `Int`, `Float` | `core.k` integer literal rule; `float.k` float literal rule |
| `For`, `#loop` | `controls.k` evaluates the iterable once and uses `#iterNext/#loopStep`; `list.k` supplies empty/cons iterator cases |
| loop target `Name("x")` | `tuple.k` `#bindTgt(Name, V)` scope update |
| `Compare`, `CmpOp(">")` | `operators.k` left-then-right contexts and `applyCmp` dispatch; `float.k` owns float and mixed Int/Float `>` |
| `If` | strict condition evaluation; `controls.k` `truthy(Bool)` and disjoint true/false branch rules |
| `Attribute`, method `Call` | `call.k` creates a bound method after evaluating the receiver, then evaluates arguments left-to-right |
| `append` | `list.k` mutates exactly the referenced heap list by tail concatenation and returns `noneV` |
| `Return` | strict expression evaluation; `functions.k` sets `retV`, restores the caller, removes the callee scope, and preserves escaping heap objects |

The fixed configuration exposes all state relevant here: `<k>`, `<env>`,
`<scopes>`, `<scopeLoc>`, `<heap>`, `<heapLoc>`, `<stack>`, `<ret>`, `<exc>`,
and `<exit-code>`. The entry claim pins every one. The loop claim changes only
the current `x` binding and the list at `H`; the body performs no output,
exception, extra allocation, return, break, or continue.

### Every proof-local declaration and rule

| Extension | Classification and domain | Soundness decision |
|---|---|---|
| `numericVal(Val):Bool [function,total]` and its equation | Definitional summary over all `Val`, using generated sort predicates `isInt` and `isFloat` | True and total. It affects only the precondition/guards and replaces no execution. |
| `numericVals(ValSeq):Bool [function,total]`; empty and cons equations | Definitional summary over the two `ValSeq` constructors | Empty/cons cases are disjoint and exhaustive; recursion strictly descends through `REST`. |
| `positiveNumeric(Val):Bool [function,total]`; Int, Float, and guarded nonnumeric equations | Definitional summary of the fixed comparison with float zero | Int and Float are sort-disjoint; the fallback guard excludes both; together the equations are exhaustive. The Int and Float RHS terms exactly match fixed `float.k` dispatch. |
| `filterPositive(ValSeq,ValSeq):ValSeq [function,total]`; empty, keep, and drop simplifications | Mathematical accumulator summary | Empty/cons are disjoint. The keep/drop guards are Boolean complements, so they are exhaustive and non-overlapping. Recursion descends through `REST`. `valSeqConcat(ACC,singleton)` preserves order and duplicates. |
| Guarded `applyCmp(">",V,0.0) => positiveNumeric(V) [simplification]` | Operational bridge over exactly `numericVal(V)` | Sound. On Int it is `gtF(intToF(I),0.0)` and on Float it is `gtF(F,0.0)`, exactly the fixed rules. All four bridge-free universal connection claims close without importing this rule. It is a pure equation: no cell, binding, evaluation order, continuation, control, state, exception, or allocation is changed. The guard excludes every other `Val`. |

There are no proof-local `symbol`, `no-evaluators`, `functional`, `concrete`,
`owise`, or priority declarations. All four local functions are fully
equationally defined. The four local simplification uses are the three
filter equations and the guarded comparison twin.

The supplied `float.k` has duplicate mixed Int/Float dispatch equations in two
sections, but their guards and right-hand sides agree exactly. The imported
opaque symbols `intToF` and `gtF` are fixed semantics primitives, not
candidate-added oracles. The bridge-free claims establish that both the
unextended program comparison and the candidate summary reach the identical
opaque term; the candidate cannot choose its value to force a postcondition.

No local rule is unsound, answer-encoding, globally false on its guard, or
execution-bypassing. Consequently there is no claimed unsound rule for which a
false-conclusion witness is required.

## 6. Fresh non-vacuity test

I did not rely on `/candidate/spec-vacuity.k`. The reviewer-authored
[`evidence/audit-spec-vacuity.k`](evidence/audit-spec-vacuity.k) executes the
actual submitted body on the satisfiable empty numeric list but mutates the
heap postcondition to require the fabricated result `[777]`.

First,

```text
kprove audit-spec-vacuity.k --definition audit-verification-kompiled \
  --spec-module AUDIT-SPEC-VACUITY --dry-run
```

exited 0, demonstrating a successful parse/build
([`evidence/06-vacuity-build.log`](evidence/06-vacuity-build.log)).
The same command without `--dry-run` exited 1. Its
`WarnStuckClaimState` shows normal completed execution with
`heap[0] = list(.ValSeq)`, which cannot unify with the mutated singleton
destination; the backend then reports that the configuration cannot be
rewritten further. See
[`evidence/06-vacuity-proof.log`](evidence/06-vacuity-proof.log).

This is an expected unmet result obligation, not a parser error, missing import,
timeout, unrelated crash, or unreachable mutation. The proof is
result-discriminating.

## 7. Proven versus assumed accounting

### Formally established

Under the freshly built Haskell MPY theory, for every finite `ValSeq` whose
elements are MPY integers or floats, if the exact submitted `get_positive`
execution terminates, it returns a reference to a freshly allocated list equal
to the stable filter of the input by the fixed semantics' `x > 0.0`
comparison. Order, duplicates, and original element values are preserved.
Normal scope, stack, return, exception, allocation, and exit-code behavior is
also constrained by the entry claim.

The loop characterization is proved coinductively for arbitrary sequence
length. The comparison bridge's value equivalence is separately proved under
the bridge-free definition. The theorem is therefore about the actual body,
not an opaque summary of a program-defined function.

### Trust ledger

| Boundary | Effect and dependents | Assessment |
|---|---|---|
| K 7.1.293 parser, kompiler, Haskell backend, and reachability/circularity implementation | All machine-checked claims | Standard proof-tool trust boundary; independently rebuilt and exercised. |
| Exact supplied MPY semantics tree | Defines the Python subset, evaluation order, cells, calls, lists, comparisons, and control | Authorized fixed semantics for this condition; recursively byte-identical to the trusted mount. |
| K mathematical hooks and built-in Int/Bool/String/Map/List theories | Equational reasoning and configuration maps/lists | Standard low-level semantics boundary. |
| Supplied `intToF` and `gtF` (`function,total,symbol,no-evaluators`) | Determine the comparison branch and therefore the result through `positiveNumeric` | Acceptable low-level external primitive boundary. The proof is interpretation-parametric and the bridge-free claims connect execution to exactly the same term. Their `[concrete]` rules instantiate binary-float conversion and `>Float`; fresh LLVM tests and 1,017 CPython differential cases support that bridge, but finite tests are not presented as a universal theorem. |
| Trusted `py2mpy.py` | Connects `solution.py` to the submitted constructor program | The translated bytes were regenerated exactly; constructor-level claim identity was then checked mechanically. |
| CPython/canonical agreement with the supplied subset | Connects the formal result to HumanEval intent | Supported by direct source inspection, the sign-boundary argument for comparison with zero, and independent differential evidence. It does not replace the K proof. |

The theorem is partial correctness: it does not claim termination or behavior
for non-list inputs, nonnumeric list elements, arbitrary Python objects with
custom comparison, concurrency, I/O, or exceptions outside the supplied
subset. Those exclusions do not materially narrow this HumanEval contract,
whose stated values are list elements that are numbers; arbitrary finite mixed
integer/float lists are covered symbolically.

The opaque float boundary is not a smuggled correctness conclusion: it is
fixed, external to the program, concretely instantiated by the supplied
semantics, and the symbolic theorem remains valid for every interpretation of
the primitive. No material adequacy or soundness gap remains.

VERDICT: PASS
LEGITIMACY: LEGIT
