# Independent adversarial review: 24-largest-divisor

The reconstructed candidate proof is legitimate under the supplied MPY
semantics, but it has two auditability/adequacy limitations: four requested
generation-provenance artifacts are absent, and the final bridge from the
recursive scan summary to an explicit mathematical maximum/divisibility
predicate is transparent but informal. Neither limitation permits a false
program result. The appropriate decision is therefore `CONCERNS / LEGIT`.

## 1. Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`, and the trusted mount is consistent
with it: `/reference/reference-semantics` is a real directory. There is no
infrastructure-mode contradiction.

The following requested provenance artifacts are missing:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`

No structured generation trace is present. I inspected the available
[`init-spec.json`](/candidate/init-spec.json) only as an untrusted KAST claim;
it encodes the initialization claim and is not independent proof evidence.
Likewise, I listed but did not extract or reuse the candidate's
`kore-exec.tar.gz`, and ignored `__pycache__` and all candidate-produced
intermediates.

The candidate's [`prompt.py`](/candidate/prompt.py) and
[`py2mpy.py`](/candidate/py2mpy.py) are byte-identical to their trusted mounted
counterparts. Recursive, no-dereference comparison of
`/candidate/reference-semantics` with the trusted tree returned exit 0. Both
trees have the same 25 regular files and two directories, with no missing,
additional, changed, mistyped, or symlinked entry. There are no symlinks
anywhere under `/candidate`.

Evidence: [integrity script](/audit-output/evidence/stage1_integrity.sh),
[bounded log](/audit-output/evidence/stage1_integrity.log).

Stage result: integrity of the available prompt, translator, and supplied
semantics passes; provenance completeness has a documented concern.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted [prompt](/reference/prompt.py:3) asks for the largest number smaller
than `n` that divides `n` evenly, with `largest_divisor(15) == 5`. The trusted
[canonical implementation](/reference/canonical.py:7) scans candidates below
`n` in descending order and returns the first divisor. The meaningful scalar
domain is integer `n > 1`: only there is a positive proper divisor guaranteed,
and both the formal entry precondition and the dataset behavior align with that
domain.

The submitted [solution](/candidate/solution.py:1) implements the same
descending scan with `divisor = n - 1`, decrementing until `n % divisor == 0`.
Running the trusted translator on the scratch copy produced a file byte-identical
to submitted [`solution.mpy`](/candidate/solution.mpy), with SHA-256
`8d08e002fe350919c0d4bbb150a688c1993c58e17567e76e0fec32f851fa3884`.

The independent differential script loads the trusted canonical and submitted
functions from distinct absolute paths and also checks an independent
divisor-property oracle. It covered:

- the documented `15` example;
- domain minimum `2`, immediate/one/many-iteration paths, primes, composites,
  squares, powers of two, and larger representatives;
- every integer from 2 through 2000;
- 128 deterministic generated representatives from 2001 through 20000;
- 2,129 distinct intended-domain inputs in total.

There were zero intended-domain mismatches. The scalar task has no collection
"empty" input; as excluded-domain observations, `n=0` exposes a real difference
(canonical returns `None`, submitted returns `-1`) and `n=1` raises
`ZeroDivisionError` in both. This does not contradict the proved `n>1` theorem,
but makes that boundary important.

Evidence: [fidelity script](/audit-output/evidence/stage2_fidelity.sh),
[differential script](/audit-output/evidence/stage2_differential.py),
[expanded inputs](/audit-output/evidence/stage2_inputs.json),
[results log](/audit-output/evidence/stage2_fidelity.log).

Stage result: pass on the intended domain.

## 3. Clean proof reconstruction

I copied source artifacts only to `/tmp/audit-work`. Before building, both
`runtime-kompiled` and `verification-kompiled` were absent. I did not reuse the
candidate archive, K definitions, caches, logs, or traces. The live toolchain
was K `v7.1.337` (build date 2026-06-18).

Fresh commands and results were:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
Exit 0

krun concrete-tests.mpy --definition runtime-kompiled
Final <k> .K </k>, <exc> NoExc </exc>, <exit-code> 0 </exit-code>
Exit 0

kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
Exit 0

kprove spec.k --definition verification-kompiled --spec-module PREFIX-SPEC
#Top
Exit 0

kprove spec.k --definition verification-kompiled --spec-module INIT-SPEC
#Top
Exit 0

kprove spec.k --definition verification-kompiled --spec-module LOOP-SPEC
#Top
Exit 0
```

Thus every positive target claim closes independently with both required
signals. Compiler warnings are accounted for in Stage 5 rather than treated as
proof success.

Evidence: [rebuild driver](/audit-output/evidence/stage3_rebuild.sh),
[combined log](/audit-output/evidence/stage3_rebuild.log), and the individual
[LLVM build](/audit-output/evidence/stage3_llvm_build.log),
[concrete run](/audit-output/evidence/stage3_concrete_tests.log),
[Haskell build](/audit-output/evidence/stage3_haskell_build.log),
[prefix proof](/audit-output/evidence/stage3_prefix_proof.log),
[initialization proof](/audit-output/evidence/stage3_init_proof.log), and
[loop proof](/audit-output/evidence/stage3_loop_proof.log).

Stage result: pass.

## 4. Adequacy and real-program pinning

The three claims state the following:

- `PREFIX-SPEC`, under `N > 1`, loads the exact translated function, calls it,
  binds `n`, executes the ASCII docstring and `divisor = n - 1`, and reaches the
  actual `#while` head. Its result is an intermediate state with
  `divisor = N - 1`, not a final-value claim.
- `INIT-SPEC` has no numeric precondition. From a real callee state containing
  `n=N`, it executes the assignment and reaches the same loop head, ensuring
  the new local `divisor` is exactly `N-1`. It is a redundant focused lemma;
  `PREFIX-SPEC` already executes this assignment.
- `LOOP-SPEC`, under `N>1` and `1 <= D < N`, executes the real while guard,
  decrement body, return, and frame pop. It returns
  `firstDivisorAtOrBelow(N,D)` and restores the caller environment, scope
  allocation counter, stack, and scope map.

The `<k>` prefix is not a substitute program. The zero-argument
`largestDivisorBody()` function expands to the exact statement body in the
byte-verified `solution.mpy`, including its docstring. The claim then executes
ordinary supplied rules for module load, function lookup and binding, statement
sequencing, arithmetic, modulo, comparison, while control, augmented assignment,
return, and frame pop.

The modular states compose exactly. The prefix destination has `env=1`,
`scopeLoc=2`, empty heap, frame `frame(.K,0,1)`, local `n=N` and
`divisor=N-1`, plus the exact loop/return/`#endcall` continuation expected by
`LOOP-SPEC`. For `N>1`, substituting `D=N-1` satisfies the loop precondition.
Its destination
`firstDivisorAtOrBelow(N,N-1)` is definitionally
`largestProperDivisor(N)`.

Concrete satisfying witnesses exist for every entry:

- initialization: `N=15`, a local scope containing `n=15`, destination
  `divisor=14`;
- prefix: `N=15` in the default configuration;
- loop: `N=15`, `D=14`, the stated local scope and frame.

Further substitutions `N=2,15,49` produce results `1,5,7`, respectively, in
the K summary, trusted canonical Python, and submitted Python. A
reviewer-authored check restated the loop lemma and the composed public-entry
claim in one spec module; it also returned `#Top`, exit 0. That check validates
composition and does not replace the candidate's three successful claims.

Evidence: [witness script](/audit-output/evidence/stage4_witnesses.py),
[composition spec](/audit-output/evidence/stage4_end_to_end.k),
[command/results log](/audit-output/evidence/stage4_adequacy.log).

Stage result: pass.

## 5. Rule-by-rule static soundness review

The full source-level inventory contains 1,111 top-level K sentences:

- 700 rules: 593 ordinary, 35 concrete, 26 `owise`, 45 priority-bearing, and
  one simplification rule;
- 229 syntax-declaration sentences, including 148 function-declaration
  sentences, 107 `total` function declarations, 25 opaque/symbolic
  declarations, and no `functional` declaration;
- three target claims, five contexts, one configuration, and all modules,
  imports, requirements, and end markers.

Every row records its source range, normalized sentence, attributes, and review
disposition in the [exhaustive inventory](/audit-output/evidence/stage5_rule_inventory.md).
The [target-path mapping](/audit-output/evidence/stage5_used_path.md) maps every
construct in `solution.mpy` to its grammar and operational rules.

### Supplied semantics on the target path

The configuration has computation, current environment, scopes, scope
allocator, heap, heap allocator, call stack, return state, exception state, and
exit code. All are pinned or framed consistently by the claims. The generated
counter is harmless cell-completion state and does not affect the language.

Evaluation order is faithful on the used subset: statements and binary operands
are left-to-right; assignments and returns evaluate their value first; compare
evaluates its left and wrapped right operand; call evaluates callee then
arguments; while re-evaluates the condition on every iteration. The only state
allocation is the callee scope. Return discards the remaining callee
continuation, pops exactly the saved frame, restores the caller state, and
places the returned integer in caller computation. No exception or heap path is
abstracted.

For positive `D`, supplied `pyMod` agrees with Python's modulo. The base and
recursive branches therefore match the program's `!= 0` decision. At `D=1`,
the modulo is zero, so the positive-divisor exit exists. No priority rule
preempts this program with a task-specific shortcut, and `VERIFICATION` imports
`MPY`, not concrete-only `MPY-CONCRETE`.

The docstring conversion is ASCII-only in this semantics, but every character
of this submitted docstring is ASCII and the resulting value is discarded.
Integer values are unbounded mathematical integers, matching Python integers
for this computation.

### Proof-local rules

- `largestDivisorBody()` is exact syntactic sharing and does not replace
  execution.
- `largestProperDivisor(N) =
  firstDivisorAtOrBelow(N,N-1)` initializes the descending mathematical scan.
- The `firstDivisorAtOrBelow` base rule returns a positive dividing candidate.
- Its recursive rule decrements exactly one non-dividing candidate. The two
  guards are disjoint; on the target domain they cover every reached state and
  recursion descends to the divisor 1.
- `deleteFreshFrame` rewrites
  `(1 |-> S SC)[1 <- undef]` to `SC` only when key 1 is absent from `SC`. This
  is the extensional Map identity produced by the supplied `#pop`; it affects
  no value, control, heap, exception, or other cell.

No proof-local item is opaque, `total`, `functional`, `concrete`, priority
bearing, or an operational bridge. There is no invocation/loop interception,
unconstrained oracle, result fabrication, answer-encoding rewrite, or
overlapping false equation. Because I found no unsound candidate rule, there is
no unsoundness allegation requiring a false-conclusion witness.

### Fixed but unused boundaries

The supplied theory contains 25 explicitly symbolic/opaque declarations:
`md5hexCodes`, `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`,
`floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`,
`eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`,
`sqrtF`, `sortVS`, and `sortKeyVS`. None can be reached by this integer-only
program or its proof summary.

The LLVM build reported non-exhaustive-total diagnostics for `mapStrVS`,
`floorFI`, `toF`, `ceilF`, `joinCodes`, and `valSeqAt`. These are limitations
of the fixed supplied language outside the target path; no target claim,
guard, result, or simplification depends on them. They do not yield a concrete
false conclusion for this theorem.

Evidence: [inventory generator](/audit-output/evidence/stage5_inventory.py),
[inventory command log](/audit-output/evidence/stage5_inventory.log), and the
two inventories linked above.

Stage result: pass for candidate-local soundness and the complete target path;
unused fixed-language abstractions are recorded in the trust boundary.

## 6. Fresh non-vacuity test

No candidate `spec-vacuity.k` exists, so I created a fresh mutation. It preserves
the exact loop source and precondition but changes the result to
`firstDivisorAtOrBelow(N,D) +Int 1`. The satisfying witness `N=15,D=14` has
real result 5 while the mutation demands 6.

`kprove --dry-run` exited 0, proving the mutation parsed and built. The actual
proof exited 1 with `WarnStuckClaimState`; the residual contains the failed
equality `D = D +Int 1` and the expected "configuration cannot be rewritten
further" diagnostic. This is an reached, result-specific proof failure, not a
parser/import error, timeout, or unrelated crash.

Evidence: [false spec](/audit-output/evidence/stage6_false_result.k),
[driver and expected-result checks](/audit-output/evidence/stage6_mutation.sh),
[bounded proof residual](/audit-output/evidence/stage6_false_result_proof.log),
[combined log](/audit-output/evidence/stage6_mutation.log).

Stage result: pass; the positive proof is non-vacuous and result-constraining.

## 7. Proven versus assumed accounting

### Precisely established

Under the supplied MPY semantics and precondition `N>1`, the candidate's
machine-checked modular reachability claims establish partial correctness of the
exact translated public call: if it terminates, its returned integer is
`firstDivisorAtOrBelow(N,N-1)`, with caller control/state restored. The
descending summary returns the first positive divisor at or below its initial
candidate. The proof does not establish behavior for `N<=1`.

### Trust and evidence ledger

| Boundary | Influence | Accounting |
|---|---|---|
| K compiler, Haskell reachability backend, LLVM backend, and builtin Int/Bool/String/Map/List/K equality operations | Core execution and proof checking | Standard low-level trusted computing base; versions and fresh commands recorded. |
| Exact trusted supplied MPY semantics | Syntax, control, scopes, arithmetic dispatch, calls/returns | Candidate tree is byte-identical; target path reviewed statically and executed concretely. |
| Proof-local recursive divisor summary | Final value | Fully defined on every reached `N>1, D>=1` case with disjoint truthful equations; no opaque value. |
| `deleteFreshFrame` simplification | Scope restoration only | Guarded extensional Map identity; sound and no result influence. |
| The 25 fixed opaque symbols listed in Stage 5 | Potential values in unrelated float/sort/md5 programs | No dependency from this program or any claim; accepted only as unused fixed-semantics boundaries. |
| Trusted Python-to-MPY translator | Link from submitted Python to proved MPY | Byte-identity regeneration establishes the exact submitted translation. |
| Trusted canonical Python and mathematical property oracle | Link to dataset intent | 2,129 finite intended-domain comparisons, zero mismatches; empirical support, not a universal K theorem. |
| “First divisor in a descending scan from `N-1` is the largest positive proper divisor” | Human-facing maximum/divisibility meaning | Ordinary mathematical argument, not expressed as a separate K theorem with explicit divisibility and maximality predicates. |
| Domain inference `N>1` | Theorem scope | Required for the requested positive proper divisor to exist; aligned with formal claims and canonical behavior, but not explicitly stated in the short prompt. |

The differential tests, composition check, and prose are supporting validation;
none is treated as a substitute for the reconstructed candidate `#Top` proofs.

### Decision

This is not `FAIL`: the source is pinned exactly, every positive claim rebuilds
and closes, the modular states compose, all result-bearing summaries are
truthfully defined, no rule bypasses real execution, and a fresh false result is
rejected for the expected reason.

I do not assign `PASS` because the requested generation-provenance record is
incomplete and because the final summary-to-natural-language maximum theorem is
an informal bridge rather than an explicit divisibility/maximality K claim.
Those are evidence/adequacy limitations, not soundness defects, so the proof
remains legitimate.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
