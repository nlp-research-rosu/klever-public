# Independent adversarial audit: 127-intersection

The candidate program is extensionally correct on the tested intended domain, and every submitted positive claim reconstructs to `#Top`. Nevertheless, the proof is not legitimate. Its whole-program definition imports a proof-local operational bridge that falsely preserves the `divisor` binding. A bridge-free theorem establishes only an existential final divisor, but the candidate turns it into a rule that leaves the initial divisor unchanged. On the valid input `(0,5),(0,5)`, fixed semantics finishes with `divisor = 3`; the bridge-enabled theory proves the false conclusion that it remains `2`.

All execution used fresh source copies under `/tmp/audit-work/127-intersection/run`. Candidate-provided compiled definitions, caches, logs, and traces were not reused. Reviewer artifacts and bounded logs are in `/audit-output/evidence/`. The live toolchain was K `v7.1.293` and Python `3.10.12` (`evidence/toolchain.log`).

## 1. Input and provenance integrity

The rendered mode and trusted mounts are consistent:

- This is `GENERATED_SEMANTICS`.
- `/reference/reference-semantics` does not exist.
- `/reference/canonical.py`, `/reference/prompt.py`, and `/reference/py2mpy.py` are regular files.
- The candidate prompt is byte-identical to `/reference/prompt.py`, with SHA-256 `aaebd5df799992f92d5d1e023101fa08b8a199d71be54536511e5ed071d5db1c`.
- The candidate translator is byte-identical to `/reference/py2mpy.py`, with SHA-256 `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.

The required generation/provenance artifacts `run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`, and the structured JSONL trace are present as regular, non-symlinked files. The required source deliverables `solution.py`, `solution.mpy`, `semantic.k`, `verification.k`, `spec.k`, and `prove.sh` are also present as regular files. No required artifact is missing, changed relative to a trusted counterpart, mistyped, or symlinked. The candidate includes additional derived artifacts—three `*-kompiled` trees, `__pycache__`, logs, and `kore-exec.tar.gz`. They were treated as untrusted extras and ignored, not as source integrity failures. A candidate `PROOF.md` and `spec-vacuity.k` are absent, but neither was a required deliverable of the bare generation prompt.

The untrusted provenance claims generation exit 0, two `#Top` lines, and 23,409 Python comparisons. Those claims were read but not relied upon. See `evidence/stage1-integrity.log` and `evidence/stage1-provenance-claims.log`.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

For two closed integer-endpoint intervals `(A,B)` and `(C,D)`, with `A <= B` and `C <= D`, let

`L = min(B,D) - max(A,C)`.

Return `"YES"` exactly when `L` is prime; otherwise return `"NO"`. In particular, disjoint or merely touching intervals return `"NO"`. The prompt and canonical implementation use geometric endpoint difference, not the number of contained integer points.

### Source inspection and translation

`solution.py` computes the maximum start and minimum end, returns `"NO"` for lengths below 2, then performs trial division from 2 through the square-root boundary. It preserves the required `intersection(interval1, interval2)` signature and stays in the trusted translator's subset.

Running the trusted copied translator on the copied `solution.py` produced a byte-identical `solution.mpy`. Both files have SHA-256 `50e2785172fe16e32b01bf02041d6aa4672707b205cafd12b2bc30c201f3627e`; both generation and `cmp` exited 0 (`evidence/stage2-regeneration.log`).

### Independent differential test

`evidence/differential_test.py` separately imports the trusted canonical entry point and copied candidate entry point. It covers:

- all three documented examples;
- disjoint and singleton/zero-length cases;
- equality and strict boundaries for both start-selection and end-selection branches;
- lengths 1, 2, 3, 4, 5, 6, 9, 97, and 121;
- a large-integer boundary;
- all 8,281 ordered pairs of valid intervals with endpoints in `[-6,6]`;
- 2,000 deterministic generated valid interval pairs with endpoints in `[-10000,10000]`.

All 10,302 comparisons matched. The exact inputs, command, output, and exit 0 are in `evidence/stage2-differential.log`.

## 3. Clean proof reconstruction

No candidate-built definition was copied. The following fresh builds and runs were made from `semantic.k`, `verification.k`, and `spec.k`:

1. Concrete LLVM definition:

   `kompile semantic.k --main-module MPY --syntax-module MPY-SYNTAX --backend llvm --output-definition semantic-fresh-kompiled`

   Exit 0: `evidence/stage3-kompile-concrete.log`.

2. Generated-semantics execution:

   `python3 /tmp/audit-work/127-intersection/run/semantics_differential.py`

   Sixteen normal and boundary inputs were compared against independently loaded trusted Python. There were zero mismatches and every `krun` exited 0 (`evidence/semantics_differential.py`, `evidence/stage3-concrete-differential.log`).

3. Bridge-free loop-proof definition:

   `kompile verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX --backend haskell --output-definition loop-fresh-kompiled`

   Exit 0: `evidence/stage3-kompile-loop.log`.

4. Submitted loop claim:

   `kprove spec.k --definition loop-fresh-kompiled --spec-module LOOP-CORRECTNESS-SPEC --output pretty`

   Output `#Top`, exit 0: `evidence/stage3-kprove-loop.log`.

5. Whole-program definition with the candidate bridge:

   `kompile verification.k --main-module VERIFICATION-WITH-LOOP-LEMMA --syntax-module MPY-SYNTAX --backend haskell --output-definition verification-fresh-kompiled`

   Exit 0: `evidence/stage3-kompile-entry.log`.

6. Submitted four-claim entry module:

   `kprove spec.k --definition verification-fresh-kompiled --spec-module SPEC --output pretty`

   Output `#Top`, exit 0: `evidence/stage3-kprove-entry.log`.

For claim-by-claim confirmation, `evidence/spec-labeled.k` reproduces the five claims unchanged except for audit labels. The loop claim and each of `entry-case-1` through `entry-case-4` independently printed `#Top` and exited 0; see `evidence/stage3-kprove-loop-individual.log` and `evidence/stage3-kprove-entry-case{1,2,3,4}.log`.

Thus fresh reconstruction verifies closure under the supplied theory. It does not establish that the supplied theory is sound; Stage 5 finds that it is not.

## 4. Adequacy and real-program pinning

### Claims in plain language

The loop claim starts at the exact submitted trial-division `While` followed by `Return("YES")`, with integer `N >= 2` in `length` and integer `D >= 2` in `divisor`. It claims that the final `<k>` value is `primeResult(N,D)` and existentially permits the final divisor to be any `Value`.

The four entry claims all require valid intervals, then partition all endpoint orderings:

| Case | Additional ordering | Claimed result | Satisfying witness | Concrete result |
|---|---|---|---|---|
| 1 | `C <= A`, `D >= B` | `lengthResult(B-A)` | `A=0,B=4,C=-1,D=5` | `"NO"` |
| 2 | `C <= A`, `D < B` | `lengthResult(D-A)` | `A=0,B=10,C=-2,D=1` | `"NO"` |
| 3 | `C > A`, `D >= B` | `lengthResult(B-C)` | `A=0,B=4,C=2,D=6` | `"YES"` |
| 4 | `C > A`, `D < B` | `lengthResult(D-C)` | `A=0,B=10,C=2,D=7` | `"YES"` |

For each witness, exactly one case precondition is true. Substitution into the claimed RHS agrees with the trusted canonical Python, candidate Python, and fresh K execution (`evidence/entry_witnesses.py`, `evidence/stage4-entry-witnesses.log`).

### Program identity and result constraint

The entry claims use `solutionProgram`, a `[function]` equation whose right-hand side is the exact constructor tree in submitted `solution.mpy`. Static comparison shows every statement and empty statement-list branch is present. The submitted `.mpy` was independently regenerated byte-for-byte from `solution.py`, and fresh concrete execution loads the same function body. This is an exact reification of the submitted program, not a substituted algorithm.

The claims start from empty function and environment maps, load the real function body, evaluate both tuple arguments, invoke `"intersection"`, and constrain the final `<k>` value to a reducible `lengthResult(...)`. The result is not a free variable, tautology, or one-way implication. Only final `<functions>` and `<env>` maps are existentially abstracted.

The four preconditions are mutually exclusive and exhaustive because `C <= A` versus `C > A`, and `D >= B` versus `D < B`, each form a complete split. Their result arithmetic is exactly `min(B,D)-max(A,C)`.

## 5. Rule-by-rule static soundness review

The exact numbered sources and attribute scans are preserved in `evidence/stage5-source-inventory.log`.

### Syntax, configuration, and construct coverage

The local syntax inventory is exhaustive:

- `MPY-SYNTAX`: `Program`/`Module`; `Stmts` as a `Stmt` list; two-string `Params`; statements `FuncDef`, `Assign`, `If`, `While`, and `Return`; `CmpOp`; expressions `Int`, `Str`, `Name`, binary `TupleExpr`, `Subscript`, `BinOp`, and single-comparator `Compare`.
- `MPY`: values `intVal`, `strVal`, `boolVal`, `tupleVal`, and `unbound`; the `Value -> Expr` and `Value -> KResult` injections; stored `function`; control items `runWith`, `saveFirstArg`, `saveSecondArg`, `invoke`, `assignTo`, `choose`, `loopGuard`, and `functionReturn`; and internal `compareValues`.
- Configuration: `<mpy>` contains `<k>`, `<functions>`, and `<env>`. Those are exactly the computation, function binding, and local-variable state used by the submitted program.
- `verification.k`: result functions `primeResult`, `intersectionResult`, `lengthResult`, and program reifier `solutionProgram`.

Every constructor in `solution.mpy` is declared and handled: `Module`, `FuncDef`, `Params`, statement lists, `Assign`, `If`, `While`, `Return`, `Name`, `Int`, `Str`, `Subscript`, `BinOp` with `+`, `-`, `*`, `%`, and `Compare` with `<`, `<=`, `>`, `==`. `TupleExpr` is used for the two entry inputs. No used construct is silently fabricated or left unmodeled.

There are no `[total]`, `[functional]`, `[simplification]`, `[concrete]`, `anywhere`, macro, opaque, oracle, or fresh-symbol declarations. The only special declarations are four `[function]` symbols and one `[priority(40)]` operational rule.

### Operational semantics inventory

Each semantic rule or context is accounted for below:

| Source | Rule/context and decision |
|---|---|
| `semantic.k:65` | `Module(S) => S`: faithful module-body loading for the one-function program. |
| `:66` | empty statement list consumes to `.K`: faithful. |
| `:67` | nonempty statement list schedules head before tail: faithful sequential control. |
| `:69-70` | registers the only `FuncDef` in an empty function map: exact for this program. It intentionally does not model multi-definition modules. |
| `:72-74` | evaluates the first argument, then the second, then invokes the designated `intersection`: correct left-to-right binding for the required entry point. |
| `:76-85` | looks up the selected function body, binds both parameters, preallocates all four locals, and replaces the old environment: correct for this single nonrecursive call. |
| `:88-90` | evaluates assignment RHS then updates an existing local: correct; every submitted assignment target was preallocated. |
| `:92-94` | evaluates the condition and selects exactly one statement list: correct. |
| `:96-98` | evaluates a loop guard, schedules body then the same loop when true, and exits when false: correct recurring small-step control. |
| `:102-103` | a `Return` discards the remaining function computation, evaluates its expression, and leaves its value: correct for the submitted side-effect-free string return expressions. |
| `:106-109` | integer/string construction and environment lookup: correct on all reached states. A lookup of the internal `unbound` marker would not raise Python's `UnboundLocalError`; no intended input reaches such a lookup, so this is an out-of-scope coverage limitation rather than an intended-domain unsoundness witness. |
| `:111-113` | two contexts enforce left-to-right tuple evaluation; the value rule constructs the pair: correct. |
| `:115-118` | two contexts enforce left-to-right subscript evaluation; index 0/1 rules return the respective pair component: exactly the used cases. Other indices are deliberately unmodeled. |
| `:120-126` | two contexts enforce left-to-right binary evaluation; `+`, `-`, `*`, and guarded nonzero `%` use K integer primitives: correct for the reached positive divisors. |
| `:128-135` | rewrites `Compare` to an explicitly ordered helper, evaluates left then right, and implements the four used integer comparators: correct. |

The semantics is deliberately a task-sized subset rather than general Python. Its restrictions—one function, two parameters, existing-name assignment, pair-only subscripting, and selected integer operations—cover every actual path of the submitted program. K integers match Python's unbounded integers here. The `%` rule is only reached with positive `length` and `divisor >= 2`, so Python/K negative-modulo differences are irrelevant.

### Proof functions and equations

| Source | Extension | Classification and decision |
|---|---|---|
| `verification.k:10-16` | Three `primeResult(N,D)` equations | Definitional summary. For the used domain `N>=2,D>=2`, guards are exhaustive and disjoint: either `D*D>N`, or the divisor is tested and is zero/nonzero. The recursive case strictly increments `D` and eventually crosses the square-root bound. No rule asserts `[total]`; undefined divisor-zero cases are outside every dependent claim. |
| `:18-24` | Two `intersectionResult` equations | Definitional summary with disjoint/exhaustive `<2`/`>=2` guards. It correctly uses `min(end)-max(start)`, but no claim depends on this symbol. |
| `:26-28` | Two `lengthResult` equations | Definitional summary with disjoint/exhaustive integer guards. It returns `"NO"` below 2 and otherwise delegates to `primeResult(N,2)`. |
| `:33-63` | `solutionProgram` equation | Exact program reification, not an execution shortcut or answer encoding. |
| `:71-89` | Priority-40 loop rewrite | Operational bridge. Its returned value is connected to bridge-free execution by the loop claim, but its state transition is false. This is the material soundness failure. |

The recursive summaries are neither opaque nor unconstrained: their equations fix all values used by the proof. Pairwise equation guards do not overlap with disagreeing right-hand sides. The ordinary mathematical bridge from trial division starting at 2 to primality is valid but is not separately formalized as a named prime predicate.

### Claims

- `LOOP-CORRECTNESS-SPEC` is a genuine bridge-free reachability proof. It exactly matches real loop control and establishes the returned `primeResult(N,D)`. Its post-state deliberately uses existential `?_VD` for the changed divisor.
- The four `SPEC` claims execute the reified submitted body and constrain its returned value. Their ordering partitions and postconditions are adequate.
- The four entry claims import and exercise the priority-40 bridge. A diagnostic run without that bridge reaches the genuine symbolic loop residual rather than closing (`evidence/spec-no-bridge.k`, `evidence/stage5-entry-without-bridge.log`). This bounded diagnostic is supporting evidence, not the basis of the verdict.

### Concrete false-conclusion witness for the unsound bridge

The bridge matches the exact loop plus trailing `Return("YES")`, any other environment entries, `N >= 2`, and `D >= 2`. It rewrites only `<k>`. Consequently, K frames and preserves the entire `<env>`, including the initial `"divisor" |-> intVal(D)`.

The bridge-free loop claim does **not** justify that preservation: its divisor cell explicitly rewrites `intVal(D) => ?_VD`, allowing the actual final value. For `N=5,D=2`, fixed execution tests 2, increments to 3, then exits because `3*3 > 5`.

This occurs on the intended valid input `interval1=(0,5)`, `interval2=(0,5)`, which satisfies entry case 1:

- Fresh concrete `krun` returns `"YES"` with `divisor = 3` (`evidence/stage5-concrete-input-0-5.log`).
- The bridge-free correct-state witness proves `divisor: 2 => 3` with `#Top` (`evidence/bridge-state-witness.k`, `evidence/stage5-bridge-fixed-correct.log`).
- The bridge-free definition rejects the false claim that the full reached environment preserves `divisor = 2`; its `WarnStuckClaimState` residual visibly contains `divisor = 3` (`evidence/stage5-bridge-actual-input-fixed-false.log`, exit 1).
- The candidate bridge-enabled definition proves that same false environment-preservation conclusion with `#Top` (`evidence/stage5-bridge-actual-input-extended-false.log`, exit 0).

Thus the priority rule enables a concrete false reachability conclusion on a state reached from a satisfying intended input. Rule priority makes it preempt the genuine `While` rule but does not supply the missing state equivalence. This violates operational-state preservation and invalidates the whole-program proof theory even though the particular returned string is correct.

## 6. Fresh non-vacuity test

The candidate supplied no vacuity artifact, so none was reused. `evidence/spec-vacuity-audit.k` is a fresh mutation of entry case 1 that replaces the result-bearing `lengthResult(B-A)` obligation with constant `strVal("YES")`.

The mutation is demonstrably false at `A=0,B=4,C=-1,D=5`: all case-1 preconditions hold, the intersection length is 4, and both Python implementations plus fresh K return `"NO"` (`evidence/stage4-entry-witnesses.log`).

- Dry-run parsing/build succeeded with exit 0 (`evidence/stage6-mutation-build.log`).
- Actual `kprove` exited 1 with `WarnStuckClaimState`. The residual has final `<k> strVal("NO")` against the mutated `"YES"` destination and retains the satisfiable case-1 constraints (`evidence/stage6-mutation-proof.log`).

This is a meaningful result-obligation failure, not a parser error, missing import, timeout, unreachable mutation, or unrelated crash. The original entry proof is result-constraining and non-vacuous. Passing non-vacuity does not repair the unsound operational bridge.

## 7. Proven versus assumed accounting

### What the successful runs establish under their actual theories

Under bridge-free `VERIFICATION`, the loop reachability proof establishes: for `N>=2,D>=2`, executing the exact trial-division loop and trailing `"YES"` return produces `primeResult(N,D)`, while the final divisor is existentially abstracted.

Under `VERIFICATION-WITH-LOOP-LEMMA`, the four whole-program runs establish: for every valid pair of integer intervals in one of the four exhaustive endpoint orderings, the final `<k>` value equals the corresponding `lengthResult` expression, while final function/environment maps are existential. This is closure under a theory containing the false state-preserving bridge; it is not a legitimate proof about fixed program execution.

### Trust ledger

| Boundary | Dependents | Accounting |
|---|---|---|
| K `INT`, `BOOL`, `STRING`, `MAP`, parser, compiler, and Haskell/LLVM backends | All semantic and proof runs | Standard low-level trusted primitives; acceptable. |
| Trusted `/reference/py2mpy.py` | Program identity | Byte regeneration establishes only syntactic fidelity; acceptable for the source-to-constructor bridge. |
| Candidate-generated `semantic.k` | All K conclusions | Reviewed rule by rule and concretely tested on used constructs. It is intentionally incomplete outside the submitted subset, but no used construct is missing. |
| `solutionProgram` exact constructor equation | Entry claims | Static exact reification plus byte-identical trusted translation; acceptable. |
| `primeResult`/`lengthResult` equations | Loop and entry postconditions | Values are fixed by truthful guarded trial-division equations on every dependent domain; no opaque oracle. |
| Trial division iff mathematical primality | Natural-language intent | Ordinary mathematical argument, not a separate K theorem. Differential evidence supports only tested cases. This would be an intent-bridge limitation, not permission for the false operational rule. |
| Existentials `?_VD`, `?_ENV`, `?_FUNCTIONS` | Loop/entry final state | Explicit state abstraction. `?_VD` is crucial: it means the loop theorem does not prove divisor preservation. |
| Priority-40 loop bridge | All four entry proof closures | Illegitimate. It strengthens existential final divisor to unchanged divisor and admits the demonstrated false conclusion. |
| Python/K differential tests | Program/semantics adequacy | Finite empirical support only; they do not substitute for the K proof or repair its theory. |

There are no opaque result symbols or external result oracles. The decisive assumed fact is instead an invalid operational-state transition. The program appears correct, the loop's returned-value connection is sound, and the entry postconditions are adequate, but the submitted whole-program proof relies on a materially unsound rule. Under the required decision boundary this is `FAIL / NOT_LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
