# Independent adversarial audit: 77-iscube

## Decision

The candidate contains a legitimate, non-vacuous partial-correctness proof of
the submitted generated program under its generated MPY semantics. I rebuilt
all definitions from source, obtained `#Top` with exit 0 for both complete spec
modules and for claim-focused proof runs, checked that the proof executes the
exact constructor tree in `solution.mpy`, and found no unsound local semantic or
proof rule.

The verdict is `CONCERNS / LEGIT`, rather than `PASS / LEGIT`, for two
non-fatal adequacy limitations:

1. The K spec proves four parameterized input families (positive/negative cubes
   and positive/negative open gaps), not one top-level theorem over arbitrary
   integer `A` with an `iff` cube predicate. Their exhaustiveness uses the
   ordinary but informal fact that every positive non-cube lies strictly
   between consecutive nonnegative cubes.
2. The trusted canonical uses floating-point cube roots and returns `False` for
   some very large exact integer cubes. The submitted exact-integer algorithm
   agrees with the plain-language contract, but universal equivalence with that
   canonical implementation is false.

All evidence referenced below is reviewer-authored or a bounded reviewer
summary under `evidence/`. Candidate logs and compiled directories were not
used as proof authority.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `GENERATED_SEMANTICS`. `/reference` contains exactly the
three regular trusted files `canonical.py`, `prompt.py`, and `py2mpy.py`;
`/reference/reference-semantics` is absent. This satisfies the required mode
boundary, so there is no infrastructure breach. See
`evidence/stage1_integrity.log`.

### Required artifacts

The following candidate artifacts are present as regular, non-symlink files:

- `run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`, and
  the JSONL generation trace;
- `prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`, `semantic.k`,
  `verification.k`, `spec.k`, and `prove.sh`.

No symlink exists anywhere below `/candidate`. There is no `PROOF.md` or
candidate `spec-vacuity.k`; neither is needed to reconstruct the submitted
proof. Candidate-generated `__pycache__`, `semantic-kompiled`,
`cube-verification-kompiled`, and `gap-verification-kompiled` directories are
additional untrusted build products. They were not copied or used. The complete
top-level inventory is in `evidence/stage1_supplement.log`.

`/candidate/prompt.py` is byte-identical to `/reference/prompt.py` with SHA-256
`7396a97d...b0de`. `/candidate/py2mpy.py` is byte-identical to the trusted
translator with SHA-256 `406485ea...db16`. No required artifact is missing,
mistyped, changed against an applicable trusted counterpart, or symlinked.

### Untrusted generation claims

I parsed all 382 JSONL trace records and scanned the full 27,580-line
`codex-output.log`. The candidate claims that `prove.sh` exited 0, both proof
partitions produced `#Top`, and a 54,101-input Python check passed. Those claims
were treated only as provenance and independently reconstructed. Counts,
hashes, and bounded excerpts are in
`evidence/untrusted_claims_summary.log`; the parser is
`evidence/untrusted_claims_summary.py`.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementations

The trusted prompt requires `iscube(a)` for a valid integer `a`, returning
`True` exactly when there exists an integer whose cube equals `a`. It explicitly
classifies `1`, `-1`, `64`, and `0` as cubes and `2` and `180` as non-cubes.

The trusted canonical normalizes with `abs`, computes a floating-point cube
root, rounds it, and compares the rounded integer's cube to the magnitude
(`/reference/canonical.py:19-20`).

The candidate (`/candidate/solution.py:1-7`) normalizes a negative input,
increments `n` from zero while `n^3 < |a|`, and returns whether the first
`n` with `n^3 >= |a|` has `n^3 == |a|`. Over mathematical integers this is an
exact implementation of the plain-language property. Zero is both the
zero-iteration/empty-loop boundary and a documented example.

### Trusted translation

I regenerated the constructor term with:

```text
python3 /reference/py2mpy.py /tmp/audit-work/77-iscube/candidate-src/solution.py > /tmp/audit-work/77-iscube/regenerated-solution.mpy
```

The command exited 0. The regenerated file is byte-identical to
`/candidate/solution.mpy`; both have SHA-256
`c77f1c5b...6073d`. See `evidence/stage2_program_fidelity.log`.

### Independent differential test

`evidence/differential_test.py` independently imports the trusted canonical and
the copied generated entry point. It also uses a separately implemented
binary-search exact-integer oracle. Its recorded scope is:

- all six documented examples;
- explicit sign, `if`, zero-loop, perfect-cube, and just-below/just-above
  boundaries;
- every integer in `[-50,000, 50,000]`;
- both signs of `n^3 + delta` for roots `0..500`, `999`, `1000`, `10000`, and
  `100000`, with `delta` in `{-2,-1,0,1,2}`;
- 5,000 deterministic random integers in `[-10^9,10^9]`, seed `770077`.

There were 109,681 unique cases, zero candidate/canonical mismatches, and zero
candidate/exact-oracle mismatches. The exact command, scope, and result are in
`evidence/stage2_program_fidelity.log`.

`evidence/canonical_precision_probe.py` separately diagnoses the trusted
reference. It reports `False` for exact cubes whose roots are
`1,000,000,000,000,000` and `562,949,953,421,312`. This is not a direct
candidate differential at those impractically large loop counts, but the final
integer equality in the candidate would be true when it terminates. This
reference limitation is one reason for `CONCERNS`; it does not make the
candidate's exact-integer theorem false.

## 3. Clean proof reconstruction

### Isolation and toolchain

Only source files were copied to `/tmp/audit-work/77-iscube/candidate-src`.
Every compiled definition used below was freshly created under
`/tmp/audit-work/77-iscube`; all three candidate-provided compiled definitions
and caches were ignored. The installed independent toolchain is K
`v7.1.293`.

### Generated-semantics build and concrete execution

The LLVM definition was freshly built from `semantic.k` as
`audit-semantic-kompiled`, exit 0. I ran the actual copied `solution.mpy` on:

```text
-65 -64 -63 -2 -1 0 1 2 7 8 9 26 27 28 64 180
```

Every `krun` exited 0, consumed `<k>` to `.K`, and produced the same Boolean as
independent Python execution. This set includes all documented examples,
negative normalization boundaries, zero iterations, exact cubes, and values on
both sides of cube boundaries. Commands and complete bounded configurations are
in `evidence/stage3_reconstruction.log`.

### Fresh Haskell definitions and positive claims

The cube and gap proof definitions were separately rebuilt from
`verification.k` with main modules `VERIFICATION` and `GAP-VERIFICATION`.
Both builds exited 0. The following reconstructed proofs all exited 0 and
printed `#Top`:

| Proof run | Claims exercised |
|---|---|
| `--spec-module CUBE-SPEC` | `cube-loop`, `nonnegative-cube`, `negative-cube` |
| `CUBE-SPEC --claims CUBE-SPEC.cube-loop` | `cube-loop` alone |
| `CUBE-SPEC --exclude CUBE-SPEC.negative-cube` | `cube-loop` and `nonnegative-cube` |
| `CUBE-SPEC --exclude CUBE-SPEC.nonnegative-cube` | `cube-loop` and `negative-cube` |
| `--spec-module GAP-SPEC` | `gap-loop`, `positive-noncube`, `negative-noncube` |
| `GAP-SPEC --claims GAP-SPEC.gap-loop` | `gap-loop` alone |
| `GAP-SPEC --exclude GAP-SPEC.negative-noncube` | `gap-loop` and `positive-noncube` |
| `GAP-SPEC --exclude GAP-SPEC.positive-noncube` | `gap-loop` and `negative-noncube` |

The exact commands and outputs are in
`evidence/stage3_reconstruction.log` and
`evidence/stage3_proofs_continue.log`.

An extra diagnostic selected `nonnegative-cube` alone and was manually
interrupted after 88 seconds. That filter removed `cube-loop` from the proof
set, forcing unbounded symbolic loop unrolling; it was not a required proof
configuration and is not treated as a candidate failure. The aggregate and
entry-plus-loop runs above are the meaningful independent reconstructions.

## 4. Adequacy and real-program pinning

### Plain-language form of each claim

- `cube-loop`: if the loop starts with `a=N^3`, `n=I`, and
  `0 <= I <= N`, it consumes the loop and ends with `n=N`.
- `nonnegative-cube`: for every `N>=0`, running the submitted program on
  `N^3` returns exactly `true`.
- `negative-cube`: for every `N>0`, running it on `-N^3` returns exactly
  `true`.
- `gap-loop`: if `a=N^3+D`, `n=I`,
  `0<=I<=N+1`, and `0<D<(N+1)^3-N^3`, the loop consumes and ends with
  `n=N+1`.
- `positive-noncube`: every positive value strictly between `N^3` and
  `(N+1)^3` returns exactly `false`.
- `negative-noncube`: the negative of every such gap value returns exactly
  `false`.

The entry postconditions rewrite the initially empty `<result>` cell to
`BoolVal(true)` or `BoolVal(false)`. The result is neither a free variable nor a
tautology; only final function/environment maps are existentially framed.

### Real program identity

Each entry `<k>` starts with
`iscubeProgram ~> invoke(IntVal(...))`. The sole `iscubeProgram` rule expands
to the complete `Module(FuncDef(...))` constructor tree. Comparing
`verification.k:11-24` with the trusted regenerated `solution.mpy` shows exact
constructor, operator, literal, statement-order, and nesting identity.
Expansion is followed by the ordinary MPY rules; it does not return a summary
or bypass the body.

I also compiled `verification.k` with LLVM and concretely executed the
`iscubeProgram` abbreviation on `8`, `-8`, `9`, and `-9`. The results were
respectively `true`, `true`, `false`, and `false`, matching actual
`solution.mpy`, Python candidate, and canonical execution. See
`evidence/stage4_pinning_llvm.log`.

### Satisfiable witnesses

Every claim precondition has a concrete satisfying state:

| Claim | Witness |
|---|---|
| `cube-loop` | `N=2, I=1, a=8, n=1` |
| `nonnegative-cube` | `N=2`, input `8` |
| `negative-cube` | `N=2`, input `-8` |
| `gap-loop` | `N=2, D=1, I=1, a=9, n=1` |
| `positive-noncube` | `N=2, D=1`, input `9` |
| `negative-noncube` | `N=2, D=1`, input `-9` |

For these entry witnesses, both Python implementations and generated-semantics
execution give `true,true,false,false`. The substitutions and concrete K
states are recorded in `evidence/stage4_witnesses.log` and the completed LLVM
pinning run above.

### Adequacy limitation

The four entry claims are universal over their `N,D` parameters, but the spec
does not contain a single arbitrary-`A` theorem or a formal K lemma proving
that these families exhaust all integers. Coverage follows informally from
strict monotonicity and discreteness of nonnegative integer cubes. That bridge
is mathematically standard and does not enable a false proof, but it remains
outside the machine-checked reachability claims.

## 5. Rule-by-rule static soundness review

The complete reviewer inventory is preserved in
`evidence/stage5_rule_inventory.md`. There are no helper K source files beyond
`semantic.k`, `verification.k`, and the claim-only `spec.k`.

### Local syntax and state inventory

`semantic.k` locally declares every one of the following:

- source constructors: `Module`, empty-separated `Stmts`, `Params`, `Int`,
  `Name`, `UnaryOp`, `BinOp`, `Compare`, `CmpOp`, `FuncDef`, `If`, `Assign`,
  `While`, and `Return`;
- values and stored functions: `IntVal`, `BoolVal`, `Value`, `KResult`,
  value-as-`Expr`, and `function`;
- internal controls: `exec`, `invoke`, `assignTo`, `ifKont`, `whileKont`,
  `compareKont`, and `returnKont`;
- configuration cells: `<k>`, `<funs>`, `<env>`, and `<result>` inside
  `<mpy>`.

`verification.k` adds `iscubeProgram` and the single `[function,total]`
symbol `cube(Int)`. There are no local `functional` declarations, priority
rules, opaque symbols, macros, or other `total` declarations.

### All 23 operational rules

| IDs | Rules and conclusion |
|---|---|
| S1–S3 (`semantic.k:60-62`) | Module scheduling, empty statement-list termination, and sequential statement execution are faithful. |
| S4–S5 (`64-69`) | The one submitted `FuncDef` is stored, then the configured one-argument `iscube` invocation reads that binding, installs the real body, and initializes `a`. No result is fabricated. |
| S6–S10 (`73-79`) | Integer literals, bound-name lookup, negation, addition, and multiplication are exact over K unbounded integers. |
| S11–S13 (`81-84`) | Comparison evaluates its RHS after the evaluated LHS and implements exact integer `<` and `==`. |
| S14–S15 (`87-89`) | Assignment evaluates the RHS and updates exactly the named local binding. |
| S16–S18 (`91-93`) | `if` evaluates its guard and selects exactly one branch. |
| S19–S21 (`95-97`) | `while` evaluates the guard, executes body then repeats on true, and exits on false. These rules return to the exact loop-head shape used by the invariant claims. |
| S22–S23 (`99-101`) | `return` evaluates the expression, writes its value to `<result>`, and discards the remaining single-function continuation. No other modeled observable cell is lost. |

The explicit rule heads are disjoint by constructor or Boolean value. Strict
evaluation contexts apply only until their selected operands are `KResult`, so
there is no value/context overlap. All reachable variable lookups are bound:
`a` is installed at invocation and `n` is assigned before the loop. Statement
state changes, the loop continuation, function return, and result cell all
match real control flow. There is no heap, allocation, I/O, call expression,
exception, or other state component in the submitted program.

`BinOp` is marked `[strict(2,3)]`, not `seqstrict`, so its comment's general
claim of Python left-to-right evaluation is too broad. Every operand in the
submitted program is a pure `Int`, `Name`, or nested arithmetic expression, and
the syntax supplies no used side-effecting expression. Therefore either strict
order has the same value and state on every intended execution. This is a
scope limitation, not a false conclusion witness for this program.

### Construct coverage

Every constructor used in `solution.mpy` maps to rules:

```text
Module→S1; lists→S2/S3; FuncDef/Params/invocation→S4/S5;
Int→S6; Name→S7; UnaryOp("-")→S8;
BinOp("+")→S9; BinOp("*")→S10;
Compare/CmpOp→S11-S13; Assign→S14/S15;
If→S16-S18; While→S19-S21; Return→S22/S23.
```

Unsupported unused strings or shapes visibly stick rather than silently
fabricating behavior, which is acceptable for a generated minimal semantics.

### All verification rules

1. `iscubeProgram => Module(...)` (`verification.k:11-24`) is a definitional
   expansion of the exact real program tree. It changes no cell and supplies
   no result.
2. `cube(I) => I*I*I` (`26-27`) is an unguarded, terminating, exhaustive
   definition over `Int`; its `[total]` declaration is justified.
3. The first gap simplification (`36-44`) rewrites `I < N+1` to `true` under
   guards including `I<=N+1`, `I^3<N^3+D`, and
   `D<(N+1)^3-N^3`. If its conclusion were false, `I=N+1`, making
   `I^3=(N+1)^3>N^3+D`, a contradiction.
4. The second gap simplification (`46-54`) rewrites `I==N+1` to `true` under
   `I<=N+1`, nonnegativity, `D>0`, and `I^3>=N^3+D`. If the conclusion were
   false, integer order gives `I<=N`; cube monotonicity then gives
   `I^3<=N^3<N^3+D`, a contradiction.

The two simplifications have different predicate heads, consistent
conclusions, complete explicit guards for their uses, and do not rewrite
program execution, state, or return values. The independent finite checker in
`evidence/gap_lemma_check.py` evaluated `N=0..100`, every in-gap `D`, and every
`I=0..N+1`: 78,552,750 first-rule guard hits and 1,030,200 second-rule guard
hits produced zero false conclusions. This finite evidence supports, but does
not replace, the universal mathematical arguments above.

No rule was found unsound, so there is no sound basis for supplying a false
conclusion witness against a candidate rule. Conversely, a reviewer mutation
changed the final real-program comparison from `==` to `<`; the rebuilt cube
proof failed with `WarnStuckClaimState` and a residual
`N^3 < N^3`. This confirms body sensitivity. See
`evidence/verification-body-mutant.k` and
`evidence/stage5_body_sensitivity.log`.

## 6. Fresh non-vacuity test

There was no candidate vacuity file to trust. I created
`evidence/spec-vacuity-review.k`, which runs the unmodified program on the
satisfying original witness `N=1`, input `1`, but changes the result obligation
from `BoolVal(true)` to `BoolVal(false)`.

The mutation's `kprove --dry-run` exited 0 with no stderr, establishing that it
parsed and built against the fresh proof definition. The actual proof exited 1
with `WarnStuckClaimState`. Its reachable residual has `<k>.K</k>`,
`a=1`, `n=1`, and `<result> BoolVal(true)`, which does not unify with the
mutated `BoolVal(false)` destination. This is the expected unmet result
obligation, not a parser error, missing import, timeout, unrelated crash, or
unreachable mutation.

`evidence/stage6_nonvacuity_rerun.log` records `NONVACUITY=PASS`. The earlier
`evidence/stage6_nonvacuity.log` contains the same successful dry run and
expected stuck proof, but its reviewer shell predicate incorrectly also
required the destination `BoolVal(false)` to be repeated in the backend
residual; that bookkeeping bug was corrected without changing the mutation or
proof outcome.

## 7. Proven versus assumed accounting

### What the reachability proof establishes

Under the compiled MPY theory, as a partial-correctness result:

- for every `N>=0`, terminating execution on `N^3` returns exactly `true`;
- for every `N>0`, terminating execution on `-N^3` returns exactly `true`;
- for every `N>=0` and `0<D<(N+1)^3-N^3`, terminating execution on either
  sign of `N^3+D` returns exactly `false`;
- the actual loops reach `n=N` in the cube family and `n=N+1` in the gap
  family from the stated invariant states.

The program body executes under the small-step semantics. There is no opaque
program-derived value, oracle result, loop shortcut, assumed source helper, or
one-way implication standing in for the final Boolean.

### Trust and assumption ledger

| Boundary | Dependents | Accounting |
|---|---|---|
| K's built-in `Int`, `Bool`, `Map`, K sequence, strictness machinery, parser, Haskell backend, prover, and SMT integration | All concrete and symbolic results | Ordinary low-level K/toolchain trust boundary; no candidate-specific answer is encoded there. |
| Trusted `py2mpy.py` translation | Program-tree identity | Mounted trusted input; fresh byte-identical translation recorded. |
| Generated MPY semantics as a model of the used Python subset | All program-execution claims | Audited rule by rule. It is intentionally incomplete outside used constructs. Unbounded K integers match Python integers for all used arithmetic; used operations raise no Python exceptions. |
| `iscubeProgram` source-tree abbreviation | All four entry claims | Exact definitional copy of regenerated `solution.mpy`; concrete pinning and a rejected body mutation provide independent sensitivity evidence. |
| `cube` function equation | All claims | Total exact definition, not opaque. |
| Two gap simplifications | Gap loop and non-cube claims | Proof-local derived arithmetic lemmas; universally justified above and finitely stress-checked. |
| Integer-family exhaustiveness | Bridge from four entry families to “iff cube” for arbitrary integer | Informal ordinary mathematics, not a K claim. This is the principal theorem-scope concern. |
| Candidate/canonical alignment | Natural-language/reference bridge | Finite differential evidence for 109,681 inputs. Universal alignment is excluded by the documented large-cube canonical precision failures. |
| Termination for every integer | Total-correctness interpretation | Not established by this partial-correctness audit. The loop's mathematical termination is plausible but outside the claimed proof status. |

### Gates and final rationale

- Real-program soundness: **PASS**. Exact program tree, all bodies execute,
  every proof-local rule is valid, witnesses are satisfiable, body sensitivity
  holds, and the false-result mutation is rejected.
- Intent adequacy: **PASS WITH CONCERNS**. The four families match the exact
  mathematical cube predicate via an informal partition argument, but there is
  no single machine-checked arbitrary-input `iff` theorem. The trusted
  canonical is itself inexact for some very large cubes.
- Evidence auditability: **PASS**. Fresh commands, source mutations, inputs,
  statuses, and bounded outputs are preserved under `evidence/`; finite tests
  are not represented as universal proofs.

These limitations narrow how the proof should be stated but do not make any
proved reachability claim false or allow a false result to be proved.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
