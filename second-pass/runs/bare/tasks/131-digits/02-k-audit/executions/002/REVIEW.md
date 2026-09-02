# Independent adversarial review: HumanEval/131 `digits`

The candidate contains a legitimate, result-constraining partial-correctness
proof of the submitted program for the complete source-contract domain of
positive integers. Fresh builds and proofs succeed, the executed K term is
mechanically pinned to trusted retranslation of `solution.py`, and independent
body/result mutations fail for the expected reasons.

The result is `CONCERNS / LEGIT`, rather than an unqualified pass, because two
unguarded arithmetic rules in the individually generated semantics use K's
truncating/remainder operations for all integers and therefore disagree with
Python on negative dividends. No state reachable from this submitted program
under its `N > 0` precondition exercises that discrepancy. The concern is a
global reuse/evidence limitation, not a false-conclusion witness on the
intended domain.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- problem `131-digits`, condition `bare`;
- `record_layout = legacy-selected-stage1`;
- `semantics_mode = GENERATED_SEMANTICS`;
- no mounted reference semantics.

I read the launcher document, its `record_layout`, `container_paths`, hashes,
integrity fields, and campaign block before using any candidate claim. The
canonicalized `audit_campaign` object is exactly equal to
`/audit-campaign-lock.json`; the lock's SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
matching `/audit-input.json`.

All records required for `legacy-selected-stage1` are present as real regular
files and readable:

- `/run.json`, `/task.json`, `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`, `codex-last.txt`,
  `codex-output.log`, `prompt.txt`, and the JSONL trace;
- optional `/generation-evidence/usage.json`.

Historical `runtime-metrics.json` is absent, which this layout explicitly
allows. The trace contains 202 valid JSONL records. I inspected its event
inventory, tool-call sequence, intermediate failures, final build/proof run,
and final agent report solely as untrusted generation history.

Every launcher-recorded regular-file hash independently matches. The raw trace
hash matches `generation-result.json` and `invocation.json`; the independently
computed pipeline tree digest for the trace matches `usage.json`. The
candidate's independently computed pipeline tree digest is
`f9e51c3c3cc86687275131d5fd51a2b0d3cce3eecf3e867bb78131cf3a353e15`,
which matches all workspace hashes in `invocation.json` and
`generation-result.json`. Per-file candidate hashes and exact commands are in
[01-integrity.log](evidence/01-integrity.log).

There are no symlinks or unsupported nodes below `/candidate`,
`/generation-evidence`, or `/reference`. Candidate `prompt.py` and `py2mpy.py`
are byte-identical to `/reference/prompt.py` and `/reference/py2mpy.py`.
`/reference` contains only `canonical.py`, `prompt.py`, and `py2mpy.py`;
`/reference/reference-semantics` is correctly absent. Thus the trusted mounts
do not contradict `GENERATED_SEMANTICS`, and there is no audit-infrastructure
breach.

All source artifacts needed for execution were copied to
`/tmp/audit-work/131-digits`; no candidate-built definition or cache was copied
or reused.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract is:

> For a positive integer `n`, return the product of all odd decimal digits of
> `n`; return `0` when there is no odd digit.

The trusted canonical implementation scans the decimal string left-to-right,
multiplies odd digits, and tracks whether it saw any. Candidate `solution.py`
scans the same digits right-to-left using repeated `% 10` and `// 10`.
Accumulator `0` means “no odd digit yet”; the first odd digit replaces it and
later odd digits multiply it. Because decimal odd digits are never zero and
integer multiplication is commutative, this computes the same value. Its loop
terminates on every positive integer because nonnegative `n // 10` strictly
decreases while `n > 0`.

Trusted regeneration command:

```text
python3 /tmp/audit-work/131-digits/trusted/py2mpy.py \
  /tmp/audit-work/131-digits/candidate-src/solution.py \
  > /tmp/audit-work/131-digits/regenerated-solution.mpy
```

It exits 0. The regenerated and submitted `solution.mpy` are byte-identical
and share SHA-256
`2896980468c0242ec42a548502e6d02a49ccf9d6e86596c4a0483aa950519b80`.

The independent test [differential_test.py](evidence/differential_test.py)
loads the trusted canonical and candidate entry points as different modules.
It covers the three documented examples; one-digit odd/even cases; zero
digits; both accumulator branches; the no-iteration boundary `n=0` (outside
the formal positive domain); all positive integers `1..5000`; and 500
deterministically generated positive integers of 1 to 120 decimal digits.
All 5,524 executions agree. The serialized input-set SHA-256 is
`0a46cbcf6217eb40e31f5d4e9531032182bc81ac17245814f3d8eacebefd3596`.
See [02-translation-differential.log](evidence/02-translation-differential.log).
This is finite bridge evidence, not a substitute for the K proof.

## 3. Clean proof reconstruction

The installed `kompile`, `krun`, and `kprove` are K v7.1.293. From source in a
clean scratch build:

```text
kompile semantic.k --main-module SEMANTIC --syntax-module MPY-SYNTAX \
  --backend llvm --output-definition .../build/semantic-kompiled
```

exits 0. Fresh concrete execution through the generated semantics agrees with
both Python implementations on:

```text
0, 1, 4, 10, 11, 235, 2468, 10203,
999999999999999999999999999999999999999999999999999999999999
```

These cases cover a zero-iteration boundary, both conditional branches, first
and later odd digits, zero digits, all-even input, normal examples, and
unbounded integer arithmetic. The reviewer harness and output are
[concrete_semantics_test.sh](evidence/concrete_semantics_test.sh) and
[03-reconstruction.log](evidence/03-reconstruction.log).

The proof definition was independently rebuilt:

```text
kompile verification.k --main-module VERIFICATION \
  --syntax-module VERIFICATION --backend haskell \
  --output-definition .../build/verification-kompiled
```

It exits 0. The positive target:

```text
kprove spec.k --definition .../build/verification-kompiled \
  --spec-module SPEC
```

exits 0 and prints exactly `#Top`, closing both claims in `SPEC`. I also copied
the claims verbatim into a labeled audit module and selected the generalized
loop claim alone; it independently exits 0 with `#Top`. The end-to-end claim
intentionally depends on that loop circularity, so the complete two-claim
target is the relevant independent entry proof.

The fresh generated semantics therefore parses and executes every submitted
construct, and the fresh proof closes without any candidate cache.

## 4. Adequacy and real-program pinning

### Formal claims in plain language

The generalized loop claim assumes:

- `N >= 0`;
- the active computation is the exact submitted loop followed by arbitrary
  continuation `CONT`;
- current accumulator A and scratch digit D are arbitrary integers;
- the answer cell is preserved.

It concludes that the loop reaches `CONT` with `n = 0`, accumulator
`oddProductFrom(N,A)`, scratch
`finalScratchDigit(N,D)`, and the answer unchanged. This is the induction
circularity over the shrinking decimal quotient.

The entry claim assumes `N > 0` and initial n/accumulator/digit cells all zero.
It executes:

```text
Invoke(SolutionProgram, "digits", N)
```

and concludes empty computation, `n = 0`, accumulator and returned answer both
equal to `oddProduct(N)`, and the exact final scratch digit. The returned value
is thus constrained twice; it is neither fresh nor implied only one way.

### Program identity

`SolutionProgram`, `digitsCond`, and `digitsLoopBody` expand constructor for
constructor to the freshly regenerated `solution.mpy`. Running:

```text
CheckProgram(SolutionProgram, <regenerated solution.mpy>)
```

on the fresh proof definition reduces to `ProgramsMatch`. This is the allowed
mechanical constructor-level comparison, not reliance on an unregenerated
source filename. The claim then executes the exact body through ordinary
semantic rules; no program operation is summarized away.

A material mutation to the executed proof term changed the nonzero-accumulator
branch from multiplication to replacement. The mutated definition compiled,
but the unchanged target proof exited 1 with `WarnStuckClaimState` on the
failed equality between the correct multiplied fold and mutated replacement
fold. The concrete satisfying witness `N=35` gives 15 in the submitted program
and 3 in the mutated term. See
[verification-body-mutation.k](evidence/verification-body-mutation.k) and
[04-body-sensitivity.log](evidence/04-body-sensitivity.log).

### Satisfiable preconditions and concrete substitution

For the entry claim, `N=235` with:

```text
<k> Invoke(SolutionProgram,"digits",235) </k>
<n> 0 </n> <acc> 0 </acc> <digit> 0 </digit> <answer> .K </answer>
```

satisfies every precondition. Fresh K execution, candidate Python, and
canonical Python all return 15; separately evaluating `oddProduct(235)` in the
proof definition also yields 15. The same substitution checks yield 1, 0, and
3 for `N=1`, `4`, and `10203`.

For the helper claim, `N=0`, any integer A/D, any continuation, and any answer
is a satisfying base state; `N=235`, A=0, D=0 is a satisfying inductive state.

The formal domain is every mathematical/K integer `N > 0`, not a finite set,
fixed digit length, or bounded unrolling. It exactly matches the prompt's
positive-integer domain.

## 5. Rule-by-rule static soundness review

[07-rule-inventory.md](evidence/07-rule-inventory.md) enumerates every local
sort, syntax production, cell, computation item, `[function,total]`
declaration, ordinary rule, and claim. There are:

- 31 operational rules in `semantic.k`;
- 12 definitional/helper/test rules in `verification.k`;
- 2 reachability claims in `spec.k`;
- no other candidate K helper files;
- no opaque, simplification, concrete, priority, `owise`, or `functional`
  declarations.

Every constructor used in `solution.mpy` maps to declared syntax and real
execution rules: module/function/parameter, assignment, while, if, return,
integer/name lookup, binary `%`/`//`/`*`, and `>`/`==` comparison.

The operational review finds:

- `Invoke` matches a module containing exactly the named one-parameter
  function, repeats the same function name on call and binding, initializes
  every state cell, and then executes the actual body.
- Statement and expression evaluation is left-to-right.
- Reads and writes map exactly to `n`, `result`, and `digit`; no used name or
  operator is missing.
- Conditional and loop rule pairs have disjoint and exhaustive zero/nonzero
  guards. Comparison pairs have disjoint and exhaustive mathematical guards.
- The loop reevaluates its condition after each complete body execution.
- Return evaluates its expression, records the answer, and discards only the
  remaining function-body continuation, as Python return does here.
- There is no allocation, output, exception, heap, or other material state in
  this program to preserve.

The proof-local equations are also exhaustive and non-overlapping.
`addOddDigit` partitions even/odd digits and zero/nonzero accumulator;
`oddProductFrom` and `finalScratchDigit` partition `N <= 0` versus `N > 0` and
strictly descend for relevant positive N. `digitsCond`, `digitsLoopBody`, and
`SolutionProgram` are closed definitional expansions. `CheckProgram(P,P)` is a
ground structural-equality helper and does not occur in either target claim.

Most importantly, no operational bridge replaces a program-defined
computation with `oddProduct` or another oracle. The loop executes one real
iteration and the generalized reachability claim is the machine-checked
connection from that execution to the recursively defined summary. No fresh
or opaque symbol influences a branch or result.

### Nonfatal generated-semantics limitation

Rules S14 and S15 are unguarded over all K integers:

```text
I %Int J
I /Int J
```

K gives `-3 %Int 2 = -1` and `-3 /Int 2 = -1`; Python gives `-3 % 2 = 1`
and `-3 // 2 = -2`. Reproducible programs and outputs are
[negative-modulo.mpy](evidence/negative-modulo.mpy),
[negative-division.mpy](evidence/negative-division.mpy), and
[05-semantic-boundary.log](evidence/05-semantic-boundary.log).

This is not labeled an unsound rule for the submitted theorem: under the
entry precondition `N > 0`, every reached `n` and `digit` is nonnegative, and
all divisors are fixed positive 10 or 2. There is no false conclusion witness
for the real program on its intended domain. It is instead an over-broad
generated-language rule and reuse limitation. Similarly, comparisons produce
integer 0/1 rather than a distinct Python Boolean object, but the submitted
program uses them only for truth testing, where behavior agrees.

Under the benchmark's decision boundary, these globally broad but
task-domain-faithful rules warrant `CONCERNS / LEGIT`; they do not justify
`FAIL / NOT_LEGIT`.

## 6. Fresh non-vacuity test

I did not rely on any candidate mutation artifact. The fresh mutation
[spec-vacuity-audit.k](evidence/spec-vacuity-audit.k) preserves the program,
precondition, invariant, and all other destination cells but changes:

```text
<answer> .K => oddProduct(N) </answer>
```

to:

```text
<answer> .K => oddProduct(N) +Int 1 </answer>
```

`N=1` is a satisfying witness: real execution and `oddProduct(1)` give 1,
while the mutation demands 2. `kprove --dry-run` exits 0, establishing that
the mutation parses and builds. The actual proof exits 1 with
`WarnStuckClaimState`; its residual contains the unmet equality:

```text
oddProductFrom(...) +Int 1 #Equals oddProductFrom(...)
```

This is the expected reachable result obligation, not a parser error,
timeout, unrelated crash, or unreachable mutation. Exact commands and bounded
output are in [06-false-mutation.log](evidence/06-false-mutation.log).

## 7. Proven versus assumed accounting

### What the successful K proof establishes

Under the fresh `VERIFICATION` definition, for every K integer `N > 0`, if the
exact submitted/retranslated function is directly invoked from the specified
initial cells and reaches a return, its returned answer and final accumulator
are:

```text
oddProductFrom(N, 0)
```

where the recursive equations inspect each base-10 digit, ignore even digits,
use the first odd digit as the initial nonzero product, multiply subsequent
odd digits, and return zero if none exists. The loop claim establishes this
summary by real operational execution, not assumption. This is a universal
partial-correctness result over unrestricted positive integers.

### Trust ledger

| Boundary | Effect and dependents | Judgment/evidence |
|---|---|---|
| K reachability logic, compiler, Haskell/LLVM backends | All builds, execution, and proof closure | Necessary low-level trusted computing base; versions and fresh outputs recorded. |
| K `Int` multiplication, comparison, Boolean guards, and nonnegative division/remainder | Operational semantics and mathematical fold | Acceptable standard built-ins on the reached nonnegative domain. Negative global mismatch is explicitly excluded and causes the concern status. |
| Trusted `py2mpy.py` | Python AST to submitted constructor tree | Benchmark-designated trusted input; byte-identical candidate copy and byte-identical fresh regeneration. No hidden normalization. |
| Direct `Invoke` harness | Connects the closed one-function module/call to body execution and cells | Audited narrow semantic bridge: binding is pinned by repeated name and literal parameter, body is not replaced, and every material cell/control effect is modeled. |
| Generated Python-subset semantics | Connects constructor execution to Python behavior | Exhaustive rule audit plus normal/boundary concrete comparisons. Faithful for every construct/state reachable by this fixed program; not claimed as general Python semantics. |
| `oddProductFrom`, `addOddDigit`, `finalScratchDigit` | Formal postcondition and invariant | Exhaustive truthful equations; loop reachability claim supplies the universal execution connection. They are not opaque or empirical oracles. |
| Natural-language/canonical bridge | Identifies the recursive fold with “product of odd decimal digits, else zero” | Direct mathematical inspection plus 5,524 independent differential cases. The finite tests support but do not replace the K proof. |

Excluded behavior is explicit: `N <= 0`, non-integer Python values, other
programs or language constructs, Python object identity/types beyond the used
integer subset, and negative-operand floor/modulo behavior. None is part of
the source contract or reachable real-program theorem.

Gate summary:

- Real-program soundness and non-vacuity: **PASS**.
- Intent/domain adequacy: **PASS**; no material narrowing.
- Evidence/auditability: **PASS with documented trust limitation**.

The proof is therefore legitimate. The only remaining limitation is nonfatal
and lies outside the submitted theorem's reachable domain.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
