# Independent adversarial audit: 123-get-odd-collatz

The candidate's build and `#Top` result are reproducible, and its generated
semantics soundly executes the submitted program on the exercised positive
inputs. The candidate nevertheless does **not** contain a partial-correctness
proof of the task contract over the intended domain. It proves eight fixed
executions, two one-step branch facts, and two ground observer calculations.
There is no symbolic entry claim, loop invariant, or postcondition connecting an
arbitrary positive input to the list of odd terms in its Collatz trajectory.

This is a material adequacy failure, not merely thin empirical support.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `GENERATED_SEMANTICS`. The required boundary check passed:
`/reference/reference-semantics` does not exist. I did not search for or use a
hidden semantics. The candidate's `semantic.k` is therefore audited on its own
merits in Stage 5. See
[`01-integrity.log`](evidence/01-integrity.log).

### Required artifacts and file integrity

The generation deliverables `solution.py`, `solution.mpy`, `semantic.k`,
`verification.k`, `spec.k`, and `prove.sh` are present. The required provenance
files `run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`, and
one structured JSONL trace are also present. All inspected source/provenance
artifacts are regular files. A recursive symlink scan of `/candidate` returned
no symlinks. No required generation artifact is missing, mistyped, or symlinked.

The candidate also contains `semantic-kompiled/`,
`verification-kompiled/`, and `__pycache__/`. These are untrusted generated
caches, not source inputs. None was copied into or used by the audit.

The candidate prompt and translator are byte-identical to the trusted mounts:

- `prompt.py`: SHA-256
  `517b9458e64b1285c8fed0636622367f2fbdd313e8f23027250740cd7588f9e3`;
- `py2mpy.py`: SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.

Both `cmp` commands exited 0. Full hashes are in
[`01-integrity.log`](evidence/01-integrity.log).

### Untrusted generation claims

I read and indexed every line of the structured trace and every byte of the four
provenance files. The JSONL trace is valid JSON on all 313 lines. It and
`codex-last.txt` claim that:

- all 12 claims closed together;
- two `krun` examples matched expected values;
- a CPython cross-check covered inputs 1 through 1000; and
- no universal termination result was claimed because of the Collatz
  conjecture.

Those statements were treated only as claims. The trace also explicitly
describes the intended proof as eight concrete entry executions, two symbolic
parity steps, and two observer checks. The complete bounded provenance index is
[`01-provenance-scan.log`](evidence/01-provenance-scan.log), produced by
[`01-provenance-scan.py`](evidence/01-provenance-scan.py).

The original generation instructions only made `KPROVE_PASSED` a report about
positive proof-command execution; they explicitly said it was not a validated
judgment. Thus the candidate's runner marker does not itself claim or establish
the result of this audit.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

For a positive integer `n`, repeatedly apply the integer Collatz transition:
halve an even value and replace an odd value by `3*n + 1`. If the trajectory
reaches 1, return all odd terms in that trajectory, including 1, sorted in
increasing order. In particular, input 1 returns `[1]`, and input 5 returns
`[1, 5]`.

Because this is a partial-correctness audit, universal Collatz termination need
not be proved. The required theorem can be conditional on termination; a loop
invariant can establish that, whenever the loop exits at 1, the accumulated list
contains exactly the odd trajectory terms.

### Source inspection

`solution.py` accumulates each odd current value before applying its odd
transition, halves positive even values using exact integer `//`, appends the
terminal 1, and sorts the result. For positive executions that reach 1, this is
faithful to the mathematical contract. It is a different but legitimate
organization from `canonical.py`.

The trusted translator regenerated `solution.mpy` byte-for-byte:

```text
66f5221c16c9b6d2b31815ba5c856f965d2c2ca1142b4152277aa3720cbb18e6
```

Both the translation and `cmp` exited 0. See
[`02-program-fidelity.log`](evidence/02-program-fidelity.log).

### Independent differential testing

The reviewer-authored differential test imports the trusted canonical entry
point and the scratch-copied candidate entry point independently. It covers:

- the zero-iteration boundary `n=1`;
- the first even and odd branch boundaries `n=2` and `n=3`;
- the documented example and mixed short/long paths;
- every integer from 1 through 1000; and
- 250 deterministic PRNG inputs in `1..1,000,000` with seed `123123`.

All 1,250 ordinary-scope comparisons matched, and all candidate results were
sorted and odd-only. The exact generated inputs and result digest are in
[`02-program-fidelity.log`](evidence/02-program-fidelity.log); the test is
[`02-differential.py`](evidence/02-differential.py). There is no valid “empty”
input because the contract accepts one positive scalar integer; `n=1` is the
relevant boundary. Inputs zero and below are outside the stated domain.

There is a material canonical discrepancy at the binary64 exact-integer
boundary. Four of five probes near `2**53` differ because the trusted canonical
uses Python `/`, converting intermediate integers to binary64 floats. For
example, at `n=2**53-1` the canonical returns four items while the candidate
returns 310. On all five probes the candidate matched a separate literal
unbounded-integer implementation of the prompt recurrence. See
[`02-precision-differential.log`](evidence/02-precision-differential.log) and
[`02-precision-differential.py`](evidence/02-precision-differential.py).

Judgment: this precision divergence prevents a universal
candidate-versus-canonical equivalence claim, but it does not show that the
candidate violates the natural-language integer contract. It instead exposes a
limitation of using the canonical's floating division as an oracle on unbounded
positive integers. This limitation is separate from the decisive proof-scope
failure below.

## 3. Clean proof reconstruction

The available toolchain is K `v7.1.293`; version evidence is in
[`00-toolchain.log`](evidence/00-toolchain.log).

Only `solution.py`, `solution.mpy`, `semantic.k`, `verification.k`, `spec.k`,
and `prove.sh` were copied to `/tmp/audit-work/candidate-src`. Fresh output
directories with audit-specific names were built from source:

```text
kompile semantic.k --main-module SEMANTIC --syntax-module MPY-SYNTAX \
  --backend llvm \
  --output-definition /tmp/audit-work/semantic-kompiled-audit

kompile verification.k --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX --backend haskell \
  --output-definition /tmp/audit-work/verification-kompiled-audit
```

Both builds exited 0. No candidate-provided compiled definition or cache was
referenced.

### Fresh concrete reconstruction

Fresh `krun` executions for inputs `1, 2, 3, 5, 27` all exited 0 with empty
`<k>`, empty final function/environment maps, and the exact result produced by
both Python implementations. These cases collectively exercise the
zero-iteration loop boundary, both parity branches, assignment, lookup,
arithmetic, list concatenation, return, and sorting. The full configurations
and Python oracle outputs are in
[`03-build-run-proof.log`](evidence/03-build-run-proof.log).

### Fresh proof reconstruction

The exact submitted `spec.k` was proved as a bundle:

```text
kprove spec.k \
  --definition /tmp/audit-work/verification-kompiled-audit \
  --spec-module SPEC --output pretty
#Top
EXIT: 0
```

This command includes every one of the 12 claims; any failed claim would make
the bundle non-`#Top`. The two labeled symbolic claims were additionally run
individually as `SPEC.even-step` and `SPEC.odd-step`; each printed `#Top` and
exited 0. Exact commands and output are in
[`03-build-run-proof.log`](evidence/03-build-run-proof.log), generated by
[`03-build-run-proof.sh`](evidence/03-build-run-proof.sh).

Therefore the candidate's mechanical `#Top` claim is reproducible. This stage
does not establish that the proved claims have adequate scope.

## 4. Adequacy and real-program pinning

### Entry claims in plain language

All eight entry claims have the same state-shaped precondition: the computation
is `run(solutionProgram)`, the indicated concrete input is present, the
function and environment maps are empty, and the result is `noResult`. There is
no additional `requires` clause. The postcondition consumes the whole
computation, leaves those exact framed cells as stated, and requires the exact
listed result:

| Input | Exact constrained return |
|---:|---|
| 1 | `[1]` |
| 2 | `[1]` |
| 3 | `[1, 3, 5]` |
| 5 | `[1, 5]` |
| 6 | `[1, 3, 5]` |
| 7 | `[1, 5, 7, 11, 13, 17]` |
| 19 | `[1, 5, 11, 13, 17, 19, 29]` |
| 27 | the exact 42-element list written at `spec.k:85` |

These are result-constraining claims, not free-result or tautological claims.
Each exact initial configuration is itself a satisfiable precondition witness.
Both trusted canonical Python and candidate Python produce the stated value for
all eight inputs; the substitutions are recorded in
[`04-adequacy-pinning.log`](evidence/04-adequacy-pinning.log).

### Helper claims in plain language

- `even-step` assumes `M > 0`, arbitrary list `OS`, and environment
  `n = 2*M`, `odds = OS`. One execution of the real branch statement must
  leave `odds` unchanged and set `n = M`. A witness is `M=1`, `OS=.Ints`.
- `odd-step` assumes `M > 0`, arbitrary `OS`, and
  `n = 2*M+1`. One execution of the branch must append the old odd value and
  set `n = 6*M+4`. A witness is `M=1`, `OS=.Ints`.
- The two observer claims are fully ground calculations: sorting one fixed
  odd list yields a sorted list, and one fixed all-odd list satisfies
  `allOdd`.

The parity claims match one real execution of the `if` body. They do not claim
or prove a loop invariant, preservation of a relationship to the original
trajectory, behavior after arbitrarily many iterations, or a returned result.
There is no helper claim about the `while` loop itself.

### Real-program pinning

The entry `<k>` cell uses a total definitional constant `solutionProgram`.
Recursively expanding `solutionProgram`, `collatzLoop`, and `collatzBranch`,
then normalizing explicit K list-unit syntax, produces the same 184-token AST
as the trusted-translator-generated `solution.mpy`. Both normalized token
streams have SHA-256
`119a22fcba8fa056680faa791b22857510b061164e384f64f1d6951f0cd08671`.
See [`04-adequacy-pinning.py`](evidence/04-adequacy-pinning.py) and its
[`log`](evidence/04-adequacy-pinning.log).

The aliases reduce to ordinary AST constructors before execution; no rule
replaces the program body with an answer. Thus the eight entry claims do pin
the real submitted program.

### Decisive adequacy failure

The intended domain is all positive integers, conditional on program
termination. The formal entry domain is only:

```text
{1, 2, 3, 5, 6, 7, 19, 27}
```

Input 9, for example, satisfies the natural contract's domain and the program
terminates with `[1, 5, 7, 9, 11, 13, 17]`, but no entry claim applies to it.
The one-step parity claims do not imply this result or any general result.
Likewise, the ground observer claims are not connected to any returned value.

Avoiding a universal termination theorem is appropriate, but it does not
justify omitting a universal partial-correctness theorem. The candidate needed
an invariant relating `n`, `odds`, the original input, and the consumed
trajectory, together with a terminal claim about `sort(odds+[1])`. It contains
none. The proof therefore stops at examples and local transition tests.

Stage 4 fails.

## 5. Rule-by-rule static soundness review

The numbered complete sources and machine-extracted inventory are preserved in
[`05-static-inventory.log`](evidence/05-static-inventory.log). Local counts are:

- `semantic.k`: 18 `syntax` declaration lines and 44 rules;
- `verification.k`: 6 `syntax` declaration lines and 10 rules;
- `spec.k`: 12 claims;
- 5 semantic `[function]` declarations, of which 3 are `[total]`;
- 5 verification `[function, total]` declarations; and
- no local simplification, priority/priorities, opaque, or explicit
  `[functional]` declaration.

### Syntax and configuration inventory

`MPY-SYNTAX` declares:

- `Pgm`: `Module`;
- list sorts `Stmts`, `Exprs`, `Ids`, and `CmpOps`;
- statements `FuncDef/Params`, `Assign`, `If`, `While`, and `Return`;
- expressions `Int`, `Name`, `ListExpr`, `BinOp`, `Compare`, and `Call`; and
- comparison item `CmpOp`.

`SEMANTIC` declares:

- integer lists `.Ints` and `Int :: Ints`;
- runtime values `vi`, `vb`, and `vl`;
- function and result values;
- continuations `run`, `load`, `start`, `exec`, `eval`, `assignTo`,
  `singleton`, `binLeft`, `binRight`, `cmpLeft`, `cmpRight`,
  `whileDecide`, `ifDecide`, `sortResult`, and `finish`; and
- a configuration with `<k>`, `<input>`, `<functions>`, `<env>`, and
  `<result>` cells.

`VERIFICATION` adds the AST constants `collatzBranch`, `collatzLoop`, and
`solutionProgram`; observers `isSorted` and `allOdd`; and operational wrappers
`checkSorted` and `checkAllOdd`.

This is a sufficient syntax/configuration inventory for the submitted program.
It deliberately does not model general Python. Missing behavior for unused
multi-argument calls, multi-element literal syntax, exceptions, heap objects,
or arbitrary function calls is not a defect in generated-semantics mode.

### Mapping every submitted construct

| Submitted construct | Declaration and execution rules |
|---|---|
| `Module`, one `FuncDef`, one `Params` | `Pgm`/`Stmt`; `run`, `load(FuncDef)`, `load(.Stmts)`, `start` |
| `Assign(Name(...), ...)` | `Assign`; `exec(Assign)`, `assignTo` map update |
| `While` | `exec(While)`, true and false `whileDecide` rules |
| `If` | `exec(If)`, true and false `ifDecide` rules |
| `Return` | `exec(Return)`, `finish` |
| `Int`, `Name` | literal and environment-lookup rules |
| empty and singleton `ListExpr` | two list-expression rules plus `singleton` |
| `BinOp` | left-to-right continuation rules plus `applyBin` |
| `+`, `*`, `%`, `//` | five typed `applyBin` equations, including list `+` |
| `Compare`, `==`, `!=` | left-to-right comparison rules plus four guarded `applyCmp` equations |
| `Call(Name("sorted"), one_arg)` | exact call rule, `sortResult`, recursive insertion sort |

### The 44 semantic rules

Every rule was reviewed individually; the following grouping enumerates all of
them without collapsing different equations:

| Rules | Review decision |
|---|---|
| `run(Module)`; `load(FuncDef)`; `load(.Stmts)`; `start` | Sound for the one-function submitted module. Loading preserves the body and binding; `start` selects the actual `get_odd_collatz` definition and binds its actual parameter to `<input>`. |
| `exec(Assign)`; `Value ~> assignTo` | Sound left-to-right RHS evaluation and immutable map update. |
| `exec(If)`; `vb(true) ~> ifDecide`; `vb(false) ~> ifDecide` | Sound and disjoint Boolean branch selection; the chosen body runs before the real remaining statements. |
| `exec(While)`; true `whileDecide`; false `whileDecide` | Sound test-before-body control flow. The true rule reconstructs the same loop after the body; the false rule continues with the real suffix. |
| `exec(Return)`; `Value ~> finish`; `exec(.Stmts)` | Sound on the target's top-level return. `finish` records the exact value and clears local runtime maps. It is intentionally narrow and would visibly stick for unsupported nested-return contexts rather than fabricate a value. |
| `eval(Int)`; `eval(Name)`; empty `ListExpr`; singleton `ListExpr`; `vi ~> singleton` | Sound for the target literals and environment lookups. Only the empty/singleton literal arities used by the submitted AST are covered. |
| `eval(BinOp)`; `binLeft`; `binRight` | Sound left-to-right operand evaluation with both values passed unchanged to `applyBin`. |
| `eval(Compare)`; `cmpLeft`; `cmpRight` | Sound left-to-right evaluation for the target's single comparison operator. |
| exact `sorted` call; `vl ~> sortResult` | Sound binding for this target because it never rebinds `sorted`; the argument is evaluated once and passed to the explicit sort. This is a narrow built-in boundary, not an oracle. |
| integer `+`; integer `*`; guarded `%`; guarded `//`; list `+` | Sound on every reachable intended state. The target only takes `%` and `//` with divisor 2 and nonnegative integer dividend. The declarations are partial, not falsely marked total. Behavior for negative/general operands is outside the used subset and is not claimed unsound. |
| `==` true; `==` false; `!=` true; `!=` false | Pairwise guards are disjoint and exhaustive for integer arguments; results are ordinary equality/inequality. |
| `appendInts` empty; `appendInts` cons | Total, structurally descending, nonoverlapping, and equal to immutable list concatenation. |
| `insertInt` empty; `insertInt` `I<=J`; `insertInt` `I>J` | Total over integer lists. Guards are disjoint/exhaustive and recursion descends. |
| `sortInts` empty; `sortInts` cons | Total structural insertion sort. Recursion descends and preserves exactly the input multiset. |

There is no allocation or heap behavior to omit: `solution.py` only rebinds
local integer/list values, which the environment and immutable `Ints` represent
adequately. There is no output, exception, or external state in the submitted
program. K `Int` gives the submitted solution's exact integer arithmetic.

### The 10 verification rules

| Rules | Review decision |
|---|---|
| `collatzBranch`; `collatzLoop`; `solutionProgram` | Total zero-argument definitional summaries. Recursive expansion is exactly the submitted translated AST; they name syntax and do not replace execution. |
| `isSorted(.Ints)`; singleton `isSorted`; recursive `isSorted` | Total, nonoverlapping structural definition of nondecreasing order. |
| `allOdd(.Ints)`; recursive `allOdd` | Total structural conjunction. It matches mathematical oddness for the positive values reachable here. Its behavior on negative lists is not evidence about this positive-input program. |
| `checkSorted`; `checkAllOdd` | Truthful operational wrappers around the named functions. They do not affect or help close the eight entry executions. `checkSorted` sorts before observing, so its ground claim does not establish that a program return is sorted. |

All five `[total]` declarations have complete pattern coverage on their
declared sorts. All recursive equations descend. No overlapping right-hand
sides disagree. There are no local priorities, simplification axioms, opaque
symbols, fresh values, or proof rules that encode a Collatz answer.

I do not label any inventoried rule unsound. Consequently no false-conclusion
witness is asserted for a rule. The limitations identified above are narrower
coverage or missing theorem connections; they do not make a false conclusion
provable on the intended positive-input domain.

Static soundness passes for the narrow generated semantics and proof helpers.
It does not repair Stage 4's missing theorem.

## 6. Fresh non-vacuity test

No candidate `spec-vacuity.k` was present. I created a fresh scratch mutation
that keeps the exact satisfiable input-5 start state but changes the required
return from `[1, 5]` to the false `[1, 7]`.

The mutation's dry run built successfully and exited 0. Its actual proof then
reached the terminal configuration with `[1, 5]`, printed
`WarnStuckClaimState`, and exited 1:

```text
<result>
  result ( vl ( 1 :: 5 :: .Ints ) )
</result>
[Error] Prover: backend terminated because the configuration cannot be
rewritten further.
EXIT: 1
```

This is the expected unmet result obligation, not a parser error, missing
import, timeout, or unrelated crash. The mutation is
[`spec-vacuity-audit.k`](evidence/spec-vacuity-audit.k); exact build/proof
commands and output are in
[`06-nonvacuity.log`](evidence/06-nonvacuity.log).

The concrete entry proof is therefore non-vacuous and result-sensitive. This
test says nothing about the absent universal theorem.

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Under the candidate's generated K semantics:

1. the exact submitted program terminates with the exact stated list for inputs
   `1, 2, 3, 5, 6, 7, 19, 27`;
2. one execution of its parity branch correctly updates arbitrary positive
   even and odd current values as stated by `even-step` and `odd-step`; and
3. two fixed observer computations reduce to `true`.

It does **not** establish:

- any entry result for an arbitrary positive input;
- that accumulated `odds` equals all odd terms of an arbitrary original
  trajectory;
- preservation of such a relationship through the loop;
- that an arbitrary returned list is sorted or all-odd;
- equivalence with `canonical.py` over unbounded Python integers; or
- the Collatz conjecture.

### Trust and assumption ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K prover/backend and standard `INT`, `BOOL`, `MAP` semantics | All builds, runs, and proofs | Ordinary low-level machine-checking trust boundary. K version and exact commands are recorded. |
| Trusted `py2mpy.py` translation | Identity of `solution.mpy` | Acceptable: translator is mounted trusted, candidate copy matches it, and regeneration is byte-identical. |
| `solutionProgram`/`collatzLoop`/`collatzBranch` constants | All K entry/helper claims | Acceptable definitional summaries: recursive normalized AST identity was checked. No computation is skipped. |
| Generated operational semantics | Meaning of every K claim | Audited rule-by-rule above. It is intentionally a minimal language, but it covers every used construct without an answer oracle. |
| K arbitrary-precision integer primitives | Arithmetic and guards | Acceptable for `solution.py` and the mathematical prompt. It differs from the trusted canonical after that code introduces binary64 floats. |
| `sortInts` insertion-sort equations | Returned order in concrete entries | Standard total structural definition, reviewed informally and executed by K. No separate universal correctness lemma connects it to all Python `sorted` behavior; only integer lists are in scope. |
| Exact `sorted` binding in the call rule | Target's only call | Acceptable for this program because no rebinding occurs. It would be too broad as general Python semantics, but unsupported general Python is outside generated-semantics scope. |
| Differential tests | Program/intent bridge on tested inputs | Finite evidence only: 1,250 ordinary inputs match; precision probes expose the canonical float limitation. Tests do not substitute for a K theorem. |
| Informal Collatz-list invariant | Intended universal property | Missing, not trusted. No claim states it and no K proof establishes it. This is the decisive illegitimate gap. |

There are no opaque symbols or program-derived oracle values to account for.
The candidate's generated traces, cached definitions, `#Top`, and finite tests
were not used as substitutes for the K proof or its adequacy review.

### Decision

Clean reconstruction, real-program identity, local semantic soundness, and a
meaningful concrete non-vacuity mutation all pass. The claimed theorem's scope
does not: a finite set of executions plus one-step branch facts is not a
partial-correctness proof for every positive input. This falls directly under
the decision boundary for a missing/materially inadequate proof.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
