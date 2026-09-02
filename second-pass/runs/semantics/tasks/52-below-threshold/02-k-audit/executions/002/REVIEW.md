# Independent adversarial audit: 52-below-threshold

This audit used the approved `using-kit` and `validating-proof` workflows. All
candidate and generation material was treated as untrusted. Execution used
fresh source copies under `/tmp/audit-work/52-below-threshold`; no
candidate-built K definition or cache was reused.

The candidate contains a sound, discriminating K reachability proof for a
strictly narrower theorem: lists of K integers and an integer threshold. It
does not prove the source contract for an unrestricted list of numbers, because
numeric floats accepted by the prompt and canonical implementation cannot
instantiate `IS:IntSeq`. The benchmark expressly maps this material
HumanEval-domain narrowing to `FAIL / NOT_LEGIT`.

## 1. Input and provenance integrity

The launcher record `/audit-input.json` is present and declares:

- `record_layout = legacy-selected-stage1`
- `problem_id = 52-below-threshold`
- `condition = semantics`
- `semantics_mode = SUPPLIED_SEMANTICS`
- `mount_reference_semantics = true`

This agrees with the rendered audit condition. The required trusted mount
`/reference/reference-semantics` is present, so there is no mode/mount
infrastructure contradiction.

All records required for `legacy-selected-stage1` are present, readable,
regular files (or the required trace directory), and not symlinks:
`/run.json`, `/task.json`, `/generation-result.json`,
`/generation-evidence/invocation.json`, `metrics.json`, `usage.json`,
`codex-last.txt`, `codex-output.log`, `prompt.txt`, and the one structured
JSONL trace. Historical runtime metrics were not recorded; the layout permits
that absence. The present legacy import records were also inspected.

The JSON value of `/audit-campaign-lock.json` exactly equals the
`audit_campaign` block in `/audit-input.json`. Its direct SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
matching the launcher record. Direct hashes of every launcher-declared mounted
file match. The trace JSONL directly hashes to
`142c2dcc211262f22d39d76b2461ea85f933900d06b1ff3ad3ac03d7df163e69`,
matching both invocation and result records.

The candidate `prompt.py` and `py2mpy.py` are byte-identical to
`/reference/prompt.py` and `/reference/py2mpy.py`. A recursive,
no-dereference comparison of candidate and trusted `reference-semantics/`
found exactly the same 24 regular files, paths, modes, and bytes, with no
additional, missing, mistyped, or symlinked entry. All five required proof
deliverables are present as regular files.

The complete 453-event structured trace was parsed, pairing all 105 historical
tool calls with 105 outputs. The complete 23,495-line generation console log
was read and hashed. Their historical `#Top` and final report were not used as
proof evidence.

Evidence:

- `evidence/01-provenance.sh` and `evidence/01-provenance.log`
- `evidence/trace_summary.py` and `evidence/trace-summary.log`
- `evidence/generation_log_summary.py` and
  `evidence/generation-log-summary.log`

Stage result: integrity gate passed; no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract is: `below_threshold(l, t)` returns true exactly when
every number in `l` is strictly below `t`; an empty list returns true, and any
element equal to or above `t` makes the result false.

The trusted canonical implementation loops over `l`, returns false at the first
`e >= t`, and otherwise returns true. The submitted `solution.py` implements
the same algorithm, differing only in the local loop-variable name.

Running the trusted translator on the scratch-copied `solution.py` exited 0.
The result was byte-identical to submitted `solution.mpy`; both have SHA-256
`964b3c4dfcbb018f5d3cd8aff7b52ec28ff49f173082a5b24c491072ff10dafe`.
The submitted Python doctests also exited 0.

The independent differential script imports the trusted canonical module and
submitted solution as separate modules. It ran:

- both documented examples;
- empty, equal, one-below, one-above, negative, early/middle/late-failure,
  large-integer, finite-float, and mixed-numeric cases;
- every list of length 0 through 5 over `{t-1,t,t+1}` for thresholds
  `-2, 0, 7`; and
- 500 deterministic seeded lists of length 0 through 25 containing integers
  and finite quarter-valued floats.

All 1,608 cases matched in value and result type. The input-manifest hash is
`bd23fa92e77a03d8c05e1058416b69e35dfd3b4ecd31fcb47f9c4c5203b637c0`.
This finite test supports implementation fidelity; it is not the K proof.

Evidence:

- `evidence/differential.py`
- `evidence/02-fidelity.sh` and `evidence/02-fidelity.log`

Stage result: submitted Python and translation are faithful.

## 3. Clean proof reconstruction

K 7.1.293 and Python 3.10.12 were available. The candidate tree had no retained
K compiled definition; its Python bytecode cache was discarded in scratch.
The reviewer created an independent concrete harness from the copied submitted
source and translated it with the trusted translator.

Exact fresh commands and outcomes:

```text
kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition reviewer-runtime-kompiled
exit 0

krun reviewer-concrete.mpy --definition reviewer-runtime-kompiled --output pretty
exit 0; final <k> .K, <stack> .List, <ret> noRet, <exc> NoExc, <exit-code> 0

kompile verification.k --backend haskell --main-module VERIFICATION-BASE --syntax-module VERIFICATION-BASE --output-definition reviewer-verification-base-kompiled
exit 0

kprove spec.k --definition reviewer-verification-base-kompiled --spec-module LOOP-SPEC --output pretty
exit 0; #Top

kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module VERIFICATION --output-definition reviewer-verification-kompiled
exit 0

kprove spec.k --definition reviewer-verification-kompiled --spec-module SPEC --output pretty
exit 0; #Top
```

The LLVM harness covers the examples, empty list, strict/equal/above boundary,
early and late failure, negatives, and large integers. Every command has its
own bounded terminal log with command exit status.

Evidence:

- `evidence/03-reconstruction.sh`
- `evidence/03-translator.log`
- `evidence/03-llvm-kompile.log` and `evidence/03-llvm-krun.log`
- `evidence/03-base-kompile.log` and `evidence/03-loop-proof.log`
- `evidence/03-final-kompile.log` and `evidence/03-entry-proof.log`

Stage result: both positive claims reconstruct cleanly. This establishes
closure only under the audited theory.

## 4. Adequacy and real-program pinning

### Claims in plain language

`LOOP-SPEC` has no explicit `requires`; its sorted variables implicitly require
`IS` and `_ORIGINAL` to be `IntSeq`, `T` and `_OLD` to be `Int`, and
`BUILTINS` to be a `Scope`. It starts at the real loop head over remaining
integer sequence `IS`, with the exact loop body, final `Return(true)`, and
`#endcall`. It includes the exact callee/module scopes, one exact frame, empty
heap, and all control/status cells. It claims termination at the Boolean
`belowThresholdSpec(IS,T)` while popping the frame and restoring the module
configuration.

`SPEC` likewise has no explicit `requires`. Its implicit domain is
`IS:IntSeq, T:Int`. From the empty module configuration, it directly calls the
submitted closure on the abstract integer-list representation and claims the
Boolean recursive conjunction `I < T` over all elements.

### Pinning

Trusted regeneration first pins `solution.mpy` to `solution.py`. The reviewer
then used K's parser and macro expander on both submitted `solution.mpy` and a
ground `#belowThresholdCall`. The expanded submitted function-body KAST and
executed closure-body KAST have identical SHA-256
`98fe85e2bb17c3e0d5fbb007c91076604f04b91e20f902815c1e9d975c0560da`.
Their parameter KASTs are also identical, with SHA-256
`555458b7b6b9341e59b6909a6ed6d408af9754c8f9748a608db3403534edb5f8`.
The submitted binding is exactly `"below_threshold"`, and fixed `FuncDef`
semantics creates this exact `closureVal(params, body, 0)` in the empty module
scope. Directly calling that closure is therefore a demonstrated inert
normalization, not a substituted body or oracle.

The loop helper is the translated `For` control point. The summary rule's
complete term/configuration is identical to the bridge-free `LOOP-SPEC`
theorem, and it matches the recursive control point actually reached after an
element is bound.

Satisfiable witnesses include:

```text
IS=.IntSeq, T=0                         -> true
IS=iCons(5,.IntSeq), T=5               -> false
IS=iCons(-4,iCons(-10,.IntSeq)), T=-3  -> true
```

All exact configuration variables were instantiated in the evidence. The
recursive K result, trusted canonical result, and submitted Python result agree
for every witness.

The body-sensitivity mutation changed the program term actually executed:
the `number >= t` branch returned true instead of false. Its fresh base
definition built successfully, but the bridge-free loop proof exited 1 with a
stuck implication on the reachable `I >= T` branch. Thus the theorem depends
on the submitted body.

Evidence:

- `evidence/pinning_check.py`, `evidence/witnesses.py`
- `evidence/04-pinning-and-inventory.sh` and
  `evidence/04-pinning-and-inventory.log`
- `evidence/05-body-sensitivity.sh`,
  `evidence/05-body-mutant-build.log`, and
  `evidence/05-body-mutant-proof.log`

### Material adequacy failure

The proof input is not a symbolic Python numeric list. `IS:IntSeq` can encode
only K `Int` elements. The trusted prompt annotates only `l: list` and says
“all numbers”; it does not narrow elements to integers. The canonical and
submitted implementations both have ordinary defined numeric behavior on
floats. For example:

```text
below_threshold([4.5], 5) = True
below_threshold([5.0], 5) = False
```

Neither source-contract input has an `IS:IntSeq` instance. The supplied
semantics even contains float comparison support, but the candidate theorem
does not use a `ValSeq`/numeric domain that can include it. This is not a
counterexample to the integer theorem; it is a material omitted portion of the
source-contract domain. Under the benchmark instruction, the corresponding
Kit status is `SOUND-BUT-LIMITED`, which must map to `FAIL / NOT_LEGIT`.

Stage result: real body pinning passed, full-contract adequacy failed.

## 5. Rule-by-rule static soundness review

The exhaustive inventory covers all 26 audited K files: the 24 supplied files,
`verification.k`, and `spec.k`. It contains 1,026 declaration blocks:
703 rules, 232 syntax declarations, 5 contexts, one configuration, two claims,
29 modules, 29 endmodules, and 25 requires. Attribute-bearing counts are:
147 function, 108 total, 48 priority, 36 concrete, 26 owise, 25 symbol,
22 no-evaluators, 7 macro, one macro-rec, two strict, and one seqstrict.
There are no `functional` or `simplification` declarations.

Every declaration and full normalized rule block, with source range and hash,
is preserved in `evidence/04-pinning-and-inventory.log`; the rule-by-rule
decision method and target-slice assessment are in
`evidence/05-static-review.md`.

The material source constructs map to:

| Submitted construct | Declaration/evaluation rules |
|---|---|
| function params/body | `syntax.k`; `functions.k` closure/return/pop; `call.k` callee, args, exact frame |
| docstring expression | `Str`, `Expr`; `str.k` ASCII construction; expression discard |
| `for number in l` | `For`, `#loop`, `#iterNext`, `#iterYield/#iterDone`, `#bindTgt`, `#loopLbl` |
| names `l`, `number`, `t` | scope lookup in `core.k`; exact target binding in `tuple.k` |
| `number >= t` | comparison contexts/dispatch in `operators.k`; exact `>=Int` in `int.k` |
| `if` | Bool literal, `truthy(Bool)`, and `#branch` rules |
| early/final return | `Return`, abrupt continuation discard, `#pop`, exact frame/scope restoration |

All used fixed rules preserve evaluation order, binding, early-return control,
and every claimed cell. The proof imports `MPY`, not concrete-only
`MPY-CONCRETE`. None of the 25 opaque supplied symbols is reached by this
integer theorem.

### Local extensions

`intsToVals(IntSeq)` is a fresh proof representation, not a function or result
oracle. Its two priority-40 iterator rules are disjoint, exhaust `IntSeq`, and
exactly mirror the fixed empty/cons list iterator transitions while preserving
all other cells. The only material operation performed on `l` is iteration.
This is an explicit structural input-encoding boundary; it does not justify
float coverage.

`belowThresholdSpec` has disjoint empty/cons equations, complete `IntSeq`
coverage, and structural descent. It computes exactly the requested universal
predicate on integers.

All three body/call declarations are macros. Mechanical expansion proves exact
constructor identity with the submitted body and parameters.

The `VERIFICATION` summary rule is a derived operational bridge. After
normalizing only `claim`/`rule` and label/priority syntax, its complete source
hash equals the `LOOP-SPEC` claim hash:
`181316c3340f9212e4277e3c2af82cf435a5c0f143e12da4c1dcf2d94e42f2bd`.
`LOOP-SPEC` imports `VERIFICATION-BASE`, which does not contain or import this
bridge, and fresh reconstruction proves it `#Top`. The bridge has no `<k>`
ellipsis and therefore admits no extra continuation. It exactly reads/writes
`k`, `env`, `scopes`, `scopeLoc`, `heap`, `heapLoc`, `stack`, `ret`, `exc`,
and `exit-code`; the abstract builtins scope is preserved unchanged. Its match
domain is therefore contained in its bridge-free universal theorem.

The supplied LLVM compiler reported non-exhaustive total-function warnings for
unused patterns in `mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and
`valSeqAt`. These declarations are fixed supplied semantics, unreachable on
the target execution, and supply no equation used in either proof. No concrete
false equation witness was found, so they are recorded as narrower evidence
gaps rather than mislabeled unsound rules.

No rule is claimed unsound in this review. The rejection is the formal domain
restriction, for which a false-rule witness is inapplicable.

Evidence:

- `evidence/inventory_k.py`
- `evidence/05-declaration-lines.txt`
- `evidence/05-static-review.md`
- `evidence/summary_compare.py`
- `evidence/05-static-checks.sh` and `evidence/05-static-checks.log`

Stage result: rule theory is sound for the stated integer theorem; the theorem
is materially too narrow.

## 6. Fresh non-vacuity test

The reviewer created a new specification module that changes the entry result:

```text
belowThresholdSpec(IS,T)
  -> notBool belowThresholdSpec(IS,T)
```

This is demonstrably false for the satisfiable exact entry state
`IS=.IntSeq, T=0`: both Python implementations and the original specification
return true, while the mutation demands false.

Exact commands:

```text
kprove reviewer-spec-vacuity.k --definition reviewer-verification-kompiled --spec-module REVIEWER-SPEC-VACUITY --dry-run --output pretty
exit 0

kprove reviewer-spec-vacuity.k --definition reviewer-verification-kompiled --spec-module REVIEWER-SPEC-VACUITY --output pretty
exit 1
```

The dry run successfully produced the backend proof command. The actual proof
failed with `WarnStuckClaimState`; its residual explicitly has `<k> true ~>
.K </k>` and `IS = .IntSeq`. This is the expected unmet result, not a parser
error, timeout, unrelated crash, or unreachable mutation.

Evidence:

- `evidence/06-non-vacuity.sh`
- `evidence/06-mutation-dry-run.log`
- `evidence/06-mutation-proof.log`

Stage result: the integer-domain proof is result-constraining and non-vacuous.

## 7. Proven versus assumed accounting

The successful reachability proof establishes this precise partial-correctness
statement:

> For every finite inductive sequence of mathematical K integers `IS` and
> integer `T`, executing the exact submitted closure body from the specified
> empty module/call configuration on the `intsToVals(IS)` iterator
> representation reaches a Boolean equal to the recursive conjunction
> `forall I in IS, I < T`, with the exact claimed frame/scope/control cleanup.

The proof is not a theorem over arbitrary Python lists or every value described
as a number.

Trust and evidence ledger:

| Boundary | Dependents | Assessment |
|---|---|---|
| K 7.1.293 parser, Haskell backend, reachability logic, and builtin Int/Bool/Map/List theories | both claims | Standard machine-checking trust boundary; versions and fresh commands recorded. |
| Trusted mounted translator | source-to-`solution.mpy` bridge | Direct trusted regeneration is byte-identical; translation correctness itself is trusted as required input. |
| Supplied `MPY` semantics | program execution | Integrity is exact. Used operational rules were statically audited; unused minimal-language behavior is excluded. |
| `IntSeq` to integer-list structural interpretation | entry input | Universally recursive iterator rules give the only used observation. Acceptable for the integer theorem, but it excludes floats and is the adequacy failure. |
| Direct closure in place of module definition/name lookup | program pinning | Fixed `FuncDef` rule plus mechanical KAST equality establishes the exact closure in module environment 0. No shadowing is possible in the exact initial scope. |
| `belowThresholdSpec` | final value | Fully defined, disjoint, descending equations; no opaque or fresh result. |
| Loop summary rule | end-to-end claim | Exact bridge-free `LOOP-SPEC` connection theorem, complete context containment, body mutation rejection, and opposite-result rejection. |
| Supplied opaque float/sort/digest symbols | none | Not reached by either proof and provide no proof power here. |
| Python differential and LLVM harness | implementation/intent evidence | Finite evidence only; never substituted for universal K proof. The float cases specifically expose omitted theorem scope. |
| Manual source-to-proof maintenance | immutable artifact identity | Mechanical comparison passes for this candidate. Lack of automatic regeneration is only a maintenance observation. |

Kit Gate A passes for the integer theorem. Gate B fails because the formal
domain materially narrows the source contract. Gate C is auditable: all trust
boundaries, commands, inputs, statuses, and residuals are preserved. The
benchmark's controlling decision boundary converts this sound-but-limited
integer theorem to a failed legitimacy verdict for the requested proof.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
