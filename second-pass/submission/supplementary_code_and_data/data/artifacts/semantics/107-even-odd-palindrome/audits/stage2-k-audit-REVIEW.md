# Independent adversarial review: 107-even-odd-palindrome

The candidate contains a legitimate, reconstructible partial-correctness proof
of its real generated program over the complete documented domain
`1 <= n <= 1000`. I found no execution-bypassing rule, result oracle, vacuous
precondition, substituted program, or domain restriction. I assign
`CONCERNS / LEGIT`, rather than `PASS / LEGIT`, for one non-fatal limitation:
the K postcondition defines the intended palindrome counts by closed-form
equations, and the equivalence of those equations to “count even/odd
palindromes” is established by ordinary finite mathematics and exhaustive
independent testing, not by a K predicate that defines decimal palindromicity.

All candidate and generation records were treated as untrusted evidence. All
execution used source-only copies under
`/tmp/audit-work/107-even-odd-palindrome`, with new definition directories.
Reviewer scripts, mutations, and bounded command logs are under
`/audit-output/evidence/`.

## 1. Input and provenance integrity

`/audit-input.json` is a regular readable file and declares:

- problem `107-even-odd-palindrome`;
- condition `semantics`;
- semantics mode `SUPPLIED_SEMANTICS`;
- record layout `legacy-selected-stage1`;
- mounted paths under `/candidate`, `/reference`, and
  `/generation-evidence`.

The rendered mode and trusted mounts agree:
`/reference/reference-semantics` is present. Therefore this is not an
infrastructure-error case.

The campaign object in `/audit-input.json` is structurally identical to
`/audit-campaign-lock.json`. The lock's independently computed SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
matching the launcher record. The canonical, trusted prompt, translator,
run/task/result manifests, invocation, metrics, optional usage, prompt,
Codex last/output records, and structured trace all independently match their
recorded hashes. The single trace JSONL file matches the hash declared in
`generation-result.json`; all 225 JSONL records parse. See
`evidence/02-integrity-python.log` and
`evidence/10-trace-summary.log`.

Every record required by `legacy-selected-stage1` is present and regular:
`/run.json`, `/task.json`, `/generation-result.json`,
`invocation.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, `prompt.txt`, and the structured trace. `usage.json` is
present and was inspected. `runtime-metrics.json` is absent, but that record is
not required for this historical layout and was not reconstructed. The raw
record inspection is preserved in `evidence/01-required-records.log`.

There are no symlinks anywhere in the candidate, trusted reference, or
generation-evidence mounts. The candidate's `prompt.py` and `py2mpy.py` are
byte-identical to the trusted versions. A recursive, no-dereference comparison
of `/candidate/reference-semantics` with
`/reference/reference-semantics` finds no missing, additional, changed,
mistyped, or symlinked entry. Reviewer-defined per-entry manifests give the
same tree digest
`a04a6aafd8ea8948ec81604d244d95fbbdbe0460f09344a297a12de0f90f6c94`
for both semantics trees. See `evidence/04-trusted-semantics-tree.log`,
`evidence/05-candidate-semantics-tree.log`, and
`evidence/06-byte-comparisons.log`.

The generation records claim prior success, but no conclusion below relies on
that claim, its compiled artifacts, or its logs.

Stage result: integrity passes; no audit infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt's contract is:

> Given an integer `n` with `1 <= n <= 1000`, return a pair whose first
> component is the number of even decimal palindromic integers in inclusive
> range `1..n`, and whose second component is the number of odd ones.

The trusted canonical iterates over every integer, tests decimal-string
reversal, and increments the appropriate parity count. The submitted
`solution.py` uses a different but valid closed form:

- below 10, all values are one-digit palindromes;
- below 100, the additional palindromes are `11, 22, ..., 99`;
- for a three-digit input with leading digit `a`, all prior leading-digit
  blocks have ten palindromes and the current block counts values
  `101*a + 10*b` not exceeding `n`;
- `1000` adds no palindrome beyond `999`, yielding `(48, 60)`.

The trusted translator regenerated `solution.mpy` with SHA-256
`cc7a50bf0a19c016af4c35d9a2d1c63d6fc0d8dc3c87a35594df3e0096516c67`.
It is byte-identical to the submission
(`evidence/12-regenerate-mpy.log`).

`evidence/differential_test.py` imports the trusted canonical and submitted
entry points independently. It covers the examples `3` and `12`, the minimal
positive/empty-prefix case `1`, every submitted branch boundary, a fixed-seed
set of 62 generated values, and exhaustively all 1,000 integers in the intended
domain. It also compares both implementations to an independently written
direct enumeration oracle. The command exits 0 with 1,000 cases and zero
mismatches (`evidence/13-differential.log`). No conclusion is drawn about
out-of-contract inputs.

Stage result: program fidelity passes over the complete intended domain.

## 3. Clean proof reconstruction

The scratch tree contains only copied sources and trusted inputs. Candidate
compiled definitions/caches were neither copied nor reused. K is independently
installed at `/usr/bin`; `kompile`, `krun`, and `kprove` all report version
7.1.293 (`evidence/08-toolchain.log`).

Fresh concrete definition:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled-audit
```

This exits 0 (`evidence/16-kompile-llvm-fresh.log`). A reviewer harness whose
function AST is identical to submitted `solution.py` was translated by the
trusted translator. It executes representative normal/boundary assertions:

```text
krun concrete_harness.mpy --definition runtime-kompiled-audit
```

The command exits 0 with `.K`, `NoExc`, and exit code 0
(`evidence/14-concrete-harness-translate.log`,
`evidence/17-krun-concrete-fresh.log`).

Fresh proof definition:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled-audit
```

This exits 0 (`evidence/15-kompile-haskell-fresh.log`). The exact submitted
spec then closes:

```text
kprove spec.k --definition verification-kompiled-audit \
  --spec-module SPEC
```

It exits 0 and prints `#Top`
(`evidence/18-kprove-all-fresh.log`).

For independent per-claim confirmation, `spec-labelled.k` differs only in the
module name and four labels (`evidence/19-labelled-spec-diff.log`). Each claim
was selected and run separately:

- `SPEC-LABELLED.region-1-to-9`: exit 0, `#Top`;
- `SPEC-LABELLED.region-10-to-99`: exit 0, `#Top`;
- `SPEC-LABELLED.region-100-to-999`: exit 0, `#Top`;
- `SPEC-LABELLED.region-1000`: exit 0, `#Top`.

The exact commands and outputs are in
`evidence/20-kprove-claim-1-to-9.log` through
`evidence/23-kprove-claim-1000.log`.

Compiler warnings concern supplied, unused semantics declarations (notably
string-tail variables and LLVM-only totality warnings). No positive command
timed out, crashed, or relied on a candidate definition.

Stage result: clean reconstruction passes.

## 4. Adequacy and real-program pinning

The four entry claims say, in plain language:

1. for every integer `1 <= N < 10`, run the generated module and return
   `(evenPalindromes(N), oddPalindromes(N))`;
2. the same for every integer `10 <= N < 100`;
3. the same for every integer `100 <= N < 1000`;
4. the same for `N = 1000`.

Every claim starts from the standard exact configuration: module environment
0, empty module map, builtin parent, empty heap and stack, `noRet`, `NoExc`,
and exit code 0. Every destination consumes the computation, constrains the
returned tuple's two concrete components, preserves the heap/stack/control
state, restores `noRet`, and adds exactly the expected top-level closure.
There is no free RHS result, existential result variable, implication-only
postcondition, or omitted result-bearing cell.

The preconditions are pairwise disjoint and their union is exactly the prompt's
domain. Satisfying witnesses are `N = 1, 10, 100, 1000`. Ground substitution
gives respectively `(0,1)`, `(4,5)`, `(8,10)`, `(48,60)` from the K-side
formula, submitted Python, and trusted canonical
(`evidence/25-precondition-witnesses.log`).

`#runEvenOdd(N)` expands to:

```text
#loadAll(solutionModule) ~> Call(Name("even_odd_palindrome"), N)
```

Thus fixed semantics loads the function, performs ordinary binding and lookup,
evaluates the argument, pushes a call frame, binds `n`, executes every reached
statement, returns, and pops the frame. It is not an operational summary of
the result.

The manual program term is pinned mechanically. The reviewer comparator
extracts the trusted-regenerated `FuncDef` body and the `solutionBody` equation,
normalizes only whitespace and explicit-versus-empty `.Stmts`, and verifies the
function name, parameter list, constructor body, and module binding. Both
normalized bodies have SHA-256
`6d3df5c2ced6c071b428bfed83a98bc0dea1948e2009845f195aab54c1e064d3`
(`evidence/24b-program-term-comparison-corrected.log`). An earlier comparator
run in `evidence/24-program-term-comparison.log` failed because the reviewer
script mistakenly parsed the operator string `"//"` as a comment; the
reviewer script was corrected before any conclusion was drawn.

Body sensitivity was checked separately. The scratch mutation changes the
first-branch executed denominator from `Int(2)` to `Int(1)`, not merely an
external Python file (`evidence/31-body-mutation-diff.log`). The mutated
definition and original `N = 1` result obligation both build successfully
(`evidence/32-kompile-body-mutant.log`,
`evidence/33-body-mutant-dry-run.log`). Proof then exits 1 with
`WarnStuckClaimState`: the mutated real body returns `(1,1)`, which does not
match the original `(0,1)` summary
(`evidence/34-body-mutant-expected-failure.log`).

Stage result: the theorem is result-constraining and pins the real submitted
program over the full source domain.

## 5. Rule-by-rule static soundness review

`evidence/k_inventory.py` inventories every declaration block in the supplied
semantics, `verification.k`, and `spec.k`. The preserved exhaustive ledger
contains:

```text
1 configuration
234 syntax declarations
5 evaluation contexts
708 rules
4 claims
```

Every item is shown with file, line, and complete declaration/rule block in
`evidence/27-k-inventory.log`. `evidence/28-special-attributes.log` separately
enumerates functions, totality, concrete/opaque symbols, priorities, macros,
strictness, and owise rules. Per-file and per-proof-rule judgments are in
`evidence/rule-review.md`.

The constructs used by `solution.mpy` map as follows:

| Used construct | Declaration/evaluation |
|---|---|
| module/function/parameter/statement sequence | `syntax.k`; `core.k:123-127`; `functions.k:14-16` |
| names and integer literals | `core.k:129-154`, `core.k:193-196` |
| call and return | `call.k:18-21,69-74`; `functions.k:62-90` |
| `BinOp` and integer arithmetic | `syntax.k` seqstrict; `operators.k:12`; `int.k:9-20` |
| compare and guards | `operators.k:14-17`; `int.k:22-27`; `controls.k:50-54` |
| assignment/augmented assignment | `controls.k:8-31` |
| tuple construction | `tuple.k:13-16`; shared left-to-right argument loop in `core.k:183-191` |

The active rules preserve Python's relevant binding, evaluation order,
unbounded integer behavior, positive-divisor floor division/modulo, control,
scope changes, stack lifecycle, and returned tuple. The program performs no
allocation, I/O, exception, or external call.

The proof-local inventory has seven syntax declarations and thirteen rules:

- `solutionBody` and `solutionModule` are complete definitional equations for
  the mechanically matched program;
- `#runEvenOdd` is only an exact load-and-call entry wrapper;
- total `leadingDigit` and `currentBlock` each have one unconditional,
  terminating integer equation;
- the four `evenPalindromes` equations and four `oddPalindromes` equations
  have satisfiable, pairwise-disjoint guards covering exactly `1..1000`;
- none of these equations is a simplification rule, priority rule, opaque
  symbol, or execution bridge.

The palindrome formulas follow ordinary mathematics. Three-digit palindromes
are exactly `101*a + 10*b`; their parity is the parity of `a`, completed
leading-digit blocks contain ten values, and `currentBlock` counts admissible
`b` in the active block. One- and two-digit cases and the `1000` endpoint give
the other equations. No proof-local rule has a false overlap or uncovered use.

The fixed semantics contains 25 opaque `symbol(...)` declarations: 22 float
symbols plus `md5hexCodes`, `sortVS`, and `sortKeyVS`. None is reachable from
this integer-only program or its postcondition. All priority rules are supplied
fixed semantics; none preempts a used operation with a summary. There are no
candidate simplification rules or auxiliary circularity claims. I found no
unsound candidate rule, so there is no false-conclusion witness to report.
For unused fixed-semantics features, the narrower finding is simply that they
are outside this theorem's dependency slice; they were inventoried but are not
claimed to validate full Python.

Stage result: static soundness passes for every proof dependency; no smuggled
correctness conclusion or execution bypass is present.

## 6. Fresh non-vacuity test

The reviewer-authored `spec-vacuity.k` fixes the satisfiable original-region
input `N = 1` and mutates only the result obligation from the true `(0,1)` to
the false `(1,1)` (`evidence/spec-vacuity.k`).

The dry run:

```text
kprove spec-vacuity.k --definition verification-kompiled-audit \
  --spec-module SPEC-VACUITY --dry-run
```

exits 0 and emits a valid `kore-exec` command, proving the mutation parses and
builds (`evidence/29-vacuity-dry-run.log`). The real proof command exits 1 with
`WarnStuckClaimState`. Its residual explicitly contains the actual
`tuple(vCons(0, vCons(1, .ValSeq)))`, which cannot unify with the mutated
destination; the failure is not a parser error, timeout, missing import, or
unreachable mutation (`evidence/30-vacuity-expected-failure.log`).

Stage result: non-vacuity passes.

## 7. Proven versus assumed accounting

### What the K proof establishes

Under the supplied `MPY` semantics and standard initial configuration, for
every integer `N` in `1..1000`, execution of the exact translated submitted
function is partially correct with respect to the displayed closed forms:
whenever the reachability obligation terminates, the only accepted result is
the two-element tuple
`(evenPalindromes(N), oddPalindromes(N))`, with the claimed final control,
scope, heap, and stack state. Each of the four universal/singleton claims
machine-closes independently.

### Trust and assumption ledger

- **K builtins/backend/SMT:** integer, Boolean, string-token, map/list, equality,
  strictness, rewriting, and solver implementations are foundational trusted
  primitives. They directly support every claim and are an acceptable
  toolchain boundary.
- **Supplied MPY semantics:** the exact trusted tree defines the Python subset.
  Only its integer/function/control/tuple path is material. This is the
  benchmark-selected semantics boundary; the candidate did not alter it.
- **Trusted translator:** byte regeneration proves that submitted
  `solution.mpy` is the trusted transliterator's output. The transliterator's
  fidelity to CPython AST construction is a trusted front-end boundary, aided
  by direct constructor and Python-AST comparison.
- **Opaque fixed-semantics symbols:** the 25 float/sort/MD5 symbols are assumed
  where their unrelated modules use them, but no target claim depends on them.
- **Closed-form-to-natural-contract bridge:** the equivalence between the K
  closed forms and decimal palindrome counting is an informal finite
  mathematical argument, not a K theorem over a formal palindrome predicate.
  Exhaustive independent comparison against the trusted canonical and a direct
  oracle gives zero mismatches over the entire finite source domain. This is
  strong reproducible evidence but is not substituted for the K execution
  proof.
- **Termination:** the reported theorem is partial correctness as requested.
  The submitted branches are loop-free, and both concrete and symbolic
  executions finish, but the verdict does not broaden the theorem into a
  separately formalized total-correctness result.

Gate A (real-program soundness and non-vacuity) passes. The theorem covers the
entire source-contract domain and its formulas are extensionally correct, so
there is no material adequacy failure or HumanEval-domain narrowing. Evidence
and trust boundaries are reproducible. The remaining informal
summary-to-natural-language bridge is a non-fatal validation limitation and
therefore maps to `CONCERNS / LEGIT`, not `FAIL / NOT_LEGIT`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
