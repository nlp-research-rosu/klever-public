# Independent adversarial review: 104-unique-digits

This audit used the required `using-kit` and `validating-proof` procedures. It
treated everything under `/candidate` and all generation records as untrusted
evidence. All executable reconstruction was performed from copied source under
`/tmp/audit-work`; candidate-provided kompiled directories, caches, logs,
`PROOF.md`, and mutation results were not reused.

## 1. Input and provenance integrity

The launcher declares `record_layout = pipeline-v3`,
`condition = kit-semantics`, and
`semantics_mode = SUPPLIED_SEMANTICS`. The trusted
`/reference/reference-semantics` mount is present, so the mount state agrees
with the rendered mode.

I read `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
`/task.json`, `/generation-result.json`, all seven required files in
`/generation-evidence`, and every one of the 1,464 JSONL records in the
structured trace. The generation records were used only to understand what the
candidate claimed; none was used as proof evidence.

The independent checks in
`/audit-output/evidence/provenance_check.py` and the successful bounded log
`/audit-output/evidence/stage1-provenance.log` establish:

- Every pipeline-v3 required file is a real regular file, every required tree
  is a real directory, and the audited mounts are read-only.
- No symlink occurs anywhere in `/candidate`, `/reference`, or
  `/generation-evidence`.
- The SHA-256 values of the campaign lock, canonical source, prompt,
  translator, run/task/result manifests, invocation, metrics, runtime metrics,
  usage, prompt, last message, output log, and structured-trace file equal the
  corresponding recorded values.
- The JSON in `/audit-campaign-lock.json` exactly equals the campaign block in
  `/audit-input.json`, and its raw digest is
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
- The task-owned fields of the embedded manifest equal `/task.json`; the one
  launcher-added `config` field equals `manifest_config`. The raw task hash is
  the declared
  `9afc0c7ec3678db767e561658e8f500c2c098ba5a7b5f3691549648d390ec4bb`.
- An independent implementation of the pipeline-v3 tree digest gives
  `d0e48191b1bc10e9bce764f867586ca62a040223e19b7943a9b39692b2523af4`
  for the mounted candidate, equal to the finalized generation result, and
  `baed98c31e85c893f9ecb67154a62f7c198f0ef036db1cc746c7f60cdcca01a4`
  for the trace, equal to `usage.json`.
- `/candidate/prompt.py` and `/candidate/py2mpy.py` are byte-identical to their
  trusted mounts.
- Recursive, no-symlink comparison of
  `/candidate/reference-semantics` against
  `/reference/reference-semantics` reports no missing, additional, mistyped,
  or changed entry. Both independently produce the pipeline tree digest
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`.

There is no audit-infrastructure breach. The files ending in `-initial.log`
under `/audit-output/evidence` preserve reviewer-side check development: one
initial schema comparison was too strict, one handwritten differential
expectation incorrectly included `101`, one K parser mode did not accept
claim-internal `.Exprs`, and one inventory script over-escaped its regexes.
The corrected scripts and final logs are the evidence cited here; none of those
reviewer-side corrections indicates a candidate defect.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

From `/reference/prompt.py` and `/reference/canonical.py`, the intended domain
is a finite list of positive integers. The result must retain exactly those
input elements whose ordinary decimal digits are all odd, preserve
multiplicity, and return the retained elements in increasing order.

The generated `/candidate/solution.py` uses a numeric implementation. For each
positive value it computes the identity `sum((value,))`, repeatedly examines
the current last decimal digit through parity and divides by ten, appends the
original value iff no even digit was seen, and finally calls `sorted`.
This is a different algorithm from the canonical string-based implementation
but is equivalent on the documented positive-integer domain. Its behavior on
zero and negative integers is not canonical, but those values are outside the
source contract. The formal K theorem actually characterizes the literal
generated behavior for all K integers; it does not narrow the required
positive domain.

### Trusted regeneration

The exact command and status are in
`/audit-output/evidence/stage2-fidelity.log`:

```text
python3 /tmp/audit-work/trusted/py2mpy.py \
  /tmp/audit-work/candidate-src/solution.py |
  cmp - /tmp/audit-work/candidate-src/solution.mpy
EXIT_STATUS: 0
```

Thus the submitted `solution.mpy` is byte-identical to regeneration with the
trusted translator. The copied and mounted `solution.py` and `solution.mpy`
hashes also agree.

### Independent differential evidence

`/audit-output/evidence/differential_test.py` imports the trusted canonical
entry point and generated entry point independently and also uses a direct
contract oracle. It covers:

- both prompt examples;
- the empty list and smallest positive/even values;
- one-iteration keep/drop branches;
- an even digit in every decimal position;
- all-odd multi-digit values;
- powers-of-ten boundaries;
- sorting and duplicate preservation;
- large positive integers;
- every singleton from 1 through 20,000;
- all ordered pairs from 23 selected boundary values; and
- 2,000 seeded generated lists of lengths 0 through 24 with values below
  `10^30`.

The exact input construction is preserved in the script, with 22,543 cases and
serialized input digest
`47918d531fa1ab9222dedf4b941b8c2ad425bb0032ff34729cbe84d73bd89daa`.
The final result was `mismatch-count=0`, exit 0. This is finite adequacy
evidence, not a substitute for the K proof.

## 3. Clean proof reconstruction

Only `solution.py`, `solution.mpy`, `verification.k`, and `spec.k` were copied
from the candidate. The semantics used in scratch came from the trusted
reference mount. No candidate-built definition or cache was copied.

The observed toolchain was K 7.1.293 for `kompile`, `krun`, and `kprove`.

### Concrete definition

The fresh LLVM build command was:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-audit-kompiled
```

It exited 0; see
`/audit-output/evidence/stage3-kompile-llvm.log`. Fresh execution of the exact
submitted `solution.mpy` exited 0 with `.K`, clean return/exception/stack cells,
and a `unique_digits` closure whose body is the submitted body; see
`/audit-output/evidence/stage3-krun-solution.log`.

### Proof definition and claims

The fresh Haskell build command was:

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION-SYNTAX \
  --output-definition verification-audit-kompiled
```

It exited 0; see
`/audit-output/evidence/stage3-kompile-haskell.log`.

The target claims were exercised with their necessary circularity
dependencies:

| Target | Claim set supplied to `kprove` | Result |
|---|---|---|
| Inner decimal loop | `SPEC.digit-loop` | `#Top`, exit 0 |
| Outer list loop | `SPEC.digit-loop,SPEC.outer-loop` | `#Top`, exit 0 |
| Whole-program entry | complete `SPEC` module (all three claims) | `#Top`, exit 0 |

The bounded command/output logs are
`stage3-kprove-digit-loop.log`,
`stage3-kprove-loop-closure.log`, and
`stage3-kprove-all.log` under `/audit-output/evidence`.

As a dependency diagnostic, selecting only `SPEC.outer-loop` excluded the
inner circularity and got meaningfully stuck at the real symbolic inner
`while`; see `stage3-kprove-outer-loop.log` (exit 1). This is not a failure of
the submitted complete proof: the inner claim is an explicit, independently
proved dependency, and the dependency-closed and complete proof commands both
close. It is evidence that the inner claim is genuinely exercised.

The positive compiler diagnostics are limited to unused variables and
pre-existing supplied-semantics coverage warnings; there is no positive-run
parse, backend, stuck-claim, or nonzero-exit failure.

## 4. Adequacy and real-program pinning

### Plain-language claims

`digit-loop` has K-sorted integer `N` and `B` in a real function scope. It
executes the exact submitted `while number > 0` body. At loop exit it requires
`number` to be unchanged when initially nonpositive and otherwise zero
(`scanNumber`), and requires `bad` to equal its initial value plus the count
computed by `scanBad`. Other cells are framed. A satisfying state is, for
example, `L = 1`, `N = 2`, `B = 0` with ordinary values for `x`, `result`, and
`value`.

`outer-loop` starts at the real internal `#loop` produced by the submitted
`for value in x`. Its precondition is `integerVals(XS)`: every item in the
remaining finite suffix is a K integer. It requires the loop to consume all of
`XS`, update the result heap object to `collect(ACC, XS)`, and leave
`value`, `number`, and `bad` with the values produced by the last iteration
(or preserve their incoming values for the empty suffix). It pins the live
scope, heap, frame, return, exception, and exit cells. `XS = .ValSeq` and
`XS = vCons(1, .ValSeq)` are satisfying witnesses. `ALL` need not be related
to `XS` in this helper theorem because the already-materialized loop never
reads `x`; in the real entry execution, fixed semantics initializes the loop
with the actual full input.

`program` starts from a clean module scope, executes the exact `FuncDef`, looks
up and calls that binding on `list(XS)`, and requires `integerVals(XS)`. At
termination it requires:

- `<k>` to contain exactly `ref(1)`;
- module binding `unique_digits` to contain the same closure body;
- heap location 0 to contain the retained sequence
  `collect(.ValSeq, XS)`;
- heap location 1 to contain
  `sortVS(collect(.ValSeq, XS))`;
- allocation to have advanced from 0 to 2; and
- clean stack, return, exception, and exit cells.

The precondition accepts every finite list of positive integers and is in fact
broader, accepting zero and negative K integers as well. It is therefore not a
finite bound, example-only theorem, or material domain narrowing. The supplied
semantics explicitly permits an unboxed `list(VS)` as a read-only claim input
(`semantics/core.k:66-67`). The function does not mutate or observe identity of
`x`, so this boundary preserves every behavior material to the contract.

### Mechanical constructor identity

`/audit-output/evidence/program_pinning.py` independently extracts the sole
`FuncDef` from regenerated `solution.mpy` and the executed `FuncDef` from the
entry claim. K parses and macro-expands the surface and claim forms
independently. Their canonical KAST byte strings are equal and have the same
digest:

```text
17ce9de074e13261ddfbf90330f8990475677e21c2f1d7f0fd39d34b3c681b35
```

The same script compares the exact submitted `while` condition/body with
`digit-loop`, and the exact `for` target/body with `outer-loop`; both
constructor comparisons are equal. See
`/audit-output/evidence/stage4-program-pinning.log`.

This demonstrates only semantically inert surface normalization such as
explicit `.Exprs` list tails. It is not a textual resemblance argument and
does not rely on automatic source-to-spec regeneration.

### Concrete satisfying substitutions

`/audit-output/evidence/witness_program.py` contains an AST-identical copy of
the submitted function followed by calls on empty, keep, drop, both prompt
examples, and duplicate/sort inputs. The AST identity check is in
`stage4-witness-body.log`. The trusted translator produced the executed MPY
program. Fresh LLVM execution and validation both exit 0
(`stage4-witness-krun.log` and `stage4-witness-validation.log`), with results:

- `[] -> []`;
- `[1] -> [1]`;
- `[2] -> []`;
- `[15, 33, 1422, 1] -> [1, 15, 33]`;
- `[152, 323, 1422, 10] -> []`; and
- `[97531, 1, 33, 1, 15] -> [1, 1, 15, 33, 97531]`.

These are the same results obtained from both Python implementations in stage
2 and are concrete satisfying substitutions into the quantified claim.

### Body sensitivity

A fresh reviewer mutation changed the digit test from `% 2` to `% 7` in the
actually executed claim terms while leaving the parity summary unchanged. The
mutated spec is `/audit-output/evidence/spec-audit-body.k`. It dry-runs
successfully, then `digit-loop` exits 1 with `WarnStuckClaimState`; the residual
explicitly contrasts `%Int 2` with `%Int 7`. See
`stage4-body-mutation-dry-run.log` and
`stage4-body-mutation-kprove.log`. Thus a material change to the executed body,
not merely to an external source file, invalidates the connection.

## 5. Rule-by-rule static soundness review

The exhaustive machine-generated location inventory is
`/audit-output/evidence/stage5-rule-inventory.log`. There is no candidate
`semantic.k` and no generated semantics helper: this is supplied-semantics
mode. The candidate-local theory is exactly `verification.k`; the used portion
of the fixed supplied semantics is mapped separately below.

### Candidate-local declarations and all fifteen equations

There are eight local function symbols, no `functional` declaration, no local
opaque/no-evaluator symbol, no local priority, `owise`, `concrete`, or
simplification rule, and no rule that mentions an operational cell.

| Symbol and attributes | Complete rule inventory | Soundness finding |
|---|---|---|
| `integerVals(ValSeq) : Bool` `[function,total]` | Empty is true; a cons is `isInt(head) andBool integerVals(tail)` (lines 25-27). | The two ValSeq constructors are disjoint and exhaustive; recursion structurally descends. It exactly states the formal input domain. |
| `scanBad(Int,Int) : Int` `[function,total]` | Return `B` for `N <= 0`; for `N > 0`, add one iff `pyMod(N,2)=0` and recurse on decimal floor division (lines 30-36). | Guards are disjoint and exhaustive. For positive `N`, the next argument is `N // 10 < N`; each step tests the parity of the current last decimal digit. Nonpositive values correctly skip the source loop. |
| `scanNumber(Int) : Int` `[function,total]` | One unconditional conditional expression: positive input maps to zero, nonpositive input to itself (lines 38-39). | Exactly the final value of repeated positive decimal floor division; exhaustive. |
| `appendCandidate(ValSeq,Val) : ValSeq` `[function]` | Append an integer iff `scanBad(0,intOf(V))=0`; otherwise retain the sequence (lines 41-47). | The equality/disequality guards are disjoint and exhaustive for admitted integer `V`. It preserves order and duplicates and does not execute or replace a program term. |
| `collect(ValSeq,ValSeq) : ValSeq` `[function]` | Empty input returns the accumulator; integer head folds through `appendCandidate` and recurses on the tail (lines 50-53). | Structural descent. It is intentionally partial outside integer lists and every proof use is protected by `integerVals`. This is a definitional summary, not an operational oracle. |
| `afterValue(ValSeq,Val) : Val` `[function,total]` | Empty suffix preserves the incoming value; cons recursively retains the last head (lines 56-58). | Disjoint/exhaustive structural recursion, matching persistent Python loop-target state. |
| `afterNumber(ValSeq,Int) : Int` `[function]` | Empty suffix preserves the incoming number; integer cons recurses with `scanNumber(intOf(V))` (lines 60-63). | Structural descent and exact per-iteration final local value; partial only outside the guarded integer domain. |
| `afterBad(ValSeq,Int) : Int` `[function]` | Empty suffix preserves incoming bad; integer cons recurses with `scanBad(0,intOf(V))` (lines 65-68). | Structural descent and exact per-iteration final local value; partial only outside the guarded integer domain. |

For positive integers, ordinary positional decimal arithmetic proves:
`scanBad(0,n)=0` iff every decimal digit of `n` is odd. The recurrence examines
the last digit because integer parity equals last-digit parity, then removes
that digit with positive floor division by ten. Consequently `collect`
retains exactly the HumanEval elements, in original order and with
multiplicity. This conclusion follows from the equations and ordinary
arithmetic; it is not injected by an operational rewrite. Stage 2 supplies
broad finite corroboration but is not used as the universal proof.

No local equation has a false-conclusion witness on its declared/guarded
domain, so no rule is classified as unsound. The benchmark requirement to
provide a false witness for every claimed unsound rule is therefore
inapplicable rather than evaded.

### All three claims

The three claims are the exact inner-loop invariant, outer-loop invariant, and
entry reachability claim described in stage 4. They are circularities checked
by `kprove`, not unconditional semantic rewrites. The isolated-outer residual
and `% 7` mutation show the loop claims are reached and constrain the real
operations.

### Used fixed-semantics mapping

Every construct in `solution.mpy` has a declaration in
`semantics/syntax.k` and a material execution route in the supplied semantics:

| Program construct | Fixed route and state/control effect |
|---|---|
| `Module`, statement sequence, `FuncDef` | `core.k:124-127` loads/sequences; `functions.k:14-16` binds the exact closure in the current scope. |
| `Name`, calls, parameters, return | `core.k:129-181` performs scope-chain lookup including real builtins; `core.k:183-191` evaluates arguments left-to-right; `call.k:18-32,69-74` evaluates the selected binding, allocates a call frame, and enters the body; `functions.k:62-90` binds parameters, records return, pops the frame, restores control, and preserves escaping heap allocations. |
| `Assign`, `AugAssign` | Strict RHS declarations in `syntax.k:41,44`; `controls.k:8-31` writes the live local scope. Integer `+`, `%`, and `//` dispatch through `operators.k:10-17` and `int.k:9-20`; the guards and operand sorts used here are disjoint. |
| `ListExpr`, `append` | `list.k:12-20` evaluates elements and allocates a fresh list; `list.k:52-55` mutates exactly the referenced result list by concatenating the new element. Allocation uses `core.k:117-121` and advances `heapLoc`. |
| Singleton `TupleExpr` and `sum` | `tuple.k:9-16` evaluates the singleton once and constructs the tuple value; `call.k:26` selects the builtin `sum` binding; `builtins.k:46-56` iterates it and returns `intOf(V)=V` for admitted integers. |
| `Compare` and integer conditions | `operators.k:14-17` enforces left-to-right operand evaluation; `int.k:22-27` gives `>`, `==`; `core.k:198-205` gives integer/boolean truth. |
| `For` | `controls.k:62-74` evaluates the iterable once and drives `#loop`; `list.k:8-10` yields the exact head/tail; `tuple.k:30-41` updates the loop target. The higher-priority ref dereference in `controls.k:104-108` agrees with the unboxed read-only entry representation. |
| `While`, `If`, expression statement | `controls.k:46-54,76-82` evaluates guards, chooses disjoint truth branches, and re-enters the exact loop; the expression statement discards only the `append` return after its heap effect. |
| `sorted(result)` | `call.k:34-45` dereferences the list argument; `sort.k:34-37` allocates a new list containing `sortVS(VS)`. |

The entry claim constrains every material cell touched by those routes:
continuation, environment/scopes, heap and allocation counter, stack/frame,
return state, exception state, and exit code. The loop claims frame omitted
cells and explicitly constrain the local or heap state changed by their
regions. Evaluation order, binding, allocation, mutation, and return control
are therefore not bypassed.

### Supplied `sortVS` boundary

`sortVS` is declared in the trusted supplied semantics at `sort.k:18` as
`[function,total,symbol(sortVS),no-evaluators]`. Symbolic proof deliberately
leaves it opaque. The same fixed file gives concrete insertion-sort rules for
integer sequences at lines 20-24 and routes the external builtin `sorted` to a
fresh allocation containing `sortVS` at lines 34-37.

This is an acceptable low-level supplied-semantics trust boundary, not a
candidate-local correctness shortcut:

- `sorted` is an external builtin, not program-defined code.
- The operational rule is part of the integrity-checked fixed semantics, not
  `verification.k`.
- The K theorem remains interpretation-parametric by stating the result
  explicitly as `sortVS(collect(...))`; it does not derive an ordering fact
  from an unconstrained candidate oracle.
- The HumanEval reading of that term is conditional on the supplied primitive's
  named ascending-sort contract. Fresh LLVM insertion-sort witnesses and the
  22,543 Python differentials support the bridge on tested inputs but are not
  presented as its universal proof.

No proof-local value is both introduced by an operational bridge and reused in
the postcondition. There is therefore no circular result-bearing abstraction.

## 6. Fresh non-vacuity test

The reviewer-authored mutation is
`/audit-output/evidence/spec-audit-false.k`. It changes only the entry
postcondition for returned heap location 1 from:

```text
list(sortVS(collect(.ValSeq, XS)))
```

to:

```text
list(vCons(0, sortVS(collect(.ValSeq, XS))))
```

This is false for the satisfying input `XS = .ValSeq`: the original entry
precondition reduces to true and the actual execution returns the empty list,
as the fresh LLVM witness also shows.

The dry-run command parsed and built the mutated target, exiting 0
(`stage6-false-dry-run.log`). The actual proof command was:

```text
kprove spec-audit-false.k \
  --definition verification-audit-kompiled \
  --spec-module SPEC-AUDIT-FALSE
```

It exited 1 with `WarnStuckClaimState`, not a parser error, timeout, or unrelated
crash. The residual reaches the genuine final `ref(1)` configuration and
records the exact failed implication:

```text
sortVS(collect(.ValSeq, XS))
  = vCons(0, sortVS(collect(.ValSeq, XS)))
```

See `/audit-output/evidence/stage6-false-kprove.log`. The proof is therefore
non-vacuous and result-constraining.

## 7. Proven versus assumed accounting

### What the reachability proof establishes

Under the supplied MPY semantics, for every finite `ValSeq` whose elements are
K integers, if execution of the exact submitted `unique_digits` definition and
call terminates, it returns a fresh reference to
`list(sortVS(collect(.ValSeq, XS)))`. The retained pre-sort heap object contains
exactly `collect(.ValSeq, XS)`. Function binding, both loops, integer
operations, `sum`, append mutation, `sorted` allocation, frames, local state,
return, exceptions, and allocation state all execute under fixed semantics.

For the required positive-integer subset, the audited summary equations and
ordinary decimal arithmetic identify `collect` with filtering for all-odd
decimal digits while preserving duplicates. Under the supplied contract for
`sortVS`, the returned sequence is that multiset in increasing order. This is
the requested partial-correctness property.

### Assumptions and trust ledger

| Boundary | Influence | Assessment |
|---|---|---|
| Integrity-checked supplied MPY semantics and K 7.1.293 Haskell prover/backend | All modeled values, evaluation, control, state, and proof search | Required benchmark foundation; acceptable. It was rebuilt from trusted source, not candidate binaries. |
| K mathematical integer, Boolean, collection, equality, and SMT hooks | Arithmetic recurrences, guards, map/list state, implication checks | Ordinary K/backend trust; acceptable. Denominators used by the program are nonzero constants 2, 7 only in the rejected probe, and 10. |
| Trusted translator | Source-to-MPY bridge | Acceptable and directly checked: trusted regeneration is byte-identical to submitted `solution.mpy`. |
| Supplied external primitive `sortVS` | Final ordering/permutation | Acceptable fixed-semantics boundary described above. The formal K result names it; finite concrete/differential evidence supports but does not prove its external contract. |
| Decimal recurrence meaning | Connects `scanBad`/`collect` to “has no even decimal digit” | Established by direct arithmetic review of exhaustive equations; independently corroborated on 22,543 cases. It is not an operational assumption used to close `kprove`. |
| Unboxed read-only input list | Entry representation of caller-provided `x` | Explicitly supported by supplied semantics and observationally adequate because this function neither mutates nor identity-tests `x`. |
| Partial-correctness termination condition | Whether a final state is reached | The theorem is conditional on termination, as requested. Positive inputs make both finite loops decrease, and concrete tests terminate, but no separate K liveness theorem is claimed. |

Excluded behavior is non-integer input, exceptions outside the supplied subset,
and the canonical interpretation of zero/negative integers, all outside the
HumanEval positive-integer contract. No bound on list length, integer size, or
number of loop iterations is added by the theorem.

### Gate and benchmark decision

- Gate A (real-program soundness): PASS. Clean `#Top`, exact constructor
  pinning, no proof-local operational bridge, body sensitivity, satisfying
  preconditions, and meaningful false-postcondition rejection all hold.
- Gate B (intent adequacy): PASS. The formal domain includes the complete
  positive-integer source domain, and the postcondition has the required
  filtering, multiplicity, and supplied ascending-sort meaning.
- Gate C (trust/evidence auditability): PASS. Every boundary is named and every
  dynamic claim cited above has a preserved script, exact command, status, and
  bounded output.

The candidate contains a legitimate, unrestricted partial-correctness proof of
the real generated program. The fixed `sortVS` primitive is part of the
integrity-checked supplied semantics and is used transparently, so it is not a
material adequacy gap or a proof-local smuggled conclusion.

VERDICT: PASS
LEGITIMACY: LEGIT
