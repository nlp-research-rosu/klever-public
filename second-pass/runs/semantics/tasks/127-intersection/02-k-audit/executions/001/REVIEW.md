# Independent adversarial audit: 127-intersection

The reconstructed K proof is legitimate. It proves partial correctness of the
submitted translated program for every pair of integer intervals satisfying the
documented ordering preconditions. The proof is result-constraining, and its
only operational summary has an independently reconstructed, bridge-free
connection proof.

The verdict is `CONCERNS / LEGIT`, rather than `PASS`, because the candidate is
missing all four requested generation/provenance records and has no structured
generation trace. Those omissions prevent a complete provenance audit, but they
do not undermine the independently reconstructed source-level theorem.

## 1. Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`, and
`/reference/reference-semantics` is present as required. There is therefore no
mode/mount contradiction and no infrastructure breach.

- A recursive, no-dereference comparison found the candidate
  `reference-semantics/` tree identical to the trusted tree: the same directories
  and 24 regular `.k` files, no extra or missing entry, no changed byte, no type
  mismatch, and no symlink. See
  [04-supplied-semantics-integrity.log](evidence/04-supplied-semantics-integrity.log).
- `/candidate/prompt.py` and `/candidate/py2mpy.py` are byte-identical to their
  trusted mounted versions. See
  [03-prompt-translator-integrity.log](evidence/03-prompt-translator-integrity.log)
  and [21-candidate-source-manifest.log](evidence/21-candidate-source-manifest.log).
- `solution.py`, `solution.mpy`, `spec.k`, and `verification.k` are present as
  regular files. The full candidate manifest contains no symlink. Candidate
  `__pycache__` files and the optional concrete harness are outside the protected
  supplied-semantics tree and were not used as proof evidence.
- `/candidate/run-input.json`, `/candidate/metrics.json`,
  `/candidate/codex-last.txt`, and `/candidate/codex-output.log` are all missing.
  No root-level structured trace or JSONL trace is present. See
  [02-provenance-required-artifacts.log](evidence/02-provenance-required-artifacts.log).
  Thus there was no generation report or trace to credit, distrust, or compare
  against the actual source.

All execution used a source-only copy under `/tmp/audit-work`. No
candidate-provided definition, cache, trace, `#Top`, or prose report was reused.
The live toolchain was K v7.1.337; exact paths and version output are in
[01-toolchain.log](evidence/01-toolchain.log).

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

Each input is a pair of mathematical integers `(start, end)` with
`start <= end`. Let

```text
left   = max(interval1.start, interval2.start)
right  = min(interval1.end,   interval2.end)
length = right - left
```

This is the task's length convention: a closed intersection `(2,3)` has length
one, not two. Return `"YES"` exactly when `length` is prime; return `"NO"` for
disjoint/touching intersections, length zero or one, and composite lengths.

The trusted canonical function computes the same `left`, `right`, and `length`,
rejects nonpositive intersection, and tests divisibility. The candidate uses a
direct divisor loop from 2 through `length - 1`. It covers all three material
paths:

1. `length <= 1` returns `"NO"`;
2. a divisor with zero remainder returns `"NO"`;
3. exhausting the divisor range returns `"YES"`.

### Translation identity

The trusted translator regenerated `solution.mpy` from the scratch copy of
`solution.py`. Both regenerated and submitted files have SHA-256
`dbff75649cdcc014adfb803aec5cfa84ecce5a1f72bfd3e2517e7c7c8c2bda7d`;
`cmp` exited 0. Exact command and status:
[06-regenerate-solution-mpy.log](evidence/06-regenerate-solution-mpy.log).

### Independent differential evidence

The reviewer-authored
[differential_test.py](evidence/differential_test.py) loads the trusted
canonical and submitted functions under separate module names and compares both
against an independently written arithmetic oracle. The exact deterministic
input set is preserved in
[05-differential-inputs.json](evidence/05-differential-inputs.json). It includes:

- all three prompt examples;
- degenerate, touching, disjoint, containment, and negative-coordinate cases;
- overlap lengths 0, 1, 2, 3, 4, 5, 9, 97, and 121, covering loop-empty,
  first-divisor, later-divisor, nonzero-remainder, prime, and composite paths;
- all 4,356 ordered pairs of valid intervals whose endpoints are in `[-5,5]`;
- 2,000 seeded valid interval pairs with endpoints in `[-500,500]`.

All 6,376 cases agreed, with zero mismatch. See
[07-differential-test.log](evidence/07-differential-test.log). This is finite
intent evidence, not a substitute for the K theorem.

## 3. Clean proof reconstruction

The scratch tree began with source files only. The submitted `prove.sh` was
inspected as an untrusted claim but was not used to drive the audit.

| Reconstruction action | Result | Evidence |
|---|---:|---|
| Compile trusted-identical semantics, LLVM, `MPY-KRUN`/`MPY-SYNTAX` | exit 0 | [08-kompile-runtime.log](evidence/08-kompile-runtime.log) |
| Regenerate concrete harness with trusted translator and run it in Python | identity, exit 0 | [09-regenerate-concrete-harness.log](evidence/09-regenerate-concrete-harness.log) |
| Execute regenerated harness with fresh LLVM definition | final `.K`, exit 0 | [10-krun-concrete-harness.log](evidence/10-krun-concrete-harness.log) |
| Compile Haskell `VERIFICATION-BASE` definition | exit 0 | [11-kompile-verification-base.log](evidence/11-kompile-verification-base.log) |
| Prove `LOOP-SPEC.loop-correct` against `VERIFICATION-BASE` | `#Top`, exit 0 | [12-kprove-loop-correct.log](evidence/12-kprove-loop-correct.log) |
| Compile Haskell `VERIFICATION` definition | exit 0 | [13-kompile-verification.log](evidence/13-kompile-verification.log) |
| Prove `SPEC.intersection-correct` | `#Top`, exit 0 | [14-kprove-intersection-correct.log](evidence/14-kprove-intersection-correct.log) |

The two positive claims in `spec.k` are the loop connection theorem and the
end-to-end entry theorem. Both were selected explicitly by label, and both meet
the required success condition: process exit 0 plus printed `#Top`.

The LLVM compiler emitted non-exhaustiveness warnings for several supplied
`[total]` helpers (`mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and
`valSeqAt`). Only `valSeqAt` is on this program's path, and there it receives the
concrete two-element tuple with indices 0 or 1, which is covered by its ordinary
constructor rules. The other warned helpers are unreachable from this program.
The warnings are therefore a documented baseline coverage limitation, not a
false conclusion witness for the theorem.

## 4. Adequacy and real-program pinning

### Plain-language claims

`LOOP-SPEC.loop-correct` says: at the exact head of the real divisor loop, with
`2 <= DIVISOR <= LENGTH`, the real loop body followed by the function's final
`return "YES"` and call cleanup produces `primeFrom(LENGTH,DIVISOR)`. It also
restores the caller environment, removes the callee scope, restores
`scopeLoc`, pops the exact frame, clears `ret`, and resumes the universally
quantified caller continuation.

`SPEC.intersection-correct` says: for all K integers `A,B,C,D` satisfying
`A <= B` and `C <= D`, calling `intersection((A,B),(C,D))` from the pinned
module/builtins configuration returns
`primeResult(min(B,D)-max(A,C))`.

### Pinning and result constraint

The entry claim does not load an arbitrary external function or introduce a
free result. Its scope binds `"intersection"` to a closure over
`intersectionBody`. The transparent `intersectionBody` and `divisorBody`
equations in `/candidate/verification.k:16` and
`/candidate/verification.k:38` reproduce the regenerated `solution.mpy`
constructor-for-constructor, including argument positions, statement order,
both branches, and the final return. Explicit `.Exprs`/`.Stmts` units are only
the K list forms of the translator's omitted trailing units.

Thus the proof uses an audited exact constructor copy of the submitted MPY
body, rather than a substituted algorithm. The return is constrained to the
concrete ASCII `str` value selected by transparent `yesV`/`noV` equations.
`primeFrom` is not opaque: its three disjoint equations perform the same
exhaustive divisor search, and `primeResult` handles the `N <= 1` boundary.

Satisfiable witnesses are recorded in
[adequacy_witness.py](evidence/adequacy_witness.py) and
[16-adequacy-witness.log](evidence/16-adequacy-witness.log):

- loop precondition: `DIVISOR=2`, `LENGTH=3`, with an ordinary local scope and
  saved caller frame; `primeFrom(3,2) = YES`;
- entry precondition: `(A,B,C,D)=(0,2,0,2)`; the claimed result, canonical
  Python, and candidate Python all return `YES`;
- composite, disjoint, and negative-coordinate satisfying witnesses also
  agree.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The reviewer-generated
[15-rule-inventory.md](evidence/15-rule-inventory.md), built by
[build_rule_inventory.py](evidence/build_rule_inventory.py), contains every
local `configuration`, `syntax`, `context`, `rule`, and `claim` directive in
the supplied semantics, helper files, `verification.k`, and `spec.k`, with
source line, collapsed full rule text, attributes, role, and decision.

The inventory has 947 items: 1 configuration, 232 syntax declarations, 5
contexts, 707 rules, and 2 claims. It identifies 151 function-bearing syntax
declarations, 107 `total` declarations, 22 explicit `no-evaluators` opaque
declarations, 46 priority-bearing rules, 35 concrete-only equations, 26
`owise` rules, and four macro declarations. There are no local
`[functional]` or `[simplification]` attributes.

The 928 supplied-semantics items are marked `ACCEPT_FIXED`: the protected tree
is byte-identical to the selected trusted semantics. This acceptance is at the
selected semantics level, not a claim that the small MPY language models every
possible Python program. Every item on the submitted program's path was also
checked directly as follows.

### Used syntax and behavior map

| Submitted construct | Declaration and governing behavior |
|---|---|
| module/function body and statement order | `syntax.k` `Module`, `FuncDef`, and `Stmts`; `core.k` load and left-to-right statement sequencing; `functions.k` closure creation |
| call/return/frame lifecycle | `Call` syntax; `core.k` left-to-right argument evaluation; `call.k` closure dispatch and frame allocation; `functions.k` parameter binding, return, frame pop, environment/scope restoration |
| integer/string/name literals and lookup | `syntax.k`; `core.k` literal and lexical-scope rules; `str.k` ASCII conversion (sufficient for `"YES"`/`"NO"`) |
| tuple arguments and `[0]`/`[1]` | `TupleExpr` and `Subscript` syntax; `tuple.k` left-to-right construction; `subscript.k` object-then-index evaluation, index normalization, and covered `valSeqAt` cases |
| `max`, `min`, and `range` | `builtinsScope` lookup; uniform call routing; `builtins.k` variadic `maxVals`/`minVals` and two-argument `range`; `range.k` iterator step/done rules |
| assignment | strict RHS in `syntax.k`; current-scope update in `controls.k` |
| subtraction and modulo | sequential operand evaluation in `syntax.k`; `operators.k` dispatch; `int.k` subtraction and `pyMod`; divisors are always positive (`>=2`) |
| `<=` and `==` | comparison contexts in `operators.k`; integer cases in `int.k` |
| `if` | strict condition and `controls.k` truth/branch rules |
| `for` | iterable evaluated once; `controls.k` `#loop`/`#loopStep`; `range.k` yields successive integers with step 1 |
| `return` | strict expression; `functions.k` sets `ret`, discards the remaining callee computation, and pops the saved frame |

This path preserves Python order relevant to the theorem: callee before
arguments, arguments left-to-right, RHS before assignment, left operand before
right operand, condition before branch, iterable once before looping, and
return before frame cleanup. The program allocates no mutable heap object; the
heap remains empty. Scope allocation/removal and call-stack changes are
explicit in the claims and the connection theorem.

### Candidate-local extension decisions

All 17 candidate proof extensions are enumerated individually at the end of
the inventory.

- The Map deletion normalization at `/candidate/verification.k:9` is a true
  Map identity: deleting known key 1 from a disjoint `1 |-> FRAME` plus
  remainder yields that remainder. Its guard excludes a duplicate key.
- `intersectionBody`, `divisorBody`, `yesV`, `noV`, and `overlapLength` are
  transparent definitional summaries. They do not replace execution with an
  unconstrained value.
- The three `primeFrom` equations have disjoint, exhaustive guards on the
  reachable domain. The recursive case increases `D` toward `N`; zero and
  nonzero remainder cases are complementary. The two `primeResult` equations
  are disjoint and exhaustive.
- The priority-40 loop rule is an operational bridge, but it is not assumed.
  The matching `LOOP-SPEC` theorem was proved against `VERIFICATION-BASE`,
  whose import graph excludes module `VERIFICATION` and therefore excludes
  the bridge. The theorem and installed rule have the same loop body, exact
  suffix (`Return("YES") ~> #endcall`), arbitrary caller continuation,
  environment, local-scope removal, `scopeLoc` restoration, frame pop,
  return state, and guard. Variable renaming and transparent expansion of
  `divisorBody` are the only textual differences.

The bridge's execution footprint is complete: it returns the exact
`primeFrom` value, changes the same control and scope cells as real return/pop,
and leaves the omitted heap, heap counter, exception, and exit-code cells
unchanged. Its match domain is contained in the bridge-free theorem's domain.

The separate operational-sensitivity artifact
[spec-bridge-sensitivity.k](evidence/spec-bridge-sensitivity.k) changes the
loop test from remainder `== 0` to remainder `== 1` at `LENGTH=3`. It passed
KORE dry-run compilation
([17-bridge-sensitivity-dry-run.log](evidence/17-bridge-sensitivity-dry-run.log))
and then failed as required
([18-bridge-sensitivity-proof.log](evidence/18-bridge-sensitivity-proof.log)):
fixed execution reached concrete `"NO"` while the destination required
`"YES"`. This shows the installed bridge does not silently match a materially
different body.

### Opaque and totality boundaries

The supplied theory imports explicit proof-opaque symbols
`md5hexCodes`, `sortVS`, `sortKeyVS`, `intFloatDiv`, `divII`, `floatMod`,
`floatLt`, `absF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`,
`decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`, and
`sqrtF`. The concrete-only `floorFI`, `toF`, and `ceilF` are likewise
unreduced for unsupported symbolic proof inputs. None occurs in
`solution.mpy`, a claim destination, a path condition, or a proof-local
summary. They cannot influence this theorem's branch, result, state, or
control.

No inventoried candidate rule was found unsound, so there is no false
conclusion witness to report. The supplied totality warnings above are stated
as the narrower evidence gap they actually establish; they do not admit a
wrong result on the intended input path.

## 6. Fresh non-vacuity test

The reviewer-authored
[spec-vacuity.k](evidence/spec-vacuity.k) changes the entry theorem's
result-bearing destination to `noV` for the satisfying input
`(0,2),(0,2)`. Both Python implementations and the formal `primeResult(2)`
return `"YES"`, so the mutation is demonstrably false.

The mutation first built successfully through `kprove --dry-run` with exit 0:
[19-vacuity-dry-run.log](evidence/19-vacuity-dry-run.log). The actual proof
then exited 1 with `WarnStuckClaimState`; its residual contains concrete ASCII
`YES` in `<k>`, which does not unify with the required `noV`/`NO` destination:
[20-vacuity-proof.log](evidence/20-vacuity-proof.log).

This is a reached, result-specific unmet obligation, not a parser failure,
missing import, timeout, or unrelated crash. The positive proof is therefore
discriminating and non-vacuous.

## 7. Proven versus assumed accounting

### What is proved

Under the supplied MPY semantics, for every mathematical integer
`A,B,C,D` with `A <= B` and `C <= D`, if the pinned `intersection` execution
terminates, its return is:

```text
NO, if min(B,D)-max(A,C) <= 1;
NO, if some integer d in [2, length-1] divides length;
YES, otherwise.
```

The bridge-free loop theorem connects every real remaining loop iteration to
that transparent divisor-search function. The end-to-end theorem connects the
exact translated body to the result. This is partial correctness; it does not
claim a separate termination theorem despite the candidate comment calling the
loop lemma “total-correctness.”

For integers greater than one, “has no divisor from 2 through `N-1`” is the
ordinary mathematical characterization of primality. Together with the
prompt's explicit length convention, this makes the formal result adequate to
the natural-language property.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| Protected supplied MPY semantics | all symbolic and concrete K execution | Acceptable and required by `SUPPLIED_SEMANTICS`; exact tree integrity established |
| K v7.1.337, Haskell/LLVM backends, K integer/Boolean/String/Map/List primitives | proof closure and concrete runs | Ordinary toolchain trust; version and fresh commands recorded |
| Trusted `/reference/py2mpy.py` | source-to-MPY bridge | Acceptable; candidate translator identical and trusted regeneration byte-identical |
| `minInt`, `maxInt`, integer arithmetic, `pyMod` with positive divisor | length and divisor calculation | Fixed semantics plus ordinary integer mathematics |
| Installed loop summary | entry proof | Not an assumption: independently proved without importing the summary, then body-sensitivity tested |
| `primeFrom`, `primeResult`, result strings, overlap helper | final result | Transparent equations, no opacity, no `total` oracle |
| Imported float/sort/MD5 opaque symbols and warned unused total helpers | none for this program | Inert; no dependency path to result/control/state |
| Canonical/candidate/oracle differential suite | finite intent/translation support only | Strong finite evidence, explicitly not used as the K proof |
| Primality characterization and prompt interpretation | human-facing intent bridge | Elementary informal mathematics; no competing length convention after checking examples |
| Program termination | excluded from theorem | Correctly excluded by partial-correctness scope |

Gate A (real-program soundness) passes: exact body, bridge-free connection,
complete bridge context, satisfiable witnesses, body sensitivity, and
non-vacuity all hold. Gate B (intent adequacy) passes: the formal domain and
result match the integer-interval contract. Gate C is limited only by the
candidate's missing provenance/generation records; all reviewer-created
evidence is reproducible.

Accordingly, the proof itself is legitimate and has no material adequacy gap,
while the missing required provenance artifacts warrant a concern-level
verdict.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
