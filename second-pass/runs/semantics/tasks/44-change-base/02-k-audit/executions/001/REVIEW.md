# Independent adversarial audit: 44-change-base

## Executive decision

The candidate contains a legitimate, non-vacuous partial-correctness proof under
the supplied MPY semantics. I rebuilt both definitions from source, proved the
two original claims together with no trusted claims, proved the direct-call
claim separately, and proved the load entry separately using only the already
proved direct-call claim as its explicit helper. The proof executes the exact
translated body. A body mutation changes the residual and invalidates the
theorem, and a fresh false result mutation builds but is rejected with the
expected unmet equality.

The result is `CONCERNS / LEGIT`, rather than `PASS`, for two intent/portability
limitations. First, the docstring does not expressly state `x >= 0` or
`base >= 2`, while the claims do. Second, the K model has unbounded recursive
calls, whereas the submitted recursive CPython function raises
`RecursionError` on a 1,051-bit base-2 input that the iterative canonical
function handles. These are limitations in the bridge from the sound K theorem
to the loosely stated contract and CPython execution model; they are not
unsound proof rules and do not make the partial-correctness conclusion false
when the submitted function returns normally.

No infrastructure breach occurred. The rendered mode is
`SUPPLIED_SEMANTICS`, the trusted semantics mount is present, and the live K
toolchain works.

## 1. Input and provenance integrity

I treated every candidate file as untrusted and used
`/reference/canonical.py`, `/reference/prompt.py`, `/reference/py2mpy.py`, and
the supplied reference semantics as the trusted baselines.

- `/reference/reference-semantics` is an ordinary directory, as required for
  `SUPPLIED_SEMANTICS`.
- The candidate `reference-semantics/` contains exactly the same directory and
  24 regular-file entries as the trusted tree. There are no missing,
  additional, mistyped, changed, or symlinked entries. Every file compared
  byte-for-byte.
- Candidate `prompt.py` and `py2mpy.py` are regular files and byte-identical to
  their trusted versions.
- `solution.py`, `solution.mpy`, `spec.k`, and `verification.k` are present as
  regular files. No candidate root entry is a symlink.
- `run-input.json`, `metrics.json`, `codex-last.txt`, and
  `codex-output.log` are all missing. No structured generation trace is
  present. This removes potentially useful provenance evidence but does not
  substitute or invalidate the independently reconstructed proof.
- Other untrusted candidate artifacts are `prove.sh`, concrete test sources,
  and a Python bytecode cache. I did not reuse their generated outputs or
  caches.

The complete type/content comparison and hashes are in
[01-provenance.log](evidence/01-provenance.log); the candidate/trusted source
listing is in [02-source-inventory.log](evidence/02-source-inventory.log).

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementation

The prompt asks `change_base(x, base)` to return the string representation of
integer `x` in a base less than 10. The examples require
`change_base(8,3) == "22"`, `change_base(8,2) == "1000"`, and
`change_base(7,2) == "111"`. The trusted canonical repeatedly prepends
`x % base` while `x > 0`, returning the empty string for `x == 0`.

The submitted implementation is recursive:

1. return `""` when `x == 0`;
2. otherwise return `change_base(x // base, base) + chr(48 + x % base)`.

For mathematical integers `x >= 0` and `2 <= base < 10`, this is the same
base-expansion recurrence as the canonical loop. It uses a different
algorithm, which is acceptable.

### Translation fidelity

I regenerated `solution.mpy` from the scratch copy of `solution.py` using the
trusted translator. `cmp` exited 0 and both files have SHA-256
`b2ca9c3b19fff8ac6ffcfb46f0d83d932adf3306cdd4a78ba1d7fa6e11d8b044`.
See [04-translation-identity.log](evidence/04-translation-identity.log).

### Independent differential testing

The reviewer-authored
[differential_check.py](evidence/differential_check.py) imports the trusted
canonical and scratch-copied submitted entry points independently. Its exact
input construction is recorded in
[differential-input-scope.md](evidence/differential-input-scope.md). The final
run covered:

- 52 examples and branch/digit boundaries;
- all `x = 0..512` at every base 2 through 9 (4,104 cases);
- 256 deterministic generated nonnegative integers up to 512 bits;
- two recursion-stress cases; and
- three negative-`x` probes exposing the prompt's unstated domain boundary.

Of 4,417 cases, 4,413 matched. The four visible mismatches were:

- at `x = 2**1050`, `base = 2`, the canonical returns a 1,051-character
  string while the submission raises `RecursionError`;
- at `(-1,2)`, `(-2,3)`, and `(-7,9)`, the canonical returns `""` because
  its loop never starts, while the recursive submission raises
  `RecursionError`. These three inputs are outside the formal `X >= 0`
  precondition but are not expressly excluded by the docstring.

The exact outcomes and exit 1 are in
[26-differential-final.log](evidence/26-differential-final.log). This is a
material CPython/intent limitation, not evidence that the K recurrence is
wrong.

Separately,
[summary_bridge_check.py](evidence/summary_bridge_check.py) evaluated the
`baseDigits` equations against the trusted canonical for all `x = 0..4096`,
all bases 2 through 9, and 512 deterministic integers up to 4,096 bits:
33,288 cases with zero mismatches. See
[30-summary-bridge.log](evidence/30-summary-bridge.log). This finite evidence
supports, but does not replace, the mathematical induction described below.

## 3. Clean proof reconstruction

All execution occurred under `/tmp/audit-work`. I copied only source inputs,
using the trusted supplied semantics rather than any candidate cache or
compiled definition. The source-only scratch manifest is in
[03-scratch-setup.log](evidence/03-scratch-setup.log). The toolchain was K
v7.1.337.

### Concrete definition

I compiled `/reference/reference-semantics/semantics.k` with LLVM as
`MPY-KRUN`/`MPY-SYNTAX`; compilation exited 0
([06-concrete-build.log](evidence/06-concrete-build.log)). A fresh
reviewer-authored program exercised the documented examples, `x == 0`, both
branches, and base-9 digit boundaries. `krun` terminated at `.K` with
`NoExc` and exit code 0
([07-concrete-run.log](evidence/07-concrete-run.log)).

### Proof definition and claims

I compiled `verification.k` with the Haskell backend as
`VERIFICATION`; compilation exited 0
([08-proof-build.log](evidence/08-proof-build.log)).

The positive proof evidence is:

| Target | Command evidence | Result |
|---|---|---|
| Original unmodified two-claim `SPEC` | [09-positive-all.log](evidence/09-positive-all.log) | exit 0, `#Top` |
| Direct-call claim alone | [10-positive-entry-call.log](evidence/10-positive-entry-call.log) | exit 0, `#Top` |
| Load claim, with the byte-identical separately proved direct-call claim admitted as its helper | [17-positive-entry-load-trusted-helper.log](evidence/17-positive-entry-load-trusted-helper.log) | exit 0, `#Top` |

The original proof used no `--trusted` claims. The last row is only a modular
isolation of the second target: K's `--trusted` flag skips reproving the helper
while keeping it available as a circularity. The exact helper had already
closed separately, and the unmodified two-claim module also closed as a unit.
An initial diagnostic that removed or filtered out the required recursive
helper was intentionally interrupted and is explained in
[isolated-load-diagnostic.md](evidence/isolated-load-diagnostic.md); it is not
a target-proof failure.

Both required positive entry claims therefore close from a clean source build
with exit 0 and `#Top`.

## 4. Adequacy and real-program pinning

### Claim 1: direct call

In plain language, the first claim says: for `X >= 0` and
`2 <= B < 10`, calling the exact `change_base` closure with `(X,B)` from a
scope store containing the module binding, builtins, and a fresh allocatable
scope suffix produces `str(baseDigits(X,B))`, then resumes the arbitrary
continuation `K`. It starts and ends with `noRet` and `NoExc`; the environment,
heap, heap allocator, caller stack, and exit code are framed and preserved.
`N > 0` and `freshScopes(N,FRAMES)` justify allocation and deletion of each
recursive call frame.

This is the recursive execution summary/circularity. It starts at the real
`#applyK(toCall(changeBaseClosure),...)` call machinery; no rule replaces that
call with `baseDigits`.

### Claim 2: module load and call

The second claim says: from the exact empty MPY initial state, load
`solutionModule`, call `change_base(X,B)`, and finish with
`str(baseDigits(X,B))`. It also requires `X >= 0` and `2 <= B < 10`. The
post-state explicitly contains the loaded `"change_base"` binding and otherwise
the specified initial cells.

### Exact program identity

`solutionModule`, `changeBaseClosure`, and `changeBaseBody` are definitional
names. Expanding them yields the exact `FuncDef`, parameters, docstring
statement, `If`, recursive call, floor division, modulo, `chr`, string
concatenation, and `Return` constructor tree regenerated from `solution.py`.
The byte-identity check in stage 2 closes the source-to-MPY link.

The direct claim executes this body through the supplied function-call,
binding, lookup, operator, builtin, return, frame-pop, and scope-allocation
rules. The load claim first executes the supplied module-load and function
definition rules, then uses the proved direct-call theorem.

As a separate body-sensitivity test, I changed only the body's `Int(48)` to
`Int(49)`, leaving `baseDigits` and the theorem unchanged. The mutated
definition compiled, but the direct-call proof exited 1 with
`WarnStuckClaimState`; its residual explicitly compares a result ending in
`48 + remainder` against execution ending in `49 + remainder`.
See [body-mutation.md](evidence/body-mutation.md),
[23-body-mutation-build.log](evidence/23-body-mutation-build.log), and
[24-body-mutation-proof.log](evidence/24-body-mutation-proof.log). This
demonstrates body sensitivity and rules out a substituted-program or
program-name oracle proof.

### Satisfiable preconditions and concrete substitution

A concrete state satisfying claim 1 uses `X=8`, `B=3`, `env=0`,
`N=1`, `FRAMES=.Map`, empty heap/stack, `noRet`, `NoExc`, and exit code 0.
Here `freshScopes(1,.Map)` reduces to true. Claim 2's exact initial
configuration with `X=8`, `B=3` also satisfies its precondition.

For this witness, `baseDigits(8,3)` is the code sequence for `"22"`;
both trusted canonical Python and submitted Python return `"22"`. The complete
states and substitution are in
[25-ground-witness.log](evidence/25-ground-witness.log).

The postcondition is exact and result-bearing: it demands
`str(baseDigits(X,B))`. It has no right-only free result variable, tautology, or
one-way implication.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[rule-inventory.tsv](evidence/rule-inventory.tsv) inventories every local
configuration, syntax declaration, context, and rule in
`reference-semantics/semantics.k`, all recursively required semantics files,
and `verification.k`. Each row gives its source line range, attributes,
normalized statement, reachability/trust classification, and disposition.
Hashes bind the inventory to the source reviewed.

The inventory contains 943 items:

- 1 configuration;
- 232 syntax declarations;
- 5 evaluation contexts; and
- 705 rules.

It records 150 function declarations, 107 `total` declarations, 25 symbol
declarations, 22 `no-evaluators` uses, 45 priority rules, 26 `owise` uses,
35 concrete-only attributes, and the two proof-local simplification rules.
There are no `functional` declarations. Counts and all 15 proof-local items are
in
[29-rule-inventory-summary-final.log](evidence/29-rule-inventory-summary-final.log).

Every fixed-semantics row has one of three task-specific decisions: accepted
and reachable, accepted but inert for this program, or an explicitly identified
unused opaque/concrete-only boundary. This is a supplied-semantics audit, so
`concrete.k` is not imported into the Haskell proof. Float, sorting, MD5,
collection, comprehension, slicing, and other opaque or partial operations
cannot be reached from this `solution.mpy` or from `baseDigits`.

The LLVM build warned that several fixed, unrelated `total` helpers are not
exhaustive for newly added value forms (`mapStrVS`, `floorFI`, `toF`, `ceilF`,
`joinCodes`, and `valSeqAt`). None of those missing cases is constructible on
this program's path, and none contributes to either proof claim. I therefore
record these as narrower unused coverage gaps, not as unsound rules: there is
no false conclusion witness they enable on the intended input domain.

### Used-construct map

| Submitted construct | Declaration/evaluation | Operational result |
|---|---|---|
| `Module`, `Stmts`, `FuncDef` | `syntax.k`; `core.k` load/sequencing; `functions.k` definition | installs the exact closure in scope 0 |
| docstring `Expr(Str(...))` | `syntax.k`; `str.k` literal; `controls.k` expression discard | evaluates ASCII literal, then discards it |
| `If` | strict condition in `syntax.k`; `controls.k` `#branch` | chooses `x == 0` versus recursion |
| `Compare` / `CmpOp("==")` | contexts in `operators.k`; integer equality in `int.k` | computes the exact Boolean guard |
| `Name`, `Int` | `core.k` lookup and literal rules | reads `x`, `base`, `change_base`, and `chr` from real scopes |
| `BinOp("//","%","+")` | left-to-right strictness; `operators.k`; `int.k` | Python-style floor quotient/remainder and integer addition |
| string `BinOp("+")` | `str.k` `seqConcat` | concatenates recursive prefix and one digit |
| `Call` | `call.k` callee/argument evaluation and dispatch | invokes the real recursive closure or real builtin route |
| builtin `chr` | `builtinsScope`; `call.k`; `builtins.k` | returns one ASCII-code string |
| `Return` | strict return in `syntax.k`; `functions.k` return/pop | restores caller continuation, env, stack, scope store, and allocator |

Evaluation order is preserved: binary operands are `seqstrict(2,3)`, calls
evaluate the callee and then arguments left-to-right, and return expressions
are strict. Recursive calls allocate a scope at `scopeLoc`, bind `x` and
`base`, push the complete continuation, and on return delete exactly that
scope, restore the caller environment and allocator, reset `ret`, and resume
the saved continuation. The program performs no heap allocation or persistent
state update. For the formal domain, division is by a positive base and
`chr(48 + x % base)` is within the supplied ASCII builtin's guard.

### Proof-local extension decisions

1. `freshScopes` is a proof invariant, not an execution oracle. Its empty and
   recursive equations describe a contiguous descending suffix of fresh scope
   keys. Under that invariant, rewriting `L in_keys(S)` to false is valid.
2. The two Map equations expose a fresh update as a disjoint binding and delete
   that same unique binding on frame pop. Their guards exclude overlap with an
   existing key. They preserve the exact scope-store effect of the supplied
   call/pop rules.
3. `changeBaseBody`, `solutionModule`, and `changeBaseClosure` are transparent
   definitional aliases. They expand to the byte-regenerated submitted AST and
   do not skip execution.
4. `baseDigits(0,B) = .IntSeq` and the positive recurrence are a definitional
   mathematical summary, not an operational bridge. For `N > 0`, `B >= 2`,
   let `r = pyMod(N,B)` and `q = (N-r)/B`. The supplied positive-modulus
   equation gives `0 <= r < B`, `N = qB+r`, and `0 <= q < N`. Thus the
   recurrence terminates structurally, appends the correct least-significant
   digit, and ordinary induction establishes the base representation. With
   `B < 10`, every appended code is an ASCII decimal digit. The zero and
   positive guards are disjoint and cover every value reachable under the
   claims.

There are no proof-local priority rules, `total` declarations, opaque symbols,
or operational rules that turn a program expression directly into
`baseDigits`. The only simplifications are the two truthful `baseDigits`
equations. Local equation overlaps are disjoint or, for the fixed semantics,
have equal effects under their priorities and guards.

I found no unsound candidate rule. Consequently, there is no candidate-rule
unsoundness assertion requiring a false-conclusion witness. The concrete
counterexamples in stage 2 witness intent/execution-model limitations, not a
false K rewrite.

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`, so I did not rely on one.

I created the fresh
[spec-vacuity.k](evidence/spec-vacuity.k). It leaves the separately proved
direct-call helper unchanged but mutates the load claim to require the actual
base-digit sequence followed by an extra ASCII `'0'`. For the satisfiable
witness `X=8`, `B=3`, execution returns `"22"` while the mutation demands
`"220"`.

- `kprove --dry-run` exited 0, demonstrating that the mutation parses and
  builds successfully
  ([20-vacuity-setup-and-dry-run.log](evidence/20-vacuity-setup-and-dry-run.log)).
- The real proof exited 1 with `WarnStuckClaimState`, not a parser, import,
  timeout, or unrelated error. The residual contains the reached
  `str(baseDigits(X,B))` and the failed equality against
  `seqConcat(baseDigits(X,B), iCons(48,.IntSeq))`
  ([21-vacuity-proof.log](evidence/21-vacuity-proof.log)).

This is meaningful result non-vacuity. The separate `48 -> 49` body mutation
from stage 4 supplies independent operational/body sensitivity.

## 7. Proven versus assumed accounting

### What is machine proved

Under the supplied MPY semantics and the formal preconditions
`X >= 0` and `2 <= B < 10`:

- the exact loaded `solution.mpy` definition calls the exact submitted
  `change_base` body;
- recursive calls follow the real supplied call/bind/return semantics;
- on normal completion the result is exactly
  `str(baseDigits(X,B))`;
- the module-load claim installs the exact closure binding shown in its
  post-state; and
- the explicitly framed heap, allocator, exception, return, caller stack,
  environment, and exit-code observations are preserved as claimed.

This is a partial-correctness reachability proof. It is not a CPython
resource-bound or termination theorem.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K v7.1.337 parser, compiler, Haskell/LLVM backends, and reachability logic | all machine-check results | normal foundational tool trust |
| K builtin `INT`, `BOOL`, `STRING`, `MAP`, `LIST`, and equality hooks | arithmetic, strings, scopes, continuations | acceptable fixed low-level semantics trust |
| Trusted supplied MPY semantics | source execution and all claims | required by `SUPPLIED_SEMANTICS`; integrity checked and relevant rules audited |
| Trusted AST translator | source-to-`solution.mpy` bridge | acceptable; exact byte regeneration succeeded |
| Ordinary induction interpreting `baseDigits` as base representation | natural-language result meaning | transparent mathematical argument; additionally supported by 33,288 zero-mismatch tests |
| Trusted canonical Python as a differential oracle | finite implementation/intent evidence only | acceptable empirical evidence, not part of the K proof |
| Opaque float, sort, MD5, and other fixed-semantics symbols | none | acceptable because unreachable from this program and theorem |
| Unbounded MPY call stack versus CPython recursion limit | bridge to actual CPython for very large `x` | documented concern; concrete mismatch exists |
| Conventional assumption that inputs use nonnegative `x` and bases 2 through 9 | bridge to the underspecified docstring | documented concern; claims are explicit but prompt is not |

### Gate results

- Real-program soundness and non-vacuity: **PASS**.
- Intent adequacy: **PASS with limitation**. The base-representation theorem
  matches the conventional intended domain, but the prompt is underspecified
  and CPython recursion limits are not modeled.
- Evidence auditability: **PASS with provenance concern**. Reviewer evidence is
  fully reproducible, but the four requested candidate generation-metadata
  files and structured trace are absent.

The reconstructed proof is sound, result-constraining, and pins the actual
submitted MPY program. The limitations warrant `CONCERNS`, but neither is an
unsound proof extension, a substituted program, or a vacuous theorem.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
