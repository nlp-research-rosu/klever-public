# Independent adversarial audit: 76-is-simple-power

## Outcome

The candidate contains a freshly reproducible, non-vacuous K reachability proof of the behavior of the actual submitted `solution.mpy` under its generated semantics. I found no execution-bypassing rule, result oracle, false semantic rule, free final result, or substituted program.

The outcome is nevertheless **CONCERNS / LEGIT**, not an unqualified pass, because the bridge from the proved local predicate to the prompt's unrestricted wording is narrower than stated. The candidate defines every nontrivial power with `n < 2` as false. The prompt supplies no positive-base precondition, and the concrete witnesses `(4,-2)`, `(9,-3)`, `(16,-2)`, and `(81,-3)` are powers in the ordinary nonnegative-exponent sense and return `true` in the trusted canonical implementation, but the submission returns `false`. This is an intent/domain limitation, not a soundness defect in the K execution proof: the K theorem accurately constrains the submitted program to its locally defined `simplePowerSpec`.

All candidate prose, traces, prior build products, and reported `#Top` results were treated only as untrusted claims.

## 1. Input and provenance integrity

The `GENERATED_SEMANTICS` mount boundary is consistent: `/reference/reference-semantics` is absent. No hidden or inferred reference semantics was used. See [01-provenance.log](evidence/logs/01-provenance.log).

The following required candidate artifacts exist as regular, non-symlink files: `run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`, `prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`, `semantic.k`, `verification.k`, `spec.k`, and `prove.sh`. The structured trace is one regular JSONL file with 287 valid JSON records; its bounded structural reading is in [02-trace-summary.log](evidence/logs/02-trace-summary.log). No symlink was found anywhere below `/candidate`.

The candidate prompt and translator are byte-identical to the trusted inputs:

| Artifact | SHA-256 | Result |
|---|---|---|
| candidate and trusted `prompt.py` | `4d99f80a460939bc03631f3a652d9af5d5a09da2fd8fab20205c9682f766a361` | identical |
| candidate and trusted `py2mpy.py` | `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16` | identical |

The untrusted records claim a bare/generated-semantics run, exit 0, six successful examples, and a successful `kprove`. Those claims were read but not relied upon. There is no candidate `PROOF.md`. That file was not a required generation deliverable, so its absence is not an integrity failure.

The candidate also contains several compiled definitions, caches, a Python bytecode cache, and `kore-exec.tar.gz`. These are extra untrusted build evidence, not source-integrity failures. None was copied or reused. The audit scratch tree contains only reviewer-copied source plus definitions whose names begin with `fresh-`; see [00-toolchain-and-isolation.log](evidence/logs/00-toolchain-and-isolation.log).

No required artifact was missing, changed, mistyped, or symlinked.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract restatement

The trusted prompt asks for `is_simple_power(x, n)` to return true exactly when `x = n**e` for an integer exponent, with examples showing that exponent zero is accepted (`1 = 4**0`). The trusted canonical implementation operationalizes this, for its normally terminating positive-base domain, by starting at `1` and repeatedly multiplying by `n` until reaching or passing `x`.

The submitted program:

1. returns true for `x == 1`;
2. returns false for `x < 1`;
3. returns false for every `n < 2`;
4. otherwise starts at `power = n`, repeatedly multiplies by `n` while `power < x`, and returns whether the final power equals `x`.

For integer `x` and positive integer `n`, this is a different but equivalent algorithm to the trusted canonical implementation. For negative bases it is not equivalent.

### Translator fidelity

The trusted translator was executed from `/tmp/audit-work/reference` against the scratch copy of `solution.py`. The regenerated file is byte-identical to the submitted `solution.mpy`, with shared SHA-256 `94eb9a3860bd9ccff041c57b307fda0db8e2bfbff67c3f508d2d9c09a343a5ed`. Exact command, `cmp` status, and hashes are in [03-translator-regeneration.log](evidence/logs/03-translator-regeneration.log); the regenerated artifact is [solution.regenerated.mpy](evidence/artifacts/solution.regenerated.mpy).

### Independent differential test

The reviewer-authored [differential_test.py](evidence/differential_test.py) independently imports `/reference/canonical.py` and the scratch copy of generated `solution.py`. It also uses a division-based mathematical oracle that does not reuse the candidate's multiplication loop.

The test covers:

- all six documented examples;
- `x` boundaries below, at, and above 1;
- `n` boundaries at 1 and 2;
- loop zero-iteration, one-iteration, true-power, and overshoot cases;
- every pair `x ∈ [-20,500]`, `n ∈ [1,12]`;
- 2,000 deterministic generated pairs with `x ∈ [-100,100000]`, `n ∈ [1,20]`.

There were zero mismatches across 8,241 unique positive-base cases. The exact scope and result are in [04-python-differential.log](evidence/logs/04-python-differential.log).

The same test preserves a material boundary discrepancy:

| `(x,n)` | Trusted canonical | Submitted program | Ordinary `n**e`, `e ≥ 0` |
|---|---:|---:|---:|
| `(4,-2)` | true | false | true |
| `(9,-3)` | true | false | true |
| `(16,-2)` | true | false | true |
| `(81,-3)` | true | false | true |

The prompt does not state `n ≥ 1`, while the generated K configuration quantifies over all integers. Therefore the positive-base restriction must be documented rather than silently treated as part of the prompt. This is the main reason for `CONCERNS`.

## 3. Clean proof reconstruction

K v7.1.293 from `/usr/bin` was used. Candidate-built definitions and caches were ignored.

Fresh builds from the scratch source both exited 0:

| Definition | Exact command | Evidence |
|---|---|---|
| Concrete generated semantics | `kompile semantic.k --backend haskell --main-module SEMANTIC --syntax-module MPY-SYNTAX --output-definition fresh-semantic-kompiled` | [05-build-concrete-semantics.log](evidence/logs/05-build-concrete-semantics.log) |
| Proof definition | `kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition fresh-verification-kompiled` | [06-build-proof-definition.log](evidence/logs/06-build-proof-definition.log) |

The submitted `solution.mpy` was concretely executed with the fresh generated semantics on 15 normal and boundary inputs. Every `krun` exited 0 and agreed with independent execution of generated `solution.py`; mismatch count was zero. Cases include all branches, true and false loop outcomes, exact powers, overshoots, `x ≤ 1`, `n = 1`, and negative `n`. The script and complete result table are [concrete_semantics_compare.py](evidence/concrete_semantics_compare.py) and [07-concrete-semantics-compare.log](evidence/logs/07-concrete-semantics-compare.log).

The combined positive proof command exited 0 and printed `#Top`:

`kprove spec.k --definition fresh-verification-kompiled --spec-module SPEC`

See [08-kprove-all-claims.log](evidence/logs/08-kprove-all-claims.log). The warning that the emitted-tree identity claim is trivial is expected: that claim is an exact definitional expansion.

Each of the six positive claims was then selected and run independently. Every command exited 0 and printed `#Top`:

| Claim | Evidence |
|---|---|
| `SPEC.emitted-tree-is-shared-tree` | [09-kprove-emitted-tree.log](evidence/logs/09-kprove-emitted-tree.log) |
| `SPEC.returns-on-one` | [10-kprove-returns-on-one.log](evidence/logs/10-kprove-returns-on-one.log) |
| `SPEC.rejects-below-one` | [11-kprove-rejects-below-one.log](evidence/logs/11-kprove-rejects-below-one.log) |
| `SPEC.rejects-small-base` | [12-kprove-rejects-small-base.log](evidence/logs/12-kprove-rejects-small-base.log) |
| `SPEC.active-path-enters-loop` | [13-kprove-active-path.log](evidence/logs/13-kprove-active-path.log) |
| `SPEC.loop-correct` | [14-kprove-loop-correct.log](evidence/logs/14-kprove-loop-correct.log) |

Thus the candidate's prior build report was independently reconstructed.

## 4. Adequacy and real-program pinning

### Plain-language claim inventory

| Claim | Starting-state requirement | Proven destination |
|---|---|---|
| `emitted-tree-is-shared-tree` | The literal constructor tree, empty environment, `noResult`; arbitrary integer input cells | The same configuration with the tree replaced by `solutionProgram` |
| `returns-on-one` | `x = 1`; arbitrary integer `n` | Program terminates, environment contains `x=1,n=N`, and result is `simplePowerSpec(1,N)` |
| `rejects-below-one` | `X < 1`; arbitrary integer `N` | Program terminates and returns `simplePowerSpec(X,N)` |
| `rejects-small-base` | `1 < X` and `N < 2` | Program terminates and returns `simplePowerSpec(X,N)` |
| `active-path-enters-loop` | `1 < X` and `2 ≤ N` | The exact program prefix runs to the real loop head, with `power=N`, unchanged `noResult`, and the exact final return as continuation |
| `loop-correct` | At that exact loop/return continuation, `1 < X`, `2 ≤ N`, and `P > 0` | Loop and return terminate; final `power` is `powerCeiling(P,X,N)` and the Boolean result is exactly whether that value equals `X` |

Every precondition is satisfiable. Concrete witnesses are respectively `(x,n)=(2,2)`, `(1,4)`, `(0,2)`, `(3,1)`, `(8,2)`, and loop state `(X,N,P)=(8,2,2)`. A second loop witness `(5,3,3)` exercises the false result. Ground substitutions, formal postconditions, and both Python results are recorded in [17-claim-witnesses.log](evidence/logs/17-claim-witnesses.log).

### Actual-program identity

The proof does not load a different implementation:

1. trusted translation reproduced the submitted `solution.mpy` byte for byte;
2. `solutionProgram` expands to the exact constructor tree in that file;
3. `emitted-tree-is-shared-tree` independently closes;
4. the concrete runs parse and execute the actual scratch copy of submitted `solution.mpy`;
5. the `active-path-enters-loop` target contains the exact submitted multiplication body and exact return continuation.

The complete line-numbered sources are in [18-source-listing.log](evidence/logs/18-source-listing.log).

### Result constraint and composition

The early-return claims rewrite `noResult` to a concrete Boolean-valued specification term. The loop claim rewrites it to the exact equality `powerCeiling(P,X,N) ==Int X`. No right-only existential or free result variable appears.

The active positive-base theorem is split across two submitted claims rather than stated as one entry claim. Their composition is sound:

- `active-path-enters-loop` reaches exactly the source of `loop-correct`;
- at that point `P=N`, and the active-path guard `N≥2` supplies `P>0`;
- under `X>1,N≥2`, `simplePowerSpec(X,N)` reduces to `powerCeiling(N,X,N) ==Int X`.

Ordinary transitivity of reachability therefore yields the full entry result. A reviewer-authored one-piece version parsed successfully but did not complete within a deliberately bounded 15-second diagnostic run; see [21-composed-entry-dry-run.log](evidence/logs/21-composed-entry-dry-run.log) and [22-composed-entry-proof.log](evidence/logs/22-composed-entry-proof.log). Per the audit rules, that bounded timeout is not treated as a candidate failure or as proof evidence. The submitted two-lemma proof and the explicit syntactic/guard match are the basis for the composition accounting.

The negative-base witness `(4,-2)` satisfies `rejects-small-base`: the formal result and generated program are both false, while trusted canonical Python returns true. This confirms that the K proof constrains the real program, but also confirms the natural-language domain concern rather than resolving it.

## 5. Rule-by-rule static soundness review

### Local declarations and construct coverage

`semantic.k` declares:

- `Program`: `Module(Stmts)`;
- `Stmts`: an unseparated list of `Stmt`;
- `Ids`: a comma-separated list of strings;
- `Stmt`: `FuncDef`, `If`, `While`, `Assign`, and `Return`;
- `Exp`: `Int`, `Bool`, `Name`, `BinOp`, and `Compare`;
- `CmpOp`: `CmpOp(String,Exp)`;
- `Value`: the `Int` and `Bool` subsorts;
- `Result`: `noResult` or a `Value`;
- internal `KItem`s: `exec`, `eval`, `choose`, `loop`, `assignTo`, `returnValue`, `binRight`, `binApply`, `cmpRight`, and `cmpApply`.

Its configuration contains only `<k>`, `<env>`, `<result>`, `<x>`, and `<n>`. This is sufficient for the submitted first-order entry function: there is no call syntax, heap object, exception form, I/O, or allocation beyond adding/updating an environment key.

Every constructor used by `solution.mpy` is mapped:

| Used syntax | Declaration | Operational rules |
|---|---|---|
| `Module`, `FuncDef`, `Params` | `semantic.k` lines 6, 9, 11 | entry rule lines 55–59 |
| statement list and empty list | lines 8, 11–15 | lines 61–62 |
| `If` | line 12 | lines 64–66 |
| `While` | line 13 | lines 68–70 |
| `Assign` | line 14 | lines 72–74 |
| `Return` | line 15 | lines 76–78 |
| `Int`, `Bool`, `Name` | lines 17–19 | lines 80–83 |
| `BinOp("*",...)` | line 20 | lines 85–90 |
| `Compare` with `==` and `<` | lines 21, 23 | lines 92–99 |

The generic string slots admit unused operators or names, but unsupported cases stop visibly because no application rule exists. Minimal generated-semantics coverage is therefore used rather than fabricated fallback behavior.

### All 23 ordinary semantic rules

| Rule | Static decision |
|---|---|
| 55–59, exact entry | Sound for the submitted entry: it accepts only the exact function name and parameters, initializes a two-binding environment from the integer input cells, and schedules the real body. |
| 61, empty `exec` | Soundly consumes an empty statement list while preserving its continuation. |
| 62, nonempty `exec` | Soundly schedules the head statement before the remaining statements. The empty/nonempty cases are disjoint. |
| 64, `If` scheduling | Soundly evaluates the guard before either branch. |
| 65, true `choose` | Selects exactly the then-list. |
| 66, false `choose` | Selects exactly the else-list. The Boolean branch rules are disjoint and complete for used guards. |
| 68, `While` scheduling | Re-evaluates the guard at every loop head. |
| 69, true `loop` | Executes the body before returning to the same loop. This creates the stable recurring configuration used by the invariant. |
| 70, false `loop` | Exits the loop and preserves the following continuation. |
| 72, assignment scheduling | Evaluates the right-hand expression before storing. |
| 73–74, assignment update | Updates or inserts the named map binding and preserves all other bindings/cells. This correctly allocates the local `power` binding. |
| 76, return scheduling | Evaluates the return expression before control transfer. |
| 77–78, return effect | Clears the remaining statement continuation and changes `noResult` to the returned value. In this generated language there are no call frames, `finally` blocks, exceptions, or other cleanup effects that this could incorrectly discard. |
| 80, integer literal | Returns the exact unbounded K integer. |
| 81, Boolean literal | Returns the exact K Boolean. |
| 82–83, name lookup | Reads the unique map binding without state change. Every used name is initialized before lookup. |
| 85–86, binary-left scheduling | Evaluates the left operand first. |
| 87–88, binary-right scheduling | Evaluates the right operand after the left and retains the left value. |
| 89–90, multiplication | Applies exact unbounded integer multiplication. It is the only used binary operator. |
| 92–93, comparison-left scheduling | Evaluates the left comparison operand first. |
| 94–95, comparison-right scheduling | Evaluates the right operand second and retains the left value. |
| 96–97, integer equality | Implements the submitted `==` comparisons exactly on integer operands. |
| 98–99, integer less-than | Implements the submitted `<` comparisons exactly on integer operands. The operator strings are disjoint from equality. |

There are no local priority rules, simplification rules, opaque symbols, `[functional]` declarations, exceptions, nondeterministic rules, or overlapping right-hand sides. State footprints are explicit: only entry initialization and assignment change `<env>`, and only return changes `<result>`; `<x>` and `<n>` are immutable mirrors of the inputs.

### Verification-local declarations and all four equations

`verification.k` contains three `[function,total]` declarations and four equations:

| Extension | Class and decision |
|---|---|
| `solutionProgram` and its one equation, lines 8–24 | Definitional abbreviation. It does not replace execution; it expands to the exact submitted tree. Its single constant case is truthful and total. |
| `powerCeiling` recursive equation, lines 28–30 | Definitional mathematical summary, not an operational bridge. Under every proof-dependent use (`P>0,N≥2`), multiplying by `N` strictly increases positive `P` until the threshold and the equation matches one loop iteration exactly. |
| `powerCeiling` base equation, lines 31–32 | Truthful and disjoint from the recursive guard. Together `P<X` and `X≤P` cover integer `P,X`. |
| `simplePowerSpec` equation, lines 36–41 | Total local definition of the claimed Boolean contract. It does not rewrite program execution or supply an oracle value to a branch. It matches ordinary nonnegative powers on the audited positive-base domain, but its `2≤N` restriction is not supplied by the prompt and creates the documented negative-base intent discrepancy. |

The global `[total]` annotation on `powerCeiling` is broader than its justified terminating evaluator domain. For example, `powerCeiling(1,2,1)` rewrites to itself, so recursive descent is not established over the full declared integer signature. This is a real declaration-quality concern. It does not furnish a false equality or affect any proof use, all of which require `P>0,N≥2`; accordingly I record the narrow totality/termination gap rather than label the equation unsound. No false-conclusion witness exists from that self-rewrite alone.

The `simplePowerSpec` equation is not a sound formalization of unrestricted-base ordinary exponentiation: `simplePowerSpec(4,-2)` reduces to false although `(-2)**2=4` and trusted canonical Python returns true. This is an intent-definition counterexample, not an unsound operational rule: the fresh symbol is explicitly defined to mean the narrower predicate and the generated program truly returns that value.

### Claim and loop-invariant soundness

The four entry-path guards partition all integer pairs: `X=1`; `X<1`; `X>1,N<2`; and `X>1,N≥2`. The actual control flow reaches the corresponding claims.

For `loop-correct`:

- if `P≥X`, the false loop guard immediately reaches the return; both the final environment and result match the `powerCeiling` base equation;
- if `P<X`, the exact submitted body writes `P*N`, returns to the identical loop/return continuation, and preserves all other cells;
- `P>0,N≥2` preserves positivity and makes the recursive `powerCeiling(P,X,N) = powerCeiling(P*N,X,N)` equation align with that one iteration.

Thus the circularity summarizes actual repeated execution and is not a result-bearing oracle. A separate body-sensitivity artifact changes the supported multiplier from `n` to `3` for `(8,2)`. It parses successfully, then K executes to `power=18,result=false` and rejects the original loop target; see [spec-body-sensitivity.k](evidence/artifacts/spec-body-sensitivity.k), [19-body-sensitivity-dry-run.log](evidence/logs/19-body-sensitivity-dry-run.log), and [20-body-sensitivity-expected-failure.log](evidence/logs/20-body-sensitivity-expected-failure.log).

No semantic or proof rule is labeled materially unsound, so there is no missing false-conclusion witness for an unsoundness accusation. The concrete negative-base example is instead attached to the narrower intent-definition finding above.

## 6. Fresh non-vacuity test

The reviewer-authored [spec-vacuity.k](evidence/artifacts/spec-vacuity.k) changes a result-bearing obligation: for the satisfiable input family `x=1` (concretely `n=4`), it falsely requires the final result to be `false`.

The mutation was copied to scratch and checked in two steps:

1. `kprove ... --dry-run` exited 0, confirming successful parsing/building; see [15-vacuity-dry-run.log](evidence/logs/15-vacuity-dry-run.log).
2. The actual proof exited 1 with `WarnStuckClaimState`. Its residual is the fully terminated real configuration with `<result>true</result>`, which cannot unify with the false destination; see [16-vacuity-proof-expected-failure.log](evidence/logs/16-vacuity-proof-expected-failure.log).

This is the expected unmet result obligation, not a parser error, missing import, timeout, unreachable mutation, or unrelated crash. The proof is non-vacuous and result-discriminating.

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Under the generated K semantics and integer input cells:

- the actual submitted constructor tree initializes and executes its real body;
- `x=1` returns true through the locally defined specification;
- `x<1` returns false;
- `x>1,n<2` returns false;
- `x>1,n≥2` reaches the exact multiplication loop, whose exact execution leaves `power=powerCeiling(n,x,n)` and returns whether that value equals `x`;
- the environment and result changes shown in the claims are constrained, with no free observable output.

By the explicit transitive composition in Stage 4, this characterizes the submitted program as returning `simplePowerSpec(X,N)` for all integer inputs in its generated execution model. It is a partial-correctness result; it does not claim CPython resource bounds or behavior for non-integer arguments.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K reachability logic, Haskell backend, parser, and fresh `#Top` results | All formal closure | Standard unavoidable toolchain trust; version and exact commands recorded. |
| Built-in K `Int`, `Bool`, `Map`, strings, and list machinery | Arithmetic, comparisons, environment, parsing | Acceptable low-level language primitives; none encodes the task answer. |
| Trusted `py2mpy.py` and its execution | Python-to-constructor identity | Trusted by the audit instructions; byte regeneration independently pins the submitted MPY artifact. |
| Reviewer validation of generated semantics against the used Python subset | Bridge from K execution to generated Python | Rules are small and exhaustively audited; 15 concrete boundary executions provide finite support. This is not a universal CPython theorem, but all used constructs are directly modeled and no opaque result-bearing primitive exists. |
| `powerCeiling` as a mathematical summary | Loop postcondition and final positive-base result | Connected to exact loop execution by the machine-checked `loop-correct` reachability claim. Acceptable on `P>0,N≥2`; its global `[total]` descent claim is over-broad outside that domain. |
| Ordinary transitivity connecting the submitted prefix and loop claims | Full active-path entry result | Exact intermediate configurations and guards match. The separate bounded one-piece automation attempt is not counted as proof. |
| `simplePowerSpec` meaning “simple power” | Bridge to the human contract | Empirically and mathematically supported for positive integer bases; not proved as an exponentiation theorem and concretely wrong for the prompt's unrestricted negative-base reading. This is the material concern. |
| Trusted canonical implementation and differential tests | Program-to-reference evidence | 8,241 positive-base cases give finite bridge evidence only. They do not replace the K proof. Negative-base counterexamples remain visible. |

There are no opaque symbols, unconstrained result-bearing abstractions, external calls, empirical operational shortcuts, or proof rules that replace a program-defined computation.

### Decision

- Real-program soundness: **passes**. Fresh proof reconstruction, exact source pinning, complete used-rule audit, body sensitivity, and the false-result mutation all support it.
- Intent adequacy: **limited**. The theorem faithfully proves the submitted program's narrower predicate, but the prompt supplies no `n≥1` precondition and concrete negative-base powers disagree with both the ordinary reading and trusted canonical implementation.
- Evidence auditability: **passes with the stated finite-testing boundary**. Scripts, inputs, commands, statuses, and bounded outputs are preserved below `evidence/`.

The intent limitation prevents `PASS`, but it does not make the reconstructed execution proof unsound, vacuous, non-constraining, or substituted. Therefore the proof remains legitimate with concerns.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
