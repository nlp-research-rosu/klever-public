# Independent adversarial review: 126-is-sorted

The candidate contains a legitimate partial-correctness proof of the submitted
program under the supplied MPY semantics. I rebuilt both definitions from
source, reran the complete positive specification, mechanically pinned the
claim to the translated function body, reviewed every proof-local equation and
the source-relevant fixed-semantics rules, and rejected independent body and
postcondition mutations.

The result has one explicit language-semantics trust boundary:
`sortVS(VS)` is the supplied semantics' fixed external model of Python
`sorted`. The K theorem is interpretation-parametric in that symbol; the
source-level ascending-order reading is conditional on its named contract.
That boundary is acceptable here because `sorted` is an external language
primitive rather than program-defined code, the candidate did not introduce or
alter it, real call/lookup/allocation behavior remains in the theorem, and the
conditional dependency is visible. It is also supported, but not proved, by
fresh concrete K tests.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- record layout `pipeline-v3`;
- problem `126-is-sorted`;
- condition `kit-semantics`;
- semantics mode `SUPPLIED_SEMANTICS`; and
- the launcher-owned container paths used in this review.

There is no mode/mount contradiction: the required trusted
`/reference/reference-semantics` tree is present.

I independently checked every required pipeline-v3 record and provenance mount.
All are readable and have the required regular-file or directory type. The
recorded SHA-256 values for `/run.json`, `/task.json`,
`/generation-result.json`, the invocation/metrics/runtime/usage records,
generation prompt/output/last message, trusted prompt, canonical source,
translator, and candidate copies of the prompt and translator all match their
mounted bytes. The campaign-lock file hash matches the recorded hash and its
JSON object is exactly equal to the `audit_campaign` block.

The structured trace contains one 924,590-byte JSONL file with 490 valid
records and no malformed record. Its file hash matches
`generation-result.json`. The 1,451,341-byte `codex-output.log` was read in
full. Those generation materials were treated only as untrusted claims.

The supplied-semantics integrity gate passes. The candidate and trusted trees
each contain the same 24 regular K files (25 entries including the helper
directory), with no symlink or special entry. Recursive relative paths, entry
types, and every file hash are identical; there is no missing, additional, or
changed entry. Candidate `prompt.py` and `py2mpy.py` are byte-identical to
their trusted mounts.

Evidence:

- [stage1-integrity.log](evidence/stage1-integrity.log)
- [stage1-record-inventory.log](evidence/stage1-record-inventory.log)
- [stage1-generation-inspection.log](evidence/stage1-generation-inspection.log)
- [check_stage1.py](evidence/check_stage1.py)
- [inspect_generation.py](evidence/inspect_generation.py)

`stage1-records-readable.log` records an unavailable optional `jq` pretty-print
attempt (exit 127). It was superseded by the Python inspection above; it did
not affect access to, hashing of, or parsing of any required record.

Stage 1: PASS. There is no audit-infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt's contract is:

- input is a finite list containing only nonnegative integers;
- return `True` exactly when the list is in nondecreasing order and no value
  occurs more than twice;
- otherwise return `False`.

The trusted canonical code builds occurrence counts, rejects a count greater
than two, and then checks every adjacent pair. The candidate instead first
compares the list to `sorted(lst)`, then scans adjacent equal runs and forces
the result to false at run length three. On a sorted list, equal values are
contiguous; on an unsorted list, the initial comparison is already false.
Thus the algorithms are extensionally equivalent on the stated domain.

Using the trusted translator copied to scratch, I regenerated
`solution.mpy`. The submitted and regenerated files are byte-identical, both
with SHA-256
`566af90b6110d8aff60a7b757b794193cb099ee6cef0fc6fd225c1c1b1bbeaec`.

The independent differential script imports `/reference/canonical.py` and the
scratch copy of candidate `solution.py`. It also uses a separately coded
adjacent-order/`Counter` oracle. Its input scope is:

- all eight documented examples;
- 16 explicit empty, singleton, sorted/unsorted, duplicate-boundary, and
  large-integer cases;
- every list of lengths 0 through 7 over values 0 through 4; and
- 2,000 deterministic generated lists of lengths 0 through 30 over values
  0 through 100.

All six source branch classes were exercised. Across 99,680 inputs there were
zero candidate/canonical/oracle mismatches and zero documented-example
failures.

Evidence:

- [stage2-regeneration.log](evidence/stage2-regeneration.log)
- [differential_test.py](evidence/differential_test.py)
- [stage2-differential.log](evidence/stage2-differential.log)

Stage 2: PASS.

## 3. Clean proof reconstruction

All execution occurred below `/tmp/audit-work/126-is-sorted`. The scratch tree
contains source files copied from the candidate and the trusted semantics,
translator, prompt, and canonical mounts. No candidate `runtime-kompiled`,
`verification-kompiled`, cache, log, or trace was copied or used.

The live toolchain is K 7.1.293. Fresh commands and results were:

```text
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-audit-kompiled
exit 0

kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-audit-kompiled
exit 0

kprove spec.k --definition verification-audit-kompiled \
  --spec-module SPEC
#Top
exit 0

kprove spec.k --definition verification-audit-kompiled \
  --spec-module SPEC --claims SPEC.scan-loop
#Top
exit 0
```

`spec.k` has exactly two positive claims. The complete specification command
is the candidate's target command and proves both together; the entry claim
uses `scan-loop` as its circularity. I additionally proved the helper in
isolation. As a diagnostic, selecting only `SPEC.entry` removes that helper
from the selected specification and begins unbounded symbolic list unrolling;
I interrupted that non-target diagnostic after more than three minutes. This
does not contradict the successful complete two-claim run.

The compiler emitted warnings from unused portions of the fixed supplied
semantics, chiefly non-exhaustive declarations for other language features.
There was no build error, and none of those warned functions is on this
program's execution/proof path.

Evidence:

- [stage3-toolchain.log](evidence/stage3-toolchain.log)
- [stage3-kompile-llvm.log](evidence/stage3-kompile-llvm.log)
- [stage3-kompile-haskell.log](evidence/stage3-kompile-haskell.log)
- [stage3-kprove-full.log](evidence/stage3-kprove-full.log)
- [stage3-kprove-scan-loop.log](evidence/stage3-kprove-scan-loop.log)
- [stage3-kprove-entry.log](evidence/stage3-kprove-entry.log)

Stage 3: PASS.

## 4. Adequacy and real-program pinning

### Plain-language claims

`SPEC.scan-loop` says that, from the actual translated loop head over any
remaining `ValSeq`, executing the loop consumes the suffix, leaves the
continuation in place, and updates exactly four loop-carried locals:

- `previous` becomes the last singleton tuple (or stays unchanged when empty);
- `repeated` becomes the final adjacent-run count;
- `result` is its prior Boolean conjoined with the condition that no processed
  run reaches three; and
- `value` becomes the last iterated value (or stays unchanged when empty).

It preserves `lst`, scope allocation, heap, heap allocation counter, stack,
return state, exception state, and exit code.

`SPEC.entry` says that, from the clean post-module-load scope containing
`is_sorted` and the fixed builtins scope, calling that exact closure on
`list(VS)` returns `sortedWithAtMostTwo(VS)` for every finite `VS` accepted by
`nonNegativeVals`. It also constrains the `sorted` result allocation at heap
location 0, heap counter 1, unchanged module binding, empty stack, restored
environment/return state, no exception, and exit code 0.

### Program identity

A reviewer-authored constructor parser mechanically compared the regenerated
`solution.mpy` term with `spec.k`:

- exactly one `FuncDef` was found;
- both closure occurrences in the entry claim have the same parameter and
  constructor body as that function;
- equality holds after removing only explicit `.Stmts` identity units and
  whitespace;
- the source `For` target and body exactly equal the helper claim's target and
  body; and
- the helper's `list(REMAINING)` is the fixed semantics' evaluated iterable
  suffix corresponding to source `Name("lst")`.

The entry starts after module loading, but the binding and body are the same
translated constructor term. Omitting the already-completed `Module/FuncDef`
load is therefore a demonstrated entry normalization, not a substituted
program.

### Satisfiable states and ground substitutions

The entry precondition is satisfiable; `VS = .ValSeq` is the simplest witness.
The helper has no Boolean side condition and has, for example, a well-sorted
empty-remaining state with integer locals, a plain current scope, and the
standard empty auxiliary cells.

Ground substitution compared the claim predicate, trusted canonical function,
and candidate function on:

```text
[]                        -> true
[0]                       -> true
[0, 1, 1]                 -> true
[0, 0, 0]                 -> false
[2, 1]                    -> false
[0, 1, 1, 2, 2]           -> true
```

All three results agree in every row. A fresh LLVM program containing the
exact function body and assertions for those cases terminates with `.K`,
`NoExc`, and exit code 0.

The formal argument uses a bare `list(VS)` value rather than a caller-owned
heap reference. This is an explicit fixed-semantics convention for read-only
symbolic list arguments. It is adequate here: the submitted function never
mutates or exposes the input, while every material consumer (`sorted`,
structural comparison, and `For`) has the corresponding fixed dereference rule.

Evidence:

- [check_program_pinning.py](evidence/check_program_pinning.py)
- [stage4-program-pinning.log](evidence/stage4-program-pinning.log)
- [ground_claim_substitution.py](evidence/ground_claim_substitution.py)
- [stage4-ground-substitution.log](evidence/stage4-ground-substitution.log)
- [concrete_witnesses.py](evidence/concrete_witnesses.py)
- [stage4-krun-witnesses.log](evidence/stage4-krun-witnesses.log)

Stage 4: PASS.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The mechanical inventory covers all 24 supplied K files plus
`verification.k` and `spec.k`. It contains 953 top-level records:

- 603 ordinary rules;
- 35 concrete rules;
- 45 priority rules;
- 27 `owise` rules;
- 78 ordinary syntax declarations;
- 39 function declarations;
- 89 function/total declarations;
- 3 function/total/symbol declarations;
- 22 opaque function/total/symbol/`no-evaluators` declarations;
- 4 macro syntax declarations;
- 5 contexts;
- 1 configuration; and
- 2 reachability claims.

There are no local simplification rules and no `functional` declarations. The
inventory gives every record an ID, source location, complete flattened
statement, origin, path relevance, and review disposition. The 124
source-relevant records were reviewed in detail. Every remaining row is a
fixed-semantics declaration/rule for a construct absent from the submitted
program and from the proof path; it cannot contribute to claim closure. This
distinguishes unused fixed-language coverage from proof-local extensions.

Evidence:

- [stage5-rule-inventory.tsv](evidence/stage5-rule-inventory.tsv)
- [stage5-rule-inventory.md](evidence/stage5-rule-inventory.md)
- [inventory_k.py](evidence/inventory_k.py)
- [stage5-used-symbol-map.log](evidence/stage5-used-symbol-map.log)

### Used constructor and rule map

| Submitted construct | Declaration and material fixed rules |
|---|---|
| `Module`, `FuncDef`, `Params`, statement sequence | `syntax.k`; `core.k` load/sequencing; `functions.k` closure binding |
| `Name`, `Int`, `Bool` | `core.k` literal and lexical-scope lookup rules |
| `Assign`, `AugAssign` | strict syntax; `controls.k` local writes; `int.k` integer `+` |
| `Call(Name(...), ...)` | `call.k` callee then left-to-right argument evaluation; closure-frame rule |
| `sorted(lst)` | builtin lookup in `builtinsScope`; `sort.k` sorted dispatch; `core.k` fresh allocation |
| list equality | `operators.k` left/right evaluation and heap dereference; `list.k` structural equality |
| tuple literal/equality | `tuple.k` left-to-right tuple evaluation and singleton structural equality |
| unary `-`, comparison `>` | `operators.k`; exact integer cases in `int.k` |
| `If` | strict guard, `truthy(Bool)`, and disjoint branch rules in `controls.k` |
| `For` | one-time iterable evaluation, list iterator, target bind, body, loop label, and suffix recurrence |
| `Return` | strict result evaluation, `retV`, frame pop, environment/scope restoration |

Evaluation order is fixed: call callee before arguments, arguments left to
right, comparison left before right, assignment RHS before write, iterable
once before iteration, and conditions before branch selection. The exact
lookup chain chooses the module's `is_sorted`, then the reserved builtins
scope's `sorted`; no proof rule pins a name by spelling alone.

The cell-variable priority rules have guards requiring a `$cells` declaration
and are inapplicable to the plain entry frame. The ordinary local-write/bind
rules therefore apply. The special `sorted` dispatch preempts the generic
`applyBuiltin` `owise` path. Heap-reference priority rules preserve structural
list comparison and one-time iteration dereference. The guards are disjoint on
the actual entry states. No unrelated special `Call` interception matches
either submitted call.

Fresh allocation reads/writes `<heap>` and `<heapLoc>` exactly as reflected in
the entry post-state. Function call/return rules read and restore `<env>`,
`<scopes>`, `<scopeLoc>`, `<stack>`, and `<ret>`. The loop body has no abrupt
control, allocation, mutation of the input, output, or exception path, so the
helper claim's framed continuation and preserved cells match its complete
fixed-semantics footprint.

### Candidate proof extensions (inventory K0929–K0951)

| Extension | Decision |
|---|---|
| `nonNegativeVals` | Truthful input predicate. Empty, integer-head, and non-integer `owise` cases are exhaustive; recursion descends. |
| `nextRepeated` | Exact counter update. Equality and its Boolean negation are complementary and right-hand sides cannot overlap inconsistently. |
| `scanPrevious` | Empty/base and cons/step cases are constructor-disjoint; the step descends on the suffix and returns the last value. |
| `scanRepeated` | Same constructor split and descent; composes the exact `nextRepeated` transition. |
| `scanValue` | Empty preserves the old loop variable; cons recursion returns the final iterated value. |
| `duplicateOK` | Empty is true; each cons rejects count 3 or greater and descends. It exactly mirrors the source's irreversible false update. |
| `scanDuplicates` | Exhaustive nonrecursive equation `B andBool duplicateOK(...)`; it preserves an already-false result. |
| `sortedWithAtMostTwo` | Guarded to the entry domain. It names, but does not execute, the conjunction of equality with the supplied sort result and the verified duplicate scan. |

All declarations marked `total` have constructor-complete equations on their
declared sorts and uses. `sortedWithAtMostTwo` is intentionally not total
outside its `nonNegativeVals` guard, and the entry claim carries that guard.
No candidate equation is a semantic rewrite over `<k>`, no candidate rule
introduces control transfer, and there is no proof-local priority,
simplification, or opaque oracle.

`SPEC.scan-loop` (K0952) is a derived circularity rather than an operational
bridge. Its base case is the fixed `#iterDone` transition. Its cons case binds
the head, executes every source statement, reaches the same `#loop` term on the
tail after progress, and composes the recursive summary. Its arbitrary
continuation is safe because the loop body contains no return/break/continue
or exceptional effect. The focused proof closes independently.

`SPEC.entry` (K0953) executes normal lookup, argument binding, every source
statement, the proved loop claim, return, and frame pop. Its result is a
Boolean formula, not a free variable, implication-only condition, or
tautology.

### Supplied `sortVS` boundary

`sortVS` is declared in the fixed supplied `sort.k` as a total opaque symbol
for symbolic proof and has concrete insertion-sort equations for integer
lists. The material operational rule is:

```text
#applyK(toCall(builtinV("sorted")), (list(VS), .Vals))
  => #alloc(list(sortVS(VS)))
```

This is an external-language primitive, not program-defined code and not a
candidate extension. The proof executes lookup, argument evaluation, dispatch,
allocation, later equality, and all surrounding control. It is parametric in
the primitive's value and makes the human-facing conclusion conditional on
the named contract that `sortVS` is Python's ascending permutation.

Without that contract, an arbitrary interpretation such as
`sortVS([2,1]) = [2,1]` would make the symbolic equality true even though the
Python input is unsorted. This is not a false candidate rule witness; it
identifies the exact external assumption and why the unconditional
ascending-order reading must not exceed it.

As finite support only, ten independent direct K assertions compare concrete
`sorted` results with explicit Python-expected lists, covering empty,
singleton, reverse/permuted, duplicates, long reverse, and large-integer
inputs. They all end with `.K`, `NoExc`, exit code 0. These tests do not replace
the named primitive contract.

Evidence:

- [sort_bridge_witnesses.py](evidence/sort_bridge_witnesses.py)
- [stage5-sort-bridge-krun.log](evidence/stage5-sort-bridge-krun.log)

### Body sensitivity

I changed both preserved copies of the executed closure from
`Return(Name("result"))` to `Return(Bool(false))`, leaving the result
obligation unchanged. Thus the mutation changes the actual program term and
does not fail merely because the final module binding differs. It builds, then
`kprove` exits 1 with `WarnStuckClaimState`; the residual has `false` in `<k>`
against the original result formula.

Evidence:

- [make_body_mutation.py](evidence/make_body_mutation.py)
- [spec-body-mutation.k](evidence/spec-body-mutation.k)
- [stage5-body-mutation-proof.log](evidence/stage5-body-mutation-proof.log)

No inventoried candidate rule was classified as unsound, so there is no
unsupported unsoundness allegation requiring a false-conclusion witness.

Stage 5: PASS.

## 6. Fresh non-vacuity test

I did not rely on the candidate's `spec-vacuity.k`. The reviewer mutation was
generated afresh from the actual entry claim:

- input is the satisfiable `list(.ValSeq)`;
- the submitted closure body is unchanged;
- expected heap allocation is fixed to the concrete empty sorted list; and
- the destination result is changed from the real `true` result to `false`.

`kprove --dry-run` exits 0, establishing that the mutation parses and builds
against the fresh proof definition. The actual proof exits 1 with
`WarnStuckClaimState`. Its residual has `true ~> .K` in `<k>`, normal final
state, `NoExc`, and exit code 0, while the destination requires `false`. This
is the expected reachable unmet result obligation, not a parser failure,
timeout, unrelated crash, or unreachable mutation.

Evidence:

- [make_nonvacuity_mutation.py](evidence/make_nonvacuity_mutation.py)
- [auditor-nonvacuity.k](evidence/auditor-nonvacuity.k)
- [stage6-mutation-dry-run.log](evidence/stage6-mutation-dry-run.log)
- [stage6-mutation-proof.log](evidence/stage6-mutation-proof.log)

Stage 6: PASS.

## 7. Proven versus assumed accounting

### Precisely proven

Under the fixed supplied MPY semantics, for every finite `ValSeq VS` whose
elements are K integers at least zero, executing the exact translated
`is_sorted` closure from the stated clean module state reaches a normal return
whose Boolean value is:

```text
(VS ==K sortVS(VS))
andBool
scanDuplicates(-1, 0, true, VS)
```

The proof also establishes the specified name binding, sorted-result heap
allocation, loop local-state transformation, frame restoration, empty stack,
normal return/exception state, and exit code.

Conditional on the supplied external contract for `sortVS`, the first
conjunct is exactly nondecreasing order. The second conjunct rejects the first
adjacent run of length three. If the list is sorted, all equal values are
contiguous, so this is equivalent to every value having multiplicity at most
two. If it is not sorted, the first conjunct is false. Because inputs are
nonnegative, the initial `-1` sentinel cannot accidentally represent a prior
input element (and the counter transition would still initialize to one on the
first iteration).

This is partial correctness. The review does not elevate it to a separate
complexity, resource, or total-correctness theorem.

### Trust ledger

| Boundary | Dependents | Classification |
|---|---|---|
| K 7.1.293 parser/compiler/Haskell prover and K's `Int`, `Bool`, `Map`, list, and equality primitives | All machine-checked results | Foundational toolchain trust; acceptable and version-recorded. |
| The integrity-verified supplied MPY rules on the used constructor slice | Operational meaning of the translated program | Fixed selected semantics; source-relevant rules were statically reviewed and concretely exercised. |
| `sortVS : ValSeq -> ValSeq` contract | Ascending-order interpretation, initial `result`, final Boolean, retained heap object | Fixed external `sorted` primitive; acceptable only with the explicit named contract. Ten fresh concrete K cases are finite support. |
| Bare `list(VS)` symbolic input convention | Entry-state relation to an ordinary Python list argument | Fixed semantics explicitly permits it; acceptable for this read-only, non-alias-observing function. |
| Trusted `py2mpy.py` | Source-to-constructor identity | Launcher hash verified; fresh output is byte-identical. |
| Canonical Python and differential tests | Implementation equivalence and intent evidence | Empirical evidence only; not used to close the K theorem. |
| `scan-loop` | Entry proof over unbounded finite lists | Proven K reachability claim, not assumed or opaque. |

The other opaque fixed-semantics symbols in the exhaustive inventory concern
floats, keyed sorting, MD5, and unrelated language features. No submitted
constructor or proof path references them, so no claim depends on them.

`PROOF.md`, generation traces, candidate compiled definitions, and
candidate-supplied proof/test logs are not in the trust ledger. They were not
used as proof substitutes.

### Domain and exclusions

The theorem covers the complete source-contract domain: arbitrary finite lists
of nonnegative integers. It is not a finite-size proof or bounded unrolling.
It excludes negative integers and non-integer elements exactly as the prompt
does. It also does not claim malformed calls, resource exhaustion, behavior of
unused language constructs, alias-sensitive input mutation, or total
correctness.

Gate A (real-program soundness): PASS.  
Gate B (intent adequacy): PASS.  
Gate C (trust/evidence auditability): PASS.

Stage 7: PASS. The explicit `sortVS` trust boundary is acceptable and does not
constitute a material adequacy gap under the supplied-semantics condition.

VERDICT: PASS
LEGITIMACY: LEGIT
