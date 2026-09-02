# Independent adversarial audit: 96-count-up-to

## Decision

The candidate contains a legitimate, result-constraining partial-correctness
proof of the exact submitted `solution.mpy` under its freshly rebuilt generated
semantics. The proof is not vacuous, and the semantic transition system does
not call the proof-side `isPrime` or `primesBelow` summaries as an oracle.

The result is `CONCERNS / LEGIT`, rather than an unqualified pass, for three
bounded reasons:

1. `semantic.k` uses a program-specific, whole-AST checked lowering into a
   `scan`/`trial` abstract machine. I found that lowering faithful for the
   submitted program and input domain, but its connection to CPython is an
   audited informal bridge plus finite differential evidence, not a
   machine-checked compiler-correctness theorem.
2. The final interpretation of `noFactor` as mathematical primality relies on
   the standard square-root divisor theorem. The K proof connects execution to
   the recursive `noFactor` definition, but does not separately formalize that
   elementary number-theory theorem.
3. The `[total]` declarations for `noFactor` and `primesFrom` are broader than
   their defining equations. The uncovered arguments cannot arise in any
   submitted claim, so this is not a false-conclusion witness on the intended
   domain, but it is avoidable global under-specification.

All candidate reports, compiled definitions, and traces were treated only as
untrusted claims.

## 1. Input and provenance integrity

### Rendered-mode boundary

The rendered mode is `GENERATED_SEMANTICS`. `/reference/reference-semantics`
does not exist, exactly as required. The trusted mount contains only:

- `/reference/prompt.py`
- `/reference/canonical.py`
- `/reference/py2mpy.py`

There is no supplied or inferred hidden reference semantics. Evidence:
`evidence/01-provenance.log`.

### Candidate artifacts and identity checks

All required candidate source and generation-record artifacts are regular
files. No candidate symlink exists at any depth. The candidate prompt and
translator are byte-identical to the trusted mounts:

- prompt SHA-256:
  `87a89ca2716858e3f17b04c2b3a30af694d0daa68da3e197f801a408d3b6bfb5`
- translator SHA-256:
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`

No required artifact is missing, changed, mistyped, or symlinked. There are no
helper K source files beyond `semantic.k`, `verification.k`, and `spec.k`.

The candidate additionally contains `semantic-kompiled/`,
`verification-kompiled/`, and `__pycache__/`. Those are extra generated
definitions/caches, not source. I did not execute or reuse them. The structured
trace is one regular JSONL file with 207 parseable records. Evidence:
`evidence/01-provenance.log`, `evidence/02-generation-trace-claims.log`, and
`evidence/03-codex-output-scan.log`.

### Untrusted generation claims read

`run-input.json` identifies problem `96-count-up-to`, condition `bare`, and
hashes matching the trusted prompt and translator. `metrics.json` claims an
exit status of 0 without timeout. `codex-last.txt`, `codex-output.log`, and the
structured trace claim that examples, translation, differential checks, and
`kprove` succeeded.

The log also records multiple intermediate parser, backend, and proof failures
before the candidate's final successful run. None of those records was used as
proof evidence. The full JSONL trace was parsed independently, and the complete
14,419-line text log was scanned. Exact extraction commands and outputs are in
`evidence/02-generation-trace-claims.log` and
`evidence/03-codex-output-scan.log`.

The live audit used K v7.1.293 and Python 3.10.12; see
`evidence/24-toolchain.log`.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For a non-negative integer `n`, `count_up_to(n)` must return, in ascending
order, the list of all prime integers strictly less than `n`. The examples
resolve the prompt's awkward phrase “first n integers” in favor of “all primes
less than n.” Thus `n` is a bound, not a requested list length.

The trusted canonical implementation tests every candidate in `[2,n)` against
all smaller potential divisors. The submitted implementation uses the
equivalent square-root trial-divisor algorithm:

- `candidate` ranges from 2 through `n - 1`;
- `divisor` ranges upward from 2 while
  `divisor * divisor <= candidate`;
- a found factor permanently clears `is_prime`;
- a candidate still marked prime is appended;
- the candidate then increments by one.

Not breaking after a found divisor affects efficiency only; `is_prime` remains
false.

### Trusted translation

I copied only candidate source files and trusted reference inputs into
`/tmp/audit-work/96-count-up-to`; no candidate compiled directory or cache was
copied. The exact copy inventory is in
`evidence/04-scratch-source-copy.log`.

Fresh translation used:

```text
python3 /tmp/audit-work/96-count-up-to/py2mpy.py \
  /tmp/audit-work/96-count-up-to/solution.py
```

The regenerated term is byte-identical to the submitted `solution.mpy`; both
have SHA-256
`f3d90b24a900cac792edf56af7c2e9b0b5d23a6318e23844a745a4867e85dc87`.
See `evidence/05-translator-byte-identity.log` and
`evidence/regenerated-solution.mpy`.

### Independent differential testing

`evidence/differential_test.py` independently imports the trusted canonical
entry point and the scratch copy of the submitted entry point. It covers:

- all six documented examples;
- the empty and outer-loop boundaries `0`, `1`, and `2`;
- entry into the loop at `3`;
- inner-loop zero-iteration cases;
- divisible and non-divisible inner branches;
- perfect-square equality at candidates 9 and 25;
- strict exclusion of the upper bound;
- every input from 0 through 300;
- 64 deterministic generated inputs in `[0,1000]` using seed `960096`.

After de-duplication, 341 inputs were tested. The complete input list is in the
log and has SHA-256
`3d049e03026b9eb0066f1837efe1f239d80916c327876fae002f8b4d68cad0fb`.
There were zero canonical mismatches and zero failures against a separately
implemented primality-property oracle. Command, inputs, representative outputs,
and exit status 0 are in `evidence/06-differential.log`.

## 3. Clean proof reconstruction

### Fresh semantics build and concrete execution

The candidate's compiled definitions were ignored. The generated semantics was
freshly built from the scratch source:

```text
kompile semantic.k --backend haskell --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition semantic-fresh-kompiled
```

It exited 0 (`evidence/07-kompile-semantic.log`).

Fresh `krun` executions covered
`N = 0,1,2,3,4,5,10,11,18,20,26,50`. Every run exited 0 with an empty final
`<k>` cell. Each K `nil`/`cons` result exactly matched both the trusted
canonical implementation and the submitted Python implementation. This covers
zero outer iterations, zero inner iterations, both divisor branches, the
`D*D == C` boundary, normal composite and prime candidates, and all documented
examples. Exact per-input commands and complete bounded outputs are in
`evidence/08-concrete-semantics-compare.log`.

### Fresh proof build

The proof definition was rebuilt from `verification.k` and the fresh source
imports:

```text
kompile verification.k --backend haskell --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-fresh-kompiled
```

It exited 0 (`evidence/09-kompile-verification.log`).

### Positive claims

The claims form a dependency hierarchy: `scan-correct` uses
`trial-correct`, and `count-up-to-correct` uses both loop claims. Each target
was therefore run in a fresh dependency-closed selection; dependencies were
re-proven, not imported from a candidate cache.

| Target | Fresh command selection | Result |
|---|---|---|
| `trial-correct` | `--claims SPEC.trial-correct` | exit 0, `#Top` |
| `scan-correct` | `--claims SPEC.trial-correct,SPEC.scan-correct` | exit 0, `#Top` |
| `count-up-to-correct` | all three claims in `SPEC` | exit 0, `#Top` |

The exact successful logs are:

- `evidence/10-kprove-trial-correct.log`
- `evidence/14-kprove-scan-with-helper.log`
- `evidence/13-kprove-all-claims.log`

As a dependency-sensitivity diagnostic, selecting `scan-correct` while
deliberately excluding `trial-correct` exited 1 after unbounded trial-loop
unrolling reached undecidable symbolic modulus constraints
(`evidence/11-kprove-scan-correct.log`). Selecting only the end claim was
bounded at 20 seconds and exited 124
(`evidence/23-kprove-count-only-bounded.log`). These are not treated as
candidate failures: they omit the submitted helper claims needed by the
dependency-closed proof. They do show that the broad claims did not close
without their stated loop summaries.

## 4. Adequacy and real-program pinning

### Claims in plain language

| Claim | Preconditions | Postcondition |
|---|---|---|
| `trial-correct` | `C >= 2`, `D >= 2`; `B`, `N`, and continuation `K` are otherwise arbitrary | Running the remaining divisor loop is equivalent to advancing to candidate `C+1`, and includes `C` exactly when the prior flag `B` is true and no divisor exists from `D` through `floor(sqrt(C))`; the continuation is preserved. |
| `scan-correct` | `C >= 2`; `N` and continuation `K` are arbitrary | `scan(C,N)` produces `primesFrom(C,N)` and preserves `K`. |
| `count-up-to-correct` | `N >= 0`, exact submitted AST in `<k>`, input cell `<n>N</n>`, and initially empty result | The computation is consumed and the result becomes exactly `primesBelow(N)`. |

None of the result-bearing RHS variables is fresh or unconstrained.
`primesBelow(N)` is an exact recursively defined `PList`, not a one-way
implication or an existential placeholder.

### Exact program identity

The end claim and the semantic lowering contain normalized identical `Module`
terms. Their normalized hashes are both
`b21cd8a80631f72bedfead9193a41d7db2d55acbadfc497e64160ec8eece4b2b`;
see `evidence/21-pinning-check.log`.

The trusted translator reproduced the submitted term byte-for-byte, and fresh
`krun` accepted that term and reached the result. Thus the proof does not use a
substituted AST. K list units such as `.Stmts` and `.Exprs` in the lowering are
exact empty-list units, not wildcard variables.

An operational-sensitivity mutation changed the outer increment from `+ 1` to
`+ 2`. The trusted translator produced a changed AST, and fresh `krun` left the
complete `Module` term visibly stuck with an empty result; it did not enter the
checked lowering or fabricate a list. The corrected successful sensitivity
record is `evidence/16-body-sensitivity-corrected.log`. The earlier reviewer
script assertion typo and its failure are preserved transparently in
`evidence/15-body-sensitivity.log`.

### Satisfiable witnesses

Every claim precondition has a concrete witness:

- `trial-correct`: `C=4`, `D=2`, `B=true`, `N=5`, `K=.K`.
  Here `noFactor(4,2)=false`, and the real trial steps reach
  `scan(5,5) ~> prependIf(4,false)`.
- `scan-correct`: `C=2`, `N=5`, `K=.K`; `primesFrom(2,5)=[2,3]`.
- `count-up-to-correct`: `N=5` with an empty initial result;
  `primesBelow(5)=[2,3]`.

Both Python implementations return `[2,3]` for the entry witness, and fresh K
execution returns `cons(2,cons(3,nil))`. See
`evidence/22-claim-witnesses.log` and the `N=5` case in
`evidence/08-concrete-semantics-compare.log`.

## 5. Rule-by-rule static soundness review

The complete numbered source and attribute scans are preserved in
`evidence/18-static-inventory-corrected.log`. The failed first version of the
reviewer inventory script is retained in `evidence/17-static-inventory.log`.

### Local syntax and configuration inventory

Every local production is accounted for:

1. `Program`: `Module(Stmts)`.
2. `Stmts`: juxtaposed list of `Stmt`.
3. `Exprs`: comma-separated list of `Expr`.
4. `Stmt`: `FuncDef(String, Params(String), Stmts)`.
5. `Stmt`: `Assign(Expr,Expr)`.
6. `Stmt`: `While(Expr,Stmts)`.
7. `Stmt`: `If(Expr,Stmts,Stmts)`.
8. `Stmt`: `Return(Expr)`.
9. `Expr`: `Name(String)`.
10. `Expr`: `Int(Int)`.
11. `Expr`: `Bool(Bool)`.
12. `Expr`: `ListExpr(Exprs)`.
13. `Expr`: `BinOp(String,Expr,Expr)`.
14. `Expr`: `Compare(Expr,Cmp)`.
15. `Cmp`: `CmpOp(String,Expr)`.
16. Runtime `PList`: `nil`.
17. Runtime `PList`: `cons(Int,PList)`.
18. Runtime `PList`: `chooseCons(Bool,Int,PList) [function,total]`.
19. `KItem`: `scan(Int,Int)`.
20. `KItem`: `trial(Int,Int,Bool,Int)`.
21. `KItem`: `prependIf(Int,Bool)`.
22. `KItem`: `returnValue`.
23. Proof-side `Bool`: `noFactor(Int,Int) [function,total]`.
24. Proof-side `Bool`: `isPrime(Int) [function,total]`.
25. Proof-side `PList`: `primesFrom(Int,Int) [function,total]`.
26. Proof-side `PList`: `primesBelow(Int) [function,total]`.

The configuration has only the state needed by this entry harness:

- `<k>` holds the exact program or abstract-machine computation;
- `<n>` holds the integer argument;
- `<result>` holds the returned `PList`.

There are no heap, I/O, exception, or global-state cells. That omission is
adequate for this pure, closed function on non-negative integers: all source
variables are local, list aliases do not escape, arithmetic does not overflow,
and the modeled operations cannot raise on the intended domain.

The submitted term uses exactly `Module`, `FuncDef`, `Params`, `Assign`,
`While`, `If`, `Return`, `Name`, `Int`, `Bool`, `ListExpr`, `BinOp`, `Compare`,
and `CmpOp`, with literal operators `+`, `*`, `%`, `<`, `<=`, and `==`. Every
one is declared and checked literally by the whole-program lowering. There is
no `Call` AST in the submitted module; the `<n>`/`<result>` configuration is the
entry-point invocation harness.

### Semantic rules

| ID | Rule | Static judgment |
|---|---|---|
| S1 | `chooseCons(true,C,P) => cons(C,P)` | True definition of conditional inclusion. |
| S2 | `chooseCons(false,_,P) => P` | True complementary case. Guards are constructor-disjoint and exhaustive for `Bool`. |
| S3 | exact `Module(...) => scan(2,N) ~> returnValue` | Program-specific operational lowering. It matches every submitted identifier, literal, operator, statement order, and empty block/list unit. It reads only `<n>` and preserves the surrounding continuation. It does not mention proof-side prime summaries. The source-to-machine equivalence is informal but was audited and differentially tested. |
| S4 | `scan(C,N) => nil` if `C >= N` | Correct empty suffix for `[C,N)`. |
| S5 | `scan(C,N) => trial(C,2,true,N)` if `C < N` | Correct candidate-loop entry. S4/S5 are disjoint and exhaustive for integers. |
| S6 | `trial(C,D,B,N) => scan(C+1,N) ~> prependIf(C,B)` if `D*D > C` | Correct exit from the divisor loop. |
| S7 | divisible trial step sets flag false when `D*D <= C`, `C%D==0`, `D!=0` | Matches the source assignment and increment. Discards only the prior flag, which is overwritten by `false` in the source. |
| S8 | non-divisible trial step preserves `B` and increments `D` | Matches the complementary source path. |
| S9 | completed suffix `P ~> prependIf(C,B)` conditionally prepends `C` | The recursive scan computes larger candidates first, then prepends `C`; this gives the same ascending final list as the source's forward append. No intermediate list identity is observable. |
| S10 | `P ~> returnValue` consumes computation and writes empty `<result>` | Correct entry-harness return. The end claim supplies the required empty initial result. |

On all reachable trial states, `C >= 2` and `D >= 2`. Thus S6 versus
S7/S8 is exhaustive, and under `D*D <= C`, divisibility versus
non-divisibility is exhaustive. The explicit `D != 0` guard is redundant on
that domain. For an artificial `D=0` state the machine can stick, but no
submitted execution or claim admits it, and the syntax need not cover unused
runtime states.

The abstract machine faithfully encodes the source-local state:

- `C` is `candidate`;
- `D` is `divisor`;
- `B` is `is_prime`;
- pending `prependIf` continuations encode the final `primes` list;
- `N` is the fixed input.

The inner trial completes before inclusion is decided, candidate increments are
by one, and the upper bound is strict. No rule skips a source-visible side
effect, allocation alias, output, exception, or abrupt control effect on the
intended domain.

### Verification functions and equations

| ID | Rule | Static judgment |
|---|---|---|
| V1 | `noFactor(C,D) => true` if `D*D > C` | Correct empty divisor suffix. |
| V2 | `noFactor(C,D) => false` on a nonzero divisor | Correct factor case. |
| V3 | otherwise recurse at `D+1` | Correct non-factor case and strictly advances on the used domain. |
| V4 | `isPrime(C) => false` if `C < 2` | Correct. |
| V5 | `isPrime(C) => noFactor(C,2)` if `C >= 2` | Correct trial-divisor definition. |
| V6 | `primesFrom(C,N) => nil` if `C >= N` | Correct empty range. |
| V7 | for `C < N` and `C >= 2`, conditionally prepend `C` and recurse at `C+1` | Correct ascending list definition and strictly decreasing range size. |
| V8 | `primesBelow(N) => primesFrom(2,N)` | Exact task-bound specialization. |

V1–V3 are disjoint and exhaustive for the only used domain
`C >= 2, D >= 2`, and recursion terminates there. V4/V5 are disjoint and
globally exhaustive. V6/V7 are disjoint and exhaustive whenever `C >= 2`,
which covers every use from `primesBelow`, `scan-correct`, and recursive V7.

Two declarations are globally broader than their equations:

- `noFactor(0,0)` has no applicable equation because `0*0 > 0` is false and
  both remaining rules require a nonzero divisor.
- `primesFrom(1,2)` has no applicable equation because `1 >= 2` is false and
  the recursive rule requires `C >= 2`.

These are concrete coverage-gap witnesses for the advertised global `[total]`
attributes. They are not false-conclusion witnesses on the intended domain:
no entry/helper precondition, semantic transition, or recursive equation can
produce either shape. Following the audit instruction, I therefore do not call
the equations unsound; I record the narrower totality-scope concern.
`isPrime`, `primesBelow`, and `chooseCons` are fully covered for all their
argument sorts.

### Claims and extension attributes

The only claims are `trial-correct`, `scan-correct`, and
`count-up-to-correct`, inventoried in Stage 4. There are:

- no local `[simplification]` rules;
- no `[concrete]` rules;
- no priority or `owise` rules;
- no opaque or fresh result symbols;
- no macros, `anywhere` rules, or trusted claims;
- no local `[functional]` declarations distinct from the five
  `[function,total]` symbols.

The proof-side summaries do not replace source execution. The semantic machine
uses `trial` and `scan`; the proof independently connects them to
`noFactor` and `primesFrom` through the reachability claims. In particular,
neither the whole-AST lowering nor a semantic step rewrites directly to
`isPrime` or `primesBelow`. This avoids the circular “same oracle in execution
and postcondition” failure.

I found no inventoried rule that enables a false result on the intended
non-negative input domain, so there is no unsound-rule accusation requiring a
false-conclusion witness.

## 6. Fresh non-vacuity test

There was no candidate `spec-vacuity.k`. I created a fresh reviewer mutation in
scratch and preserved it as `evidence/spec-vacuity.k`.

The mutation retains and re-proves both helper claims, fixes the satisfiable
input condition `N == 5`, and changes the result-constraining end postcondition
from `primesBelow(N)` to `nil`. This is demonstrably false because both Python
implementations and fresh K execution return `[2,3]`.

The mutation first built successfully:

```text
kprove spec-vacuity.k --definition verification-fresh-kompiled \
  --spec-module SPEC-VACUITY --dry-run
```

Exit status was 0 (`evidence/19-vacuity-dry-run.log`).

The real mutation proof then exited 1 with
`WarnStuckClaimState`. Its residual was the expected final configuration:

```text
<n> 5 </n>
<k> .K </k>
<result> cons(2, cons(3, nil)) </result>
```

That concrete result does not unify with the mutated `nil` destination. This is
a meaningful unmet result obligation, not a parser error, missing import,
timeout, unrelated crash, or unreachable mutation. Exact command and output:
`evidence/20-vacuity-proof.log`.

## 7. Proven versus assumed accounting

### What is formally proved

Under the freshly rebuilt MPY/VERIFICATION K theory, for every mathematical K
integer `N >= 0`, starting from:

- the exact translated `Module(FuncDef("count_up_to", ...))` term;
- `<n> N </n>`;
- an empty `<result>`;

the partial-correctness reachability claim consumes the computation and yields
exactly `primesBelow(N)` in the result cell. `primesBelow` is definitionally the
ascending `nil`/`cons` list of numbers in `[2,N)` accepted by `noFactor(_,2)`.
The helper claims establish the divisor-loop and candidate-loop summaries used
by the end claim.

This is not merely a proof that some free result exists, and it is not a proof
of a substituted program.

### Trust ledger and limitations

| Boundary | Dependents | Assessment |
|---|---|---|
| K v7.1.293 reachability prover, circularity mechanism, parser, and Haskell backend | All machine-checked claims | Standard toolchain trust boundary. Rebuilt and exercised, not re-proved. |
| K builtin unbounded `Int` arithmetic, comparisons, positive-divisor `%Int`, `Bool`, list units, and K sequencing | All semantic and proof rules | Acceptable primitive boundary. On positive divisors these operations match Python's integer behavior; Python and K integers are both unbounded here. |
| Trusted `py2mpy.py` | Source-to-`solution.mpy` identity | Trusted mounted transliterator. Byte identity was independently re-established; it supplies syntax, not semantics. |
| Whole-AST lowering to `scan`/`trial` and implicit entry invocation through `<n>` | End-to-end link from the submitted AST to the abstract machine | Audited but not machine-checked against a separate Python semantics. Exact AST pinning, source-mutation rejection, concrete K/Python comparisons, and rule-by-rule correspondence support it. This is the main reason for `CONCERNS`. |
| `nil`/`cons` as the Python list representation | Human-facing result interpretation | Straightforward structural bridge, checked concretely. No aliasing or mutation is observable after return. |
| Square-root divisor theorem: a composite `C >= 2` has a divisor no greater than `sqrt(C)` | Meaning of `isPrime` and therefore `primesBelow` | Ordinary mathematical argument, not a separate K theorem. The recursive equations compute the stated test exactly. |
| Global values of `noFactor` and `primesFrom` outside their covered claim domains | No submitted claim depends on them | Under-specified `[total]` scope; concerning for reuse, immaterial to this theorem. |
| Differential tests | Python equivalence and generated-semantics bridge on tested values only | Finite evidence, not a universal proof. Scope and zero mismatch count are fully recorded. |

There are no opaque symbols, external calls, random values, I/O primitives,
heap operations, or proof-local trusted rewrites.

### Excluded behavior

The formal theorem excludes negative inputs, non-integer Python values, changed
source bodies, and general Python programs not equal to the checked AST. It is
a partial-correctness theorem; termination is apparent from increasing
`divisor` and `candidate` measures but is not the theorem claimed here.

### Gate summary

- Real-program soundness: pass on the stated generated-semantics theorem
  domain. Exact source pinning, dependency-sensitive helper claims, body
  sensitivity, result sensitivity, and non-vacuity all succeeded.
- Intent adequacy: legitimate with a documented limitation. The generated
  semantics and number-theory interpretation were independently audited and
  empirically supported, but their universal connection to CPython/natural
  language is informal.
- Trust/evidence auditability: pass. Reviewer artifacts, commands, exit
  statuses, inputs, and bounded outputs are preserved under `evidence/`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
