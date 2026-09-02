# Independent adversarial review: HumanEval/25 `factorize`

## Decision

The candidate is **not a legitimate proof of the requested unrestricted
HumanEval program contract**.

The clean reconstruction is real but much narrower than the requested theorem:
it proves 26 ground claims for exactly 13 constants

`{1, 2, 3, 4, 8, 9, 13, 25, 31, 70, 100, 360, 999}`.

There is no symbolic entry claim, quantified positive-integer input, invariant,
or induction covering any other input. The first 13 claims prove exact lists at
those constants; the other 13 prove the product/order/primality predicate at the
same constants. The benchmark decision rule expressly maps this materially
narrow `SOUND-BUT-LIMITED` situation to `FAIL / NOT_LEGIT`, not to concerns.

There is an independent real-program gap as well. The submitted recursive
`solution.py` raises `RecursionError` for the positive primes 999,983 and
1,000,003, while the trusted canonical implementation returns the singleton
prime list. The generated K semantics has an unbounded call stack and returns
`[1000003]` at the latter input. Thus it does not model a material real control
outcome over the unrestricted positive-integer domain.

The positive ground results are not vacuous: all 26 reconstruct cleanly, the
program constructor term is pinned, a body mutation changes the result and
breaks a claim, and a fresh false postcondition is rejected. Those facts do not
enlarge the theorem beyond its 13 fixed inputs.

All reviewer scripts, exact commands, exit statuses, and bounded outputs are
under [`evidence/`](evidence/). A compact command index is
[`evidence/COMMANDS.md`](evidence/COMMANDS.md).

## 1. Input and provenance integrity

### Launcher records and layout

`/audit-input.json` declares:

- problem `25-factorize`;
- condition `bare`;
- `record_layout = legacy-selected-stage1`;
- `semantics_mode = GENERATED_SEMANTICS`;
- no mounted reference semantics.

All records required for that layout are present, readable, real regular files
or real directories, and not symlinks:

- `/run.json`, `/task.json`, `/generation-result.json`;
- `/generation-evidence/invocation.json`,
  `metrics.json`, `codex-last.txt`, `codex-output.log`, and `prompt.txt`;
- the structured trace below `/generation-evidence/codex-trace/`;
- optional legacy `usage.json`, which was present and inspected.

`runtime-metrics.json` is absent, which is explicitly permitted for this legacy
layout. Historical runtime/image records were not reconstructed.

The generated-semantics boundary is consistent: `/reference/reference-semantics`
does not exist, and the candidate provides `semantic.k`. There is no
infrastructure-mode contradiction.

### Hashes, campaign lock, and trace

The campaign-lock JSON object equals `audit_input.audit_campaign`, and the
mounted lock hash is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
matching the launcher record. The declared hashes of the canonical source,
trusted prompt, trusted translator, run/task/result/invocation/metrics records,
generation prompt, generation output, final message, and optional usage record
all match independently computed SHA-256 values.

Every evidence output listed in `generation-result.json`, including the sole
trace JSONL file, independently matches its per-file recorded hash. The
structured trace parses completely: one file, 621 JSON objects. The full
generation output, final message, prompt, and trace were read; relevant
untrusted generation actions are preserved in bounded form.

The candidate has ten regular source artifacts and no links or unsupported
entries. Its independently reproduced pipeline tree digest is
`15783d0036ebdd0ab1e582274d0790860721a1565b45dffc9e1cccfccdea0658`,
matching both the invocation's retained-workspace hash and the generation
result's workspace hash. The structured-trace pipeline digest similarly matches
`usage.json`.

`/candidate/prompt.py` is byte-identical to `/reference/prompt.py`, and
`/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`. The trusted
hashes are respectively:

- prompt:
  `b619821eb84b3f0f1296d3f955acfcd54e9f78bc70d2f06929cdfc08fd6b3788`;
- translator:
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.

The mounts report read-only options. K tools independently report version
7.1.293, matching the campaign record.

Evidence:

- [`evidence/stage1_integrity.py`](evidence/stage1_integrity.py)
- [`evidence/stage1_integrity.log`](evidence/stage1_integrity.log)
- [`evidence/stage1_generation_summary.py`](evidence/stage1_generation_summary.py)

**Stage 1 result: PASS.** There is no audit infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

The trusted prompt asks `factorize(n: int) -> List[int]` to return the prime
factors of a given positive integer in nondecreasing order, with multiplicity,
whose product is the input. Examples are:

- `factorize(8) == [2, 2, 2]`;
- `factorize(25) == [5, 5]`;
- `factorize(70) == [2, 5, 7]`.

Although the prompt does not spell out `n >= 1` as a formal precondition, prime
factorization plus the product requirement determines the meaningful source
domain as positive integers. The empty factorization at `n = 1` has product 1.
Zero and negative integers were recorded separately, not used to manufacture a
candidate-domain mismatch.

The trusted canonical implementation performs iterative trial division from 2,
appending repeated factors and finally any residual factor greater than 1.

The candidate uses a different recursive trial-division algorithm:

1. return `[]` when `n < 2`;
2. return `[n]` when `divisor² > n`;
3. when divisible, prepend the divisor and recurse on the quotient with the
   same divisor;
4. otherwise increment the divisor.

This computes the same mathematical lists when it returns, but recursion depth
is a material implementation difference.

### Trusted regeneration

Running the trusted translator on scratch-copied `solution.py` produced SHA-256
`bf6ee159f1b49574a2720939d30a6d1ee0f2ebae7e4e46729f888c54c676714e`.
The submitted `solution.mpy` has the same hash and is byte-identical.

### Independent differential execution

The differential script imports the trusted canonical entry point and the
submitted generated entry point under distinct module names. It covers:

- all three documented examples;
- `n = 1` and branch/equality boundaries around primes, squares, repeated
  factors, and mixed composites;
- every `n` from 1 through 2,000;
- 300 deterministic generated inputs from 1 through 200,000;
- the recursion-boundary primes 999,983 and 1,000,003;
- separate observations at `-2`, `-1`, and `0`.

There were zero returned-value contract failures and two result/exception
mismatches among 2,296 unique intended-domain inputs:

| Input | Trusted canonical | Candidate |
|---:|---|---|
| 999,983 | `[999983]` | raises `RecursionError` |
| 1,000,003 | `[1000003]` | raises `RecursionError` |

This is a material divergence on the unrestricted positive-integer source
domain. It is finite evidence of the divergence and not a substitute for the K
proof.

Evidence:

- [`evidence/differential_factorize.py`](evidence/differential_factorize.py)
- [`evidence/stage2_program_fidelity.log`](evidence/stage2_program_fidelity.log)

**Stage 2 result: FAIL for unrestricted implementation fidelity.** Translation
identity passes; the generated Python implementation does not agree with the
trusted canonical behavior throughout the intended domain.

## 3. Clean proof reconstruction

### Source-only builds

The candidate's ten mounted artifacts contain no compiled definitions or
caches. They were copied to `/tmp/audit-work/25-factorize`; all definitions were
built there from source. No candidate-provided kompiled output was reused.

Fresh Haskell builds both exited 0:

```text
kompile semantic.k --backend haskell --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition fresh-semantic-kompiled

kompile verification.k --backend haskell --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition fresh-verification-kompiled
```

A fresh LLVM concrete definition also built with exit 0.

### Generated-semantics concrete execution

Fresh LLVM `krun` executions covered `-1, 0, 1, 2, 3, 4, 8, 9, 25, 70, 999,
1000003`. Every `krun` invocation exited 0. For positive inputs, the K result
matched the trusted canonical result on all tested cases. It matched actual
`solution.py` on the ordinary cases but not at 1,000,003:

```text
K=('return', [1000003])
canonical=('return', [1000003])
candidate=('raise', 'RecursionError')
```

That result identifies an execution-model difference, not a K-tool timeout.
An earlier Haskell concrete diagnostic for the large prime was interrupted
after it ran slowly; the fresh LLVM definition completed the same check in
about one second, so no verdict rests on the interrupted diagnostic.

### Every positive claim independently

The reviewer mechanically split `spec.k` into 26 single-claim spec modules and
ran each separately against `fresh-verification-kompiled`. All 26 commands
exited 0 and printed `#Top`. The backend reported every claim as
`WarnTrivialClaim: Claim proven without rewriting`; this is consistent with
ground normalization of the `[function]`-declared `Machine` and proof helper
terms. It is not evidence of a symbolic theorem.

Evidence:

- [`evidence/stage3_build.log`](evidence/stage3_build.log)
- [`evidence/stage3_llvm_build.log`](evidence/stage3_llvm_build.log)
- [`evidence/compare_generated_semantics.py`](evidence/compare_generated_semantics.py)
- [`evidence/stage3_concrete_execution.log`](evidence/stage3_concrete_execution.log)
- [`evidence/split_positive_claims.py`](evidence/split_positive_claims.py)
- [`evidence/stage3_positive_claims.log`](evidence/stage3_positive_claims.log)
- the individual specs/logs in [`evidence/positive-claims/`](evidence/positive-claims/)

**Stage 3 result:** reconstruction and all submitted positive commands pass,
but the concrete generated semantics does not faithfully reproduce the real
program's recursion outcome across the intended domain.

## 4. Adequacy and real-program pinning

### Plain-language claim scope

No claim has a symbolic input or an input precondition. Each source is already
a fully ground term. The exact-output and contract claims are:

| Claims | Ground input | Exact-output postcondition | Contract postcondition |
|---:|---:|---|---|
| 1 / 14 | 1 | `[]` | product/order/primality is `true` |
| 2 / 15 | 2 | `[2]` | same predicate is `true` |
| 3 / 16 | 3 | `[3]` | same predicate is `true` |
| 4 / 17 | 4 | `[2, 2]` | same predicate is `true` |
| 5 / 18 | 8 | `[2, 2, 2]` | same predicate is `true` |
| 6 / 19 | 9 | `[3, 3]` | same predicate is `true` |
| 7 / 20 | 13 | `[13]` | same predicate is `true` |
| 8 / 21 | 25 | `[5, 5]` | same predicate is `true` |
| 9 / 22 | 31 | `[31]` | same predicate is `true` |
| 10 / 23 | 70 | `[2, 5, 7]` | same predicate is `true` |
| 11 / 24 | 100 | `[2, 2, 5, 5]` | same predicate is `true` |
| 12 / 25 | 360 | `[2, 2, 2, 3, 3, 5]` | same predicate is `true` |
| 13 / 26 | 999 | `[3, 3, 3, 37]` | same predicate is `true` |

For exact claim `i`, a satisfying source state is the literal ground term
`Run(SolutionMachine(n))`. For contract claim `i + 13`, it is the literal
ground term
`Observe(ValidFactorization(n, MachineValue(SolutionMachine(n))))`.
There are no side conditions whose satisfiability is in doubt.

Substitution of all 13 constants into the expected lists matches both trusted
canonical Python and candidate Python at those constants. This establishes only
the listed ground instances.

### Pinning the executed term

`SolutionModule()` in `verification.k` names a full constructor term.
The reviewer mechanically extracted its RHS, normalized only explicit
associative-list unit tokens (`.Exprs` and `.Stmts`) for concrete parsing, and
parsed both that term and trusted-regenerated `solution.mpy` with `kast`. The
two JSON constructor ASTs are identical, each 14,897 bytes.

`SolutionFunctions()` applies the semantic collector to that exact module.
`SolutionMachine(N)` invokes the collected `"factorize"` binding with `N`,
empty local environment and stack, `noResult`, and the real `Finish`
continuation. This is constructor-level equivalent to the material machine
state produced by the top-level initialization rule; it is not an opaque value
oracle. The typing-only import is collected as inert under the submitted
semantics.

The claims use `Run(MachineState)` rather than a `<k>` configuration because
`Machine` is declared a K function. That representation still executes the
actual submitted binding and body for these ground cases.

### Body sensitivity

A reviewer mutation changed the divisor literal in the executed
`factorize` wrapper inside `SolutionModule` from `Int(2)` to `Int(3)`. The
mutated definition built successfully. The original `n = 4` postcondition then
failed with a meaningful stuck residual whose actual value was `[4]`, not
`[2,2]`. This changes the program term actually used by the claim and shows the
ground theorem depends on the body.

Evidence:

- [`evidence/compare_program_term.py`](evidence/compare_program_term.py)
- [`evidence/extracted-solution-module-k-term.txt`](evidence/extracted-solution-module-k-term.txt)
- [`evidence/stage4_pinning.log`](evidence/stage4_pinning.log)
- [`evidence/claim_witnesses.py`](evidence/claim_witnesses.py)
- [`evidence/stage4_claim_witnesses.log`](evidence/stage4_claim_witnesses.log)
- [`evidence/body-sensitivity-verification.k`](evidence/body-sensitivity-verification.k)
- [`evidence/body-sensitivity-spec.k`](evidence/body-sensitivity-spec.k)

**Stage 4 result:** real-program pinning and result constraint pass for the 13
ground instances. Intent adequacy fails decisively: finitely many constants do
not prove the unrestricted source-contract domain.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

There are no generated helper K files. The local source inventory contains:

- 37 syntax/configuration declarations;
- 62 rules: semantic rules 1–40 and verification rules 41–62;
- zero local claims outside `spec.k`;
- zero `total`, `functional`, `simplification`, priority, `owise`, `anywhere`,
  macro, or opaque declarations.

`[function]` appears on `Machine`, semantic helper functions, exact program
constructors, and mathematical observers. It does not by itself assert the
truth of a task result. The complete normalized declaration/rule text, source
lines, attributes, and stable IDs are in
[`evidence/stage5_static_inventory.md`](evidence/stage5_static_inventory.md).
Every individual rule's classification and justification is in
[`evidence/stage5_rule_review.md`](evidence/stage5_rule_review.md).

The rule families account for all 62 rules:

| Rules | Role | Static decision |
|---|---|---|
| 1–2 | top-level initialization/result plumbing | faithful for target |
| 3–10 | calls, statements, branches, return, stack, halt | binding/control faithful on ground cases; rule 3 participates in the material unbounded-stack mismatch |
| 11–15 | literals, lookup, empty/singleton lists | faithful for every reachable target shape |
| 16–21 | binary/comparison evaluation order | left-to-right and faithful |
| 22–26 | one/two-argument named calls | faithful for target's direct named calls |
| 27–32 | function collection and argument binding | faithful for unique target names and exact arity; broader Python errors/redefinitions are not modeled |
| 33–40 | integer/list primitives and comparisons | faithful for reachable positive operands |
| 41–44 | exact program term, function map, entry machine | truthful definitional pinning; no oracle |
| 45–50 | `FactorFrom`/`FactorizeSpec` helpers | mathematically truthful on guards but unused by all 26 claims |
| 51–62 | product/order/primality/value observers | truthful structural definitions over the concrete executed list |

### Construct coverage and control/state review

`solution.mpy` uses:

- `Module`, `ImportFrom`, `FuncDef`, `Params`, and sequential `Stmts`;
- `If` and `Return`;
- `Int`, `Name`, binary `+`, `*`, `%`, `//`;
- comparisons `<`, `>`, `==`;
- empty/singleton `ListExpr`;
- one- and two-argument direct named `Call`.

Syntax declarations 1–9 cover each constructor. Rules 1, 3–40 cover every
reachable operation. Empty/multiple list, call, and comparison cases are
separated by constructor shape. Evaluation is left-to-right. Calls bind exact
parameter/value lists, install a local environment, preserve the functions map,
push caller continuation/environment, and returns restore/pop them. Branch
guards are complementary. The result cell is written only on final halt.

The machine places environment, function map, stack, and intermediate result
inside `MachineState`; `<input>` and `<result>` remain outer cells. No target
state mutation, allocation, I/O, exception, or heap behavior is silently
fabricated because the submitted program uses none of those facilities.

The ground-reachable rule overlaps are disjoint by constructor or complementary
guard. `FactorFrom` is guard-complete only for `N < 2` or
`N >= 2, D >= 2`; `HasDivisor` is used from `D = 2` with candidate factors at
least 2. No priority rule preempts fixed execution.

### Material false-conclusion witness

The semantic call rule treats the list of frames as unbounded. On the intended
positive input `n = 1,000,003`, the fixed candidate Python execution exceeds
CPython's recursion depth and raises `RecursionError`. The K rules continue
allocating frames, reach `divisor² > n`, and produce the normal-return
conclusion `[1000003]`. This is a concrete false real-program conclusion
enabled by the generated call model on the intended domain.

Other broader-language limitations are not mislabeled as target unsoundness:

- ignoring `ImportFrom` would miss import failure/side effects, but the
  standard `typing.List` import is inert for this translated target;
- right-to-left collection gives the wrong binding for a different program
  with duplicate function names, but the immutable submitted program has two
  unique names;
- mismatched call arity becomes stuck rather than raising `TypeError`, but all
  target calls have exact arity;
- K `%Int` and `/Int` use truncation-style signed arithmetic, unlike Python
  floor division/remainder for negative operands (`-3 // 2` is the concrete
  counterexample), but all reachable division/remainder operands are positive.

These have no false target-program witness beyond the separately established
recursion-resource mismatch.

### No smuggled correctness conclusion

`FactorFrom`, `FactorizeSpec`, and `PrependFactor` look like a task-specific
summary, but no submitted claim references them and no operational rule rewrites
program execution to them. They cannot contribute to claim closure. The
contract claims instead normalize the real ground `SolutionMachine`, extract
its halted value, and structurally evaluate product, ordering, and primality.
There is no fresh or opaque result-bearing symbol.

**Stage 5 result:** the ground proof rules are result-bearing and mostly
truthful for the 13 cases, with no answer oracle. The generated language model
has a concrete real-program recursion mismatch on the intended domain and
several explicitly bounded off-target limitations.

## 6. Fresh non-vacuity test

The candidate's `mutation-spec.k` was not relied on. The reviewer created a
fresh spec at
[`evidence/fresh-vacuity-spec.k`](evidence/fresh-vacuity-spec.k).

Its satisfiable input is `n = 25`. It changes the exact result obligation from
the true `[5,5]` to the false `[5]`.

The `kprove --dry-run` command exited 0 and produced the backend invocation, so
the mutation parsed and built successfully. The real proof exited 1 with
`WarnStuckClaimState`. Its residual contains the executed actual value:

```text
ListVal ( ListItem ( IntVal ( 5 ) )
          ListItem ( IntVal ( 5 ) ) )
```

The failure is therefore the expected unmet result obligation, not a parser
error, missing import, timeout, unreachable mutation, or unrelated crash.

Evidence:

- [`evidence/run_stage6_vacuity.sh`](evidence/run_stage6_vacuity.sh)
- [`evidence/stage6_fresh_vacuity.log`](evidence/stage6_fresh_vacuity.log)

**Stage 6 result: PASS for non-vacuity of the ground proof suite.**

## 7. Proven versus assumed accounting

### What is actually proved

Under the candidate's generated K theory and K 7.1.293 builtins, each of the 13
ground `SolutionMachine(n)` terms normalizes to its exact listed halted list.
For those same 13 concrete executions, the list:

1. has product `n`;
2. is nondecreasing with every item at least 2;
3. consists only of values accepted by the trial-divisor primality observer.

That is the complete theorem. It says nothing about any other integer. In
particular, it does not establish a partial-correctness implication of the form
“for every positive `n`, if the submitted program terminates normally then the
returned list satisfies the contract.”

### Trust and assumption ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| Trusted `/reference/py2mpy.py` translation from Python AST to MPY constructors | program identity | Acceptable and byte-checked; output equals submitted `solution.mpy`. |
| Mechanical `SolutionModule` reconstruction | all 26 claims | Acceptable for the immutable artifact; constructor AST equality and body sensitivity are demonstrated. |
| K 7.1.293 INT/BOOL/MAP/LIST/K-sequence builtins and Haskell/LLVM backends | all semantics and proofs | Ordinary low-level trust boundary; versions recorded. |
| Candidate-authored Python subset semantics | all 26 claims | Conditional, not independently supplied. Ground behavior is strongly checked; unrestricted real-program fidelity fails at recursion depth. |
| Unbounded semantic call stack | every recursive K execution | Illegitimate as a bridge to the unrestricted real CPython program without an explicit abstraction/domain restriction; concrete positive-input witness recorded. |
| Ignored `typing.List` import and omitted broader Python constructs/errors | target parsing/execution | Nonfatal for ordinary execution of the fixed ground cases; explicitly excluded elsewhere. |
| `Machine`, semantic helpers, and observers declared `[function]` | ground normalization and `WarnTrivialClaim` closure | Acceptable only after rule audit/non-vacuity; the attribute is not itself evidence of correctness. |
| `FactorFrom` and `FactorizeSpec` | none | Unused; no claim depends on these task-specific helpers. |
| Differential and concrete tests | translation/semantics adequacy bridges | Finite empirical evidence only; never treated as a universal proof. |
| Informal domain interpretation `n >= 1` | comparison with prompt | Supported by prime factorization and product contract. No finite upper bound is supported. |

There are no opaque local symbols, external result oracles, empirical summaries
used as proof rules, or imported proof-local lemmas.

### Gate accounting and final mapping

- Ground Gate A (program identity, result constraint, body sensitivity,
  non-vacuity): passes for the 13 fixed inputs.
- Full real-program Gate A: fails the generated-semantics/CPython recursion
  bridge at positive input 1,000,003.
- Gate B (intent adequacy): fails because 13 constants materially narrow the
  unrestricted HumanEval source-contract domain.
- Gate C (auditability): the evidence is reproducible and trust boundaries are
  explicit, but finite evidence cannot repair Gates A/B.

Even if the 13 ground instances are described in generic Kit terminology as a
sound but limited result, the controlling benchmark rule requires
`FAIL / NOT_LEGIT` for this material finite-domain narrowing.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
