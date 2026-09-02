# Independent adversarial review: 142-sum-squares

The candidate reconstructs to a genuine, non-vacuous K reachability proof under
its own definition. The proof term is the submitted translated program, and the
mathematical summary is correct. It is nevertheless not a legitimate proof of
the real generated Python program over the unrestricted source-contract domain:
the generated call semantics admits unbounded recursion and returns a value for
a 1,500-element input on which the submitted `solution.py` terminates with
`RecursionError`. This is a concrete, result-bearing semantics mismatch, not
merely missing evidence.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout =
legacy-selected-stage1`, condition `bare`, problem `142-sum-squares`, and
`semantics_mode = GENERATED_SEMANTICS`. I used only its `container_paths`;
host-only provenance paths were not followed.

- `/audit-campaign-lock.json` is a real regular file, is byte-hashed as
  `ad5dfcc...d745`, and its decoded object is exactly equal to the
  `audit_campaign` block. The hash equals the launcher record.
- `/reference/reference-semantics` is absent, as generated-semantics mode
  requires. `/reference` contains exactly the three real regular trusted files
  `canonical.py`, `prompt.py`, and `py2mpy.py`.
- The required selected-stage1 records are present and real:
  `/run.json`, `/task.json`, `/generation-result.json`,
  `invocation.json`, `metrics.json`, `codex-last.txt`,
  `codex-output.log`, `prompt.txt`, and the structured trace. `usage.json`
  is present and was inspected. The legacy extras were also inspected.
  Historical `runtime-metrics.json` is not required for this layout.
- Every launcher-recorded regular-file hash matches an independent SHA-256.
  Every evidence leaf listed by `/generation-result.json` also matches,
  including the sole trace JSONL file. The independently computed
  pipeline tree hash is `f909625c...c4d`, equal to the retained-workspace
  hash in both the invocation and result records. The trace tree hash is
  `136fea0f...1777`, equal to `usage.json`'s source-trace hash.
- No symlink exists below `/candidate`, `/reference`, or
  `/generation-evidence`. The candidate prompt and translator are byte-identical
  to their trusted mounted versions.
- I inspected the generation records as untrusted history. The 198-event
  structured trace and the full generation log describe construction attempts
  followed by one `#Top`; that claim played no role in accepting the proof.
- The required candidate proof artifacts are all real files:
  `solution.py`, `solution.mpy`, `semantic.k`, `verification.k`, `spec.k`,
  and `prove.sh`. The candidate cache was not copied or used.

The reproducible checks, exact command, statuses, and hashes are in
`evidence/01-provenance.log` and
`evidence/24-launcher-root-hash-and-types.log`; the checker is
`evidence/check_provenance.py`. There is no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

For every finite list of integers, add the square of an element at an index
divisible by 3; otherwise add its cube if its index is divisible by 4; otherwise
add the element unchanged. Index 0 and indices divisible by both 3 and 4 take
the square branch. Return the sum, with the empty-list result 0.

The trusted canonical implementation iterates left-to-right and implements
exactly that contract. The candidate implements the same recurrence from the
right: it computes the last index, selects the same contribution, recursively
processes the prefix, and adds the contribution.

Running the trusted translator on the scratch copy of `solution.py` produced a
file byte-identical to submitted `solution.mpy` (both SHA-256
`2987f9f6...3417`), recorded in
`evidence/02-translation-byte-identity.log`.

`evidence/differential_test.py` independently imports the trusted canonical
function and candidate function. It covers:

- all three documented examples;
- prefix lengths 0 through 14, including indices 0, 3, 4, 6, 8, 9, and the
  square-over-cube precedence boundary at 12;
- all 19,531 lists of lengths 0 through 6 over
  `[-5, -1, 0, 1, 2]`;
- 502 deterministic representative cases, including negative, zero, large,
  and arbitrary-precision integers.

All 20,051 normal cases matched
(`evidence/03-differential.log`). A separate unrestricted-domain probe found:

```text
input: list(range(1500))
canonical.py: 211307438250
solution.py: RecursionError: maximum recursion depth exceeded in comparison
```

That source-level divergence is preserved in the same log and is connected to
the K model in `evidence/22-recursion-boundary-bridge.log`.

## 3. Clean proof reconstruction

Only source files were copied to `/tmp/audit-work/candidate-src`; the candidate
`__pycache__` and every candidate-built definition/cache were excluded.
K v7.1.293 was found independently (`evidence/04-toolchain.log`).

Fresh builds:

```text
kompile semantic.k --main-module MPY-SEMANTICS \
  --syntax-module MPY-SYNTAX --backend llvm \
  --output-definition /tmp/audit-work/semantic-llvm-kompiled-audit
exit 0

kompile verification.k --main-module MPY-VERIFICATION \
  --syntax-module MPY-SYNTAX --backend haskell \
  --output-definition /tmp/audit-work/verification-kompiled-audit
exit 0
```

The bounded complete outputs are
`evidence/05-kompile-llvm.log` and
`evidence/06-kompile-haskell.log`.

The recursive call claim was selected independently and closed:

```text
kprove spec.k --definition /tmp/audit-work/verification-kompiled-audit \
  --spec-module MPY-SPEC --claims MPY-SPEC.sum-squares-call
#Top
exit 0
```

The candidate's two-claim proof unit was then run with both labels explicitly:

```text
kprove spec.k --definition /tmp/audit-work/verification-kompiled-audit \
  --spec-module MPY-SPEC \
  --claims MPY-SPEC.sum-squares-call,MPY-SPEC.sum-squares-program
#Top
exit 0
```

See `evidence/07-kprove-call.log`,
`evidence/09-kprove-all.log`, and
`evidence/21-kprove-explicit-all-labels.log`. Selecting only the end-to-end
claim removes its induction/circularity claim from the prover and consequently
unrolls until the bounded 20-second diagnostic timeout
(`evidence/23-kprove-program-isolated-timeout.log`). That diagnostic is not a
failure of the submitted proof unit: the call claim is its explicit proved
auxiliary lemma, and the complete proof unit closes.

The fresh LLVM semantics was executed on 17 normal and boundary inputs. Every
execution exited 0 with a terminal `VInt`, and every value matched trusted
Python, including empty, every material branch boundary, negative values, and
arbitrary-precision values. See
`evidence/k_concrete_differential.py` and the successful
`evidence/11-k-concrete-differential-fixed.log`. The earlier
`evidence/10-k-concrete-differential.log` records a reviewer regex-escaping
mistake; it was repaired in the preserved script, and no K execution in that
run failed.

## 4. Adequacy and real-program pinning

The call claim at `/candidate/spec.k:8` says: for any constructor-level integer
list `IS`, any caller environment `ENV`, and any continuation `KREST`, invoking
the loaded `sum_squares` binding returns exactly
`VInt(sumSquaresSpec(IS))`, preserves `KREST`, and restores `ENV`. Its function
cell is fixed to `solutionFunctions`; there is no free return variable.

The entry claim at `/candidate/spec.k:16` says: for any `IS:Ints`, starting with
empty function and environment maps, load `solutionProgram`, run the required
entry point on `ListVal(IS)`, and finish with exactly
`VInt(sumSquaresSpec(IS))`, while the function cell becomes
`solutionFunctions`. It has no domain-strengthening `requires`.

Both preconditions are satisfiable. For example:

```text
IS = 2, -3, 4, -5, 6
ENV = .Map
KREST = .K
sumSquaresSpec(IS) = 246
canonical.py = 246
solution.py = 246
fresh krun = 246
```

The trusted regenerated MPY establishes source-to-constructor identity. For
constructor-level claim pinning, I compiled a definition whose syntax includes
the proof aliases and ran both the submitted `solution.mpy` and the nullary
`solutionProgram` alias on the same input. Their complete terminal KAST
configurations were byte-identical, SHA-256
`32e9c854...5fe8` (`evidence/14-kompile-pinning-syntax.log` and
`evidence/15-constructor-pinning-fixed.log`). `ListExpr()` in the submitted
surface syntax parses as `ListExpr(.Exprs)`, the only normalization visible in
the alias.

The body is sensitivity-tested, not merely source-file-sensitive. In
`evidence/verification-body-mutated.k`, the actual constructor term executed by
`solutionProgram` changes the index-divisible-by-3 branch from multiplication
to addition. The mutated definition compiled, but its original result claim
failed with the explicit residual

```text
sumSquaresSpec(initInts(IS)) + (lastInt(IS) + lastInt(IS))
  = sumSquaresSpec(initInts(IS)) + lastInt(IS) * lastInt(IS)
```

See `evidence/19-kompile-body-mutation.log` and
`evidence/20-kprove-body-mutation.log`. Thus the proof depends on the submitted
body.

## 5. Rule-by-rule static soundness review

### Configuration and construct coverage

`semantic.k` has exactly the state needed by this program: `<k>` for active
computation/continuations, `<functions>` for the loaded binding, and `<env>` for
locals. Saved environments and recursive control are represented in the K
continuation. There is no heap or I/O because the submitted program neither
mutates lists nor performs I/O.

Every used constructor is declared and modeled:

| Submitted construct | Declaration | Behavior |
|---|---|---|
| `Module`, `FuncDef`, `Params` | `semantic.k:6-15` | load rules S01-S03 |
| statement sequencing, `Return`, `Assign`, `If` | `semantic.k:8-12` | S09-S18 |
| `Int`, `Name`, empty `ListExpr` | `semantic.k:17-25` | S19-S21 |
| `BinOp` `+ - * %` and unary `-` | `semantic.k:21-22` | S22-S26, S38-S41 |
| singleton `Compare` and `CmpOp("==", ...)` | `semantic.k:23,26-27` | S27-S29, S42-S43 |
| `Call(len, ...)` and recursive call | `semantic.k:24` | S30-S33 |
| last-element subscript and `[:-1]` slice | `semantic.k:25,28-30` | S34-S37, S47-S50 |
| integer-list runtime values | `semantic.k:37-43` | S44-S50 |

### Exhaustive local declaration inventory

The 25 declarations in `semantic.k` are: `Pgm` (line 6), `Stmts` (8), `Stmt`
(9-12), `Params` (14), `Strings` (15), `Exprs` (17), `Expr` (18-25),
`CmpOps` (26), `CmpOp` (27), `Index` (28-29), `Bound` (30), the three `Ints`
productions (37, 38, 39), `Value` (40-43), `Function` (59), `Outcome` (61),
the continuation `KItem` declaration (63-80), `makeReturned` (119),
`negateResult` (136), and the five function declarations `binResult` (161),
`compareResult` (167), `lengthInts` (172), `lastInt` (177), and `initInts`
(181).

The five declarations in `verification.k` are the functions
`elementContribution` (line 9), `sumSquaresSpec` (19), `sumSquaresBody` (29),
`solutionProgram` (61), and `solutionFunctions` (65).

There are no local `[total]`, `[functional]`, `[concrete]`, priority, `owise`,
or macro declarations. There is no unaxiomatized result-bearing opaque symbol.
The deliberately partial semantic functions stop on unsupported operator/type
or empty-last-element combinations; they do not fabricate a result. The only
local simplification rules are V01-V03 below.

The full machine-extracted declaration list and counts are preserved in
`evidence/16-local-declaration-inventory.log`.

### All 50 semantic rules

| IDs and source | Rules reviewed | Static decision |
|---|---|---|
| S01 `:84`, S02 `:85`, S03 `:86-88` | turn a module into `load`, finish empty loading, install each one-argument binding | Sound for the exact one-function module; Map update matches later binding replacement. |
| S04 `:90` | `run(ARG)` invokes `"sum_squares"` | Sound task entry-point selection. |
| S05 `:94-96` | look up `F`, save caller env, bind one parameter, execute body, finish, restore | Binding, argument value, and caller-env behavior are correct for ordinary calls, but its unguarded, depth-free match domain is materially over-broad relative to real CPython; concrete witness below. |
| S06 `:97`, S07 `:98`, S08 `:99-100` | convert normal/returned call outcomes and restore env | Sound for ordinary completion and return. |
| S09 `:104`, S10 `:105`, S11 `:106-107`, S12 `:108-109` | empty statement list, return, assignment evaluation, assignment update | Sound; return discards only the unexecuted statement tail while retaining call continuations. |
| S13 `:110-111`, S14 `:112-113`, S15 `:114-115`, S16 `:116`, S17 `:117` | evaluate guard, select exactly one branch, resume or propagate return | Guards are disjoint; control and trailing statements are preserved correctly. |
| S18 `:120` | turn an evaluated value into `returned(V)` | Sound return packaging. |
| S19 `:123`, S20 `:124-125`, S21 `:126` | integer literal, lexical/local name lookup, empty list literal | Sound on every occurrence in the submitted body. |
| S22 `:128-129`, S23 `:130-131`, S24 `:132-133` | left-to-right binary evaluation and result dispatch | Sound evaluation order and continuation preservation. |
| S25 `:135`, S26 `:137` | unary-minus evaluation and integer negation | Sound. |
| S27 `:139-140`, S28 `:141-142`, S29 `:143-144` | left-to-right singleton comparison evaluation | Sound for the submitted singleton equality comparisons. |
| S30 `:146`, S31 `:147`, S32 `:148-149`, S33 `:150` | evaluate `len`; disjointly evaluate every non-`len` one-argument call; invoke it | The `"len"` and non-`"len"` guards are disjoint and preserve binding for this module. S33 feeds S05 and inherits its recursion-resource mismatch. |
| S34 `:154-155`, S35 `:156`, S36 `:157-158`, S37 `:159` | evaluate `[-1]` and `[:-1]`, then take last/prefix | Sound on nonempty integer lists; empty use visibly gets stuck and is unreachable after the submitted empty-list branch. |
| S38 `:162`, S39 `:163`, S40 `:164`, S41 `:165` | integer `+`, `-`, `*`, `%` result equations | True, pairwise operator-disjoint equations. Divisors in the program are positive 3 and 4 and indices are nonnegative. |
| S42 `:168`, S43 `:169-170` | integer equality and integer-list equality against empty | True and disjoint by value constructor. The list equation tests exactly emptiness. |
| S44 `:173`, S45 `:174`, S46 `:175` | length of empty, singleton, and snoc lists | Constructor-disjoint, exhaustive on parsed ground integer lists, and recursively descending. |
| S47 `:178`, S48 `:179` | last of singleton and snoc lists | Constructor-disjoint and true on every nonempty ground list. |
| S49 `:182`, S50 `:183` | prefix of singleton and snoc lists | Constructor-disjoint and true on every nonempty ground list. |

### All eight verification rules and both claims

| IDs and source | Rule/claim | Static decision |
|---|---|---|
| V01 `verification.k:10-11` | square when `I % 3 == 0` `[simplification]` | True. |
| V02 `:12-14` | cube when not divisible by 3 but divisible by 4 `[simplification]` | True. |
| V03 `:15-17` | unchanged in the remaining case `[simplification]` | True. V01-V03 have disjoint guards and cover every integer. |
| V04 `:20-21` | empty `sumSquaresSpec` is 0 | True base equation. |
| V05 `:22-25` | nonempty summary equals prefix summary plus last contribution at `length-1` | True, descending structural recurrence. V04/V05 guards are disjoint and exhaustive on ground lists. |
| V06 `:30-59` | `sumSquaresBody` alias | Exact constructor definition; does not replace execution. |
| V07 `:62-63` | `solutionProgram` alias | Exact module wrapper; does not replace execution. |
| V08 `:66-67` | `solutionFunctions` alias | Exact loaded-binding Map; does not replace execution. |
| C01 `spec.k:8-12` | contextual recursive-call reachability claim | A proved induction/circularity, not an ordinary execution-bypassing rule. It takes semantic steps before the smaller recursive call, preserves arbitrary `KREST`, and restores `ENV`. |
| C02 `spec.k:16-20` | end-to-end reachability claim | Result-constraining and pinned, but its interpretation as a claim about actual CPython inherits S05's material gap. |

The proof adds no operational bridge or answer oracle. `sumSquaresSpec` is a
fully equated definitional summary, and the recursive call is connected to it
by C01 under the operational semantics.

### Required false-conclusion witness for the unsound match domain

S05 matches every loaded one-argument call with no recursion-depth state, guard,
or exception behavior. Starting from the submitted module and the intended
input `list(range(1500))`, the fresh K semantics performs all 1,500 recursive
calls and reaches:

```text
VInt(211307438250)
```

The trusted canonical Python function also returns `211307438250`, confirming
the intended mathematical result. The submitted `solution.py`, however,
terminates with:

```text
RecursionError: maximum recursion depth exceeded in comparison
```

The exact executable witness is
`evidence/recursion_boundary_bridge.py`; command, exit status, and results are
in `evidence/22-recursion-boundary-bridge.log`. Thus S05/S33 enable the false
conclusion that this actual program call returns normally. Because the formal
precondition admits every finite `Ints` value and the HumanEval prompt gives no
length bound, the witness is inside both the formal and source-contract
domains. This is material generated-semantics unsoundness, not an unused
construct gap.

## 6. Fresh non-vacuity test

The candidate supplied no vacuity artifact to rely on. I created
`evidence/spec-vacuity-audit.k`, retained the genuine recursive call claim, and
changed only the end-to-end result obligation to
`VInt(sumSquaresSpec(IS) +Int 1)`. The satisfying input `IS = .Ints` makes the
true result 0 and mutated result 1.

The mutation dry-run parsed and built successfully with exit 0
(`evidence/17-vacuity-dry-run.log`). The actual proof exited 1 with
`WarnStuckClaimState` and the expected unmet implication:

```text
sumSquaresSpec(IS) +Int 1 = sumSquaresSpec(IS)
```

See `evidence/18-vacuity-proof.log`. The failure is reachable and
result-specific, so the positive proof is non-vacuous.

## 7. Proven versus assumed accounting

What the successful K proof establishes is precise: under the candidate's
three-cell, unbounded-stack MPY semantics, for every constructor-level finite
integer sequence, the exact submitted function body returns the recursively
defined `sumSquaresSpec`, preserves its continuation, and restores the caller
environment. The summary implements the stated square/cube/unchanged
contribution recurrence. This theorem is universal over list length in that
model; it is not a finite unrolling.

Trust and assumption ledger:

| Boundary | Dependents | Assessment |
|---|---|---|
| K v7.1.293 compiler, Haskell prover/backend, LLVM concrete backend | all machine results | Necessary low-level trust boundary; tool version and fresh builds recorded. |
| Built-in mathematical `Int`, `Bool`, `String`, structural K equality, and `Map` operations | arithmetic, guards, state | Acceptable for mathematical integers and maps. |
| Trusted `py2mpy.py` transliteration | source-to-MPY bridge | Strongly supported: byte-identical regeneration. |
| Alias-to-submitted-program identity | both claims | Mechanically supported by identical terminal KAST and body mutation sensitivity. |
| `sumSquaresSpec` to the prose contract | postcondition meaning | Direct structural definition plus 20,051 zero-mismatch differential cases; finite testing supports but does not replace the K execution theorem. |
| Integer-list-only input representation | theorem domain | Matches the stated list-of-integers domain; unsupported Python objects are properly excluded. |
| Unbounded call stack and absence of `RecursionError` in S05/S33 | C01, C02, every sufficiently deep execution | Illegitimate here: it changes a reachable control/result outcome for an unrestricted intended input, with the concrete 1,500-element witness above. |

The candidate's prior `#Top`, prose, and traces are not part of the trust
boundary. The fresh `#Top` proves closure only under the submitted definition.
Because that definition produces a normal return where the real submitted
Python program raises on an admitted input, the proof does not pin the real
program over the material source-contract domain. Under the benchmark's
decision boundary, this requires `FAIL / NOT_LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
