# Independent adversarial review: 76-is-simple-power

The candidate reconstructs and proves a non-vacuous theorem about its submitted
rewrite, but it does not prove the HumanEval contract implemented by the trusted
canonical program.  The decisive witness is `x = 4, n = -2`: `(-2) ** 2 = 4`,
the trusted canonical returns `True`, and both the submitted Python and its K
semantics return `False`.  The formal predicate deliberately rejects every
`n < 2` when `x > 1`.  This is a material source-contract discrepancy, so the
benchmark's special decision rule maps the otherwise sound-but-limited theorem
to `FAIL / NOT_LEGIT`.

All candidate prose, prior logs, generated caches, and the supplied
`kore-exec.tar.gz` were treated only as untrusted evidence.  All execution below
used source copied to `/tmp/audit-work/76-is-simple-power`; no candidate-built
definition or cache was reused.

## 1. Input and provenance integrity

Status: **PASS; no infrastructure breach**.

`/audit-input.json` declares:

- problem `76-is-simple-power`;
- condition `bare`;
- record layout `legacy-selected-stage1`;
- semantics mode `GENERATED_SEMANTICS`;
- no mounted reference semantics.

I read and checked `/audit-input.json`, `/audit-campaign-lock.json`,
`/run.json`, `/task.json`, `/generation-result.json`, and all records required
for `legacy-selected-stage1`: `invocation.json`, `metrics.json`,
`codex-last.txt`, `codex-output.log`, `prompt.txt`, the structured trace, and
the present `usage.json`.  Historical runtime metrics are not required for this
layout and were not reconstructed.

The independent checker and complete bounded result are
`evidence/01_integrity.py` and `evidence/01_integrity.log`.  Its findings were:

- Every required record is a readable regular file, every required directory
  is a real directory, and no required entry or candidate entry is a symlink.
- The campaign block exactly equals `/audit-campaign-lock.json`.  Its mounted
  SHA-256 is
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  exactly the recorded value.
- Every recorded single-file SHA-256 checked by the script matches, including
  the run/task/result manifests, invocation/metrics/usage records, prompt,
  translator, canonical, final generation message, full generation log, and
  trace JSONL file.
- The independently recomputed pipeline tree hash of `/candidate` is
  `633d577f29d0b6630cebc81345674517d577cc8d77879f2b862ffbf740f4dc13`,
  matching both `invocation.json`'s retained-workspace hash and
  `generation-result.json`'s workspace hash.
- The structured trace contains one regular JSONL file with 287 valid JSON
  events and no parse errors.  Its independently recomputed pipeline tree hash
  is `068721950d14ced5ceab22a0e00084be897da76018e4576bf6f354f20019edd3`,
  matching `usage.json`'s source-trace hash.  The trace file's own SHA-256 also
  matches `invocation.json`.
- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`, and
  `/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`.
- Neither `/reference/reference-semantics` nor
  `/candidate/reference-semantics` exists.  This is exactly the required
  boundary for `GENERATED_SEMANTICS`.

The generation records claim `KPROVE_PASSED`, but that claim was not used as
proof evidence.

## 2. Program fidelity and candidate-versus-canonical checks

Status: **FAIL**.

### Contract and implementations

The trusted prompt says to return true exactly when `x` is a simple power of
`n`, expressed as `n**int = x`.  The example `is_simple_power(1, 4) => true`
shows that exponent zero is included.  The prompt places no positivity
restriction on `n`.

The trusted canonical starts at `power = 1`, repeatedly multiplies by `n` while
`power < x`, and returns whether the resulting value equals `x` (with a special
case for `n == 1`).  On terminating negative-base cases it therefore recognizes
even powers such as `(-2) ** 2 = 4`.

The submitted `/candidate/solution.py` instead:

1. returns true for `x == 1`;
2. returns false for `x < 1`;
3. returns false for every `n < 2`;
4. otherwise starts at `power = n`, multiplies until `power >= x`, and tests
   equality.

Step 3 is not faithful to the unrestricted source contract or the trusted
canonical.

### Translator identity

The exact command was:

```sh
python3 /reference/py2mpy.py \
  /tmp/audit-work/76-is-simple-power/solution.py \
  > /tmp/audit-work/76-is-simple-power/solution.regenerated.mpy
cmp -s /tmp/audit-work/76-is-simple-power/solution.regenerated.mpy \
  /tmp/audit-work/76-is-simple-power/solution.mpy
```

`cmp` exited 0.  Both files have SHA-256
`94eb9a3860bd9ccff041c57b307fda0db8e2bfbff67c3f508d2d9c09a343a5ed`.
See `evidence/02_translation_identity.log`.

### Independent differential test

`evidence/02_differential.py` imports the trusted canonical directly from
`/reference/canonical.py` and the scratch copy of the submitted implementation.
It covers all six documented examples, every submitted branch boundary,
zero/one/multiple loop iterations, exact hits and overshoots, selected larger
cases, five floating-number cases, and a generated grid containing every
integer `x` from -8 through 64 and bases
`{-5,-4,-3,-2,1,2,3,4,5,6,7,8}`.  There is no empty-container case because both
inputs are scalar numbers.  Two potentially nonterminating canonical cases
were isolated in bounded subprocesses.

Exact command:

```sh
python3 /audit-output/evidence/02_differential.py
```

It exited 0 as a test recorder, compared 886 unique terminating cases, and
reported eight result mismatches:

```text
(4, -2), (16, -2), (4096, -2), (9, -3),
(16, -4), (25, -5), (64, -2), and (2.25, 1.5)
```

In every mismatch the trusted canonical returned `True` and the generated
implementation returned `False`.  The first witness alone is decisive and uses
only integers.  The bounded canonical probes `(2, 0)` and `(2, -1)` timed out
while the generated function returned false; those timeouts are recorded but
are not used as candidate defects.  Full results are in
`evidence/02_differential.log`.

The Int-only K configuration also excludes floating values even where both
Python programs agree, such as `(x,n) = (6.25,2.5)`.  That is a secondary scope
limitation; the negative-integer mismatch already establishes failure without
depending on how broadly “number” is interpreted.

## 3. Clean proof reconstruction

Status: **PASS for the candidate's own theorem**.

The candidate's `build/`, bytecode cache, and `kore-exec.tar.gz` were not copied
or used.  Fresh definitions were built from the copied `.k` sources.

Concrete definition:

```sh
kompile semantic.k --backend llvm \
  --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition fresh-semantic-kompiled
```

Exit 0; see `evidence/03_build_concrete.log`.

Proof definition:

```sh
kompile verification.k --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition fresh-verification-kompiled
```

Exit 0; see `evidence/03_build_proof.log`.  The live toolchain reported K
version 7.1.293.

Every positive claim was then selected and run independently with:

```sh
kprove spec.k --definition fresh-verification-kompiled \
  --claims SPEC.<label>
```

| Claim label | Output | Exit |
|---|---:|---:|
| `emitted-tree-is-shared-tree` | `#Top` (also `WarnTrivialClaim`) | 0 |
| `returns-on-one` | `#Top` | 0 |
| `rejects-below-one` | `#Top` | 0 |
| `rejects-small-base` | `#Top` | 0 |
| `active-path-enters-loop` | `#Top` | 0 |
| `loop-correct` | `#Top` | 0 |

The exact expanded commands, outputs, and individual statuses are in
`evidence/03_run_positive_claims.sh` and
`evidence/03_positive_claims.log`.

For generated-semantics validation, `evidence/03_concrete_compare.py` ran the
fresh LLVM definition on 12 normal and boundary inputs.  Every command had the
form:

```sh
krun solution.mpy -cX=<x> -cN=<n> \
  --definition fresh-semantic-kompiled
```

All 12 K executions exited 0 and matched the submitted Python result.  They
exercised both outcomes of every `If`, the `x==1`, `x<1`, and `n<2` boundaries,
zero/one/multiple `While` iterations, exact hits, overshoots, assignment,
multiplication, and both Boolean literals.  As expected from Stage 2, the K
result at `(4,-2)` was false, matching the submitted rewrite but not the trusted
canonical.  The full configurations and comparisons are in
`evidence/03_concrete_compare.log`.

## 4. Adequacy and real-program pinning

Status: **program pinning PASS; intent adequacy FAIL**.

### Claim meanings and satisfiable witnesses

| Claim | Plain-language precondition | Plain-language postcondition | Satisfying witness |
|---|---|---|---|
| `emitted-tree-is-shared-tree` | No guard; empty environment and `noResult` | The literal constructor tree equals the proof abbreviation `solutionProgram`; it asserts no return value | `<x>=0`, `<n>=0` |
| `returns-on-one` | `x=1`, any integer `n` | Execute the submitted module to `.K`, preserve `x,n`, and return `simplePowerSpec(1,n)` (true) | `x=1,n=-2` |
| `rejects-below-one` | `x<1`, any integer `n` | Execute to `.K` and return `simplePowerSpec(x,n)` (false) | `x=0,n=2` |
| `rejects-small-base` | `x>1` and `n<2` | Execute to `.K` and return `simplePowerSpec(x,n)` (false) | `x=4,n=-2` |
| `active-path-enters-loop` | `x>1` and `n>=2` | Execute the real prefix to the actual loop head, with `power=n`; this is an intermediate, not a result claim | `x=8,n=2` |
| `loop-correct` | `x>1`, `n>=2`, `power=P>0` | Execute the actual loop and following return; finish with `power=powerCeiling(P,x,n)` and return whether that value equals `x` | `x=8,n=2,P=2` |

`evidence/04_pinning_and_witnesses.py` evaluates these substitutions.  For the
loop witness, the claimed final power is 8 and both Python implementations
return true.  For the small-base witness, the claimed/submitted result is false
but the trusted canonical result is true.

The active-path claim's destination exactly satisfies the loop claim with
`P=N`; its guard implies `P>0`.  Reachability transitivity plus the defining
equation for `simplePowerSpec` composes the two claims into the submitted
active-path result.  This composition is mathematically valid, although the
candidate did not include one final entry-to-result claim for that partition.

### Mechanical pinning

Pinning is supported by three independent checks:

1. Trusted translator regeneration is byte-identical to `solution.mpy`
   (Stage 2).
2. `evidence/04_pinning_and_witnesses.py` extracts the actual right-hand side
   of `verification.k`'s `solutionProgram` equation.  It applies only the
   demonstrated empty-list normalization (`.Stmts` in K versus no characters
   in external `.mpy` syntax), parses both terms with `kast`, and compares the
   constructor JSON.  Both parses exited 0, the terms were identical, and both
   canonical constructor hashes were
   `8f1f94e7e88d93c7e8bfe1d9c4c40d14cc55144bdeb420cb3b829a62a31d5720`.
3. A separate body-sensitivity mutation changed the `Return(Bool(true))` term
   in the *executed* `solutionProgram` equation to
   `Return(Bool(false))`, rather than changing an external unused source file.
   The mutated definition built successfully, and the unchanged
   `returns-on-one` claim exited 1 with `WarnStuckClaimState`; its residual
   contained `<result>false</result>`.  See
   `evidence/04_body_mutation_build.log` and
   `evidence/04_body_mutation_proof.log`.

Thus the proof is about the actual submitted rewrite, not a substituted K
program.  That fact does not cure the rewrite's disagreement with the trusted
program and contract.

## 5. Rule-by-rule static soundness review

Status: **no witnessed execution-bypassing unsoundness on the proved Int
subset; material specification/domain defect remains**.

The complete source index is preserved in `evidence/05_source_inventory.log`.
There are no additional helper `.k` files.

### Syntax, configuration, and attributes

`semantic.k` declares:

- `Program ::= Module(Stmts)`;
- generated lists `Stmts ::= List{Stmt,""}` and
  `Ids ::= List{String,","}`;
- five statement constructors: `FuncDef`, `If`, `While`, `Assign`, `Return`;
- five expression constructors: `Int`, `Bool`, `Name`, `BinOp`, `Compare`;
- `CmpOp(String,Exp)`;
- values `Int | Bool` and results `noResult | Value`;
- ten internal continuations: `exec`, `eval`, `choose`, `loop`, `assignTo`,
  `returnValue`, `binRight`, `binApply`, `cmpRight`, and `cmpApply`;
- configuration cells `<k>`, `<env>`, `<result>`, `<x>`, and `<n>`.

`verification.k` adds exactly three function symbols:

- `solutionProgram : Program [function,total]`;
- `powerCeiling(Int,Int,Int) : Int [function,total]`;
- `simplePowerSpec(Int,Int) : Bool [function,total]`.

There are no local `functional` declarations, opaque symbols, priority rules,
`simplification` rules, or other attributes.  The only imported primitives are
K's `INT`, `BOOL`, and `MAP` theories and their syntax modules.

### Used-construct coverage

| Submitted construct | Declaration | Behavior |
|---|---|---|
| `Module` / exact `FuncDef` / `Params` | `semantic.k:6,11` | Entry rule `55-59` binds `$X,$N` to `x,n` and executes the actual body |
| Statement sequencing / empty list | `8` | Rules `61-62` |
| `If` | `12` | Rules `64-66` |
| `While` | `13` | Rules `68-70` |
| `Assign(Name,Exp)` | `14` | Rules `72-74` |
| `Return` | `15` | Rules `76-78` |
| `Int`, `Bool`, `Name` | `17-19` | Rules `80-83` |
| `BinOp("*",...)` | `20` | Rules `85-90` |
| `Compare(...,"=="/"<",...)` and `CmpOp` | `21,23` | Rules `92-99` |

Every constructor in `solution.mpy` is mapped.  Missing semantics for unused
Python constructs is not a defect in generated-semantics mode.

### Every operational rule

| Rule | Decision |
|---|---|
| `55-59` module entry | Sound and target-scoped.  It requires the exact function name and parameter names, executes arbitrary matched `BODY`, initializes only the two local bindings, and does not encode the answer. |
| `61` empty `exec` | Sound: empty statement sequence contributes no computation. |
| `62` nonempty `exec` | Sound: places the head statement before execution of the tail. |
| `64` start `If` | Sound: evaluates the guard before choosing a branch. |
| `65` true `choose` | Sound; selects only the then-list. |
| `66` false `choose` | Sound; selects only the else-list.  Rules 65 and 66 are disjoint. |
| `68` start `While` | Sound: evaluates the guard before loop selection. |
| `69` true `loop` | Sound: executes one body instance, then re-enters the same `While`. |
| `70` false `loop` | Sound; exits without executing the body.  Rules 69 and 70 are disjoint. |
| `72` start assignment | Sound: evaluates the right-hand side before mutation.  The submitted target is exactly a `Name`. |
| `73-74` commit assignment | Sound: writes the evaluated `Value` to the named map key and preserves the remaining continuation. |
| `76` start return | Sound: evaluates the return expression first. |
| `77-78` commit return | Sound for the modeled single-function configuration: records the value and discards the remaining function continuation, as Python `return` does.  It preserves the environment and input cells.  The early-return concrete cases exercise this control effect. |
| `80` integer literal | Sound identity into K `Int`. |
| `81` Boolean literal | Sound identity into K `Bool`. |
| `82-83` name lookup | Sound for the unique-key K map; it reads without mutation. |
| `85-86` begin binary operation | Sound left-first evaluation. |
| `87-88` continue binary operation | Sound right-second evaluation while preserving the evaluated left value. |
| `89-90` integer `*` | Sound for submitted uses; K arbitrary-precision multiplication matches Python integer multiplication. |
| `92-93` begin comparison | Sound left-first evaluation. |
| `94-95` continue comparison | Sound right-second evaluation. |
| `96-97` integer `==` | Sound for submitted uses. |
| `98-99` integer `<` | Sound for submitted uses. |

No operational rule bypasses the loop, fabricates its returned value, invokes an
oracle, or imports a proof-specific result into `SEMANTIC`.

### Every proof-local equation

| Equation | Class and decision |
|---|---|
| `solutionProgram => Module(FuncDef(...actual body...))` (`verification.k:9-24`) | Definitional abbreviation, not an operational bridge.  It is total, single-rule, exact, constructor-pinned, and body-sensitive. |
| `powerCeiling(P,X,N) => powerCeiling(P*N,X,N)` when `P<X` (`29-30`) | Definitional summary of one loop iteration.  Under the loop claim's `P>0,N>=2` guard it exactly matches the real assignment and strictly increases `P`. |
| `powerCeiling(P,X,N) => P` when `X<=P` (`31-32`) | Definitional base case matching loop exit.  Its guard is disjoint from the recursive guard, and together the guards partition integer `P,X`. |
| `simplePowerSpec(X,N) => X==1 or (X>1 and N>=2 and powerCeiling(N,X,N)==X)` (`37-41`) | A result-bearing postcondition definition, not an execution replacement.  It truthfully characterizes the submitted rewrite, but it is not the requested predicate over unrestricted bases.  Witness: at `X=4,N=-2` it is false while `(-2)^2=4` and the canonical result are true.  This is a specification-substitution/adequacy failure, not an inconsistent K equation. |

There is one non-fatal theory-quality gap inside the proof-local summary:
`powerCeiling` is marked `total` over all integer triples even though the
recurrence is not globally well-founded.  For example,
`powerCeiling(1,2,1)` recurs to itself.  The successful loop claim uses it only
under `P>0,N>=2`, and `simplePowerSpec` reaches it only in the
`X>1,N>=2` branch with initial `P=N`; there it strictly grows and is
well-founded.  I found no false conclusion enabled on the proof domain, so,
consistent with the required witness rule, I do not label this global
termination gap an unsound equation.

The rules have no overlapping right-hand sides on a satisfiable common guard.
Map effects, evaluation order, and control are explicit.  The model deliberately
omits Python floats, generic calls/scopes, exceptions, heap, and I/O; these are
unused by the submitted Int execution, although the Int-only input cells are a
source-domain limitation noted in Stages 2 and 7.

## 6. Fresh non-vacuity test

Status: **PASS**.

The candidate supplied no vacuity artifact, so I created the independent
`evidence/06_spec-vacuity.k`.  It keeps the executable program unchanged and
mutates the result-bearing `x=1` obligation from true to false.  The concrete
satisfying witness is `x=1,n=4`.

First, the mutation was checked for parse/build validity:

```sh
kprove spec-vacuity.k \
  --definition fresh-verification-kompiled \
  --spec-module SPEC-VACUITY \
  --dry-run
```

Exit 0; the generated backend invocation appears in
`evidence/06_mutation_dry_run.log`.

Then:

```sh
kprove spec-vacuity.k \
  --definition fresh-verification-kompiled \
  --spec-module SPEC-VACUITY
```

Exit 1 with `WarnStuckClaimState`.  The residual is a fully executed
configuration with `.K` and `<result>true</result>`, while the destination
requires false.  This is the expected unmet obligation, not a parser error,
timeout, unreachable mutation, or unrelated crash.  See
`evidence/06_mutation_proof.log`.

## 7. Proven versus assumed accounting

### What the K proof actually establishes

Subject to the generated Int semantics and K's partial-correctness reading, the
six successful claims establish the following about the exact submitted
`solution.mpy`:

- for all K integers `N`, `x=1` returns true;
- for all K integers `N` and `X<1`, it returns false;
- for `X>1` and `N<2`, it returns false;
- for `X>1` and `N>=2`, it executes the real loop from `power=N`, finishes
  with the first member of `N, N*N, ...` that is at least `X`, and returns
  whether that member equals `X`.

Equivalently, the submitted rewrite returns:

```text
X == 1
or (X > 1 and N >= 2 and powerCeiling(N,X,N) == X)
```

This is a genuine, result-constraining characterization of the submitted
rewrite.  It is not a proof of the unrestricted simple-power contract.

### Trust ledger

| Boundary | Dependents | Accounting |
|---|---|---|
| K reachability logic, circularity mechanism, Haskell/LLVM backends | All claims and runs | Standard low-level trusted computing base; version recorded and fresh execution used. |
| K `INT`, `BOOL`, and `MAP` built-ins | Arithmetic, comparisons, Boolean guards, environment | Acceptable primitive boundary for arbitrary-precision integer execution. |
| Trusted `py2mpy.py` transliteration | Python-source-to-constructor identity | Launcher-trusted input; independently rerun with byte identity, then constructor-compared. |
| Candidate-generated `semantic.k` | Meaning of every proof execution | Not assumed merely because it compiled.  Audited exhaustively above and tested on 12 construct-covering inputs.  It is adequate for the submitted Int subset, not for Python's broader numeric domain. |
| `solutionProgram` | All entry/path claims | Exact definitional abbreviation; no opacity; mechanically pinned and body-sensitive. |
| `powerCeiling` | Loop post-state and active result | Proof-local mathematical summary, not an operational shortcut.  Its equations match loop execution under the claim guard.  Global `[total]` well-foundedness outside that guard is unsupported. |
| `simplePowerSpec` | Three final path claims and the informal active-path composition | Fully defined, but defines the submitted rewrite's narrowed behavior rather than the source contract.  The negative-base witness disproves the intended bridge. |
| Composition of `active-path-enters-loop` with `loop-correct` | Final active-path theorem | Informal use of exact reachability transitivity and guard implication; no single final active entry claim was submitted.  This is auditable and not the decisive defect. |
| Differential and concrete tests | Python/K adequacy evidence only | Finite empirical support.  They do not substitute for the K proof and are used to expose, not conceal, the contract mismatch. |

There are no opaque symbols, unconstrained result oracles, trusted proof-local
lemmas, operational bridges, priority overrides, or simplification axioms.

### Gate accounting and decision

- Real-program soundness/non-vacuity (Kit Gate A): **PASS** for the exact
  submitted Int program.  Fresh proofs close, the term is pinned, body and
  result mutations fail, and no execution-bypassing extension was found.
- Intent adequacy (Kit Gate B): **FAIL**.  The implementation and postcondition
  reject negative bases that satisfy the prompt and trusted canonical, and the
  theorem additionally models only K integers.
- Trust/evidence auditability (Kit Gate C): **PASS with the explicitly recorded
  totality and composition limitations**.  All empirical claims used here have
  scripts, commands, scopes, outputs, and exit statuses.

Under generic Kit terminology this is at best a sound-but-limited proof of a
different classifier.  The benchmark prompt explicitly requires a material
HumanEval source-domain restriction or specification substitution to be
`FAIL / NOT_LEGIT`, not `CONCERNS / LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
