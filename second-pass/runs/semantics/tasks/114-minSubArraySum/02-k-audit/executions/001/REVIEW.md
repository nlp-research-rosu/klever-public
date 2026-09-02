# Independent adversarial audit: 114-minSubArraySum

## Executive decision

The candidate contains a legitimate, freshly reconstructed partial-correctness
proof of the exact translated function for every nonempty finite list of
mathematical integers. The proof is result-constraining and body-sensitive. All
three positive claims independently close with exit status 0 and `#Top`, while a
fresh off-by-one postcondition builds successfully and fails on the expected
unmet equality.

The decision is `CONCERNS / LEGIT`, rather than `PASS / LEGIT`, for three
documented limitations:

1. `minSubArraySumSpec` is a Kadane recurrence. Its equivalence to “the minimum
   sum of any contiguous nonempty subarray” is supported by a sound informal
   induction and extensive independent differential evidence, but it is not a
   separate K theorem.
2. The two proof-local priority iterator rules for the fresh `intVals` symbolic
   embedding are transparent and structurally correct, but a reviewer-authored
   bridge-free contextual connection claim gets stuck. Thus their contextual
   connection is an audited informal proof-extension argument, not an
   independently closed K theorem.
3. All requested generation/provenance records are absent, limiting historical
   auditability. This does not affect fresh source reconstruction.

I found no rule that enables a concrete or symbolic false conclusion on the
intended domain. In particular, I do not relabel the bridge evidence gap as
unsoundness without the required false-conclusion witness.

Audit scratch root: `/tmp/audit-work/review-114.pELioR`. Candidate-provided
compiled definitions and caches were not used. Reviewer evidence is under
`/audit-output/evidence/`.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `SUPPLIED_SEMANTICS`, and
`/reference/reference-semantics` is present as a real directory. There is no
mode/mount contradiction, so this is a candidate audit rather than an
infrastructure error.

I recursively compared `/candidate/reference-semantics` with the trusted tree
using:

```text
diff --no-dereference --recursive --brief \
  /reference/reference-semantics /candidate/reference-semantics
```

It exited 0 with no differences. The candidate tree has no symlinks. There are
no missing, added, mistyped, or changed entries in the supplied-semantics tree.
See `evidence/02_semantics_tree_diff.log` and
`evidence/06_symlink_check.log`.

The prompt and translator are byte-identical to the trusted mounts:

- `/candidate/prompt.py` equals `/reference/prompt.py`;
- `/candidate/py2mpy.py` equals `/reference/py2mpy.py`.

Both `cmp -l` commands exited 0 with no output. Hashes and commands are in
`evidence/03_prompt_cmp.log`, `evidence/04_translator_cmp.log`, and
`evidence/05_integrity_hashes.log`.

### Candidate inventory and missing records

`evidence/01_candidate_inventory.log` records every candidate entry, type,
mode, size, and symlink target. The only cache is
`/candidate/__pycache__/solution.cpython-310.pyc`; it was ignored.

The following requested provenance artifacts are missing:

- `/candidate/run-input.json`;
- `/candidate/metrics.json`;
- `/candidate/codex-last.txt`;
- `/candidate/codex-output.log`.

No structured trace (`*trace*` or `*.jsonl`) is present. See
`evidence/07_provenance_presence.log`. Consequently, there were no provenance
claims to trust or rebut. The omission is an auditability concern, not a
substitute for fresh verification and not an infrastructure failure.

The candidate has no `PROOF.md`, `spec-vacuity.k`, or candidate-built
`*-kompiled` directory. No prior `#Top` or final report was available or
accepted.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

From trusted `/reference/prompt.py` and `/reference/canonical.py`, the function
takes a nonempty array/list of integers and returns the minimum sum among its
contiguous nonempty subarrays. The two documented examples are:

```text
[2, 3, 4, 1, 2, 4] -> 1
[-1, -2, -3]        -> -6
```

The empty-list case is outside that contract: there is no nonempty subarray,
and the trusted canonical implementation itself calls `max` on an empty
sequence.

### Submitted implementation

`/candidate/solution.py` is the standard minimum-ending-here recurrence:

- `smallest` starts at the first list element;
- for each value, `current` becomes `min(value, current + value)`;
- `smallest` becomes `min(current, smallest)`;
- `smallest` is returned.

This is a different algorithm from the trusted canonical implementation but is
extensionally correct over nonempty integer lists.

Trusted regeneration used:

```text
python3 /tmp/audit-work/review-114.pELioR/trusted/py2mpy.py \
  /tmp/audit-work/review-114.pELioR/candidate-src/solution.py \
  > /tmp/audit-work/review-114.pELioR/regenerated-solution.mpy
cmp -l \
  /tmp/audit-work/review-114.pELioR/candidate-src/solution.mpy \
  /tmp/audit-work/review-114.pELioR/regenerated-solution.mpy
```

The command exited 0. Both files have SHA-256
`f1476cc2c62686c10e41dbc7811275b5f0340b82321e7d5188a356b1d8b8838d`.
See `evidence/09_solution_translation_identity.log`.

### Independent differential test

`evidence/differential_test.py` independently imports:

- the trusted entry point from `/reference/canonical.py`;
- the generated entry point from the scratch copy of `solution.py`;
- a third, independently written brute-force oracle that enumerates every
  contiguous nonempty slice.

Its exact expanded inputs are preserved in
`evidence/differential-inputs.json`. The scope was:

- 13 documented and hand-selected boundary cases, including singleton, zero,
  equality boundaries, all-positive, all-negative, mixed-sign, and arbitrary
  precision integers;
- every list of lengths 1 through 5 over `[-3, -2, -1, 0, 1, 2, 3]`
  (19,607 cases);
- 500 deterministic pseudorandom lists, seed 114, lengths 1 through 30,
  elements from -1000 through 1000.

Command and result:

```text
python3 /audit-output/evidence/differential_test.py
nonempty_cases=20120
mismatches=0
branch_pairs=[(False, False), (False, True), (True, False), (True, True)]
all_branch_pairs_seen=True
exit_status: 0
```

See `evidence/10_differential_test.log`. Both source `if` decisions exercised
true, false, and equality boundaries. On the deliberately tested empty input,
the canonical raises `ValueError` and the candidate raises `IndexError`; this
is a real behavioral difference outside the stated/formal nonempty domain, not
a result divergence on that domain.

## 3. Clean proof reconstruction

K was independently available at `/usr/bin/{kompile,kprove,krun}`, version
7.1.337 (`evidence/00_toolchain.log`). Sources were copied into a fresh scratch
tree; trusted supplied semantics, rather than candidate caches, were used.
`evidence/08_scratch_copy.log` records the copy.

### Concrete definition

The concrete harness was also regenerated with the trusted translator and is
byte-identical to the submitted `concrete-tests.mpy`
(`evidence/11_concrete_translation_identity.log`). I built the LLVM definition:

```text
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

This exited 0 (`evidence/12_kompile_runtime.log`). The compiler reported
nonexhaustive fixed-semantics functions for several unused domains and for
out-of-bounds/opaque `valSeqAt`; none is reached outside its covered,
in-bounds case by this program.

Concrete execution:

```text
krun /tmp/audit-work/review-114.pELioR/regenerated-concrete-tests.mpy \
  --definition runtime-kompiled --output pretty
```

It exited 0 with `<k> .K </k>`, `<exc> NoExc </exc>`, and
`<exit-code> 0 </exit-code>`. See `evidence/13_krun_concrete_tests.log`.

### Proof definitions and every positive target

The base Haskell definition was freshly built:

```text
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION-BASE \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-base-kompiled
```

Build exit: 0 (`evidence/14_kompile_verification_base.log`).

Both claims that must be established before adding the loop summary were run
independently:

```text
kprove spec.k --definition verification-base-kompiled \
  --spec-module LOOP-SPEC --output pretty
#Top
exit_status: 0

kprove spec.k --definition verification-base-kompiled \
  --spec-module LOAD-SPEC --output pretty
#Top
exit_status: 0
```

See `evidence/15_kprove_loop_spec.log` and
`evidence/16_kprove_load_spec.log`.

The full definition was then freshly built:

```text
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

Build exit: 0 (`evidence/17_kompile_verification.log`).

The whole-function target:

```text
kprove spec.k --definition verification-kompiled \
  --spec-module FUNCTION-SPEC --output pretty
#Top
exit_status: 0
```

See `evidence/18_kprove_function_spec.log`. These three are all positive claims
in `/candidate/spec.k`; none was omitted or filtered.

## 4. Adequacy and real-program pinning

### Plain-language reading of each entry claim

**`LOOP-SPEC`.** There is no separate `requires` clause. Its structural
precondition is a nonempty symbolic integer suffix
`iCons(I,R)`, an active loop over exactly `kadaneBody`, an active scope at
location `L` with exactly `nums`, `smallest`, `current`, and `value`, and parent
scope 0. It proves that the fixed loop consumes the whole suffix, leaves `nums`
unchanged, makes `current` the `kadaneCurrent` fold, makes `smallest` the
`kadaneSmallest` fold, and leaves `value` equal to the last iterated element.
The framed continuation and all omitted cells are preserved.

**`LOAD-SPEC`.** From the exact initial module configuration, loading
`Module(minSubArraySumDef .Stmts)` consumes the module and installs exactly
`minSubArraySumClosure` at global name `"minSubArraySum"`, with every other
configuration cell unchanged.

**`FUNCTION-SPEC`.** For arbitrary `H:Int` and `T:IntSeq`, hence every
nonempty finite integer sequence, directly applying the exact closure to the
read-only list embedding returns
`minSubArraySumSpec(iCons(H,T))`. It requires the standard empty caller scope,
builtins scope, empty heap and stack, no pending return or exception, and exit
code 0. The destination pins the result in `<k>` and pins all cells to their
initial values; it is neither a free RHS variable, a tautology, nor a one-way
postcondition.

### Exact program connection

The macro expansions in `/candidate/verification.k` were compared term by term
with trusted-regenerated `solution.mpy`:

- `kadaneBody` is exactly the translated `For` body;
- `minSubArraySumBody` is exactly the function body, including the docstring,
  three initial assignments, loop, and return;
- `minSubArraySumDef` is the exact translated `FuncDef`;
- `minSubArraySumClosure` is exactly the closure installed by fixed
  `FuncDef` semantics at defining environment 0.

`LOAD-SPEC` machine-checks the translated-definition-to-closure link without
the loop summary. `FUNCTION-SPEC` executes that same closure. Therefore this is
not a substituted algorithm or an answer-returning oracle.

The universal claim uses the supplied semantics' supported unboxed,
read-only-list representation. Real translated calls with `ListExpr` first
allocate a heap `ref`; the program only reads the list, and fixed `Subscript`
and `For` rules dereference that `ref`. The concrete translated harness tests
this actual allocation/call path. There is no single universal K claim that
composes module load, name lookup, heap-ref input construction, and invocation;
that is an evidence limitation, but the exact loader theorem, exact closure
theorem, read-only body, and concrete K runs pin the real function rather than
a replacement.

### Satisfying states and concrete substitutions

`evidence/adequacy_witness.py` and
`evidence/adequacy-witness.json` exhibit a satisfying state for every entry:

- loop witness: `L=1`, `I=-2`, `R=[3,-5]`, `C=4`, `B=-1`,
  `INPUT=[99]`, `OLD=123`; the claimed final local values are
  `smallest=-5`, `current=-5`, `value=-5`;
- load witness: exactly the concrete initial configuration in `LOAD-SPEC`;
- function witness: `H=3`,
  `T=[-4,2,-3,-1,7,-5]`, with all specified cells in their initial form.

For the function witness, the formal recurrence, trusted canonical, and
submitted Python implementation all return `-6`. The same three-way agreement
holds for `[5] -> 5` and `[-1,-2,-3] -> -6`. The witness script exits 0; see
`evidence/22_adequacy_witness.log`.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/k_inventory.py` generated
`evidence/k-inventory.json`, which records full text, source, line range,
declaration kind, and attributes for every declaration in all 24 supplied K
files plus `verification.k` and `spec.k`. Summary:

```text
records=1138
syntax declarations=238
rules=715
claims=3
contexts=5
configurations=1
priority-attributed rules/declarations=55
simplification rules=1
total declarations=116
functional declarations=0
```

The per-file counts are in `evidence/k-inventory-summary.txt`, and the command
exited 0 in `evidence/21_k_inventory_run.log`. There are no generated-semantics
helper files in this `SUPPLIED_SEMANTICS` candidate. The supplied tree is the
trusted, integrity-checked fixed semantics; its complete inventory remains
visible rather than being silently replaced by a hand-selected subset.

`evidence/construct-map.md` maps every submitted syntactic constructor to its
declaration and applicable rules. The reachable chain is:

1. fixed module sequencing and `FuncDef` install the closure;
2. call rules allocate and bind a plain local frame;
3. strictness evaluates RHS operands and conditions left-to-right;
4. `Subscript` performs the proven in-bounds index-0 access;
5. `For`, list iteration, and target binding run the exact loop body;
6. integer `+` and `<` use mathematical K integers;
7. `Return` unwinds exactly the function frame and restores every pinned cell.

Unused supplied domains (float, dict, set, sort, methods, comprehensions,
builtins not called by this function) cannot contribute a rewrite because
their symbols never occur on this execution path. Fixed-semantics totality
warnings are therefore not used to fabricate this result. The applicable
`valSeqAt` call is provably index 0 of a nonempty sequence.

### Every proof-local declaration and rule

The proof-local inventory has no opaque or externally uninterpreted
result-bearing symbol.

| Extension | Class and static decision |
|---|---|
| `intVals(.IntSeq) => .ValSeq` | Definitional embedding base case; exact and terminating. |
| `intVals(iCons(I,R)) => vCons(I,intVals(R))` | Definitional embedding step; exact, structurally decreasing, and covers the other `IntSeq` constructor. |
| Empty `#iterNext(list(intVals(.IntSeq)))` priority rule | Operational symbolic bridge; result is the exact empty-list iterator result, no state or continuation change. |
| Nonempty `#iterNext(list(intVals(iCons(I,R))))` priority rule | Operational symbolic bridge; yields exactly `I` and preserves exactly the embedded tail and arbitrary continuation. No allocation, scope, control, or exception effect. |
| `valSeqAt(intVals(iCons(I,R)),0) => I [simplification]` | Exact head equation on its complete domain; it cannot match empty/OOB use. |
| Two `chooseSmaller` equations | Definitional minimum: guards `A < B` and `A >= B` are disjoint and exhaustive over K `Int`; RHSs agree with ordinary integer order. |
| `nextCurrent(I,C)` | Total one-step recurrence `min(I,C+I)`; all inputs covered. |
| Two `kadaneCurrent` equations | Base/constructor guards are disjoint and exhaustive; recursion strictly decreases the sequence. |
| Two `kadaneSmallest` equations | Base/constructor guards are disjoint and exhaustive; recursive arguments implement the exact loop assignments and structurally decrease. |
| `minSubArraySumSpec(iCons(H,T))` | Deliberately non-total and restricted to the formal nonempty domain; seeds both folds with `H`. |
| Two `lastFrom` equations | Disjoint/exhaustive structural fold; yields the actual last iterated value and terminates. |
| `kadaneBody` macro rule | Compile-time exact expansion of the submitted loop body; it does not replace execution. |
| `minSubArraySumBody` macro rule | Compile-time exact expansion of the submitted function body. |
| `minSubArraySumDef` macro rule | Compile-time exact expansion of the submitted translated definition. |
| `minSubArraySumClosure` macro rule | Compile-time exact closure matching fixed `FuncDef` installation at environment 0. |
| Final priority loop-summary rule | Operational bridge with the same complete match, destination, arbitrary continuation frame, scope footprint, and omitted-cell framing as `LOOP-SPEC`; the bridge-free universal claim closes with `#Top`. |

The total helpers have complete constructor/guard coverage and no overlapping
disagreeing equations. All recursion descends on `IntSeq`. Priorities select
exact specialized cases rather than changing a result. The loop summary reads
and writes only the four exact local bindings; the body does not allocate,
mutate the heap, call another function, return, break, continue, or raise an
exception. Its arbitrary `<k>` suffix is justified because `LOOP-SPEC` has the
identical suffix frame. The summary's `parent(0)` matches the fixed call rule,
and the exact local map matches the real four locals at loop entry.

The relationship between the whole-loop summary and fixed execution is
machine-checked: `LOOP-SPEC` closes against `VERIFICATION-BASE`, which does not
contain the summary rule. It is then imported as the rule used by
`FUNCTION-SPEC`; this is a legitimate verified summary rather than circular use
of the same rule.

### Iterator-bridge evidence gap, narrowly stated

I constructed `evidence/bridge-connection.k`, a bridge-free definition that
keeps only the fresh structural embedding and imports fixed `MPY`. Its build
exited 0 (`evidence/19_kompile_bridge_base.log`). A universal contextual claim
for `#iterNext(list(intValsAudit(...)))` then got stuck because the fixed
evaluator does not reduce the fresh embedding underneath `#iterNext`
(`evidence/20_kprove_bridge_connections.log`).

This means the candidate lacks the strongest machine-checked contextual
connection theorem for its two iterator accelerations. It does not supply a
false conclusion witness: the equations transparently map empty to empty and
`iCons(I,R)` to head `I` plus tail `R`, exactly matching fixed list iteration.
The bridge preserves the arbitrary continuation and has no state footprint.
Accordingly this audit records an evidence gap and conditional trust boundary,
not an unsound rule.

Two attempted “wrong value” reachability diagnostics are preserved in
`evidence/25_kprove_iterator_wrong.log` and
`evidence/26_kprove_subscript_wrong.log`. They explored unrelated narrowing
branches and hit a missing Haskell float hook, so they are not valid rejection
evidence and are not used for the verdict.

### Body sensitivity

`evidence/body-sensitivity.k` changes one real source operation:
`smallest = nums[0]` becomes `smallest = 0`, while retaining the original loop.
The mutated definition builds successfully
(`evidence/23_kompile_body_mutation.log`). On satisfying input `[5]`, the
original-result claim requires 5 but fixed execution reaches 0. `kprove` exits
1 with `WarnStuckClaimState` and residual `<k> 0 </k>`, not a parser or backend
error (`evidence/24_kprove_body_mutation.log`). Thus the proof is sensitive to
the actual program body.

### Mathematical intent bridge

The informal invariant is correct:

- after a nonempty processed prefix, `current` is the minimum sum of a
  nonempty suffix ending at the last processed element;
- `smallest` is the minimum sum of any contiguous nonempty subarray in the
  processed prefix;
- for next element `I`, every ending subarray is either `[I]` or a previous
  ending subarray extended by `I`, hence
  `current' = min(I,current+I)` and
  `smallest' = min(smallest,current')`.

Base case `H` and the inductive step establish the natural result for every
finite nonempty sequence. This argument is ordinary mathematics and supported
by the independent brute-force differential run, but no K claim defines
subarrays and proves this equivalence. That limitation is the main reason for
`CONCERNS`.

## 6. Fresh non-vacuity test

The candidate supplied no vacuity file. I created
`evidence/spec-vacuity-audit.k`, changing the result-constraining destination
from:

```text
minSubArraySumSpec(iCons(H,T))
```

to the demonstrably false:

```text
minSubArraySumSpec(iCons(H,T)) +Int 1
```

The same satisfiable precondition is retained. `[5]` is a concrete witness:
the real/formal result is 5, while the mutation requires 6.

First, the mutation parsed and compiled to KORE:

```text
kprove /audit-output/evidence/spec-vacuity-audit.k \
  -I /tmp/audit-work/review-114.pELioR/candidate-src \
  --definition verification-kompiled \
  --spec-module FUNCTION-VACUITY-SPEC \
  --dry-run
exit_status: 0
```

See `evidence/27_vacuity_dry_run.log`.

Then the actual proof:

```text
kprove /audit-output/evidence/spec-vacuity-audit.k \
  -I /tmp/audit-work/review-114.pELioR/candidate-src \
  --definition verification-kompiled \
  --spec-module FUNCTION-VACUITY-SPEC \
  --output pretty
exit_status: 1
```

The residual is the expected implication failure:

```text
WarnStuckClaimState
kadaneSmallest(T,H,H) +Int 1
#Equals
kadaneSmallest(T,H,H)
```

See `evidence/28_kprove_vacuity_mutation.log`. This is meaningful non-vacuity
evidence: the mutated obligation was reachable and rejected on its result
constraint.

## 7. Proven versus assumed accounting

### Precisely proven

Under the integrity-checked supplied MPY semantics plus the audited
proof-local definitions:

1. Loading the exact trusted-regenerated `solution.mpy` function definition
   installs the exact closure used by the function theorem.
2. For arbitrary mathematical integers `H` and finite `T:IntSeq`, applying
   that closure to the nonempty read-only list `[H] + T` terminates in
   `minSubArraySumSpec(iCons(H,T))`.
3. The caller environment, global/builtins scopes, heap, allocation counter,
   stack, return state, exception state, and exit code are restored/preserved
   exactly as stated.
4. The real loop transforms `current`, `smallest`, and `value` according to the
   three total structural folds. The loop theorem is proved without assuming
   its compiled summary rule.

This is a universal reachability result over the formal nonempty integer-list
domain, not a finite test claim.

### Trust ledger

| Boundary | Dependents and assessment |
|---|---|
| Trusted supplied semantics tree | All K execution. Integrity is exact. Relevant rules were mapped and audited; unused fixed domains do not appear on the path. Acceptable selected-semantics trust boundary. |
| K 7.1.337 frontend, LLVM backend, Haskell backend, SMT/builtin evaluators | All builds/runs/proofs. Standard tool trust; exact versions and outputs are recorded. |
| K mathematical `Int`, Boolean order, `Map`, `List`, equality, and generated strictness rules | Arithmetic, comparisons, scopes, frames, evaluation order. Acceptable low-level semantics primitives and consistent with arbitrary-precision Python integers on the intended domain. |
| Trusted `py2mpy.py` | Source-to-`solution.mpy` bridge. Byte identity was independently regenerated; acceptable and directly checked for this source. |
| Macro-to-translated-AST correspondence | Load and function pinning. Audited term by term; macros compile away and do not compute an answer. Acceptable. |
| `intVals` iterator contextual bridge | Loop and function symbolic generality. Equations are exhaustive and truthful, but no bridge-free contextual K theorem closes because the fresh embedding is opaque under fixed `#iterNext`. Concerning evidence gap, not a witnessed false rule. |
| `valSeqAt` fixed `[total]` primitive | Initial `nums[0]`. Globally it is underspecified OOB/opaque, but formal input is structurally nonempty and only exact index 0 is used; acceptable on the theorem domain. |
| Verified loop summary | Whole-function closure. Its exact universal bridge-free `LOOP-SPEC` closes; acceptable derived operational bridge. |
| Bare read-only list representation versus allocated `ref` from a real `ListExpr` call | Universal theorem uses bare list; concrete translated K calls exercise the allocated-ref path, and the body only reads. Sound for the supported verification representation, with a documented universal-composition evidence limitation. |
| Kadane recurrence equals the natural-language subarray minimum | Final intent statement. Supported by the explicit induction above and 20,120 three-way differential cases, but not machine-checked in K. This is an informal intent bridge and the principal concern. |
| Candidate provenance/history | No proof dependence. All requested records are absent; concerning only for generation auditability. |

Differential tests, concrete K runs, and the informal induction are supporting
evidence. They are not treated as substitutes for the successful K
reachability claims. Conversely, `#Top` is not treated as proof that the
proof-local theory is sound; the extension inventory, bridge analysis, body
sensitivity, and fresh non-vacuity check supply that separate audit.

No infrastructure uncertainty was converted into a candidate failure. The
isolated missing-float-hook diagnostics in two optional wrong-value experiments
are excluded from the decision because the required builds, concrete run,
three positive proofs, body mutation, and non-vacuity mutation all completed
normally.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
