# Independent adversarial audit: 155-even-odd-count

The candidate contains a freshly reconstructible, non-vacuous K proof of what
its submitted program actually does under its generated semantics. It does not,
however, prove the HumanEval contract over the stated integer domain. The
submitted program and its proof-specific reference model both mishandle input
`0`: they return `(0, 0)`, while the trusted canonical implementation counts the
single decimal digit `0` as even and returns `(1, 0)`. Because `0` is an integer
and the source contract has no exclusion, this is a material contract-domain
failure, not a non-fatal testing limitation.

## 1. Input and provenance integrity

The launcher declares:

- problem `155-even-odd-count`;
- generation condition `bare`;
- record layout `legacy-selected-stage1`;
- semantics mode `GENERATED_SEMANTICS`.

I read `/audit-input.json`, its `record_layout`, `container_paths`, integrity
fields, and recorded hashes before using any candidate claim. I also read
`/audit-campaign-lock.json`, `/run.json`, `/task.json`,
`/generation-result.json`, `/generation-evidence/invocation.json`,
`metrics.json`, `usage.json`, `codex-last.txt`, `codex-output.log`,
`prompt.txt`, both legacy auxiliary records, and every one of the 222 JSON
records in the structured trace. Historical `runtime-metrics.json` is absent,
which is permitted for this legacy-selected layout. The structured trace was
parsed independently; its full type, message, command, and output inventory is
in [stage1-trace-inventory.log](evidence/stage1-trace-inventory.log).

The campaign object in `/audit-input.json` is exactly equal to the campaign
lock. The lock SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
matching the recorded value. All required records and all launcher-declared
container paths exist, are readable, are the expected regular-file/directory
type, and are not symlinks. Every recorded regular-file hash matches. The
candidate tree also reproduces the stage-1 workspace digest
`1a46f3efa13e83afb8a7e25bb3864082bc32a3013145b0d8bec490b96f71a25f`,
and the trace tree reproduces `usage.json`'s source-trace digest
`8f092f6e74ec1048eeccc9ce62dc19faf8576fd0e8d14be666ae6ec6a47bb0f7`.
All mounted tree entries were independently enumerated and hashed. See
[provenance_check.py](evidence/provenance_check.py) and
[stage1-integrity.log](evidence/stage1-integrity.log).

`/candidate/prompt.py` is byte-identical to `/reference/prompt.py`, and
`/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`. There is no
`/reference/reference-semantics`, as required in `GENERATED_SEMANTICS` mode.
There is no supplied semantics baseline to infer or compare. The candidate
contains all requested proof artifacts: `solution.py`, `solution.mpy`,
`semantic.k`, `verification.k`, `spec.k`, `definition.k`, and `prove.sh`.

The generation result and final generation prose claim `KPROVE_PASSED`. I
treated that solely as an untrusted historical claim. No infrastructure breach
was found, so a candidate verdict is appropriate.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

From the trusted prompt and canonical code, `even_odd_count(num)` accepts an
integer and returns a pair:

1. the number of even decimal digits in `abs(num)`;
2. the number of odd decimal digits in `abs(num)`.

The canonical implementation iterates over `str(abs(num))`. Therefore `0` has
one digit, and that digit is even:

```text
even_odd_count(0) == (1, 0)
```

The submitted implementation first makes a negative input nonnegative, then
loops only while `num > 0`, classifies the current least-significant digit by
`num % 2`, and removes it with `num // 10`. Classifying a decimal digit via the
parity of the remaining integer is correct for every positive remaining
integer. The defect is the zero-iteration case: an original input of `0` skips
the loop and returns `(0, 0)`.

### Translation fidelity

I regenerated the constructor program in scratch using the trusted translator:

```text
python3 /reference/py2mpy.py \
  /tmp/audit-work/155-even-odd-count-audit/source/solution.py \
  > /tmp/audit-work/155-even-odd-count-audit/build/solution.regenerated.mpy
```

The command exited 0. `cmp -s` against the submitted `solution.mpy` exited 0,
and both files have SHA-256
`27f1ddc4e5c550a671e1ee9e493b5196c65148fcd2f5e3aafe4632e587494b4f`.
See [stage2-translator-identity.log](evidence/stage2-translator-identity.log).

### Independent differential test

[differential_test.py](evidence/differential_test.py) imports the trusted and
candidate entry points independently. Its input scope is:

- the two documented examples;
- zero, sign, one-digit, parity, decimal-boundary, and large-integer cases;
- every integer in `[-10000, 10000]`;
- 2,000 seed-155 arbitrary-precision integers in
  `[-10**200, 10**200]`.

There is no collection “empty input” for this integer-only contract; zero is
the corresponding no-loop boundary. Among 22,005 distinct inputs the script
found exactly one mismatch:

```text
input=0 canonical=(1, 0) candidate=(0, 0)
```

The script exited 1 because a mismatch is a failed fidelity check. Full bounded
output is in [stage2-differential.log](evidence/stage2-differential.log).
Finite agreement elsewhere is supporting evidence only; the concrete zero
counterexample is decisive.

## 3. Clean proof reconstruction

I copied only source artifacts to
`/tmp/audit-work/155-even-odd-count-audit/reconstruction`. No candidate
definition or cache was reused. The available independently installed tools
are K `v7.1.293`; see [stage3-toolchain.log](evidence/stage3-toolchain.log).

### Fresh builds

The generated semantics alone was rebuilt with:

```text
kompile semantic.k --backend haskell \
  --main-module SEMANTIC --syntax-module MPY-SYNTAX \
  --output-definition semantic-fresh-kompiled
```

It exited 0. See
[stage3-kompile-semantics.log](evidence/stage3-kompile-semantics.log).

The proof definition was independently rebuilt with:

```text
kompile definition.k --backend haskell \
  --main-module DEFINITION --syntax-module MPY-SYNTAX \
  --output-definition proof-fresh-kompiled
```

It exited 0. See [stage3-kompile-proof.log](evidence/stage3-kompile-proof.log).

### Fresh generated-semantics execution

[concrete_semantics_compare.py](evidence/concrete_semantics_compare.py) ran the
fresh semantics on:

```text
[-12, 123, 0, -1, 1, -2, 2, 9, 10, 11, -78, 346211]
```

These inputs exercise the negative and nonnegative initial branches, the
zero-iteration and iterating loop cases, both digit-parity branches, assignment,
augmented assignment, floor division, tuple construction, and return. Every
`krun` invocation exited 0 and its returned pair matched an independent
execution of the submitted Python implementation. In particular, both K and
the submitted Python return `(0, 0)` for zero; this confirms semantic fidelity
to the buggy submitted program, not fidelity to the HumanEval contract. See
[stage3-concrete-semantics.log](evidence/stage3-concrete-semantics.log).

### Fresh positive proofs

The original spec, containing both the generalized loop claim and end-to-end
claim, was run exactly as a fresh proof target:

```text
kprove spec.k --definition proof-fresh-kompiled \
  --spec-module SPEC --output pretty
```

It printed `#Top` and exited 0; see
[stage3-kprove-all-claims.log](evidence/stage3-kprove-all-claims.log). The loop
claim copied unchanged into a one-claim module also printed `#Top` and exited 0;
see [spec-loop-only.k](evidence/spec-loop-only.k) and
[stage3-kprove-loop-claim.log](evidence/stage3-kprove-loop-claim.log).

The end-to-end claim uses the loop claim as a circularity/loop invariant. A
diagnostic module that removes that auxiliary claim timed out after 15 seconds;
this is not a failed target proof and is not used as a verdict signal. The
authoritative original module includes and proves both claims together.

Thus clean reconstruction succeeds. The historical `#Top` was independently
confirmed, but it proves only the formal theorem stated by this candidate.

## 4. Adequacy and real-program pinning

### Claims in plain language

The first claim starts with:

- control at the digit loop followed by the real return subtree;
- an exact environment containing `num = N`, `even = E`, and `odd = O`;
- an arbitrary unchanged input cell;
- no result yet;
- precondition `N >= 0`.

It claims that execution reaches empty control, changes `num` to zero, changes
the two counters to the recursively defined `evenFrom(E,N)` and
`oddFrom(O,N)`, and returns that exact pair.

The second claim has no side precondition, so its formal domain is every K
mathematical integer `N`. It starts the term `solutionProgram()` with an empty
environment, input `N`, and no result. It claims empty control, final
`num = 0`, the two recursively defined counts of `absNum(N)`, and result
`expected(N)`.

Both claims constrain the observable return value and final environment. No
result variable is left free, and neither postcondition is a tautology or a
one-way implication.

### Satisfiable witnesses and concrete substitution

[claim_witnesses.py](evidence/claim_witnesses.py) records satisfying ground
states:

- loop claim: `N=12`, `E=0`, `O=0`, arbitrary input `99`; the precondition is
  true and the formal result is `(1,1)`, matching both Python implementations
  on `12`;
- entry claim: `N=12`; the formal result `(1,1)` matches both Python
  implementations;
- entry claim: `N=0`; the formal result `(0,0)` matches the submitted
  implementation but contradicts the trusted canonical `(1,0)`.

### Mechanical pinning to `solution.mpy`

The pinning chain is:

1. trusted regeneration is byte-identical to submitted `solution.mpy`;
2. the RHS constructor term recorded in
   [spec-program-pinning.k](evidence/spec-program-pinning.k) is mechanically
   identical to `solution.mpy`, allowing only the explicit K spelling
   `.Stmts` for the translator's blank empty statement list; see
   [program_pinning_compare.py](evidence/program_pinning_compare.py) and
   [stage4-program-constructor-identity.log](evidence/stage4-program-constructor-identity.log);
3. `solutionProgram()` and the submitted `solution.mpy`, parsed separately,
   reach byte-identical pretty-printed configurations after the semantics'
   first rewrite, including the complete `exec(...)` body and environment; see
   [program_pinning_execution.py](evidence/program_pinning_execution.py) and
   [stage4-program-pinning-execution.log](evidence/stage4-program-pinning-execution.log).

This establishes that the claim executes the submitted function body rather
than a substituted summary program. The failed attempt to express the pure
function equality as a standalone K reachability claim is retained in
[stage4-kprove-program-pinning.log](evidence/stage4-kprove-program-pinning.log);
K reported that functional claims are not supported by this backend. That
diagnostic is not used as positive evidence; the successful parser/first-step
comparison above supplies the mechanical constructor check.

A separate body-sensitivity mutation changed the `functionBody()` term actually
executed by the entry claim so that the function returns `(odd, even)`. The
mutated definition built successfully, but the original spec failed with a
`WarnStuckClaimState`. A reachable residual for a positive even one-digit
input has actual result `(0,1)` where the theorem requires `(1,0)`. See
[verification-body-mutation.k](evidence/verification-body-mutation.k),
[stage4-body-mutation-kompile.log](evidence/stage4-body-mutation-kompile.log),
and [stage4-body-mutation-kprove.log](evidence/stage4-body-mutation-kprove.log).

Real-program pinning and result constraint therefore pass. Intent adequacy
fails at zero.

## 5. Rule-by-rule static soundness review

The complete numbered source and declaration search is preserved in
[stage5-rule-inventory-source.log](evidence/stage5-rule-inventory-source.log).
There are no additional helper K sources beyond `definition.k`, which only
imports `SEMANTIC` and `VERIFICATION`.

### Local syntax, attributes, configuration, and special declarations

`MPY-SYNTAX` declares all of the following:

| ID | Declaration | Review |
|---|---|---|
| S1 | `Pgm ::= Module(Stmts)` | Used by the submitted module. |
| S2 | `Stmts ::= List{Stmt,""}` | Used for all bodies and empty `else`. |
| S3 | `Stmt ::= FuncDef / Assign / AugAssign / If / While / Return` | Every alternative is used by `solution.mpy`. |
| S4 | `Params ::= Params(Strings)` | Used by the function definition. |
| S5 | `Strings ::= List{String,","}` | Used for the single parameter. |
| S6 | `Expr ::= Int / Name / UnaryOp / BinOp / Compare / TupleExpr` | Every alternative is used. |
| S7 | `Exprs ::= List{Expr,","}` | Used by the returned pair. |
| S8 | `CmpOp ::= CmpOp(String,Expr)` | Used for `<`, `>`, and `==`. |
| S9 | `CmpOps ::= List{CmpOp,","}` | Used for each one-element comparison chain. |
| S10 | `Val ::= intVal / boolVal / pairVal / noResult` | Sufficient result domain for the target. |
| S11 | partial functions `eval`, `envGet`, `negVal`, `addVal`, `modVal`, `divVal`, `ltVal`, `gtVal`, `eqVal` | No `total` assertion; all target uses have a defining equation. |
| S12 | computations `exec(Stmts)` and `loop(Expr,Stmts)` | Direct sequencing and stable loop-head representation. |

The configuration has exactly the state required here: `<k>`, a local-variable
`<env>` map, immutable `<input>`, and `<result>`. The target has no heap, I/O,
exceptions, nested calls, or externally observable allocation.

`VERIFICATION` adds 14 `[function,total]` symbols:
`absNum`, `evenDigits`, `oddDigits`, `evenFrom`, `oddFrom`, `expected`,
`numPositive`, `numNegative`, `digitIsEven`, `returnedCounts`, `digitBody`,
`functionBody`, `returnCounts`, and `solutionProgram`. Guard coverage and
termination are reviewed below.

There are no local `[functional]`, `[simplification]`, priority, `owise`,
`anywhere`, or macro declarations; no opaque or fresh symbols; and no
proof-local operational rewrite that bypasses program execution.

### `semantic.k`: all 29 rules

| Rules | Exact role | Decision |
|---|---|---|
| M1 | `envGet((X |-> V) REST,X) => V` | Sound map lookup. K maps cannot contain two values for one key. |
| M2 | `eval(Int(I),_)` | Sound integer literal. |
| M3 | `eval(Name(X),ENV)` | Sound lookup; every target lookup is bound. |
| M4 | unary `-` through `negVal` | Sound for target integer values. |
| M5 | binary `+` through `addVal` | Sound but unused by this AST; augmented addition uses the same primitive. |
| M6 | `%` through `modVal` | Sound on the target's nonnegative dividend and divisor `2`. |
| M7 | `//` through `divVal` and `/Int` | Sound on the target's nonnegative dividend and positive divisor `10`, where Python floor division and K integer division agree. |
| M8 | `<` through `ltVal` | Sound integer comparison. |
| M9 | `>` through `gtVal` | Sound integer comparison. |
| M10 | `==` through `eqVal` | Sound integer equality. |
| M11 | two-element `TupleExpr` to `pairVal` | Sound for the submitted return expression. |
| M12 | `negVal(intVal(I))` | Exact `0 -Int I`. |
| M13 | `addVal(intVal(I1),intVal(I2))` | Exact `+Int`. |
| M14 | `modVal(intVal(I1),intVal(I2))` | Exact `%Int`; target never uses zero divisor. |
| M15 | `divVal(intVal(I1),intVal(I2))` | Exact `/Int`; target divisor is `10`. |
| M16 | `ltVal` | Exact `<Int`. |
| M17 | `gtVal` | Exact `>Int`. |
| M18 | `eqVal` | Exact `==Int`. |
| M19 | module/function entry | Matches the exact name and parameter, binds input `N`, and executes `BODY`. Preinitializing `even` and `odd` is redundant because the target assigns both before any read. It is over-broad as reusable Python-module semantics, but it enables no false target conclusion. |
| M20 | `exec(.Stmts) => .K` | Correct sequence termination. |
| M21 | `exec(S REST) => S ~> exec(REST)` | Correct left-to-right statement sequencing. |
| M22 | `Assign(Name(X),E)` | Evaluates against the old environment and then updates `X`, as required here. |
| M23 | `AugAssign(Name(X),"+",E)` | Reads the old value and RHS, adds, and updates; exact for both counter increments. |
| M24 | true `If` branch | Guard and selected body are correct. |
| M25 | false `If` branch | Complementary guard and selected body are correct. The two rules are disjoint and exhaustive for target Boolean guards. |
| M26 | `While` to stable `loop` | Correct control reification. |
| M27 | true loop iteration | Executes the body then returns to the same loop head. |
| M28 | false loop exit | Correctly removes the loop. M27/M28 are disjoint and exhaustive for target guards. |
| M29 | `Return(E)` | Evaluates the pair in the current environment, records it, and discards the remaining same-function continuation. The rule is broad without a call stack, but every reachable target return is final in this one direct function invocation, so there is no false intended-domain witness. |

The semantics is intentionally a small target-language model rather than full
Python. Its over-broad entry and return contexts are reuse limitations, not
material unsoundness for this fixed submitted program. I do not label them
unsound because no state reachable from a satisfying entry precondition enables
a false target conclusion. All material target operations execute; none is
replaced by an oracle or answer rule.

### `verification.k`: all 19 equations

| Rules | Exact role | Decision |
|---|---|---|
| V1–V2 | `absNum`: negative and nonnegative cases | Guards are disjoint and exhaustive; exact mathematical absolute value. |
| V3–V5 | `evenFrom`: base, positive-even, positive-odd cases | Guards are disjoint and exhaustive. For positive `N`, `N /Int 10 < N`, so recursion descends. It exactly summarizes the candidate loop. |
| V6–V8 | `oddFrom`: base, positive-even, positive-odd cases | Same coverage and descent; exactly summarizes the candidate loop. |
| V9 | `evenDigits(N) => evenFrom(0,N)` | Truthful definitional wrapper for the candidate summary. |
| V10 | `oddDigits(N) => oddFrom(0,N)` | Truthful definitional wrapper for the candidate summary. |
| V11 | `expected(N)` | Builds exactly the pair of the two summary functions after `absNum`. |
| V12 | `numPositive()` | Exact `num > 0` AST subtree. |
| V13 | `numNegative()` | Exact `num < 0` AST subtree. |
| V14 | `digitIsEven()` | Exact `num % 2 == 0` AST subtree. |
| V15 | `returnedCounts()` | Exact `(even, odd)` AST subtree. |
| V16 | `digitBody()` | Exact parity branch followed by `num // 10` assignment. |
| V17 | `returnCounts()` | Exact final return subtree. |
| V18 | `functionBody()` | Exact submitted function body. |
| V19 | `solutionProgram()` | Exact submitted module/function binding. |

The `[total]` equations are covered: V1/V2 cover every integer; V3–V5 and
V6–V8 cover every integer with mutually exclusive guards; V9–V19 are
unconditional; the recursive equations descend on every recursive use. There
are no overlapping equations with disagreeing RHSs.

V3/V9/V11 expose the decisive intent gap. At `N=0`,
`evenDigits(0) => evenFrom(0,0) => 0`, so
`expected(0) => pairVal(intVal(0),intVal(0))`. This is a consistent definition
and an accurate summary of the submitted program, so it does not make the K
theory logically unsound. But the claimed informal interpretation “number of
even digits” is false on the intended domain: the concrete witness `0` has the
single even digit `0`, and the trusted canonical result is `(1,0)`. Thus the
summary-to-HumanEval-property bridge is false.

### `spec.k`: both claims

The loop claim matches the real stable loop configuration and exact continuation
reached from V18 through M21 and M26. Its environment is exact, its precondition
is satisfiable, and its result and final counters are constrained.

The entry claim uses V19, which expands to the real submitted binding and body.
It has the full integer domain and an exact result. Its failure is not vacuity
or program substitution; it proves the wrong all-integer property because V11
uses the candidate's zero-dropping summary.

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`; no candidate mutation evidence was
trusted. I created [spec-vacuity-audit.k](evidence/spec-vacuity-audit.k) in
scratch. It retains the loop claim needed by the end-to-end proof and changes
the end-to-end result obligation to demand one extra even digit:

```text
pairVal(
  intVal(evenDigits(absNum(N)) +Int 1),
  intVal(oddDigits(absNum(N))))
```

`N=12` is a satisfying witness: actual/formal execution returns `(1,1)`, while
the mutation demands `(2,1)`.

The `kprove --dry-run` build exited 0; see
[stage6-vacuity-dry-run.log](evidence/stage6-vacuity-dry-run.log). The real
proof exited 1 with `WarnStuckClaimState`, and the residual exposes exactly the
unmet result obligation:

```text
evenFrom(0,N) +Int 1 #Equals evenFrom(0,N)
```

See [stage6-vacuity-kprove.log](evidence/stage6-vacuity-kprove.log). This is a
meaningful reachable proof failure, not a parser error, missing import, timeout,
or unrelated crash. The original proof is non-vacuous.

## 7. Proven versus assumed accounting

### Precisely proven

Conditional on the generated K semantics and imported K built-ins, the fresh
`#Top` establishes:

- for every `N >= 0` and arbitrary starting counters `E,O`, the submitted
  digit loop consumes `N`, updates the counters according to the guarded
  `evenFrom`/`oddFrom` recurrences, and returns that pair;
- for every K mathematical integer `N`, the exact submitted
  `solution.mpy` executes from the candidate's direct-call initial
  configuration and returns the candidate-defined
  `expected(N)`;
- in particular, the theorem proves a result of `(0,0)` for `N=0`.

The proof is body-sensitive and result-constraining. It is not a proof of the
trusted HumanEval postcondition at zero.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K 7.1.293 Haskell backend and reachability logic | Both claims and all mutation results | Necessary low-level machine-checking boundary. Fresh builds/runs were used. |
| K `Int`, `Bool`, `Map`, equality, list, and computation-sequence built-ins | All semantic and reference equations | Acceptable standard primitive boundary. Target uses arbitrary-precision integers, positive divisors, and pure maps. |
| Trusted `py2mpy.py` transliteration | Source-to-`solution.mpy` identity | Trusted benchmark input; candidate copy is byte-identical and regeneration is byte-identical. |
| Generated `semantic.k` | Meaning of every proof execution | Not assumed blindly: all 29 local rules were statically reviewed and concrete execution covered every target construct. The executable comparison is finite evidence, while the direct rules provide the general informal Python bridge. |
| Direct module-as-call convention in M19 | Entry claim | Acceptable for this single exact function term and input cell. It is not general Python module/call semantics. |
| K `/Int` and `%Int` as Python `//` and `%` | Loop behavior | Acceptable only because the target first makes `num` nonnegative and uses positive divisors 10 and 2. |
| V1–V11 mathematical summary | Result postcondition | V1–V10 accurately summarize the submitted loop. The bridge from V11 to the HumanEval meaning is illegitimate at zero, witnessed by canonical `(1,0)` versus formal `(0,0)`. |
| V12–V19 AST aliases | Real-program pinning | Acceptable: constructor comparison and first-step configuration identity are mechanical, and the body mutation is rejected. |
| Differential and concrete tests | Fidelity evidence only | Finite empirical evidence; never used as a substitute for `kprove`. |

There are no opaque symbols, fresh result-bearing values, unproved operational
bridges, or empirical oracles in the proof. The important informal boundary is
the claim that the recursively defined summary is the requested decimal-digit
count; that boundary is demonstrably false for `0`.

### Gate and benchmark decision

- Gate A, real-program soundness: **PASS**. The exact submitted program runs,
  the proof closes freshly, and mutation checks show body and result
  sensitivity.
- Gate B, intent adequacy: **FAIL**. The unrestricted integer contract includes
  `0`, but both implementation and formal postcondition return the wrong result
  there.
- Gate C, trust/evidence auditability: **PASS with explicitly bounded empirical
  evidence**. All sources, commands, exits, and rule inventories are present;
  tests are reported only as finite support.

Under generic Kit terminology this is a sound theorem about a materially
limited/wrong implementation. Under the benchmark's explicit decision boundary,
materially failing the HumanEval source-contract domain is
`FAIL / NOT_LEGIT`, not `CONCERNS / LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
