# Independent adversarial review: 109-move-one-ball

The candidate reconstructs and proves both of its universal K reachability
claims, pins the submitted constructor program, covers the unrestricted finite
integer-list domain (and thus the promised unique-list domain), and is
non-vacuous. I found no materially false semantic or proof rule.

The result is not a clean `PASS` because the generated semantics contains an
exact-body, result-bearing operational bridge for the program's loop. That
bridge is mathematically faithful, but the candidate supplies no bridge-free
universal connection theorem and uses the same `dropsFrom` summary in execution
and the postcondition. Reviewer concrete bridge-free tests agree, while a fresh
full-context symbolic connection attempt did not close. The separate
equivalence between “at most one circular drop” and the HumanEval
right-rotation contract is also an informal mathematical bridge. These are
trust/evidence limitations, not witnesses of a false conclusion.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout =
legacy-selected-stage1`, condition `bare`, and
`semantics_mode = GENERATED_SEMANTICS`. The campaign object is structurally
identical to `/audit-campaign-lock.json`; the lock's SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
matching the launcher record.

I read and checked all records required by this layout:

- `/run.json`, `/task.json`, and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`, and the present
  `usage.json`;
- `codex-last.txt`, `codex-output.log`, and `prompt.txt`; and
- all 282 JSON objects in the one structured trace file below
  `/generation-evidence/codex-trace/`.

All were readable regular files. The trace contained no malformed JSON.
Historical `runtime-metrics.json` is absent, which is explicitly allowed for
this legacy-selected layout. The generation records' `KPROVE_PASSED` marker and
prior outputs were treated only as untrusted claims.

The launcher-recorded direct hashes for the campaign lock, run/task/result
records, invocation, metrics, usage, prompt, output log, final message,
canonical source, trusted prompt, and both translator copies all match fresh
SHA-256 calculations. Every generation-output hash listed in
`generation-result.json`, including the trace file, also matches. A complete
independent candidate per-file hash manifest was recorded. There are no
symlinks anywhere below `/candidate`, `/reference`, or
`/generation-evidence`.

`/candidate/prompt.py` is byte-identical to `/reference/prompt.py`, and
`/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`.
`/reference/reference-semantics` does not exist, as required by the rendered
generated-semantics mode. Thus there is no supplied-semantics integrity check
and no hidden semantics was sought or used.

Evidence:

- `evidence/provenance-check.log`
- `evidence/provenance-inventory.log`
- `evidence/campaign-check.log`
- `evidence/trusted-copy-integrity.log`
- `evidence/generation-records.log`
- `evidence/generation-trace-inspection.log`

No audit-infrastructure breach was found.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

From `/reference/prompt.py`, the input is a finite list of unique integers.
The required result is `True` exactly when some number of cyclic right shifts
makes the list non-decreasing; the empty list must return `True`.

The trusted canonical implementation in `/reference/canonical.py` finds the
minimum, rotates it to the front, and compares that rotation with `sorted(arr)`.
The candidate `/candidate/solution.py` instead counts strict descents around
the circular list by starting `previous` at the last element. It returns
`True` exactly when the count is at most one.

For a unique nonempty list, these formulations are equivalent. If a rotation
is increasing, no internal edge of that rotation descends, so the only possible
circular descent is its cut edge. Conversely, if there is at most one circular
descent, cutting immediately after it yields an increasing rotation (with the
singleton case immediate). Empty input is handled explicitly. The candidate's
use of mathematical integers also agrees with Python's arbitrary-precision
integers for the used operations.

### Translation identity

Fresh execution of

```text
python3 /reference/py2mpy.py /candidate/solution.py
```

produced SHA-256
`e646b542620bbc9d7ed94850d6eac6b5a9d4b15e6b4d989667fd6e13c35e7e66`,
identical byte-for-byte to `/candidate/solution.mpy`. See
`evidence/translator-byte-identity.log`.

### Independent differential test

`evidence/differential_test.py` imports the trusted canonical and generated
entry points under distinct module names and compares both to an independently
implemented oracle that enumerates every right rotation and checks adjacent
non-decreasing order. It covers:

- both documented examples;
- empty, singleton, negative, and very large integer cases;
- zero, one, and multiple circular-descent boundaries;
- every permutation of `range(n)` for `n = 0..8`; and
- 1,800 deterministic seeded unique lists at lengths
  `2,3,4,5,8,9,16,31,64`.

All 48,048 cases matched, with 0 mismatches. Exact scope, seed, input-sequence
hash, command, result, and exit 0 are in
`evidence/differential-test.log`. This is finite bridge evidence, not a
substitute for the K proof or the mathematical equivalence argument.

## 3. Clean proof reconstruction

Only source files were copied to
`/tmp/audit-work/reconstruction-109`. No candidate-built definitions or caches
were copied or reused. K was independently identified as v7.1.293.

Fresh builds:

```text
kompile semantic.k --backend llvm --main-module HUMAN-EVAL \
  --syntax-module HUMAN-EVAL-SYNTAX \
  --output-definition reviewer-llvm-kompiled
```

and

```text
kompile semantic.k --backend haskell --main-module HUMAN-EVAL \
  --syntax-module HUMAN-EVAL-SYNTAX \
  --output-definition reviewer-haskell-kompiled
```

both exited 0. See `evidence/llvm-build.log`,
`evidence/haskell-build.log`, and `evidence/toolchain-versions.log`.

The reconstructed LLVM semantics was run on empty, singleton, sorted,
one-drop, two-drop, both documented, and negative-boundary inputs. Each final
configuration had the expected `bVal`, input cell, and environment and agreed
with both Python implementations and the direct rotation oracle. See
`evidence/concrete-semantics.log`.

The original positive proof command

```text
kprove spec.k --definition reviewer-haskell-kompiled \
  --spec-module HUMAN-EVAL-SPEC
```

exited 0 and printed exactly `#Top`
(`evidence/kprove-original-all.log`). I also copied each source claim
unchanged into a separate reviewer module and proved it independently:

- empty claim: exit 0, `#Top`
  (`evidence/kprove-empty.log`, source
  `evidence/spec-empty-reviewer.k`);
- nonempty claim: exit 0, `#Top`
  (`evidence/kprove-nonempty.log`, source
  `evidence/spec-nonempty-reviewer.k`).

For generated-semantics validation, I removed only the special loop-summary
rule in a separate scratch definition, leaving generic ordinary iteration.
That bridge-free LLVM definition built and produced the same final K results
on all eight reviewer cases. Sources and logs are
`evidence/semantic-bridgefree.k`,
`evidence/bridgefree-llvm-build.log`, and
`evidence/bridgefree-concrete.log`.

## 4. Adequacy and real-program pinning

### Entry claims in plain language

The empty claim in `/candidate/spec.k:7` says: starting with `theSolution`,
empty input, and an empty environment, execution reaches `bVal(true)` and an
environment containing only `arr` bound to the empty list.

The nonempty claim in `/candidate/spec.k:13` says: for every integer `I` and
finite integer tail `IS`, starting with `theSolution`, input `I :: IS`, and an
empty environment, execution reaches

```text
bVal(rotationSortable(I :: IS))
```

and the exact final bindings
`arr = I::IS`, `drops = cyclicDrops(I::IS)`,
`previous = last(I::IS)`, and `value = last(I::IS)`.

There is no hidden finite-size bound and no uniqueness precondition. The
formal theorem is broader than the source contract, not narrower. Its
postcondition constrains the returned Boolean by an equality-bearing K term;
it is not a free variable, tautology, or one-way implication.

Both preconditions are satisfiable. Concrete witnesses include the empty
configuration and nonempty inputs `[3,4,5,1,2]` (result true, drops 1) and
`[3,5,4,1,2]` (result false, drops 2). The K, candidate Python, trusted
canonical, and direct oracle results agree in
`evidence/concrete-semantics.log`.

### Program identity

The claim executes `theSolution`, whose defining rule is manually maintained
in `/candidate/mpy-syntax.k:32`. I mechanically parsed both the freshly
regenerated `solution.mpy` and that rule with `kast`, extracted the rule RHS,
and compared the complete KAST constructor trees. Both canonical JSON
constructor hashes were
`3e112e81eb334abd29bbc105c4d605c6a6615a997de04be1cc7b3c9c5bcf1194`;
the terms were equal. See `evidence/check_program_pinning.sh` and
`evidence/program-pinning.log`.

Thus the immutable claim term is the same function name, parameter, and body as
the trusted translation. The manual duplicate is an artifact-maintenance risk,
not a present identity failure.

A separate body-sensitivity mutation changed the final comparison in the
executed `theSolution` term from `drops <= 1` to `drops <= 0`. The mutated
definition built, but the original nonempty proof exited 1 with
`WarnStuckClaimState`; its residual explicitly compared the computed
`<= 0` Boolean with the required `<= 1` Boolean. See
`evidence/mpy-syntax-body-mutation.k`,
`evidence/body-mutation-build.log`, and
`evidence/body-mutation-kprove.log`. This changes the term actually executed by
the claim and confirms theorem sensitivity to the program body.

## 5. Rule-by-rule static soundness review

The complete declaration and 48-rule inventory is
`evidence/RULE-INVENTORY.md`; exact numbered sources and attribute searches
are preserved in `evidence/static-source-inventory.log`.

### Declaration inventory

`mpy-syntax.k` declares the exact translated constructors for module,
function, statements, expressions, comparison operators, and finite integer
lists, plus total nullary function `theSolution`.

`verification.k` declares six mathematical functions:
`length`, partial-nonempty `last`, `dropBit`, `dropsFrom`, `cyclicDrops`, and
`rotationSortable`. All except `last` are marked total. `last` has no empty
equation, correctly exposing invalid empty use.

`semantic.k` declares three values, sixteen computation/control forms, and
exactly the required `<k>`, `<input>`, and `<env>` cells. There is one
`priority(40)` rule, one `owise` rule, and no local simplification, anywhere,
macro, opaque, or explicit functional declaration.

### Every rule

- M1 (`mpy-syntax.k:32-47`) is the exact, total, mechanically matched program
  constant.
- V1-V2 are the disjoint, descending list-length equations.
- V3-V4 are the disjoint, descending nonempty-last equations.
- V5-V6 define `dropBit`; `>` and `<=` guards are disjoint and exhaustive on
  integers.
- V7-V8 are the disjoint, descending linear-drop fold.
- V9-V10 define the empty and nonempty circular-drop count; nonempty V10 is
  the only use of `last` there.
- V11 defines `rotationSortable` as `cyclicDrops(L) <= 1`; the human-facing
  meaning of that name is not assumed merely from the name.
- S1 launches the submitted sole unary function and binds input.
- S2-S3 sequence empty/nonempty statement lists left-to-right.
- S4-S5 evaluate and commit name assignment.
- S6-S8 evaluate an `If` guard and select disjoint Boolean branches.
- S9-S11 evaluate the used list iterable, initialize a loop, and handle zero
  iterations.
- S12 is the exact-body operational loop bridge discussed below.
- S13-S14 provide ordinary descending iteration and loop-variable binding for
  all other bodies; `owise` makes S12 the only preemption.
- S15-S17 evaluate return expressions and implement top-level function return.
- S18-S20 evaluate integer/Boolean literals and environment names.
- S21 implements the only used unary-minus form.
- S22-S24 implement left-to-right integer addition.
- S25-S29 implement left-to-right `==`, `>`, and `<=`; operand orientation is
  correct.
- S30 specializes `len(E) == 0` to constructor emptiness at priority 40. It is
  equivalent to the generic length/equality path for lists and enables
  symbolic case splitting.
- S31-S32 are disjoint empty/nonempty list-emptiness rules.
- S33-S34 evaluate the used unary `len` call and compute recursive length.
- S35-S36 evaluate the only used `[-1]` subscript and return nonempty `last`.
  Empty use sticks because `last(.IList)` is undefined; the program's empty
  branch prevents that path.

All constructors in `solution.mpy` map to these declarations and rules:
`Module`, `FuncDef`, `Params`, statement lists, `If`, `Return`, `Assign`,
`For`, `Name`, `Int`, `Bool`, unary minus, addition, the three comparisons,
unary `len`, and `[-1]`. Unsupported unused Python forms remain visibly
unmodeled, which is acceptable for minimal generated semantics.

### S12 operational bridge

`/candidate/semantic.k:51-63` matches only the exact loop variable and exact
two-statement body from the submitted program, on a nonempty list, with
integer-valued `drops` and `previous`. It replaces ordinary iteration with:

- `drops := D + dropsFrom(P, I::IS)`;
- `previous := last(I::IS)`;
- `value := last(I::IS)`;
- preservation of all other environment entries, `<input>`, and the arbitrary
  continuation admitted by the `<k> ... </k>` frame.

This state result follows by induction over S13/S14 and the ordinary body
rules: the head contributes `dropBit(P,I)`, the recursive tail starts with
previous `I`, and the last bound value is the list's last element. The rule has
no fresh or opaque value; `dropsFrom` is exhaustively and decreasingly defined
by V7-V8.

Nevertheless, S12 is result-bearing and uses the same `dropsFrom` symbol that
feeds `cyclicDrops` and the final postcondition. The candidate has no
bridge-free universal connection claim, so its `#Top` alone would be circular
evidence for this connection.

I made two fresh bridge-free symbolic attempts:

- a theorem over the rule's full `REST` map and arbitrary continuation built
  but exited 1 with a residual symbolic-map lookup branch
  (`evidence/bridge-connection-spec.k` and
  `evidence/bridge-connection-kprove.log`);
- a theorem narrowed to the exact environment shape reachable before this
  program's loop produced no result in approximately 120 seconds and was
  interrupted with status 130
  (`evidence/bridge-reachable-connection-spec.k` and
  `evidence/bridge-reachable-connection-kprove.log`).

These failures are not candidate proof failures—the claims are
reviewer-authored validation probes—but they mean a machine-checked universal
connection was not obtained. Bridge-free concrete execution agrees on all
reviewer cases. Static induction shows the rule is faithful, and no satisfiable
state was found where S12 enables a false result, state, or control conclusion.
Accordingly I record a narrower trust/evidence limitation rather than label
the rule unsound.

The broad top-level return rule and launch convention likewise exceed a full
Python semantics, but they are sound for the only function/control context the
submitted program uses and do not fabricate any used result.

No local rule is classified as materially unsound; therefore there is no
required false-conclusion witness to report.

## 6. Fresh non-vacuity test

I did not rely on a candidate mutation artifact. The fresh
`evidence/spec-vacuity-reviewer.k` keeps the nonempty precondition and final
environment but changes the result obligation to `bVal(false)`.

The mutation is demonstrably false for the satisfying input
`[3,4,5,1,2]`: fresh K execution, candidate Python, trusted canonical, and the
rotation oracle all return true
(`evidence/nonvacuity-witness.log`).

The mutated specification successfully parsed and compiled to KORE with
`kprove --dry-run` exit 0
(`evidence/nonvacuity-dry-run.log`). Actual proof then exited 1 with
`WarnStuckClaimState`. The residual shows the expected unmet obligation:
`false` is not equal to
`dropBit(last(I::IS),I) + dropsFrom(I,IS) <= 1`. This is a semantic proof
failure, not a parser error, timeout, unreachable mutation, or unrelated crash.
See `evidence/nonvacuity-kprove.log`.

The positive proof is therefore discriminating and result-constraining.

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Conditional on the reconstructed generated K definition, the exact submitted
program term:

- returns true on empty input; and
- for every nonempty finite K integer list, any completed modeled execution has
  `bVal(cyclicDrops(list) <= 1)` with the exact final `arr`, `drops`,
  `previous`, and `value` bindings stated in the claim.

This is a universal inductive-list result, not finite unrolling or a set of
examples. The trusted regeneration and KAST comparison connect the formal term
to `solution.py`; the mathematical circular-drop argument connects the
returned predicate to the source contract on unique lists.

### Trust ledger

| Boundary | Influence | Evidence and assessment |
|---|---|---|
| Trusted `/reference/prompt.py`, `canonical.py`, and `py2mpy.py` | Contract, executable oracle, source-to-constructor translation | Launcher hashes and byte comparisons pass. Accepted trusted inputs. |
| K `INT`/`BOOL` | All arithmetic, comparisons, and returned Boolean | Standard mathematical-integer/Boolean primitives; appropriate for used Python integer behavior. |
| K `MAP`, finite list, and sequencing machinery | Environment lookup/update, inputs, evaluation order | Standard K primitives; no candidate-local axiom changes them. |
| K parser, kompilers, LLVM/Haskell backends, and `kprove` | All dynamic and symbolic results | Independently rebuilt with recorded K v7.1.293; ordinary toolchain trust boundary. |
| Generated launch and expression/statement semantics S1-S36 | Meaning of the translated program | Exhaustive static audit and concrete cross-checks. Minimal coverage is complete for every used construct. |
| S12 exact-loop operational bridge | Computes `drops`, final loop bindings, and therefore the result | Fully defined and statically faithful; bridge-free concrete evidence passes. No candidate or successful reviewer universal connection theorem. This is the principal concern. |
| `rotationSortable = cyclicDrops <= 1` to “some right rotation is sorted” | Human-facing theorem intent | Informal two-direction mathematical argument above plus zero-mismatch differential evidence. Not a separate K theorem; non-fatal concern. |
| Differential and concrete tests | Translator/implementation/semantics bridge on tested cases | Reproducible finite evidence only; not used as universal proof. |

There are no opaque local symbols or unconstrained oracles. `last` is partial
only where it should be, and no entry execution reaches its undefined empty
case. There is no external I/O, heap, allocation, exception, mutation of the
input list, or concurrency in the submitted construct set.

### Decision

The proof is legitimate: it reconstructs, is universal over the material
source domain, constrains the result, executes a mechanically identical program
term, survives body sensitivity, and rejects a meaningful false result. It is
not `FAIL`: there is no domain narrowing, substituted program, vacuity, failed
positive claim, or witnessed false semantic conclusion.

The proper classification is `CONCERNS / LEGIT`, not `PASS`, because the
formal closure substantially depends on an exact task-specific operational
summary whose universal bridge-free connection is not part of the candidate
and was not independently machine-closed, plus an informal summary-to-contract
equivalence. Both limitations are visible and do not enable a known false
conclusion on the intended domain.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
