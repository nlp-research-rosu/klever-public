# Independent adversarial audit: 40-triples-sum-to-zero

The candidate contains a legitimate, result-constraining partial-correctness
proof of the submitted program over arbitrary finite lists of mathematical
integers. Fresh reconstruction succeeds, the claim executes the exact translated
function body, and the four reachability claims have sound invariants.

The verdict is `CONCERNS / LEGIT`, rather than `PASS`, for one non-material
auditability limitation: the result-bearing structural simplifications
connecting the proof's `IntSeq` representation to the supplied semantics'
`vsLen` and `valSeqAt` helpers are true constructor-induction lemmas, but the
candidate installs them directly as `[simplification]` rules and supplies no
separate bridge-free universal machine-checked connection theorem. I found no
false case or unsound rule. Bridge-free ground checks produce distinct correct
values and reject a wrong interpretation; an attempted universal K claim gets
stuck on symbolic structural induction rather than producing a counterexample.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout: pipeline-v3`,
`condition: kit-semantics`, and `semantics_mode: SUPPLIED_SEMANTICS`. The
trusted supplied-semantics mount is present, as required.

I inspected all required launcher and generation records:

- `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`, `/task.json`,
  and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`,
  `runtime-metrics.json`, `usage.json`, `codex-last.txt`, `codex-output.log`,
  and `prompt.txt`;
- all 503 JSON records in the sole structured trace under
  `/generation-evidence/codex-trace/`.

The generation report's `VALIDATED` and `KPROVE_PASSED` statements were treated
only as untrusted claims. The parsed trace inventory and its untrusted final
claim are recorded in
[generation-trace-summary.log](/audit-output/evidence/generation-trace-summary.log).

Independent integrity results are in
[provenance.log](/audit-output/evidence/provenance.log):

- the campaign-lock object exactly equals the campaign block in
  `/audit-input.json`, and its SHA-256 matches;
- every launcher-recorded required regular-file hash matches;
- the structured trace file and trace-tree hashes match their generation
  records;
- the mounted candidate tree has pipeline-v3 digest
  `5c4982f216f0a22da0aff695a7684917ecea62d6723b7b7d37fe3332883fba08`,
  matching `/generation-result.json`;
- candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
  mounts;
- candidate `reference-semantics/` and
  `/reference/reference-semantics/` contain exactly the same 25 directories
  and files, types, and bytes;
- no candidate, reference, or generation-evidence entry is a symlink.

There is no infrastructure breach, missing provenance record, or supplied
semantics integrity failure.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract says that for a list of integers, the function returns
`True` exactly when three distinct list positions have values summing to zero.
The trusted canonical implementation realizes “distinct” as indices
`i < j < k`.

The candidate program enumerates the same increasing triples. It records a
monotone `found` Boolean instead of returning early, which changes execution
cost but not the result. It handles repeated values correctly because
distinctness is positional; for example, `[0,0,0]` is true.

Trusted regeneration:

```text
python3 /reference/py2mpy.py /candidate/solution.py \
  > /tmp/audit-work/fresh/regenerated-solution.mpy
cmp /tmp/audit-work/fresh/regenerated-solution.mpy /candidate/solution.mpy
```

exited 0. Both files have SHA-256
`6c0ecf6c9a08ba5d4962a2421b037bd56552cea88ddbf70f65769395cfcfb816`;
see [translation_identity.log](/audit-output/evidence/translation_identity.log).

The independent differential test
[independent_differential.py](/audit-output/evidence/independent_differential.py)
imports both the trusted canonical entry point and candidate entry point and
also compares them with an independent `itertools.combinations` contract
oracle. Its scope includes:

- all five documented examples;
- lengths 0, 1, 2, and 3; both condition outcomes; duplicate values; and
  triple positions at the beginning, middle, and end;
- all 19,608 lists of lengths 0 through 5 over `[-3,3]`;
- 1,000 deterministic generated lists of lengths 0 through 15 with values up
  to magnitude `10^30`;
- explicit values around `10^100`.

It checked 20,626 cases, with 10,842 true and 9,784 false outcomes, and found
zero mismatches. Exact scope, corpus digest, command, and exit 0 are in
[independent_differential.log](/audit-output/evidence/independent_differential.log).
This is finite fidelity evidence, not a replacement for the symbolic proof.

## 3. Clean proof reconstruction

I copied only source artifacts and trusted inputs to
`/tmp/audit-work/fresh`. Candidate `runtime-kompiled/`,
`verification-kompiled/`, caches, logs, and traces were not reused.

Fresh concrete build:

```text
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

exited 0; see [llvm-build.log](/audit-output/evidence/llvm-build.log). A
reviewer-authored harness has a byte-identical 18-line implementation prefix
and covers examples, empty and short lists, true/false branches, duplicates,
and a `10^30` integer case. CPython and:

```text
krun concrete_harness.mpy --definition runtime-kompiled
```

both exited 0. The K run ends in `.K`, `NoExc`, and exit code 0; see
[concrete_harness.py](/audit-output/evidence/concrete_harness.py) and
[concrete-krun.log](/audit-output/evidence/concrete-krun.log).

Fresh proof build:

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module VERIFICATION \
  --output-definition verification-kompiled
```

exited 0; see [haskell-build.log](/audit-output/evidence/haskell-build.log).
The complete positive proof:

```text
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

exited 0 and printed `#Top`; see
[proof-all.log](/audit-output/evidence/proof-all.log).

I also selected the claims cumulatively so each dependent claim was rerun with
the circularities it needs:

| Target reached | Selected positive claims | Result |
|---|---|---|
| `inner-loop` | `SPEC.inner-loop` | `#Top`, exit 0 |
| `middle-loop` | `SPEC.inner-loop,SPEC.middle-loop` | `#Top`, exit 0 |
| `outer-loop` | inner, middle, outer | `#Top`, exit 0 |
| entry theorem | all four claims | `#Top`, exit 0 |

The bounded logs are
[proof-inner-loop.log](/audit-output/evidence/proof-inner-loop.log),
[proof-middle-loop.log](/audit-output/evidence/proof-middle-loop.log),
[proof-outer-loop.log](/audit-output/evidence/proof-outer-loop.log), and
[proof-triples-sum-to-zero.log](/audit-output/evidence/proof-triples-sum-to-zero.log).

Thus every positive claim closes under a fresh definition. The compiler
warnings concern unused variables in the unchanged supplied `str.k` and the
preserved arbitrary continuation variable; none is a failed totality or proof
obligation.

## 4. Adequacy and real-program pinning

### Claims in plain language

- `inner-loop` assumes `0 <= I < J < K <= len(IS)`. It executes the actual
  innermost while loop from third index `K`, preserves the arbitrary active
  continuation and caller frame, sets `k` to `len(IS)`, and changes `found` to
  `FOUND or thirdFrom(IS,I,J,K)`.
- `middle-loop` assumes `0 <= I < J <= len(IS)`. It executes all second-index
  iterations from `J`, including their real inner loops, ends with
  `j = len(IS)` and `k = 0`, and changes `found` to
  `FOUND or pairFrom(IS,I,J)`.
- `outer-loop` assumes `0 <= I <= len(IS)`. It executes all remaining
  first-index iterations, ends with `i = len(IS)` and `j = k = 0`, and changes
  `found` to `FOUND or tripleFrom(IS,I)`.
- `triples-sum-to-zero` has no size or value bound. For arbitrary
  `IS:IntSeq`, it looks up and calls `triples_sum_to_zero` on the heap list
  represented by `IS` and returns exactly `tripleFrom(IS,0)`.

The helper preconditions are satisfiable; for `IS=[0,0,0]`, witnesses are
`I=0,J=1,K=2` for the inner claim, `I=0,J=1` for the middle claim, and `I=0`
for the outer claim. The entry precondition is satisfiable for every ground
`IntSeq`.

### Constructor-level program identity

[generate_pinning_spec.py](/audit-output/evidence/generate_pinning_spec.py)
uses the fresh definition's parser to extract the sole `FuncDef` from trusted
regeneration. It mechanically checks:

- function label `FuncDef(_,_,_)`;
- name `"triples_sum_to_zero"`;
- sole parameter `"l"`;
- no trailing module statements;
- the complete function-body KAST.

It then generates
[pinning-spec.k](/audit-output/evidence/pinning-spec.k), whose three claims
compare the extracted body with `programBody()`, `triplesClosure()`, and
`solutionBindings()`. `kprove` prints `#Top` and exits 0; frontend normalization
makes the claims trivial only because the nullary definitions expand to the
same constructor tree. See
[pinning-generation.log](/audit-output/evidence/pinning-generation.log) and
[pinning-proof.log](/audit-output/evidence/pinning-proof.log).

The entry claim therefore executes the actual translated closure body, not an
external source filename, an uninterpreted function name, or a substituted
algorithm.

### Result constraint and witnesses

[witness-spec.k](/audit-output/evidence/witness-spec.k) imports
`VERIFICATION`, not the candidate loop claims, and concretely executes the
entry configuration for `[0,0,0] => true` and `[1,2] => false`. Both close in
[witness-proof.log](/audit-output/evidence/witness-proof.log).

[summary-witness-spec.k](/audit-output/evidence/summary-witness-spec.k)
independently substitutes the same inputs into `tripleFrom(IS,0)`; it reduces
to true and false respectively in
[summary-witness-proof.log](/audit-output/evidence/summary-witness-proof.log).
Both candidate and canonical Python implementations agree on those inputs in
the differential log.

The returned value is not free and the postcondition is not an implication or
tautology. It is the nested bounded-existential summary. All unarrowed cells
are preserved, including heap, global/builtin scopes, return state, exception
state, and exit code. Call setup and return restore the module environment,
empty stack, and scope allocator.

The fresh body-sensitivity check changes the closure term actually stored in
the claim's scope to `Return(Bool(true))`, uses the false short-list witness
`[1,2]`, and demands false. The spec dry-runs successfully, then proof exits 1
with `WarnStuckClaimState` and residual `true ~> .K`; see
[body-sensitivity-spec.k](/audit-output/evidence/body-sensitivity-spec.k) and
[body-sensitivity-proof.log](/audit-output/evidence/body-sensitivity-proof.log).
The theorem is therefore sensitive to the executed body.

## 5. Rule-by-rule static soundness review

The exhaustive, line-addressable inventory is
[k-inventory.tsv](/audit-output/evidence/k-inventory.tsv), generated by
[inventory_k.py](/audit-output/evidence/inventory_k.py). It contains 1,137
records: every module/import boundary, configuration, syntax block, context,
ordinary/priority/owise/concrete/simplification rule, function/total
declaration, no-evaluator symbol, and claim in all 25 supplied K files plus
candidate `verification.k` and `spec.k`. Totals include 613 ordinary rules, 45
priority rules, 26 owise rules, 35 concrete rules, 2 simplification rules, 130
function-declaration blocks, 23 no-evaluator symbol blocks, 5 contexts, one
configuration, and four claims. Counts and the inventory SHA-256 are in
[k-inventory.log](/audit-output/evidence/k-inventory.log).

### Supplied semantics disposition

The following table decides the relevance and disposition of every supplied
module's inventoried records. “Inert” means its constructor patterns cannot
occur on the submitted program/proof path; it is still included in the full
inventory.

| Supplied module/file | Disposition for this theorem |
|---|---|
| `semantics.k` | Assembly only; imports are byte-identical to the trusted supplied tree. `MPY-CONCRETE` is absent from the Haskell proof definition. |
| `syntax.k` | Used declarations map `Module`, `FuncDef`, `Params`, `Assign`, `Name`, `Bool`, `Int`, `While`, `Compare/CmpOp`, `Call`, `BinOp`, `Subscript`, `If`, `AugAssign`, and `Return` exactly. All other syntax is absent and inert. Strict/seqstrict annotations provide the used evaluation order. |
| `core.k` | Used configuration, statement sequencing, lookup, builtin scope, argument evaluation, literals, Boolean truth, `vsLen`/`isLen`, and value/scope constructors are consistent with the exact state. Allocation/cell/closure-capture paths are absent. Heap key `-1` is never allocated or read by the program. |
| `call.k` | Generic call evaluates callee then arguments, dereferences the list argument for `len`, binds the exact closure, pushes one frame, and preserves the caller continuation. No method/type/fold route matches. |
| `functions.k` | Plain closure definition, one-parameter binding, `Return`, and `#pop` implement the used function lifecycle. Abrupt return correctly discards the remaining function-body suffix and restores all modeled frame state. Annotated closure paths are inert. |
| `controls.k` | Name assignment/augmented assignment, `If`, and `While/#while/#whileCond/#loopLbl` exactly model the source path. Loop counters increase; no break/continue/import/reference branch matches. |
| `operators.k`, `int.k` | Used left-to-right arithmetic and comparison dispatch reduces only integer `+`, `<`, and `==`; these are ordinary mathematical-integer operations. Reference, membership, unary, division, and other cases are inert. |
| `subscript.k` | Used list/ref dereference, nonnegative `normIdx`, and `valSeqAt` path is exact. Every source access is in bounds by the loop guards. The supplied total but underspecified out-of-bounds cases are unreachable. Slice and string/tuple paths are inert. |
| `builtins.k` | Only `len(list(VS)) -> vsLen(VS)` is used. All fold, conversion, range, eval, and MD5 declarations/rules are inert. |
| `bool.k` | Used only through Boolean truth of comparison results; BoolOp rules are inert. |
| `list.k` | The `list(ValSeq)` representation is used, but literal allocation, iteration, concatenation, comparison, mutation, and membership rules do not occur in the proof path. |
| `iter.k`, `range.k`, `float.k`, `str.k`, `set.k`, `tuple.k`, `comprehension.k`, `methods.k`, `sort.k`, `dict.k` | All operational and equational rules are inert for this program. Their opaque/no-evaluator symbols cannot influence a branch, cell, or result. |
| `assert.k` | Imported in `MPY` but inert on the theorem path because the submitted function and claims contain no `Assert`; exercised successfully by the fresh LLVM harness. |
| `concrete.k` | `MPY-CONCRETE` is not imported by the Haskell theorem and is used only by the fresh LLVM test definition. |

The priority rules that matter are the supplied ref-dereference rules before
generic builtin/subscript dispatch. Their complete matched states agree with
ordinary list reads and preserve all other cells. No candidate priority,
owise, concrete, or anywhere rule exists.

### Candidate `verification.k`: all declarations and 26 rules

The eight syntax blocks and all rule groups are:

1. `intVals` (two rules) is an exhaustive, injective constructor-by-constructor
   embedding from finite `IntSeq` to integer-valued `ValSeq`.
2. `intSeqGhost` is a plain `Val` constructor, not a function or oracle. It
   occurs only at inaccessible heap key `-1`, is unchanged across every claim,
   and is read by no semantics rule.
3. `intAt` (four rules) covers empty sequence, zero, positive, and negative
   index cases. Guards are disjoint; positive recursion consumes one
   constructor. Its out-of-bounds zero totalization does not affect any source
   access because the connection rule is guarded in bounds.
4. The two `[simplification]` rules state
   `vsLen(intVals(IS)) = isLen(IS)` and, for `0 <= I < isLen(IS)`,
   `valSeqAt(intVals(IS),I) = intAt(IS,I)`. Both follow by constructor
   induction and agree with overlapping ground supplied rules. They alter no
   cell or control state.
5. `thirdFrom` (three rules), `pairFrom` (three), and `tripleFrom` (three) have
   pairwise-disjoint and exhaustive guards. Invalid/base cases return false.
   Recursive cases advance `K`, `J`, or `I` toward the fixed finite length.
   Their step equations are exactly the nested existential over
   `i < j < k` and the sum-equals-zero test.
6. `innerCond/body`, `middleCond/body`, `outerCond/body`, and `programBody`
   (seven rules) are ground nullary constructor abbreviations. The mechanical
   pinning proof shows their full expansion equals trusted regeneration.
7. `triplesClosure` and `solutionBindings` (two rules) bind the exact function
   name, sole parameter, exact body, and defining environment 0.

No candidate function has overlapping contradictory equations. The fresh
Haskell build reports no candidate non-exhaustive-totality warning.

### Candidate `spec.k`: all four claims

The three loop claims match the real `#while` heads and exact local/global
bindings. Each accepts an arbitrary active K suffix and saved caller
continuation, preserves both, executes only the loop prefix, and stops when its
right-hand pattern is reached. Each includes exact environment, scope
allocator, heap, heap allocator, stack frame, return, exception, and exit-code
state. No claim invents return, exception, allocation, mutation, or frame
unwinding.

The inner claim proves one third-index suffix; the middle claim uses the
already-proved inner circularity; the outer uses both; and the entry claim uses
all three. Cumulative reruns demonstrate that dependency order. The entry
claim's exact closure binding and body are independently pinned.

### Structural-connection limitation

Because list values affect branches and the final result, I attempted a
bridge-free universal K connection proof. The separate definition
[connection-verification.k](/audit-output/evidence/connection-verification.k)
imports only the supplied semantics and auditor-local copies of `intVals` and
`intAt`; it deliberately omits the candidate simplification rules. It compiles
successfully. The universal claim in
[connection-spec.k](/audit-output/evidence/connection-spec.k) remains stuck on
the symbolic equality `vsLen(auditIntVals(IS)) = isLen(IS)`; see
[connection-proof.log](/audit-output/evidence/connection-proof.log). This is
an inability of that functional reachability shape to perform structural
induction, not a false witness.

Bridge-free ground claims cover empty/nonempty lengths and first/middle/last
indices with distinct values and print `#Top`; see
[connection-ground-proof.log](/audit-output/evidence/connection-ground-proof.log).
The opposite interpretation demanding `99` for the middle element of
`[7,-3,11]` builds, then fails with residual `-3 ~> .K`; see
[connection-opposite-proof.log](/audit-output/evidence/connection-opposite-proof.log).

Accordingly, I do not label either structural rule unsound: there is no false
conclusion witness, and the equations have a direct ordinary-mathematics
induction proof. The missing separate universal machine-checked connection
artifact is the narrow reason for `CONCERNS`.

## 6. Fresh non-vacuity test

I did not rely on candidate `spec-vacuity.k`. The fresh mutation
[fresh-false-spec.k](/audit-output/evidence/fresh-false-spec.k) uses
`[1,-1,0]`, whose three positions sum to zero, executes the exact candidate
closure, and changes the result obligation from true to false.

The dry run exits 0, establishing that the mutation parses and builds. The
actual proof exits 1 with `WarnStuckClaimState`; the residual configuration
contains `true ~> .K` against the demanded false result. The state is
satisfiable, and the contract oracle, canonical Python, and candidate Python
all return true for this input. Exact commands and bounded output are in
[fresh-false-proof.log](/audit-output/evidence/fresh-false-proof.log).

This is a reachable unmet result obligation, not a parser error, crash,
timeout, or irrelevant mutation. The proof is non-vacuous.

## 7. Proven versus assumed accounting

### What the reachability proof establishes

Conditional on the supplied MPY semantics, K toolchain, and the truthful local
equations listed below, the exact submitted call
`triples_sum_to_zero(ref(0))` on every arbitrary finite integer sequence
terminating under that semantics returns `tripleFrom(IS,0)`. The equations
define that Boolean to be true exactly when there are indices
`0 <= i < j < k < len(IS)` whose mathematical integer values sum to zero.
There is no finite length or integer magnitude bound.

This is partial correctness. Termination is not itself a reachability theorem,
although the concrete implementation's three counters plainly progress to a
fixed finite length and all tests terminate.

### Trust ledger

| Boundary | Effect and dependents | Assessment |
|---|---|---|
| Trusted `/reference/reference-semantics` | Defines all source evaluation, state, calls, loops, and primitives. All claims depend on it. | Acceptable benchmark-supplied trust boundary; exact candidate copy verified. Used rule subset audited above. |
| Trusted `/reference/py2mpy.py` | Connects `solution.py` to `solution.mpy`. | Acceptable; trusted regeneration is byte-identical. |
| K v7.1.293, Haskell/LLVM backends, builtin Int/Bool/Map/List theories | Proof execution and mathematical primitives. | Standard toolchain trust; versions match launcher records. |
| `intVals`, `intAt`, `vsLen` and `valSeqAt` structural equations | Determine list length, every indexed source value, branches, summaries, and final result. | Equations are sound by direct constructor induction and ground/opposite checks. Concern: no separate universal machine-checked bridge-free theorem accompanies the candidate. |
| `thirdFrom`, `pairFrom`, `tripleFrom` | Formal result specification and loop invariants. | Truthful exhaustive recursive definitions; no opaque result oracle. Their equivalence to the natural-language increasing-index existential is an ordinary mathematical unfolding argument. |
| `intSeqGhost` | Helps symbolic circularity matching; preserved in heap key `-1`. | Inert, no value/control/state influence visible to the program. |
| Source abbreviations and closure binding | Select the executed program body. | Machine-checked constructor identity and fresh body-sensitivity rejection. |
| Differential/concrete evidence | Supports Python fidelity and ground semantic behavior. | Finite evidence only; not used as the universal proof. |

There is no proof-local external oracle, opaque sort primitive, answer-encoding
rule, unconstrained result, or execution-bypassing operational rewrite on the
program path. The source-to-property bridge covers the full material HumanEval
domain of arbitrary finite mathematical-integer lists.

Gate summary:

- real-program soundness and non-vacuity: pass, with the structural-lemma
  auditability limitation above;
- intent adequacy: pass;
- reproducible evidence/trust accounting: concern, because the candidate
  labels itself `VALIDATED` without a separate universal bridge-free
  connection proof for the two result-bearing simplifications.

The limitation does not make a false conclusion provable and does not narrow
the source-contract domain, so the proof remains legitimate.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
