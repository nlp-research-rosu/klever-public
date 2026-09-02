# Independent adversarial review — 139-special-factorial

## Executive decision

The candidate contains a legitimate, non-vacuous partial-correctness proof of
the submitted program under the supplied MPY semantics. The proof executes the
exact translated function body; it does not replace the call, loop, return, or
state changes with a proof-local bridge. Its only proof-local extensions are
ordinary recursive definitions of factorial and the product of factorials.
Their equations are disjoint, exhaustive over mathematical integers, and
descending on the positive domain. The actual loop invariant connects those
summaries to execution.

I assign `CONCERNS / LEGIT`, rather than `PASS / LEGIT`, for two evidence
limitations that do not make a false conclusion provable:

1. `/candidate/run-input.json`, `metrics.json`, `codex-last.txt`, and
   `codex-output.log` are absent, and no structured generation trace is present.
2. The final bridge from the supplied MPY model and the recursive
   `specialFactorial` summary to the human-facing Python description rests on
   the trusted supplied semantics, ordinary mathematical interpretation, and
   finite differential/concrete evidence. It is not a separate K theorem about
   CPython or a separate closed-form product definition.

No candidate rule is alleged unsound, so there is no false-conclusion witness
to report for an unsoundness finding.

## 1. Input and provenance integrity

Status: **integrity PASS; provenance CONCERN**.

The rendered mode is `SUPPLIED_SEMANTICS`, and
`/reference/reference-semantics` is present as required. The infrastructure
therefore does not contradict the rendered mode.

The reviewer-authored recursive comparator checked every relative path with
`lstat`, did not follow symlinks, compared entry types, rejected candidate
symlinks, and SHA-256-compared all regular files. It found 26 entries in each
tree and zero differences:

- no missing, additional, changed, mistyped, or symlinked entry under
  `/candidate/reference-semantics`;
- byte identity between `/candidate/prompt.py` and `/reference/prompt.py`;
- byte identity between `/candidate/py2mpy.py` and
  `/reference/py2mpy.py`.

The prompt hash is
`be0a59f5cf0d2c13ca98ace59ca3a5bf4b8c4a153d42450c7cf6abb87d22d0c8`;
the translator hash is
`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.
Evidence and exact statuses are in
[`stage1_integrity.log`](evidence/stage1_integrity.log); the comparison program
is [`integrity_compare.py`](evidence/integrity_compare.py).

The following requested provenance artifacts are missing:

- `/candidate/run-input.json`;
- `/candidate/metrics.json`;
- `/candidate/codex-last.txt`;
- `/candidate/codex-output.log`.

No trace-like path (`*trace*`, `*.jsonl`, or `*trajectory*`) exists under the
candidate. The additional non-proof artifacts are the regular files
`run.py`, `run.mpy`, and `prove.sh`, plus a regular `__pycache__` directory.
They were treated only as untrusted evidence. No candidate compiled K
definition or K cache was present or reused.

## 2. Program fidelity and candidate-versus-canonical checks

Status: **PASS**.

The trusted contract says that, for an integer `n > 0`, the result is

`n! * (n-1)! * ... * 1!`,

with `special_factorial(4) == 288`. The trusted canonical program maintains
the current factorial while iterating from 1 through `n`, multiplying each
cumulative factorial into the result.

The submitted `solution.py` implements the same recurrence with a `while`
loop:

- initially `factorial = result = i = 1`;
- while `i <= n`, set `factorial *= i`, then `result *= factorial`, then
  increment `i`;
- return `result`.

On the intended positive-integer domain, this yields the stated product.
For the out-of-domain zero/negative boundary, both implementations return 1
because their loops execute zero times; that observation does not broaden the
formal domain.

The trusted translator regenerated `solution.mpy` from the scratch copy of
`solution.py`. `cmp` exited 0 and both files had SHA-256
`31cb7e21f905df1583a395328f21ae7897b025872a95b95d4b016f75f73b3628`.
The exact commands are in
[`stage2_fidelity.log`](evidence/stage2_fidelity.log).

The independent differential program
[`differential_test.py`](evidence/differential_test.py) imported the trusted
canonical entry point and the scratch copy of the submitted entry point under
different module names. It covered:

- `-5..40` exhaustively, including the empty/zero-iteration and loop-entry
  boundaries;
- the prompt example and expected values for `1..6`;
- named medium/large values 25 and 100;
- 40 deterministic generated inputs from seed `139_20260724`, up to 157.

There were 72 unique inputs, zero canonical/submitted mismatches, and zero
documented-expected-value failures. These are finite bridge evidence, not a
substitute for the K proof.

## 3. Clean proof reconstruction

Status: **PASS**.

All candidate source artifacts needed for execution were copied to
`/tmp/audit-work/139-special-factorial`. No candidate-built definition was
available. Both K definitions were rebuilt from source with K v7.1.337.

The concrete definition was built with:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

It exited 0. `krun run.mpy --definition runtime-kompiled --output pretty`
also exited 0 with final `<k> .K </k>`, empty stack, `NoExc`, and exit code 0.
The LLVM build issued non-exhaustive warnings for fixed-semantics functions
outside this program's path; none is used by the target.
See [`stage3_concrete_build.log`](evidence/stage3_concrete_build.log) and
[`stage3_concrete_run.log`](evidence/stage3_concrete_run.log).

The proof definition was built with:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

It exited 0. Positive proof results were:

- helper loop selected alone: exit 0 and `#Top`
  ([log](evidence/stage3_prove_loop.log));
- entry and its declared helper selected explicitly: exit 0 and `#Top`
  ([log](evidence/stage3_prove_entry_with_dependency.log));
- the complete submitted spec, proving both claims: exit 0 and `#Top`
  ([log](evidence/stage3_prove_all.log)).

For transparency, selecting only `SPEC.special-factorial-correct` removes the
loop circularity it depends on. That altered selection unrolled to a backend
decision residual and exited 1
([diagnostic log](evidence/stage3_prove_entry.log)). It is not the submitted
proof context: the helper is independently proved, and the explicit
entry-plus-helper and complete-spec invocations both close. The dependency is
one-way; the helper proof does not depend on the entry claim.

## 4. Adequacy and real-program pinning

Status: **PASS**.

### Entry claim in plain language

For every mathematical integer `N > 0`, start from the supplied initial module
configuration and load:

1. the submitted `special_factorial` definition; then
2. a real assignment `answer = special_factorial(N)`.

If execution terminates normally, the continuation is empty, the current
environment is restored to module scope 0, the heap and stack are empty, there
is no pending return or exception, and the module map binds `answer` to
`specialFactorial(N)`. The existential `?REST` permits the expected function
closure and other irrelevant module bindings; it does not make `answer` free.

### Loop claim in plain language

At the actual `#while` control point, assume `N >= 1`,
`1 <= I <= N+1`, and the current local frame contains:

- `n = N`;
- `factorial = factorial(I-1)`;
- `result = specialFactorial(I-1)`;
- `i = I`.

The claim preserves the arbitrary continuation and all framed cells, exits the
loop with `i = N+1`, and fixes the locals to `factorial(N)` and
`specialFactorial(N)`. At `I <= N`, one real loop iteration establishes the
same invariant at `I+1`; at `I = N+1`, the real condition is false.

The reviewer balanced and extracted the sole `FuncDef(...)` constructor from
submitted `solution.mpy` and from `spec.k`. After whitespace normalization,
the constructors were equal and both had SHA-256
`f5079cd641097ba17bd7a80f85f5cb079893b67020fb648364b2eb229eb4545d`.
See [`pinning_check.py`](evidence/pinning_check.py) and
[`stage4_adequacy.log`](evidence/stage4_adequacy.log).

A satisfying entry state is obtained with `N=4` and the exact initial cells
written in the claim: environment 0; empty module scope with parent -1;
`builtinsScope` at -1; `scopeLoc=1`; empty heap/stack; `noRet`; `NoExc`; and
exit code 0. A loop witness is `N=4, I=1, L=1`, with the function frame parented
to module scope 0.

Substitution checks gave:

| N | Claimed summary | Trusted canonical | Submitted Python |
|---:|---:|---:|---:|
| 1 | 1 | 1 | 1 |
| 2 | 2 | 2 | 2 |
| 4 | 288 | 288 | 288 |
| 6 | 24883200 | 24883200 | 24883200 |
| 10 | 6658606584104736522240000000 | same | same |

Reviewer-authored concrete MPY execution also stored
`answer_n1=1`, `answer_n2=2`, `answer_n4=288`, and
`answer_n6=24883200` in module scope with normal termination. The source is
[`ground_driver.py`](evidence/ground_driver.py).

## 5. Rule-by-rule static soundness review

Status: **PASS**.

[`rule_inventory.tsv`](evidence/rule_inventory.tsv) is the exhaustive,
reviewer-generated ledger. It identifies each item by file and line, hashes the
complete normalized sentence, gives a bounded preview, records attributes and
program relevance, and gives an assessment. It contains:

- 699 rules: 695 fixed supplied-semantics rules and 4 proof-local equations;
- 229 syntax declarations;
- 5 contexts and 1 configuration;
- 2 reachability claims;
- every `function`, `total`, `symbol`, `no-evaluators`, `[concrete]`,
  priority, `owise`, strictness, and macro occurrence;
- module/import/require structure.

There are no `[simplification]` or `[functional]` declarations. The fixed tree
contains 45 priority-rule items, 36 `[concrete]` rule items, and 25 symbol
declarations. Twenty-two symbols explicitly use `no-evaluators`. Every such
item is in the trusted, byte-identical supplied tree and is unreachable from
this integer/loop-only target.

The ledger makes an explicit decision for every rule. All 695 fixed rules are
accepted at the selected supplied-semantics level; static review found no
false-conclusion witness on the intended program path. The four local
equations are accepted as sound definitional equations. The detailed
construct-to-rule map is
[`program_rule_map.md`](evidence/program_rule_map.md), and inventory commands
and attribute scans are in
[`stage5_static_checks.log`](evidence/stage5_static_checks.log).

The program-path review found:

- module and statement sequencing execute the submitted body in order;
- the function rule stores the exact body as a closure;
- call routing looks up that closure, evaluates the integer argument, creates
  and later pops a real frame, and resumes the captured caller continuation;
- `Assign` and `AugAssign` use current-scope updates, with strict RHS
  evaluation; all targets here are simple names;
- comparison contexts evaluate the left and then right integer operands and
  dispatch `<=` to `<=Int`;
- `While` reevaluates the actual condition on every iteration and sequences
  the actual body before its loop marker;
- the first multiplication updates `factorial`, so the second multiplication
  reads the updated value, matching Python;
- return evaluates `result`, sets the return state, pops only the active call
  frame, and resumes the caller's assignment.

Proof-local inventory:

1. `factorial(Int) [function,total]`.
2. `factorial(N) => 1` when `N <= 0`.
3. `factorial(N) => factorial(N-1) * N` when `N > 0`.
4. `specialFactorial(Int) [function,total]`.
5. `specialFactorial(N) => 1` when `N <= 0`.
6. `specialFactorial(N) => specialFactorial(N-1) * factorial(N)` when
   `N > 0`.

For each function, the two guards are disjoint and exhaustive over `Int`.
Positive recursion strictly decreases to the base case. The negative extension
to value 1 is harmless because entry and loop claims use only nonnegative
summary arguments. No local rule matches `<k>`, calls, loops, return, bindings,
frames, heap, or state. There is no priority, opacity, oracle, answer-encoding
operational rewrite, or execution bypass in `verification.k`.

`specialFactorial` is result-bearing, but it is a definitional summary rather
than an operational bridge: it never replaces program evaluation. The
independently proved loop claim is the universal connection from actual fixed
loop execution to the summary-valued invariant. The entry claim then connects
the actual call/return path to the result. No circular use of an unconstrained
oracle occurs.

## 6. Fresh non-vacuity test

Status: **PASS**.

The fresh mutation
[`spec-audit-vacuity.k`](evidence/spec-audit-vacuity.k) preserves the exact
program and genuine loop helper, but changes only the entry destination to:

```text
"answer" |-> specialFactorial(N) +Int 1
```

`N=4` is a satisfying witness: execution returns 288, while the mutation
requires 289.

The mutation dry-run built successfully (exit 0), proving that the test was not
a parser/import failure
([build log](evidence/stage6_mutation_build.log)). The real proof exited 1 with
`WarnStuckClaimState`; the backend said the destination term unified but the
condition implication failed. Its residual requires the actual summary plus 1
to equal the actual summary
([proof log](evidence/stage6_mutation_proof.log)). This is the expected unmet
result obligation, not a timeout, crash, unreachable mutation, or unrelated
failure.

## 7. Proven versus assumed accounting

Status: **formal proof PASS; evidence/intent bridge CONCERN**.

### What is formally proved

Conditional on the supplied K definition and K's reachability logic, for every
`N:Int` with `N > 0`, normal terminating execution of the exact submitted
function in the entry harness binds `answer` to the recursively defined product
`specialFactorial(N)`. The real loop establishes the cumulative-factorial
invariant, the real return value flows through the call frame, and the
postcondition fixes that observable value. The false off-by-one result is
rejected.

This is partial correctness. It does not independently prove CPython
termination, resource bounds, behavior for `N <= 0`, non-integer inputs, or
behavior outside the MPY subset.

### Trusted primitives and assumptions

- **K implementation and logic:** K v7.1.337, generated strictness machinery,
  reachability/circularity handling, matching, and the Haskell/LLVM backends.
- **K built-ins used by this theorem:** unbounded `Int`; `+Int`, `-Int`,
  `*Int`, `<=Int`, `>Int`, and `>=Int`; Boolean conjunction/negation; maps,
  lists, strings used as scope keys, and K sequencing. This is an acceptable
  low-level theorem-prover boundary.
- **Supplied MPY semantics:** the exact trusted `/reference/reference-semantics`
  tree. Its target-reachable rules are audited above. This is the selected
  semantics level, not a candidate proof extension.
- **Trusted front end and source contract:** `/reference/py2mpy.py` and
  `/reference/prompt.py`, byte-matched to the candidate copies.
- **Trusted executable oracle for finite checks:** `/reference/canonical.py`
  and CPython. These support only the tested Python bridge.

The 25 fixed-semantics symbol declarations are:

`sortVS`, `sortKeyVS`, `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`,
`floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`,
`eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`,
`sqrtF`, and `md5hexCodes`.

All are outside the submitted program's syntax and data path; none affects its
condition, control, state, returned value, summary, or postcondition. Their
opacity/concrete interpretation is therefore an acceptable unused fixed
boundary, not a smuggled correctness conclusion.

### Empirical and informal bridges

- Byte-identical trusted translation proves provenance of `solution.mpy` from
  `solution.py`, not semantic equivalence of MPY and all of CPython.
- The 72-input differential run supports equivalence of submitted and
  canonical Python on those inputs only.
- Concrete K executions support the supplied-semantics/Python bridge on the
  recorded ground cases only.
- The reading of the recursive equations as `1! * 2! * ... * n!`, and hence as
  the prompt's reversed product, is ordinary mathematics. It is sound and
  directly reflected by the equations, but is not stated as a separate K
  product theorem.
- Missing generation/provenance records limit historical auditability but do
  not affect the fresh reconstruction, program identity, or non-vacuity
  results.

These limitations justify `CONCERNS`, while the reconstructed proof remains
legitimate.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
