# Independent adversarial review: 52-below-threshold

## Outcome

The reconstructed K proof is sound and result-constraining for every finite list
of K integers and integer threshold. It executes a direct closure whose
parameters and body are syntactically identical to the trusted regeneration of
the submitted `solution.py`; the only derived operational summary is exactly the
loop claim separately proved without that summary.

I assign **CONCERNS / LEGIT**, rather than PASS, for three non-fatal scope and
auditability limitations:

1. The formal domain is `IntSeq`, while the prompt annotates only `l: list` and
   calls its elements “numbers.” Floating-point and other Python numeric values
   are not covered by the K theorem.
2. The entry claim directly calls the exact closure body. It does not include
   loading the submitted `Module`, executing `FuncDef`, and looking up
   `below_threshold` in the module scope. Static term identity and the supplied
   one-step `FuncDef` rule make this a sound bridge here, but that bridge is
   outside the reachability claim.
3. `run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`, and
   any structured generation trace are absent. Fresh reconstruction makes the
   proof independently checkable despite that missing candidate provenance.

No candidate-provided compiled definition, cache, prior report, or claimed
`#Top` was trusted or reused.

## 1. Input and provenance integrity

The rendered mode and trusted mounts are consistent: this is
`SUPPLIED_SEMANTICS`, and `/reference/reference-semantics` exists. Therefore
there is no infrastructure-mode breach.

The complete integrity run is
[stage1-integrity.log](evidence/stage1-integrity.log), produced by
[audit_stage1.sh](evidence/audit_stage1.sh). Its material results are:

- `prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`, `spec.k`, and
  `verification.k` are regular files, not symlinks.
- The candidate prompt is byte-identical to `/reference/prompt.py`
  (`cmp` exit 0).
- The candidate translator is byte-identical to `/reference/py2mpy.py`
  (`cmp` exit 0).
- Recursive `diff -qr --no-dereference` of the candidate and trusted
  `reference-semantics/` trees exits 0. There are no missing, additional,
  changed, mistyped, or symlinked entries in that tree.
- The whole candidate tree has zero symlinks.
- `run-input.json`, `metrics.json`, `codex-last.txt`, and
  `codex-output.log` are all missing. No top-level structured trace matching
  the checked trace/generation names is present.

The candidate's `__pycache__/solution.cpython-310.pyc` was treated as an
untrusted generated cache and was not copied. The clean source copy was created
by [prepare_scratch.sh](evidence/prepare_scratch.sh), with the exact copied
files listed in
[scratch-preparation.log](evidence/scratch-preparation.log). Trusted semantics,
prompt, translator, and canonical implementation were copied from `/reference`,
not from candidate caches or compiled outputs.

Toolchain evidence is:

- [toolchain-kompile-version.log](evidence/toolchain-kompile-version.log):
  K `v7.1.337`, exit 0.
- [toolchain-kprove-version.log](evidence/toolchain-kprove-version.log):
  K `v7.1.337`, exit 0.
- [toolchain-python-version.log](evidence/toolchain-python-version.log):
  Python `3.10.12`, exit 0.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract is: `below_threshold(l, t)` returns `True` exactly when
every element of `l` is strictly less than `t`. An empty list returns `True`.
An element equal to the threshold is not below it and therefore causes
`False`.

The trusted canonical implementation iterates through `l`, returns `False` on
the first `e >= t`, and otherwise returns `True`. The generated implementation
does the same; its only algorithmic textual difference is the loop variable
name `number` instead of `e`.

### Translation identity

The trusted translator was run from the scratch copy:

```text
python3 py2mpy.py solution.py > regenerated-solution.mpy
cmp -s regenerated-solution.mpy submitted-solution.mpy
```

Both commands exited 0. The regenerated and submitted terms have the same
SHA-256:

```text
964b3c4dfcbb018f5d3cd8aff7b52ec28ff49f173082a5b24c491072ff10dafe
```

See
[translation-byte-identity.log](evidence/translation-byte-identity.log) and
[translate_and_compare.sh](evidence/translate_and_compare.sh).

### Independent differential execution

[differential_test.py](evidence/differential_test.py) imports the trusted
canonical and generated functions independently. It does not use K proof
equations as an oracle. The exact run and reproducible input descriptions are
in [differential-test.log](evidence/differential-test.log).

It exercised 24,659 cases:

| Group | Cases |
|---|---:|
| Documented examples | 2 |
| Empty, equality, sign, and arbitrary-precision integer boundaries | 12 |
| Every first/middle/last early-return position at `t-1`, `t`, and `t+1` | 33 |
| Exhaustive lists of length 0–4 over elements -3…3, thresholds -3…3 | 19,607 |
| Deterministic generated integer cases, seed 520052 | 5,000 |
| Extended numeric cases outside the K claim | 5 |

There were zero mismatches and zero exceptions. The five extended cases
included floats, infinities, and booleans; they support source-to-canonical
fidelity only and do not enlarge the K theorem's `IntSeq` domain.

## 3. Clean proof reconstruction

All builds occurred in `/tmp/audit-work/52-below-threshold` from fresh source.
The candidate had no compiled definition reused by this audit.

### Fresh concrete definition

The exact LLVM build was:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

It exited 0; see
[kompile-runtime-llvm.log](evidence/kompile-runtime-llvm.log). Compiler
non-exhaustiveness warnings concern unused helpers such as float conversion,
`mapStrVS`, `joinCodes`, and out-of-bounds `valSeqAt`; none is reachable from
this submitted program.

The reviewer harness
[k-concrete-audit.py](evidence/k-concrete-audit.py) was translated with the
trusted translator and executed as:

```text
krun k-concrete-audit.mpy --definition runtime-kompiled --output pretty
```

It checked both documented examples, empty input, strict/equality boundaries,
failure at every loop position, negative integers, and large integers. The run
exited 0 with final `<k> .K </k>`, `<exc> NoExc </exc>`, and exit code 0.
See [k-concrete-preparation.log](evidence/k-concrete-preparation.log) and
[krun-concrete-audit.log](evidence/krun-concrete-audit.log).

### Fresh positive proof targets

The loop definition was built without the derived loop rule:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION-BASE --syntax-module VERIFICATION-BASE \
  --output-definition verification-base-kompiled
```

This exited 0
([kompile-verification-base.log](evidence/kompile-verification-base.log)).
The positive loop claim was then run independently:

```text
kprove spec.k --definition verification-base-kompiled \
  --spec-module LOOP-SPEC --output pretty
```

It exited 0 and printed `#Top`
([kprove-loop-spec.log](evidence/kprove-loop-spec.log)).

The complete definition was separately built:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module VERIFICATION \
  --output-definition verification-kompiled
```

This exited 0
([kompile-verification.log](evidence/kompile-verification.log)). The entry
claim was run as:

```text
kprove spec.k --definition verification-kompiled \
  --spec-module SPEC --output pretty
```

It exited 0 and printed `#Top`
([kprove-entry-spec.log](evidence/kprove-entry-spec.log)).

These are the only two positive target claims in `spec.k`, and both satisfy the
required success condition independently.

## 4. Adequacy and real-program pinning

### Plain-language claims

The `LOOP-SPEC` precondition has:

- a remaining integer sequence `IS` represented as
  `list(intsToVals(IS))`;
- loop target `number` and the exact translated loop body;
- the exact trailing `Return(true) ~> #endcall`;
- a live function frame at scope 1 containing integer `t`, an arbitrary
  previous integer `number`, and the original input representation;
- the exact caller frame, empty heap, normal return/exception state, and exit
  code 0.

Its postcondition says that the frame has returned to the caller and the
function result is `belowThresholdSpec(IS,T)`, the conjunction of `I <Int T`
over all remaining elements. A satisfying example is `IS = .IntSeq`, `T = 0`,
`_ORIGINAL = .IntSeq`, `_OLD = 0`, and `BUILTINS = builtinsScope` with the
displayed exact maps and cells.

The `SPEC` precondition is the exact empty module-level state and arbitrary
well-sorted `IS:IntSeq` and `T:Int`. Its postcondition is the Boolean
`belowThresholdSpec(IS,T)`. A satisfying instance is the empty list with
threshold 0.

Neither postcondition contains a free result variable or a one-way
implication. `belowThresholdSpec` is a total, constructor-recursive Boolean:

```text
belowThresholdSpec(.IntSeq, T) = true
belowThresholdSpec(iCons(I, REST), T)
  = (I <Int T) andBool belowThresholdSpec(REST, T)
```

Thus the returned value is fully constrained, including the equality boundary.

### Pinning to the submitted term

The entry `<k>` cell expands to a direct `Call` of:

```text
closureVal(("l", "t", .ParamNames), belowThresholdBody, 0)
```

It does not start from `#loadAll(Module(...))`. I therefore checked the
factoring rather than accepting its comment:

- submitted `solution.mpy` equals the trusted regeneration;
- `belowThresholdLoopBody` equals the submitted `For` body's third argument;
- after expanding that loop macro, `belowThresholdBody` equals the complete
  submitted `FuncDef` body;
- `#belowThresholdCall` is the expected direct closure call with the exact
  parameters and body.

All four checks are true in
[program-pinning-v2.log](evidence/program-pinning-v2.log), generated by
[pinning_check.py](evidence/pinning_check.py). The script accounts for K's two
equivalent surface spellings of an empty `Stmts` list: omitted text and
`.Stmts`.

The submitted module contains only this `FuncDef`; the fixed `FuncDef` rule
would bind the same closure in scope 0. Consequently the direct-call factoring
does not substitute another algorithm or skip a property-bearing top-level
effect. The omission of module loading and name lookup remains a documented
formal-scope concern, not a soundness failure.

### Concrete satisfying substitutions

[ground-spec.k](evidence/ground-spec.k) substitutes four satisfying inputs:
empty/0, both documented examples, and `[5]/5`. All four K claims collectively
proved `#Top` with exit 0
([kprove-ground-witnesses.log](evidence/kprove-ground-witnesses.log)).
Both Python implementations returned the same claimed values
([ground-witnesses-python.log](evidence/ground-witnesses-python.log)):

```text
([], 0)                         -> True
([1, 2, 4, 10], 100)           -> True
([1, 20, 4, 10], 5)            -> False
([5], 5)                        -> False
```

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[inventory_k.py](evidence/inventory_k.py) enumerates every source-level
`requires`, module/import, syntax declaration, configuration, context, rule,
claim, and relevant attribute in the supplied semantics, helper files,
`verification.k`, and `spec.k`. Its complete 1,120-record output is
[static-rule-inventory-v2.log](evidence/static-rule-inventory-v2.log).

The inventory contains 232 syntax records, one configuration, five contexts,
703 rules, and two claims. It identifies 147 `function`, 108 `total`, 48
`priority`, 26 `owise`, 36 `concrete`, 25 `symbol`, and 22 `no-evaluators`
occurrences. There are no `functional` or `simplification` declarations.

Unused fixed-semantics declarations are still listed individually. They cannot
be reached from this program, entry term, loop term, or postcondition, so no
false conclusion witness on the intended integer-list execution exists for
them. In particular, the supplied opaque float, sort, and MD5 symbols are not
dependencies of either proof.

### Complete proof-local inventory and decisions

| Extension | Class and decision |
|---|---|
| `syntax ValSeq ::= intsToVals(IntSeq)` | Fresh typed input representation. It has no equation that can choose a result. Acceptable low-level boundary. |
| Empty `#iterNext(list(intsToVals(.IntSeq)))` rule | Returns `#iterDone`, exactly the fixed list iterator behavior for `.ValSeq`. Sound. |
| Cons `#iterNext(list(intsToVals(iCons(I,REST))))` rule | Yields exactly `I` and represents the tail by `REST`, matching fixed `vCons` iteration. Sound. |
| `belowThresholdSpec` declaration and two equations | Total structural recursion over `IntSeq`; guards are constructor-disjoint, coverage is exhaustive, recursion descends. Sound mathematical definition. |
| `belowThresholdLoopBody` syntax/rule | Compile-time macro, exact submitted loop body; no execution replacement. Sound. |
| `belowThresholdBody` syntax/rule | Compile-time macro, exact submitted function body; no execution replacement. Sound. |
| `#belowThresholdCall` syntax/rule | Compile-time macro for a direct call of that exact closure with the represented input and threshold. Sound, with the module-load scope limitation recorded above. |
| Derived loop rule in `VERIFICATION` | Operational summary, but its complete rule body is identical to the separately proved `LOOP-SPEC` claim. Sound derived lemma. |

The two iterator rules are disjoint from each other (`.IntSeq` versus `iCons`)
and from the supplied list iterator rules (`intsToVals(...)` is a distinct
`ValSeq` constructor from `.ValSeq` and `vCons`). Their priority cannot preempt
behavior for ordinary list representations. They model only input iteration;
they do not inspect `T`, call `belowThresholdSpec`, branch on the desired
answer, or fabricate a Boolean.

The derived loop rule matches the entire active continuation
`Return(Bool(true)) ~> #endcall`, not an arbitrary suffix. It matches the exact
function/caller scopes and exact single stack frame. It preserves the arbitrary
builtins scope, empty heap, heap location, normal return/exception state, and
exit code, while performing exactly the frame-pop changes to `<k>`, `<env>`,
`<scopes>`, `<scopeLoc>`, and `<stack>`. `_ORIGINAL` and `_OLD` may be
arbitrary because neither the remaining loop nor body reads them before
overwriting `number`; this does not broaden the result conclusion.

[derived-loop-rule-identity.log](evidence/derived-loop-rule-identity.log)
independently confirms that the summary is absent from `VERIFICATION-BASE` and
that its normalized body exactly equals the proved loop claim body.

As an operational/value-sensitivity check, I changed only the cons iterator
bridge to yield `I +Int 1`. The mutated source is
[bridge-mutated-verification.k](evidence/bridge-mutated-verification.k).
It built successfully
([bridge-mutation-kompile-base.log](evidence/bridge-mutation-kompile-base.log)),
but the loop proof failed with a genuine implication residual and exit 1
([bridge-mutation-loop-proof-failure.log](evidence/bridge-mutation-loop-proof-failure.log)).
For example, `I = 4`, `T = 5` makes the altered execution return `false` while
the original strict-less-than specification is `true`. This demonstrates that
the proof depends on the iterator yielding the real element value.

### Used supplied-semantics path

Every syntax construct in `solution.mpy` and the entry call maps to the
following supplied declarations/rules:

| Construct | Declaration and behavior used |
|---|---|
| `Module`, statement sequence | `syntax.k`; `core.k` `#loadAll`/sequence rules (module load is statically bridged for the entry claim) |
| `FuncDef`, `Params`, closure call | `syntax.k`, `functions.k`, `call.k` |
| docstring `Expr(Str(...))` | `str.k` ASCII `Str` conversion; `controls.k` discards an expression-statement value |
| `For(Name(...), Name("l"), ...)` | strict iterable evaluation; `core.k` lookup; `controls.k` `#loop/#loopStep`; `tuple.k` `#bindTgt` |
| `If` | strict condition evaluation and `controls.k` `#branch` |
| `Compare(..., CmpOp(">=", ...))` | left/right contexts in `operators.k`; integer `applyCmp(">=",...)` in `int.k` |
| `Bool`, `Return` | literal rule in `core.k`; return/frame-pop rules in `functions.k` |
| `list(intsToVals(IS))` | proof-local input representation and the two reviewed iterator rules |

Evaluation order is left-to-right where used: the closure callee is already a
value, arguments pass through `#evalArgs`, parameters bind in order, statements
sequence, the `For` iterable is evaluated once, each yielded integer is bound
before the body, comparison evaluates its two names before integer dispatch,
and `Return` records the value before popping the exact frame. The submitted
function performs no heap mutation or allocation on its unboxed read-only
input. Both normal loop exhaustion and early return restore the caller cells
matched by the claims.

No proof-local declaration is opaque, `no-evaluators`, `functional`, or
`simplification`. No overlap, unguarded totalization, non-descending recursion,
answer-encoding rule, unconstrained oracle, or arbitrary-continuation bridge
was found. Accordingly, this review makes no unsound-rule allegation requiring
a false-conclusion witness.

## 6. Fresh non-vacuity test

The fresh mutation is [spec-vacuity.k](evidence/spec-vacuity.k). It changes the
entry destination from:

```text
belowThresholdSpec(IS,T)
```

to the deliberately false:

```text
notBool belowThresholdSpec(IS,T)
```

The empty-list input with any integer threshold is a satisfying witness:
execution returns `true`, while the mutated destination is `false`.

First, the exact dry-run command was:

```text
kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY --dry-run
```

It exited 0 and emitted a valid `kore-exec --prove` command, establishing that
the mutation parsed and built
([nonvacuity-dry-run.log](evidence/nonvacuity-dry-run.log)).

The actual proof command was:

```text
kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY --output pretty
```

It exited 1 with `WarnStuckClaimState`, not a parser error, timeout, or unrelated
crash. The residual has `<k> true ~> .K </k>` under
`IS #Equals .IntSeq`, exactly the unmet opposite-result obligation. See
[nonvacuity-proof-failure.log](evidence/nonvacuity-proof-failure.log).
The proof is therefore non-vacuous and result-sensitive.

## 7. Proven versus assumed accounting

### What the K proof establishes

Under the supplied MPY semantics plus the reviewed input-representation rules,
for every finite `IS:IntSeq` and every K mathematical integer `T`, the exact
submitted function body, called with the represented integer list and `T` from
the displayed normal initial state, reaches a returned Boolean equal to:

```text
true                              if IS is empty
(I <Int T) andBool result(REST)   if IS = iCons(I, REST)
```

This is a partial-correctness reachability result. The report does not promote
it to a separate machine-checked total-termination theorem, even though the
finite iterator and structural recursion descend in the reviewed rules.

### Trust ledger

| Boundary | Dependence and assessment |
|---|---|
| K `v7.1.337`, its Haskell/LLVM backends, and mathematical Int/Bool hooks | Foundational trusted computing base for all machine results; acceptable and version-recorded. |
| Trusted supplied MPY semantics | Required by `SUPPLIED_SEMANTICS`; candidate copy is exact. Relevant rules were statically reviewed and concretely exercised. Unused fragments and their opaque symbols do not contribute to claim closure. |
| `IntSeq` ↔ read-only Python integer-list representation | The two proof-local iterator rules define the complete observation this function makes. Structurally justified and mutation-sensitive; acceptable low-level input boundary. |
| Direct exact closure call instead of module load/name lookup | Static normalized identity plus the fixed `FuncDef` rule supports it, but the connection is outside the reachability theorem. Concerning but not illegitimate here because the module has no other effect. |
| `belowThresholdSpec` ↔ English “all below threshold” | Its equations are the standard finite universal conjunction. The bridge is ordinary mathematics, not an oracle. |
| `IntSeq` as the intended element domain | `t` is annotated `int`, but `l` has no element annotation and the prose says “numbers.” Integer lists are fully proved; floats/other numerics are excluded. This is the principal intent-scope concern. |
| Trusted canonical implementation and differential testing | Supports source-to-intent fidelity only for the 24,659 tested inputs. It is not used as a substitute for either K claim. |
| Missing candidate generation records | Prevents auditing the candidate's claimed generation narrative. Fresh source reconstruction and reviewer evidence avoid relying on that narrative, but provenance remains incomplete. |

Gate A (real-program soundness and non-vacuity) passes. The theorem is
faithfully tied to the submitted function body and has no result-bearing
oracle. The natural-language/domain bridge and direct-entry factoring have the
documented limitations above, so the strongest warranted user-facing decision
is concerns with legitimacy, not an unrestricted pass.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
