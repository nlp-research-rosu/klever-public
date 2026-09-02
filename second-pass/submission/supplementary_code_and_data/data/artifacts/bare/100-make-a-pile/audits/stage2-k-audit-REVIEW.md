# Independent adversarial review: HumanEval/100 `make_a_pile`

The candidate does not contain a legitimate partial-correctness proof of the
generated program. The Python implementation is correct, its translation is
authentic, the generated concrete semantics is adequate for every construct the
program uses, and all five submitted K claims reproducibly print `#Top`.
Nevertheless, the proof-local rule at `verification.k:47-65` directly rewrites
the exact loop from an invariant state to the desired final answer. The
initialization, preservation, and exit claims are not premises of that rule and
do not establish it. They are separate claims, while the loop summary is already
installed as a `[simplification]` equation in the compiled definition.

This is an assumed correctness conclusion, not a derivation from the submitted
program's operational semantics. The candidate therefore fails the
real-program execution and proof-extension soundness gate even though the
claimed answer is true.

## 1. Input and provenance integrity

The launcher declares:

- problem `100-make-a-pile`;
- condition `bare`;
- `record_layout = legacy-selected-stage1`;
- `semantics_mode = GENERATED_SEMANTICS`;
- candidate mount `/candidate`;
- trusted mounts `/reference/canonical.py`, `/reference/prompt.py`, and
  `/reference/py2mpy.py`.

I read `/audit-input.json` before using the candidate, then read
`/audit-campaign-lock.json`. The complete `audit_campaign` object equals the
lock object. The mounted lock hashes to
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
exactly the value recorded in `/audit-input.json`.

All records required for `legacy-selected-stage1` are present and readable.
The listed files are regular files, and the trace is a real directory:

- `/run.json`
- `/task.json`
- `/generation-result.json`
- `/generation-evidence/invocation.json`
- `/generation-evidence/metrics.json`
- `/generation-evidence/codex-last.txt`
- `/generation-evidence/codex-output.log`
- `/generation-evidence/prompt.txt`
- `/generation-evidence/codex-trace/`

`/generation-evidence/usage.json` is also present and was inspected. Historical
runtime metrics are not required for this layout and were not reconstructed.
The 498,954-byte trace contains 282 JSONL records; every record parses. Its one
JSONL file hashes to
`2032c4e34a6975c5d001b58fe6cf8a86eaa724850d31893e07d45a7b1cbd7e51`,
matching both `invocation.json` and `generation-result.json`. The generation
output has 22,571 lines and was scanned in full; its final claim is treated only
as untrusted history.

The independently computed hashes of the mounted records match the launcher
values:

| Mounted input | SHA-256 |
|---|---|
| `/run.json` | `16ab5496e5b7251ecd747d4b58693a614cb2f6d680317214f597d0437ab39c24` |
| `/task.json` | `3c8faafb991e37395fcad232edfa28a8085a913426b07efd1b0d4767fdb61543` |
| `/generation-result.json` | `bb16c423336078bd9293e38a184c3ff4cf09f6402143ad63cc362f7e6e1f87ea` |
| `invocation.json` | `50c319f781c1db0749a84786b4d065584efd66f5930b4de65cc1c80f228e00bc` |
| `metrics.json` | `3538ceef3e37ad5d55dd8216b172da062a2959ed45ddf5480edc895c469cddd4` |
| `usage.json` | `43a9cce244b0c1bd5f3b9473b718c3d23b314e64cf1e5144d8c737453352d02a` |
| `codex-last.txt` | `0c3266e941aacd48ba941a2d4c2f82cfe21e1dd45103a879530d11f8ace21250` |
| `codex-output.log` | `0d9a6d5b0b9e325585394b8da61c9bc3bdc0b751169475b231c9b7907a0a4304` |
| `prompt.txt` | `4fbd8d83152646045c82c9b1c86a3c0c9bf686de949fcbf8c3eff6755a261d9e` |
| trusted canonical | `72f04a58d8d5be9f6287cc032ef29c428b708b982c9b45007c481e231887f77b` |
| trusted prompt | `bec48d3dcd0c53db5bf1a185da2df8f0b1d58608c9c953c96f090d38e8fb0a98` |
| trusted translator | `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16` |

I recursively enumerated and hashed every candidate and trace entry rather than
using the recorded opaque tree digests as evidence. No symlink or unsupported
node was found. `/candidate/prompt.py` and `/candidate/py2mpy.py` are
byte-identical to their trusted mounts. The candidate's compiled/cache evidence
(`kore-exec.tar.gz` and `__pycache__`) was not reused.

The generated-semantics boundary is correct:
`/reference/reference-semantics` is absent. I did not infer or seek a hidden
reference semantics. K 7.1.293 is independently installed and matches the
campaign lock. There is no infrastructure breach.

Evidence:

- `evidence/stage1_provenance.log`
- `evidence/stage1_trace_and_identity.log`
- `evidence/inspect_generation_trace.py`
- `evidence/stage1_generation_output_inspection.log`

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For every positive integer `n`, return a list of exactly `n` level sizes. The
first is `n`; each following level is the next number of the same parity, hence
two larger. Equivalently, the result is:

```text
[n + 2*i for i in range(n)]
```

Thus the list is `[n, n+2, ..., n+2(n-1)]`. This restates both
`/reference/prompt.py` and `/reference/canonical.py`.

### Submitted implementation

`/candidate/solution.py` starts with an empty list, takes `i` from `n-1` down
through zero, and prepends `n + 2*i`. At termination it returns the ascending
sequence required by the contract. Its use of repeated prepend is less
efficient than the canonical comprehension but extensionally correct.

I regenerated the constructor program from the scratch copy with the trusted
translator:

```bash
python3 py2mpy.py solution.py > solution.regenerated.mpy
cmp -s solution.regenerated.mpy solution.mpy
```

Both files have SHA-256
`40fe8a33eb00f4b494b665af35e35e0da0fd3280a3c345acd004bdaca512136c`;
`cmp` exited 0.

The independent differential script imports the trusted canonical function and
the submitted function separately. Its expected-value oracle is the direct
contract formula, not any K equation. It tested the example `3`, positive
boundary `1`, both loop-guard outcomes, odd/even representatives, every integer
from 1 through 64, and 99, 100, 257, and 1000. It also tested 0 and -1 as
explicit out-of-contract empty-loop probes. All 70 inputs matched the canonical
function and the direct oracle; `MISMATCHES=0`, exit 0.

This finite evidence supports implementation fidelity but is not used as a
universal proof.

Evidence:

- `evidence/differential_test.py`
- `evidence/stage2_fidelity_and_differential.log`

## 3. Clean proof reconstruction

I copied only source artifacts and trusted inputs into
`/tmp/audit-work/reconstruction`. No candidate-built definition, KORE archive,
or Python cache was copied or used.

### Generated concrete semantics

The exact clean build command was:

```bash
kompile --backend llvm semantic.k \
  --main-module MPY --syntax-module MPY-SYNTAX \
  --output-definition audit-semantic-kompiled
```

It exited 0. I then ran:

```bash
krun solution.mpy --definition audit-semantic-kompiled -cN=0
krun solution.mpy --definition audit-semantic-kompiled -cN=1
krun solution.mpy --definition audit-semantic-kompiled -cN=2
krun solution.mpy --definition audit-semantic-kompiled -cN=3
krun solution.mpy --definition audit-semantic-kompiled -cN=6
```

Every run exited 0 with `.K`. The K results were respectively:

```text
[]
[1]
[2, 4]
[3, 5, 7]
[6, 8, 10, 12, 14, 16]
```

Independent Python execution returned the same lists. Zero is outside the
stated theorem domain but validates the boundary false-guard path.

### Proof definition and all positive claims

The proof definition was independently built with:

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
```

The build exited 0. I ran each submitted positive claim independently:

```bash
kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC --claims SPEC.invariant-initialization
kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC --claims SPEC.invariant-preservation
kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC --claims SPEC.invariant-exit
kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC --claims SPEC.loop-invariant
kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC --claims SPEC.functional-correctness
```

Each command printed `#Top` and exited 0. The combined unfiltered command also
printed `#Top` and exited 0.

Crucially, every claim emitted `WarnTrivialClaim: Claim proven without
rewriting`. This is consistent with both sides being simplified through the
proof-local function equations before reachability reasoning. The clean
reconstruction establishes closure under the submitted theory, not the
soundness of that theory.

Evidence:

- `evidence/stage3_concrete_rebuild_and_execution.log`
- `evidence/stage3_proof_rebuild_and_claims.log`

## 4. Adequacy and real-program pinning

### Plain-language claims

| Claim | Precondition | Claimed result |
|---|---|---|
| `invariant-initialization` | `N > 0` | Executing `result=[]; i=N-1` from `{n=N}` ends normally with empty suffix `pileFrom(N,N)`. |
| `invariant-preservation` | `N > 0` and `0 <= I < N` | One loop body step changes suffix `I+1` to suffix `I` and changes `i` from `I` to `I-1`. |
| `invariant-exit` | `N > 0` | Returning from `i=-1, result=pileFrom(N,0)` produces that list. |
| `loop-invariant` | `N > 0` and `-1 <= I < N` | The whole loop plus trailing return reaches `i=-1` and returns `pileFrom(N,0)`. |
| `functional-correctness` | `N > 0` | The exact submitted module, under `evalEntry`, returns `pileFrom(N,0)`. |

All formal preconditions are satisfiable. The preserved witness check uses:

- initialization: `N=3`, starting environment `{n:3}`;
- preservation: `N=3, I=1`, starting result `[7]`;
- exit: `N=3, I=-1`, starting result `[3,5,7]`;
- loop: `N=3, I=2`, starting result `[]`;
- function: `N=3`.

For `N=3`, the claimed `pileFrom(3,0)` is `[3,5,7]`; both the trusted
canonical and submitted Python functions return `[3,5,7]`, and concrete K
execution produces `VList(VCons(VInt(3), VCons(VInt(5),
VCons(VInt(7), .Vals))))`.

Evidence:

- `evidence/claim_witness_check.py`
- `evidence/stage4_claim_witnesses.log`

### Constructor-level source pinning

The functional claim contains the submitted module and body constructor for
constructor. The only textual difference is that the K claim spells the
generated empty expression-list terminator as `ListExpr(.Exprs)`, whereas the
concrete parser spells it `ListExpr()`. After this parser-level list
normalization, `kast --output kore` produced byte-identical KORE for the
submitted `solution.mpy` and the extracted claim term. Both KORE files hash to:

```text
c280d58fa37d454bb830e6ff6ade59049fe43ed6a45a5b0b35012e929818a102
```

The initial attempt to feed `.Exprs` directly to the program parser failed,
which is preserved; the normalized comparison exited 0. This demonstrates the
normalization rather than assuming it.

A body-sensitivity mutation changed the multiplier in the function term from 2
to 4 while leaving the postcondition unchanged. The mutated claim parsed and
reached the prover, then failed with `WarnStuckClaimState`, exit 1, at the
unmatched `evalLoop`. Thus the claim term is genuinely sensitive to the body
embedded in the claim.

Evidence:

- `evidence/spec_program_term.mpy`
- `evidence/stage4_program_term_comparison.log`
- `evidence/stage4_program_term_comparison_normalized.log`
- `evidence/spec-body-mutation.k`
- `evidence/stage4_body_sensitivity.log`

### Fatal real-execution gap

Syntactic pinning does not establish semantic execution. The functional claim's
outer term is:

```text
goal(proof(evalEntry(Module(...), N)))
```

It is not a claim over the generated `<mpy><k>...</k>...</mpy>`
configuration. `evalEntry`, `evalStmts`, `evalExpr`, `evalBin`, and `evalCmp`
form a second, proof-local big-step evaluator. When it encounters the actual
`While`, `evalStmts` rewrites to the otherwise unevaluated constructor
`evalLoop`. The rule at `verification.k:47-65` then changes:

```text
proof(evalLoop(exact-loop, exact-return, invariant-map))
```

directly to the desired `proof(Returned(... pileFrom(N,0) ...))`.

There is no rule that unfolds an `evalLoop` iteration, no circular reachability
claim deriving the loop result, and no bridge-free theorem connecting this
big-step summary to the generated small-step `<k>` semantics.

I attempted the missing universal connection directly using only
`semantic.k`: execute the exact real `While` and trailing return from an
arbitrary invariant state. The fixed semantics compiled successfully, but
`kprove` stopped with `WarnStuckClaimState` and two unexplored branches, exit 1.
That failed attempt is not evidence that the claimed loop equation is false; it
shows that the required connection theorem is absent and was not recovered by
the candidate's theory.

Removing only `verification.k:45-65` (the summary comment and rule) also built
successfully. The functional claim then failed at the residual
`proof(evalLoop(...))`, exit 1. Therefore its successful closure depends on
that rule.

The three separately named initialization, preservation, and exit claims do
not repair this. K claims in `spec.k` are targets; they are not imported as
premises proving the simplification rule. The `loop-invariant` claim has
essentially the same left and right sides as the already-installed
simplification equation, which explains why it is reported as proven without
rewriting.

Evidence:

- `evidence/spec-connection.k`
- `evidence/stage4_bridge_free_connection_attempt.log`
- `evidence/verification-no-summary.k`
- `evidence/spec-no-summary.k`
- `evidence/stage5_summary_dependency.log`

## 5. Rule-by-rule static soundness review

There are no additional helper K source files. `semantic.k`,
`verification.k`, and `spec.k` are the complete local theory audited here.

### Syntax, declarations, attributes, and cells

`semantic.k` declares:

- `PyModule` with `Module`;
- list sorts `Stmts`, `Strings`, and `Exprs`;
- statement constructors `FuncDef`, `Assign`, `While`, and `Return`;
- expression constructors `Name`, `Int`, `ListExpr`, `BinOp`, and `Compare`;
- `CmpOp`;
- values `VInt`, `VBool`, `VList`, and `VNone`;
- value-list constructors `.Vals` and `VCons`;
- the `Val < Expr` subsort;
- continuation items `exec`, `assignTo`, `binLeft`, `binRight`, `makeList`,
  `listOne`, `compareLeft`, `compareApply`, `whileGuard`, and `finishReturn`;
- transparent functions `vAppend` and `pileFrom`;
- cells `<k>`, `<n>`, `<env>`, and `<result>` under `<mpy>`.

`verification.k` declares:

- function symbols `evalExpr`, `evalBin`, `evalCmp`, `evalStmts`,
  `evalEntry`, and `proof`;
- outcomes `Normal` and `Returned`;
- the `evalLoop` outcome constructor;
- the `Goal` constructor.

No local declaration has `[total]`, `[functional]`, `[priority]`,
`[anywhere]`, `[macro]`, `[alias]`, or an opaque attribute. The label
`functional-correctness` is a claim label, not a `[functional]` declaration.
`evalLoop` is nevertheless operationally opaque: it has no iteration
semantics. `proof` has no general evaluator; its material evaluator is the
loop-summary simplification. The only local `[simplification]` rule is
`verification.k:47-65`.

### Construct coverage

`solution.mpy` uses `Module`, `FuncDef`, one `Params` name, statement and
expression lists, `Assign`, `Name`, empty and singleton `ListExpr`, `BinOp`
with `+`, `-`, and `*`, `While`, `Compare`, `CmpOp(">=")`, `Int`, and
`Return`. Every used constructor has a syntax declaration and a concrete rule
path. Missing rules for unused multi-element list literals, other operators,
multiple functions, and Python exceptions are not defects in this
generated-semantics mode.

The concrete configuration has exactly the material state for this program:
current computation, external integer argument, variable bindings, and return
result. Python integers and K `Int` are both unbounded in the relevant model.
The program performs no I/O, heap mutation, allocation visible outside lists,
exceptions on intended inputs, or nested calls.

### Every `semantic.k` rule

| Lines | Rule decision |
|---|---|
| 51 | `vAppend(.Vals,YS) => YS`: true base equation. |
| 52 | `vAppend(VCons(V,XS),YS)`: true recursive equation; strict structural descent. |
| 56-57 | `pileFrom(N,I) => .Vals` for `I>=N`: correct empty suffix. |
| 58-59 | `pileFrom(N,I)` cons case for `I<N`: correct head and increasing-index recursion. Guards are disjoint and cover all K integers. |
| 70-72 | Module load binds the sole parameter to `<n>` and starts its body. It ignores the function name, but matches the actual sole-function module exactly and introduces no wrong behavior on the submitted term. |
| 74 | Empty statement execution terminates. |
| 75 | Nonempty statements execute head before tail, matching source order. |
| 77 | Integer literal becomes the same integer value. |
| 78-79 | Name lookup returns the existing map binding. All submitted lookups are bound. |
| 81 | `ListExpr` delegates to list construction. |
| 82 | Empty expression list yields an empty value list. |
| 83 | Singleton expression list evaluates its element. Only empty and singleton literals are used. |
| 84 | The singleton continuation wraps the evaluated value. |
| 86 | Binary evaluation starts with the left operand. |
| 87 | The evaluated left value is retained while the right operand evaluates. |
| 88 | Integer addition reconstructs left-plus-right correctly despite continuation variable order. |
| 89 | Integer subtraction reconstructs left-minus-right correctly. |
| 90 | Integer multiplication reconstructs left-times-right correctly. |
| 91 | List addition appends the evaluated right list to the evaluated left list. |
| 93 | Comparison starts with its left operand. |
| 94 | Comparison retains the left value while evaluating the right. |
| 95 | `>=` computes left-greater-or-equal-right correctly. |
| 97 | Assignment evaluates the right side before mutation. |
| 98-99 | Assignment replaces/inserts exactly the named environment binding. |
| 101 | While first evaluates its guard. |
| 102-103 | A true guard executes the body, then returns to the same loop head. |
| 104 | A false guard consumes the loop. The true/false cases are disjoint and exhaustive for the program's boolean guards. |
| 106 | Return first evaluates its expression. |
| 107-108 | Return stores the value and discards the remaining computation, matching abrupt function return. The actual return is last, but the rule also has correct broader control behavior for this model. |

I found no mathematically false concrete rule and therefore make no
unsupported unsoundness allegation requiring a false witness. Evaluation order,
state updates, guard polarity, list order, and return control agree with the
program on its intended positive-integer domain. The fresh concrete runs
exercise every used rule family.

### Every `verification.k` rule

| Lines | Rule decision |
|---|---|
| 13 | Big-step integer literal: locally correct. |
| 14 | Big-step bound-name lookup: locally correct. |
| 15 | Big-step empty list: locally correct. |
| 16-17 | Big-step singleton list: locally correct for used literals. |
| 18-19 | Big-step binary-expression dispatch: locally correct and functional. |
| 20-21 | Big-step comparison dispatch: locally correct. |
| 23 | Big-step integer addition: true. |
| 24 | Big-step integer subtraction: true. |
| 25 | Big-step integer multiplication: true. |
| 26 | Big-step list concatenation: true given `vAppend`. |
| 27 | Big-step integer `>=`: true. |
| 37 | Empty statement sequence returns the current environment: true. |
| 38-39 | Assignment evaluates in the old environment and updates one binding before the tail: locally correct. |
| 40-41 | Return evaluates its expression and discards the tail: locally correct. |
| 42-43 | While becomes `evalLoop`: a dispatch step, but `evalLoop` has no fixed iteration semantics. |
| 47-65 | Fatal proof extension. It replaces the exact loop and continuation with the complete desired final map and value whenever the stated invariant holds. It reads the whole body, continuation, and exact three-binding map; it writes the final index, result binding, and returned value. Its result affects the final theorem. No bridge-free universal connection theorem justifies it. |
| 67-69 | Entry binds the single parameter and invokes the proof-local evaluator: locally correct, but it selects the duplicate evaluator rather than the concrete `<k>` semantics. |

The proof-local expression and straight-line statement equations appear
truthful for the used subset, but they are a parallel interpreter with no
machine-checked equivalence to `semantic.k`. The loop summary is worse: it
contains the property-bearing computation's complete answer. It is a
program-derived operational bridge, not an external primitive or merely a
mathematical name.

I do **not** claim that the summary equation is extensionally false; for the
exact loop and invariant its conclusion agrees with the Python algorithm, so
there is no honest false-conclusion witness for that existing equation. Its
defect is proof-theoretic and still disqualifying: the candidate assumes the
universal loop-correctness result it was required to derive. The benchmark
explicitly rejects a rule that encodes the task's answer even when finite tests
suggest the encoded answer is true.

### Claims in `spec.k`

The five claims are exhaustively restated in Stage 4. Initialization,
preservation, and exit prove valid isolated big-step calculations. They are not
linked by a circularity, induction theorem, or premise relation to the summary
rule. The loop and whole-program claims close only after that summary is
available as an equation. This is confirmed mechanically by the
summary-removal experiment.

Evidence:

- `evidence/stage5_static_inventory.log`
- `evidence/stage5_summary_dependency.log`

## 6. Fresh non-vacuity test

The candidate contains no `spec-vacuity.k`; none was trusted. I created a
distinct reviewer mutation that changes only the final returned value of the
functional-correctness claim:

```diff
- VList(pileFrom(N, 0)))))
+ VList(pileFrom(N, 1)))))
```

The environment postcondition still requires the correct full list. The
changed return obligation is demonstrably false for the satisfying input
`N=1`: the program and original claim return `[1]`, while `pileFrom(1,1)` is
empty.

The mutation successfully built to KORE:

```bash
kprove spec-vacuity.k --definition audit-verification-kompiled \
  --spec-module SPEC-VACUITY \
  --claims SPEC-VACUITY.functional-correctness --dry-run
```

Exit: 0.

The actual proof command:

```bash
kprove spec-vacuity.k --definition audit-verification-kompiled \
  --spec-module SPEC-VACUITY \
  --claims SPEC-VACUITY.functional-correctness
```

exited 1 with `WarnStuckClaimState`. Its residual contrasts the correct
`VCons(VInt(N), pileFrom(N,1))` return with the mutated `pileFrom(N,1)`.
This is meaningful non-vacuity evidence: the original postcondition constrains
the returned value.

Passing non-vacuity does not repair the real-execution gap. It shows that the
summary axiom fixes a specific answer, not that the program was proved to
compute that answer.

Evidence:

- `evidence/spec-vacuity.k`
- `evidence/stage6_fresh_non_vacuity.log`

## 7. Proven versus assumed accounting

### What the successful K run establishes

Under the compiled theory consisting of `semantic.k` plus all equations in
`verification.k`, K establishes for every K integer `N > 0` that:

```text
goal(proof(evalEntry(exact-submitted-module, N)))
```

simplifies to a `Returned` outcome whose environment and value contain
`pileFrom(N,0)`. It also establishes the three isolated initialization,
one-body-step, and return calculations. The exact submitted constructor term
is present, and `pileFrom` transparently denotes
`[N, N+2, ..., N+2(N-1)]`.

### What is assumed or only empirically supported

| Boundary | Effect | Assessment |
|---|---|---|
| K 7.1.293 Haskell/LLVM backends and built-in `INT`, `BOOL`, `MAP`, `K-EQUAL` | Arithmetic, booleans, maps, parsing, and proof execution | Acceptable low-level toolchain trust. |
| Trusted `py2mpy.py` | Connects `solution.py` to `solution.mpy` | Acceptable provenance bridge; byte identity was checked. |
| Generated `semantic.k` | Defines the intended Python subset | Independently reviewed and concretely tested; adequate for all used constructs, but generated semantics itself remains part of the candidate trust boundary. |
| `pileFrom` equations | Define the mathematical postcondition | Acceptable transparent definition; guards cover all integers and recursion descends. |
| Proof-local `evalExpr`/`evalBin`/`evalCmp`/straight-line `evalStmts`/`evalEntry` | Duplicate concrete behavior | Locally plausible but not machine-connected to the concrete semantics. |
| `evalLoop` and `proof(evalLoop(...))` simplification | Supplies all remaining control evolution, final state, and returned value | Illegitimate program-derived operational bridge; it assumes the central theorem and has no bridge-free universal connection proof. |
| Differential tests over 70 inputs and concrete K runs over five inputs | Support Python equivalence and generated-semantics adequacy on tested cases | Reproducible finite evidence only; not a universal proof. |
| Informal mathematical observation that the descending prepend loop is correct | Explains why tests and the asserted summary agree | True-looking informal argument, but absent as a K reachability/connection proof. |

The proof does not establish that the generated `<k>` semantics executes the
submitted loop to the claimed outcome for arbitrary positive `N`. It does not
establish a universal equivalence between the proof-local big-step evaluator
and the generated operational semantics. Finite differential and concrete
tests cannot supply either theorem.

### Gate and verdict accounting

- Real-program soundness / Gate A: **FAIL**. The result-bearing loop is replaced
  by an unproved, task-answer simplification. Removing it makes functional
  correctness fail.
- Intent adequacy / Gate B considered independently: the domain `N > 0` matches
  the full positive-integer source contract, and the stated result is the right
  unrestricted mathematical sequence. There is no bounded-domain narrowing.
- Trust and evidence / Gate C: provenance and tests are reproducible, but no
  universal connection evidence exists for the fatal bridge.
- Fresh non-vacuity: **PASS**, but it cannot override Gate A.

Accordingly, this is not a `CONCERNS / LEGIT` case. The central correctness
fact is encoded as a proof rule rather than proved from real program execution,
which meets the benchmark's `FAIL / NOT_LEGIT` boundary.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
