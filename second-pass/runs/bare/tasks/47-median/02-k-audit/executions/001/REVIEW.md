# Independent adversarial audit: 47-median

This is a completed audit under `GENERATED_SEMANTICS`. I treated every file
under `/candidate` as untrusted evidence, copied only source artifacts into
`/tmp/audit-work/47-median`, rebuilt both definitions there, and wrote
reviewer-authored artifacts and bounded logs under `/audit-output/evidence`.

The decisive result is `FAIL / NOT_LEGIT`. The K claims do close freshly and
are non-vacuous, but they do not prove the requested median implementation.
The submitted Python program deliberately implements a different even-length
formula, and the generated semantics' value-bearing model of Python `/` is
false on inputs admitted by the universal claim. In particular, K returns an
exact `floatVal` for large integers for which the real submitted Python
program raises `OverflowError`.

## 1. Input and provenance integrity

### Semantics-mode boundary

`/reference/reference-semantics` is absent, as required by
`GENERATED_SEMANTICS`. The trusted mount contains exactly the three expected
regular files:

- `/reference/prompt.py`
- `/reference/canonical.py`
- `/reference/py2mpy.py`

There is therefore no infrastructure contradiction and no hidden/supplied
semantics was used. See `evidence/stage1-integrity.sh` and
`evidence/stage1-integrity.log`.

### Required candidate artifacts

The generation deliverables and audit provenance inputs are present as regular,
non-symlink files: `prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`,
`semantic.k`, `verification.k`, `spec.k`, `prove.sh`, `run-input.json`,
`metrics.json`, `codex-last.txt`, and `codex-output.log`. The structured trace
is one regular JSONL file and all 209 records parse.

No required source artifact is missing, mistyped, or symlinked. The candidate
also contains extra generated state: `semantic-kompiled/` and `__pycache__/`.
Those are not integrity failures, but they were ignored and never copied into
the clean build. There is no candidate `PROOF.md` or `spec-vacuity.k`; neither
was a required generation deliverable, and no claim is inferred from their
absence.

The candidate prompt is byte-identical to `/reference/prompt.py`, and the
candidate translator is byte-identical to `/reference/py2mpy.py`:

```text
prompt SHA-256:
12794c9b475e4c41b878cf4d466feb8fa24d9d3dd6311f9845760f64b4748fd4
translator SHA-256:
406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16
cmp exit: 0 for both
```

The untrusted provenance says the run was `bare`, exited 0, did not time out,
and eventually obtained `#Top`. The generation log also records an earlier
stuck proof before the final successful run. Those statements were treated
only as claims and were independently reconstructed. A bounded extraction of
`run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`, and the
complete JSONL parse is in `evidence/stage1-provenance-summary.log`; the
extractor is `evidence/provenance_summary.py`.

The independently available K binaries are version `v7.1.293`.

Stage 1 result: **PASS** (provenance integrity and mode boundary).

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The trusted prompt says to return the median of the list elements. The trusted
canonical program makes that precise:

1. Sort the list.
2. For odd length, return the center element at index `n // 2`.
3. For even length, return the average of indices `n // 2 - 1` and `n // 2`
   using Python floating division.

The prompt's odd example is consistent with that contract. Its even example is
not: sorting `[-10, 4, 6, 1000, 10, 20]` gives
`[-10, 4, 6, 10, 20, 1000]`, whose conventional/canonical median is `8.0`,
while the prompt text says `15.0`. This is an intent inconsistency in the
trusted task inputs, not a semantics-mount infrastructure breach. The natural
word “median” and the executable trusted canonical agree with each other.

The candidate chose the erroneous example instead of the contract/canonical:

```python
return (ordered[middle] + ordered[middle + 1]) / 2
```

Thus it averages the two elements above the center for even lists. For length
two it indexes past the end and raises `IndexError`.

### Translation identity

Running the trusted translator on the copied `solution.py` produced a
byte-identical `solution.mpy`; both hashes are:

```text
22ebb0b2ad4475019b325a98fcf8cd283169bed4495a4e725073b98b109197f0
```

The exact commands and exits are in `evidence/stage2-fidelity.sh` and
`evidence/stage2-fidelity.log`.

### Independent differential

`evidence/differential.py` imports the trusted canonical and copied candidate
through separate module paths. It exercises:

- both documented examples;
- empty and lengths 1, 2, 3, and 4;
- odd/even branch boundaries, duplicates, negatives, rounding, and overflow;
- all 19,531 lists of lengths 0 through 6 over `{-2,-1,0,1,2}`;
- 500 deterministic random lists of lengths 0 through 20, seed `470047`.

There were 14,397 mismatches among 20,042 cases, so the differential command
correctly exited 1. Material ground divergences include:

| Input | Canonical | Candidate |
|---|---:|---:|
| `[-10,4,6,1000,10,20]` | `8.0` | `15.0` |
| `[1,2]` | `1.5` | `IndexError` |
| `[1,2,3,4]` | `2.5` | `3.5` |
| `[-9,-7,-3,-1]` | `-5.0` | `-2.0` |

The script contains the complete deterministic input construction and the log
contains all named inputs, scope parameters, totals, and bounded mismatch
samples.

Stage 2 result: **FAIL** (material implementation/canonical divergence).

## 3. Clean proof reconstruction

The scratch build used only the copied `.k`, `.py`, and `.mpy` source files.
No candidate definition, cache, or binary was reused.

The concrete definition was freshly compiled with:

```text
kompile .../semantic.k --main-module MEDIAN-SEMANTICS
  --syntax-module MEDIAN-SYNTAX --backend llvm
  --output-definition .../build/concrete-kompiled
```

Exit was 0. LLVM emitted a relevant warning:

```text
Non exhaustive match detected:
nthInt(nil,_)
```

The proof definition was freshly compiled with the Haskell backend, main module
`SEMANTIC`, syntax module `MEDIAN-SYNTAX`, and exit 0.

I copied each of the three original claims without changing its body into a
separate audit module. A whitespace/comment-normalized check finds each split
claim exactly once in the original `spec.k`. Each was then proved
independently:

| Claim | `kprove` result | Exit |
|---|---|---:|
| universal claim | `#Top` | 0 |
| odd prompt example | `#Top` | 0 |
| even prompt example | `#Top` | 0 |
| original three-claim module | `#Top` | 0 |

The split artifacts are preserved in `evidence/audit-specs/`. Commands and
outputs are in `evidence/stage3-reconstruction.log`; the exact-claim check is
in `evidence/stage4-partition-check.log`.

### Generated-semantics concrete comparison

`evidence/semantics-differential.py` runs the fresh LLVM definition and the
copied Python entry point independently. The corrected run is
`evidence/stage3-semantics-differential-corrected.log`. The first comparison
inside `stage3-reconstruction.log` had an audit-side regular-expression escape
bug and classified every spaced K result as residual; it is superseded by the
corrected script and log, while its raw K outputs remain valid.

The corrected run gives exact-value matches on five ordinary cases: odd and
even normal inputs, both prompt examples as implemented by the candidate, and
the length-one boundary. It exposes four semantic/model discrepancies:

- Empty and length-two inputs produce an unmodeled `nthInt(nil,0)` failure
  rather than the Python `IndexError`.
- For `[0,1,2**54,2**54+1]`, K returns the exact rational
  `floatVal(36028797018963969,2)`, while CPython rounds to
  `18014398509481984.0`.
- For four copies of `10**400`, K reaches `.K` with
  `floatVal(2*10**400,2)`, while the submitted Python program raises
  `OverflowError`.

The latter two inputs have length four and satisfy the universal claim's
precondition.

Stage 3 result: **PASS** for clean claim closure, but **FAIL** for generated
semantics fidelity to the real Python program.

## 4. Adequacy and real-program pinning

### Plain-language claims

1. **Universal entry claim.** For every K integer-list term `IS` with at least
   three elements, execute the exact translated candidate function from an
   initial `noResult` state; execution must finish with result
   `promptMedian(IS)`.
2. **Odd example.** The same program on `[3,1,2,4,5]` must finish with
   `intVal(3)`.
3. **Even example.** The same program on
   `[-10,4,6,1000,10,20]` must finish with `floatVal(30,2)`.

The fixed example claims have precondition `true`.

### Program identity and result constraint

After whitespace/comment normalization, the byte-regenerated `solution.mpy`
term occurs exactly three times in `spec.k`, once in each `<k>` entry claim.
The entry rule does not replace the body with a summary: it binds `"l"` to the
input and calls `evalBody(BODY,...)`. Assignments, calls, the conditional, and
the selected return expression execute through the semantic functions.

There are no loops, helper-function claims, circularity claims, or auxiliary
execution claims. The only proof-local summary is in the postcondition and does
not rewrite the program's `<k>` term.

The returned result is not free: both concrete body and postcondition reduce to
specific `Val` constructors. A separate body-sensitivity mutation changed
`middle + 1` to `middle + 0` but retained the original result obligation. It
parsed and reached a residual `floatVal(6,2)` versus required
`floatVal(7,2)`, and `kprove` exited 1. See
`evidence/stage4-adequacy.log` and
`evidence/audit-specs/spec-body-sensitivity.k`.

### Satisfiable witnesses

`evidence/stage4-witnesses.py` exhibits ground states for all entries:

| Claim | Input | Formal claimed result | Candidate Python | Canonical Python |
|---|---|---|---:|---:|
| universal (`len=4 >= 3`) | `[1,2,3,4]` | `floatVal(7,2)` | `3.5` | `2.5` |
| odd example | `[3,1,2,4,5]` | `intVal(3)` | `3` | `3` |
| even example | `[-10,4,6,1000,10,20]` | `floatVal(30,2)` | `15.0` | `8.0` |

Thus the claim is satisfiable and discriminating, but it is pinned to the wrong
Python algorithm. The universal precondition also silently excludes length
one, which both Python implementations handle, and length two, which the
canonical handles but the candidate does not.

Stage 4 result: **PASS** for real submitted-AST pinning and result constraint;
**FAIL** for adequacy to the requested/canonical median.

## 5. Rule-by-rule static soundness review

The complete mechanical source inventory, including line numbers and full
normalized rule text, is in `evidence/stage5-static-inventory.log`.
There are 16 syntax-declaration statements and 37 rules in `semantic.k`, plus
one syntax-declaration statement and two rules in `verification.k`.

### Declaration inventory

The 17 local syntax declarations are:

1. `Module ::= Module(Stmts)`.
2. `Stmts ::= List{Stmt,""}`.
3. `Stmt ::= FuncDef | Assign | If | Return`.
4. `Params ::= Params(String)`.
5. `Expr ::= Name | Int | Call | BinOp | Subscript`.
6. `Ints ::= nil | cons(Int,Ints)`.
7. `Val ::= intVal | floatVal | listVal`.
8. `Env ::= .Env | bind`.
9. `ExecResult ::= next | returned`.
10. `ResultSlot ::= noResult | Val`.
11. Function `lookup`.
12. Function `evalExpr`.
13. Functions `sortVal`, `lenVal`, `subscriptVal`, `binopVal`, and `ifVal`.
14. Total functions `lenInts` and `nthInt`.
15. Total functions `sortInts` and `insertInt`.
16. Functions `evalBody`, `continueWith`, and `chooseBody`.
17. Proof-local functions `promptMedian` and `promptMedianSorted`.

There are 16 function symbols in total, of which four are marked `total`.
There are no `functional` declarations, opaque symbols/attributes, priority
rules, `owise` rules, `anywhere` rules, trusted attributes, or simplification
rules. The only configuration has `<k>`, immutable `<input>`, and mutable
`<result>` cells under `<median>`.

Declarations 1–6 cover exactly every AST constructor used by `solution.mpy`.
Declarations 7–13 and 16 provide the necessary values, bindings, expression
evaluation, and control. `floatVal` is the defective Python-float
representation discussed below. `lenInts`, `sortInts`, and `insertInt` are
genuinely total over their declared input sorts. `nthInt` is not: `nil` and
negative indices have no equation even though it is marked total. The fresh
LLVM compiler independently diagnosed the `nil` hole. This is an incomplete
and false totality declaration; `nthInt(nil,0)` is the concrete coverage
witness. I do not claim that this hole by itself proves a false main result,
because the main guard keeps the candidate's selected indices in bounds.

Declaration 17 is fully reducible on the claim's safe uses, but it is not an
independent median specification: it duplicates the submitted program's
upper-middle calculation and shares all its semantic primitives.

### Used-syntax coverage

| Submitted construct | Declaration/rules |
|---|---|
| `Module`, `FuncDef`, `Params` | declarations 1, 3, 4; rule 36 |
| statement sequence, two `Assign`s | declarations 2–3; rules 27–28 |
| `Name`, `Int` | declaration 5; rules 3–4 |
| `sorted` and `len` calls | declaration 5; rules 5–6, 9–10, 18–19, 22–26 |
| `//`, `%`, `+`, `/` | declaration 5; rules 8, 12–15 |
| `Subscript` | declaration 5; rules 7, 11, 20–21 |
| `If` with returning arms | declaration 3; rules 16–17, 30–35 |
| `Return` | declaration 3; rules 29–30, 37 |

Every submitted construct parses and has an applicable path on the formal
`len >= 3` domain. Missing semantics for unused Python constructs is not
counted as a defect.

### Exhaustive rule decisions

The numbering below is the numbering emitted in
`evidence/stage5-static-inventory.log`.

| Rule | Decision |
|---:|---|
| 1 `lookup` top binding | Sound shadowing lookup. |
| 2 `lookup` recurse | Sound with the disjoint string-inequality guard; missing-name behavior remains visibly partial. |
| 3 integer literal | Sound over mathematical integers. |
| 4 name expression | Sound for the modeled lexical environment. |
| 5 literal `sorted` call | Sound for this exact target binding and `Ints`; hard-codes the builtin and would not model rebinding, which the target does not perform. |
| 6 literal `len` call | Same binding limitation; sound for the target list value. |
| 7 subscript evaluation | Preserves left-to-right pure values for this target, but delegates all bounds behavior to partial rule 11. |
| 8 binary dispatch | Sound as dispatch; operator behavior is determined by rules 12–15. |
| 9 `sortVal` | Sound reduction to insertion sort for integer lists. |
| 10 `lenVal` | Sound list-length reduction. |
| 11 `subscriptVal` | Sound for nonnegative in-bounds indices; does not model Python negative indices or `IndexError`. The main guard makes selected indices in bounds, but empty/length-two boundary runs expose the semantic gap. |
| 12 integer `+` | Sound for the K/Python arbitrary-integer subset. |
| 13 candidate `//` | The actual use is nonnegative `len / 2`, where it agrees with Python floor division. The globally broad operator equation is not separately justified outside that used scope. |
| 14 candidate `%` | The actual use is nonnegative `len % 2`, where it agrees with Python. |
| 15 Python `/` to `floatVal(I,J)` | **Materially unsound value-bearing bridge.** It models neither IEEE-754 rounding nor conversion/overflow exceptions. False-conclusion witnesses are below. |
| 16 zero `ifVal` | Sound integer falsiness branch. |
| 17 nonzero `ifVal` | Sound and guard-disjoint from rule 16. |
| 18 `lenInts(nil)` | Sound base case. |
| 19 `lenInts(cons)` | Sound structural recursion. |
| 20 `nthInt` at zero | Sound for nonempty lists. |
| 21 positive `nthInt` recursion | Sound descent while in bounds; combined equations do not justify the `[total]` attribute. |
| 22 `sortInts(nil)` | Sound base case. |
| 23 recursive insertion sort | Sound structural descent. |
| 24 insert into empty | Sound base case. |
| 25 insert before `J` | Sound under `I <= J`. |
| 26 insert after `J` | Sound under the disjoint `I > J` guard; descends structurally. |
| 27 empty body | Sound normal completion. |
| 28 assignment | Correctly evaluates the pure expression and shadows the binding; no heap/alias effects are used by this target. |
| 29 return | Correctly discards trailing statements and produces `returned`. |
| 30 specialized returning-arm `if` | Sound for its exact two pure `Return` arms. It selects through `ifVal`; the length-one run confirms an invalid unselected else expression is not forced. |
| 31 general `if` | Sound integer-condition control for the modeled statements. It overlaps rule 30 but agrees observationally there: both exact arms return pure values and discard the suffix. |
| 32 false `chooseBody` | Sound and disjoint from rule 33. |
| 33 true `chooseBody` | Sound under nonzero guard. |
| 34 continuation after return | Sound abrupt-return propagation. |
| 35 continuation after normal completion | Sound sequencing. |
| 36 median entry | Soundly binds the actual input and executes the submitted body. It is not an execution-bypassing bridge. |
| 37 final returned value | Soundly writes the result and empties `<k>`. |
| 38 `promptMedian` sorting | A terminating definitional equation, not an operational bridge. |
| 39 `promptMedianSorted` | A terminating definition of the candidate's upper-middle formula on safe uses, but its claimed interpretation as the prompt's median is false and it is not independent of execution. |

### Overlaps, control, and state

The guarded lookup, truthiness, choice, and insertion pairs are disjoint and
cover their used domains. The sole unguarded overlap is specialized rule 30
with general rule 31. On the overlap, each arm is exactly one pure `Return`;
both routes select the same expression, produce `returned(V)`, discard the same
suffix, and touch no state other than the final result. There are no priority
rules that preempt ordinary execution.

The environment is immutable/shadowing, the input cell is preserved, and the
result cell is written only on return. `sorted` allocation/alias identity is
abstracted to an immutable `Ints` value; this target never observes identity or
mutates either list. No I/O, heap, output, exception, or call-stack cell is
present. That is sufficient for normal small-integer executions of this
particular body, but it is inadequate for its reachable Python exceptions.

### Required false-conclusion witnesses

Rule 15's comment asserts that `floatVal(N,D)` is an exact model of Python
floating division. Both witnesses below have length four, satisfy the entry
precondition, and reach the even return:

1. Let `L = [0,1,2**54,2**54+1]`. K concludes
   `floatVal(36028797018963969,2)`, an exact value ending in `.5`. CPython
   returns the rounded float `18014398509481984.0`. Thus the exact result
   conclusion is false.
2. Let `B = 10**400` and `L = [B,B,B,B]`. K terminates at `.K` with
   `floatVal(2*B,2)`. The real submitted Python program raises
   `OverflowError: integer division result too large for a float`. Thus both
   the normal-return and value conclusions are false.

These are not inferred from a timeout or parser failure: the fresh LLVM K runs
exit 0 with terminal configurations, while independent CPython produces the
different outcomes. Exact commands and complete bounded outputs are in
`evidence/stage3-semantics-differential-corrected.log`.

If `floatVal(I,J)` is instead read merely as an uninterpreted record of the two
operands, rule 15 avoids asserting exact arithmetic only by ceasing to
constrain the actual Python float result. Under that reading the proof has a
material adequacy gap and still does not prove the requested program result.

Rule 39 is not logically inconsistent merely because its symbol is named
`promptMedian`; it defines that new symbol. Its proposed interpretation as
median is nevertheless refuted by `[1,2,3,4]`: it gives `3.5`, whereas the
trusted canonical and ordinary median give `2.5`.

Stage 5 result: **FAIL** (materially unsound used division rule and false
summary-to-median interpretation).

## 6. Fresh non-vacuity test

I did not rely on a candidate mutation. The fresh audit mutation retains the
exact real program and the satisfiable even example input, but changes only the
result obligation from `floatVal(30,2)` to the false `floatVal(31,2)`.

The dry run parsed and built successfully with exit 0. The actual proof then
reached a terminal configuration with `floatVal(30,2)`, emitted
`WarnStuckClaimState`, and exited 1. This is the expected unmet result
obligation, not a parser error, missing import, timeout, or unrelated crash.

Artifacts:

- `evidence/audit-specs/spec-vacuity-audit.k`
- `evidence/stage6-nonvacuity.sh`
- `evidence/stage6-nonvacuity.log`

Stage 6 result: **PASS** (the K claim is result-constraining and non-vacuous
within the submitted theory).

## 7. Proven versus assumed accounting

### What the successful reachability proof actually establishes

Conditional on the submitted K theory, for every K `Ints` value `IS` with
`lenInts(IS) >= 3`, the exact submitted AST rewrites from `noResult` to `.K`
with `promptMedian(IS)`. The two ground example claims also rewrite to
`intVal(3)` and `floatVal(30,2)`. The proof executes the body and is sensitive
to its even-index expression.

It does **not** establish that:

- `solution.py` implements the trusted canonical or conventional median;
- the prompt's inconsistent `15.0` example is a correct median;
- `floatVal(I,J)` is the actual CPython result of `/`;
- real Python normally returns on every integer list of length at least three;
- lists of length one or two meet the requested contract;
- non-integer numeric elements are supported.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K v7.1.293 rewrite engine and imported `INT`/`STRING` operations | all builds and claims | Acceptable foundational tool/math boundary. |
| Trusted `/reference/py2mpy.py` translation | program identity | Acceptable by task authority; regeneration is byte-identical. |
| `Ints` as the input model | all entry claims | Explicit restriction to integer lists; narrower than the prompt's unqualified `list`. |
| Insertion-sort and length equations | `sorted`, `len`, both program and post | Program-derived semantics actually executes terminating equations; acceptable for finite integer lists, with finite concrete support. |
| Hard-coded `sorted`/`len` bindings | calls in this exact body | Acceptable only because this body does not rebind those names; not a general Python semantics. |
| Partial `nthInt` plus false `[total]` declaration | subscripting and proof simplification | Concerning/incomplete. In-bounds main uses avoid the hole, but boundary execution and compiler warning expose it. |
| `floatVal` rule 15 | every even returned result and the universal claim | **Illegitimate.** It is value- and termination-bearing, has no IEEE/exception connection theorem, and the two satisfying witnesses refute it. |
| `promptMedian`/`promptMedianSorted` | universal postcondition | Fully defined, not opaque, but it duplicates the candidate and shared primitives. It supports only self-refinement, not the requested median meaning. |
| Differential evidence | candidate/canonical and K/Python bridges | Finite evidence only. It exposes failures; it is not used as a substitute for the K proof. |

There are no opaque or fresh result symbols and no proof-local operational
bridges. That prevents an unconstrained-oracle failure, but it does not repair
the false concrete division semantics or the wrong specification target.

### Final decision

Fresh `#Top` and successful non-vacuity are real, but they establish a theorem
inside an unsound generated execution model and against a proof-local clone of
the wrong algorithm. The admitted length-four rounding and overflow witnesses
make false conclusions about the real submitted Python program provable.
Separately, the implementation and formal summary materially diverge from the
trusted canonical median. These are direct `FAIL / NOT_LEGIT` conditions, not
mere thin evidence or an informal-intent concern.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
