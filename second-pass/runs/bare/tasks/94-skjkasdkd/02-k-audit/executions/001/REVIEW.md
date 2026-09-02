# Independent adversarial review: 94-skjkasdkd

## Outcome

The candidate contains a legitimate partial-correctness proof of its submitted
translated program under the generated, resource-unbounded K semantics. The
proof was reconstructed from source, all six submitted claims closed as a
dependency-complete family, the entry result is constrained, the submitted
program is pinned exactly, and a fresh false-result mutation was rejected for
the expected logical reason.

The result is `CONCERNS / LEGIT`, rather than an unqualified pass, for three
bridge limitations:

1. The K theorem uses equational reference functions whose connection to the
   English phrase “largest prime and digit sum” is established by ordinary
   mathematical review and finite differential evidence, not by a separate K
   theorem about primality/maximality/decimal notation.
2. CPython recursion limits are outside the generated semantics. The submitted
   recursive Python raises `RecursionError` on a one-element list containing
   `1000003` and on lists of 1000 or 1100 twos, while the K model has an
   unbounded call stack.
3. The trusted canonical implementation treats `1` as prime when no larger
   prime is present. The submitted implementation instead follows the usual
   mathematical definition. The prompt does not specify the no-prime case, so
   this is a real canonical/candidate divergence but not evidence that the
   candidate violates the stated mathematical contract.

No intended integer-list input witness was found on which the K proof can
establish a false returned value.

## 1. Input and provenance integrity

The rendered mode and trusted mounts are consistent. This is
`GENERATED_SEMANTICS`, and `/reference/reference-semantics` is absent. Had that
tree existed, the audit would have stopped as an infrastructure breach.

All required candidate and trusted artifacts are regular files, not symlinks or
mistyped entries. The candidate prompt and translator are byte-identical to
their trusted counterparts:

| Artifact | Trusted/candidate result |
|---|---|
| `prompt.py` | byte-identical, SHA-256 `1c6ca165...25812` |
| `py2mpy.py` | byte-identical, SHA-256 `406485ea...db16` |
| `/reference/canonical.py` | regular trusted file, SHA-256 `d1dd5909...22daa` |
| Structured trace | one regular JSONL file; all 294 records parsed |

The full type/tree/hash check is in
`evidence/01-provenance.log`. The candidate also contains
`semantic-kompiled/`, `verification-kompiled/`, and `__pycache__/`; these are
extra generated build/cache artifacts, not source integrity failures. They
were never copied into or used by the audit build.

`run-input.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, and the structured trace were inspected only as untrusted
claims. They say that one six-claim `kprove` run produced `#Top`; that assertion
was not used as proof evidence. A bounded structural summary, hashes, parsed
event counts, relevant tool calls, and claimed outputs are preserved in
`evidence/04-untrusted-generation-summary.log`.

Evidence:

- `evidence/check_provenance.sh`
- `evidence/01-provenance.log`
- `evidence/summarize_untrusted_generation.py`
- `evidence/04-untrusted-generation-summary.log`

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For a list of integers, find its largest mathematical prime and return the sum
of that prime's base-10 digits. The prompt supplies six examples but does not
say what to return when the list has no prime.

The trusted canonical scans the list, keeps the largest value passing its
nested `isPrime`, converts that maximum to decimal, and sums the digits. Its
`isPrime(1)` returns true because the divisor loop is empty. Consequently,
`canonical.skjkasdkd([1]) == 1`, even though 1 is not mathematically prime.

The candidate uses:

- `is_prime_from(n,d)`: trial division from `d`;
- `is_prime(n)`: rejects values below 2;
- `largest_prime`: structural recursion over list tails, with base value 0;
- `digit_sum`: recursion by quotient and remainder;
- `skjkasdkd`: composition of `largest_prime` and `digit_sum`.

For normally returning executions, this is a faithful alternative algorithm
for the natural-language property.

### Translator identity

The trusted `/reference/py2mpy.py` was run against the scratch copy of
`solution.py`. The regenerated and submitted `solution.mpy` files are
byte-identical, both with SHA-256
`a537d17594c25efbe49fe5a6a69f79faa6e23d4445c269e483dafb5ec4eb678e`.
The exact command and exit status 0 are in
`evidence/03-translator-identity.log`.

### Independent differential

`evidence/differential_test.py` imports the trusted canonical and scratch
candidate by absolute path. It also contains an independently written
mathematical oracle. It executed 23,653 inputs:

- all six prompt examples;
- explicit empty, negative, 0/1/2, square/divisibility, ordering, duplicate,
  digit-sum, and large-prime boundaries;
- every list of length 0 through 4 over
  `(-2,-1,0,1,2,3,4,5,8,9,10,11)` (22,621 inputs);
- 1,000 seeded lists of length 0 through 30 with values from -100 through
  10,000;
- lists of 950, 990, 1000, and 1100 twos.

All six documented examples agree with their expected values. The run found:

| Comparison | Mismatches | Judgment |
|---|---:|---|
| Candidate vs canonical | 1,886 | 1,883 arise from canonical treating 1 as prime; three arise from candidate recursion limits |
| Candidate vs mathematical oracle | 3 | `RecursionError` for `[1000003]` and lengths 1000/1100 |
| Canonical vs mathematical oracle | 1,883 | all are the no-larger-prime cases containing 1 |

The differential exits 1 intentionally because divergences are evidence to
report, not to hide. The complete input construction, first mismatches, command,
and exit are in `evidence/05-differential.log`.

The 1-divergence is not a false candidate result under ordinary mathematics.
The recursion divergences are language-model/resource limitations. Because the
requested theorem is partial correctness, they do not exhibit a normally
returned candidate value violating the postcondition.

## 3. Clean proof reconstruction

Only the source files explicitly copied by
`evidence/00-copy-source.log` were used. Both definitions were freshly built
under `/tmp/audit-work/94-skjkasdkd/build` with K
`v7.1.293`; tool versions are in `evidence/02-tool-versions.log`.

Fresh build commands:

```text
kompile semantic.k --backend haskell --syntax-module MPY-SYNTAX \
  --main-module SEMANTIC \
  --output-definition /tmp/audit-work/94-skjkasdkd/build/semantic-kompiled

kompile verification.k --backend haskell --syntax-module MPY-SYNTAX \
  --main-module VERIFICATION \
  --output-definition /tmp/audit-work/94-skjkasdkd/build/verification-kompiled
```

Both exited 0. See `evidence/06-kompile-semantic.log` and
`evidence/07-kompile-verification.log`.

### Generated-semantics execution

The fresh semantic definition was concretely run on 18 cases covering empty
input, negative-only input, 0/1/2, composite squares, a nearby prime, maximum
ordering, one/two/multiple decimal digits, and all six prompt examples. Every
run exited 0, ended with `.K`, and matched candidate Python and the independent
mathematical oracle. The `[1]` case returned 0 in K and candidate Python while
the canonical returned 1, as already judged above.

Exact per-case `krun` commands and complete final configurations are in
`evidence/09-concrete-semantics.log`.

### Positive claims

The original six-claim command was reconstructed exactly against the fresh
definition:

```text
kprove spec.k \
  --definition /tmp/audit-work/94-skjkasdkd/build/verification-kompiled \
  --spec-module SPEC
```

It exited 0 and printed `#Top`
(`evidence/10-kprove-all-claims.log`).

The submitted claims form a dependency family: `is_prime` uses
`is_prime_from`; `choose_prime` uses both; `largest_prime` uses those three;
and the entry uses the full helper family. The audit added labels without
changing claim bodies and independently proved each target with its dependency
closure:

| Target | Included claims | Result |
|---|---|---|
| `is_prime_from` | itself | `#Top`, exit 0 |
| `is_prime` | `is_prime_from`, `is_prime` | `#Top`, exit 0 |
| `choose_prime` | preceding two plus `choose_prime` | `#Top`, exit 0 |
| `largest_prime` | preceding three plus `largest_prime` | `#Top`, exit 0 |
| `digit_sum` | itself | `#Top`, exit 0 |
| entry | all six | `#Top`, exit 0 |

Evidence is in `evidence/11-kprove-is-prime-from.log`,
`evidence/17-kprove-is-prime-closure.log`,
`evidence/18-kprove-choose-closure.log`,
`evidence/19-kprove-largest-closure.log`,
`evidence/15-kprove-digit-sum.log`, and
`evidence/20-kprove-entry-closure.log`. The labeled audit artifact is
`evidence/spec-labeled.k`.

Diagnostic filters that deliberately removed required helper claims got stuck;
for example, isolated `largest_prime` cannot summarize its call to
`choose_prime`. This is expected dependency sensitivity, not a reconstructed
positive-command failure. The dependency-complete claims themselves are all
proved, rather than assumed.

## 4. Adequacy and real-program pinning

### Claim meanings and satisfiable preconditions

| Claim | Plain-language precondition and postcondition | Satisfying witness |
|---|---|---|
| `is_prime_from` | For integers `N >= 2`, `D >= 2`, invoking the submitted helper returns `refPrimeFrom(N,D)` and preserves the continuation/result cell. | `N=2,D=2`, result `true` |
| `is_prime` | For any K integer `N`, invoking the submitted helper returns `refPrime(N)`. | `N=1`, result `false` |
| `choose_prime` | For any K integers `N,BEST`, return `N` iff it is prime and larger; otherwise return `BEST`. | `N=5,BEST=3`, result `5` |
| `largest_prime` | For `VS:Vals`, return `refLargest(VS)`. Intended calls restrict `VS` to `intVal` elements. | `[4,11,3]`, result `11` |
| `digit_sum` | For any K integer `N`, return `refDigitSum(N)`. Reachable entry calls use `N >= 0`. | `N=123`, result `6` |
| entry | Starting from `noResult`, consume the submitted program and set the result to exactly `intVal(refAnswer(VS))`. | `[4,11,3]`, result `2` |

The ground K claims all printed `#Top` and exited 0
(`evidence/22-kprove-ground-witnesses.log`,
`evidence/spec-ground.k`). Candidate helper execution and both Python entry
points agree on the concrete entry witness
(`evidence/23-ground-python.log`).

### Program identity

The entry claim names a `solutionProgram` macro rather than opening a file at
proof time. This is not a substitution gap: the audit parsed the submitted
`solution.mpy` and independently parsed and macro-expanded `solutionProgram`
under the fresh verification definition. Their expanded KORE terms are
byte-identical with SHA-256
`41abd9460ba9fe574958f5a1d101c661f497de799aa6a8afda047866e07a4875`.
See `evidence/check_program_pinning.sh` and
`evidence/21-program-pinning.log`.

The macro contains all six submitted definitions and matches their parameters,
body statements, operators, recursive calls, index, and slice exactly.

### Result constraint and control-flow fit

Every variable in the entry postcondition is fixed by the initial state; there
is no RHS-only existential, free result variable, tautological `ensures`, or
one-way implication. The entry consumes `<k>` to `.K` and rewrites
`noResult` to the exact result. The false mutation in stage 6 confirms that
this equality is proof-relevant.

The five helper claims begin at the actual invocation configurations reached by
the program. They summarize normal function return while framing an arbitrary
continuation. This context is justified here because the generated semantics
passes environments explicitly, has no heap/output/exception/control-stack
cell, a returned `Val` resumes the existing K continuation, and helper calls do
not touch `<result>`. Recursive calls return to the same stable invocation
shape, so the claims act as ordinary reachability circularities/induction
summaries for real control flow.

## 5. Rule-by-rule static soundness review

There are no additional helper K files. The complete numbered source and
declaration index are in `evidence/24-k-rule-inventory.log`.

### Local declarations

`MPY-SYNTAX` declares exactly these source constructors:

- `Module`; statement lists; `FuncDef`, `Return`, and `If`;
- parameter/string and expression lists;
- `Int`, `Bool`, `Name`, `BinOp`, `BoolOp`, `Compare`, `Call`, and
  `Subscript`;
- comparison lists/operators; expression indexes; `Slice`; expression and
  `NoBound` bounds.

`SEMANTIC` declares `intVal`, `boolVal`, `listVal`, value lists, function
definitions, result values, and the 20 continuation/control KItems from
`init` through `finish`. Its configuration has only `<k>` and `<result>`,
which is adequate because this program has no assignments, mutation, heap,
I/O, exceptions, closures, or allocation.

Function declarations in `semantic.k` are:
`collectDefs`, `getDef`, `lookupEnv`, `bind`, `valLength`, `intHead`,
`intTail`, and `appendStmts`. None is declared `total`.

`verification.k` adds the `solutionProgram` and `solutionDefs` macros;
`programDefs`; and `refPrimeFrom`, `refPrime`, `refChoose`, `refLargest`,
`refDigitSum`, and `refAnswer`. Only `refPrimeFrom` and `refPrime` are marked
`[total]`.

There are no local `[simplification]`, priority, `[opaque]`, or explicit
`[functional]` declarations. There are no proof-local operational rewrite
bridges that replace a program body.

### Construct-to-rule coverage

| Construct used in `solution.mpy` | Declaration and execution rules | Judgment |
|---|---|---|
| Module and six functions | `Module`, `FuncDef`; `collectDefs`; `invokeProgram`, `invoke`, `invokeDef` | All names are unique and every called definition exists. |
| Parameters and names | `Params`, string lists; `bind`, `lookupEnv` | Exact arities and bindings hold for every actual call. |
| `If` and `Return` | `execStmts`; two complementary `returnIf` rules | Branch guards are disjoint; return discards the remaining function body as Python does. |
| Integer/Boolean literals and names | three base `eval` rules | Exact for used values. |
| `+`, `*`, `%`, `//` | left-to-right `binLeft`/`binRight` rules | Exact on reachable nonnegative operands and positive divisors. |
| `<`, `>`, `==` | left-to-right comparison rules | Exact for the integer operands used. |
| `and` | `andLeft`, `andRight` | Final Boolean is correct for the actual pure, total RHS; general Python short-circuiting is not modeled. |
| Calls and arguments | `evalArgs`, `argsRest`, `prependArg`, `callWith` | Arguments evaluate left-to-right and are restored in original order. |
| `len` | dedicated `callWith("len",...)` rule | Exact for the only use, a `listVal`. |
| `lst[0]`, `lst[1:]` | guarded head and exact slice rules | Both are reached only after the nonempty guard. |
| Final result | `init ... ~> finish` and `finish` | The only observable result is written once from the returned value. |

### All 48 semantic rules

The following groups account for and decide every rule in `semantic.k`:

| Rules | Count | Decision |
|---|---:|---|
| `collectDefs` empty/cons | 2 | Truthful structural fold for the six unique definitions. |
| `getDef`, `lookupEnv` | 2 | Truthful map lookup; intentionally stuck on missing keys, which are unreachable here. |
| `bind` empty/cons | 2 | Truthful exact-arity parameter binding. |
| `valLength` empty/cons; `intHead`; `intTail` | 4 | Truthful for lists of integer values; head/tail deliberately partial on empty or non-integer heads. |
| `appendStmts` empty/cons | 2 | Truthful statement-list concatenation. |
| `init`, `invokeProgram`, `invoke`, `invokeDef` | 4 | Correct entry selection, definition lookup, fresh parameter environment, and continuation preservation. |
| `execStmts(Return)`, `execStmts(If)`, true/false `returnIf` | 4 | Correct return and branch control; Boolean guards are complementary. |
| literal/name evaluation | 3 | Direct and state-preserving. |
| binary setup/second-operand plus four operators | 6 | Left-to-right and mathematically correct on every reachable operand pair. |
| comparison setup/second-operand plus three comparisons | 5 | Left-to-right and correct on used integer pairs. |
| Boolean-and setup/RHS/result | 3 | Correct returned Boolean for the actual expression; see limitation below. |
| call setup, empty/nonempty args, arg continuation/prepend, `len`, user call | 7 | Left-to-right call evaluation and exact builtin dispatch. |
| subscript setup, index 0, slice 1-to-end | 3 | Correct and guarded for actual AST forms. |
| `finish` | 1 | Correctly consumes the final value and writes the sole observable cell. |

Total: 48.

No rule changes hidden state because there is no such state in the selected
program subset. The function-call continuation supplies the effective call
stack; explicit environment terms supply local binding, and callers' pending
K continuations retain caller context.

### All 15 verification rules

| Rules | Count | Decision |
|---|---:|---|
| `solutionProgram` macro | 1 | Exact submitted AST, independently pinned in stage 4. |
| `programDefs`, `solutionDefs` | 2 | Definitional expansion to the same collected definitions. |
| three `refPrimeFrom` equations | 3 | Disjoint and exhaustive for the proved domain `N>=2,D>=2`; divisor increases until `D*D>N`. |
| two `refPrime` equations | 2 | Disjoint/exhaustive over all integers; excludes values below 2. |
| two `refChoose` equations | 2 | A Boolean condition and its negation; disjoint and exhaustive. |
| two `refLargest` equations | 2 | Empty/nonempty split; structural descent by `intTail`. |
| two `refDigitSum` equations | 2 | Disjoint split at 10; for reachable `N>=0`, quotient strictly decreases and remainder is the last decimal digit. |
| `refAnswer` | 1 | Pure composition of the previous summaries. |

Total: 15.

For integer lists, these equations define: primality by trial division,
selection of the larger prime, a structural largest-prime fold with default 0,
and decimal digit sum. Thus `refAnswer` has the intended mathematical meaning
on the entry domain.

### Narrow limitations, with witnesses

Two broad declarations are inaccurate outside the submitted program's intended
calls:

1. The `and` rules eagerly evaluate the RHS. The admitted test term
   `False and (1 % 0)` returns `False` in Python but leaves K stuck at division
   by zero. The exact witness is
   `evidence/eager-and-witness.mpy`; results are in
   `evidence/28-eager-and.log`. The only actual `and` RHS is the pure integer
   comparison `n > best`, so no integer-list input can expose this difference.
2. `[total]` on `refPrimeFrom(Int,Int)` is broader than its equations. At
   `refPrimeFrom(5,0)`, `D*D>N` is false and both remaining guards require
   modulo by zero; concrete evaluation leaves the function term unreduced.
   Valid probes `(5,2)` and `(4,2)` reduce to true and false. See
   `evidence/27-refprimefrom-totality.log`. Every dependent proof occurrence
   has `N>=2,D>=2`, so this unsupported totality region is outside the claim
   precondition and entry execution.

Under the audit instruction requiring an intended-domain false-conclusion
witness, neither issue is labeled a materially unsound proof rule. They are
scope/evidence gaps and reasons for `CONCERNS`. Similarly, K's unbounded
integers and call stack deliberately omit CPython resource exceptions.

No rule was found that encodes an unconnected answer, fabricates a used
construct's result, replaces program-defined execution with an oracle, or makes
a false returned result provable on an intended integer-list input.

## 6. Fresh non-vacuity test

The candidate supplied no mutation evidence. The audit created a fresh
`SPEC-VACUITY` artifact preserving all five helper obligations and changing
only the entry result to:

```text
result(intVal(refAnswer(VS) +Int 1))
```

This is demonstrably false for the satisfying witness `VS = intVal(2)`: both
Python implementations and concrete K return 2, while the mutation requires 3.

The mutation compiled to KORE successfully with `kprove --dry-run` (exit 0,
`evidence/25-vacuity-dry-run.log`). The real proof exited 1 with
`WarnStuckClaimState`; its residual final configuration contains the actual
`refDigitSum(refLargest(VS))` and the unmet equality against the same value plus
1. This is the expected logical failure, not a parser error, missing import,
timeout, or unrelated crash.

Artifacts:

- `evidence/spec-vacuity.k`
- `evidence/25-vacuity-dry-run.log`
- `evidence/26-vacuity-proof.log`

## 7. Proven versus assumed accounting

### What the reachability proof establishes

Under the rules in `semantic.k` and equations in `verification.k`, the six
dependency-complete reachability claims establish:

- exact return summaries for the five submitted recursive helpers; and
- for every initial `listVal(VS)` covered by the K term, if execution reaches a
  final result, `<k>` is consumed and `<result>` is exactly
  `result(intVal(refAnswer(VS)))`.

On the intended subdomain where every member of `VS` is `intVal(I)`,
`refAnswer` is the decimal digit sum of the largest mathematical prime, with 0
as the implementation's no-prime default.

This is partial correctness. It does not prove CPython termination, absence of
`RecursionError`, complexity bounds, or behavior for non-integer list members.

### Trust ledger

| Boundary | Dependents | Accounting |
|---|---|---|
| K v7.1.293 compiler, Haskell backend, reachability logic, and Z3 | All claims | Ordinary machine-checking trust boundary; version and fresh commands recorded. |
| Builtin `INT`, `BOOL`, `STRING`, and `MAP` operations | Semantics and reference equations | Trusted primitives. Reachable arithmetic uses nonnegative values/positive divisors where Python and K agree. |
| Trusted translator `/reference/py2mpy.py` | Program identity | Its correctness as a Python-AST encoder is trusted; its output identity is proved byte-for-byte. |
| Generated Python-subset semantics | Bridge from AST to execution | Not assumed wholesale: construct coverage, all 48 rules, concrete boundary runs, evaluation/control/state behavior, and limitations were audited. |
| `refPrimeFrom`, `refPrime`, `refChoose`, `refLargest`, `refDigitSum`, `refAnswer` | Formal postconditions | Definitional summaries, not operational bridges. Their equations are reviewed mathematically; no opaque value remains in the intended domain. |
| English-intent bridge | Human-facing theorem statement | Informal mathematics plus finite differential evidence; no separate K theorem defines “prime”, “maximum”, or decimal representation independently. |
| Unbounded stack/resource model | Large inputs | Conditional idealization. Concrete CPython recursion counterexamples are preserved and excluded from any termination claim. |
| Trusted canonical | Differential comparison only | It supports all examples and most tested inputs, but its `1` bug prevents treating it as a universal mathematical oracle. |

There are no opaque local symbols, fresh unconstrained result values, empirical
operational bridges, hidden generated-semantics files, or proof-local
simplification/priority rules. Differential testing supports the
Python/K/intent bridge only on the tested inputs; it is not used as a substitute
for the successful K reachability proof.

### Final decision

The proof is sound and result-constraining for the real submitted translated
program under its stated generated semantics. Program identity, executable
semantics, all positive claims, dependency structure, and non-vacuity were
independently confirmed. The canonical edge disagreement, resource-unbounded
execution model, broad off-path declarations, and informal English-intent
bridge are documented limitations, but none supplies an intended-domain false
returned-value witness or an execution bypass.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
