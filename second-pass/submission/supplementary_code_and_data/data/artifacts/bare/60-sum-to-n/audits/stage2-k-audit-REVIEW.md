# Independent adversarial review: 60-sum-to-n

## Executive finding

The candidate contains a fresh-reconstructible, result-constraining K proof of a
restricted theorem: for `N >= 0`, the submitted constructor program returns
`N * (N + 1) / 2`. The proof definition rebuilds, its only positive claim
prints `#Top`, the claim mechanically contains the submitted program body, and
both body-sensitivity and false-postcondition mutations fail for the expected
result obligations.

That theorem is not a legitimate proof of the full source contract. The trusted
prompt gives an unqualified `int` input and the trusted canonical implementation
is `sum(range(n + 1))`; negative integers are therefore in the executable
source-contract domain and produce the empty sum `0`. The submitted closed form
returns nonzero values for every `n <= -2` (for example, `n = -2` returns `1`),
and `spec.k` excludes all negative inputs with `requires N >=Int 0`.
Independent differential testing found 2,108 such divergences and no
nonnegative divergence. This is the benchmark's expressly disqualifying case:
a materially narrowed HumanEval source-contract domain.

## 1. Input and provenance integrity

The launcher record declares:

- problem `60-sum-to-n`, condition `bare`;
- `record_layout = legacy-selected-stage1`;
- `semantics_mode = GENERATED_SEMANTICS`;
- complete input provenance.

I read `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
`/task.json`, `/generation-result.json`, the required invocation/metrics/last
message/output/prompt records, the present `usage.json`, and the complete
101-record structured JSONL trace. Historical runtime metrics are not required
for this legacy-selected layout. The generation records were treated only as
untrusted claims; their reported `KPROVE_PASSED` did not contribute to the
proof verdict.

The campaign object exactly equals `/audit-campaign-lock.json`; the lock's
audit-prompt hash also matches `/audit-prompt.md`. Every required mount and
record is readable and is a real regular file or real directory as applicable.
The candidate and trace trees contain no symlink or unsupported entry. All
recorded individual file hashes match, including the run/task/result records,
prompt, canonical, translator, invocation, metrics, output log, final message,
usage, and trace JSONL. The benchmark's canonical content-tree digest of
`/candidate` is
`21cffa14189fe45cb8333f8700a644d1de001b7ee32902a50f5e5d8cd98091fc`,
which matches the invocation's retained/output workspace hashes and the stage
result. The canonical trace-tree digest matches `usage.json`, and the trace
file hash matches the invocation and result manifests.

`/candidate/prompt.py` and `/candidate/py2mpy.py` are byte-identical to the
trusted `/reference` copies. Consistent with generated-semantics mode,
`/reference/reference-semantics` does not exist. All required proof artifacts
are present. No infrastructure breach was found.

Evidence:

- [`evidence/01-provenance.log`](evidence/01-provenance.log)
- [`evidence/provenance_check.py`](evidence/provenance_check.py)
- [`evidence/01-trace-summary.log`](evidence/01-trace-summary.log)
- [`evidence/trace_summary.py`](evidence/trace_summary.py)

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

The trusted prompt defines `sum_to_n(n: int)` as summing the numbers from `1`
to `n`, with examples `1 -> 1`, `5 -> 15`, `10 -> 55`, `30 -> 465`, and
`100 -> 5050`. It states no positivity precondition. The trusted canonical
implementation is:

```python
return sum(range(n + 1))
```

Consequently, `n = 0` and all negative integers use an empty range and return
`0`. This behavior is defined by the trusted executable oracle, not inferred
from candidate prose.

The submitted implementation is:

```python
return n * (n + 1) // 2
```

It agrees with the canonical implementation for nonnegative integers. It
disagrees for every integer `n <= -2`; for example:

```text
n = -2: canonical = 0, candidate = 1
n = -3: canonical = 0, candidate = 3
n = -100: canonical = 0, candidate = 4950
```

Using the trusted translator on the scratch copy produced SHA-256
`e1450114979c8fb27a984a4763e80a16edf6c7d6e3bca86d3246d11bc0552c13`,
byte-identical to submitted `solution.mpy`.

The independent differential test covered all five examples, the empty/range
boundaries around `-1` and `0`, every integer in `[-2000, 2000]`, 256
deterministically generated integers in `[-10000, 10000]`, and larger boundary
values. Across 4,203 unique inputs it found 2,108 mismatches, all negative, and
zero nonnegative mismatches. Its expected nonzero exit records the material
candidate/oracle divergence.

Evidence:

- [`evidence/02-translation.log`](evidence/02-translation.log)
- [`evidence/02-regenerated-solution.mpy`](evidence/02-regenerated-solution.mpy)
- [`evidence/02-differential.log`](evidence/02-differential.log)
- [`evidence/differential_test.py`](evidence/differential_test.py)

## 3. Clean proof reconstruction

Only source artifacts were copied to `/tmp/audit-work/reconstruction`; no
candidate-provided compiled definition or cache was copied or reused. The
observed toolchain was K `v7.1.293`.

Fresh commands and outcomes:

```text
kompile --backend llvm semantic.k --main-module MPY \
  --syntax-module MPY-SYNTAX --output-definition concrete-kompiled
exit 0

kompile --backend haskell verification.k --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX --output-definition proof-kompiled
exit 0

kprove spec.k --definition proof-kompiled --spec-module SPEC
#Top
exit 0
```

`spec.k` contains exactly one positive target claim, so the last command
independently executes every positive target. The candidate's historical
definition and proof output were not used.

Fresh LLVM execution on `[-3, -2, -1, 0, 1, 2, 30, 100]` matched the submitted
Python implementation on every input. It also exposed the source-contract
failure: K and candidate Python returned `3` and `1` for `-3` and `-2`, while
trusted canonical Python returned `0` for both. Normal and boundary executions
therefore validate that the generated semantics models this submitted body;
they do not repair the submitted body's disagreement with the canonical
program.

Evidence:

- [`evidence/03-toolchain.log`](evidence/03-toolchain.log)
- [`evidence/03-concrete-build.log`](evidence/03-concrete-build.log)
- [`evidence/03-proof-build.log`](evidence/03-proof-build.log)
- [`evidence/03-kprove-positive.log`](evidence/03-kprove-positive.log)
- [`evidence/03-concrete-execution.log`](evidence/03-concrete-execution.log)
- [`evidence/k_concrete_compare.py`](evidence/k_concrete_compare.py)
- [`evidence/03-concrete-execution-attempt1.log`](evidence/03-concrete-execution-attempt1.log)
  records and distinguishes the reviewer's corrected negative-argument CLI
  encoding attempt.

## 4. Adequacy and real-program pinning

### Formal claim in plain language

The only entry claim starts from:

- the exact constructor module containing a single function named
  `"sum_to_n"`;
- the single parameter named `"n"`;
- the return body `n * (n + 1) // 2`;
- an invocation of `"sum_to_n"` with symbolic K integer `N`;
- `result = noResult`;
- precondition `N >= 0`.

It requires execution to consume the complete `<k>` computation and change
`result` to:

```text
sumSpec(N) = (N * (N + 1)) /Int 2
```

The result is not free, existential, an implication antecedent, or a tautology.
It is fixed to a concrete arithmetic expression.

### Mechanical program identity

An independent balanced-term extractor and constructor parser compared the
submitted `solution.mpy` tree with the `Module(...)` tree embedded in the
claim. The trees are equal constructor-for-constructor, including binding
`"sum_to_n"`, parameter `"n"`, operator nesting, and integer literals. This is
stronger than a textual source-file association. Trusted regeneration also
made the submitted `.mpy` byte-identical to the current `solution.py`.

The operational rule uses the same K variable `F` in the function definition
and `invoke(F, V)`, so it cannot silently select a differently named function.
There are no helper or loop claims and no alternate summarized control flow.

### Satisfying states and substituted results

The initial exact configurations with `N = 0, 1, 2, 30, 100` all satisfy the
entry precondition. Substitution yields claimed/candidate/canonical triples
`0/0/0`, `1/1/1`, `3/3/3`, `465/465/465`, and `5050/5050/5050`.

The decisive excluded witness is `N = -2`: it does not satisfy the formal
precondition, submitted Python and K return `1`, and trusted canonical Python
returns `0`. Thus the precondition excludes precisely a class on which the
program violates the source contract.

### Body sensitivity

A separate mutation changed the program term actually executed by the claim
from `n * (n + 1) // 2` to `n * (n + 2) // 2`, leaving the original
postcondition intact. `kprove` parsed it and exited `1` with
`WarnStuckClaimState`; the residual compared
`N*(N+1)/2` with `N*(N+2)/2`. This confirms dependence on the embedded body,
not merely on an external source filename.

Evidence:

- [`evidence/04-claim-adequacy.log`](evidence/04-claim-adequacy.log)
- [`evidence/claim_adequacy.py`](evidence/claim_adequacy.py)
- [`evidence/04-spec-body-mutation.k`](evidence/04-spec-body-mutation.k)
- [`evidence/04-body-sensitivity.log`](evidence/04-body-sensitivity.log)

Adequacy result: real-program pinning and result constraint pass for the
restricted theorem; source-contract domain adequacy fails materially.

## 5. Rule-by-rule static soundness review

There are no generated helper K files. The complete local inventory is
`semantic.k`, `verification.k`, and the one reachability claim in `spec.k`.
The numbered source and lexical inventory are preserved in
[`evidence/05-numbered-sources.log`](evidence/05-numbered-sources.log) and
[`evidence/05-source-inventory.log`](evidence/05-source-inventory.log).

### Syntax, configuration, and attributes

`MPY-SYNTAX` imports only K integer and string syntax and declares:

1. `Program ::= Module(Function)`;
2. `Function ::= FuncDef(String, Params(String), Statement)`;
3. `Statement ::= Return(Expr)`;
4. `Expr ::= Int(Int)`;
5. `Expr ::= Name(String)`;
6. `Expr ::= BinOp(String, Expr, Expr)`.

`MPY` imports the syntax plus K `INT` and `STRING`, and declares:

7. `invoke(String, Int)` as a `KItem`;
8. `noResult` as a `KItem`;
9. `evalExpr(Expr, String, Int)` returning `Int`, with `[function]`.

`VERIFICATION` declares:

10. `sumSpec(Int)` returning `Int`, with `[function]`.

The configuration has exactly `<k>` and `<result>` under `<mpy>`. The initial
`<k>` is `$PGM ~> invoke($FUNCTION, $ARG)` and the initial result is
`noResult`. These are all the state components needed by this single pure,
single-argument return expression.

There are exactly two local `[function]` declarations. There is no `[total]`,
`[functional]`, `[simplification]`, `[concrete]`, priority, `owise`, macro,
alias, fresh symbol, opaque symbol, or uninterpreted result oracle. The
`[symbol(...)]` attributes only name syntax constructors. There are no local
priority interactions or overlapping same-shape rules.

Every submitted constructor is covered:

| Submitted construct | Declaration/rule |
|---|---|
| `Module` | `Program` syntax and execution rule S6 |
| `FuncDef`, `Params` | `Function` syntax and execution rule S6 |
| `Return` | `Statement` syntax and execution rule S6 |
| `Int(1)`, `Int(2)` | `Expr` syntax and S1 |
| `Name("n")` | `Expr` syntax and S2 |
| `BinOp("+",...)` | `Expr` syntax and S3 |
| `BinOp("*",...)` | `Expr` syntax and S4 |
| `BinOp("//",...)` | `Expr` syntax and S5 |

### Ordinary semantic and proof rules

| ID | Exact local rule | Complete local domain and effect | Assessment |
|---|---|---|---|
| S1 | `evalExpr(Int(I), _P, _V) => I` | Any integer literal; no cells or control affected | Faithful literal evaluation. |
| S2 | `evalExpr(Name(P), P, V) => V` | A name exactly equal to the sole parameter name; returns its bound integer | Repeated `P` enforces binding equality. An unknown name stops visibly rather than receiving a fabricated value. |
| S3 | `evalExpr(BinOp("+",L,R),P,V) => evalExpr(L,P,V) +Int evalExpr(R,P,V)` | Pure supported expressions | Faithful unbounded integer addition. |
| S4 | Corresponding `*Int` rule | Pure supported expressions | Faithful unbounded integer multiplication. |
| S5 | Corresponding `/Int` rule for `"//"` | All syntactically accepted pure expressions | Faithful on the submitted execution path; scope limitation described below. |
| S6 | Exact `<k>` module/function/invocation rewrite; `noResult => evalExpr(E,P,V)` | The entire `<k>` content must be exactly the module followed by a same-name invocation, and `<result>` must be `noResult` | Faithfully binds the sole parameter and evaluates the actual returned expression. It has no `...` continuation, no omitted local cell, and introduces no abrupt return over a broader context. |
| V1 | `sumSpec(N) => (N *Int (N +Int 1)) /Int 2` | Every K integer; affects the postcondition only | A terminating, nonoverlapping definitional abbreviation. It does not replace execution. |

S3–S5 evaluate only the pure expression forms declared here. There are no
calls, mutation, allocation, output, exceptions represented as values, or
other observable state whose order could be lost in the submitted program.
S6 reads/writes both local cells: it consumes the exact computation and writes
only the result. The function-name mismatch test left the complete computation
unconsumed, and an unknown-name test stopped on
`evalExpr(Name("x"), "n", 2)`; no binding or result was fabricated.
The run is preserved in
[`evidence/05-binding-sensitivity.log`](evidence/05-binding-sensitivity.log).

S6 is the generated language's ordinary execution rule, not a proof-local
bridge preempting another fixed semantics. It executes `E` through S1–S5.
V1 is a postcondition abbreviation, not an operational bridge. There is no
program-derived opaque value and therefore no circular oracle appearing in
both execution and the postcondition.

### Floor-division scope limitation

K `/Int` truncates a negative quotient toward zero, whereas Python `//` floors.
Fresh synthetic terms witnessed:

```text
-3 /Int 2  -> -1, while Python -3 // 2  == -2
 3 /Int -2 -> -1, while Python  3 // -2 == -2
```

This demonstrates that S5 is broader than a reusable faithful Python
floor-division rule. It is not a false-conclusion witness for this submitted
program on any integer input: the only divisor is positive `2`, and
`n * (n + 1)` is nonnegative for every integer `n`. Thus S5 agrees with Python
on every reachable instance of the submitted body. Following the benchmark's
required witness rule, I classify this as a narrow generated-semantics scope
limitation rather than materially unsound semantics for the theorem. The
synthetic evidence is in
[`evidence/05-division-scope.log`](evidence/05-division-scope.log), with the
inputs in
[`evidence/05-synthetic-division-negative.mpy`](evidence/05-synthetic-division-negative.mpy)
and
[`evidence/05-synthetic-divisor-negative.mpy`](evidence/05-synthetic-divisor-negative.mpy).

The proof does not formally define or execute `range` and `sum`; it proves the
closed formula produced by the submitted program. The familiar equivalence
between that formula and `1 + ... + n` for nonnegative `n` is an informal
mathematical intent bridge. For negative `n` the bridge is false for the
trusted canonical contract, which is the material adequacy failure rather than
a smuggled semantic rule.

Static soundness result: no operational bypass, answer oracle, inconsistent
equation, priority exploit, or false rule reachable on the claimed program
domain was found. The restricted theorem's proof theory is sound, subject to
the explicit trust boundaries in stage 7.

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`. I created a fresh spec with the
same exact program, precondition, and control obligation, changing only the
result requirement from `sumSpec(N)` to `sumSpec(N) +Int 1`.

`N = 0` is a concrete satisfying witness: execution returns `0`, while the
mutation requires `1`. A dry run built the mutation successfully (exit `0`,
320-byte generated KORE). The actual proof exited `1` with
`WarnStuckClaimState`, and its residual was the expected unmet equality:

```text
N * (N + 1) / 2 + 1 == N * (N + 1) / 2
```

This is a semantic proof failure, not a parser error, missing import, timeout,
or unrelated crash. The positive claim is therefore discriminating.

Evidence:

- [`evidence/06-spec-vacuity.k`](evidence/06-spec-vacuity.k)
- [`evidence/06-vacuity-build.log`](evidence/06-vacuity-build.log)
- [`evidence/06-vacuity-proof.log`](evidence/06-vacuity-proof.log)
- [`evidence/06-spec-vacuity-dry-run.kore`](evidence/06-spec-vacuity-dry-run.kore)

## 7. Proven versus assumed accounting and decision

### Precisely proven

Relative to the freshly compiled generated semantics and imported K integer
theory, the successful reachability claim establishes:

> For every K integer `N` satisfying `N >= 0`, executing the exact submitted
> `Module(FuncDef("sum_to_n", Params("n"), Return(n*(n+1)//2)))` followed by
> the same-name invocation consumes the computation and leaves the result
> `(N * (N + 1)) /Int 2`.

It does not establish the required behavior for negative Python integers. It
also does not prove the trusted canonical `sum(range(n + 1))` program directly.

### Trust ledger

| Boundary | Influence | Accounting |
|---|---|---|
| Trusted `py2mpy.py` | Connects `solution.py` to the constructor program | Byte identity was independently regenerated. The translator itself is a trusted input, not proved in K. |
| K `INT`/`STRING` and backend | Arithmetic, strings, matching, reachability | Standard low-level proof trust boundary. Fresh build, execution, and mutation behavior were checked. |
| Generated rules S1–S6 | Entire program execution | Exhaustively reviewed above and concretely compared with submitted Python on normal/boundary inputs. No opaque result is introduced. |
| `sumSpec` V1 | Final result obligation | Fully defined by one universal nonrecursive equation; no overlap, opacity, or oracle. |
| Python/K numeric bridge | Relates K integers and operators to Python | Exact unbounded `+` and `*` are accepted; division agrees on the reachable nonnegative numerator/positive divisor. The broader negative-quotient mismatch is explicitly excluded from reuse. |
| Formula-to-sum intent bridge | Relates `n(n+1)/2` to summing `1..n` | Ordinary mathematics and finite differential evidence support it for `n >= 0`; it is false against the trusted canonical behavior for `n <= -2`. |
| Generation reports and historical `#Top` | None in the audit conclusion | Treated only as untrusted provenance evidence; the audit used a fresh `#Top`. |

There are no proof-local opaque symbols, fresh result values, assumed lemmas,
helper claims, loop invariants, or operational shortcuts. Differential testing
supports only the finite Python/contract comparison; it is not substituted for
the K proof.

### Gate and benchmark decision

- Gate A, real-program soundness for the stated restricted theorem: **PASS**.
  The proof rebuilds, pins and executes the body, constrains the result, is
  body-sensitive, and rejects the false postcondition.
- Gate B, source-contract intent adequacy: **FAIL**. The unqualified integer
  contract is materially narrowed to `N >= 0`, and the submitted implementation
  demonstrably disagrees with the trusted canonical implementation on excluded
  inputs such as `-2`.
- Gate C, trust/evidence auditability for the restricted theorem: **PASS with
  the recorded division-reuse limitation**. All relevant evidence is
  reproducible and the trust boundary is explicit.

Kit terminology would call this restricted theorem sound but limited. The
benchmark prompt explicitly maps a `SOUND-BUT-LIMITED` finding caused by
materially narrowing the HumanEval source-contract domain to
`FAIL / NOT_LEGIT`, not to concerns.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
