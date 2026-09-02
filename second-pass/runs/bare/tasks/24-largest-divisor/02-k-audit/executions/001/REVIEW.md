# Independent adversarial review: 24-largest-divisor

## Outcome

The candidate contains a legitimate partial-correctness proof for the submitted
program on integers `N > 1`. I rebuilt both K definitions from source, proved
the loop claim independently, proved the complete two-claim specification, and
checked the entry claim modularly after independently establishing its loop
theorem. All relevant successful `kprove` runs exited 0 and printed `#Top`.

The proof is result-constraining and body-sensitive. A fresh, satisfiable
mutation requiring the result to equal 2 failed after reaching a final `.K`
configuration, and changing the program's initialization from `N - 1` to `N`
also failed at the resulting wrong return value.

The exact theorem is deliberately limited to `N > 1`, where a positive proper
divisor exists. This agrees with the meaningful domain of the prompt and the
trusted canonical implementation. The candidate and canonical implementation
differ at `N = 0`, outside the formal and meaningful domain; that difference is
reported below and is not hidden by the verdict.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `GENERATED_SEMANTICS`.
`/reference/reference-semantics` is absent, as required. I did not search for or
use a hidden reference semantics. There is therefore no infrastructure breach.

The mechanical provenance check is
[`evidence/01-provenance.log`](evidence/01-provenance.log). It reports:

- Every required candidate artifact is a regular file:
  `run-input.json`, `metrics.json`, `codex-last.txt`,
  `codex-output.log`, `prompt.py`, `py2mpy.py`, `solution.py`,
  `solution.mpy`, `semantic.k`, `verification.k`, `spec.k`, and
  `prove.sh`.
- There are no symlinks anywhere below `/candidate`.
- Candidate `prompt.py` is byte-identical to `/reference/prompt.py`;
  both have SHA-256
  `3bc8bf3f66a3b5e171a358bbd5f33fba1a5d16ea65459198757dcb662dbaaac2`.
- Candidate `py2mpy.py` is byte-identical to `/reference/py2mpy.py`;
  both have SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.
- The structured trace contains 244 valid JSONL records and no malformed
  record.

No required artifact is missing, changed, mistyped, or symlinked. There are no
additional candidate helper `.k` files. The extra top-level directories
`semantic-kompiled/` and `verification-kompiled/` are candidate-produced build
outputs; they were treated as untrusted and never copied or used. The remaining
extra material (`codex-trace/` and the requested generation logs/metrics) is
supporting evidence rather than proof source.

All source hashes are recorded in
[`evidence/17-source-hashes.log`](evidence/17-source-hashes.log).

### Untrusted generation claims

I read `run-input.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, and the complete structured trace only as claims:

- `run-input.json` identifies problem `24-largest-divisor`, condition `bare`,
  and no supplied semantics.
- `metrics.json` claims a 922-second successful, non-timeout generation run.
- `codex-last.txt` claims the universal `N > 1` proof printed `#Top`.
- The output log and trace contain intermediate compiler/proof failures,
  subsequent edits, later `#Top` outputs, and the final
  `KPROVE_PASSED` claim.

The complete trace was parsed by
[`evidence/trace_claim_summary.py`](evidence/trace_claim_summary.py), with its
bounded output in
[`evidence/02-trace-claims.log`](evidence/02-trace-claims.log).
Relevant claims from the text log are independently summarized in
[`evidence/02b-codex-output-claims.log`](evidence/02b-codex-output-claims.log).
None of those claimed outcomes was used in place of reconstruction.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and intended domain

The trusted prompt asks for the largest number below `n` that divides `n`
evenly, with example `largest_divisor(15) == 5`. The trusted canonical
implementation scans `n - 1, n - 2, ...` and returns the first divisor.

For the domain on which that request is defined, the contract is:

> Given an integer `n > 1`, return the greatest positive integer `d` such that
> `0 < d < n` and `n mod d = 0`.

`n > 1` is not an opportunistic proof restriction. At `n = 1` there is no
positive proper divisor and the canonical implementation raises
`ZeroDivisionError`; at `n = 0` it returns `None`. The prompt's mathematical
request has no valid positive-proper-divisor result there.

### Submitted algorithm

`solution.py` starts `divisor` at `n - 1`, decrements it while it does not
divide `n`, and returns the first divisor encountered. For `n > 1`, the search
cannot pass 1, because 1 divides every such integer. It therefore implements
the same descending search as the canonical program.

### Trusted translation

I regenerated the constructor program in scratch with the trusted translator:

```text
python3 trusted-py2mpy.py solution.py > regenerated-solution.mpy
cmp -l solution.mpy regenerated-solution.mpy
```

Both files have SHA-256
`dfeae40e927213369b88e91ab649f8cceb179f11256be1094e3ec8a8b8673a06`;
`cmp` exited 0. Exact command and status:
[`evidence/03-translation.log`](evidence/03-translation.log).

### Independent differential execution

[`evidence/differential_test.py`](evidence/differential_test.py) imports the
trusted canonical and candidate implementations from separate files. It tests:

- the documented input 15;
- every in-domain integer from 2 through 500;
- explicit branch-sensitive boundaries, including 2 (guard false
  immediately), 3 (prime search to 1), 4 (true then false), primes,
  composites, squares, and powers of two;
- 200 deterministic generated draws from 2 through 5000 using seed 240024;
- out-of-domain boundaries 0 and 1, reported separately.

There were 680 unique in-domain inputs and zero mismatches. At `n = 0`, the
canonical returns `None` and the candidate returns `-1`; at `n = 1`, both raise
`ZeroDivisionError`. There is no collection-valued “empty” input for this
integer function, so 0 and 1 are the relevant empty/boundary probes.

The exact command, test scope, results, and exit 0 are in
[`evidence/04-differential.log`](evidence/04-differential.log). This is finite
bridge evidence, not a substitute for the K proof.

## 3. Clean proof reconstruction

All candidate source needed for execution was copied to
`/tmp/audit-work/24-largest-divisor`. No candidate `*-kompiled` directory,
cache, generated definition, or trace was copied. Fresh definitions were
written to the distinct scratch directories `audit-semantic-kompiled/` and
`audit-verification-kompiled/`.

The installed toolchain is K `v7.1.293` and Python `3.10.12`; see
[`evidence/00-toolchain.log`](evidence/00-toolchain.log).

### Concrete definition

```text
kompile semantic.k --backend llvm --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-semantic-kompiled
```

This exited 0:
[`evidence/05-kompile-llvm.log`](evidence/05-kompile-llvm.log).

Fresh `krun` executions for `N = 2, 3, 4, 15, 49, 101, 1024` all exited 0,
ended with `.K`, and matched both Python implementations. This set covers
immediate loop exit, taken and untaken guard edges, prime searches, composites,
a square, and a power of two. Exact internal `krun` commands and complete final
configurations are in
[`evidence/06-concrete-semantics.log`](evidence/06-concrete-semantics.log).

### Proof definition and claims

```text
kompile verification.k --backend haskell --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
```

This exited 0:
[`evidence/07-kompile-haskell.log`](evidence/07-kompile-haskell.log).

The positive proofs were reconstructed as follows:

| Target | Command form | Result |
|---|---|---|
| Loop contract alone | `kprove ... --claims SPEC.largest-divisor-loop-contract` | exit 0, `#Top` |
| Complete submitted two-claim set | `kprove spec.k ... --spec-module SPEC` | exit 0, `#Top` |
| Entry claim modularly, after the loop theorem was proved | `kprove ... --claims loop,entry --trusted loop` | exit 0, `#Top` |

The exact logs are
[`evidence/08-kprove-loop.log`](evidence/08-kprove-loop.log),
[`evidence/09-kprove-all.log`](evidence/09-kprove-all.log), and
[`evidence/09b-kprove-entry-modular.log`](evidence/09b-kprove-entry-modular.log).

The modular `--trusted` use does not add an unproved assumption: the exact loop
claim was independently proved in the preceding command, and the ordinary
complete-spec command also proves both claims together. It separates the entry
obligation from its already-established auxiliary theorem.

As a diagnostic, filtering the spec down to the entry label alone also filters
out the circular loop theorem, so that form unrolls and was bounded at five
seconds. It is not a target-proof failure and played no role in the verdict;
the exact diagnostic is
[`evidence/09a-entry-selector-diagnostic.log`](evidence/09a-entry-selector-diagnostic.log).

## 4. Adequacy and real-program pinning

### Plain-language claims

**`largest-divisor-loop-contract`.** Start at the actual submitted `while`
loop, followed by the actual `return divisor` continuation, with:

- `N > 1`;
- environment exactly `n |-> N, divisor |-> D`;
- `0 < D < N`;
- every candidate from `D + 1` through `N - 1` already known not to divide
  `N`;
- no result yet.

When the loop and return finish, the environment's `divisor` and the result
cell must contain the same existential `RESULT`, and that value must be the
largest proper divisor of `N`.

**`largest-divisor-natural-contract`.** Start with the exact constructor tree
from submitted `solution.mpy`, argument `N > 1`, an empty environment, and no
result. At completion the computation must be consumed, the environment must
be exactly `n |-> N, divisor |-> RESULT`, the result cell must equal the same
`RESULT`, and `RESULT` must be the largest proper divisor.

### Pinning and control-flow match

The entry claim's constructor tree is byte-for-byte the trusted regeneration
of `solution.py`. It does not invoke a summary symbol or a substituted helper
program. The actual execution reaches the loop claim as follows:

1. The module rule binds `"n"` to `N`.
2. The first assignment sets `"divisor"` to `N - 1`.
3. Statement scheduling reaches the exact loop and exact trailing
   `Return(Name("divisor"))`.
4. At that point the loop precondition holds because
   `noDivisorFrom(N, N, N - 1)` is the empty interval.
5. Every taken iteration adds the just-rejected `D` to the known
   non-divisor interval and decrements `D`, returning to the same loop head.

The loop claim includes the complete continuation
`Return(Name("divisor")) .Stmts ~> .K` and all four configuration cells. It
does not accept an arbitrary suffix, omit mutable state, fabricate a return, or
pop a caller frame.

### Result constraint and satisfying states

`?RESULT` is not free: the same existential occurs in the final environment and
result cell, and the `ensures` clause constrains it with
`isLargestProperDivisor`. That predicate expands to:

- `RESULT > 0`;
- `RESULT < N`;
- `N mod RESULT == 0`;
- every integer from `RESULT + 1` through `N - 1` is a non-divisor.

This is an equivalent characterization of the requested greatest positive
proper divisor, not a one-way or tautological condition.

[`evidence/claim_witness_check.py`](evidence/claim_witness_check.py) exhibits
the ground witness `N = 15`; for the loop claim it uses `D = 14`. Both
preconditions are true. Substitution gives `RESULT = 5`, the candidate Python
result is 5, the canonical result is 5, and the postcondition is true. Exact
output: [`evidence/10-claim-witness.log`](evidence/10-claim-witness.log).

The separate body-sensitivity mutation changes only the initial assignment to
`divisor = n`. It builds but the proof reaches `.K` with result `N` and fails
on the proper-divisor obligation `N < N`. See
[`evidence/spec-body-mutation.k`](evidence/spec-body-mutation.k),
[`evidence/15-body-mutation-dry-run.log`](evidence/15-body-mutation-dry-run.log),
and
[`evidence/16-body-mutation-proof.log`](evidence/16-body-mutation-proof.log).
This confirms that the proof depends on the real initialization and that the
loop theorem's `D < N` guard does not overreach.

## 5. Rule-by-rule static soundness review

The line-numbered source and attribute search are preserved in
[`evidence/13-static-source-inventory.log`](evidence/13-static-source-inventory.log).
The trusted Python AST, constructor term, and used constructor names are in
[`evidence/14-program-constructs.log`](evidence/14-program-constructs.log).

### Local syntax and configuration inventory

| Declaration | Used by submitted program? | Review |
|---|---:|---|
| `Pgm ::= Module(Stmts)` | Yes | Represents the translated module tree. |
| `Params ::= Params(String)` | Yes | Represents the single parameter `"n"`. |
| `Expr ::= Int(Int)` | Yes | Used for 0 and 1. |
| `Expr ::= Name(String)` | Yes | Used for `n` and `divisor`. |
| `Expr ::= BinOp(String,Expr,Expr)` | Yes | Used only with `"-"` and `"%"`. |
| `Expr ::= Compare(Expr,CmpOp)` | Yes | Represents the single `!=` comparison. |
| `CmpOp ::= CmpOp(String,Expr)` | Yes | Carries comparator and RHS. |
| `Stmt ::= FuncDef(...)` | Yes | Exact entry function constructor. |
| `Stmt ::= Assign(Expr,Expr)` | Yes | Both assignments have `Name` targets. |
| `Stmt ::= While(Expr,Stmts)` | Yes | Exact loop. |
| `Stmt ::= If(Expr,Stmts,Stmts)` | No | Unused extra syntax; its rules do not affect this proof. |
| `Stmt ::= Return(Expr)` | Yes | Exact return. |
| `Stmts ::= List{Stmt,""}` | Yes | Preserves translator statement order. |
| `KItem ::= noResult` | Yes | Initial result marker; carries no hidden value. |
| `KItem ::= whileBranch(Expr,Stmts)` | Internal | Explicit loop-test continuation. |
| `KItem ::= branch(Stmts,Stmts)` | Internal, unused here | Explicit `if` continuation. |

The configuration contains exactly the needed state:

- `<k>` for computation;
- `<arg>` for the externally configured integer call argument;
- `<env>` for local bindings;
- `<result>` for the returned integer or `noResult`.

There is no heap, I/O, allocation, exception, or call-stack cell because none
is exercised by the submitted single-function, integer-only program.

### Semantic function equations

Every local semantic equation is inventoried below.

| Rule | Domain/overlap/descent | Assessment |
|---|---|---|
| `envInt(ENV,X) => {ENV[X]}:>Int` | Partial on a missing or non-integer binding; no `[total]` claim | Correct lookup for all program states reached here. |
| `evalInt(Int(I),_) => I` | Constructor-disjoint | Correct literal evaluation. |
| `evalInt(Name(X),ENV) => envInt(ENV,X)` | Constructor-disjoint | Correct binding lookup. |
| `evalInt(BinOp("-",A,B),ENV) => ... -Int ...` | Operator-disjoint | Correct unbounded-integer subtraction. |
| `evalInt(BinOp("%",A,B),ENV) => ... modInt ...` | Operator-disjoint | Correct for the strictly positive divisors established by the invariant. Division by zero visibly gets stuck rather than fabricating a result. |
| `evalBool(Compare(A,CmpOp("!=",B)),ENV) => ... =/=Int ...` | Comparator-disjoint | Exact submitted guard. |
| `evalBool(... "==" ...) => ... ==Int ...` | Comparator-disjoint, unused | Ordinary integer equality. |
| `evalBool(... ">" ...) => ... >Int ...` | Comparator-disjoint, unused | Ordinary integer greater-than. |

Expression evaluation is encoded as pure functions. Python left-to-right order
therefore has no observable discrepancy for the submitted expressions: there
are no calls, mutations, or exceptions on the `N > 1` execution path.

### Ordinary operational rules

| Rule | State/control effect | Assessment |
|---|---|---|
| `Module(FuncDef(_,Params(P),BODY))` | With empty env, binds `P` to `<arg>` and executes `BODY` | Faithful model of invoking the sole HumanEval entry point. The actual name/tree is pinned by the claim. |
| `S:Stmt REST:Stmts => S ~> REST` | Schedules statements left-to-right | Preserves source order. |
| `.Stmts => .K` | Removes an empty statement list | Correct list cleanup. |
| `Assign(Name(X),E)` | Evaluates in old `ENV`, then updates `X` | Preserves RHS-before-store behavior. |
| `While(COND,BODY)` | Evaluates the pure guard in current `ENV`, then installs `whileBranch` | Correct guard timing and stable loop head. |
| `true ~> whileBranch(...)` | Executes body, then the same loop | Correct taken edge. |
| `false ~> whileBranch(...)` | Consumes loop | Correct exit edge. |
| `If(COND,THEN,ELSE)` | Evaluates guard, then installs `branch` | Unused but ordinary for the modeled pure guards. |
| `true ~> branch(THEN,_)` | Selects then branch | Guards are disjoint. |
| `false ~> branch(_,ELSE)` | Selects else branch | Guards are disjoint. |
| `Return(E) ~> _:K` | Evaluates return expression, records result, discards the current function continuation | Correct for the only modeled function frame, including return from loop/branch context. It requires `noResult`, so it cannot fabricate a second return. |

Normal `N = 15` execution exercises module entry, statement scheduling,
assignment, both loop edges, lookup, subtraction, modulo, comparison, return,
and all cells. Boundary `N = 2` exercises the zero-iteration loop. Those fresh
executions are recorded in Stage 3.

There are no local priority declarations. The true/false branch rules are
disjoint; expression constructor/operator rules are disjoint; the statement
and empty-list rules are disjoint. No rule silently handles an unmodeled
constructor. Unsupported expressions or bad bindings remain visibly stuck.

### Verification function equations

| Rule | Validity and coverage | Assessment |
|---|---|---|
| `noDivisorFrom(_,LO,HI) => true` if `LO > HI` | Empty interval | True by definition. |
| Recursive `noDivisorFrom(N,LO,HI)` if `LO <= HI` | Tests `LO`, then increments it | Exactly enumerates the finite interval and strictly descends in interval length. Its proof uses all have `LO >= 1`; at `LO = 0`, `modInt 0` is partial and the function is not declared total. No false Boolean is fabricated. |
| `isLargestThrough(N,D,UPPER)` | Positive, bounded divisor plus no larger divisor | Direct conjunction of the mathematical property. |
| `isLargestProperDivisor(N,D)` | Adds `D < N`, uses upper bound `N - 1` | Equivalent to the requested result for `N > 1`. |

The two guards for `noDivisorFrom` are mutually exclusive and exhaustive over
integers. The single equations for the other predicates have no overlap. The
recursive helper increases `LO` until the base guard, so every use in the proof
terminates.

These functions are definitional summaries of the postcondition. They never
rewrite `While`, `Assign`, `Return`, or any program term and therefore are not
operational bridges. They encode the property to prove, not the answer produced
by execution.

### Attribute, oracle, and proof-extension inventory

- `[function]`: exactly `envInt`, `evalInt`, `evalBool`,
  `noDivisorFrom`, `isLargestThrough`, and
  `isLargestProperDivisor`.
- `[total]`: none.
- `[functional]`: none.
- `[simplification]` or `[concrete]` local rules: none.
- Priority, `owise`, `anywhere`, or macro rules: none.
- Opaque or fresh result-bearing symbols: none.
- Operational bridge rules in `verification.k`: none.
- Local trusted claims: none in the submitted files.

The loop claim is a derived reachability lemma/circularity, not an oracle. Its
matched context includes the exact loop, exact return suffix, `<arg>`, exact
two-binding `<env>`, and `<result> noResult`; its guards are the invariant. Its
state footprint and justification scope coincide. It was proved independently
under the fixed generated semantics and rejected the body mutation. The entry
claim is the target theorem over the exact program.

I found no unsound local rule. Accordingly, there is no claimed-unsound rule
for which a false-conclusion witness is owed. Partial behavior outside the
modeled/claimed domain is identified as such rather than mislabeled as a false
rule.

## 6. Fresh non-vacuity test

The accepted fresh mutation is
[`evidence/spec-vacuity.k`](evidence/spec-vacuity.k). It retains the exact
correct loop support claim and strengthens the entry postcondition with
`?RESULT ==Int 2`.

This mutation is meaningful and satisfiable:

- `N = 4` really returns 2, so the destination is not logically bottom.
- `N = 15` satisfies the original precondition and really returns 5, so the
  strengthened universal claim is false.

The mutated spec parsed and built to KORE successfully:

```text
kprove spec-vacuity.k --definition audit-verification-kompiled \
  --spec-module SPEC-VACUITY --dry-run
```

Exit was 0; see
[`evidence/11-vacuity-dry-run.log`](evidence/11-vacuity-dry-run.log).

The actual mutated proof:

```text
kprove spec-vacuity.k --definition audit-verification-kompiled \
  --spec-module SPEC-VACUITY --output pretty
```

exited 1 with `WarnStuckClaimState`. The residual contains a final
`<k> .K </k>`, the computed `?RESULT`, the original proper-divisor
constraints, and the unmet equality `?RESULT == 2`. This is the expected
result-sensitive failure, not a parser/import error, unrelated crash, timeout,
or unreachable mutation. See
[`evidence/12-vacuity-proof.log`](evidence/12-vacuity-proof.log).

For audit transparency, I first tried the stronger mutation `RESULT == N` and
rejected it because it made the RHS contradictory with `RESULT < N`; those
discarded logs are retained as
[`evidence/11a-rejected-bottom-mutation-dry-run.log`](evidence/11a-rejected-bottom-mutation-dry-run.log)
and
[`evidence/12a-rejected-bottom-mutation-proof.log`](evidence/12a-rejected-bottom-mutation-proof.log).
They are not counted as non-vacuity evidence.

## 7. Proven versus assumed accounting

### What the reachability proof establishes

Under the submitted generated semantics and K's imported integer/Boolean/map
theory, for every K integer `N > 1`, execution of the exact trusted-translated
constructor tree for `solution.py`, from an empty local environment and
`noResult`, is partially correct:

- if it terminates in the claimed final configuration, `<k>` is empty;
- the result and final `divisor` binding are the same integer;
- that integer is positive and strictly below `N`;
- it divides `N`;
- no larger integer below `N` divides `N`.

The auxiliary theorem establishes the same property from every real loop-head
state satisfying its invariant. The theorem does not merely state that the
execution agrees with an uninterpreted summary.

### Trust and assumption ledger

| Boundary | Dependents | Classification |
|---|---|---|
| Mounted prompt, canonical implementation, and translator | Intent statement, executable oracle, source-to-`.mpy` identity | Trusted inputs mandated by the audit. Byte identity was checked where required. |
| K toolchain and Haskell/LLVM backend correctness | Parsing, execution, and `#Top` proof result | Necessary low-level proof-system trust. Fresh builds avoid candidate caches. |
| Imported `INT`, `BOOL`, and `MAP` hooks | Arithmetic, comparisons, modulo, conjunction, map lookup/update | Acceptable standard K primitives. On the proof path integers are unbounded as in Python and modulo divisors remain positive. |
| Handwritten generated semantics as a model of the used Python subset | Bridge from constructor program to Python behavior | Audited rule-by-rule above. The bridge is direct for pure integer expressions and local control; seven fresh K/Python comparisons and 680 Python differential inputs provide finite independent support. No result-bearing oracle is involved. |
| Invocation modeling (`Module(FuncDef(...))` executes the sole entry body using `<arg>`) | HumanEval call configuration | Acceptable explicit model of calling the requested entry point; the function name, parameter, and body are pinned by the entry claim. |
| `N > 1` | Every proof claim | Explicit theorem domain, justified by existence of a positive proper divisor and canonical boundary behavior. |
| Program termination | Total-correctness conclusion | Not proved or claimed. The Kit theorem is partial correctness. Informally, termination for `N > 1` follows because the positive candidate decreases and 1 divides `N`, but this is outside the claimed result. |
| Modular `--trusted` loop label in one audit command | Separated entry-obligation replay | Not a remaining assumption: the exact loop theorem separately closed with `#Top`, and the unmodified two-claim spec also closed without a trusted label. |

Finite differential and concrete tests support only the translation/semantics
and intent bridges on their recorded inputs. They are not presented as a
universal proof. Universal result correctness comes from the reconstructed K
reachability proof plus the statically audited, non-oracular semantics and
predicate equations.

### Exclusions

The proof does not cover `N <= 1`, booleans masquerading as Python integers,
floats, arbitrary Python exceptions, missing bindings, division by zero, other
functions/calls, or unused translator constructs. It also does not prove
runtime complexity or total correctness. None of those exclusions is used to
make a false result provable for the intended `N > 1` domain.

VERDICT: PASS
LEGITIMACY: LEGIT
