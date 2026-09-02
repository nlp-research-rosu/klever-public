# Independent adversarial review: 115-max-fill

This audit reconstructed the candidate from source in `/tmp/audit-work` and did
not reuse candidate-provided compiled definitions, caches, logs, traces, or the
reported `#Top`. The reconstructed proof is legitimate for the HumanEval
source-contract domain, but it has two nonfatal audit limitations: the formal K
domain is broader than the Python behavior for negative cells, and the
proof-specific `gridVal`/`rowVal` representation is connected to ordinary
Python lists by an exhaustive rule review plus finite paired executions rather
than by a separate machine-checked representation theorem.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout:
legacy-selected-stage1`, condition `bare`, and
`semantics_mode: GENERATED_SEMANTICS`. The declared container paths, not the
host-only provenance paths, were used.

The required launcher records are present as real, non-symlinked regular files:

- `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
  `/task.json`, and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`,
  `codex-last.txt`, `codex-output.log`, and `prompt.txt`;
- the structured trace under `/generation-evidence/codex-trace/`.

The optional legacy `usage.json` is also present and was inspected. The
historical runtime metrics absent from this legacy-selected-stage1 layout were
not reconstructed. Recursive inspection found only directories and regular
files in the candidate and trace trees. `findmnt` reported all launcher-owned
inputs read-only.

The campaign lock object exactly equals the `audit_campaign` block and hashes
to the recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
Every launcher-recorded individual file hash checked by the audit matched. An
independent length-delimited tree traversal produced:

- candidate tree
  `7794c14ebac8697cc228dd85e23df7ee7791094f6849777f5730c3e31b14c969`,
  matching both the generation-result workspace hash and invocation retained
  workspace hash;
- trace tree
  `9b7b57c8c71e94843ab62a6980d62a8600b5aef4401d8eac0d1cca17a2529b41`,
  matching `usage.json`;
- trace JSONL file
  `0ccb4040f7296070cc4f944f34e7790cfb43504dc82fe286b1789758fdc5138e`,
  matching the invocation and generation result.

All 319 JSONL trace records parse. The trace contains 61 recorded tool calls
and ends in an untrusted generation claim that the proof passed. The 28,750-line
generation log contains two exact `#Top` lines, but neither was used as audit
proof evidence.

The candidate `prompt.py` and `py2mpy.py` are byte-identical to the trusted
mounted versions. `/reference/reference-semantics` is absent, as required in
GENERATED_SEMANTICS mode. There is no infrastructure breach.

Evidence: [integrity script](evidence/01_integrity_and_trace.py) and
[integrity/trace log](evidence/01-integrity.log).

## 2. Program fidelity and canonical comparison

### Contract

For a rectangular grid with 1–100 rows, 1–100 binary cells per row, and bucket
capacity 1–10, `max_fill` must sum, separately for each row, the ceiling of the
row's number of ones divided by capacity.

The trusted canonical implementation is
`sum(math.ceil(sum(row) / capacity) for row in grid)`. The candidate recursively
sums each row and computes `(water + capacity - 1) // capacity`, then recursively
sums those per-row values. On the stated domain `water >= 0` and
`capacity > 0`, so this is the same ceiling formula. Its maximum recursion
depth is at most the contract's row or column bound of 100.

Running the trusted translator from the scratch copy produced a file
byte-identical to submitted `solution.mpy`; both hash to
`7d64ef28ec1ccf1567d62479e28792152036f7818b9985a45e9999c6648b470f`.
See [translator identity](evidence/02-translator-identity.log).

The independent differential test covered:

- all three prompt examples;
- empty-grid and empty-row robustness cases outside the contract;
- minimum, maximum-capacity, zero-water, ceiling boundary, and per-row
  separation cases;
- every rectangular binary grid with 1–3 rows and 1–4 columns at every
  capacity 1–10 (50,500 cases);
- 500 deterministic random rectangular binary grids with sizes up to 100×100;
- 100×100 all-zero and all-one boundaries.

It ran 51,015 cases with zero mismatches. This is finite implementation evidence,
not a substitute for the K proof. Evidence:
[differential script](evidence/02_differential.py) and
[differential log](evidence/02-differential.log).

## 3. Clean proof reconstruction

Only explicit source artifacts were copied to
`/tmp/audit-work/reconstruction`; the candidate `__pycache__` and any compiled
definition were excluded. The copy inventory is in
[02-copy-sources.log](evidence/02-copy-sources.log).

The generated semantics was rebuilt for concrete execution:

```text
kompile semantic.k --backend llvm --main-module MPY \
  --syntax-module MPY-SYNTAX --output-definition semantic-clean-kompiled
```

It exited 0. Compiler diagnostics were unused-variable warnings only; see
[03-kompile-concrete.log](evidence/03-kompile-concrete.log).

Fifteen fresh `krun` executions covered the examples, empty recursive bases,
minimum values, capacity 10, exact/above ceiling boundaries, and a case that
distinguishes per-row ceilings from a global ceiling. Examples 1 and 2, empty
grid/row, and the per-row case were each run in both ordinary nested `listVal`
and proof-typed `gridVal`/`rowVal` representations. Every run exited 0 and its
K result equaled both Python implementations. Full commands and configurations
are in [03-concrete-executions.log](evidence/03-concrete-executions.log);
the driver is [03_concrete_compare.py](evidence/03_concrete_compare.py).

The proof definition was independently rebuilt:

```text
kompile verification.k --backend haskell --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-clean-kompiled
```

It exited 0; see [03-kompile-proof.log](evidence/03-kompile-proof.log).
The sole positive target-proof command was then rerun against that clean
definition:

```text
kprove spec.k --definition verification-clean-kompiled --spec-module SPEC
```

It exited 0 and printed `#Top`, proving all three claims in `SPEC`; see
[03-kprove-positive.log](evidence/03-kprove-positive.log).

## 4. Adequacy and real-program pinning

The three claims mean:

1. For every finite `ROW:Ints`, with the exact `_water_in` binding installed,
   invoking `_water_in(rowVal(ROW))` emits `intVal(water(ROW))`. Arbitrary
   continuation, arguments, caller environment, and result cells are
   preserved.
2. For every finite `GRID:Rows` and `C > 0`, with the exact `_buckets_for`
   binding installed, invocation emits
   `intVal(requiredBuckets(GRID,C))`, again preserving the framed state and
   continuation.
3. Starting with the submitted module term, typed grid/capacity arguments,
   empty function/environment maps, and `noneVal` result, module loading and
   the `max_fill` call consume the computation and set the result to
   `intVal(requiredBuckets(GRID,C))`, for every `C > 0`.

These are result-constraining claims. In particular, the entry destination
contains the deterministic `requiredBuckets(GRID,C)`, not a free right-hand
variable or implication that can avoid equality.

Satisfying ground states were exhibited for each claim. For
`ROW = (1,0,1)`, `GRID = ((1,0,1),(0,1,1))`, and `C = 2`, the formal summaries,
candidate helpers, candidate entry point, and trusted canonical entry point
all produce the stated results. See
[04-claim-witnesses.log](evidence/04-claim-witnesses.log).

Program identity is pinned in three independent ways:

- the trusted translator regenerates the submitted `solution.mpy` byte for
  byte;
- `solution-program.k:8-43` is a constructor-for-constructor copy of that
  translated module (with only the K list terminator made explicit);
- after one module-loading step under the clean proof definition, the KORE
  states for `solution.mpy` and `solution-token.mpy` are byte-identical:
  both are 20,096 bytes and hash to
  `33b7b763ef5c2a8de49baccd99071e427cc4124b534c0936a15473aa6e47f8e4`.

See [04-program-pinning.log](evidence/04-program-pinning.log).

A body-sensitivity mutation changed the `solutionProgram` term actually
executed by the claims, replacing `_water_in([]) = 0` with `1`. With that
mutated term, the translated source program still returned 0 on `[[]],2`,
while the mutated claim program returned 1, and the original proof exited 1.
This was not a mutation of an ignored external source file. Evidence:
[mutation diff](evidence/04-body-mutation-diff.log),
[ground execution](evidence/04-body-mutation-ground.log), and
[failed proof](evidence/04-body-mutation-kprove.log).

The proof precondition uses `gridVal(Rows)` instead of generic nested
`listVal`. This does not narrow the HumanEval data: every finite rectangular
binary grid has a direct `gridVal(rowVal(...),...)` representation, and the
semantic rules for the only observed operations—empty comparison, index zero,
and suffix slice—are structurally identical for generic and typed lists.
Nevertheless, the correspondence is not itself stated as a separate universal
K theorem. That is one reason for `CONCERNS` rather than `PASS`.

## 5. Rule-by-rule static soundness review

The mechanical inventory is
[05-rule-inventory.log](evidence/05-rule-inventory.log), generated by
[05_inventory.sh](evidence/05_inventory.sh).

### Syntax, cells, and attributes

`MPY-SYNTAX` declares:

- `Module`: translated `Module(Stmts)` and the nullary `solutionProgram`
  function;
- statement sequences and `FuncDef`/`Return`;
- `Params` and comma-separated parameter strings;
- expressions `Int`, `Name`, `ListExpr`, `BinOp`, `Compare`, `IfExp`,
  `Subscript`, and `Call`;
- expression lists, comparison operators/lists, indices, slices, and
  expression/`NoBound` slice bounds.

The runtime module declares:

- values `intVal`, `boolVal`, generic `listVal`, typed `rowVal` and `gridVal`,
  and `noneVal`;
- `Vals`, `Ints`, `Rows`, `Function`, `Exprs`, `Values`, and the
  `noArgs`/`arg` argument spine;
- the configuration cells `<k>`, `<args>`, `<functions>`, `<env>`, and
  `<result>`;
- control frames `invoke`, `restoreEnv`, `binRight`, `binApply`,
  `chooseBranch`, `compareEmpty`, `subscriptIndex`, `subscriptApply`,
  `sliceFrom`, `evalCallArgs`, `collectCallArg`, `evalListItems`, and
  `collectListItem`.

The local `[function]` symbols are `solutionProgram`, `collectFunctions`,
`fromVals`, `appendArg`, `argValsToVals`, `bindParams`, `arithmetic`,
`getItem`, `dropItems`, `water`, `requiredBuckets`, `solutionFunctions`, and
`functionsOf`. There are no local `[total]`, `[functional]`,
`[simplification]`, `[concrete]`, priority, `owise`, `anywhere`, or opaque
declarations.

### All semantic rules

The 58 rules in `semantic.k` were reviewed as the following exhaustive groups:

| Lines | Count | Role and finding |
|---|---:|---|
| 81–100 | 10 | Function collection, value/argument conversion, append, and parameter binding. Empty/nonempty cases are disjoint, recursive calls descend, and every use in the submitted module has unique names and exact arity. |
| 103–106 | 3 | Integer `+`, `-`, and guarded nonzero `//`. Addition/subtraction are exact. Division is exact on the intended nonnegative numerator and positive divisor; its out-of-contract limitation is discussed below. |
| 109–120 | 6 | Generic-list, row, and grid indexing. Zero and positive-index rules are disjoint and descend. The submitted program uses only index zero on a branch-proven nonempty value. |
| 123–131 | 6 | Generic-list, row, and grid prefix dropping. Zero and positive cases are disjoint and descend. The program uses only the suffix slice starting at one. |
| 151–164 | 4 | Module loading, exact function lookup/invocation, caller-environment save, `Return`, and environment restoration. The function map is populated from the actual bodies and no call is summarized by an oracle. |
| 166–167 | 2 | Integer literal evaluation and exact environment lookup. |
| 169–171 | 3 | Left-to-right binary evaluation and application. |
| 173–175 | 3 | Condition-first `IfExp` and disjoint Boolean branches. |
| 179–186 | 7 | Evaluation of the sole used comparison, equality with `[]`, and disjoint empty/nonempty rules for all three list representations. |
| 188–195 | 5 | Base-before-index evaluation, integer subscript application, and the exact `[1:]` slice. `Expr` and `Slice` heads do not overlap. |
| 197–203 | 4 | Name-bound calls and left-to-right argument collection. |
| 205–212 | 4 | Left-to-right list-literal evaluation and collection. |
| 214–216 | 1 | A final value is consumed only when no continuation remains and the initial result is `noneVal`. |

`solution-program.k` contributes one definitional rule, expanding
`solutionProgram` to the mechanically matched translated module. It is a
program identity constant, not an execution-bypassing summary.

`verification.k` contributes exactly six rules:

- two structurally recursive, exhaustive equations for `water`;
- an empty-grid equation and a positive-capacity descending equation for
  `requiredBuckets`;
- `functionsOf(Module(SS)) = collectFunctions(SS)`;
- `solutionFunctions = functionsOf(solutionProgram)`.

The summary functions are mathematical definitions. The program-defined helper
bodies still execute; the helper reachability claims connect those executions
to the summaries. There is no fresh result-bearing oracle, abrupt-control
bridge, fabricated allocation/state change, or task-answer rewrite.

Every constructor used by `solution.mpy` maps to the syntax and rules above:
module/function/parameters/return; integer and name lookup; empty list and
empty comparison; conditional expression; `+`, `-`, `//`; calls; index zero;
and `[1:]`. The semantics models left-to-right evaluation, caller binding,
recursive control, result placement, and every state cell material to this
pure program. It intentionally omits exceptions and unused Python constructs;
all stated contract inputs avoid division by zero, invalid types, and
out-of-range accesses.

### Division limitation

`semantic.k:105` implements Python `//` with K `/Int`. The installed K domain
documents `/Int` as truncation toward zero, while Python `//` floors. For the
out-of-contract input `grid=[[-2]], capacity=2`, both Python implementations
return `-1`, while the fresh K semantics returns `0`. See
[K division documentation](evidence/05-k-int-division-doc.log) and the
[ground witness](evidence/05-out-of-domain-division.log).

This is not a false-conclusion witness on the intended domain: source cells are
only 0 or 1, so every numerator reaching division is nonnegative and the two
operations agree. The K theorem is internally sound because
`requiredBuckets` uses the same K division, and its typed domain contains the
entire required binary-grid subset. I therefore record a language-model and
overclaim limitation, not material semantic unsoundness or domain narrowing.
The untrusted generation report's statement that the result corresponds to
Python for arbitrary integer-valued rows is not established.

## 6. Fresh non-vacuity test

The reviewer-authored
[06-spec-vacuity.k](evidence/06-spec-vacuity.k) retains both exact helper
claims and changes the end-to-end destination to:

```text
intVal(requiredBuckets(GRID, C) +Int 1)
```

The intended-domain satisfying witness `GRID = rowVal(0), C = 1` executes to
0, while the mutation requires 1; the fresh concrete executions already
record that result.

The mutation parsed and built successfully with `kprove --dry-run` (exit 0);
see [06-vacuity-dry-run.log](evidence/06-vacuity-dry-run.log). The actual
mutated proof exited 1 with `WarnStuckClaimState`; the residual says the
destination unifies but the implication between `requiredBuckets(GRID,C)` and
`requiredBuckets(GRID,C) +Int 1` fails. This is the expected unmet obligation,
not a parser error, timeout, missing import, or unrelated crash. See
[06-vacuity-kprove.log](evidence/06-vacuity-kprove.log).

The proof is therefore non-vacuous and result-discriminating.

## 7. Proven versus assumed accounting

### What is machine-checked

Under the rebuilt `MPY` operational semantics and verification equations, for
every finite `GRID:Rows` and every `C > 0`, any terminating execution of the
exact submitted translated module from the specified empty initial state
returns `intVal(requiredBuckets(GRID,C))`. The helper claims establish the
corresponding row-sum and recursive grid-summary facts while preserving their
arbitrary framed continuation and state.

For HumanEval inputs—finite rectangular 0/1 rows within the stated size bounds
and capacity 1–10—the reviewed operational rules make
`requiredBuckets` equal to the natural-language sum of per-row ceilings.

### Trust and evidence ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K 7.1.293 compiler, Haskell/LLVM backends, reachability logic, and imported `INT`, `BOOL`, `STRING`, and `MAP` domains | All compilation, execution, and proof results | Ordinary unavoidable toolchain/mathematical trust boundary. |
| Trusted mounted `py2mpy.py` | Source-to-`solution.mpy` identity | The regenerated artifact is byte-identical. |
| Manual `solutionProgram` constructor constant | All symbolic claims | Mechanically equal after module loading and body-sensitive, but not automatically regenerated inside the proof build; this is a maintenance observation. |
| `rowVal`/`gridVal` as symbolic representations of nested Python lists | Universal input coverage and helper claims | Rule-by-rule structural correspondence and paired concrete evidence support the bridge, but no separate universal K representation theorem is present. Nonfatal concern because no property-bearing computation is replaced. |
| Integer identity between `(water+C-1)//C` and a ceiling for `water>=0,C>0` | Natural-language postcondition | Ordinary mathematics; the source contract guarantees the guard. |
| Trusted canonical Python and CPython executions | Implementation-intent and finite semantics checks | Independent finite evidence only; not used to close the K proof. |

There are no candidate-local opaque symbols, unconstrained result primitives,
empirical execution bridges, proof-local simplifications, assumed lemmas, or
result-bearing oracles. The proof is a partial-correctness proof; it does not
separately establish termination. Invalid types, zero/negative capacity,
out-of-range operations, and arbitrary negative-cell Python equivalence are
outside the HumanEval contract and outside the validated intent bridge.

### Decision

Clean reconstruction, actual-body pinning, claim adequacy, the exhaustive rule
review, body sensitivity, and the false-postcondition test all pass. The proof
covers the complete material HumanEval domain and does not rely on an unsound
answer shortcut. The unchecked universal representation bridge and the
out-of-contract negative-division discrepancy are real but nonfatal
trust/scope limitations. The appropriate benchmark decision is therefore
`CONCERNS / LEGIT`, not `FAIL`: no intended-domain input is excluded or given a
false proved result.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
