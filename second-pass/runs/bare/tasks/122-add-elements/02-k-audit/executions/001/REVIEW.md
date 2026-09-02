# Adversarial audit: 122-add-elements

The completed audit finds a real, freshly reconstructed, non-vacuous K proof of
the submitted program's own `-100 < value < 100` behavior.  It is not a proof
that the program meets the trusted HumanEval contract.  On the intended domain,
`arr=[-10], k=1` satisfies every stated constraint; the submitted program and
its K summary return `-10`, while trusted `canonical.py` returns `0`.

There is also a narrower formal-scope defect: `intAt(List,Int)` is marked
`[total]` despite non-exhaustive equations, and the proof depends on that
attribute.  I do not use that issue as an intended-integer-domain false-result
witness; the decisive intended-domain witness is the implementation/canonical
divergence above.

## 1. Input and provenance integrity

The rendered mode is `GENERATED_SEMANTICS`.  The trusted mount is consistent:
`/reference/reference-semantics` is absent, including as a symlink.  The only
trusted reference files are regular files:

- `/reference/canonical.py`
- `/reference/prompt.py`
- `/reference/py2mpy.py`

The candidate contains regular, non-symlinked copies of every required
generation artifact: `prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`,
`semantic.k`, `verification.k`, `spec.k`, `prove.sh`, `run-input.json`,
`metrics.json`, `codex-last.txt`, `codex-output.log`, and one structured JSONL
trace.  No required source/control/log/trace artifact is missing, mistyped, or
symlinked.  Candidate `prompt.py` and `py2mpy.py` are byte-identical to the
trusted mounted versions; their hashes also match the hashes claimed in
`run-input.json`.

The candidate additionally contains `semantic-kompiled/`,
`verification-kompiled/`, and `__pycache__/`.  These are extra derived artifacts,
not trusted proof inputs.  They were not copied or used.  There is no candidate
`spec-vacuity.k`; it was optional evidence, and a fresh reviewer mutation was
created in stage 6.

I read `run-input.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, and the structured trace only as untrusted generation
claims.  They claim a bare/generated-semantics run, exit 0, concrete results
`24` and `18`, and final `#Top`.  The logs also show that proof attempts without
`intAt [total]` became stuck on `#Ceil(intAt(A,I))`, after which `[total]` was
added.  Every material claim was checked independently below.

Evidence:

- [`00-mount-and-inventory.log`](evidence/00-mount-and-inventory.log)
- [`01-provenance-integrity.log`](evidence/01-provenance-integrity.log)
- [`04-untrusted-generation-claims.log`](evidence/04-untrusted-generation-claims.log)

Stage 1 result: integrity pass; no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Trusted contract

For a nonempty integer array `arr` with `1 <= len(arr) <= 100` and
`1 <= k <= len(arr)`, return the sum of the first `k` elements whose Python
decimal string has length at most two.  The documented example returns `24`
from `21 + 3`.

Trusted `canonical.py` implements:

```python
sum(elem for elem in arr[:k] if len(str(elem)) <= 2)
```

For integers, this includes `-9..99`.  The minus sign makes `str(-10)` three
characters, so `-10..-99` are excluded.  The prompt does not prohibit negative
integers.

### Submitted implementation and translation

The candidate iterates exactly the first `k` positions and adds an element when:

```python
-100 < value and value < 100
```

That condition includes `-99..99`, so it materially differs from the trusted
canonical predicate for every integer in `-99..-10`.

Using the trusted translator copied from `/reference/py2mpy.py`, I regenerated
`solution.mpy` from the scratch copy of `solution.py`.  It is byte-identical to
the submitted `solution.mpy` (same SHA-256
`c51f69d4c2834a4e00bf348ef1ede2dcee74c4d7623993bbe71b04bfa1c90206`).

The independent differential script imports the two entry points separately,
uses trusted `canonical.py` as oracle, and covers:

- the documented example;
- empty/out-of-domain probes;
- minimum and maximum array/prefix sizes;
- both sides of `-100` and `100`;
- the negative string-length boundaries `-9` and `-10`;
- exhaustive singleton values from `-150` through `150`;
- 100 deterministic generated arrays (seed 122).

It ran 417 cases, 415 within the documented domain, and exited 1 because 140
tested intended-domain cases diverged.  The minimal witness is:

```text
arr=[-10], k=1
candidate=-10
canonical=0
```

The all-boundaries case returned `-1` from the candidate and `108` from the
canonical implementation.  The documented positive example does agree at
`24`.  Finite test counts are evidence, not a universal proof; the source-level
predicate comparison establishes the complete divergence interval.

Evidence:

- [`02-translation-identity.log`](evidence/02-translation-identity.log)
- [`differential_test.py`](evidence/differential_test.py)
- [`03-differential-results.log`](evidence/03-differential-results.log)

Stage 2 result: **fail**.  The submitted program does not implement the trusted
contract on its intended domain.

## 3. Clean proof reconstruction

All candidate definitions and caches were ignored.  The source files needed for
execution were copied to `/tmp/audit-work/122-add-elements`; fresh output
definitions used reviewer-selected names.

The available independent toolchain is K v7.1.293.  Fresh reconstruction did
the following:

1. Compiled `semantic.k` with LLVM into
   `semantic-llvm-kompiled` (exit 0).  The compiler emitted a
   non-exhaustive-match warning for `intAt(List,Int) [function,total]`.
2. Ran the fresh concrete semantics on the documented example, a zero-iteration
   boundary, all predicate boundaries, and a prefix boundary.  Every K result
   matched an independent execution of the submitted Python function:
   `24`, `0`, `-1`, and `21`.
3. Compiled `verification.k` with Haskell into
   `verification-fresh-kompiled` (exit 0).
4. Proved `loop-invariant` alone: exit 0 and `#Top`.
5. Proved `add-elements-contract` with the already independently proved loop
   invariant marked as its trusted helper for that decomposition: exit 0 and
   `#Top`.
6. Ran the original complete claim set without filtering or trust flags: exit 0
   and `#Top`.

Filtering the entry claim alone also removes the circular loop helper and does
not represent its intended proof dependency.  The separately proved-helper
run plus the unmodified all-claims run checks both positive targets without
treating the candidate's prior `#Top` as evidence.

The generated semantics therefore executes the submitted candidate faithfully
on the normal and boundary cases tested.  In particular, K and candidate Python
both return the wrong-contract result on negative two-digit integers; concrete
agreement with the candidate is not agreement with the canonical program.

Evidence:

- [`05-toolchain.log`](evidence/05-toolchain.log)
- [`06-kompile-semantic-llvm.log`](evidence/06-kompile-semantic-llvm.log)
- [`concrete_semantics_test.sh`](evidence/concrete_semantics_test.sh)
- [`07-concrete-semantics-results.log`](evidence/07-concrete-semantics-results.log)
- [`08-kompile-verification-haskell.log`](evidence/08-kompile-verification-haskell.log)
- [`09-kprove-loop-invariant.log`](evidence/09-kprove-loop-invariant.log)
- [`11-kprove-all-positive.log`](evidence/11-kprove-all-positive.log)
- [`12-kprove-entry-with-proved-helper.log`](evidence/12-kprove-entry-with-proved-helper.log)

Stage 3 result: reconstruction pass under the candidate's generated theory.

## 4. Adequacy and real-program pinning

### Claims in plain language

`loop-invariant` starts at the submitted loop with environment:

```text
arr=A, k=K, total=T, i=I, value=V
```

and requires `0 <= I <= K <= size(A)`.  With the real return statement as the
continuation, it claims execution consumes the computation and stores:

```text
T + sumRange(A,I,K)
```

as the result.

`add-elements-contract` starts with the complete submitted program, an empty
environment, input cells `A,K`, and no result.  It requires:

```text
1 <= K <= size(A) <= 100
```

and claims the result is exactly:

```text
sumRange(A,0,K)
```

The postcondition is result-constraining.  Its result is not existential, free,
tautological, or guarded by a one-way implication.  The environment is allowed
to become an existential map, but that does not weaken the concrete result
cell.

### Real control flow and program identity

`solutionProgram` and `solutionLoop` are parse-time macros, not execution
shortcuts.  Using the fresh proof definition, I expanded both the submitted
`solution.mpy` and `solutionProgram` with `kast --expand-macros`.  The two
expanded KAST files are byte-identical.  The loop helper has the exact
post-initialization continuation reached by the real statement-sequencing
rules, including `exec(Return(Name("total")) .Stmts)`.

All actual assignments, list reads, conditionals, increments, loop tests, and
the return execute under `semantic.k`; `sumRange` does not replace the loop.

### Satisfiable witnesses and ground substitution

The entry precondition is satisfied by `A=[-10], K=1`.  Ground substitution
gives:

```text
sumRange([-10],0,1) = -10
candidate Python               = -10
trusted canonical Python       = 0
```

The loop precondition is satisfied, for example, by:

```text
A=[-10,21,4000], K=2, I=1, T=-10, V=-10
```

Its claimed ground result is `-10 + 21 = 11`.  Thus neither claim is vacuous.
The entry witness simultaneously exposes the fatal intent mismatch.

Evidence:

- [`13-real-program-pinning.log`](evidence/13-real-program-pinning.log)
- [`18-adequacy-witness.log`](evidence/18-adequacy-witness.log)

Stage 4 result: the proof pins the real submitted program and constrains its
result, but the constrained result is not the trusted task result.

## 5. Rule-by-rule static soundness review

The exhaustive inventory is in
[`rule-inventory.md`](evidence/rule-inventory.md).  It enumerates:

- all 15 local syntax/data/function declarations;
- the full configuration and cell roles;
- all 31 ordinary rules in `semantic.k`;
- both macro rules and all four mathematical function equations in
  `verification.k`;
- both reachability claims;
- the declaration/rule coverage of every constructor used by `solution.mpy`.

There are no local priority, `owise`, `[functional]`, `[simplification]`, or
`[concrete]` declarations, and no result-bearing opaque symbol with no defining
rules.

### Operational semantics

The configuration is sufficient for the submitted subset: computation,
bindings, immutable inputs, and a return result.  No heap, allocation, I/O,
exceptions, or call stack is needed by this single top-level, mutation-free-list
program.

The rules preserve the relevant behavior:

- the exact function entry binds `arr` and `k`;
- statement sequences execute left to right;
- assignments evaluate before environment update;
- loop guards are re-evaluated and true bodies complete before recurrence;
- `and` short-circuits;
- arithmetic, comparison, and subscript operands evaluate left to right;
- return stores the evaluated value and discards the remaining top-level
  continuation.

Rule heads for true/false branches and administrative continuations are
disjoint.  No local priorities are needed.  Map updates preserve other
bindings.  The loop returns to the stable configuration matched by the
circularity.  For valid integer arrays and `0 <= i < k <= len(arr)`, the two
`intAt` equations implement ordinary zero-based lookup by structural descent.

The generated language intentionally does not model Python slicing, generator
expressions, `str`, or `sum`, so it cannot execute trusted `canonical.py`
directly.  Minimal coverage is otherwise acceptable because every constructor
of submitted `solution.mpy` is declared and covered.

### Functions, totality, and summaries

`smallContribution` has disjoint, exhaustive integer guards and exactly matches
the submitted conditional.  `sumRange` has disjoint base/recursive guards and
advances `I` toward `K`.  It is a definitional RHS summary, not an operational
bridge: the actual loop still executes.

That same fact exposes the intent failure.  The summary equation:

```text
smallContribution(-10) => -10
```

truthfully describes the submitted branch but does not describe the trusted
canonical property, for which the contribution is `0`.  The false
intended-domain conclusion witness is the satisfying `[-10],1` entry state
documented above.  This is an implementation-to-intent/summary-to-property
failure, not a claim that the arithmetic equation is internally inconsistent.

`intAt(List,Int)` is declared `[function,total]`, but its two equations cover
only a nonempty integer-headed list at index zero and positive traversal through
integer items.  They do not cover empty lists, negative or out-of-range indices,
or non-integer list items.  Fresh LLVM compilation reports this exact
non-exhaustiveness.

Removing only `[total]` still builds, but the proof then fails on
`#Ceil(intAt(A,I))`; the successful proof therefore depends on the declaration.
The written formal precondition says only `A:List`, not that every item is an
`Int`.  `A=ListItem(true), K=1` satisfies the written entry inequalities, while
fresh concrete execution gets stuck at `intAt(ListItem(true),0)` with exit 113.
This witnesses a defect in the theorem's broad formal K scope.

The task's intended domain is integer arrays.  On that narrower domain, every
access made under the claim preconditions is in bounds, and structural
`intAt` is well-defined.  I found no false intended-domain result enabled by the
totality attribute itself.  Consistent with the audit rule requiring such a
witness, I classify it as an over-broad formal-scope/assumption gap rather than
using it as a second intended-domain unsound-rule verdict basis.  It remains a
real reason not to read the unqualified universal K `#Top` as self-justifying.

Evidence:

- [`rule-inventory.md`](evidence/rule-inventory.md)
- [`semantic-no-intat-total.k`](evidence/semantic-no-intat-total.k)
- [`16-kompile-no-intat-total.log`](evidence/16-kompile-no-intat-total.log)
- [`17-kprove-no-intat-total-expected-failure.log`](evidence/17-kprove-no-intat-total-expected-failure.log)
- [`19-intat-totality-formal-scope-witness.log`](evidence/19-intat-totality-formal-scope-witness.log)

Stage 5 result: ordinary execution rules and summaries faithfully characterize
the submitted program on intended integer inputs, but the answer summary is the
wrong task property; `intAt [total]` also leaves an explicit formal-scope
assumption gap.

## 6. Fresh non-vacuity test

No candidate mutation was trusted.  I created a fresh spec preserving the
genuine loop helper and changed the entry result obligation from:

```text
result(sumRange(A,0,K))
```

to:

```text
result(sumRange(A,0,K) +Int 1)
```

The mutation is demonstrably false at the satisfying input
`A=ListItem(21), K=1`: execution and `sumRange` yield `21`, while the target
requires `22`.

`kprove --dry-run` parsed and built the mutation successfully (exit 0).  The
actual proof exited 1 with `WarnStuckClaimState`; the residual explicitly shows
the failed implication between `x +Int 1` and `x`.  This is the expected unmet
result obligation, not a parser error, missing import, timeout, or unrelated
crash.

Evidence:

- [`spec-vacuity.k`](evidence/spec-vacuity.k)
- [`14-vacuity-build-dry-run.log`](evidence/14-vacuity-build-dry-run.log)
- [`15-vacuity-proof-expected-failure.log`](evidence/15-vacuity-proof-expected-failure.log)

Stage 6 result: pass.  The reconstructed proof is discriminating and
non-vacuous.

## 7. Proven versus assumed accounting

### What `#Top` establishes

Under the generated K semantics, imported K built-ins, and the local totality
declarations, the reconstructed reachability proof establishes partial
correctness of the exact submitted AST:

- from a loop state satisfying `0 <= I <= K <= size(A)`, terminating execution
  produces `T + sumRange(A,I,K)`;
- from the submitted entry program satisfying
  `1 <= K <= size(A) <= 100`, terminating execution produces
  `sumRange(A,0,K)`.

For intended integer arrays, the equations define `sumRange` as the sum of
elements in the prefix satisfying `-100 < element < 100`.  The proof is not a
termination proof.

### Trust and assumption ledger

| Boundary | Role and dependence | Assessment |
|---|---|---|
| K v7.1.293 and imported `INT`, `BOOL`, `LIST`, `MAP`, `MAP-SYMBOLIC` | Parsing, rewriting, integer/Boolean/list/map mathematics, and proof engine for both claims. | Normal low-level trust boundary. |
| Trusted `/reference/py2mpy.py` | Connects `solution.py` to `solution.mpy`. | Acceptable; fresh output is byte-identical. |
| `solutionProgram`/`solutionLoop` macros | Connect spec terms to the submitted constructor AST. | Formally syntactic and fresh expanded KAST is identical. |
| Generated operational rules | Connect constructor execution to a small Python-like model. | Audited rule by rule; concrete tests support only the tested normal/boundary executions. There is no independent universal CPython equivalence theorem. |
| `intAt [total]` | Supplies definedness of symbolic list lookup and is needed by both symbolic claims. | Concerning/over-broad. Equations are correct on valid integer-list accesses, but totality is false on the declared full domain and the written K precondition lacks an integer-list predicate. |
| `smallContribution` and `sumRange` | Mathematical summaries in the claims; no execution is skipped. | Internally well-defined on the intended claim uses and connected to the submitted loop by the non-vacuous proof. |
| Differential/concrete tests | Empirically compare candidate Python, canonical Python, and generated K on finite inputs. | Support only their tested bridges; not substitutes for the K proof. |
| Candidate prose, prior definitions, trace, and prior `#Top` | Generation claims. | Untrusted and not used as proof evidence. |
| Bridge from `sumRange` to trusted natural-language/canonical result | Needed for correctness of HumanEval 122. | **False.** `[-10],1` is a satisfying counterexample. |

### Decision

Fresh reconstruction, AST pinning, and non-vacuity all succeed.  Those facts
show that this is not a substituted-program or free-result trick.  They do not
repair the material contract error.  The proof establishes that the real
submitted program computes the wrong predicate, and the independent canonical
comparison supplies a concrete counterexample within the intended domain.

This is not the sort of thin or informal bridge limitation eligible for
`CONCERNS / LEGIT`: the required result itself is false for a legal input.
Accordingly, the candidate does not contain a legitimate partial-correctness
proof of the required HumanEval program.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
