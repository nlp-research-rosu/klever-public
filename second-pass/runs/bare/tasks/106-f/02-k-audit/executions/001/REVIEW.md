# Independent adversarial audit: Problem 106-f

## Outcome

The candidate contains a legitimate, result-constraining partial-correctness proof of the submitted translated program under its generated K semantics. The proof was rebuilt without candidate caches, both positive claims closed, the proof shorthand expands to the submitted AST exactly, a reachable false postcondition was rejected, and a material body mutation invalidated the theorem.

The verdict is `CONCERNS / LEGIT`, rather than `PASS / LEGIT`, for two limited trust/adequacy reasons that do not make a false result provable:

1. `semantic.k` is an individually generated, minimal interpreter, not a supplied or independently proved CPython semantics. Its rules are sound for every construct used here, but the bridge to Python remains an exhaustively reviewed informal model supported by finite concrete tests.
2. The formal postcondition uses the accumulator recurrence `expected`; it does not formally state or prove `expected(N)` equal to the separately declared `expectedAt`/`mathFactorial`/`mathTriangle` functions. That connection follows by a straightforward induction and has broad differential support, but is not a separate machine-checked K theorem.

No materially unsound rule, oracle, execution bypass, substituted program, vacuity, or candidate infrastructure defect was found.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `GENERATED_SEMANTICS`. `/reference/reference-semantics` is absent as required; it is neither a file nor a symlink. There is therefore no infrastructure breach and no hidden reference semantics was sought or used. The exact check, candidate tree, artifact types, hashes, and bounded scans of the untrusted logs/trace are preserved in [00_provenance.sh](/audit-output/evidence/00_provenance.sh) and [00_provenance.log](/audit-output/evidence/00_provenance.log).

### Required artifacts and types

The following candidate artifacts are present and are ordinary regular files, not symlinks:

- `run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`
- the structured JSONL trace under `codex-trace/2026/07/22/`
- `prompt.py`, `py2mpy.py`
- `solution.py`, `solution.mpy`
- `semantic.k`, `verification.k`, `spec.k`, `prove.sh`

There are no candidate helper K files. `PROOF.md` and `spec-vacuity.k` are absent, but neither was a required candidate deliverable in this generation condition. Candidate-provided `semantic-kompiled/` and `verification-kompiled/` are additional build outputs; they were treated as untrusted extras and never copied or used.

No required artifact is missing, mistyped, or symlinked. `prompt.py` is byte-identical to `/reference/prompt.py` (SHA-256 `f9dee569...49ce19d`) and `py2mpy.py` is byte-identical to `/reference/py2mpy.py` (SHA-256 `406485ea...64db16`); both `cmp` operations exited 0.

### Untrusted generation claims

`run-input.json` claims problem `106-f`, condition `bare`, and hashes matching the mounted prompt and translator. `metrics.json` claims generation exit 0 without timeout. `codex-last.txt`, `codex-output.log`, and the structured trace claim a final successful `kprove`; the logs also contain intermediate stuck attempts. These were read only as provenance claims. None is used as proof evidence below.

All executable source artifacts needed for audit were copied to `/tmp/audit-work/106-f/source`; trusted inputs were copied separately to `/tmp/audit-work/106-f/reference`. Candidate compiled definitions and caches were not copied.

**Stage result:** integrity passes; the generated-semantics mount boundary is consistent.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

For a nonnegative integer `n`, `f(n)` must return a list of length `n`, indexed in the prompt by one-based `i = 1..n`. At each odd `i` it returns `1 + ... + i`; at each even `i` it returns `1 * ... * i = i!`. Thus `f(0) = []` and the documented example is `f(5) = [1, 2, 6, 24, 15]`.

The trusted canonical implementation computes each element with a fresh inner loop. The candidate uses running accumulators:

- before appending at iteration `i`, `factorial` becomes the product through `i`;
- `total` becomes the sum through `i`;
- the even branch appends `factorial`, and the odd branch appends `total`.

This is a different but extensionally equivalent algorithm on the intended domain. The K theorem restricts `N >= 0`, which matches the meaningful “list of size n” integer domain. Negative integers are excluded; non-integers, including Python booleans, are outside the K input sort/domain.

### Trusted regeneration

The trusted `/reference/py2mpy.py` regenerated `solution.mpy` from the submitted `solution.py`. The regenerated and submitted files are byte-identical with SHA-256:

```text
c3b6b7a6b415641b7bb201cb69b8bfb18fdb92963412f8ea5063d0a08e2f08d7
```

Commands and exits are in [01_fidelity_and_differential.log](/audit-output/evidence/01_fidelity_and_differential.log).

### Independent differential testing

[01_differential_test.py](/audit-output/evidence/01_differential_test.py) independently imports:

- the trusted `/reference/canonical.py` entry point;
- the copied candidate `solution.py` entry point;
- a reviewer-authored direct contract oracle.

It covers the empty boundary, first odd/even branch boundary, documented example, all successive parity/loop boundaries for `n=0..40`, and broader generated inputs `50`, `75`, and `100`: 44 inputs total. It records each input and either the complete result or length/head/tail/hash. There were zero mismatches and exit status 0. This is finite bridge evidence, not a universal substitute for the K proof.

**Stage result:** program fidelity passes.

## 3. Clean proof reconstruction

### Fresh builds

K version:

```text
K version: v7.1.293
Build date: Fri Oct 03 13:32:35 CDT 2025
```

The audit script first required both output-definition paths to be absent. It then built:

```text
kompile semantic.k --main-module SEMANTIC --syntax-module MPY-SYNTAX \
  --backend llvm \
  --output-definition /tmp/audit-work/106-f/build/semantic-kompiled

kompile verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --backend haskell \
  --output-definition /tmp/audit-work/106-f/build/verification-kompiled
```

Both exited 0. The script and bounded logs are [02_clean_rebuild.sh](/audit-output/evidence/02_clean_rebuild.sh), [02_kompile_semantic.log](/audit-output/evidence/02_kompile_semantic.log), and [02_kompile_verification.log](/audit-output/evidence/02_kompile_verification.log).

### Generated-semantics execution

The fresh LLVM definition executed the actual copied `solution.mpy` for `n = 0, 1, 2, 5, 8, 10`. [02_concrete_compare.py](/audit-output/evidence/02_concrete_compare.py) extracted each `<result>` list and compared it with both independent Python implementations. All six `krun` commands exited 0, all final `<k>` cells were `.K`, all result cells were `done(listVal(...))`, and the mismatch count was zero. Complete per-input logs are `02_krun_input_*.log`; the aggregate is [02_concrete_compare.log](/audit-output/evidence/02_concrete_compare.log).

These cases collectively exercise every construct and every branch used by the submitted program:

- module/function entry and parameter binding;
- empty and nonempty statement lists;
- assignments, lookups, integer/list values;
- zero-iteration and iterative `while`;
- true and false `if`;
- empty and singleton list expressions;
- integer `+`, `*`, `%`, list `+`, `<=`, and `==`;
- return.

### Real-program syntactic identity

The fresh Haskell definition expanded both the submitted `solution.mpy` and the `solution` macro to KORE. `cmp` exited 0, and both files have SHA-256:

```text
540c1642f3003eaf9d0dcff1aa11e5a9cae3c933d7158e7d17ed7ddb70d9f315
```

This is machine-checked syntactic pinning: the entry claim's shorthand is exactly the submitted translated program after macro expansion.

### Positive proof claims

The two labels in `spec.k` are `SPEC.loop-invariant` and `SPEC.main-correct`.

1. `SPEC.loop-invariant` was selected alone and returned exact `#Top`, exit 0.
2. To isolate `SPEC.main-correct` without deleting its required loop lemma, the already separately proved loop claim was retained with CLI `--trusted SPEC.loop-invariant`; the main proof returned exact `#Top`, exit 0. This is proof composition, not an unverified final assumption.
3. Both claims were then proved together with neither trusted; `kprove` returned exact `#Top`, exit 0.

Commands and outputs are in [02_claim_reconstruction.sh](/audit-output/evidence/02_claim_reconstruction.sh), [02_claim_reconstruction.log](/audit-output/evidence/02_claim_reconstruction.log), `02_kprove_loop_invariant.log`, `02_kprove_main_with_proved_loop.log`, and `02_kprove_all.log`.

One auditor diagnostic initially selected `main-correct` alone. K's `--claims` removed the loop circularity from the proof module, causing unbounded loop unrolling; the auditor interrupted that diagnostic (exit 130). It is preserved in `02_clean_rebuild.log`/`02_kprove_main_without_helper.log` and is not treated as a candidate failure. The required isolated-composition and fully untrusted runs above both succeeded.

**Stage result:** clean reconstruction passes.

## 4. Adequacy and real-program pinning

### `loop-invariant` claim in plain language

Precondition:

- `N >= 0` and `I >= 1`;
- `<k>` is exactly the submitted loop macro followed by the real `return result`;
- `<input>` is `N`;
- the environment contains exactly the five program variables:
  `factorial = F`, `i = I`, `n = N`, `result = L`, `total = T`;
- the result cell is `noResult`.

Postcondition:

- the computation is consumed (`<k> .K`);
- `n` remains `N`;
- the environment's `result` and the returned value are both exactly
  `expectedCompletion(I,N,F,T,L)`;
- the final `factorial`, `i`, and `total` are existentially quantified because the requested observable is the list result.

The claim deliberately does not require `F`, `T`, and `L` to be a mathematically valid prefix. This is not a weakness: it proves the exact loop summary for arbitrary accumulator values. `expectedCompletion` starts from precisely those arbitrary values and performs the same guarded updates as the loop.

### `main-correct` claim in plain language

Precondition:

- `N >= 0`;
- `<k>` contains `solution`, which expands exactly to submitted `solution.mpy`;
- input is `N`, environment is empty, and result is initially `noResult`.

Postcondition:

- execution consumes the computation;
- the exact five-variable final environment contains `n = N` and
  `result = expected(N)`;
- the returned value is exactly `done(listVal(expected(N)))`;
- only the irrelevant final accumulator values are existential.

The returned value is neither free nor connected by a one-way implication. Both the environment result and return cell are constrained to the same recursively defined exact list.

### Satisfying witnesses and concrete substitution

For `main-correct`, `N=0` with the initial empty environment satisfies the precondition and returns `[]`; `N=5` also satisfies it and returns `[1,2,6,24,15]`.

For `loop-invariant`, a reachable loop-head state after iterations 1 and 2 at `N=5` is:

```text
I=3, F=2, T=3, L=[1,2], n=5, result=noResult
```

All preconditions hold. A reviewer harness executed the real `solutionLoop ~> return` from this state and returned `[1,2,6,24,15]`; independently evaluating
`expectedCompletion(3,5,2,3,[1,2])` returned the same list. Both Python implementations also return that list for `n=5`. Evidence is in [03_loop_state_witness.log](/audit-output/evidence/03_loop_state_witness.log) and [03_ground_witnesses.log](/audit-output/evidence/03_ground_witnesses.log).

The first ground-harness invocation omitted the required `$INPUT` configuration value and exited 1 before execution. It was corrected by supplying `-cINPUT=0`; the fresh rebuilt harness and all ground runs then exited 0. The failed auditor invocation is preserved as `03_ground_witnesses_first_attempt.log` and is not candidate evidence.

### Body sensitivity

The reviewer changed only the `solution` macro's real initialization from `total = 0` to `total = 1`, leaving the claimed theorem unchanged. At `N=1`, the original returns `[1]` and the mutated body returns `[2]`. The mutated proof definition built successfully, and `kprove` then exited 1 with `WarnStuckClaimState`, exposing the unequal `expectedCompletion(...,T=0,...)` and `expectedCompletion(...,T=1,...)` terms. See [06_body_sensitivity.log](/audit-output/evidence/06_body_sensitivity.log), [verification-body-mutation.k](/audit-output/evidence/verification-body-mutation.k), and [spec-body-mutation.k](/audit-output/evidence/spec-body-mutation.k).

**Stage result:** both claims are adequate and pin the real submitted translated program.

## 5. Rule-by-rule static soundness review

The complete numbered source and mechanical inventory are preserved in [04_static_inventory.log](/audit-output/evidence/04_static_inventory.log). There are 28 semantic rules, 12 verification rules, and two claims. No helper K files exist.

### Local syntax and configuration inventory

`MPY-SYNTAX` declares:

- `Program`: `Module(Stmts)`;
- list sorts: juxtaposed `Stmts`, comma-separated `Strings`, comma-separated `Exprs`;
- `Params(Strings)`;
- `Stmt`: `FuncDef`, `Assign`, `While`, `If`, `Return`;
- `Expr`: `Int`, `Name`, `ListExpr`, `BinOp`, `Compare`;
- `CmpOp(String,Expr)`.

`SEMANTIC` declares:

- `Value`: `intVal(Int)`, `boolVal(Bool)`, `listVal(List)`;
- `Result`: `noResult`, `done(Value)`;
- continuations: `exec`, `eval`, `store`, `singleton`, `binLeft`, `binRight`,
  `cmpLeft`, `cmpRight`, `ifBranch`, `whileBranch`, `doReturn`.

The configuration has one top-level `<py>` cell containing:

- `<k>` for the parsed `Program`;
- immutable external `<input>` integer;
- `<env>` map, initially empty;
- `<result>`, initially `noResult`.

No heap, call stack, allocation store, I/O, or exception cell is needed by this program: it has one directly invoked function, immutable integer values, pure list concatenation followed by rebinding, and no calls, aliases, output, or exceptional used operations.

`VERIFICATION` locally declares exactly five `[function]` symbols:

- `mathFactorial(Int) : Int`;
- `mathTriangle(Int) : Int`;
- `expectedAt(Int) : Int`;
- `expected(Int) : List`;
- `expectedCompletion(Int,Int,Int,Int,List) : List`.

It also declares two `[macro]` shorthands: `solution : Program` and
`solutionLoop : Stmt`.

There are no `[total]`, `[functional]`, `[simplification]`, `[concrete]`,
priority, `owise`, `anywhere`, trusted-rule, opaque, oracle, fresh-result, or
uninterpreted declarations. The right-only `?_FOUT`, `?_IOUT`, and `?_TOUT`
variables are ordinary existential post-state values and cannot affect the
constrained returned list.

### Mapping every submitted construct to semantics

| Submitted construct | Declaration | Rules |
|---|---|---|
| `Module(FuncDef("f",Params("n"),...))` | `Program`, `Stmt`, `Params` | entry rule 63–65 |
| statement sequencing | `Stmts` | rules 67–68 |
| assignments to names | `Assign`, `Name` | rules 70–72 |
| `while` and its `i <= n` guard | `While`, `Compare`, `CmpOp` | rules 78–81, 102–105 |
| `if` and `i % 2 == 0` | `If`, `BinOp`, `Compare`, `CmpOp` | rules 74–76, 95–99, 102–104, 106 |
| integer/name expressions | `Int`, `Name` | rules 87–89 |
| `[]` and singleton `[x]` | `ListExpr`, `Exprs` | rules 91–93 |
| integer `+`, `*`, `%` | `BinOp` | rules 95–99 |
| list `+` | `BinOp` | rules 95–96, 100 |
| `return result` | `Return` | rules 83–85 |

Every used syntax production has behavior; no used construct is silently fabricated or left stuck.

### All 28 ordinary semantic rules

| # / source | Rule role | Soundness assessment |
|---|---|---|
| 1 / `semantic.k:63` | Enter sole `FuncDef`, bind sole parameter to external input | Sound for the submitted one-function entry artifact. This defines the generated interpreter's call interface; it does not claim full Python module-import behavior. |
| 2 / `:67` | Empty statement list becomes `.K` | Sound sequence base case. |
| 3 / `:68` | Execute head statement, then remaining statements | Sound left-to-right statement order. |
| 4 / `:70` | Assignment evaluates RHS before storing | Sound evaluation order for name assignment. |
| 5 / `:71` | Store evaluated value with map update | Sound; preserves all other bindings. |
| 6 / `:74` | Stage `if` condition evaluation | Sound; neither branch executes early. |
| 7 / `:75` | True selects only then-statements | Sound. |
| 8 / `:76` | False selects only else-statements | Sound. |
| 9 / `:78` | Stage `while` condition evaluation | Sound. |
| 10 / `:79` | True executes body and then reconstructs the same loop | Sound reevaluation/control flow. |
| 11 / `:81` | False exits loop | Sound zero/final-iteration behavior. |
| 12 / `:83` | Evaluate return expression | Sound. |
| 13 / `:84` | Set result and discard remaining function-body continuation | Sound for the sole top-level invocation; prior state is preserved and no caller frame exists in the modeled subset. |
| 14 / `:87` | Evaluate integer literal | Sound identity embedding into `intVal`. |
| 15 / `:88` | Look up name in environment | Sound; undefined names visibly stick, and none occurs on intended executions. |
| 16 / `:91` | Empty list expression | Sound. |
| 17 / `:92` | Evaluate singleton list element | Sound for the only nonempty list literal shape used. |
| 18 / `:93` | Build singleton integer list | Sound; the used elements are integers. |
| 19 / `:95` | Evaluate binary left operand first | Sound Python order. |
| 20 / `:96` | Then evaluate right operand while retaining left value | Sound. |
| 21 / `:97` | Integer addition | Sound on unbounded integers. |
| 22 / `:98` | Integer multiplication | Sound on unbounded integers. |
| 23 / `:99` | Integer remainder | Sound on the used positive `i` and positive divisor 2; no sign/zero-divisor discrepancy is reachable. |
| 24 / `:100` | Ordered list concatenation | Sound for Python `result + [value]`; because result is rebound and no alias observes allocation identity, a heap is unnecessary. |
| 25 / `:102` | Evaluate comparison left side first | Sound. |
| 26 / `:104` | Then evaluate comparison right side | Sound. |
| 27 / `:105` | Integer `<=` | Sound. |
| 28 / `:106` | Integer `==` | Sound. |

The rules are deterministic on all configurations reached by the submitted program. Their continuations enforce left-to-right evaluation. The true/false control rules and operator-specific completion rules are disjoint. There are no priorities or overlapping used semantic completions.

The entry rule ignores the textual function name and directly runs the sole definition. This is broader than necessary but does not enable a false conclusion for the actual term, which contains exactly `FuncDef("f", Params("n"), ...)` and is KORE-pinned. Unsupported general-Python situations—multiple definitions, calls, mutation aliases, exceptions, arbitrary list literals, or wrong operand types—remain outside this intentionally minimal language and are unused.

### All 12 verification rules

| # / source | Classification and domain | Soundness assessment |
|---|---|---|
| 1 / `verification.k:12` | Definitional summary: `0! = 1` | True. |
| 2 / `:13` | Definitional summary: `N! = (N-1)! * N`, `N>0` | True, strictly descends on nonnegative ground inputs. |
| 3 / `:16` | Definitional summary: triangular sum at 0 is 0 | True. |
| 4 / `:17` | Definitional summary: `T(N)=T(N-1)+N`, `N>0` | True, strictly descends. |
| 5 / `:20` | `expectedAt(N)=N!` for positive even `N` | True by definition of intended even entries. |
| 6 / `:22` | `expectedAt(N)=T(N)` for positive odd `N` | True by definition of intended odd entries. |
| 7 / `:28` | Initialize completion at `I=1,F=1,T=0,L=[]`, `N>=0` | True contract initialization. |
| 8 / `:31` | Stop at `I>N` and return accumulated list | True. |
| 9 / `:33` | Even step updates product/sum, appends updated product, increments `I` | Exactly matches the real loop. |
| 10 / `:38` | Odd step updates product/sum, appends updated sum, increments `I` | Exactly matches the real loop. |
| 11 / `:47` | `solutionLoop` macro expansion | Pure syntax expansion to the submitted real while term; not an operational shortcut. |
| 12 / `:62` | `solution` macro expansion | Pure syntax expansion to the submitted full module; KORE equality independently confirmed. |

Guard analysis:

- factorial and triangle base/recursive guards are disjoint; negative inputs are intentionally partial and no `[total]` attribute claims otherwise;
- `expectedAt`'s positive even/odd guards are disjoint and exhaustive for positive integers; it is partial outside that domain and is unused by the reachability claims;
- `expected` is used only under the claim's `N >= 0` precondition;
- `expectedCompletion` guards partition all integer `I,N`: `I>N` versus `I<=N`, then even versus non-even. The recursive cases increment `I`, so ground evaluation terminates after `N-I+1` steps when `I<=N`.

`mathFactorial`, `mathTriangle`, and `expectedAt` are mathematically sound but not dependents of either claim. They therefore neither help nor compromise closure.

`expected`/`expectedCompletion` are result-bearing definitional summaries, but they do not replace execution. The real program executes under the 28 semantic rules; the loop reachability claim is the universal machine-checked connection from that execution to `expectedCompletion`. Using the same summary in the postcondition is therefore not a circular oracle pattern.

The two macros are compile-time syntax aliases, not operational bridges. Their complete expansion is identical to the submitted AST. No proof-local rule preempts a semantic computation, fabricates a branch/result, pops a frame, or omits observable state.

### Calls, returns, state, overlap, and trust-boundary findings

- **Calls/binding:** there is no `Call` node in the submitted AST. The module-entry convention binds the exact sole parameter `"n"` to input `N`; the exact AST pin excludes rebinding or substituted bodies.
- **Returns/control:** return evaluates its expression before setting `<result>` and discarding only the remaining top-level function-body continuation. This matches the used model, which has no caller/call stack.
- **State:** the environment map preserves prior bindings on update; input is unchanged; result changes only once at return.
- **Allocation/identity:** integers and the observable list contents are modeled. Python list allocation identity is unobservable here because there are no aliases or identity tests.
- **Exceptions:** intended inputs make all lookups defined and every operation well typed; `%` divisor is constant 2. Missing exception semantics for unused/error cases is not silently used to prove the claim.
- **Numbers:** K mathematical integers match Python arbitrary-precision integers for the used arithmetic.
- **Overlaps/priorities:** used rules and proof equations have disjoint completion guards. There are no explicit priorities or simplifications to audit.

No inventoried rule was found unsound, so no false-conclusion witness is asserted. The narrower evidence limitations are the intentionally minimal entry-point convention and the unformalized whole-language equivalence to CPython; both are recorded as concerns rather than mislabeled unsoundness.

**Stage result:** static soundness passes for the submitted program and intended domain.

## 6. Fresh non-vacuity test

The reviewer created a fresh `SPEC-VACUITY` module, preserved as [spec-vacuity.k](/audit-output/evidence/spec-vacuity.k). It changes both result-bearing destinations from:

```text
expected(N)
```

to the deliberately false:

```text
expected(N) ListItem(0)
```

`N=0` satisfies the original precondition. Both Python implementations and fresh concrete K execution return `[]`, whereas the mutation requires `[0]`.

Results:

1. Mutated-spec `kprove --dry-run` exited 0, establishing successful parse/build.
2. The live mutated proof exited 1, not by timeout or parser/import failure.
3. It produced `WarnStuckClaimState` with the expected failed implication and residual equality:

```text
expectedCompletion(1,N,1,0,.List) ListItem(0)
  #Equals
expectedCompletion(1,N,1,0,.List)
```

The artifact, exact commands, exit statuses, and residual are in [05_nonvacuity.sh](/audit-output/evidence/05_nonvacuity.sh), [05_nonvacuity.log](/audit-output/evidence/05_nonvacuity.log), [05_vacuity_dry_run.log](/audit-output/evidence/05_vacuity_dry_run.log), and [05_vacuity_kprove.log](/audit-output/evidence/05_vacuity_kprove.log).

**Stage result:** non-vacuity passes.

## 7. Proven versus assumed accounting

### Precisely machine-proved

Under the freshly compiled candidate definition, for every mathematical integer `N >= 0`:

- starting from the exact submitted program AST (via a macro whose expanded KORE is byte-identical), empty environment, input `N`, and `noResult`;
- every terminating execution under `semantic.k` reaches `.K`;
- the final environment's `"result"` and the returned `<result>` cell both contain exactly `expected(N)`.

The auxiliary claim universally proves that from any state with `N>=0`, `I>=1`, and arbitrary accumulator values `F,T,L`, executing the actual loop followed by the actual return produces exactly `expectedCompletion(I,N,F,T,L)`.

This is a partial-correctness result. Although the concrete loop plainly terminates for nonnegative `N` because `i` starts at 1 and increases by 1 until exceeding `N`, total correctness/termination is not the theorem claimed here.

### Trust ledger

| Boundary | Effect/dependents | Assessment and support |
|---|---|---|
| K toolchain, reachability logic, Haskell/LLVM backends | All builds, executions, and claims | Acceptable foundational trust boundary. Fresh builds and independent positive/negative runs reduce cache/report risk but do not prove the prover itself. |
| Imported K `INT`, `BOOL`, `STRING`, `MAP`, `LIST` hooks | Arithmetic, comparisons, parity, bindings, list order | Acceptable low-level primitives. They are fixed outside the program theorem and used according to their standard meanings. |
| Trusted `py2mpy.py` mount | Bridge from `solution.py` AST to `solution.mpy` | Acceptable designated translator trust. Trusted regeneration was byte-identical. |
| Candidate-generated `semantic.k` | Meaning of every submitted MPY construct | Concerning but legitimate. It was not assumed from prior compilation: every local rule was inventoried/reviewed, all used constructs were exercised, and six K/Python concrete comparisons agreed. There is no machine-checked universal CPython equivalence theorem. |
| Entry interface `Module(FuncDef(...))` directly executes the sole body with `$INPUT` | Binding/call convention for the proof | Acceptable for this single-entry generated artifact and exact AST, but intentionally not a general Python-module semantics. |
| Ordinary induction connecting running `F,T` to factorial/triangular values | Bridge from formal `expected` recurrence to prompt wording | Mathematically straightforward and supported by 44 differential inputs, but not expressed as a K theorem. This is the principal intent-formalization concern. |
| Finite differential/concrete tests | Python equivalence and generated-semantics bridge on tested inputs | Empirical support only; explicitly not treated as universal proof. |
| CLI-trusted loop claim in isolated main run | Isolated proof composition | Not a remaining assumption: that exact loop claim was independently proved first, and the final all-claims run used no trusted claims. |

There are no candidate opaque symbols, result-bearing oracles, external I/O contracts, simplification axioms, trusted proof rules, or empirical values injected into execution. The existential final accumulator variables do not influence the observable result.

### Gate accounting

- **Real-program soundness:** PASS. Actual body execution is KORE-pinned; no operational bridge replaces it; all state/control footprints are modeled for used constructs; functions are guarded and sound; satisfying witnesses exist; body and postcondition mutations are rejected.
- **Intent adequacy:** behaviorally aligned, with a documented formalization limitation. The formal `expected` recurrence is extensionally the prompt's sequence, but the named factorial/triangle functions are not connected to it by a separate K claim.
- **Evidence/auditability:** PASS. Scripts, exact commands, inputs, exits, and bounded logs are preserved under `/audit-output/evidence`; finite evidence is not overstated.

The limitations support `CONCERNS`, not `FAIL`: neither admits an incorrect result under the intended domain, and the proof remains a genuine theorem about the real submitted translated program.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
