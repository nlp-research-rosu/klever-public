# Independent adversarial audit: 163-generate-integers

## Overall decision

**CONCERNS / LEGIT.** The source-only reconstruction proves the one positive
entry claim under the candidate's generated semantics: the fresh targeted
`kprove` run exited 0 and printed `#Top`. The claim executes the submitted
`solution.mpy`, constrains both the returned result and the final `result`
binding, has satisfiable positive-input states, and rejects a fresh false-result
mutation. I found no answer-encoding execution rule, opaque oracle, unsound
proof lemma, or bypass of the program body.

The concern is a trust/evidence limitation rather than a legitimacy failure.
`semantic.k` is a small, purpose-specific model, not a machine-checked
refinement of CPython. Its entry rule is an invocation harness, and its return
machinery is faithful for this program's final-position `Return` but is not
general abrupt-return semantics. Static review shows that the model is sound on
every state reachable by this submitted program, and fresh finite K/Python
comparisons support that bridge, but the bridge remains an audited informal
argument rather than a universal connection theorem.

## 1. Input and provenance integrity

The rendered mode and trusted mounts agree. This is
`GENERATED_SEMANTICS`, and `/reference/reference-semantics` does not exist.
There is therefore no hidden or supplied semantics baseline to compare or use.
The absence check, K tool versions, comparisons, and exit statuses are in
[`environment-and-integrity.log`](evidence/environment-and-integrity.log).

The candidate has all required generation artifacts as ordinary files:
`solution.py`, `solution.mpy`, `semantic.k`, `verification.k`, `spec.k`, and
executable `prove.sh`. `prompt.py` and `py2mpy.py` are also ordinary files.
There are no symlinks anywhere under `/candidate`. The candidate prompt is
byte-identical to `/reference/prompt.py`, and the candidate translator is
byte-identical to `/reference/py2mpy.py`; their SHA-256 values also match the
values asserted in `run-input.json`. See
[`filesystem-inventory.txt`](evidence/filesystem-inventory.txt),
[`source-sha256.txt`](evidence/source-sha256.txt), and
[`integrity-checks.txt`](evidence/integrity-checks.txt).

No required source artifact is missing, changed relative to a trusted mounted
counterpart, mistyped, or symlinked. There are extra build products
(`semantic-kompiled/`, `verification-kompiled/`, and `__pycache__/`); these are
not source-integrity failures, but I excluded them completely from
reconstruction. There are no additional candidate K helper source files.

I read `run-input.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, and the 171-line structured trace at
`/candidate/codex-trace/2026/07/22/rollout-2026-07-22T08-02-44-019f89eb-dfb2-7680-a603-95f156b1d1d2.jsonl`
only as claims. They assert a final successful script, `#Top`, and a 900-case
Python sweep; the construction log also records earlier failures. None was
relied upon. A bounded summary is preserved in
[`untrusted-claims-summary.txt`](evidence/untrusted-claims-summary.txt).

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract is: for positive integers `a` and `b`, return, in
ascending order, the even decimal digits lying in the inclusive interval whose
endpoints are `a` and `b`, irrespective of endpoint order. On positive inputs
the possible values are exactly `2, 4, 6, 8`. The trusted canonical
implementation computes the interval intersection with `[2,8]` and filters it
for even values.

`solution.py` implements a different but equivalent finite algorithm. It starts
with an empty list, chooses the endpoint order using `a <= b`, and checks
membership of `2`, `4`, `6`, and `8` in ascending order. Every appended value
is therefore an even digit in the unordered inclusive interval, and every such
positive even digit is checked once.

The trusted command

```text
python3 /reference/py2mpy.py /tmp/audit-work/src/solution.py
```

regenerated the IR with exit 0. The result was byte-identical to submitted
`/candidate/solution.mpy`; both hashes are
`54429f6b9e491fb77c192588c91cb091f01486578cfabc7f76be228ac25eaeab`.
Exact evidence is in
[`translation-identity.log`](evidence/translation-identity.log).

The independent differential test imports
`/reference/canonical.py:generate_integers` and the scratch candidate entry
point separately. It covers the three documented examples, explicit empty and
threshold cases, both endpoint orders, every ordered pair in
`[1,12] x [1,12]`, four very-large-integer boundaries, and 500 deterministic
generated pairs from `[1,10^6]`. All 650 unique positive-input cases agreed,
including result type; mismatch count was zero. The script, exact generator
scope, command, exit status, and result are
[`differential_test.py`](evidence/differential_test.py),
[`differential-input-scope.txt`](evidence/differential-input-scope.txt), and
[`differential-test.log`](evidence/differential-test.log).

## 3. Clean proof reconstruction

K `v7.1.293` was available. I copied only source artifacts into
`/tmp/audit-work/src`; no candidate `*-kompiled` directory or cache was copied
or named by a command.

The concrete definition was freshly built with:

```text
kompile semantic.k --backend llvm --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/fresh-semantic-kompiled
```

It exited 0; see
[`kompile-semantic.log`](evidence/kompile-semantic.log). A smoke run for
`(2,8)` reached `.K` with `[2,4,6,8]`
([`krun-smoke-2-8.log`](evidence/krun-smoke-2-8.log)). A reviewer-authored
driver then ran the fresh semantics on 20 normal and boundary pairs, including
forward/reversed examples, empty intervals, every digit threshold, and a
40-digit endpoint. Every `krun` exited 0, reached `.K`, and matched independent
trusted Python. See
[`concrete_semantics_compare.py`](evidence/concrete_semantics_compare.py) and
[`concrete-semantics-compare.log`](evidence/concrete-semantics-compare.log).
The preserved `concrete-semantics-compare-attempt1-reviewer-parser-error.log`
records an initial reviewer regex error: its captured K outputs were correct,
but the harness failed to recognize whitespace. The corrected parser produced
the zero-mismatch result above.

The proof definition was freshly built with:

```text
kompile verification.k --backend haskell --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/fresh-verification-kompiled
```

It exited 0; see
[`kompile-verification.log`](evidence/kompile-verification.log). `spec.k`
contains exactly one positive claim. I selected it explicitly:

```text
kprove spec.k \
  --definition /tmp/audit-work/fresh-verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.generate-integers-correct
```

The command exited 0 and printed `#Top`; the claim inventory, command, output,
and exit status are in
[`kprove-generate-integers-correct.log`](evidence/kprove-generate-integers-correct.log).
Thus the clean dynamic gate passes.

## 4. Adequacy and real-program pinning

There is one entry claim and no loop, helper, or auxiliary reachability claim.
In plain language:

- Precondition: symbolic K integers `A` and `B` are both strictly positive.
  The initial input is `pair(A,B)`, the environment is empty, and the result
  cell is `noResult`.
- Execution: the `<k>` cell contains the full `Module(FuncDef(...))` term for
  `generate_integers(a,b)` and must rewrite to `.K`.
- Postcondition: the final environment is exactly `a = A`, `b = B`, and
  `result = expected(A,B)`; the result cell is also exactly
  `expected(A,B)`.
- `expected(A,B)` is the ascending K list formed by including each of
  `2,4,6,8` precisely when it lies in the inclusive interval in either endpoint
  order.

The result is not free or merely implied: the same deterministic expression of
the left-hand variables appears in both observable result locations.

To check program identity independently, I extracted the balanced `Module`
term from the claim, converted claim-only empty-list unit notation to equivalent
concrete empty syntax, and parsed both that term and `solution.mpy` with the
fresh definition. Their KORE bytes and SHA-256 hashes were identical
(`78cc4dea14ed2976669d3000fdc3540a8e3d8b83a497482eef2d3798ce19a4c2`).
See [`extract_spec_program.py`](evidence/extract_spec_program.py) and
[`program-pinning-kast.log`](evidence/program-pinning-kast.log). The preserved
first attempt shows why concrete syntax normalization was needed; it is not a
candidate parse failure.

A complete satisfying initial state exists, for example the exact claimed
program with `<input> pair(2,8) </input>`, empty environment, and
`<result> noResult </result>`. The precondition is true. Ground substitutions
give:

- `(2,8)`: formal result, candidate Python, and canonical Python are all
  `[2,4,6,8]`;
- `(10,14)`: all are `[]`;
- `(3,7)`: all are `[4,6]`.

These checks and exit 0 are in
[`claim-witnesses.log`](evidence/claim-witnesses.log). The first case alone
satisfies the required entry-state witness; the other two show an empty and an
interior result.

## 5. Rule-by-rule static soundness review

The complete reviewer-authored inventory, with source lines, is
[`rule-inventory.txt`](evidence/rule-inventory.txt), and the mechanical
declaration scan is
[`static-declaration-scan.log`](evidence/static-declaration-scan.log).

### Local declaration inventory

`MPY-SYNTAX` declares all of the following and nothing else:

| Sort | Productions |
|---|---|
| `Program` | `Module(Stmts)` |
| `Stmts` | `List{Stmt, ""}` |
| `Stmt` | `FuncDef(String,Params,Stmts)`, `Assign(Expr,Expr)`, `If(Expr,Stmts,Stmts)`, `Return(Expr)` |
| `Params` / `Strings` | `Params(Strings)`; comma-separated `String` list |
| `Expr` | `Name(String)`, `Int(Int)`, `ListExpr(Exprs)`, `Compare(Expr,CmpOps)`, `BinOp(String,Expr,Expr)` |
| `Exprs` / `CmpOps` / `CmpOp` | comma-separated expression and comparison-op lists; `CmpOp(String,Expr)` |

`MPY` locally declares `pair(Int,Int)`; values `intVal`, `boolVal`, and
`listVal`; result `noResult | Value`; scheduling items `exec`, `execStmt`,
`eval`, `assignTo`, `binRight`, `cmpLeft`, `cmpRight`, `choose`, and
`returnValue`; and the internal `evalPlaceholder(Expr)` value constructor.
Its `<py>` configuration contains only `<k>`, `<input>`, `<env>`, and
`<result>`, which are exactly the state components the target needs.

`VERIFICATION` declares exactly two `[function]` symbols,
`expectedDigit(Int,Int,Int)` and `expected(Int,Int)`, both returning a K
`List`. There are no local `[total]`, `[functional]`, `[simplification]`,
`[concrete]`, opaque, priority, macro, or anywhere declarations.

### All 21 operational rules

| IDs | Rules and decision |
|---|---|
| S1 | The exact `generate_integers(a,b)` entry harness loads `A,B` into an initially empty map and schedules the actual `BODY`. Accepted: binding is exact and the body/result are not summarized or fabricated. |
| S2-S3 | Empty statement sequence finishes; nonempty sequence executes head then tail. Accepted: target statement order is preserved. |
| S4-S5 | Assignment evaluates its RHS, then updates the named environment binding. Accepted: correct state footprint and evaluation order for all target assignments. |
| S6-S8 | `If` evaluates its condition; true selects `THEN`, false selects `ELSE`. Accepted: guards are value-disjoint and control is preserved. |
| S9-S10 | `Return` evaluates its expression and writes the value to `<result>`. Accepted on every reachable target state because the only `Return` is final; scope limitation discussed below. |
| S11-S12 | Integer literals become `intVal`; names read their exact map binding. Accepted. Every target lookup is defined after S1/S5. |
| S13-S14 | Empty list and singleton integer list expressions become the corresponding built-in K Lists. Accepted and exhaustive for the list literals actually used. |
| S15-S17 | Binary operation evaluates left, then right, then concatenates a retained left list before the right list for `"+"`. Accepted: the order and result match target Python list addition. |
| S18-S21 | Comparison evaluates left, then right; `"<="` returns true under `LEFT <=Int RIGHT` and false under its Boolean complement. Accepted: the two guards are disjoint and exhaustive for K integers. |

The internal `evalPlaceholder` is declared as a `Value` solely to fit the
`binRight` scheduling field. It cannot be constructed by source `Expr` syntax,
and no target execution can assign, return, compare, or branch on it. It
therefore introduces no result-bearing oracle or reachable overlap.

S9-S10 are intentionally not credited as general Python function-return
semantics. With a different body such as `Return(Int(1))` followed by an
assignment, S3 would retain and execute the suffix, unlike Python abrupt return.
That is a concrete scope witness, but it substitutes a different program:
the submitted body's return is final, so the problematic suffix is `.Stmts`
for every positive `A,B`. It cannot enable a false conclusion about the
intended program and is recorded as a reuse limitation rather than labeled an
unsound target rule. Missing or non-general behavior for unused contexts is
permitted by the generated-semantics boundary.

### All three verification equations

| ID | Equation and decision |
|---|---|
| V1 | `expectedDigit(A,B,D) => ListItem(D)` under interval predicate `P`. True by definition of inclusive membership. |
| V2 | `expectedDigit(A,B,D) => .List` under `notBool(P)`. True; its guard is the exact complement of V1, so coverage is exhaustive and overlap impossible. |
| V3 | `expected(A,B)` rewrites unconditionally to the concatenation of the four expected-digit terms for `2,4,6,8`. True and terminating. |

These functions occur only in the destination. They do not rewrite a program
term, influence a branch, or replace execution. The prover must symbolically
execute the submitted body and show that its concrete list construction equals
the independently defined destination expression. There are no proof-local
operational bridges, opaque symbols, loop summaries, auxiliary claims, or
smuggled task-answer rules.

### Used-construct and state coverage

The submitted IR uses `Module`, `FuncDef`, `Params`, statement sequencing,
`Assign`, `If`, final `Return`, `Name`, `Int`, empty/singleton `ListExpr`,
`BinOp("+")`, and single `Compare/CmpOp("<=")`. Respectively these are covered
by S1, S2-S3, S4-S5, S6-S8, S9-S10, S12, S11, S13-S14, S15-S17, and S18-S21.
No used term can silently fall through to a fabricated result.

The environment and result are the only mutable observable cells needed.
Lists are rebuilt by concatenation; the source has no alias-observable list
mutation or allocation identity. There are no body calls, loops, exceptions on
the used integer/list operations, heap effects, I/O, or external state. This
justifies the small configuration for this target without claiming a general
Python semantics.

I found no materially unsound rule on the intended input domain, so no
false-conclusion witness against a candidate rule exists to report. The
non-general return behavior is stated at its narrower, evidenced scope above.

## 6. Fresh non-vacuity test

No candidate mutation was trusted. I created
[`spec-vacuity.k`](evidence/spec-vacuity.k) from the entry claim in scratch and
changed only the result-bearing obligation (plus module/label): the destination
now requires
`listVal(expected(A,B) ListItem(10))`, while the final environment still
requires the correct `expected(A,B)`. The exact diff is
[`spec-vacuity.diff.log`](evidence/spec-vacuity.diff.log).

The mutation is demonstrably false at the satisfying input `(2,8)`: the actual
and formal correct result is `[2,4,6,8]`, while the mutation demands
`[2,4,6,8,10]`. It is also false for every satisfying input because the program
never appends `10`.

`kprove ... --dry-run` exited 0, proving that the mutation imported and built
successfully; see
[`spec-vacuity-dry-run.log`](evidence/spec-vacuity-dry-run.log). The actual
proof then exited 1 with `WarnStuckClaimState`: the residual execution had
reached `.K` with the real list and could not unify with the mutated
destination. This is the expected unmet result obligation, not a parser error,
missing import, timeout, or unrelated crash. Exact output is in
[`spec-vacuity-kprove.log`](evidence/spec-vacuity-kprove.log). The positive
proof is therefore non-vacuous and result-sensitive.

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Under the freshly compiled `MPY`/`VERIFICATION` theory, for every mathematical
K integer pair `A,B` with `A > 0` and `B > 0`, execution from the exact submitted
program term, input `pair(A,B)`, empty environment, and `noResult` reaches
`.K`. At that destination, the environment contains exactly the original
arguments and `result = expected(A,B)`, and the result cell contains the same
value. `expected` is transparently defined as the ascending subsequence of
`2,4,6,8` lying between the endpoints. This is a result-constraining
partial-correctness theorem about the actual generated IR under this semantics.

The proof does not use differential testing, candidate logs, or the candidate's
old `#Top` as proof steps.

### Trust ledger and limitations

| Boundary | Dependents | Assessment |
|---|---|---|
| K `kompile`, `kast`, `krun`, `kprove`, LLVM/Haskell backends | All machine results | Ordinary unavoidable toolchain trust; versions and fresh commands recorded. |
| Built-in `INT`, `BOOL`, `STRING`, `LIST`, and `MAP` modules, including `<=Int`, Boolean connectives, list concatenation, and map lookup/update | Semantic rules and `expected` equations | Acceptable low-level K trust boundary; no task answer is hidden in these primitives. |
| Trusted `/reference/py2mpy.py` | Python-source-to-IR identity | Authority-designated translator. Byte identity proves the submitted IR is exactly its output; it does not independently prove the translator's semantic correctness. |
| Purpose-specific entry harness S1 | Connecting the top-level IR function wrapper and input cell to body execution | Acceptable for this entry-point verification: exact name/parameters, correct bindings, and real body execution. It is not general module/call semantics. |
| Generated semantics as a model of the used Python subset | Bridge from K theorem to `solution.py` behavior | Statically audited rule-by-rule and supported by 20 fresh K/Python executions, but not backed by a universal machine-checked CPython refinement theorem. This is the principal concern. |
| Manual contract bridge from transparent `expected` to the English phrase “even digits between” | Natural-language intent | Mathematically direct and supported by trusted canonical comparison, but informal rather than a separate K theorem. |
| Finite 650-case candidate/canonical differential test | Source implementation-to-canonical evidence | Strong finite evidence with boundary and generated coverage, not a universal proof and not substituted for `kprove`. |

The theorem excludes nonpositive inputs, which is aligned with the trusted
prompt. It does not claim correctness for arbitrary Python programs accepted by
the broad syntax, Python exceptions, mutable aliasing, calls inside the body,
or a `Return` followed by further statements. Those behaviors are unused and
outside this generated semantics' validated scope.

Gate A (real-program soundness and non-vacuity) passes. The claim executes and
pins the body, its equations are truthful, and the false-result mutation fails.
Intent alignment for positive inputs is adequate. Evidence auditability passes,
but the semantics-to-CPython and natural-language bridges remain partly
informal; that limitation warrants `CONCERNS` rather than `PASS` without
invalidating the proof.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
