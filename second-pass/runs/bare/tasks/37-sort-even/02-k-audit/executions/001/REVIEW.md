# Independent adversarial review: 37-sort-even

## Decision

The candidate contains a legitimate, non-vacuous partial-correctness proof of
the submitted constructor program under its generated, idealized integer-list
semantics. The formal theorem is narrower than the English contract: it proves
equality to recursively defined reference functions, while the fact that those
functions mean “sort the even-indexed values and preserve the odd-indexed
values” is an unchecked mathematical induction. The bridge to concrete CPython
also assumes normal execution with an unbounded call stack. Those limitations
make the result `CONCERNS / LEGIT`, not `PASS`.

All candidate claims, logs, compiled definitions, and prose were treated as
untrusted. All executable checks used source copied to
`/tmp/audit-work/37-sort-even`; no candidate-provided compiled definition was
used.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `GENERATED_SEMANTICS`.
`/reference/reference-semantics` is absent as required. This is not an
infrastructure-breach case, so a candidate verdict is appropriate.

### Trusted/candidate comparisons

`/candidate/prompt.py` is byte-identical to `/reference/prompt.py` (SHA-256
`82b621b23095040636b376f49469c4fc1d951c6563fed5aae1f5460f60ba7696`).
`/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py` (SHA-256
`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`).
The complete type listing found only regular files and directories under
`/candidate`; there are no symlinked artifacts.

The required source deliverables are present and regular:

- `solution.py`, `solution.mpy`
- `semantic.k`, `verification.k`, `spec.k`
- `prove.sh`
- the unchanged prompt and translator copies

There are no generated helper K source files beyond `semantic.k` and
`verification.k`. Extra non-source artifacts are the two candidate-built
`*-kompiled` directories, `__pycache__`, generation logs, metrics, and the
structured trace. They were inventoried and ignored for reconstruction.

`run-input.json` claims problem `37-sort-even`, condition `bare`, and no supplied
semantics. `metrics.json` claims a successful, non-timed-out generation.
`codex-last.txt`, `codex-output.log`, and the trace claim that the combined proof
printed `#Top`. The structured trace has 432 valid JSONL records and no malformed
record. These are provenance claims only; none was used as proof evidence.

Evidence:

- `/audit-output/evidence/01-integrity.log`
- `/audit-output/evidence/02-provenance-claims.log`
- `/audit-output/evidence/02b-trace-summary.log`
- `/audit-output/evidence/00-toolchain.log`

The first trace-summary attempt in `02-provenance-claims.log` ends in a reviewer
script sorting error. It was fixed and superseded by the successful
`02b-trace-summary.log`.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementations

The trusted prompt requires `sort_even(l)` to return a list with:

1. exactly the original values at odd indices; and
2. the multiset of original even-index values, sorted into the even indices.

The trusted canonical slices the even and odd positions, sorts the even slice,
and interleaves it with the unchanged odd slice.

The submitted program uses a different but recognizable algorithm:

- `even_values` recursively extracts positions 0, 2, 4, ...;
- `sort_values` and `insert_sorted` perform insertion sort;
- `rebuild` interleaves the sorted evens with the original odd positions.

For ordinary finite integer lists this implements the same transformation.

### Translator pin

Running the trusted translator on the scratch copy of `solution.py` produced a
file byte-identical to submitted `solution.mpy`; both hashes are
`2144d649be69f3df37e515fc281c34f70df737cbf97bf684bbf41956d31f050f`.
See `/audit-output/evidence/03-regenerate-mpy.log`.

### Independent differential testing

`/audit-output/evidence/differential_test.py` imports the trusted canonical and
the submitted entry point independently. It also uses a third oracle:

```python
result = list(values)
result[::2] = sorted(values[::2])
```

The ordinary test scope was:

- both documented examples;
- empty, singleton, both parities, negative values, equality/duplicate cases,
  insertion-front/insertion-later boundaries, and large-magnitude integers;
- all 19,531 lists of lengths 0 through 6 over `[-2, -1, 0, 1, 2]`;
- 1,000 deterministic generated lists, seed 370037, lengths 0 through 25.

Those 20,543 cases had zero result mismatches and zero input mutations
(`/audit-output/evidence/04-differential.log`). Exact generated inputs are in
`/audit-output/evidence/differential-inputs.json`.

An expanded boundary run added the descending integer list of length 2,000.
The canonical and direct oracle returned the same 2,000-element list, while the
submitted recursive Python raised:

```text
RecursionError: maximum recursion depth exceeded in comparison
```

That is the sole mismatch among 20,544 cases
(`/audit-output/evidence/04b-differential-resource-boundary.log` and
`differential-inputs-expanded.json`). It is a real total-correctness/CPython
resource limitation. Because the requested theorem is partial correctness, it
does not exhibit a normally returned wrong value, but it prevents treating the
K model as an unconditional concrete-CPython execution model.

The prompt does not explicitly restrict element types. The generated semantics
models integer list elements only. This is another stated intent-domain
restriction rather than a hidden strengthening.

## 3. Clean proof reconstruction

### Toolchain and clean builds

The independent toolchain is K `v7.1.293` and Python `3.10.12`.

The generated semantics was freshly compiled with:

```text
kompile semantic.k --backend llvm --main-module MPY \
  --syntax-module MPY-SYNTAX --output-definition semantic-audit-kompiled
```

It exited 0. The compiler warned that the `[total]` function `headInt` has a
non-exhaustive match; that warning is analyzed in stages 5 and 7.

The proof definition was freshly compiled with:

```text
kompile verification.k --backend haskell --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-audit-kompiled
```

It exited 0. See `05-kompile-semantic-llvm.log` and
`07-kompile-verification-haskell.log`.

### Concrete generated-semantics execution

Fresh LLVM `krun` executions on empty, singleton, two-element, both documented,
negative, duplicate, and longer even-length cases all exited 0. Each K result
matched the submitted Python, trusted canonical, and direct contract oracle.
The final examples include:

```text
[5, 6, 3, 4]       -> [3, 6, 5, 4]
[-1, 7, -3, 6, 0] -> [-3, 7, -1, 6, 0]
[2, 9, 2, 8, 1, 7] -> [1, 9, 2, 8, 2, 7]
```

See `/audit-output/evidence/06c-concrete-semantics-differential.log`.
`06b` is a superseded reviewer-harness run whose empty input used the invalid
surface spelling `pyList()`; `06c` correctly uses `pyList(.List)`.

An attempted K run on the length-2,000 resource witness was killed while the K
frontend parsed the very large configuration (exit 137), before semantic
execution. This is an audit-infrastructure limit and is not used as a candidate
failure. It remains visible in
`/audit-output/evidence/06d-concrete-semantics-resource-boundary.log`.

### Positive proof claims

The candidate has ten positive claims. Every claim closes in a clean proof run
with its required circularity dependencies:

| Claim | Fresh result |
|---|---|
| `empty-example` | isolated `#Top`, exit 0 |
| `prompt-example` | isolated `#Top`, exit 0 |
| `first-prompt-example` | isolated `#Top`, exit 0 |
| `symbolic-four-ordered` | isolated `#Top`, exit 0 |
| `symbolic-four-reversed` | isolated `#Top`, exit 0 |
| `even-correct` | isolated `#Top`, exit 0 |
| `insert-correct` | isolated `#Top`, exit 0 |
| `sort-correct` | `#Top`, exit 0 with its `insert-correct` dependency |
| `rebuild-correct` | isolated `#Top`, exit 0 |
| `top-correct` | `#Top`, exit 0 with the four helper dependencies |

The per-claim logs are `08-kprove-*.log`. Selecting `sort-correct` while
excluding `insert-correct` produces the expected stuck recursive insertion
obligation. Selecting `top-correct` while excluding all helper claims did not
finish promptly and was reviewer-interrupted; this diagnostic is not treated
as a target failure. The dependency-explicit successful runs are:

- `/audit-output/evidence/09a-kprove-sort-with-dependency.log`
- `/audit-output/evidence/09b-kprove-top-with-dependencies.log`

Finally, a clean run selecting the complete submitted claim set printed `#Top`
and exited 0:

- `/audit-output/evidence/09c-kprove-all-claims.log`

Thus the candidate's intended positive proof command is independently
reconstructed.

## 4. Adequacy and real-program pinning

### Claim meanings

All claims also require the exact `<program> solutionProgram() </program>`
cell. Their plain-language preconditions and postconditions are:

| Claim(s) | Preconditions | Postcondition |
|---|---|---|
| Three concrete examples | Fixed integer list; no side condition | Exact fixed result list |
| `symbolic-four-ordered` | Four arbitrary integers and `A <= C` | Original list; odd `B,D` unchanged |
| `symbolic-four-reversed` | Four arbitrary integers and `A > C` | `C,B,A,D`; odd `B,D` unchanged |
| `even-correct` | Any modeled list `L` | `even_values(L)` returns `evenPositions(L)` |
| `insert-correct` | Integer `X`, modeled list `L` | `insert_sorted(X,L)` returns `insertReference(X,L)` |
| `sort-correct` | Any modeled list `L` | `sort_values(L)` returns `sortReference(L)` |
| `rebuild-correct` | Modeled lists `L,EVENS` | `rebuild` returns `rebuildReference(L,EVENS)` |
| `top-correct` | Any modeled list `L` | `sort_even(L)` returns `sortEvenReference(L)` |

Realizable witnesses exist for every precondition:

- the three listed concrete inputs;
- `A=1,B=2,C=3,D=4` for `A <= C`;
- `A=3,B=2,C=1,D=4` for `A > C`;
- `L=.List` for `even-correct`, `sort-correct`, and `top-correct`;
- `X=0,L=.List` for `insert-correct`;
- `L=.List,EVENS=.List` for `rebuild-correct`.

Nonempty ground substitutions for the reference functions also printed `#Top`
in `/audit-output/evidence/10g-adequacy-ground-witnesses.log`. For the
satisfying input `[5,6,3,4]`, the formal destination reduces to
`[3,6,5,4]`, which equals both Python results and the concrete K result.

### Exact program identity

The specification does not load `solution.mpy` dynamically; it uses the
nullary function `solutionProgram()`. I independently checked this bridge:

1. `solution.mpy` was regenerated with the trusted translator.
2. K's parser normalized that trusted output.
3. A reviewer script extracted the balanced `Module(...)` term from the
   `solutionProgram()` rule.
4. K's parser normalized the extracted term.
5. The normalized files compared byte-for-byte equal, both with SHA-256
   `66b85b0045c62274f2f1333be348059763fd0524496d03f1e986bb36792c4553`.

See `/audit-output/evidence/10i-program-term-byte-pinning.log`,
`extract_solution_program.py`, `normalized-solution.mpy`, and
`normalized-extracted-solution-program.mpy`.

Earlier `10a`, `10d`, `10f`, and `10h` logs preserve unsuccessful reviewer
attempts to express or parse a bare functional equality claim. They are
superseded by the successful parsed-term comparison; they are not target-proof
failures.

The body-sensitivity test changed only the encoded `sort_even` body to
`return l`, rebuilt a separate Haskell definition successfully, and reran the
top theorem with its helpers. The proof failed with an unmet condition
`L == rebuildReference(...)`, as expected:

- `/audit-output/evidence/verification-body-mutated.k`
- `/audit-output/evidence/14a-body-mutated-kompile.log`
- `/audit-output/evidence/14b-body-mutated-proof-expected-failure.log`

This confirms that the top theorem depends on the real encoded function body.
The earlier functional-only mutation attempt in `11b` was rejected by a
backend limitation and is not used as sensitivity evidence.

### Result constraint

`top-correct` is not a free-result or implication-only claim. Its terminal
`<k>` value is exactly `pyList(sortEvenReference(L))`; the program cell is
pinned, and cell ellipses preserve the same continuation frame. The semantics
is deterministic over the used fragment. The false-result mutation in stage 6
also confirms that the result equality is genuinely required.

## 5. Rule-by-rule static soundness review

The complete numbered sources and declaration/rule extraction are in
`/audit-output/evidence/13-rule-inventory-source.log`.

### Syntax, configuration, and attributes

Local syntax in `MPY-SYNTAX` declares:

- `Program = Module(Stmts)`;
- list-backed `Stmts`, `Strings`, `Exprs`, and `CmpOps`;
- statements `FuncDef`, `Return`, and `If`;
- `Params`;
- expressions `Int`, `Name`, `ListExpr`, `BinOp`, `Compare`, `Subscript`,
  `Slice`, and `Call`;
- `CmpOp`, bounds (`Expr` or `NoBound`), and runtime `pyInt`, `pyBool`,
  `pyList`.

Local runtime syntax declares the 16 continuation/control symbols from `run`
through `listItemResult`, the internal `comparison` value, the concrete
`function` value, and four functions:

- `findFunction` `[function]`;
- `bind` `[function]`;
- `dropList` `[function,total]`;
- `headInt` `[function,total,smtlib(headInt)]`.

`VERIFICATION` adds the `[function]` constant `solutionProgram` and six
`[function]` list symbols: `evenPositions`, `oddPositions`,
`insertReference`, `sortReference`, `rebuildReference`, and
`sortEvenReference`.

There are no local `functional` declarations distinct from `[function]`, no
local simplification rules, no priority rules, and no `owise` rules.
`headInt` is the only local SMT/opaque boundary.

The configuration contains only:

- `<k>` for computation; and
- read-only `<program>` for the parsed constructor program.

There is no hidden heap, output, exception, or mutable global-state cell.

Every constructor in submitted `solution.mpy` is declared and mapped:
`Module`, `FuncDef`, `Params`, `If`, `Compare`, `Name`, `CmpOp("==")`,
`CmpOp("<=")`, `ListExpr`, `Return`, `BinOp("+")`, `Subscript`, `Int`,
`Slice`, `NoBound`, and `Call`. No submitted construct relies on a fabricated
catch-all rule.

### `semantic.k`: all 39 rules

| Lines/rules | Static decision |
|---|---|
| 77 `dropList(L,0)` | Correct identity case. |
| 78-79 positive `dropList` | Correctly drops `min(I,size(L))` leading elements for the only used starts 1 and 2. Guard is disjoint from zero. Negative starts are unsupported despite `[total]`, but no submitted AST uses one. |
| 80 `headInt(ListItem(I) REST)` | Correct nonempty integer-head projection. It is not exhaustive even though declared total; see the trust-boundary discussion below. |
| 82 `run` | Calls the submitted entry name with exactly one `PyVal`; correct. |
| 84-85 `applyFunction` | Reads the exact program and preserves arbitrary K continuation; correct. |
| 86 `applyFound` | Binds arguments and executes the selected body; correct for the modeled call discipline. |
| 88-92 two `findFunction` rules | Same-name and different-name guards are disjoint and select the first definition. Submitted function names are unique. For a broader Python module with duplicate definitions this would disagree with Python's later-binding behavior, but no such state occurs here. |
| 94-96 two `bind` rules | Correct recursive positional binding for equal arities. Actual calls have exact arity. Mismatched arity is visibly unsupported. |
| 98 `exec(Return...)` | Correctly abandons trailing statements on return. |
| 99-100 `exec(If...)` | Evaluates the condition, but drops the outer `_REST`. In every submitted function the `If` is the final statement and every reachable branch returns, so this is sound on the actual program path. It is incomplete for a broader translated body such as `if xs == []: return [1]; return [2]`: on nonempty `xs`, Python returns `[2]`, while this semantics selects an empty else body after discarding the trailing return and gets stuck. This is an out-of-scope generated-language gap, not a false terminal result for submitted `sort_even`. |
| 101-108 four branch rules | Equality/inequality and less-or-equal/greater guards are pairwise disjoint and exhaustive over integers. They select the proper branch. |
| 110 integer literal | Correct `Int` to `pyInt`. |
| 111 name lookup | Correct for the exact argument maps; no assignment/local mutation is used. |
| 112 list-expression start | Starts left-to-right element evaluation with an empty accumulator. |
| 113-117 three `+` rules | Evaluate left then right and concatenate runtime lists in order; exactly the submitted uses. |
| 119-124 comparison setup | Evaluates the left operand before the right and retains operand order. |
| 125-126 list-empty equality | Correctly implements only the used pattern `list == []`. Other list equality is intentionally unmodeled. |
| 127 integer equality | Operand bookkeeping yields the original left/right integer order; equality is correct. |
| 128 integer `<=` | Operand bookkeeping yields `left <= right`; correct. |
| 130-133 index/slice setup | Covers exactly integer indexing and positive-start/open-end slicing used by the program. |
| 135 index result | Correct on a nonempty integer list and in-range nonnegative index. Actual entry executions use only index 0 after an emptiness/length check. Out-of-range behavior is not modeled as Python `IndexError`. |
| 137 slice result | Correctly drops the positive prefix for starts 1 and 2. |
| 139-146 four call/argument rules | Resolve named functions and evaluate arguments left-to-right while preserving the active continuation. Actual global bindings are unique and fixed. |
| 148-152 three list-item rules | Evaluate list elements left-to-right and require integer results. All submitted list literals contain integer-valued expressions. |

No semantic-rule overlap was found outside the explicitly disjoint guards.
There is no priority rule that can preempt ordinary execution.

`headInt` deserves separate attention. For `ListItem(I:Int) REST`, its equation
fixes the value exactly, so it is not an oracle on valid uses. On `.List`, on a
list headed by a non-Int K item, or after an invalid index, `[total]` leaves an
opaque integer term instead of modeling Python `IndexError`/type failure. A
concrete off-domain witness is the internal call `rebuild([1], [])`: Python
raises `IndexError`, whereas the K helper/reference pair can both contain
`headInt(.List)`. The public `sort_even` path never calls `rebuild` with too few
even values; that fact follows by an ordinary length induction, but it is not
a machine-checked invariant. This totalization is therefore a documented
concern and trust condition, not evidence that a wrong public result can be
proved on a normally returning integer-list input.

### `verification.k`: all 13 rules

| Lines/rules | Static decision |
|---|---|
| 8-65 `solutionProgram` | Definitional constant, not an execution bridge. Independently equal to trusted translation as shown in stage 4. |
| 75-79 two `evenPositions` rules | Empty/nonempty guards are disjoint and exhaustive. Nonempty case emits the head and recurs after dropping two; correct even-index extraction. |
| 81 `oddPositions` | Drops one then extracts even positions, correctly defining odd positions. It is unused by the proof. |
| 83-92 three `insertReference` rules | Empty, nonempty/front, and nonempty/recurse cases are disjoint. They define insertion before the first value not less than `X`; correct for integer lists. |
| 94-98 two `sortReference` rules | Empty base and nonempty recursive insertion-sort definition; structurally decreases by one. |
| 100-109 three `rebuildReference` rules | Empty, singleton, and length-at-least-two cases are disjoint and interleave an even value with the original odd value. They assume enough values in `EVENS`; the valid top-level call satisfies that invariant. |
| 111-112 `sortEvenReference` | Composition of extraction, insertion sort, and rebuild; a truthful deterministic summary. |

The reference functions have no overlapping inconsistent equations. Recursive
calls strictly reduce a concrete list by one or two elements. They do not
rewrite an operational program term and cannot bypass the submitted bodies.

### Proof-extension and helper-claim inventory

- `solutionProgram` is a definitional source-term constant, with exact parsed
  identity evidence.
- The six reference functions are definitional mathematical summaries.
- `even-correct`, `insert-correct`, `sort-correct`, and `rebuild-correct` are
  derived reachability lemmas/circularities. Each begins at the exact real
  helper invocation, preserves the exact program and arbitrary continuation,
  and connects actual execution to its corresponding reference definition.
- `top-correct` composes those exact helper connections. There is no rule of the
  form “program call rewrites directly to desired answer.”
- The concrete/symbolic example claims are additional consequences, not
  axioms.

All operational state is in the K continuation and read-only program cell.
Calls and returns preserve the continuation admitted by the helper claims; no
control stack, output, allocation, or mutable state is omitted. The
body-mutation test confirms execution sensitivity.

The reference definitions do encode the candidate algorithm closely. That
makes the proof an execution-refinement theorem, not by itself a theorem that
the recursive result satisfies the English sortedness/permutation property.
It is not circular in the proof-extension sense because the program bodies
execute and are connected to separately reducing reference terms.

## 6. Fresh non-vacuity test

The reviewer-created mutation is
`/audit-output/evidence/spec-vacuity-audit.k`. It changes only the universal
top result from:

```k
pyList(sortEvenReference(L))
```

to:

```k
pyList(ListItem(0) sortEvenReference(L))
```

and renames the module/label. `L=.List` is a satisfying witness: the actual
result is `[]`, while the mutation requires `[0]`.

The mutated spec parsed and compiled successfully under `kprove --dry-run`
(exit 0, `12a-vacuity-mutation-dry-run.log`). The real proof then exited 1 with
`WarnStuckClaimState`. Its residual explicitly says the actual
`rebuildReference(...)` result is not equal to
`ListItem(0) rebuildReference(...)`:

- `/audit-output/evidence/12b-vacuity-mutation-expected-failure.log`
- generator: `/audit-output/evidence/generate_false_postcondition.py`

This is the expected unmet result obligation, not a parser error, timeout, or
unreachable mutation. Gate A5 passes.

## 7. Proven versus assumed accounting

### What the machine-checked proof establishes

Under the rules in freshly compiled `semantic.k`, for every modeled list term
`L`, executing the exact translated `sort_even` constructor program reaches:

```text
pyList(sortEvenReference(L))
```

The helper proofs establish the corresponding exact execution summaries for
`even_values`, `insert_sorted`, `sort_values`, and `rebuild`. The two symbolic
length-four claims further establish both integer order branches. This result
is body-sensitive and result-constraining.

### Trust ledger

| Boundary | Influence and dependents | Assessment |
|---|---|---|
| K built-ins: arbitrary integers, Boolean connectives, strings, maps, list `size`, `range`, concatenation, and `minInt` | All semantic and reference rules | Ordinary low-level K trust boundary; acceptable. |
| `dropList` as positive Python slicing | Extraction, sorting tails, rebuild tails | Equations are correct for used starts 1 and 2; finite K/Python evidence supports them. Negative slicing is excluded. |
| `headInt`/`smtlib(headInt)` | Indexing, comparisons, every reference function | Exact on nonempty Int-headed lists. Empty/non-Int behavior is opaque because of non-exhaustive `[total]`; concerning and conditionally accepted only because public entry executions are structurally in range. |
| Integer-list-only runtime model | All universal claims | Prompt does not state an element type. This is a real scope restriction. |
| Unique global function names and exact arities | Function lookup/binding | True of the pinned submitted term; checked statically. |
| No Python exceptions, recursion limit, memory limit, or other resource exhaustion | Concrete-Python bridge and termination behavior | The 2,000-element witness demonstrates the limitation. Acceptable only as an idealized normal-return partial-correctness boundary; it blocks a total-correctness or unconditional CPython claim. |
| Reference-to-English meaning | Natural-language contract | Informal induction: `evenPositions` extracts evens; `insertReference` inserts; `sortReference` insertion-sorts and preserves the multiset; `rebuildReference` copies original odds and places sorted evens. This was not proved as a separate K theorem. |
| Trusted canonical and differential testing | Program/intent bridge only | 20,543 ordinary integer cases agree; one resource-boundary exception differs. Finite evidence is not a universal theorem and was not used to close K claims. |
| Trusted translator and parsed-term normalization | Source-to-constructor identity | Byte identity plus normalized term equality; strong reproducible evidence, but the translator remains a trusted frontend. |

### Gate assessment

- **Gate A — real-program soundness:** PASS for the pinned constructor program
  on normally executing finite integer-list states under the stated idealized
  primitive contracts. No result oracle, false operational bridge, or vacuity
  was found. The out-of-range `headInt` and general-language continuation gaps
  are outside the actual public path but remain explicit concerns.
- **Gate B — intent adequacy:** LIMITED. The reference-to-English induction is
  informal, element types are restricted to integers, and concrete CPython can
  raise `RecursionError` on an unrestricted valid list length.
- **Gate C — auditability:** PASS. Builds, per-claim proofs, parsed-term pinning,
  ground checks, body sensitivity, differential inputs/results, mutation, and
  bounded logs are preserved under `/audit-output/evidence`.

The K proof is therefore legitimate as a partial-correctness refinement proof,
but it is not a complete machine-checked proof of the unrestricted English
contract or of total concrete-CPython behavior.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
