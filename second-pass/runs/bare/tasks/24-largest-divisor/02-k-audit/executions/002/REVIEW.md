# Independent adversarial review: 24-largest-divisor

This review was performed from the launcher-owned mounts and fresh scratch
builds. Candidate prose, prior `#Top` output, compiled artifacts, and generation
traces were treated only as untrusted claims. The proof theory is sound for its
stated precondition, but the entry theorem materially narrows the HumanEval
source-contract domain from `int` to `n > 1`. Under the benchmark-specific
decision rule, that adequacy failure makes the submitted proof not legitimate
for the requested contract.

## 1. Input and provenance integrity

### Declared layout and campaign

`/audit-input.json` declares:

- problem `24-largest-divisor`;
- generation condition `bare`;
- `record_layout` `legacy-selected-stage1`;
- `semantics_mode` `GENERATED_SEMANTICS`; and
- no mounted reference-semantics tree.

I read `/audit-input.json`, used only its `container_paths` values for mounted
inputs, and compared `/audit-campaign-lock.json` structurally with the
`audit_campaign` object. They are equal. The lock's independent SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
exactly the recorded value.

For the declared legacy-selected layout I read and checked:

- `/run.json`;
- `/task.json`;
- `/generation-result.json`;
- `/generation-evidence/invocation.json`;
- `/generation-evidence/metrics.json`;
- `/generation-evidence/usage.json` (present and therefore inspected);
- `/generation-evidence/codex-last.txt`;
- the complete `/generation-evidence/codex-output.log`;
- `/generation-evidence/prompt.txt`; and
- all 244 JSONL records in the sole file below
  `/generation-evidence/codex-trace/`.

Historical `runtime-metrics.json` is absent, but it is not required for this
legacy-selected layout. The required records are regular readable files (or,
for the trace, a regular readable directory), not symlinks. All
launcher-recorded file hashes checked match. The full checks and per-candidate
file hash inventory are in
[`01-provenance.log`](evidence/01-provenance.log). The trace was parsed in full;
its file hash is
`5399cc1f430f4e60f83dc5929e968c452f1a6c7dea6a5429a00894c3703fc77c`
and its structured summary is in
[`02-structured-trace.log`](evidence/02-structured-trace.log). The complete
10,993-line generation output was read and summarized in
[`18-generation-log-summary.log`](evidence/18-generation-log-summary.log).
Those generation records claim prior proof success, but no audit conclusion
below depends on that claim.

### Trusted-input checks and semantics boundary

The following independent hashes match `/audit-input.json`:

| Mounted artifact | SHA-256 |
|---|---|
| `/reference/prompt.py` and `/candidate/prompt.py` | `3bc8bf3f66a3b5e171a358bbd5f33fba1a5d16ea65459198757dcb662dbaaac2` |
| `/reference/py2mpy.py` and `/candidate/py2mpy.py` | `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16` |
| `/reference/canonical.py` | `7a164aecc7bc236de8f23b42963d5ee1e4053af79d2d6bcbb4c05da0742fe21c` |
| generation prompt | `4fbd8d83152646045c82c9b1c86a3c0c9bf686de949fcbf8c3eff6755a261d9e` |
| generation metrics | `981a0095d9bdeebd870acfaa0598d5a53af337b7491886ab1838356a3d671806` |
| generation usage | `2dbf9ae7e99039e0e2796e9abe1aedf9cfd4ca28be2f2f94fd8b1f53818db673` |

Direct byte comparisons of candidate prompt and translator against the trusted
mounts succeed. `/reference/reference-semantics` does not exist, as required in
`GENERATED_SEMANTICS` mode. The candidate contains no `reference-semantics`
tree to masquerade as a supplied definition. There is therefore no
infrastructure breach and the candidate can be judged.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract and implementations

The trusted prompt declares:

```python
def largest_divisor(n: int) -> int:
```

and asks for “the largest number that divides `n` evenly, smaller than `n`.”
The only example is `largest_divisor(15) == 5`. It states no positivity or
lower-bound precondition.

The trusted canonical implementation searches `reversed(range(n))` and returns
the first `i` with `n % i == 0`. The submitted implementation starts
`divisor = n - 1`, decrements while it is not a divisor, and returns the first
divisor found. These are equivalent descending searches for `n > 1`.

Using the trusted translator copied to scratch, I ran:

```text
python3 py2mpy.py solution.py > regenerated.mpy
sha256sum solution.mpy regenerated.mpy
cmp -s solution.mpy regenerated.mpy
```

Both files have SHA-256
`dfeae40e927213369b88e91ab649f8cceb179f11256be1094e3ec8a8b8673a06`;
`cmp` exits 0. See
[`03-translation.log`](evidence/03-translation.log).

### Independent differential test

[`differential_test.py`](evidence/differential_test.py) imports the trusted
canonical and scratch candidate through separate module loaders. It checks the
documented example; zero-iteration, one-or-more-iteration, prime, composite,
square, and other branch boundaries; then every integer from 2 through 2000.
There are zero mismatches on `2..2000`.

The same script deliberately checks the boundary outside the proof
precondition:

| `n` | Trusted canonical | Submitted Python |
|---:|---|---|
| 1 | raises `ZeroDivisionError` | raises `ZeroDivisionError` |
| 0 | returns `None` | returns `-1` |
| -1 | returns `None` | did not terminate within 0.25 s |
| -2 | returns `None` | did not terminate within 0.25 s |

The exact command, exit 0 for the in-formal-domain oracle comparison, and all
results are in [`04-differential.log`](evidence/04-differential.log). The
timeouts are finite observations, not universal divergence proofs. The
`n = 0` return mismatch is a direct terminating witness.

Thus source-to-source fidelity is strong on `n > 1` but is not fidelity over
the unqualified annotated `int` domain.

## 3. Clean proof reconstruction

Only these source artifacts were copied into `/tmp/audit-work/src`:
`solution.py`, `solution.mpy`, `semantic.k`, `verification.k`, `spec.k`, and
`prove.sh`, plus the trusted translator. No candidate-built definition, K
cache, or generated proof output was copied or reused.

### Fresh generated-semantics build and concrete execution

The LLVM definition was rebuilt with:

```text
kompile --backend llvm semantic.k --main-module MPY \
  --syntax-module MPY-SYNTAX --output-definition llvm-kompiled
```

It exits 0; see
[`05-kompile-llvm.log`](evidence/05-kompile-llvm.log).

Fresh `krun` executions for `n = 2, 3, 4, 15, 25, 101` all reach `.K`; their
result cells are respectively `1, 1, 2, 5, 5, 1`, exactly matching independent
Python execution. These cover a loop with zero iterations (`n = 2`), immediate
and delayed exits, prime descent to one, composites, and a square. See
[`06-krun-concrete.log`](evidence/06-krun-concrete.log).

At excluded boundary `n = 1`, LLVM's `modInt` hook crashes on modulus zero
rather than modeling Python's `ZeroDivisionError`. At `n = 0`, K and submitted
Python both return `-1`. See
[`07-krun-excluded-boundary.log`](evidence/07-krun-excluded-boundary.log).
This exception-model gap is unreachable under the theorem's `N > 1`
precondition; it is nevertheless relevant to the adequacy of imposing that
precondition.

### Fresh proof build and positive claims

The Haskell proof definition was rebuilt with:

```text
kompile --backend haskell verification.k --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

It exits 0; see
[`08-kompile-haskell.log`](evidence/08-kompile-haskell.log).

The loop claim was selected independently using its correct generated CLI
label:

```text
kprove spec.k --definition verification-kompiled --spec-module SPEC \
  --claims SPEC.largest-divisor-loop-contract --output pretty
```

It exits 0 and prints exactly `#Top`; see
[`09b-kprove-loop.log`](evidence/09b-kprove-loop.log).

The end-to-end claim depends on the loop claim as a circularity. Filtering the
spec to only the end-to-end label removes that required auxiliary claim, so
such a filtered run is not the submitted target proof. I retained the
deliberately interrupted diagnostic in `10-kprove-entry.log`. The correct fresh
target command includes both claims:

```text
kprove spec.k --definition verification-kompiled \
  --spec-module SPEC --output pretty
```

It exits 0 and prints exactly `#Top`; see
[`10b-kprove-all.log`](evidence/10b-kprove-all.log). Consequently both positive
claims close under the freshly rebuilt submitted theory.

## 4. Adequacy and real-program pinning

### Plain-language meaning of the claims

`largest-divisor-loop-contract` starts at the actual submitted `while` loop
with a subsequent actual `return divisor`. Its state contains `n = N` and
`divisor = D`. Its precondition says:

- `N > 1`;
- `0 < D < N`; and
- every integer strictly above `D` through `N - 1` has already been ruled out
  as a divisor.

On termination it requires the returned and final `divisor` value to be
positive, below `N`, to divide `N`, and to have no larger divisor below `N`.
This is the descending-search loop invariant and result condition.

`largest-divisor-natural-contract` starts with a `Module(FuncDef(...))` term.
Its only precondition is `N > 1`. It initializes an empty environment, executes
the function body, and requires the final result to satisfy the same
largest-positive-proper-divisor predicate.

### Exact program term and control flow

[`compare_program_term.py`](evidence/compare_program_term.py) extracts the
balanced `Module(...)` constructor from the entry claim and compares it
mechanically, modulo whitespace only, with regenerated `solution.mpy`. The
normalized terms are exactly equal; see
[`11-program-pinning.log`](evidence/11-program-pinning.log). The term includes:

- the binding `largest_divisor(n)`;
- initialization `divisor = n - 1`;
- the `% != 0` guard;
- decrement by one;
- the `while` body; and
- `return divisor`.

No typing import or other material source construct is omitted. The loop claim
has the exact same loop and immediate return continuation reached by this
entry body. The semantics executes initialization, every guard, every
decrement, and the return; no proof rule replaces the program body with a
summary.

The entry's right-only `?RESULT` is existential but constrained in three
independent ways: it is the final environment value, it is the result cell
value, and it must satisfy `isLargestProperDivisor`. It is neither free nor
tautological.

### Satisfiable states and ground substitution

For the loop claim, `N = 15, D = 14` satisfies every precondition: the skipped
interval `15..14` is empty. For the entry claim, `N = 15` satisfies `N > 1`.
Both trusted canonical and submitted Python return 5, and 5 satisfies the
expanded K postcondition. The executable witness check is
[`claim_witnesses.py`](evidence/claim_witnesses.py), with output in
[`12-claim-witnesses.log`](evidence/12-claim-witnesses.log).

### Adequacy failure

The proof establishes the intended result only under `N > 1`. Neither
`/reference/prompt.py` nor its function signature states that precondition; the
declared input type is simply `int`. This is not a finite-testing complaint:
`n = 0` is a concrete annotated-domain input on which the generated
implementation terminates, the theorem has no instance, and the trusted
canonical and generated implementations return different values.

One could infer from the mathematical task and the canonical's failure at
`n = 1` that HumanEval's tests were intended to use numbers above one. That is
an informal reconstruction of an unstated precondition, not part of the
mounted source contract. The benchmark instruction specifically maps a
materially narrowed HumanEval source-contract theorem to `FAIL / NOT_LEGIT`.
Accordingly, the sound restricted theorem is not adequate for the required
unqualified contract.

## 5. Rule-by-rule static soundness review

The raw declaration inventory is preserved in
[`17-static-inventory.log`](evidence/17-static-inventory.log). There are no
additional helper K files.

### Syntax, attributes, and configuration inventory

`MPY-SYNTAX` declares:

- `Pgm`: `Module(Stmts)`;
- `Params`: one string parameter;
- `Expr`: `Int`, `Name`, `BinOp`, and one-link `Compare`;
- `CmpOp`: an operator string plus comparator expression;
- `Stmt`: `FuncDef`, `Assign`, `While`, `If`, and `Return`; and
- `Stmts`: a juxtaposed list of statements.

The constructors `Module`, `Params`, `IntExpr`, `Name`, `BinOp`, `Compare`,
`CmpOp`, `FuncDef`, `Assign`, `While`, `If`, and `Return` have only `[symbol]`
attributes. Symbols do not assert semantic equations.

`MPY` additionally declares result marker `noResult`, continuation markers
`whileBranch` and `branch`, and functions `envInt`, `evalInt`, and `evalBool`.
The configuration has exactly the state used by the program:

- `<k>` for computation;
- `<arg>` for the externally supplied integer argument;
- `<env>` for local bindings; and
- `<result>` for the returned value.

`VERIFICATION` declares three `[function]` predicates:
`noDivisorFrom`, `isLargestThrough`, and `isLargestProperDivisor`.

There are no `[total]`, `[functional]`, `[simplification]`, `[concrete]`,
`[owise]`, strictness, priority, or trusted/opaque declarations. There are no
proof-local operational rules in `spec.k`, only the two reachability claims.

Every constructor in `solution.mpy` is declared: `Module`, `FuncDef`, `Params`,
`Assign`, `Name`, `BinOp("-")`, `Int`, `While`, `Compare`,
`BinOp("%")`, `CmpOp("!=")`, and `Return`. Each used constructor also has the
operational behavior inventoried below.

### `semantic.k` rules

1. **`envInt`.** `envInt(ENV, X)` returns the map value at `X` cast to `Int`.
   Lookup is partial when the key is absent or has another sort. The actual
   module rule binds `n`, initialization binds `divisor`, and all later lookups
   are therefore defined. It neither fabricates nor constrains a result.

2. **Integer literal.** `evalInt(Int(I), _) => I` is the direct meaning of an
   integer constructor and does not read state.

3. **Name lookup.** `evalInt(Name(X), ENV) => envInt(ENV, X)` delegates exactly
   to the environment lookup above.

4. **Subtraction.** The `BinOp("-")` equation recursively evaluates both pure
   operands and applies unbounded K integer subtraction. For the submitted
   expression subset this agrees with Python integer subtraction.

5. **Modulo.** The `BinOp("%")` equation recursively evaluates both pure
   operands and applies K `modInt`. Throughout every state admitted by the
   proof, the divisor is positive, so this agrees with Python remainder and
   never divides by zero. With a zero divisor it becomes undefined/backend
   failure rather than a modeled Python exception. This is an incomplete
   semantics case, not a false rewrite that can prove a result, and is exposed
   by `07-krun-excluded-boundary.log`.

6. **Inequality comparison.** `Compare(A, CmpOp("!=", B))` evaluates both
   integer operands and applies integer inequality. This is the exact used
   guard.

7. **Equality comparison.** The analogous `"=="` rule is mathematically
   correct but unused.

8. **Greater-than comparison.** The analogous `">"` rule is mathematically
   correct but unused.

9. **Single-function module entry.** A module containing one `FuncDef` installs
   its sole parameter at the configured integer argument and begins its body.
   It ignores the textual function name but does not ignore or replace the
   body. The entry claim itself fixes both the submitted name and exact body.
   This is a deliberately small model of calling the only submitted entry
   function, not ordinary Python module-import behavior. For this one-function
   program it preserves binding and control.

10. **Nonempty statement list.** The first statement is sequenced before the
    rest. This provides left-to-right statement evaluation.

11. **Empty statement list.** `.Stmts` is consumed to `.K`, allowing the
    active continuation to resume.

12. **Assignment.** `Assign(Name(X), E)` atomically evaluates the pure
    expression against the old environment, then updates `X`. This gives the
    correct read-before-write behavior for `divisor = divisor - 1`.

13. **While test.** `While(COND, BODY)` snapshots the current environment for
    pure Boolean evaluation and then schedules `whileBranch`.

14. **While true branch.** `true ~> whileBranch` schedules the body followed
    by the original `While`. Statement-list cleanup occurs before the next
    test, giving a stable, genuine loop head.

15. **While false branch.** `false ~> whileBranch` consumes the loop and
    resumes its existing continuation.

16. **If test.** The unused `If` rule evaluates the condition and schedules a
    branch marker. It is structurally analogous to the while guard.

17. **If true branch.** It selects exactly the `THEN` statement list.

18. **If false branch.** It selects exactly the `ELSE` statement list.

19. **Return.** With a remaining K continuation, `Return(E)` evaluates the
    pure expression in the current environment, stores it in a previously
    empty result cell, and discards the remaining function computation. There
    is no call stack, heap, output, or exception cell to preserve in this
    generated subset. In the submitted entry it discards only list cleanup and
    `.K`, so there is no mismatched outer continuation.

The expression patterns are disjoint by constructor or operator string. The
true/false branch rules are disjoint. Module, list, assignment, loop, if, and
return rules match distinct front computations. No priority is needed to hide
an overlap. Environment updates are the only state mutation. There is no
allocation, I/O, heap, exception state, or function-call stack in the submitted
construct set.

### `verification.k` rules

20. **Empty interval.** `noDivisorFrom(_, LO, HI) => true` under `LO > HI`
    truthfully states that an empty integer interval has no divisor.

21. **Nonempty interval.** Under `LO <= HI`, it checks `N mod LO != 0` and
    recurses at `LO + 1`. The interval strictly shrinks, and its guard is
    complementary to rule 20. On all theorem uses `LO > 0`, so no modulus-zero
    term occurs. The declaration is not marked total, which correctly avoids a
    global totality claim for intervals crossing zero.

22. **Largest through an upper bound.** `isLargestThrough` expands to
    positivity, `D <= UPPER`, divisibility, and absence of a divisor in
    `D+1..UPPER`. This is a definitional mathematical summary. It does not
    rewrite program execution.

23. **Largest proper divisor.** `isLargestProperDivisor` additionally requires
    `D < N` and selects upper bound `N - 1`. This is exactly the formal
    postcondition described in stage 4.

The two `noDivisorFrom` guards cover all integer orderings and do not overlap.
The other two functions each have a single unguarded definitional equation.
No rule uses a fresh or opaque result, and no helper occurs on the operational
left-hand side of a program step. Thus there is no circular
program-result oracle or task-answer execution shortcut.

### Claims and circularity

The loop claim matches the real loop head, full two-binding environment,
argument cell, empty result, and exact return continuation. A recursive
application is possible only after at least the while-test, true-branch,
assignment, and list-cleanup steps, so the circularity is guarded by real
execution progress. The entry claim reaches this exact loop shape after the
module and initialization rules. Its dependence on the loop claim is visible
from the fact that filtering the helper out causes exploration rather than
immediate closure.

No local rule is classified as unsound, so there is no false-conclusion witness
to report for an unsound rule. The zero-divisor exception case is instead the
narrower evidenced semantics-coverage gap described above: execution becomes
undefined and cannot make a false postcondition provable.

## 6. Fresh non-vacuity test

I did not rely on any candidate vacuity artifact. The fresh mutation
[`spec-vacuity.k`](evidence/spec-vacuity.k) keeps the genuine loop,
precondition, state transition, and largest-divisor postcondition, then adds
the false result obligation:

```text
?RESULT =/=Int ?RESULT
```

`N = 15, D = 14` is a satisfying starting state, and the real result is 5, so
the added obligation is demonstrably false.

First:

```text
kprove /audit-output/evidence/spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY --dry-run
```

exits 0 and emits a valid `kore-exec` command, showing that the mutation parses
and builds. See
[`13-vacuity-dry-run.log`](evidence/13-vacuity-dry-run.log).

Then the same proof without `--dry-run` exits 1. It emits
`WarnClaimRHSIsBottom`, followed by `WarnStuckClaimState` specifically because
the destination unifies but the implication between conditions fails. This is
the expected unmet result obligation, not a parser error, missing import,
timeout, or unrelated crash. See
[`14-vacuity-proof.log`](evidence/14-vacuity-proof.log).

As a separate body-sensitivity probe, I changed the decrement inside the
executed `Module(...)` term from 1 to 2, fixed `N = 15`, and retained expected
result 5. [`spec-body-mutation.k`](evidence/spec-body-mutation.k) dry-runs
successfully but the proof exits 1 at the reached state `divisor = 0`, with the
mutated `Int(2)` body visible in the residual. See
[`15-body-mutation-dry-run.log`](evidence/15-body-mutation-dry-run.log) and
[`16-body-mutation-proof.log`](evidence/16-body-mutation-proof.log). This
mutation changes the actual claim term, not merely an external source file.

## 7. Proven versus assumed accounting

### What the K proof establishes

Under the submitted `MPY` semantics and built-in K integer/Boolean/map theory,
for every K integer `N > 1`, executing the exact regenerated constructor term
for the submitted `largest_divisor` function reaches a result `D` such that:

- `0 < D < N`;
- `N mod D = 0`; and
- every integer `x` with `D < x < N` fails to divide `N`.

The loop claim establishes the corresponding invariant for any positive
current candidate with all larger candidates already ruled out. The theorem is
unbounded in `N`; it is not finite unrolling or a proof of only the tested
sizes.

It does **not** establish behavior for `N <= 1`, Python exceptions, non-integer
arguments, multiple functions, arbitrary Python expressions, or any
constructor not covered by this generated subset.

### Trust ledger

| Boundary | Influence | Evidence and judgment |
|---|---|---|
| Trusted `py2mpy.py` | Constructor identity | Candidate translator is byte-identical to the trusted mount; fresh translation is byte-identical to submitted `.mpy`. Acceptable trusted front end. |
| K `INT`, `BOOL`, and `MAP` built-ins and K v7.1.293 backends | All arithmetic, predicates, maps, and proof checking | Standard low-level proof trust boundary. Both LLVM and Haskell definitions were rebuilt. Acceptable. |
| Generated `MPY` rules | Binding, state, loop control, and return | Audited exhaustively above; concrete execution covers every used construct and static review finds no result oracle. Acceptable on `N > 1`. |
| K `modInt` as Python `%` | Guard and divisibility result | Exact for the proof's positive divisor states; independently compared over `n=2..2000`. Zero-divisor exception behavior is not modeled. Acceptable only inside the stated proof domain. |
| `noDivisorFrom`, `isLargestThrough`, `isLargestProperDivisor` | Invariant and final mathematical result | Exhaustive recursive/definitional equations, no opacity, disjoint guards, positive interval at all uses. Formally part of the checked theory and mathematically justified. |
| Single-function configured entry rule | Relates `Module(FuncDef(...))` to invocation with `<arg>` | Executes the exact body and binding but abstracts CPython module/import machinery. Constructor pinning plus direct static correspondence and differential tests support it. Acceptable for this isolated entry function. |
| Differential testing | Python/K and candidate/canonical bridge | Zero mismatches on 2..2000 and stated boundaries; finite empirical evidence only, not substituted for the K proof. |
| Assumption `N > 1` | Excludes all theorem obligations at zero and negative inputs | Not stated in trusted prompt or signature, and `n=0` is a terminating candidate/canonical mismatch. This is an illegitimate material source-domain restriction for this benchmark. |

### Gate results and decision

- Real-program soundness gate: **passes** for the stated `N > 1` domain. The
  proof is non-vacuous, body-sensitive, result-constraining, and executes the
  exact regenerated program under sound subset semantics.
- Intent adequacy gate: **fails**. The theorem adds `N > 1` to a source
  signature and contract that declare only `int`, and concrete excluded inputs
  show materially different behavior.
- Trust/evidence gate: **passes for the restricted theorem**. All artifacts,
  commands, tests, boundaries, and negative probes are reproducible.

In generic Kit terminology this is a sound-but-limited theorem. The controlling
benchmark instruction explicitly maps sound-but-limited work caused by
materially narrowing the HumanEval source-contract domain to failure and
non-legitimacy.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
