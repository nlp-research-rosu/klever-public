# Independent adversarial review: 114-minSubArraySum

The candidate contains a legitimate, result-constraining partial-correctness
proof for every finite non-empty list of mathematical integers. The submitted
Python implementation agrees with the trusted canonical implementation, the
trusted translator regenerates the submitted constructor program byte for byte,
the end-to-end claim executes that constructor-identical program, and all three
claims close from clean source builds.

The verdict is `CONCERNS / LEGIT`, rather than `PASS / LEGIT`, because the
generated semantics includes a priority-40 task-specific acceleration for
`len(E) == 1`. It is sound on every reachable state in the theorem's intended
non-empty domain, and removing it preserves all recorded results, but the
candidate supplies no separate bridge-free universal connection claim. Its
match is also broader than its complete behavior: if `E` evaluates to an empty
modeled list, the fused path sticks instead of returning `false`. This cannot
make a false result provable for an intended input, so it is a non-fatal
evidence/semantics limitation rather than an unsoundness or domain-narrowing
failure.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- problem `114-minSubArraySum`, condition `bare`;
- record layout `legacy-selected-stage1`;
- semantics mode `GENERATED_SEMANTICS`;
- candidate `/candidate`;
- trusted prompt, translator, and canonical program below `/reference`;
- no mounted reference semantics.

This boundary is consistent. `/reference/reference-semantics` does not exist,
and neither does `/candidate/reference-semantics`; no hidden or inferred
reference semantics was used.

I read and independently inspected `/audit-input.json`,
`/audit-campaign-lock.json`, `/run.json`, `/task.json`,
`/generation-result.json`, `/generation-evidence/invocation.json`,
`metrics.json`, `usage.json`, `legacy-metrics.json`, `legacy-run-input.json`,
`codex-last.txt`, `codex-output.log`, `prompt.txt`, and the complete structured
trace tree. `runtime-metrics.json` is absent, as permitted for this
`legacy-selected-stage1` record layout.

The campaign lock is structurally identical to the `audit_campaign` block and
has the declared SHA-256. Every required record is a readable regular file;
the candidate, generation, trace, and reference trees contain no symlink or
unsupported node. The one trace file has 176 valid JSONL records and no
malformed line. Candidate `prompt.py` and `py2mpy.py` are byte-identical to
their trusted mounts.

Every individually specified record digest matches. Independently reproduced
pipeline tree digests also match the generation records:

- candidate: `2b26a23bfa05cd2cf81d2b8b1fc4fe517418751995a8cd0cb42e0e0a56eaa373`,
  equal to the invocation's retained workspace digest;
- trace: `c1cbb5179dfe4cd782ee482c617c0450891c664361cb80baf12175f759f9b8b6`,
  equal to `usage.json`'s source-trace digest.

`audit-input.json` additionally records opaque launcher tree digests
`1ef78f...` and `f41e4c...` without defining their tree serialization. I did
not pretend that a different tree-hash serialization could reproduce those
values. This is not a mount-integrity contradiction: all file digests, the
stage workspace digest, the trace-file digest, and both documented pipeline
tree digests agree. Full results are in
[01-integrity.log](evidence/01-integrity.log) and
[02-generation-records.log](evidence/02-generation-records.log).

No infrastructure breach was found.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and domain

The trusted prompt asks `minSubArraySum(nums)` to return the minimum sum of any
non-empty contiguous subarray of an integer array. A realizable input must
therefore contain at least one integer. The trusted canonical implementation
also confirms this boundary: it raises `ValueError` on an empty list when it
takes `max` of an empty generator.

The candidate uses a different but correct recursive algorithm:

1. `min_prefix_sum` computes the least sum among non-empty prefixes.
2. `minSubArraySum` takes the minimum of the tail's least subarray and the
   current list's least prefix.
3. Singleton lists are the base case for both functions.

There is no fixed length bound and no bound on integer magnitude in either the
program or the claims.

### Trusted regeneration

Running the trusted `/reference/py2mpy.py` over the scratch copy of
`solution.py` produced SHA-256
`5824615b9afe1a35b69f5a428651e2361081b01cc0274796f1516e8c04dd9838`,
identical byte for byte to submitted `solution.mpy`. See
[03-translation.log](evidence/03-translation.log) and the regeneration script
[check_translation.py](evidence/check_translation.py).

### Independent differential testing

[differential_test.py](evidence/differential_test.py) imports the trusted
canonical entry point and the scratch candidate entry point independently. It
also compares both with a direct brute-force enumeration of all non-empty
contiguous subarrays. Inputs are recorded in
[differential_inputs.json](evidence/differential_inputs.json):

- both documented examples;
- 18 curated singleton, two-element, zero, mixed-sign, all-positive,
  all-negative, and large-integer cases;
- all 19,607 lists of lengths 1 through 5 over `[-3,3]`;
- 250 deterministic random lists of lengths 1 through 40 over `[-100,100]`.

All 19,877 intended-domain cases agreed. On the separately recorded empty
input, canonical Python raises `ValueError` and the recursive candidate
eventually raises `RecursionError`; this is an out-of-contract difference, not
a hidden restriction of a defined source behavior. Exact output is in
[04-differential.log](evidence/04-differential.log).

## 3. Clean proof reconstruction

All candidate source artifacts were copied to `/tmp/audit-work/source`; all
definitions were written to new directories below `/tmp/audit-work/build`.
No candidate-built definition or cache was used. The candidate/scratch source
hash pairs for `solution.py`, `solution.mpy`, `semantic.k`, `verification.k`,
and `spec.k` are identical in
[21-source-copy-check.log](evidence/21-source-copy-check.log).

The observed toolchain is K v7.1.293
([05-toolchain.log](evidence/05-toolchain.log)).

Fresh builds:

- LLVM generated semantics:
  [06-build-concrete.log](evidence/06-build-concrete.log), exit 0.
- Haskell proof definition:
  [07-build-proof.log](evidence/07-build-proof.log), exit 0.

The claims have real proof dependencies. The target-call circularity uses the
helper circularity, and the end-to-end claim uses both. I therefore checked the
dependency-closed sequence:

- helper alone: exit 0 and `#Top`,
  [08-proof-helper.log](evidence/08-proof-helper.log);
- helper plus target call: exit 0 and `#Top`,
  [09-proof-helper-target.log](evidence/09-proof-helper-target.log);
- the unchanged candidate `spec.k`, containing all three claims: exit 0 and
  `#Top`, [10-proof-all.log](evidence/10-proof-all.log).

A diagnostic target-only spec, with its required helper circularity
deliberately removed, becomes stuck in the helper call. That expected result
is preserved in
[09a-dependency-stripped-target-diagnostic.log](evidence/09a-dependency-stripped-target-diagnostic.log);
it is evidence that the supporting claim is exercised, not a positive-target
failure. The exact cumulative specs are preserved as
[spec-helper-only.k](evidence/spec-helper-only.k) and
[spec-helper-target.k](evidence/spec-helper-target.k).

The newly compiled LLVM semantics was then executed on eight cases spanning
both prompt examples, singleton `7`, `0`, and `-11`, a two-element recursive
case, and two longer mixed-sign lists. Every `krun` exited 0, consumed the
computation to `pyInt(result) ~> .K`, and agreed with both Python
implementations. See
[11-concrete-semantics.log](evidence/11-concrete-semantics.log) and
[concrete_semantics_compare.py](evidence/concrete_semantics_compare.py).

## 4. Adequacy and real-program pinning

### Claims in plain language

The claims have no textual `requires`; their sorted configuration patterns are
their preconditions.

| Claim | Precondition | Postcondition |
|---|---|---|
| Helper, `spec.k:8-18` | The function map is exactly `solutionFunctions`; call the exact `min_prefix_sum` binding on any `cons(H,T)`, from arbitrary caller environment, continuation, stack, entry, arguments, and depth. | Return exactly `pyInt(minPrefix(cons(H,T)))`, restore caller environment/stack/depth, and resume the same continuation. |
| Target call, `spec.k:21-31` | The same framing, but call the exact `minSubArraySum` binding on any non-empty finite integer list. | Return exactly `pyInt(minSubarray(cons(H,T)))` and restore the framed caller state. |
| End to end, `spec.k:35-45` | Begin with `solutionProgram`, target entry `"minSubArraySum"`, one `cons(H,T)` argument, and empty function/environment/stack state at depth `z`. | Consume the complete computation and leave exactly `pyInt(minSubarray(cons(H,T)))`; load exactly `solutionFunctions`; leave environment/stack empty and depth `z`. |

These are equality-style result obligations, not implications to an
unconstrained variable. `minPrefix` and `minSubarray` have disjoint,
structurally recursive equations, so the result is fixed for every non-empty
`IntList`.

Satisfying states exist. For the two call claims, one instance is `H=4`,
`T=cons(-5,nil)`, `K=.K`, `RHO=.Map`, `STACK=.List`, `D=z`, with arbitrary
well-sorted entry/args. The helper summary is `-1`; the target summary is `-5`.
For the end-to-end claim, `[5,-2,-3,7,-10,4]` satisfies the exact initial
configuration and yields `-10`. K summary evaluation, generated Python, and
canonical Python agree in
[14-claim-witnesses.log](evidence/14-claim-witnesses.log).

### Mechanical program identity

The end-to-end `<k>` cell does not begin with a source filename; it begins with
the defined constructor constant `solutionProgram`. I checked the allowed
constructor-level pinning mechanically:

- extracted the `solutionProgram` RHS;
- normalized only K's `.Stmts` spelling to the concrete parser's empty
  statement-list spelling;
- parsed both it and submitted `solution.mpy` with K's `MPY-SYNTAX` parser;
- obtained identical KAST JSON and identical KAST SHA-256
  `e732624fc8c29ed806becaa128f04ee4882e4c70ce9760fe3038b0a958a6e301`.

See [12-program-term-identity.log](evidence/12-program-term-identity.log) and
[compare_program_term.py](evidence/compare_program_term.py).

The call claims use `solutionFunctions`. A second mechanical comparison
extracts each submitted `FuncDef`, constructs its corresponding closure, and
parses both sides with K. Both names, parameter terms, and bodies are
constructor-identical. See
[13-function-map-identity.log](evidence/13-function-map-identity.log) and
[compare_function_map.py](evidence/compare_function_map.py).

The end-to-end semantics starts with an empty function map and executes both
real `FuncDef` terms before invocation. The call claims match the exact map
that loading produces; no rule substitutes a different function body.

### Body sensitivity

I mutated the program term actually executed by the end-to-end claim, not an
external Python file: only the target singleton branch inside
`solutionProgram` changed from `return nums[0]` to `return 1`. The mutated
definition built successfully
([15-build-body-mutant.log](evidence/15-build-body-mutant.log)), and proof
failed with a reachable singleton state whose actual result is `pyInt(1)`
([16-body-sensitivity.log](evidence/16-body-sensitivity.log)). The exact change
and spec are preserved in
[body-sensitivity.patch](evidence/body-sensitivity.patch) and
[spec-body-mutant.k](evidence/spec-body-mutant.k). This establishes sensitivity
to the submitted body's material behavior.

## 5. Rule-by-rule static soundness review

The exhaustive inventory is
[RULE-INVENTORY.md](evidence/RULE-INVENTORY.md). It enumerates:

- every local syntax production and the seven-cell configuration;
- all 45 rules in `semantic.k`;
- all six equations in `verification.k`;
- all three reachability claims;
- all local attributes and submitted-constructor coverage.

There are exactly six local `[function]` declarations: `length`, `intMin`,
`minPrefix`, `minSubarray`, `solutionFunctions`, and `solutionProgram`. There
are no local `[total]`, `[functional]`, `[simplification]`, `[concrete]`,
opaque-without-equations, `context`, or `alias` declarations. There is one
priority rule.

### Configuration, evaluation, state, and control

The semantics explicitly models computation, configured entry and arguments,
function bindings, local bindings, a call stack, and structural call depth.
The submitted program needs no heap, mutable aggregate, I/O, or exception
effect on its intended inputs.

Rules 1-14 load definitions, schedule statements left to right, evaluate
guards and assignment/return expressions, and implement abrupt return. The
return rule restores both the exact saved caller continuation and caller local
map, pops the top frame, and decrements depth. No observable modeled cell is
silently discarded.

Name lookup rules can overlap in a generic language state, but not in a
reachable state of this fixed program: locals contain only `nums`, `tail_min`,
and `prefix_min`; the function map contains only `min_prefix_sum` and
`minSubArraySum`; builtins are `len` and `min`. Thus the submitted execution
has a unique binding at every lookup.

Rules 19-34 evaluate callees and operands left to right, save exact
continuations across user calls, and interpret only the used external
primitives: list length, binary integer minimum, integer addition, and integer
equality. Rules 38-41 model exactly `nums[0]` and `nums[1:]`; their skipped
index/bound evaluation consists only of inert integer/omitted-bound literals.
Head and tail are reached only for non-empty lists. K integers are unbounded,
matching Python integer arithmetic rather than introducing overflow.

Every constructor appearing in submitted `solution.mpy` has both a syntax
declaration and an execution path. Missing behavior for unrelated translator
constructors is permitted in `GENERATED_SEMANTICS` and does not affect this
program.

### Functions and mathematical equations

`length` descends over `IntList`. `intMin` has disjoint and exhaustive `<=` and
`>` guards. `minPrefix` is the minimum of the singleton prefix `[H]` and every
prefix obtained by adding `H` to a non-empty tail prefix. `minSubarray` is the
minimum of subarrays beginning at `H` and subarrays wholly in the tail. Their
base/recursive equations are truthful and structurally descending on every
claimed use. They are intentionally undefined on `nil`; no claim or recursive
equation calls them on `nil`.

`solutionProgram` and `solutionFunctions` are definitional names for
mechanically checked program syntax. They do not replace source execution with
an opaque value.

### Priority-40 fused guard

`semantic.k:160-163` preempts generic evaluation of
`Compare(Call(Name("len"), E), CmpOp("==", Int(1)))`. It evaluates `E` once
and distinguishes `cons(_,nil)` from `cons(_,cons(_,_))`.

For every state reachable from an entry claim, `E` is `Name("nums")` bound to
a non-empty `IntList`. The two constructors are then exhaustive, and the rule
has exactly the same Boolean result as the ordinary `length` and integer
equality equations. It preserves evaluation count, caller continuation, and
all state cells.

The rule is broader than this justification. If `E` yields `pyList(nil)`, the
fused path has no `singletonTest` rule, whereas unfused `len(nil) == 1` would
produce `false`. This witness shows incompleteness outside the intended domain,
not a false conclusion: the fused rule cannot fabricate either Boolean or a
returned task result there. The real program already has undefined/error
behavior for empty input.

As an independent sensitivity check, I removed only the fused rule, rebuilt
the semantics successfully
([19-build-no-fused.log](evidence/19-build-no-fused.log)), and reran all eight
normal/boundary cases. Every unfused result agreed with fused K and both Python
implementations ([20-no-fused-concrete.log](evidence/20-no-fused-concrete.log));
the exact edit is [no-fused-bridge.patch](evidence/no-fused-bridge.patch).
This is finite evidence, not a universal theorem. The absence of a candidate
bridge-free universal connection claim is the main reason for `CONCERNS`.

No rule was classified as materially unsound, so there is no alleged
unsoundness for which a false-conclusion witness is missing. No answer-encoding
rule, unconstrained result oracle, false simplification, inconsistent overlap,
or execution-bypassing program summary was found.

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`; I created a fresh one in scratch
while preserving both supporting call circularities. Only the end-to-end
result obligation changed:

`minSubarray(cons(H,T))` became `minSubarray(cons(H,T)) +Int 1`.

This is false for every satisfying input; for example `[0]` returns `0`, not
`1`.

The mutated spec compiled to KORE successfully with `--dry-run`, exit 0
([17-vacuity-dry-run.log](evidence/17-vacuity-dry-run.log)). Actual `kprove`
then exited 1 with `WarnStuckClaimState` after reaching the original
`pyInt(minSubarray(cons(H,T)))`. The residual is the expected failed
implication:

`minSubarray(cons(H,T)) +Int 1 = minSubarray(cons(H,T))`.

This is a reached, result-specific unmet obligation—not a parse error,
timeout, missing import, or unrelated crash. See
[18-vacuity-proof.log](evidence/18-vacuity-proof.log) and the exact preserved
mutation [spec-vacuity.k](evidence/spec-vacuity.k).

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Under the compiled local K theory, for every finite non-empty `IntList`:

1. the exact two submitted function bodies load;
2. the configured target binding is selected;
3. calls, recursion, assignments, slicing, indexing, arithmetic, and returns
   execute through the generated operational rules;
4. if execution reaches normal completion, the sole result is
   `pyInt(minSubarray(input))`;
5. the mathematical equations characterize that value as the minimum sum of
   a non-empty contiguous subarray.

The helper and target claims are universal circularities over arbitrary caller
frames and continuations. The end-to-end claim pins their use to the actual
loaded bodies. This is an unbounded partial-correctness theorem, not a finite
size proof or bounded unrolling.

The proof does not separately establish a CPython resource/termination theorem.
In particular, it abstracts from CPython recursion limits. That is compatible
with partial correctness but should not be read as a guarantee that the
recursive Python implementation returns normally under every finite machine
resource limit.

### Trust ledger

| Boundary | Influence | Assessment and evidence |
|---|---|---|
| K v7.1.293 compiler, LLVM/Haskell backends, reachability logic, and K's `INT`, `BOOL`, `STRING`, `MAP`, and `LIST` domains | All parsing, rewriting, arithmetic, maps, stacks, and proof closure | Necessary low-level trusted computing base; versions and fresh builds recorded. |
| Trusted `py2mpy.py` | Python AST to constructor term | Launcher-designated trusted input; candidate copy matches; regeneration is byte-identical. |
| Generated `semantic.k` Python subset | Connects constructor execution to intended Python behavior | Audited rule by rule rather than assumed. Complete for every used construct on non-empty integer lists; differential and concrete evidence support the bridge. |
| `len`, two-argument `min`, integer `+`/`==`, list head, and `[1:]` | Guards, recursive inputs, and final values | Direct equations over K integers/inductive lists; ordinary mathematics and used Python behavior. |
| Priority-40 fused singleton test | Recursive branch control and hence result | Truthful on every reachable theorem state; broader match is incomplete on empty lists; no universal bridge-free candidate theorem. Non-fatal concern. |
| `minPrefix`/`minSubarray` equations | Final postcondition meaning | Inductive mathematical decomposition reviewed statically; ground K/Python witnesses and 19,877 differentials support, but finite tests do not replace the K proof. |
| `solutionProgram`/`solutionFunctions` constants | Program identity and circularity binding | K-parser constructor identity plus body-sensitivity mutation; acceptable definitional normalization. |
| Differential and concrete executions | Program/canonical and semantics/Python bridges on tested inputs | Reproducible finite validation only; never treated as universal proof closure. |

### Gate and decision summary

- Real-program soundness: passes on the material non-empty integer-list domain.
  The proof executes exact bodies, preserves modeled state/control, constrains
  the result, and rejects both body and postcondition mutations.
- Intent adequacy: passes. The theorem covers arbitrary finite non-empty lists
  and unbounded integers; it is not restricted to examples or fixed sizes.
- Auditability/trust: limited but legitimate. The generated-semantics bridge is
  explicit and extensively audited; the fused priority rule lacks a separate
  universal connection artifact and is incomplete off-domain.

That limitation fits `CONCERNS / LEGIT`: it does not narrow the HumanEval
source-contract domain and cannot make a false conclusion provable on that
domain.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
