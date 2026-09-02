# Independent adversarial audit: 59-largest-prime-factor

## Executive decision

The candidate contains a legitimate, non-vacuous partial-correctness proof of
the submitted translated program under its generated semantics. Fresh builds
and proof runs succeeded, the formal result is constrained, and the proof does
not use an oracle, an execution shortcut, or a false proof-local equation.

The verdict is `CONCERNS / LEGIT`, rather than `PASS / LEGIT`, because the
machine-checked postcondition is `lpfSpec(N, 2)`. The proof establishes that the
real program computes this recursive trial-division summary, but it does not
machine-check that the summary is prime, divides the original input, and is
maximal among its prime factors. That final intent bridge has a sound ordinary
mathematical argument and strong finite differential evidence, but remains
informal. It does not permit a false program result to be proved.

All candidate files were treated as untrusted. Builds and experiments used
only the clean copy at `/tmp/audit-work/review-59`; candidate-built definitions
and caches were not used.

## 1. Input and provenance integrity

### Rendered semantics boundary

The rendered mode is `GENERATED_SEMANTICS`. `/reference` contains exactly the
three trusted regular files `canonical.py`, `prompt.py`, and `py2mpy.py`;
`/reference/reference-semantics` is absent, as required. There is therefore no
mode/mount contradiction and no hidden semantics was sought or used. K
v7.1.293 was available. Exact checks are in
`evidence/00-environment.log`.

### Candidate inventory and comparisons

The candidate contains the required regular source artifacts:
`solution.py`, `solution.mpy`, `semantic.k`, `verification.k`, `spec.k`, and
`prove.sh`. It also contains regular copies of `prompt.py` and `py2mpy.py`, the
required JSON metadata, the two untrusted prose/log records, and one regular
structured JSONL trace. There are no symlinks, no generated helper K files, and
no candidate compiled definitions or caches. `PROOF.md`, `NOTES.md`, and
`spec-vacuity.k` are absent, but none is a required generation deliverable in a
claimed successful run.

`/candidate/prompt.py` is byte-identical to `/reference/prompt.py`, and
`/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`. Their
SHA-256 values also equal the values named in `run-input.json`. The complete
tree/type listing, comparisons, and hashes are in
`evidence/01-integrity.log`.

I read `run-input.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, and all 111 JSON objects in the structured trace only as
untrusted claims. They claim a successful aggregate proof and differential
test. Nothing in the verdict relies on those claimed runs. A bounded metadata,
trace, and log summary is preserved in
`evidence/01-untrusted-metadata.log`.

Integrity result: no missing, changed, mistyped, symlinked, or unexplained extra
required artifact; no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementations

The trusted prompt asks `largest_prime_factor(n)` to return the largest prime
factor of an integer `n`, under the assumptions `n > 1` and `n` is not prime.
It gives `largest_prime_factor(13195) == 29` and
`largest_prime_factor(2048) == 2`.

The trusted canonical implementation enumerates every `j` from 2 through `n`,
checks divisibility and primality, and retains the largest qualifying `j`.
The candidate uses a different but standard algorithm: starting with factor 2,
it repeatedly divides the residual by the current factor when divisible,
otherwise increments the factor, and returns the residual once
`factor * factor > residual`.

The trusted command

```text
python3 /reference/py2mpy.py /tmp/audit-work/review-59/src/solution.py > /tmp/audit-work/review-59/build/regenerated-solution.mpy
```

exited 0, and `cmp` established byte identity with submitted `solution.mpy`;
both files have SHA-256
`db068bfdeddf4555800505c6781d12cabba9f862bbe376347326aeec08e2c591`.
See `evidence/02-regenerate-mpy.log`.

### Independent differential test

`evidence/differential_test.py` independently imports the entry point from
trusted `/reference/canonical.py` and from the scratch copy of generated
`solution.py`. It does not reuse `lpfSpec` or any K equation. It covers:

- both documented examples;
- 4, the smallest composite and therefore the lower intended-domain boundary;
- repeated-division, non-dividing, dividing, and loop-exit paths;
- the equality boundary `factor * factor == n`, including 25 and 49;
- every composite from 4 through 1000; and
- 100 fixed-seed generated composites up to 20,000.

The exact command exited 0 with 929 intended-domain cases and zero mismatches
(`evidence/02-differential.log`). The parameter is a scalar integer, so there is
no empty-container case; the script records that explicitly. It also records
0, 1, and primes as out-of-domain observations. The divergence at `n=0`
(canonical 1, candidate 0) is outside the stated domain and is not correctness
evidence in either direction.

Stage result: program fidelity passes on the intended domain.

## 3. Clean proof reconstruction

I copied source files only and built two new definitions:

```text
kompile semantic.k --backend llvm --main-module SEMANTIC --syntax-module MPY-SYNTAX --output-definition /tmp/audit-work/review-59/build/semantic-llvm-kompiled
```

and

```text
kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition /tmp/audit-work/review-59/build/verification-haskell-kompiled
```

Both exited 0. Logs are `evidence/03-build-concrete-llvm.log` and
`evidence/03-build-proof-haskell.log`.

### Fresh generated-semantics execution

`evidence/semantics_compare.py` ran the submitted `solution.mpy` through the
fresh LLVM definition for inputs 4, 8, 15, 25, 2048, 13195, and the prime-2
loop-false edge. Every `krun` exited 0 and agreed with both Python
implementations; there were zero semantic mismatches. These inputs collectively
exercise module loading, statement sequencing, assignment, map lookup/update,
both `if` branches, both `while` branches, repeated division, all four binary
operators, both comparisons, and return. Exact subcommands and results are in
`evidence/03-concrete-semantics-compare.log`.

### Fresh positive proofs

Each target was selected and checked against the fresh Haskell definition:

| Target | Required dependency in command | Exit | Output | Evidence |
|---|---|---:|---|---|
| `SPEC.loop-refines-lpf` | none | 0 | `#Top` | `evidence/03-proof-loop-refines-lpf.log` |
| `SPEC.largest-prime-factor-correct` | `SPEC.loop-refines-lpf` circularity | 0 | `#Top` | `evidence/03-proof-end-to-end-with-helper.log` |
| `SPEC.prompt-example-13195` | none | 0 | `#Top` | `evidence/03-proof-example-13195.log` |
| `SPEC.prompt-example-2048` | none | 0 | `#Top` | `evidence/03-proof-example-2048.log` |

The end-to-end selection explicitly includes the loop claim because that claim
is its checked circularity. Selecting only the end-to-end label filters the
circularity out and causes symbolic unrolling; that non-result is not used as
proof evidence. The bounded diagnostic record and explanation are
`evidence/03-diagnostic-universal-without-helper.log` and
`evidence/03-diagnostic-note.txt`.

Stage result: every positive target closes with exit 0 and `#Top` under a clean
source-built definition.

## 4. Adequacy and real-program pinning

### Claims in plain language

1. `loop-refines-lpf` starts with the exact translated factor loop followed by
   the translated return, environment `{factor: F, n: N}`, no result, and
   `N > 1, F >= 2`. On termination it requires empty computation, preserves the
   input cell, sets both `n` and the result to `lpfSpec(N,F)`, and permits only
   the final factor value to be existential.
2. `largest-prime-factor-correct` starts with the complete `solutionModule`,
   input `N > 1`, empty environment, and no result. On termination it requires
   empty computation, an environment containing exactly `factor` and `n`,
   fixes `n` and the returned value to `lpfSpec(N,2)`, and leaves only the final
   factor existential.
3. `prompt-example-13195` executes the complete module from empty state and
   requires result 29.
4. `prompt-example-2048` does the same and requires result 2.

These postconditions are equalities over the observable result, not free
variables, tautologies, or one-way implications. The existential factor and
example environment do not influence the constrained result.

### Exact program identity

`solutionModule` is a macro, not an operational shortcut. Its expansion at
`verification.k:30-35` is constructor-for-constructor identical to submitted
`solution.mpy`; `factorLoop` at `verification.k:20-27` is its exact middle
`While` subtree. The trusted regeneration establishes that this constructor
tree is the translation of submitted `solution.py`. The claim therefore
executes the actual submitted program term under the ordinary semantic rules;
no call or loop body is replaced by `lpfSpec`.

### Satisfying states and ground substitution

All preconditions are realizable. For the universal claim, `N=4` with the
declared initial empty environment is a witness. For the loop claim,
`N=4,F=2`, arbitrary integer input, and `noResult` is a witness. The two example
initial configurations are concrete witnesses for their claims.

Ground substitution gives:

```text
lpfSpec(4,2)
=> lpfSpec(4 / 2, 2)
=> 2
```

because `2*2 <= 4`, `4 % 2 == 0`, and then `2*2 > 2`. Both Python
implementations and fresh K execution return 2. The reviewer-authored
`evidence/spec-witness.k` strengthens the two symbolic witnesses to exact final
maps and result 2; it proves with exit 0 and `#Top` in
`evidence/04-ground-claim-witnesses.log`. The prompt examples similarly compare
to 29 and 2 in stages 2 and 3.

### Adequacy limitation

The K theorem never states `isPrime(R)`, `N mod R == 0`, or that no larger prime
factor exists. Its postcondition is a computation summary. The informal bridge
is persuasive: candidates are advanced only after non-divisibility; any
candidate that divides after all smaller candidates have been rejected is
prime; division happens only while `F*F <= N`, so the new residual is at least
the removed factor; and at loop exit a composite residual would have a prime
factor below its square root that should already have been found. Hence the
final residual is prime and at least every removed prime factor. This reasoning
is not a machine-checked K claim. It is the reason for `CONCERNS`, not `FAIL`,
because the execution theorem itself remains truthful and finite differential
evidence supports the bridge.

## 5. Rule-by-rule static soundness review

The numbered source record is `evidence/05-numbered-k-sources.log`. There are no
additional candidate K helper files.

### Local syntax, configuration, and construct coverage

`MPY-SYNTAX` declares:

- `PyModule` with `Module(Stmts)`;
- empty-separated `Stmts` and comma-separated `Strings` lists;
- `Params(Strings)`;
- statement constructors `FuncDef`, `Assign`, `While`, `If`, and `Return`;
- expression constructors `Int`, `Name`, `BinOp`, and `Compare`; and
- a `CmpOps` list and `CmpOp`.

`SEMANTIC` adds `Result ::= noResult | result(Int)` and K items
`exec(Stmts)`, `execStmt(Stmt)`, and `setVar(String,Int)`. The configuration has
exactly the needed cells: `<k>`, immutable `<input>`, mutable `<env>`, and
`<result>`. No heap, allocation, stack, I/O, exception, or call-frame behavior
is used by the submitted program.

Every submitted constructor is covered:

| Program construct | Declaration | Behavior |
|---|---|---|
| `Module`/single `FuncDef`/`Params("n")` | `semantic.k:5,8,10` | entry harness `:63-66` |
| statement list | `:6` | `exec` rules `:68-69` |
| `Assign` | `:11` | evaluate then update `:71-74` |
| `While` | `:12` | true/false rules `:83-89` |
| `If` | `:13` | true/false rules `:76-81` |
| `Return` | `:14` | result rule `:91-93` |
| `Int`, `Name` | `:16-17` | `evalInt` `:43-44` |
| `BinOp` `+`, `*`, `//`, `%` | `:18` | `evalInt` `:45-50` |
| `Compare`/`CmpOp` `<=`, `==` | `:19-21` | `evalBool` `:53-56` |

The concrete runs in stage 3 exercise every used behavior.

### Function and equation inventory

There are exactly three local `[function]` declarations and no `[total]`
declarations:

1. `evalInt(Expr,Map)` (`semantic.k:42`) has six equations:
   integer literal, name lookup, addition, multiplication, guarded integer
   division, and guarded remainder (`:43-50`). Each is the ordinary
   mathematical operation. Division/remainder are guarded against zero; all
   operands in the actual program are positive, where K `/Int` and `%Int`
   coincide with Python `//` and `%`. The name rule requires the key to exist.
2. `evalBool(Expr,Map)` (`:52`) has two equations for `<=` and `==`
   (`:53-56`). They are exact and non-overlapping for the used operator tokens.
3. `lpfSpec(Int,Int)` (`verification.k:9`) has three equations: stop when
   `F*F>N`; divide when `F*F<=N` and `F` divides `N`; otherwise increment `F`
   (`:10-15`). Their guards are disjoint and cover the proof domain
   `N>1,F>=2`. Division strictly reduces positive `N`; incrementing `F`
   eventually reaches the stop guard for fixed `N`. Calls remain in that
   domain. The function is intentionally not declared total outside it (for
   example, no division-by-zero behavior for `F=0`). These equations define the
   trial-division summary; they do not assume its largest-prime-factor meaning.

There are no opaque symbols, fresh result-bearing functions, local priorities,
`[simplification]` equations, `[total]` declarations, or `[functional]`
declarations. The three `[function]` declarations are the ones inventoried
above.

### Ordinary semantic rule inventory

1. The module-entry rule (`semantic.k:63-66`) matches exactly one
   `largest_prime_factor(n)` definition, initializes `n` from `<input>`, and
   schedules its real body. It is an explicit verification harness for the
   requested entry point, not a summary of the body.
2. The two list rules (`:68-69`) make empty execution disappear and sequence
   the head before the tail with `~>`, preserving source order.
3. Assignment and `setVar` (`:71-74`) read the current environment, evaluate a
   pure expression, then update exactly the selected map key.
4. The two `If` rules (`:76-81`) have complementary Boolean guards and schedule
   exactly one branch.
5. The two `While` rules (`:83-89`) have complementary guards. The true rule
   schedules the body and then the same loop term, so the guard is reevaluated
   in the updated environment and the loop claim returns to the real loop head.
6. Return (`:91-93`) evaluates `n` in the current environment and writes the
   only result. In a general Python subset this rule would need abrupt
   continuation handling: a hypothetical statement after a return would still
   remain scheduled. That is a scope limitation, not a false rule used by this
   proof: the submitted return is the final statement, and its only generated
   suffix is `exec(.Stmts)`, which has no state or control effect. A second
   return would also be unmodeled once `<result>` is nonempty, but none exists.

The module loader is the only modeled entry-call mechanism. General Python
function-definition/call semantics is deliberately absent, but no `Call`
constructor or nested function is present in `solution.mpy`. This is acceptable
minimal generated-semantic coverage rather than fabricated behavior.

### Proof-local macros and claims

`factorLoop` and `solutionModule` are the only `[macro]` declarations
(`verification.k:19-35`). Their two macro rules expand to exact submitted AST
fragments at compile time. They neither rewrite runtime execution nor inject a
result.

`spec.k` has exactly four reachability claims, restated in stage 4. The loop
claim is a checked circularity over the actual stable loop head. On a
divisibility step its post-summary follows the second `lpfSpec` equation; on an
increment step it follows the third; on loop exit it follows the first. The
entry theorem uses that checked loop claim after executing the real module
loader and initial assignment. The example claims execute the same complete
module.

### Static soundness conclusion

No inventoried rule encodes the task answer, replaces a property-bearing
program computation with an oracle, bypasses the loop, or silently fabricates a
value for a used construct. No materially unsound rule was found, so there is
no false-conclusion witness to report. The two general-language limitations
above are explicitly outside the submitted construct contexts and cannot
enable a false result for the real program on the intended domain.

## 6. Fresh non-vacuity test

The candidate supplied no vacuity test, so I created
`evidence/spec-vacuity.k`. It executes the exact complete program at `N=4` but
mutates the result obligation from the true 2 to the false 3.

First:

```text
kprove spec-vacuity.k --definition /tmp/audit-work/review-59/build/verification-haskell-kompiled --spec-module SPEC-VACUITY --dry-run --output pretty
```

exited 0, establishing that the mutation parsed and built
(`evidence/06-vacuity-dry-run.log`). The actual proof command then exited 1
with `WarnStuckClaimState`. Its residual is a fully terminated real execution:
empty `<k>`, environment `{factor: 2, n: 2}`, and `result(2)`, which cannot
unify with required `result(3)`. See `evidence/06-vacuity-proof.log`.

This is the expected unmet result obligation for a satisfiable input, not an
unreachable mutation, parser failure, missing import, timeout, or unrelated
crash. Stage result: non-vacuity passes.

## 7. Proven versus assumed accounting

### Machine-checked facts

Conditional on the source-built K definition and K's reachability logic:

- for every `N>1,F>=2`, terminating execution of the exact factor loop and
  return computes `lpfSpec(N,F)` in both `n` and `<result>`;
- for every `N>1`, terminating execution of the exact submitted module from the
  declared initial state computes `lpfSpec(N,2)`;
- the complete program returns 29 for 13195 and 2 for 2048; and
- the false result 3 for input 4 is rejected.

This is partial correctness. The report does not upgrade it to a formal
termination theorem.

### Trust ledger

| Boundary | Influence and dependents | Assessment/evidence |
|---|---|---|
| K v7.1.293 parser, compiler, Haskell/LLVM backends, reachability logic, and built-in `INT`, `BOOL`, `MAP`, and `List` modules | All parsing, arithmetic, maps, concrete runs, and proofs | Standard low-level trusted computing base; fresh builds and exact logs |
| Trusted `/reference/py2mpy.py` | Bridge from `solution.py` to the constructor tree proved | Authorized translator; byte identity in `evidence/02-regenerate-mpy.log` |
| Generated entry harness and Python-subset rules | Bridge from constructor execution to intended Python behavior | Audited rule by rule; all used constructs concretely exercised; finite K/Python comparisons in stage 3 |
| `lpfSpec` equations | Exact returned value in loop and entry claims | Not opaque and not assumed: execution-to-summary connection is machine checked |
| `lpfSpec(N,2)` means “largest prime factor of `N`” | Human-facing correctness conclusion | Ordinary mathematical argument only, plus 929-case independent differential test; not a K theorem, hence the concern |
| Existential final factor/example map | Non-result state only | Acceptable; cannot affect the equality-constrained `<result>` |

There are no opaque primitives or empirical oracles inside the proof theory.
Differential testing supports only the generated-semantics/Python and
summary/intent bridges on tested inputs; it is not treated as a universal K
proof.

### Gate summary

- Real-program soundness: **pass**.
- Intent adequacy: **sound but formally limited** by the unproved
  summary-to-largest-prime-factor bridge.
- Trust and reproducibility: **pass**, with all limits stated.

The formal limitation warrants `CONCERNS`, while the successful reconstruction,
exact program pinning, truthful theory, and non-vacuity warrant `LEGIT`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
