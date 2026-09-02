# Independent adversarial review: 13-greatest-common-divisor

## Decision

The candidate contains a legitimate, result-constraining partial-correctness
proof of the exact submitted `solution.mpy` program under its generated MPY
semantics. Both candidate target claims reconstruct from source, and a fresh
off-by-one result claim is rejected for the expected unmet obligation.

The result is qualified rather than an unqualified pass for two intent-bridge
reasons:

1. The submitted implementation deliberately returns the nonnegative
   mathematical GCD, but the trusted canonical implementation returns a negative
   value on many signed inputs. The independent differential found 1,334 such
   divergences among 2,687 inputs, including `(25, -15)`, for which the submitted
   program returns `5` and the canonical returns `-5`.
2. K proves equality with the candidate's Euclidean `gcdSpec`; the final bridge
   from those Euclidean equations to the phrase “greatest common divisor” is
   ordinary mathematics plus finite `math.gcd` evidence, not a K theorem about
   divisibility and greatestness.

Neither limitation makes a false result provable about the submitted program.

Toolchain: K v7.1.293. Exact tool locations and versions are recorded in
[`evidence/00-toolchain.log`](evidence/00-toolchain.log).

## Stage 1 — Input and provenance integrity

### Mode boundary

The rendered mode is `GENERATED_SEMANTICS`. `/reference/reference-semantics`
does not exist and is not a symlink, so the trusted mounts do not contradict the
rendered mode. This audit therefore evaluates the candidate's own `semantic.k`;
it does not infer or use any hidden reference semantics.

### Required artifacts and trusted comparisons

All checked source and metadata artifacts are regular files, not symlinks:
`run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`,
`prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`, `semantic.k`,
`gcd-spec.k`, `loop-spec.k`, `loop-verification.k`, `verification.k`, `spec.k`,
`prove.sh`, and the structured JSONL trace. No required checked artifact is
missing or mistyped.

Candidate `prompt.py` is byte-identical to `/reference/prompt.py` (SHA-256
`a7946546…60c19`), and candidate `py2mpy.py` is byte-identical to
`/reference/py2mpy.py` (SHA-256 `406485ea…db16`). The exact checks, all source
hashes, candidate top-level inventory, and an empty symlink inventory are in
[`evidence/01-provenance.log`](evidence/01-provenance.log).

The top-level extras are untrusted generated material, not trusted inputs:
`NOTES.md`, `__pycache__/`, `gcd-spec-kompiled/`, `loop-kompiled/`,
`semantic-kompiled/`, `semantic-llvm-kompiled/`, and
`verification-kompiled/`. They were not copied into or used by any fresh build.
The candidate has no `PROOF.md` and supplied no `spec-vacuity.k`; those are
evidence/documentation omissions, not substitutions for the source claims.

### Untrusted generation claims

`run-input.json` identifies problem `13-greatest-common-divisor`, condition
`bare`, and hashes consistent with the trusted prompt and translator.
`metrics.json` claims generation exit 0 without timeout. `codex-last.txt` and
`codex-output.log` claim four concrete checks and two successful `kprove`
commands. These claims were not accepted as proof evidence.

The complete 388-line structured trace was independently deserialized with no
invalid JSON lines; it contains both failed proof-development attempts and later
claimed `#Top` outputs. The bounded summary is
[`evidence/01-trace-summary.log`](evidence/01-trace-summary.log), produced by
[`evidence/trace_summary.py`](evidence/trace_summary.py). The full
`codex-output.log` and trace were hashed and scanned; their claimed successes
were superseded by Stage 3's clean reconstruction.

**Stage 1 result: PASS.** There is no infrastructure breach and no source
provenance integrity failure.

## Stage 2 — Program fidelity and candidate-versus-canonical checks

### Contract and implementations

The trusted prompt asks
`greatest_common_divisor(a: int, b: int) -> int` to return a greatest common
divisor of two integers, with examples `(3,5) -> 1` and `(25,15) -> 5`.

The trusted canonical program is the usual two-variable Euclidean loop:
while `b` is truthy, set `(a,b) = (b,a % b)`, then return `a`. The submitted
program first replaces negative inputs by their negations, initializes `r = 0`,
and runs the equivalent three-assignment Euclidean loop. For Python integers it
therefore returns the conventional nonnegative GCD, including `0` for `(0,0)`.

Running the trusted translator on the scratch copy of `solution.py` produced
SHA-256 `7f5ef56c…84b96`, exactly the submitted `solution.mpy` bytes. Command,
status 0, and both hashes are in
[`evidence/02-translation.log`](evidence/02-translation.log); the reproducible
check is [`evidence/translation_check.sh`](evidence/translation_check.sh).

### Independent differential

[`evidence/differential_test.py`](evidence/differential_test.py) separately
imports `/reference/canonical.py` and the scratch copy of the generated
`solution.py`. Its deterministic scope is:

- both documented examples;
- zero/empty-loop cases `(0,0)`, `(0,1)`, and `(1,0)`;
- each sign-test and loop-test branch boundary around `-1`, `0`, and `1`;
- representative large values;
- every pair in `[-20,20] × [-20,20]`; and
- 1,000 random pairs in `[-10^12,10^12]²`, seed `130013`.

There is no collection-valued “empty” input for this scalar signature; `(0,0)`
is the empty-loop analogue. Across 2,687 unique inputs:

- submitted program versus `math.gcd`: 0 mismatches;
- submitted program versus trusted canonical: 1,334 mismatches;
- trusted canonical versus `math.gcd`: the same 1,334 mismatches.

The test intentionally exits 1 when any candidate/canonical divergence exists.
Inputs, explicit results, mismatch count, first witnesses, command, and status
are in [`evidence/02-differential.log`](evidence/02-differential.log).

The divergence is systematic: the canonical returns a negative GCD when its
active divisor is negative and preserves a negative `a` when `b == 0`; the
submitted program normalizes signs. The submitted behavior agrees with the
ordinary nonnegative mathematical reading of “greatest,” but not with the
trusted canonical on the full annotated integer domain. This is an intent
qualification, not a proof substitution.

**Stage 2 result: CONCERN.** Program/MPY fidelity passes; canonical behavioral
fidelity does not pass for signed inputs.

## Stage 3 — Clean proof reconstruction

All candidate source needed for execution was copied to
`/tmp/audit-work/source`. Candidate kompiled directories, caches, and bytecode
were ignored. [`evidence/03-scratch-source-integrity.log`](evidence/03-scratch-source-integrity.log)
shows byte identity between every copied candidate proof/program source and its
scratch copy.

### Generated-semantics execution

The concrete definition was freshly built from `semantic.k`:

```text
kompile semantic.k --main-module MPY --syntax-module MPY-SYNTAX \
  --backend llvm \
  --output-definition /tmp/audit-work/build/semantic-llvm-kompiled
```

It exited 0; see
[`evidence/03-build-semantic-llvm.log`](evidence/03-build-semantic-llvm.log).
Fresh `krun` execution was compared with both submitted Python and `math.gcd` on
13 normal, zero, sign, boundary, large, and multi-iteration inputs. All three
results agreed. The script and complete results are
[`evidence/semantics_differential.sh`](evidence/semantics_differential.sh) and
[`evidence/03-semantic-differential.log`](evidence/03-semantic-differential.log).
Full final configurations for `(25,15)`, `(0,0)`, and `(25,-15)` are preserved
in the three `03-krun-*.log` files; all have `.K`, `b = 0`, `r = 0`, and the
expected result.

### Positive target claims

The fixed-semantics loop definition was freshly compiled with the Haskell
backend. The candidate loop claim was then selected explicitly:

```text
kprove loop-spec.k \
  --definition /tmp/audit-work/build/loop-kompiled \
  --spec-module LOOP-SPEC
```

It exited 0 and printed exactly `#Top`. Build and proof records:
[`evidence/03-build-loop-haskell.log`](evidence/03-build-loop-haskell.log) and
[`evidence/03-kprove-loop.log`](evidence/03-kprove-loop.log).

The verification definition, now including the discharged loop summary as a
rule, was independently compiled. The entry claim was selected explicitly:

```text
kprove spec.k \
  --definition /tmp/audit-work/build/verification-kompiled \
  --spec-module SPEC
```

It exited 0 and printed exactly `#Top`. Build and proof records:
[`evidence/03-build-verification-haskell.log`](evidence/03-build-verification-haskell.log)
and [`evidence/03-kprove-entry.log`](evidence/03-kprove-entry.log).

No candidate-built definition contributed to either result.

**Stage 3 result: PASS.**

## Stage 4 — Adequacy and real-program pinning

### Claims in plain language

The loop claim has precondition:

- control is exactly the submitted Euclidean `while b != 0` statement;
- the environment is exactly `a ↦ A, b ↦ B, r ↦ R0`; and
- `A >= 0` and `B >= 0`.

Its postcondition says the loop is gone, `a` is `gcdSpec(A,B)`, `b` is `0`, and
`r` is `R0` if the loop took zero iterations and `0` otherwise (encoded by
`finalR(B,R0)`). A satisfying witness is `A=25, B=15, R0=0`; the fixed semantics
reaches `a=5,b=0,r=0`. The zero-iteration witness `A=7,B=0,R0=9` reaches
`a=7,b=0,r=9`, exactly `finalR(0,9)`.

The entry claim has no `requires` clause: every K `Int` pair `A,B` is admitted.
Its initial state contains the literal submitted MPY function, empty
environment, `inputA=A`, `inputB=B`, and `noResult`. Its postcondition requires:

- empty `<k>`;
- `a = gcdSpec(normInt(A),normInt(B))`, `b = 0`, and `r = 0`;
- unchanged input cells; and
- `result(gcdSpec(normInt(A),normInt(B)))`.

Thus the result is neither free nor merely implied one way. For `A=25,B=15`,
the formal result, submitted Python, canonical Python, and concrete K execution
are all `5`. For the also-satisfying `A=25,B=-15`, the formal result, submitted
Python, and concrete K execution are `5`, while canonical Python is `-5`; this
is the Stage 2 intent discrepancy, not a weakening of the K postcondition.

### Exact program and control-flow pinning

The `<k>` left-hand side in `spec.k` is a statement-for-statement literal copy
of the 14-line submitted `solution.mpy`: both sign-normalizing `If`s, `r = 0`,
the exact three-assignment loop body, and `Return(a)`. The trusted regeneration
is byte-identical, so the claim does not prove a substituted algorithm.

The verification bridge matches only that exact loop body and the exact local
keys. To check the candidate's broader continuation frame, the reviewer created
[`evidence/loop-frame-spec.k`](evidence/loop-frame-spec.k), which universally
quantifies `REST:K` and proves the loop transitions to the same summarized
environment followed by `REST`. It closes with exit 0 and `#Top` against the
fixed loop definition:
[`evidence/04-kprove-loop-frame.log`](evidence/04-kprove-loop-frame.log).

A concrete continuation that assigns `a = 42` after the loop produces the same
complete final configuration under the fixed and bridge-enabled definitions,
including `result(42)`; see
[`evidence/04-bridge-fixed.log`](evidence/04-bridge-fixed.log) and
[`evidence/04-bridge-extended.log`](evidence/04-bridge-extended.log).
A body mutation changing `r = a % b` to `r = 0` does not match the bridge:
both definitions execute it and return `15` for `(25,15)`, rather than the
original `5`. See the two `04-body-mutation-*.log` files and
[`evidence/bridge-body-mutation.mpy`](evidence/bridge-body-mutation.mpy).

**Stage 4 result: PASS.** The theorem is result-constraining and pins the real
translated program.

## Stage 5 — Rule-by-rule static soundness review

The line-numbered source and declaration/rule index are preserved in
[`evidence/05-rule-inventory.log`](evidence/05-rule-inventory.log).

### Local syntax, configuration, and attributes

`MPY-SYNTAX` declares:

- `Pgm = Module(Stmts)` and an ordered, separator-free `Stmts` list;
- five statement constructors: `FuncDef`, `If`, `While`, `Assign`, `Return`;
- `Params` and a comma-separated `Strings` list;
- five expression constructors: `Int`, `Name`, `UnaryOp`, `BinOp`, `Compare`;
  and
- `CmpOp(String,Expr)`.

`MPY` adds `Result = noResult | result(Int)`, the
`<gcd-program>` configuration (`k`, `env`, two input cells, and result), and
internal `execStmts`/`execStmt` items. `evalInt` and `evalBool` are local
`[function]` symbols, not declared total.

`GCD-SPEC` declares `gcdSpec`, `finalR`, and `normInt` as
`[function,total]`. There are no local `[functional]`, `owise`, `anywhere`,
macro, alias, or trusted-opaque declarations. The only local priority is the
loop bridge's `[priority(40)]`. Symbolic `gcdSpec` is intentionally left as a
summary term, but all ground uses in the claimed domain are fixed by descending
Euclidean equations; it is not an unconstrained program-result oracle.

Every constructor used by `solution.mpy` maps to the declarations above and to
the rules below. No used construct is fabricated or left unmodeled.

### `semantic.k` operational rules

| ID | Rule | Static decision |
|---|---|---|
| S1 | `evalInt(Int(I),ENV) => I` | Sound literal evaluation. |
| S2 | `evalInt(Name(X),(X↦I) REST) => I` | Sound unique Map lookup for all reachable names. |
| S3 | unary `"-"` becomes `0 -Int value` | Sound for unbounded Python/K integers. |
| S4 | binary `"%"` becomes `%Int` | Sound on every reachable use: after normalization both operands are nonnegative and the divisor is nonzero. K `%Int` is truncating while Python `%` is floored for mixed signs, so this syntax rule is not a reusable full-Python model for negative divisors; no such state is reachable in the submitted loop. Builtin details: [`evidence/05-k-builtin-modulo.log`](evidence/05-k-builtin-modulo.log). |
| S5 | comparison `"<"` | Sound integer comparison. |
| S6 | comparison `"!="` | Sound integer inequality. |
| S7 | exact named `Module(FuncDef(...))` initializes parameters from input cells | Sound entry harness for the sole submitted function; it does not compute or assume the answer. |
| S8 | `execStmts(.Stmts) => .K` | Sound sequence base case. |
| S9 | `execStmts(S SS) => execStmt(S) ~> execStmts(SS)` | Preserves source statement order. |
| S10 | assignment updates Map with the old-environment expression value | Sound for the submitted pure expressions and Python assignment order. |
| S11 | true `If` selects `THEN` | Sound when `evalBool` is defined. |
| S12 | false `If` selects `ELSE` | Complementary to S11; guards are disjoint and exhaustive on used comparisons. |
| S13 | true `While` executes body then recurs | Standard while control flow and correct sequencing. |
| S14 | false `While` removes the loop | Complementary to S13. |
| S15 | `Return(E)` discards the remaining continuation and sets `result` | Correct abrupt return for the sole reachable return; input cells and environment are preserved. |

Expression evaluation is implemented as pure K functions rather than explicit
left-to-right control. That is observationally sound for this program because
its expressions have no calls, mutation, I/O, or reachable exceptional
subexpression; `%` is only evaluated after `b != 0`. Map update preserves all
bindings. No heap, allocation, call stack, exception, or I/O cell is needed by
the submitted program.

### `gcd-spec.k` functions and simplifications

| ID | Rule | Attributes and static decision |
|---|---|---|
| G1 | `gcdSpec(A,0) => A` if `A>=0` | Sound Euclidean base equation. |
| G2 | `gcdSpec(A,B) => gcdSpec(B,A %Int B)` if `A>=0,B>0` | `[simplification,concrete]`; sound, ground-terminating because `0 <= A%B < B`. |
| G3 | `normInt(A) => 0-A` if `A<0` | Sound absolute-value negative branch. |
| G4 | `normInt(A) => A` if `A>=0` | Disjoint and exhaustive with G3. |
| G5 | `finalR(R,R) => 0` | `[simplification]`; at recursive entries `r` equals current `b`, so a terminating nonzero-start loop ends with `r=0`. |
| G6 | `finalR(B,0) => 0` | `[simplification]`; sound and overlap-compatible. |
| G7 | `finalR(0,R) => R` | Sound zero-iteration case. |
| G8 | `finalR(B,R) => 0` if `B != 0` | Sound nonzero-start case and completes coverage. |
| G9 | `{gcdSpec(A,0) #Equals A} => #Top` if `A>=0` | `[simplification]`; true base equality. |
| G10 | symmetric base equality | `[simplification]`; same true equation. |
| G11 | `{gcdSpec(A,B) #Equals gcdSpec(B,R)} => #Top` when `R=A%B`, `A>=0,B>0` | `[simplification]`; true Euclidean equality. |
| G12 | symmetric recursive equality | `[simplification]`; same true equation. |

The G5–G8 overlaps all agree: every overlap with second argument `0` yields
`0`; `finalR(R,R)` with nonzero `R` agrees with G8; and G7/G8 have disjoint
first-argument guards. G1/G2 have disjoint `B=0` and `B>0` guards on their
nonnegative domain. G9–G12 only replace true equalities with `#Top`; symmetric
overlaps have the same right-hand side.

`normInt` and `finalR` have complete, disjoint-or-agreeing coverage.
`gcdSpec` has executable coverage for all nonnegative ground pairs and descends
there, which is every occurrence reachable from the entry and loop claims.
Its `[total]` declaration is broader than its equations for negative arguments:
such terms remain an under-specified reuse boundary. No negative `gcdSpec`
argument can affect a branch, state, or postcondition here, so this is a narrow
coverage limitation rather than a false rule or oracle witness.

### `verification.k` operational bridge and claims

V1 is the sole added operational rule. It matches the exact Euclidean loop and
exact `a,b,r` environment, requires nonnegative `A,B`, preserves the arbitrary
`<k>` suffix and all omitted cells, and writes precisely the environment proved
by the fixed-semantics loop claim. `[priority(40)]` lets it preempt loop
unrolling, but does not supply its correctness. Correctness is supplied by:

- the reconstructed candidate loop theorem (`#Top`);
- the stronger reviewer-authored arbitrary-`REST:K` theorem (`#Top`);
- matching fixed/extended continuation configurations; and
- rejection-by-nonmatch of the body mutation.

The bridge introduces no return, frame pop, exception, fresh value, or hidden
state change. `gcdSpec` is not introduced as a free value: its ground result is
fixed by G1/G2, and its symbolic induction step is G11/G12.

`loop-verification.k` contains imports only. `loop-spec.k` contains the one
loop claim described in Stage 4. `spec.k` contains the one exact entry claim.
There are no additional helper claims, priority rules, opaque symbols, or
proof-local rewrites.

No inventoried rule permits a concrete false conclusion on the submitted
program's intended integer domain. Accordingly, no rule is labeled unsound.
The two narrower evidence limitations are the non-reusable negative-divisor
meaning of S4 and negative-argument totality coverage of `gcdSpec`; neither is
reachable in or used to prove the entry theorem.

**Stage 5 result: PASS with documented reuse limitations.**

## Stage 6 — Fresh non-vacuity test

The reviewer-authored mutation
[`evidence/spec-vacuity-review.k`](evidence/spec-vacuity-review.k) preserves the
exact program, environment postcondition, and proof definition, but changes the
result obligation to:

```text
result(gcdSpec(normInt(A),normInt(B)) +Int 1)
```

It is demonstrably false for the satisfying input `(3,5)`: the real and formal
result is `1`, while the mutation requires `2`.

The dry run successfully generated the backend command and exited 0:
[`evidence/06-vacuity-dry-run.log`](evidence/06-vacuity-dry-run.log). The actual
proof exited 1 with `WarnStuckClaimState`. Its residual contains the reached
real result `result(gcdSpec(A,B))` and the unmet condition
`gcdSpec(A,B) +Int 1 #Equals gcdSpec(A,B)`. It was not a parser error, missing
import, timeout, unrelated crash, or unreachable mutation:
[`evidence/06-vacuity-proof.log`](evidence/06-vacuity-proof.log).

**Stage 6 result: PASS.**

## Stage 7 — Proven versus assumed accounting

### What the reachability proof establishes

Under the submitted MPY semantics and imported K builtins, for every K integer
pair `A,B`, any terminating execution of the exact submitted translated
function from the configured entry state reaches empty control with:

```text
result = gcdSpec(normInt(A), normInt(B))
a      = gcdSpec(normInt(A), normInt(B))
b      = 0
r      = 0
```

The loop summary itself is proved against the unextended fixed semantics for
all nonnegative `A,B` and arbitrary initial `r`, and the reviewer additionally
proved it with an arbitrary continuation. This is partial correctness. It is
not a separate K termination proof, although concrete tests terminate and the
Euclidean descent gives the usual informal termination argument.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K v7.1.293 parser, Haskell/LLVM backends, and reachability implementation | All builds, `krun`, and `kprove` results | Necessary low-level trusted computing base; versions and exact commands are recorded. |
| Imported `INT`, `BOOL`, and `MAP` hooks and simplifications | Arithmetic, guards, environment, Euclidean descent | Acceptable standard K primitives. `%Int` is truncating; nonnegative reachable operands make it coincide with Python and Euclidean remainder. |
| Trusted `py2mpy.py` translation from Python AST to MPY | Identity between `solution.py`, `solution.mpy`, and the literal claim | Trusted input plus byte-identity reconstruction. No separate semantic-preservation theorem is supplied. |
| Generated entry harness interpreting the sole `FuncDef` using input cells | Connection from configured `A,B` to function locals | Acceptable minimal generated-language boundary for this pure single-function task; it executes the body and assumes no result. It does not model the general Python call stack. |
| Candidate MPY operational rules | Meaning of the translated program | Audited rule-by-rule and concretely differential-tested. Coverage is deliberately only the used subset. |
| `gcdSpec` Euclidean equations and equality simplifications | Loop and entry postconditions | Truthful mathematical definition on all nonnegative claimed arguments; not an opaque program-result oracle. Negative-argument reuse is under-specified but irrelevant to all dependents here. |
| Informal theorem that the Euclidean equations denote the nonnegative greatest common divisor | Bridge from K postcondition to prompt phrase | Mathematically standard and supported by 2,687 zero-mismatch comparisons with `math.gcd`, but not formalized in K as divisibility/greatestness. This causes a concern rather than illegitimacy. |
| Trusted canonical behavior | Candidate-to-reference fidelity | Material signed-input mismatch remains visible. The candidate matches the ordinary nonnegative GCD reading; it does not duplicate canonical signed behavior. |
| Termination of the submitted Euclidean loop | Total correctness only | Outside this partial-correctness theorem. Informal descent is straightforward after normalization. |

There is no fresh/opaque symbol whose unconstrained interpretation can change
the program result. `finalR` is fully equational; `normInt` is fully
equational; `gcdSpec` is ground-executable over every claimed argument. The
off-by-one mutation confirms that the proof cannot accept an opposite result.

Finite Python/K differential tests support only translator/semantics/intent
bridges on their documented inputs. They do not replace either reconstructed K
claim.

Gate accounting:

- Real-program soundness: **PASS**.
- Intent adequacy: **LIMITED** by the canonical signed-input discrepancy and
  informal Euclidean-spec-to-greatestness bridge.
- Evidence auditability: **PASS**; all reviewer scripts, inputs, exact commands,
  statuses, and bounded outputs are under `evidence/`.

The earliest limitation is intent adequacy, not proof soundness. The appropriate
pairing is therefore concerns with legitimacy.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
