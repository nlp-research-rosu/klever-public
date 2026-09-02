# Independent adversarial audit: 43-pairs-sum-to-zero

The candidate is **not a legitimate universal partial-correctness proof of the
real submitted program**. Fresh reconstruction does produce `#Top`, and the
result obligation is non-vacuous, but the universal claim is over a synthetic
`intValues(IntSeq)` list representation rather than ordinary semantic
`vCons` lists. A proof-local priority rule also replaces the program's real
empty-list allocation with that synthetic representation. This is not merely an
unproved prose bridge: on the intended input `[]`, it makes a false
fixed-semantics heap conclusion provable. The fixed definition rejects that
conclusion, and a continuation-sensitivity test shows different behavior.

Audit workspace: `/tmp/audit-work/pairs-audit`. Candidate files were never
modified or used as compiled definitions. Reviewer scripts, source mutations,
and bounded logs are under `evidence/`.

## 1. Input and provenance integrity

The rendered mode and trusted mounts are coherent:

- Mode is `SUPPLIED_SEMANTICS`.
- `/reference/reference-semantics` is present, so there is no infrastructure
  contradiction.
- Recursive `diff -ruN --no-dereference` between the trusted and candidate
  `reference-semantics/` trees exits 0. There are no missing, additional,
  changed, mistyped, symlinked, or other non-regular entries in that candidate
  tree.
- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`.
- `/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`.
- No symlinks occur anywhere in the candidate tree. Candidate `__pycache__`
  files and the auxiliary `prove.sh`/concrete-test files were treated as
  untrusted extras and were not used as proof caches.

Four requested provenance artifacts are missing:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`

No structured generation trace is present. These omissions reduce provenance
auditability but are not the reason for the negative legitimacy verdict.

Exact tree listings, file types, comparisons, and hashes are in
[`stage1_integrity.sh`](evidence/stage1_integrity.sh) and
[`stage1_integrity.log`](evidence/stage1_integrity.log). The live toolchain is
independently installed at `/usr/bin`; `kompile` and `kprove` are K v7.1.337.
See [`toolchain.log`](evidence/toolchain.log).

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

For every finite list of integers, return `True` iff there are two **distinct
positions** whose values sum to zero; otherwise return `False`. Consequently,
`[0]` is false and `[0, 0]` is true.

The trusted canonical implementation checks every pair of indices `i < j`.
The candidate implementation maintains a list of earlier values. For each
current integer `value`, it returns true exactly when `-value` is already in
that earlier-values list, then appends `value` if no pair was found. The initial
`value = 0` assignment is redundant but harmless. On the intended integer-list
domain, the algorithm implements the stated contract and does not mutate its
input.

### Translation identity

Running the trusted translator afresh on the scratch copy of `solution.py`
produces SHA-256
`e301c4a2be59c74f263a77fad0f37b88cdf0a27f9e94341fff3e1285afe13475`.
The regenerated and submitted `solution.mpy` files are byte-identical (`cmp`
exit 0). Commands and results are in
[`stage2_fidelity.log`](evidence/stage2_fidelity.log).

### Independent differential testing

[`differential.py`](evidence/differential.py) loads the trusted canonical and
generated entry points from explicit paths and also uses an independently
written index-pair oracle. It checks:

- all five documented examples;
- 14 empty, zero, duplicate, first-match, late-match, ordering, and large-int
  boundaries;
- every list of length 0 through 6 over `[-2, -1, 0, 1, 2]` (19,531 cases);
- 1,000 deterministic generated lists of lengths 0 through 30 and values from
  -1,000,000 through 1,000,000, seed 430043.

All 20,550 cases agree, with zero mismatches and Boolean result types. The
input generators, exact command, exit 0, and counts are preserved in
[`stage2_fidelity.sh`](evidence/stage2_fidelity.sh) and its log. This is finite
evidence about source intent; it does not repair a K execution bridge.

## 3. Clean proof reconstruction

Only source artifacts were copied to `/tmp/audit-work/pairs-audit`. The
semantics copy came from the trusted reference mount. Candidate bytecode was
ignored, and no candidate-built definition or cache existed or was reused.

Fresh commands and outcomes:

| Reconstruction target | Outcome | Evidence |
|---|---:|---|
| Trusted translation of `concrete-tests.py` and byte comparison | exit 0, identical | `stage3_translate_concrete.log` |
| LLVM `MPY-KRUN` definition | exit 0 | `stage3_kompile_llvm.log` |
| Concrete test execution | exit 0, final `.K`, `NoExc`, exit code 0 | `stage3_krun_concrete.log` |
| Haskell base `PAIRS-VERIFICATION` definition | exit 0 | `stage3_kompile_base.log` |
| `bounded-empty` | exit 0, `#Top` | `stage3_kprove_bounded-empty.log` |
| `bounded-one` | exit 0, `#Top` | `stage3_kprove_bounded-one.log` |
| `bounded-two` | exit 0, `#Top` | `stage3_kprove_bounded-two.log` |
| `membership-summary` | exit 0, `#Top` | `stage3_kprove_membership-summary.log` |
| `loop-summary`, with only the separately proved membership claim trusted | exit 0, `#Top` | `stage3_kprove_loop-summary.log` |
| Haskell `PAIRS-VERIFICATION-LEMMAS` definition | exit 0 | `stage3_kompile_lemmas.log` |
| `all-integer-lists` | exit 0, `#Top` | `stage3_kprove_all-integer-lists.log` |

The exact command sequence is
[`stage3_rebuild.sh`](evidence/stage3_rebuild.sh). Compiler warnings concern
unused variables and pre-existing supplied-semantics totality diagnostics; no
positive command failed. Thus proof closure under the candidate's extended
theory is genuine. Proof closure is not sufficient for legitimacy.

## 4. Adequacy and real-program pinning

### Claims in plain language

| Claim | Precondition | Claimed postcondition |
|---|---|---|
| `bounded-empty` | Exact initial call state, ordinary empty `vCons` list | Returns false; allocates an ordinary empty local `seen` list |
| `bounded-one` | Same state with one arbitrary integer `A` | Returns `pairsSpec([A])` (false); heap holds the processed prefix |
| `bounded-two` | Same state with arbitrary integers `A,B` | Returns `pairsSpec([A,B])`; heap holds the prefix before a match or both values |
| `membership-summary` | `#memberAcc(V, list(intValues(INPUT)))` followed by arbitrary `CONT`; all omitted cells are framed | Replaces the membership machine with `memberIS(V,INPUT)` and preserves `CONT` |
| `loop-summary` | Exact loop-head/call-return context; synthetic remaining and seen sequences; exact local frame, `builtinsScope`, `NoExc`, exit 0 | Returns `scanIS(REM,SEEN)`, updates synthetic seen prefix, pops the call frame |
| `all-integer-lists` | Exact initial call cells, but argument is synthetic `list(intValues(INPUT))` | Returns `pairsIS(INPUT)` and leaves a synthetic `seenAfterIS` heap payload |

There are no explicit `requires` clauses. Sorts and complete cell patterns are
the preconditions.

All preconditions are satisfiable. Examples are: empty input for
`bounded-empty`; `A=7`; `A=2,B=-2`; membership with `V=2`,
`INPUT=iCons(2,.IntSeq)`, `CONT=.K`; loop summary with
`REM=SEEN=ORIGINAL=.IntSeq`, `OLD=0`, `H=0`, `HEAP=.Map`, `NEXT=1`; and main
input `iCons(0,iCons(0,.IntSeq))`.

### Program body identity

`pairsBody` expands to the same statement AST as the regenerated
`solution.mpy`: empty-list assignment, redundant zero assignment, `for value
in l`, unary negation, list membership, early true return, append, and final
false return. Grammar normal forms explain the textual `.Exprs` forms.
`pairLoopBody` is the exact loop body. The claims call a closure with parameter
`l`, that body, and defining environment 0, so no alternate source-level
function binding is selected.

This link is nevertheless manually duplicated: no positive claim loads
`solution.mpy` itself. Changing only the submitted file would not affect the
proof definition. For the current candidate, trusted translation plus direct
AST inspection establishes that the duplicate is exact, so this manual link is
a documented concern rather than the decisive failure.

### Ground substitutions

Reviewer-authored claims execute ordinary `vCons` inputs under the base
definition, without either promoted priority rule. Empty, `[0]`, `[0,0]`, the
documented late-pair example, and a no-pair example all close with `#Top`.
Separate ground reductions of the formal `pairsIS` results agree. Both Python
implementations agree on every one of these substitutions. Sources and logs
are [`stage4_ground-spec.k`](evidence/stage4_ground-spec.k),
[`stage4_ground_checks.sh`](evidence/stage4_ground_checks.sh), and the
`stage4_kprove_*.log` files.

### Adequacy failure

The universal source configuration is not the real fixed-semantics call
configuration for a finite integer list. A real list is
`list(vCons(X,...,.ValSeq))`; the theorem starts from
`list(intValues(iCons(X,...,.IntSeq)))`. `intValues` has no equation or
bridge-free theorem connecting it to `vCons`. The bounded fixed-semantics
claims cover only lengths 0, 1, and 2. Finite ground executions do not supply
the missing universal connection.

Accordingly, the universal `#Top` proves execution over a proof-added data
constructor, not over every actual semantic list accepted by the submitted
program. This is a substituted-input proof and fails real-program pinning.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[`rule_inventory.txt`](evidence/rule_inventory.txt) is a source-indexed,
line-numbered inventory with normalized full declarations and attributes. It
contains 1,147 items across 26 K files: 719 rules, 239 syntax declarations, 6
claims, 5 contexts, 1 configuration, and module/import declarations. It
separately lists all priority, concrete, symbolic, and `no-evaluators` entries.
There are no `functional` or `simplification` declarations. Its SHA-256 is
`63797d8ab273bdc9e8f4871ed3a363374d649f6be951abfc8e2ff51a3419d1a2`.

The 1,091 supplied-baseline items are byte-identical to the trusted selected
semantics and are therefore accepted at the stipulated semantics level. The
complete per-rule decision for that class is `ACCEPTED_SUPPLIED_BASELINE`;
proof-local rules receive no such presumption. The baseline module inventory
is:

| Module/file | Syntax | Rules | Target role or assessment |
|---|---:|---:|---|
| `semantics.k` | 0 | 0 | Imports the supplied module graph |
| `syntax.k` | 16 | 0 | Used AST grammar and strictness declarations |
| `core.k` | 37 | 46 | Configuration, sequencing, literals, lookup, evaluation, allocation |
| `iter.k` | 1 | 0 | Iterator protocol declaration |
| `operators.k` | 0 | 10 | Unary/compare evaluation and dispatch |
| `int.k` | 1 | 16 | Integer unary minus used |
| `list.k` | 5 | 27 | List construction, iteration, membership, append used |
| `controls.k` | 3 | 34 | Assignment, `if`, `for`, expression statements used |
| `functions.k` | 4 | 15 | Function frame, return, and pop used |
| `call.k` | 3 | 21 | Closure and bound-method call paths used |
| `assert.k` | 0 | 3 | Concrete-test assertions only |
| `bool.k` | 0 | 13 | Boolean behavior; no problematic target path |
| `builtins.k` | 38 | 137 | Builtins map and `len` in sensitivity witness |
| `range.k` | 2 | 6 | Unused by submitted algorithm |
| `float.k` | 34 | 121 | Unused |
| `str.k` | 5 | 28 | Unused |
| `set.k` | 6 | 12 | Unused |
| `tuple.k` | 4 | 21 | Unused |
| `dict.k` | 12 | 28 | Unused |
| `subscript.k` | 15 | 40 | Unused |
| `sort.k` | 6 | 19 | Unused |
| `methods.k` | 27 | 75 | Generic method framework; append dispatch reaches `list.k` |
| `comprehension.k` | 3 | 7 | Unused |
| `concrete.k` | 5 | 16 | Unused by proof target |

The 25 baseline `symbol` declarations (22 also `no-evaluators`) are listed in
the inventory. They concern floats, sorting, and MD5 and are unreachable from
this integer/list-only target. No opaque supplied primitive affects the target
result.

### Used-construct map

| Submitted construct | Declaration/rule path |
|---|---|
| `Module`, `FuncDef`, `Params`, statement list | `syntax.k`; `core.k` load/sequencing; `functions.k` definition |
| Direct closure call and parameter binding | `call.k` closure rule; `functions.k #bindP/#endcall/#pop` |
| `Assign`, `Name`, `Int`, `Bool` | `syntax.k` strictness; `controls.k`; `core.k` lookup/literals |
| `ListExpr()` | `list.k #evalArgs/#applyK(toList,...)`; `core.k #alloc`—but proof priority rule preempts it |
| `For` over input | `controls.k` dereference/`#loop`; `list.k #iterNext`—but universal claim uses proof-added iterator rules |
| `If` and return | `controls.k #branch`; `functions.k` return/pop |
| unary `-` | `operators.k`; `int.k applyUn` |
| `in seen` | compare contexts in `operators.k`; membership machine in `list.k` |
| `seen.append(value)` | `call.k` attribute/bound-method flow; priority append mutation in `list.k` |
| final expression statement | `controls.k Expr` discard |

On ordinary integer lists these supplied paths preserve left-to-right
evaluation, mutate only the allocated `seen` heap object, leave input unchanged,
and restore the call environment, scopes, stack, and return cell.

### Every proof-local declaration and rule

The exact 12 syntax declarations and 24 rules are entries 1095–1133 in the full
inventory. Their decisions are:

| `verification.k` lines | Extension | Decision |
|---|---|---|
| 6–14 | `pairLoopBody` function and equation | Sound definitional AST alias; exact loop body |
| 18–31 | `pairsBody` function and equation | Sound definitional AST alias for the current translated source |
| 34–37 | `oppositeIn`, two equations | Correct recursion on integer `vCons`; declared too broadly total over all `ValSeq` |
| 42–45 | `pairsSpec`, two equations | Correct distinct-position contract on integer `vCons`; same broad-totality limitation |
| 49–55 | `seenAfter`, three equations | Guards are complementary on intended integer lists and recursion descends; broad-totality limitation outside that domain |
| 61 | `intValues(IntSeq)` | Fresh opaque algebraic representation; no equation or bridge-free connection to ordinary `vCons` |
| 63–66 | `snocIS`, two equations | Sound, disjoint, exhaustive, descending |
| 68–71 | `memberIS`, two equations | Sound, disjoint, exhaustive, descending |
| 73–74 | `oppositeIS` | Sound definition; unused by the main claim |
| 78–82 | `scanIS`, two equations | Sound mathematical scan over earlier positions; exact Boolean result |
| 84–85 | `pairsIS` | Sound name for `scanIS(INPUT,.IntSeq)` |
| 87–93 | `seenAfterIS`, two equations | Sound, exhaustive, descending |
| 97–99 | two `#iterNext` rules for `intValues` | Internally consistent observations for the new constructor, but operational rules for a synthetic object, not a connection to fixed list execution |
| 103–104 | `valSeqConcat(intValues(...), singleton)` | Correct homomorphism for the one append shape used; does not make the extended `ValSeq` representation generally equivalent or restore all baseline total functions |
| 115–117 | priority empty-list allocation bridge | **Materially unsound operational bridge; concrete false-conclusion witness below** |
| 119–160 | promoted loop rule | Based on a separately closing loop claim, but copied with a broader match: arbitrary builtins scope and omitted `exc`/`exit-code` restrictions versus the proved claim. No false target-domain result was found for the exact main state, so this is recorded as a narrower justification/context-containment gap, not independently labeled unsound |

The IntSeq functions have constructor-complete and non-overlapping equations.
The guarded `seenAfter` rules use `B` versus `notBool B`; on the intended
integer domain they are disjoint and exhaustive. By contrast, proof-local
functions declared total over `ValSeq` do not cover non-integer heads or the
new `intValues` constructor. More seriously, extending `ValSeq` with
`intValues` leaves supplied total functions such as `vsLen` without an
equation, which the sensitivity test reaches.

The two priority rules deliberately preempt fixed rules. There are no local
simplification rules, `symbol` attributes, or `no-evaluators` attributes.
Nevertheless, `intValues` is result- and state-bearing: it controls input
iteration, membership, append state, the final heap, and ultimately the result
summarized by the promoted loop.

### Concrete false-conclusion witness

For the real intended input `[]`, use the exact submitted closure body and
ordinary argument `list(.ValSeq)`:

1. Under the base definition, fixed execution proves return `false` and final
   heap `0 |-> list(.ValSeq)` (`stage5_fixed_correct_heap.log`, exit 0,
   `#Top`).
2. The same source configuration with claimed heap
   `0 |-> list(intValues(.IntSeq))` is rejected by the base definition
   (`stage5_fixed_rejects_synthetic_heap.log`, exit 1,
   `WarnStuckClaimState`); the residual shows the real `.ValSeq` heap.
3. Under the candidate's lemma definition, that false fixed-semantics synthetic
   heap conclusion proves (`stage5_extended_accepts_synthetic_heap.log`, exit
   0, `#Top`).

Thus the line 115 bridge changes an observable K cell for a satisfying,
intended-domain input and can enable a false conclusion about real execution.
This meets the required concrete unsoundness witness. The source and exact
commands are [`stage5_bridge-witness.k`](evidence/stage5_bridge-witness.k) and
[`stage5_bridge_checks.sh`](evidence/stage5_bridge_checks.sh).

An independent context-containment witness strengthens the finding.
`assert len([]) == 0` completes under the fixed base definition with `.K`,
`NoExc`, and exit 0. Under the bridge-enabled definition, `krun` exits 111 with
conditions containing unresolved `vsLen(intValues(.IntSeq))` and an
`AssertionError` branch. See
[`stage5_bridge_context.py`](evidence/stage5_bridge_context.py),
`stage5_context_fixed.log`, and `stage5_context_extended.log`. The allocation
bridge accepts an arbitrary continuation, but its few iterator/append equations
do not justify that match domain.

## 6. Fresh non-vacuity test

The reviewer-authored mutation leaves the source and every post-state cell
unchanged but replaces the main result with `notBool pairsIS(INPUT)`. It is
demonstrably false at the satisfying input `[0,0]`: both Python
implementations and `pairsIS` are true, while the mutated target is false.

- `kprove --dry-run` exits 0, so the mutation parses and builds.
- The real mutation proof exits 1 with `WarnStuckClaimState`.
- The residual is the expected unmet equality
  `notBool scanIS(INPUT,.IntSeq) == scanIS(INPUT,.IntSeq)`, not a parser,
  import, timeout, or unrelated failure.

The mutation and exact evidence are
[`stage6_false-mutation.k`](evidence/stage6_false-mutation.k),
[`stage6_nonvacuity.sh`](evidence/stage6_nonvacuity.sh),
`stage6_mutation_dry_run.log`, and `stage6_mutation_proof.log`.

The extended theorem is therefore result-constraining and non-vacuous. This
does not make its substituted execution model sound.

## 7. Proven versus assumed accounting

### What the successful reachability proofs establish

Conditional on the supplied semantics **plus all proof-local rules**, the
machine checks:

- direct fixed-semantics calls for ordinary lists of lengths 0, 1, and 2;
- the synthetic-list membership summary;
- the loop summary over synthetic remaining/seen sequences, with the separately
  proved membership claim trusted in that modular step;
- for every `INPUT:IntSeq`, a direct call of the exact duplicated body on
  `list(intValues(INPUT))` reaches Boolean `pairsIS(INPUT)` and the stated
  synthetic heap prefix.

The result is not a free variable, tautology, or one-way implication.
`pairsIS` is a total, explicit Boolean recursion, and the fresh false mutation
is rejected. These are partial-correctness reachability results; they do not by
themselves assert termination.

### Trust and assumption ledger

| Boundary | Influence | Assessment |
|---|---|---|
| Supplied reference MPY semantics | All execution, cells, evaluation, calls | Acceptable named trust boundary required by `SUPPLIED_SEMANTICS`; integrity verified |
| K v7.1.337 compiler/prover/backend | Proof checking | Standard unavoidable tool trust; fresh builds used |
| Trusted CPython-AST translator | Source-to-`.mpy` bridge | Acceptable here; trusted mount and byte identity verified |
| Manual `pairsBody`/`pairLoopBody` duplication | Selects executed body | Current AST is exact, but linkage is not mechanical; documented concern |
| Transparent `pairsIS`/`memberIS` mathematics | Final Boolean contract | Ordinary recursive mathematics; correct for finite integer sequences |
| `intValues(IntSeq)` as real-list surrogate | Input iteration, membership, state, result | **Illegitimate assumption**: no bridge-free universal connection to real `vCons` execution |
| Priority empty-list allocation bridge | Heap payload and downstream operations | **Illegitimate**: false fixed-semantics heap conclusion demonstrated; arbitrary continuation not contained |
| Promoted loop rule | Skips the target loop, returns final result, pops frame, updates heap | Concerning/underjustified beyond the exact separately proved claim; main theorem depends on it |
| Baseline opaque float/sort/MD5 symbols | None on target path | Irrelevant |
| Differential and ground tests | Source-intent and finite bridge evidence | Supportive only on tested cases; not a universal K connection theorem |
| Missing generation provenance | Audit trail only | Concerning, not independently dispositive |

### Decision

The reconstructed `#Top` and successful non-vacuity test are real, and the
Python implementation itself appears correct. The proof nonetheless fails the
mandatory real-program soundness and pinning gate. Its universal theorem starts
from a proof-added list representation, and its operational allocation bridge
provably changes the real target execution state for `[]`. This is exactly a
substituted-program/materially-unsound-proof-rule case under the decision
boundary. Finite differentials, bounded real executions, and the transparent
mathematical oracle cannot substitute for the missing bridge-free universal
connection theorem.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
