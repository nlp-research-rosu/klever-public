# Independent adversarial review: 130-tri

This is a completed seven-stage audit in `SUPPLIED_SEMANTICS` mode. I rebuilt
everything from source in `/tmp/audit-work`; no candidate-provided compiled
definition or cache was used.

The candidate's two reachability claims do close freshly, and the proof is
non-vacuous and sensitive to a wrong loop body. Nevertheless, the entry claim
does not constrain the returned `ValSeq` to the requested sequence. It only
constrains the proof-local, incompletely characterized
`prefixIndex(?RESULT)` symbol. There is no proved connection from that property
to equality with the concrete Tribonacci list. A true whole-result
strengthening fails, and the proof-local property cannot even establish its
claimed index on the correct ground concrete list `[1, 3, 2, 8]` when presented
extensionally. The successful proof therefore establishes a representation-
dependent ghost/index property, not partial correctness for the requested
return value. This is a material adequacy failure under the problem's decision
boundary.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode and mounts are consistent:

- `/reference/reference-semantics` exists and contains `semantics.k` plus 23
  helper `.k` files.
- The candidate's `/candidate/reference-semantics` has the same directory and
  regular-file entry types, contains no symlink, has no missing or extra entry,
  and is recursively byte-identical to the trusted tree.
- `diff -ruN --no-dereference` exited 0.

This is not an infrastructure breach, so a candidate verdict is appropriate.
The complete entry-type listings, hashes, comparisons, and statuses are in
[`evidence/stage1_integrity.sh`](evidence/stage1_integrity.sh) and
[`evidence/stage1_integrity.log`](evidence/stage1_integrity.log).

The candidate's `prompt.py` and `py2mpy.py` are byte-identical to
`/reference/prompt.py` and `/reference/py2mpy.py` respectively (`cmp` exit 0).
All execution-relevant candidate sources are regular files and present:
`solution.py`, `solution.mpy`, `spec.k`, `verification.k`, and `prove.sh`.

### Missing and extra provenance artifacts

The following named artifacts are missing:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`

No structured trace (`*trace*`, `*.jsonl`, or other JSON file) is present.
Therefore there were no generation claims in those artifacts to inspect.
`/candidate/__pycache__/solution.cpython-310.pyc` is an extra generated cache;
it was ignored and never copied or executed. There is also no candidate
`spec-vacuity.k`; the non-vacuity artifact used below is reviewer-authored.

The missing provenance weakens auditability but was not used to manufacture the
substantive verdict: all source, proof, differential, and mutation checks were
independently reproducible.

### Isolation

Trusted inputs were copied to `/tmp/audit-work/trusted`. The candidate proof and
program sources, but not its cache, were copied to
`/tmp/audit-work/reconstruction`; the semantics used there came directly from
the trusted reference tree. The copy record is
[`evidence/scratch_copy.log`](evidence/scratch_copy.log).

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

From the trusted prompt and canonical implementation, the intended domain is a
non-negative Python integer `n`. The result is a list of length `n + 1`
containing indices 0 through `n`, with:

- index 0 equal to 1 (shown by the example and canonical base case);
- index 1 equal to 3;
- even index `i >= 2` equal to `1 + i / 2`;
- odd index `i >= 3` equal to the previous two values plus the value at the
  following even index, equivalently
  `tri[i-1] + tri[i-2] + 1 + (i+1)/2`.

The candidate uses a `while` loop with rolling variables `a` and `b`. On
non-negative integers its `//` expressions are exact integer versions of these
integer-valued divisions. The assignments after each append advance
`a,b` from values at `i-2,i-1` to values at `i-1,i`.

### Trusted translation

I regenerated `solution.mpy` from the scratch copy of `solution.py` with the
trusted translator:

```text
python3 /reference/py2mpy.py solution.py | tee solution.regenerated.mpy
cmp solution.mpy solution.regenerated.mpy
```

Both commands exited 0. Both files have SHA-256
`981dfdba56e992c7f3c332501505f3eccf7c04c752418534a06c9ce2874544e6`.
See [`evidence/stage2_fidelity.log`](evidence/stage2_fidelity.log).

### Independent differential test

[`evidence/differential_test.py`](evidence/differential_test.py) imports the
trusted `/reference/canonical.py:tri` and the scratch candidate
`solution.py:tri` through independent module loaders. Its complete scope was:

- documented cases `n = 0, 3`;
- branch boundaries `n = 1,2,3,4,5,6`;
- every integer in `0..64`;
- 200 deterministic draws from `0..500` using seed 130;
- 216 unique non-negative inputs in total.

The command exited 0 with zero Python-equality value mismatches. Representative
results included `n=3`, for which the candidate returned `[1,3,2,8]` and the
canonical returned `[1,3,2.0,8.0]`.

There is a real type-level difference: 214 of 216 inputs had a recursive
element-type mismatch. For every tested `n >= 2`, the canonical implementation
returns floats after the first two elements because it uses `/`, whereas the
candidate returns integers because it uses `//`. Python list equality treats
these numerically equal, and the prompt's example prints integers, so this is
an intent-model limitation rather than the principal failure. The complete
inputs and results are in
[`evidence/stage2_fidelity.log`](evidence/stage2_fidelity.log).

## 3. Clean proof reconstruction

The toolchain was independently available:

```text
K version: v7.1.337
Build date: Thu Jun 18 07:59:56 CDT 2026
```

Before building, both `runtime-kompiled` and `verification-kompiled` were
confirmed absent. The exact reconstruction script is
[`evidence/stage3_reconstruct.sh`](evidence/stage3_reconstruct.sh), and its
bounded combined output is
[`evidence/stage3_reconstruction.log`](evidence/stage3_reconstruction.log).

The concrete definition was built from the trusted supplied semantics:

```text
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

It exited 0. The reviewer-authored concrete harness executed the exact submitted
function term and asserted the results for `n = 0,1,2,3,4,10`; `krun` exited 0.
The harness is
[`evidence/concrete_harness.mpy`](evidence/concrete_harness.mpy).

The LLVM build reported non-exhaustive `total` warnings for `mapStrVS`,
`floorFI`, `toF`, `ceilF`, `joinCodes`, and `valSeqAt`. None is used by this
program, whose executed subset consists of integer operators, lists, calls,
conditionals, and a while loop. These warnings remain part of the fixed,
trusted semantics boundary rather than candidate proof extensions.

The proof definition was freshly built with:

```text
kompile verification.k \
  --backend haskell \
  --main-module TRI-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

This exited 0. Each positive target was then run independently:

```text
kprove spec.k --definition verification-kompiled \
  --spec-module TRI-LOOP-SPEC --output pretty
#Top
exit=0

kprove spec.k --definition verification-kompiled \
  --spec-module TRI-CORRECT-SPEC --output pretty
#Top
exit=0
```

Thus the clean dynamic reconstruction gate succeeds. The remaining question is
what those successful claims establish.

## 4. Adequacy and real-program pinning

### Loop claim in plain language

The loop claim starts at `#while(TriLoopCond, TriLoopBody)` with:

- `I >= 2`, `R >= 0`, and `n = I + R - 1`;
- local `i = I`;
- locals `a = triAt(I-2)`, `b = value = triAt(I-1)`;
- a heap list `VS` for which `prefixIndex(VS) = I-1`;
- arbitrary continuation `KREST` and arbitrary preserved stack `STACK`;
- no return, exception, or nonzero exit state.

Its postcondition says that execution reaches `KREST`, final `i = I + R`, and
`prefixIndex(?OUT) = I + R - 1`. It deliberately leaves final `a`, `b`, and
`value` existential and does not say `?OUT = triPrefix(I+R-1)` or equate
`?OUT` to any concrete sequence.

A satisfying witness exists: `I=2`, `R=0`, `H=0`,
`VS=[1,3]`, `n=1`, `a=1`, `b=value=3`, and `i=2`.
All loop requires clauses hold. The witness record is
[`evidence/stage4_witness.py`](evidence/stage4_witness.py), whose run is in
[`evidence/stage4_adequacy.log`](evidence/stage4_adequacy.log).

### Entry claim in plain language

For every K integer `N >= 0`, the entry claim directly calls

```text
closureVal(("n", .ParamNames), TriFunctionBody, 0)
```

with argument `Int(N)`. It says that the call returns `ref(0)`, leaves
`0 |-> list(?RESULT)` in the heap, increments `heapLoc` from 0 to 1, restores
the caller environment and stack, and leaves no exception. The only property
of the list contents is:

```text
prefixIndex(?RESULT) = N
```

This is encoded as paired `<=Int` and `>=Int` inequalities. `?RESULT` is
otherwise existential.

`N=3` is a concrete satisfying entry witness. Substitution into the intended
recurrence gives `[1,3,2,8]`, numerically equal to both Python
implementations. Witnesses for `N=0,1,2,3,4,10` are recorded in the same
stage-4 evidence.

### Real-program pinning

The claim does not load `solution.mpy` as a `Module` and then resolve the name
`tri`; it directly constructs a closure with a proof-local `TriFunctionBody`
macro. This bypasses only the module-level `FuncDef` binding and subsequent
name lookup. Static comparison found that:

- `TriFunctionBody` is exactly the submitted function body;
- `TriLoopCond` is exactly `i <= n`;
- `TriLoopBody` exactly matches the translated `If`, `append(value)`, rolling
  assignments, and `i += 1`;
- the closure has the submitted single parameter `n` and defining environment
  0, which is what the supplied module-level `FuncDef` rule creates.

Thus the current body and its real control flow are pinned by duplication, even
though the proof is not automatically sensitive to a future mismatch between
the file and macro. The trusted translation comparison and this static check
make that duplication a limited but acceptable current-program bridge. The
principal failure is the postcondition, not a hidden replacement algorithm.

### Material result-constraint failure

I tested the result abstraction in three independent ways:

1. [`evidence/spec-exact-strengthening.k`](evidence/spec-exact-strengthening.k)
   replaces the weak heap target with the true intended abstract result
   `list(triPrefix(N))`. It builds, but `kprove` exits 1 with
   `WarnStuckClaimState`. The residual already contains the `N=0` final state
   `list(vCons(1,.ValSeq))`, which does not unify with
   `list(triPrefix(0))`.

2. [`evidence/spec-post-discrimination.k`](evidence/spec-post-discrimination.k)
   asks the proof-local `prefixIndex` about the correct concrete ground list
   `[1,3,2,8]`. This also exits 1: the residual is the unmet equality
   `prefixIndex(vCons(1,vCons(3,vCons(2,vCons(8,.ValSeq))))) = 3`.
   A wrong concrete list `[9]` likewise fails, while the abstract tag
   `prefixIndex(triPrefix(3)) = 3` closes trivially with `#Top`.

3. The entry and loop claims never assert equality between `?RESULT`/`?OUT`
   and `triPrefix(...)`, a concrete `vCons` sequence, or any extensional list
   function. They carry only the ghost `prefixIndex` equality across the loop
   circularity.

These are not merely failures to prove an optional strengthening. They show
that the successful postcondition is tied to proof-term construction history
and a fresh abstract tag, and that the candidate contains no formal bridge from
that tag to the observable list value required by the prompt. Differential
testing cannot supply that missing universal K theorem.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[`evidence/rule_inventory.md`](evidence/rule_inventory.md) is a generated,
line-addressable inventory of every local configuration, syntax declaration,
context, rule, and claim in the trusted supplied semantics, `verification.k`,
and `spec.k`. Its source generator is
[`evidence/k_inventory.py`](evidence/k_inventory.py).

The inventory contains 952 entries:

- 1 configuration;
- 206 ordinary syntax declarations;
- 27 symbolic/no-evaluator syntax declarations;
- 5 contexts;
- 700 ordinary rules;
- 11 simplification rules;
- 2 reachability claims.

Across those entries it records 147 `function`, 109 `total`, 24
`no-evaluators`, 27 `symbol`, 45 `priority`, 26 `owise`, 35 `concrete`, 7
`macro`, and 1 `macro-rec` entries; 2 declaration entries contain `strict`
markers and 1 contains a `seqstrict` marker.
There is no explicit `[functional]` declaration. Each inventory entry includes
its complete source span, attributes, and audit disposition.

All entries under the trusted semantics tree are accepted as the selected fixed
semantics because the candidate copy is exactly identical to that authoritative
tree. This does not bless the entries in `verification.k`, which are assessed
below.

### Used-construct coverage and execution

Every constructor in `solution.mpy` has fixed-semantics support:

| Submitted construct | Supplied declaration and relevant behavior |
|---|---|
| `Module`, statement sequence | `syntax.k`; `#loadAll` and sequencing in `core.k` |
| `FuncDef`, `Params` | closure creation in `functions.k`; parameter binding and frame creation in `functions.k`/`call.k` |
| `Int`, `Name` | literal evaluation and chained scope lookup in `core.k` |
| `Compare`, `CmpOp` | ordered operand contexts in `operators.k`; integer comparison cases in `int.k` |
| `BinOp("+","%","//")` | sequential strictness in `syntax.k`; dispatch in `operators.k`; integer rules and `pyMod` in `int.k` |
| `If` | strict condition followed by `truthy` and `#branch` in `controls.k` |
| `ListExpr` | left-to-right element evaluation and fresh heap allocation in `list.k`/`core.k` |
| `Assign`, `AugAssign` | current-frame writes in `controls.k`; integer `i += 1` uses `applyBin("+",...)` |
| `While` | `#while`, condition evaluation, and loop continuation in `controls.k` |
| `Call`, `Attribute` | callee-before-arguments routing in `call.k`; bound method construction |
| `result.append(value)` | the priority-40 list rule appends in place to the referenced heap list |
| `Expr` | evaluates the call for its effect and discards `noneV` |
| `Return` | strict return expression, return state, frame pop, caller restoration, and persistent heap in `functions.k` |

The proof configurations include every fixed cell: `k`, `env`, `scopes`,
`scopeLoc`, `heap`, `heapLoc`, `stack`, `ret`, `exc`, and `exit-code`.
The loop claim preserves the continuation, stack, heap location, scope
location, return state, exception, and exit status while explicitly updating
the locals and the single result-list heap entry. The body has no abrupt
`return`, `break`, or exception path inside the loop, so its arbitrary
`KREST` frame does not hide a control effect used by this program.

### Candidate proof-extension inventory and decisions

The 22 local declarations/rules in `verification.k` are as follows.

| Lines | Extension | Classification and decision |
|---|---|---|
| 9-13 | `triAt`, base rules 0 and 1 | Result-bearing definitional summary. The bases match the prompt. The symbol is `total`, symbolic, and has no evaluators. |
| 15-25 | Two guarded even-index simplifications | Both equate the fixed-semantics value `1 + i//2` with `triAt(i)` for even `i>=2`. Their overlap has the same right-hand side and the equations are ordinary integer mathematics on the guard. |
| 27-40 | Two guarded odd-index simplifications | Both equate the executed odd expression with the recurrence using `triAt(i-1)` and `triAt(i-2)`. Their guards select odd `i>=3`; their overlapping backend forms have the same right-hand side. |
| 44 | `triPrefix(Int)` constructor | Fresh abstract sequence tag. It is not itself an executable oracle, but its connection to an extensional concrete list is not proved. |
| 45-46 | `prefixIndex(ValSeq)` | Fresh, `total`, result-bearing symbolic function with no evaluators. Its equations cover proof-generated base/tag/append forms but not general or even all correct concrete `ValSeq` terms. The final claims depend directly on it. This is the material evidence/adequacy gap. |
| 48-49 | Concrete bases rewrite to `triPrefix(0/1)` | Intended definitional bridge for the two bases. These are ordinary rules rather than a universal equality/connection theorem and did not make the exact heap strengthening close. |
| 50-52 | Base/tag `prefixIndex` simplifications | Truthful on the displayed terms and mutually consistent. The `triPrefix(J)` rule assigns the desired index to the fresh tag but does not establish the tag's concrete contents. |
| 53-58 | Append-step `prefixIndex` simplification | If the old proof term already has index `I-1` and the appended value is syntactically `triAt(I)`, it assigns index `I`. This is a one-way, history-sensitive induction rule, not an inverse theorem characterizing list contents. |
| 59-62 | `valSeqConcat(triPrefix(...),...)` simplification | Intended inductive tag construction. Its guard and index step are consistent, but no bridge-free theorem proves that every accepted tag equals the concrete sequence required by the task. |
| 66-68 | `TriLoopCond` macro | Exact expansion of the submitted condition. |
| 70-86 | `TriLoopBody` macro | Exact expansion of the submitted loop body. |
| 88-100 | `TriFunctionBody` macro | Exact expansion of the submitted function body. |

No candidate-local priority rule, opaque external primitive, allocation
shortcut, return shortcut, or rule that intercepts the program before fixed
execution is present. The arithmetic simplifications run after the supplied
integer operations expose their results. Guard coverage is adequate on the
formal `N>=0` domain; parity guards are disjoint, and the duplicate backend
forms agree on overlap. The base guards do not overlap recurrence guards.

I do **not** classify an individual arithmetic or prefix equation as
mathematically false: there is no concrete false-conclusion witness for such a
claim, and the instructions prohibit calling a rule unsound without one. The
narrower and evidenced defect is that the fresh result-bearing abstraction is
not connected to extensional result equality. It is therefore illegitimate as
the sole statement of the requested return-value theorem even though its
individual equations are consistent.

### Body sensitivity

To test whether the proof merely ignored the body, I generated a one-line
mutation changing the exact loop macro from `append(value)` to `append(999)`.
The generator is
[`evidence/make_body_mutation.py`](evidence/make_body_mutation.py), the complete
mutated source is
[`evidence/verification-body-mutated.k`](evidence/verification-body-mutated.k),
and the clean build/proof record is
[`evidence/stage5_body_sensitivity.log`](evidence/stage5_body_sensitivity.log).

The mutated proof definition built successfully. Both target claims then exited
1 with `WarnStuckClaimState`; the residual explicitly contained:

```text
prefixIndex(valSeqConcat(VS, vCons(999, .ValSeq)))
```

This is valid body-sensitivity evidence. It confirms that the ghost property is
not wholly vacuous, but it does not repair the missing
`prefixIndex`-to-result-equality theorem.

## 6. Fresh non-vacuity test

[`evidence/spec-vacuity-audit.k`](evidence/spec-vacuity-audit.k) is a fresh
mutation of the entry result obligation from index `N` to the false index
`N+1`. `N=0` is a satisfying witness: execution returns `[1]`, for which the
candidate's own base equation gives index 0, not 1.

Exact commands and statuses:

```text
kprove spec-vacuity-audit.k \
  --definition verification-kompiled \
  --spec-module TRI-VACUITY-AUDIT-SPEC \
  --dry-run
exit=0

kprove spec-vacuity-audit.k \
  --definition verification-kompiled \
  --spec-module TRI-VACUITY-AUDIT-SPEC \
  --output pretty
exit=1
```

The second command failed with `WarnStuckClaimState`, not a parser, import,
build, timeout, or unrelated backend error. Its residual is the normal final
state for `N=0` with heap list `[1]`, showing the expected unmet result
obligation. The full record is
[`evidence/stage6_nonvacuity.log`](evidence/stage6_nonvacuity.log).

The proof therefore passes this non-vacuity test.

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Relative to the supplied semantics plus all candidate rules in
`verification.k`, the successful claims establish partial correctness of this
formal statement:

- if the direct closure call with `N>=0` terminates in the specified normal
  configuration, it returns heap reference 0;
- heap location 0 holds some `ValSeq ?RESULT`;
- the proof-local function application `prefixIndex(?RESULT)` is equal to `N`;
- the call restores the caller frame, has no exception, and leaves exit code 0.

The loop circularity similarly establishes the final counter and the propagated
`prefixIndex` relation. As appropriate for this task, neither claim proves
termination.

The successful proof does **not** establish:

- `?RESULT == triPrefix(N)`;
- equality with a concrete list of the recurrence values;
- an extensional theorem saying `prefixIndex(VS)=N` iff `VS` is that concrete
  list;
- identity with the canonical Python result at the element-type level;
- execution of the module-level `FuncDef` and name lookup (these are bridged
  statically by the exact copied body).

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| Trusted supplied MPY semantics and K built-ins/backends | Concrete run and both K proofs | Authorized fixed boundary. The candidate copy is exactly identical. Unused non-exhaustive warnings are disclosed. |
| `triAt` equations | Loop locals, branch results, append summary, `prefixIndex` step | Mathematically consistent recurrence summary on `N>=0`; supported by fixed integer execution and finite differential tests. No separate universal connection theorem to canonical Python float values. |
| `triPrefix` tag and rules | Intended interpretation of the abstract prefix | Concerning: proof-local tag with no successful whole-result connection theorem. |
| `prefixIndex`, `[total,no-evaluators]` | Every loop and entry result obligation | Illegitimate as the sole correctness result. It is incomplete and representation-sensitive; no inverse/extensional theorem connects it to the observable list. |
| `Tri*` body macros | Both target claims | Current text is statically exact and a wrong append mutation invalidates the proof. The module binding/name-lookup wrapper is not executed in the entry claim. |
| Trusted translator | `solution.py` to `solution.mpy` identity | Byte identity established independently. |
| Canonical differential oracle | Intent bridge only | 216 finite inputs, zero numeric-equality mismatches, but systematic float/int type divergence. It cannot replace the K result theorem. |
| Reviewer non-vacuity and body mutations | Discrimination evidence only | Both build and fail for the expected proof obligation. They show sensitivity, not full correctness. |

### Decision

The clean `#Top` results are genuine closure results for the theory that was
built, and the proof is neither trivially vacuous nor body-insensitive.
Nevertheless, the theory's actual entry postcondition is materially weaker than
the required return-value contract. Its only list-content observation is a
fresh symbolic index/tag whose extensional connection is neither stated nor
proved. The true whole-result strengthening and a ground correct-list
characterization both fail. The candidate therefore contains a proof of a
ghost representation property, not a legitimate partial-correctness proof of
the requested generated program result.

The missing provenance artifacts and canonical float-versus-candidate-int
difference are additional limitations, but the material result-constraint gap
alone determines the decision.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
