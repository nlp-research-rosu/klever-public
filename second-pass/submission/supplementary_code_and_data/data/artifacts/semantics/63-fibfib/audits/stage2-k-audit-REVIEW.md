# Independent adversarial audit: 63-fibfib

This review treats every candidate artifact and generation record as untrusted.
I rebuilt from copied source artifacts in `/tmp/audit-work/rebuild`, using the
trusted translator and trusted supplied semantics. I did not use the
candidate's compiled artifacts or `parsed-spec.json`.

## 1. Input and provenance integrity

The launcher declares `record_layout = legacy-selected-stage1`,
`condition = semantics`, and `semantics_mode = SUPPLIED_SEMANTICS`. The trusted
`/reference/reference-semantics` mount is present, so the trusted mounts agree
with the rendered mode.

The campaign object in `/audit-input.json` is exactly equal to
`/audit-campaign-lock.json`. The lock's independently calculated SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
equal to the recorded value.

All launcher-declared mounts and all records required for
`legacy-selected-stage1` are real, readable files/directories rather than
symlinks:

- `/run.json`, `/task.json`, and `/generation-result.json`;
- `invocation.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`,
  `prompt.txt`, and the structured trace;
- `usage.json`, which is present and therefore was also inspected;
- the candidate, canonical, prompt, translator, generation, and supplied
  semantics mounts.

Historical `runtime-metrics.json` is absent, but this is explicitly permitted
for this legacy-selected layout. Every recorded file SHA-256 checked by the
reviewer matches. The current candidate tree's independent, length-delimited
digest is
`d6bcecda8bb00c12c1802722b4f9df752be850612f81767774c511aa8cdc7ba5`,
which equals the retained workspace hash in `/generation-result.json`. The
trace tree digest is
`e14ad1cca65e8eddb511caf7ef3091e5bd8ee061b3cfc65dd64c668c48d730e3`,
which equals `usage.json`'s source-trace digest.

The candidate prompt and translator are byte-identical to their trusted
mounts. A recursive path/type/content comparison found exactly 25 entries in
each supplied-semantics tree, no unsupported entries or symlinks, and no
missing, additional, or changed entry. Thus the candidate semantics is exactly
the trusted supplied semantics. Evidence:
[stage1-integrity.log](evidence/stage1-integrity.log).

I read the complete 339-event JSONL trace and the complete generation output
through a reviewer parser. The trace contains 74 completed tool-output events,
including exploratory failures and the eventual claimed `#Top`. Those are only
historical claims; none is used as proof evidence here. See
[generation-record-summary.log](evidence/generation-record-summary.log) and
[generation_record_summary.py](evidence/generation_record_summary.py).

No infrastructure breach was found.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted source contract defines the nonnegative FibFib sequence:

- `T(0) = 0`, `T(1) = 0`, and `T(2) = 1`;
- for `n >= 3`, `T(n) = T(n-1) + T(n-2) + T(n-3)`;
- compute the `n`-th element efficiently.

The submitted `solution.py` maintains the triple `(a,b,c)`, initially
`(0,0,1)`, and applies `(a,b,c) := (b,c,a+b+c)` exactly `n` times. It then
returns `a`. This is a different, iterative algorithm from the trusted
recursive canonical implementation, which is allowed.

Running the trusted translator in scratch produced
`regenerated-solution.mpy` with SHA-256
`c368841f1caa6223476b198afe39b7d479f69ec3268b813d7e9421a56be184eb`.
It is byte-identical to the submitted `solution.mpy`; both translation and
`cmp` exited 0. See
[translator-identity.log](evidence/translator-identity.log).

The independent differential harness imports the trusted canonical entry point
and the submitted Python entry point. It covers the documented examples,
boundaries 0/1/2/3/4, every integer from 0 through 25, and a recorded
seed-63063 generated sample. It reported zero mismatches. There is no “empty”
integer case. An explicit `n = -1` probe shows the canonical implementation
raises `RecursionError`, while the submitted implementation returns 0.
Negative indices are outside the sequence's nonnegative index domain and do
not represent normally terminating canonical behavior, so this is not a
material domain narrowing. Evidence:
[differential.py](evidence/differential.py) and
[differential.log](evidence/differential.log).

## 3. Clean proof reconstruction

K 7.1.293 was used; versions are recorded in
[tool-versions.log](evidence/tool-versions.log). No candidate-built definition
or cache was copied. The concrete and proof definitions were rebuilt from the
scratch sources.

The fresh commands and results were:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
EXIT_STATUS: 0

krun /audit-output/evidence/reviewer-smoke.mpy \
  --definition runtime-kompiled --output none
EXIT_STATUS: 0

kompile verification.k --backend haskell \
  --main-module FIBFIB-VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
EXIT_STATUS: 0
```

The reviewer-authored concrete program tests calls at
`n = 0,1,2,3,5,8,12`; see
[reviewer-smoke.mpy](evidence/reviewer-smoke.mpy) and
[krun-reviewer-smoke.log](evidence/krun-reviewer-smoke.log). Build logs are
[kompile-llvm.log](evidence/kompile-llvm.log) and
[kompile-haskell.log](evidence/kompile-haskell.log).

Every positive claim was then exercised from the fresh Haskell definition:

| Claims retained | Exit | Exact success |
|---|---:|---|
| `FIBFIB-SPEC.fibfib-loop` | 0 | `#Top` |
| `fibfib-loop,fibfib-correct` | 0 | `#Top` |
| `example-1` | 0 | `#Top` |
| `example-5` | 0 | `#Top` |
| `example-8` | 0 | `#Top` |
| complete `FIBFIB-SPEC` | 0 | `#Top` |

The target pair is the correct independent target run: filtering to
`fibfib-correct` alone also removes the loop circularity that the entry theorem
uses. That diagnostic was interrupted after more than 90 seconds and is not a
failed positive target; retaining the required helper and target closes in
6.4 seconds. Logs:
[kprove-fibfib-loop.log](evidence/kprove-fibfib-loop.log),
[kprove-targets.log](evidence/kprove-targets.log),
[kprove-example-1.log](evidence/kprove-example-1.log),
[kprove-example-5.log](evidence/kprove-example-5.log),
[kprove-example-8.log](evidence/kprove-example-8.log), and
[kprove-all.log](evidence/kprove-all.log).

The compile warnings concern fixed-semantics unused cases and unused variables;
they do not alter the success criterion. Each successful proof command exits 0
and contains an exact `#Top`.

## 4. Adequacy and real-program pinning

### Claims in plain language

`fibfib-loop` starts at the supplied semantics' internal `#while` head. Its
current scope contains integer values `a=A`, `b=B`, `c=C`, `d=D`, `i=I`, and
`n=N`, with `0 <= I <= N`. It proves that finishing this exact loop sets
`i=N` and sets `a` to `fibFrom(A,B,C,N-I)`. It deliberately leaves final
`b`, `c`, and `d` existential because the caller does not observe them. It
frames the continuation, other scopes, and all omitted configuration cells.

`fibfib-correct` assumes an integer `N >= 0`, a clean module configuration, and
the `fibfib` name bound to the exact submitted closure. It proves that the real
call returns exactly `fibFrom(0,0,1,N)`, restores the caller configuration,
leaves no return state or exception, and does not merely imply or permit an
unconstrained result.

The three example claims reduce the formal summary at 1, 5, and 8 to 0, 4, and
24.

### Program identity

A fresh KAST parse of the regenerated `solution.mpy` was mechanically compared
with a fresh JSON serialization of the entry claim. There is exactly one
translated `FuncDef("fibfib",...)`, exactly one closure in the target claim,
and their constructor-level bodies have the identical SHA-256
`de743987219db528698ec6a1760adc665d19254acc73dfb4308cbbcf58f7782a`.
Their parameter terms are identical after removing the exact `Params(_)`
wrapper consumed by the fixed `functions.k:14` binding rule. See
[pinning_check.py](evidence/pinning_check.py) and
[pinning-check.log](evidence/pinning-check.log).

Thus the claim's constructed closure is the same binding, parameters, and body
that loading the translated `FuncDef` produces. The claim does not execute an
unrelated substitute program.

### Satisfiability and intended value

The entry precondition is satisfied, for example, by `N=5` and the exact clean
configuration written in the claim. A loop precondition witness is
`L=1, A=0, B=0, C=1, D=0, I=0, N=5`, with the displayed six local bindings.

Ground substitutions at `N = 0,1,2,3,5,8,12,20,25` make the claimed
`fibFrom` result equal to both Python implementations. See
[claim_substitution.py](evidence/claim_substitution.py) and
[claim-substitution.log](evidence/claim-substitution.log).

Mathematically, let `(x_n,y_n,z_n)` be the triple after `n` shifts from
`(0,0,1)`. The defining equations for `fibFrom` make its value `x_n`.
The base triple is `(T_0,T_1,T_2)`, and one shift changes
`(T_n,T_{n+1},T_{n+2})` to
`(T_{n+1},T_{n+2},T_n+T_{n+1}+T_{n+2})`.
Induction therefore gives `x_n = T_n` for every nonnegative `n`, including
the three required bases and the stated recurrence. This is a direct
mathematical interpretation of the fully defined summary, not an oracle
assumption.

Finally, the body-sensitivity mutation changes the actual closure term executed
by the claim from initial `c=1` to `c=2`. It builds, then fails with a genuine
stuck implication requiring
`fibFrom(0,0,2,N) = fibFrom(0,0,1,N)`; `N=2` is a concrete false witness. See
[spec-body-mutation.k](evidence/spec-body-mutation.k),
[body-mutation-build.log](evidence/body-mutation-build.log), and
[body-mutation-proof.log](evidence/body-mutation-proof.log).

## 5. Rule-by-rule static soundness review

The exhaustive source inventory is
[static-rule-inventory.md](evidence/static-rule-inventory.md), generated by
[static_inventory.py](evidence/static_inventory.py). It contains all 937 local
entries:

- 698 rules, 228 syntax declarations, 5 contexts, 1 configuration, and 5
  claims;
- 107 declarations marked `total`, 147 marked `function`, no declaration
  marked `functional`, 45 priority occurrences, 35 concrete-rule occurrences,
  22 `no-evaluators` declarations, and 1 simplification rule;
- 928 entries from the byte-verified supplied semantics, 4 entries from
  `verification.k`, and 5 claims from `spec.k`.

Every fixed-semantics entry is individually source-located and classified in
the inventory as directly exercised/mapped or outside the directly mapped
slice. Entries outside that slice were screened for syntactic overlap,
task-specific content, and dependency through opaque results. That
classification is appropriate in `SUPPLIED_SEMANTICS` mode: these rules
constitute the selected semantics level, while the used slice still requires
an overlap, state, and control audit. The proof definition imports `MPY`, not
the LLVM-only `MPY-CONCRETE`.

### Used construct mapping and state/control audit

| Program construct | Declaration and material fixed rules |
|---|---|
| `Call`, `Name`, `Int` | `syntax.k:9,28`; `call.k:20-21,69-74`; `core.k:131-154,189-195` |
| function parameters/return | `syntax.k:50,53,57,60`; `functions.k:14-16,63-90` |
| statement sequence/assignment | `syntax.k:41,56`; `core.k:126-127`; `controls.k:9-18` |
| `While` | `syntax.k:46`; `controls.k:65-67,77-85` |
| `Compare("<",...)` | `syntax.k:30,32`; `operators.k:15-17`; `int.k:22` |
| integer `+` | `syntax.k:15`; `operators.k:12`; `int.k:9` |

The fixed call route evaluates the callee, evaluates the sole argument
left-to-right, allocates a fresh local scope, pushes the complete caller
continuation, and binds `n`. Assignments evaluate their right sides before
updating the current scope. `BinOp` is sequentially strict. The while rules
reevaluate the integer guard, execute the body, and return through an explicit
loop label. Integer truthiness, comparison, and addition use unbounded K
integers, matching Python integers on this path. Return records the value,
pops the exact frame, restores the caller environment, deletes the local
scope, and restores `scopeLoc`. The program performs no heap allocation,
output, imports, exceptions, or other observable effects.

Potential priority overlaps are pruned on this path: the cell-assignment rules
require a `"$cells"` binding absent from the plain closure frame; ref-dereference
rules require heap references while all values are integers; and the generic
call rule has no proof-local interception. No proof-local priority rule exists.

### Proof-local extension inventory

1. `syntax Int ::= fibFrom(Int,Int,Int,Int) [function]` is a
   result-bearing definitional summary, not an operational rewrite.
2. For `N <= 0`, `fibFrom(A,B,C,N) = A`.
3. For `N > 0`, it becomes
   `fibFrom(B,C,A+B+C,N-1)`.
4. The simplification
   `N - (I+1) = (N-I) + (-1)` is a valid integer identity.

The two `fibFrom` guards are disjoint and exhaustive over integer `N`; the
positive branch strictly decreases `N`, and the base branch terminates.
There is no overlap disagreement. The summary's result is therefore fixed for
every use. The simplification is universally true and does not recreate its
left-hand shape.

There is no `<k>` rule, `total` assertion, opaque symbol, priority rule,
concrete rule, trusted claim, or operational bridge in `verification.k`. A
task-answer scan found no `fibfib`, `fibFrom`, or task-specific material in the
supplied semantics, and none of its 22 opaque/no-evaluator primitives occurs
in the program, verification module, or spec. See
[task-answer-and-bridge-scan.log](evidence/task-answer-and-bridge-scan.log).

The loop claim supplies the universal connection theorem for the
program-derived summary. It executes the exact fixed-semantics loop body and
matches its complete arbitrary continuation; it frames all nonlocal cells and
summarizes only the local values it constrains. One productive iteration
changes `(A,B,C,I)` to `(B,C,A+B+C,I+1)`, after which the same circularity
applies. The valid arithmetic simplification aligns the remaining iteration
count. It neither returns abruptly nor skips binding, argument evaluation,
the body, frame handling, or exceptions.

The supplied semantics compiler reports several non-exhaustive `total`
functions on unused junk constructors (for example float/string helper cases).
Those fixed, opaque or partial-language boundaries are not reachable and no
claim depends on their value or definedness. They do not enable a false
conclusion here. No unsound rule or false-conclusion witness was found.

## 6. Fresh non-vacuity test

The reviewer-authored mutation changes the entry result to
`fibFrom(0,0,1,N) + 1`, while retaining the exact body, loop helper, and
satisfiable precondition. It is demonstrably false at `N=0`.

The mutation first built successfully:

```text
kprove /audit-output/evidence/spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module FIBFIB-SPEC-VACUITY \
  --claims FIBFIB-SPEC-VACUITY.fibfib-loop,FIBFIB-SPEC-VACUITY.fibfib-correct-plus-one \
  --dry-run
EXIT_STATUS: 0
```

The same command without `--dry-run` exited 1, printed
`WarnStuckClaimState`, and exposed the expected unmet equality
`fibFrom(...) +Int 1 #Equals fibFrom(...)`. It did not fail through parsing,
imports, timeout, or an unrelated crash. Evidence:
[spec-vacuity.k](evidence/spec-vacuity.k),
[vacuity-build.log](evidence/vacuity-build.log), and
[vacuity-proof.log](evidence/vacuity-proof.log).

This passes the fresh non-vacuity gate. The independent body mutation in stage
4 separately demonstrates execution/body sensitivity.

## 7. Proven versus assumed accounting

The successful reachability proof establishes the following partial-correctness
theorem:

> Under the exact supplied MPY semantics, for every K integer `N >= 0`, if the
> exact translated `fibfib` call terminates from the claim's clean module
> configuration, its returned value is `fibFrom(0,0,1,N)`, with normal frame
> restoration and no exception. The exact loop computes the corresponding
> triple-shift summary.

Together with the elementary induction in stage 4,
`fibFrom(0,0,1,N)` is the natural-language FibFib value for every nonnegative
`N`. This is unrestricted over that source-contract domain; it is not a finite
unrolling or a finite set of examples.

Trust and evidence ledger:

| Boundary | Dependents | Assessment |
|---|---|---|
| K 7.1.293 parser/compiler/Haskell prover and builtin integer theory | all machine checks | Standard necessary proof-tool trust; acceptable. |
| Byte-verified supplied MPY semantics | execution theorem | The mandated fixed semantics. Its used integer/call/loop slice was reviewed in detail; acceptable. |
| Trusted `py2mpy.py` translation | source-to-K bridge | Byte regeneration and constructor-level body pinning pass; acceptable. |
| Mathematical identification of triple shift with the stated recurrence | human-facing contract | Direct induction with no new primitive or oracle; acceptable. |
| Python differential execution over 0..25 plus generated cases | implementation/canonical evidence | Finite supporting evidence only; not used as the universal K proof. |
| Opaque float, sort, hash, and other supplied primitives | none | Unused and absent from every result/control dependency; inert. |
| Negative integers | none | Outside the nonnegative sequence-index domain; the canonical function does not normally return there. |
| Termination | not claimed by K reachability result | This audit concerns partial correctness. For nonnegative concrete `N`, the source loop plainly increments `i` to `N`, but that fact is not substituted for the reachability proof. |

There is no proof-local trusted primitive, opaque oracle, empirical operational
bridge, answer-encoding semantic rule, or unconstrained result. The differential
tests and candidate generation traces are not used as substitutes for the K
proof.

Gate A (real-program soundness): PASS. Gate B (intent adequacy): PASS. Gate C
(trust/evidence auditability): PASS. The reconstructed proof is sound,
result-constraining, and pins the real generated program over the full material
source-contract domain.

VERDICT: PASS
LEGITIMACY: LEGIT
