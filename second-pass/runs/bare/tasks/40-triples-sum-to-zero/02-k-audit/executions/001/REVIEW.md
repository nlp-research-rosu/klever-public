# Independent adversarial review: 40-triples-sum-to-zero

## Executive decision

The candidate's positive claims reconstruct from source: the fresh Haskell
definition proves the helper alone, the helper plus entry claim, and all three
claims with `#Top`/exit 0. The submitted `solution.mpy` is also mechanically
pinned to the quoted `solutionProgram`, and the postcondition is
result-constraining and non-vacuous.

The candidate nevertheless fails the required static soundness gate. Two
ordinary rules in the generated semantics are false for terms admitted by that
semantics:

1. `semantic.k:117-118` represents the slice `[1:]` by the ordinary value
   `VInt(1)`. Consequently, a direct integer subscript `l[1]` is also rewritten
   as a tail slice. On input `[10,20,30]`, CPython returns integer `20`, while
   the rebuilt K semantics returns `VList(20 ; 30 ; .Ints)`.
2. `semantic.k:159` rewrites function fallthrough to `VBool(false)`. On the
   same list, a Python function with no return yields `None`, while K yields
   `false`.

Both counterexamples are concrete and preserved in
[`stage5_static_witnesses.log`](evidence/stage5_static_witnesses.log). Neither
bad case is reached by the submitted AST, and no target-specific answer oracle
was found. Nevertheless, the required `validating-proof` soundness contract
expressly disallows globally false off-path rules: these rules can prove false
reachability conclusions for syntax that the candidate itself declares.
Therefore Gate A and the audit fail.

There is also a separate intent/model limitation: with the default CPython
recursion limit, the trusted iterative program returns `True` on a documented
1,153-element witness while the recursive candidate raises `RecursionError`.
That does not refute a normal-return partial-correctness statement, but it
prevents reading the proof as total correctness for every finite Python list.
See [`recursion_boundary.log`](evidence/recursion_boundary.log).

## 1. Input and provenance integrity

### Rendered-mode boundary

The rendered mode is `GENERATED_SEMANTICS`. The trusted
`/reference/reference-semantics` path is absent as required; there is no
contradictory supplied-semantics mount. The trusted inputs
`/reference/canonical.py`, `/reference/prompt.py`, and
`/reference/py2mpy.py` are ordinary regular files. This is not an
infrastructure breach.

The candidate's `prompt.py` and `py2mpy.py` are byte-identical to the trusted
copies:

- prompt SHA-256:
  `9d88f259a8dff048e25628589b4c2a1b4fb22419540df1e34d2d731216ae41dc`
- translator SHA-256:
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`

The exact `cmp`, hash, type, mode-boundary, and symlink checks are in
[`stage1_integrity.sh`](evidence/stage1_integrity.sh) and
[`stage1_integrity.log`](evidence/stage1_integrity.log); the script exited 0.

### Required and extra artifacts

The required source artifacts are present as regular files:
`solution.py`, `solution.mpy`, `semantic.k`, `verification.k`, `spec.k`, and
the executable `prove.sh`. There are no source helper K files and none are
referenced. `run-input.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, and one structured JSONL generation trace are also present.
No candidate symlink or special file was found.

No required artifact is missing, changed, mistyped, or symlinked. The extra
`.kbuild/`, `.kprove/`, `semantic-kompiled/`, and `__pycache__/` entries are
candidate-generated build/cache artifacts. They were treated only as untrusted
extras and were not copied into or used by the audit.

### Untrusted generation claims

`run-input.json` identifies the bare/no-supplied-semantics condition.
`metrics.json` claims a successful, non-timeout generation run.
`codex-last.txt`, `codex-output.log`, and the JSONL trace claim that the final
`prove.sh` run produced `#Top`; the larger logs also show earlier iterative
compile/runtime/proof failures before the claimed success. These records were
read only as provenance claims. Their sizes and hashes are recorded in the
stage-1 log; no verdict relies on them.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

For a finite list of integers `l`, return `True` exactly when there are three
distinct positions `i < j < k` such that
`l[i] + l[j] + l[k] == 0`; otherwise return `False`. “Distinct elements” is
interpreted as distinct positions, as demonstrated by the trusted canonical
implementation's three nested increasing-index loops. Equal values at
different positions are therefore allowed.

The candidate uses a different but appropriate recursive algorithm:
`_has_pair_sum(first, rest)` enumerates each second position and checks the
needed third value only in the later suffix; the entry function enumerates
each first position.

### Translator identity

The audit regenerated the MPY constructor tree with:

```text
python3 /reference/py2mpy.py /tmp/audit-work/candidate-src/solution.py \
  > /tmp/audit-work/regenerated-solution.mpy
```

The command exited 0. `cmp -s` against the submitted scratch copy exited 0,
and both files have SHA-256
`b863637652ba42e8c3117b599f9a96abaa4ccfbd8cac616807adf0b2a54593c3`.
See [`stage2_fidelity.log`](evidence/stage2_fidelity.log).

### Independent differential evidence

[`differential_test.py`](evidence/differential_test.py) independently imports
the trusted canonical entry point and scratch-copied candidate entry point. It
checked:

- all five prompt examples;
- 13 empty, length, duplicate-position, branch-order, sign, and large-integer
  boundaries;
- all 137,257 lists of length 0 through 6 over integers `-3..3`;
- 1,000 deterministic generated lists of length 0 through 30, with every
  other eligible case forced to contain a triple.

The command exited 0 with `total=138275` and `mismatches=0`; exact scope and
output are in [`stage2_fidelity.log`](evidence/stage2_fidelity.log).

The separate default-runtime boundary test deliberately went beyond that
bounded sample. For
`[0] + [1] * 1150 + [-2, 2]`, length 1,153 with recursion limit 1,000, the
trusted iterative function returned `True` while the candidate raised
`RecursionError: maximum recursion depth exceeded in comparison`. The script
and result are
[`recursion_boundary.py`](evidence/recursion_boundary.py) and
[`recursion_boundary.log`](evidence/recursion_boundary.log). This is an
implementation/totality discrepancy, not a wrong Boolean normal return.

## 3. Clean proof reconstruction

Only these candidate source files were copied to
`/tmp/audit-work/candidate-src`: `solution.py`, `solution.mpy`, `semantic.k`,
`verification.k`, `spec.k`, and `prove.sh`. Trusted inputs were copied
separately. Candidate definitions and caches were not reused.

The installed toolchain was K `v7.1.293`. The definitive reconstruction is
[`stage3_reconstruction.sh`](evidence/stage3_reconstruction.sh), with exact
commands, outputs, and statuses in
[`stage3_reconstruction.log`](evidence/stage3_reconstruction.log):

1. Fresh LLVM build of `semantic.k`: exit 0.
2. Sixteen fresh `krun` executions on empty, short, duplicate, true, false,
   signed, example, recursive-branch, and large-integer inputs: every run
   exited 0 and agreed with both Python implementations.
3. Fresh Haskell build of `verification.k`: exit 0.
4. `SPEC.pair-correct` alone: `#Top`, exit 0.
5. `pair-correct` and `triples-correct` together, excluding only
   `program-correct`: `#Top`, exit 0.
6. All three claims, including `program-correct`: `#Top`, exit 0.

The claims were run in dependency layers because `triples-correct` uses the
helper theorem and `program-correct` uses both recursive theorems. An
additional diagnostic removed `pair-correct` while selecting
`triples-correct`; it kept unfolding recursion and was interrupted after 177
seconds. That diagnostic is not a candidate failure and is separately
documented in
[`stage3_filtered_attempt_NOTE.md`](evidence/stage3_filtered_attempt_NOTE.md).

Thus the candidate passes the dynamic reconstruction gate. This `#Top` result
establishes closure only under the submitted generated semantics and
verification theory; it does not validate those rules.

## 4. Adequacy and real-program pinning

### Claims in plain language

There are no explicit `requires` clauses. The preconditions instead come from
sorts and exact cell patterns.

- `pair-correct` (`spec.k:7-15`): for every mathematical integer `FIRST`,
  finite `Ints` suffix `IS`, and arbitrary continuation `RESTK`, invoking the
  exact two-argument `_has_pair_sum` binding in `solutionFunctions` yields
  `VBool(hasPairWith(FIRST, IS))`, preserves `RESTK`, and frames the
  environment, input, and result cells.
- `triples-correct` (`spec.k:19-27`): for every finite `Ints` list `IS` and
  arbitrary `RESTK`, invoking the exact one-argument entry binding yields
  `VBool(hasZeroTriple(IS))`, preserving the continuation and framed cells.
- `program-correct` (`spec.k:31-38`): from the fresh generated-semantics
  configuration, execute `solutionProgram`, load exactly `solutionFunctions`,
  consume the computation, and change `noResult` to
  `result(VBool(hasZeroTriple(IS)))` for every finite mathematical-integer
  list.

The returned Boolean is not a free variable, existential, tautology, or
one-way implication. It is fixed by structurally recursive, total functions.

### Source-tree and binding pin

`pairBody` and `tripleBody` quote both translated bodies;
`solutionFunctions` gives the exact named bindings and arities; and
`solutionProgram` gives the exact two-function module. A reviewer transcription
of the right-hand side of `solutionProgram` was parsed to KORE and compared to
the submitted `solution.mpy`; the KORE files are byte-identical with SHA-256
`67cc053e40eff5a285ec0a98a052ab4c3751e57fe2ab25884a1ec317533aa4c6`.
Commands and status are in
[`stage4_pinning.log`](evidence/stage4_pinning.log), with the transcription in
[`solutionProgram-expanded.mpy`](evidence/solutionProgram-expanded.mpy).

A material body mutation changing the helper's successful return from true to
false produced non-identical KORE (`cmp` exit 1 as expected) and changed the K
result for `[0,0,0]` to false. This demonstrates that the external source-tree
pin is body-sensitive; see
[`solution-mutated.mpy`](evidence/solution-mutated.mpy) and
[`stage5_static_witnesses.log`](evidence/stage5_static_witnesses.log).

### Satisfiable witnesses

All claim patterns are realizable. With `RESTK=.K` and the exact function map:

- `FIRST=1, IS=[1,-2]` satisfies the helper claim and yields true;
- `FIRST=1, IS=[2,3]` satisfies it and yields false;
- `IS=[1,1,-2]` satisfies both entry claims and yields true;
- `IS=[1,2,3,7]` satisfies both and yields false.

[`ground_witnesses.py`](evidence/ground_witnesses.py) compares
`hasPairWith`/`hasZeroTriple` values, an independent combinations predicate,
the candidate helper, the candidate entry, and trusted canonical entry; all
four witnesses agree. The exact output is in
[`stage4_pinning.log`](evidence/stage4_pinning.log). The same entry inputs are
covered by fresh K executions in the stage-3 log.

### Continuation and state containment

The recursive claims retain an arbitrary `RESTK` rather than manufacturing an
abrupt return, and the semantics leaves the outer K continuation in place when
a function body returns. Ground checks placed the observable `finish`
continuation after both helper and entry invocations; each updated the result
cell to true and the combined proof returned `#Top`. See
[`context-check.k`](evidence/context-check.k) and the stage-5 log.

## 5. Rule-by-rule static soundness review

There are no generated helper K source files beyond `semantic.k`,
`verification.k`, and `spec.k`.

### Local syntax, configuration, and attributes

`semantic.k:8-30` declares:

- `Program = Module(Stmts)`;
- statement lists and `FuncDef`, `If`, `Return`;
- parameter, identifier, expression, and comparison-operation lists;
- `Bool`, `Int`, `Name`, `UnaryOp`, `BinOp`, `Subscript`, `Slice`,
  `Compare`, and `Call`;
- `CmpOp`, expression bounds, and `NoBound`.

`semantic.k:41-70` declares:

- integer sequences;
- `VInt`, `VBool`, and `VList`;
- `noResult`/`result`, function closures, embedded values;
- all internal K items: `load`, `start`, `eval`, `unaryK`, `binLeftK`,
  `binRightK`, `subscriptLeftK`, `subscriptRightK`, `compareLeftK`,
  `compareRightK`, `call1K`, `call2LeftK`, `call2RightK`, `invoke1`,
  `invoke2`, `exec`, `ifK`, and `finish`.

The configuration (`semantic.k:72-79`) has `<k>`, `<funs>`, `<env>`,
`<input>`, and `<result>`. `<funs>`, `<input>`, and `<result>` are used as
expected. `<env>` is unused but is consistently framed; it cannot affect
control or the result.

`memberInt` (`semantic.k:127`) is `[function,total]`.
`verification.k:8-11` declares the zero-argument `[function]` constants
`pairBody`, `tripleBody`, `solutionProgram`, and `solutionFunctions`.
`verification.k:71-72` declares `[function,total]` functions
`hasPairWith` and `hasZeroTriple`.

There are no local `[functional]`, `[simplification]`, `[concrete]`,
`[owise]`, or priority declarations; no priority rules; and no opaque, fresh,
or otherwise unconstrained result symbols. The only imported computational
primitives are standard K Boolean, integer, string, map, and list-domain
operations.

Every source construct used by `solution.mpy` is covered:

| Submitted construct | Declaration/rules |
|---|---|
| module and two function definitions | `semantic.k:8,11,81-86` |
| parameters and local names | `15-16,98,142-147` |
| `if` and `return` | `11-13,149-158` |
| Boolean/int/name values | `20-22,95-98` |
| `not` on lists | `23,100-102` |
| integer subtraction | `24,105-109` |
| list index `0` | `25,112-116` |
| list slice `[1:]` | `25-26,112-118` |
| membership comparison | `27,29,120-130` |
| one- and two-argument named calls | `28,132-147` |

### All 39 ordinary rules in `semantic.k`

| ID/line | Rule role | Decision |
|---|---|---|
| S1/81 | `Module` starts loading | Sound for the submitted module. |
| S2/83-84 | load a function and update `<funs>` | Sound; later same-name definitions would override, as Python does. |
| S3/86 | empty load starts entry | Sound for this execution harness. |
| S4/88-90 | call named entry with `<input>` | Sound for the single-program harness; formal input is restricted to `VList(Ints)`. |
| S5/92-93 | `finish` stores returned `PyVal` | Sound and result-constraining. |
| S6/95 | embedded `Value` evaluates to its value | Sound. |
| S7/96 | Boolean literal | Sound. |
| S8/97 | integer literal | Sound with mathematical/unbounded K integers. |
| S9/98 | local name lookup | Sound when bound; exact calls bind every used name. |
| S10/100 | evaluate operand before unary operation | Sound evaluation order. |
| S11/101 | `not` empty list | Sound. |
| S12/102 | `not` nonempty list | Sound. |
| S13/103 | Boolean `not` | Sound, though not needed by the submitted AST. |
| S14/105-106 | evaluate binary left operand first | Sound. |
| S15/107-108 | then evaluate binary right operand | Sound. |
| S16/109 | integer subtraction | Sound and used. |
| S17/110 | integer addition | Sound but unused. |
| S18/112-113 | evaluate subscript base first | Sound. |
| S19/114-115 | then evaluate subscript expression | Sound order. |
| S20/116 | list index `0` returns head | Sound on its nonempty guard and used only after a nonempty check. |
| S21/117 | encode `Slice(1,None,None)` as `VInt(1)` | Not a faithful Python value semantics; tolerable only as a private sentinel. It collides with real integer index 1. |
| S22/118 | `VInt(1)` over a list returns the tail | **Unsound over its declared match domain.** Direct `l[1]` falsely returns a list tail; concrete witness below. |
| S23/120-121 | compare: evaluate left operand first | Sound. |
| S24/122-123 | then evaluate right operand | Sound. |
| S25/124-125 | integer membership in integer list | Sound and preserves operand direction. |
| S26/128 | membership in empty list is false | Sound; disjoint base case. |
| S27/129-130 | membership head test or recursive tail | Sound, covering and structurally decreasing. |
| S28/132-133 | evaluate unary-call argument | Sound. |
| S29/134 | convert value to one-argument invocation | Sound. |
| S30/136-137 | evaluate first two-call argument | Sound. |
| S31/138-139 | then evaluate second argument | Sound left-to-right order. |
| S32/140 | convert both values to two-argument invocation | Sound. |
| S33/142-143 | select exact arity-1 binding and bind local | Sound; map pattern pins the selected function. |
| S34/145-147 | select exact arity-2 binding and bind locals | Sound; argument order and two distinct parameter names are preserved. |
| S35/149 | return evaluates expression and drops remaining body | Sound; it retains the outer K continuation. |
| S36/151-152 | evaluate `if` guard | Sound. |
| S37/153-155 | true guard executes the exact single-return branch | Sound for the submitted `if` shape. |
| S38/156-158 | false guard resumes remaining statements | Sound for the submitted empty-else shape; guards are disjoint/exhaustive over `Bool`. |
| S39/159 | empty body returns `VBool(false)` | **Unsound over its declared match domain.** Python fallthrough returns `None`; concrete witness below. |

### All eight rules in `verification.k`

| ID/line | Rule role | Decision |
|---|---|---|
| V1/13-34 | define `pairBody` | Exact source quotation; KORE/source pin confirmed. |
| V2/36-52 | define `tripleBody` | Exact source quotation; KORE/source pin confirmed. |
| V3/54-60 | define `solutionProgram` | Exact two-definition module; KORE equality and mutation sensitivity confirmed. |
| V4/62-66 | define `solutionFunctions` | Exact, distinct string bindings and arities; no overlap. |
| V5/74 | `hasPairWith` empty suffix | Mathematically true base case; disjoint. |
| V6/75-76 | choose second position and search later third | Mathematically true; recursive tail strictly decreases and preserves distinct positions. |
| V7/78 | `hasZeroTriple` empty list | Mathematically true base case; disjoint. |
| V8/79-80 | choose first position or recurse on later first | Mathematically true; recursive tail strictly decreases. |

The equations for each total function cover empty/nonempty `Ints`, have
disjoint constructor patterns, and descend structurally. The four zero-argument
source constants each have one unconditional equation. No overlapping
right-hand sides, totalization gap, or non-descent was found.

### Three reachability claims

`pair-correct`, `triples-correct`, and `program-correct` are not opaque
operational rules in `verification.k`; they are the claims being proved.
`pair-correct` is a universal execution connection theorem for the exact helper
and arbitrary continuation. `triples-correct` is the analogous connection
theorem for the exact entry body. `program-correct` executes the quoted module
from fresh cells. Their state footprints and value influence are described in
stage 4. The ground continuation checks confirm that neither recursive summary
discards the observable `finish` continuation.

### Required false-conclusion witnesses

The S21/S22 collision is demonstrated by the admitted program:

```text
def triples_sum_to_zero(l):
    return l[1]
```

On the intended list-of-integers domain with `[10,20,30]`, CPython concludes
`20`, but K concludes
`result(VList(20 ; 30 ; .Ints))`. Thus S22 can enable a concrete false
reachability conclusion.

S39 is demonstrated by an admitted empty entry body. CPython concludes `None`,
but K concludes `result(VBool(false))` on `[10,20,30]`. Thus S39 also enables a
concrete false reachability conclusion.

The artifacts are
[`direct-index-one.mpy`](evidence/direct-index-one.mpy),
[`fallthrough.mpy`](evidence/fallthrough.mpy), and
[`semantic_scope_witness.py`](evidence/semantic_scope_witness.py); exact K and
Python outputs are in the stage-5 log.

These terms are not reachable from the submitted `solutionProgram`: it uses
only direct index `0`, every `Slice(1,None,None)` has slice provenance, and both
functions have trailing returns on every path. Therefore the witnesses do not
show that the target Boolean theorem itself is false. They do show that the
candidate's proof theory contains globally false ordinary semantic rules.
Under the mandated proof-extension soundness contract, off-path reachability is
not a justification for retaining a false rule. S21/S22 should use a distinct
slice-continuation symbol, and S39 should be omitted for this minimal subset or
model Python `None`.

## 6. Fresh non-vacuity test

The reviewer authored
[`spec-vacuity.k`](evidence/spec-vacuity.k), preserving the two real recursive
connection claims but mutating the top program result to `VBool(true)` for
every input. The precondition is satisfiable, and `IS=.Ints` is a direct false
witness: both trusted and candidate Python return false for `[]`.

The mutation dry run:

```text
kprove evidence/spec-vacuity.k \
  --definition /tmp/audit-work/build/verification-haskell-r2 \
  --spec-module SPEC-VACUITY --dry-run --output none
```

exited 0, so the mutation parsed, imported, and built successfully. The actual
proof exited 1 with `WarnStuckClaimState`. Its residual explicitly reports the
failed implication involving
`true #Equals hasZeroTriple(IS)` after reaching a final configuration whose
result is `VBool(hasZeroTriple(IS))`. This is the expected unmet result
obligation, not a parser error, missing import, timeout, or unrelated crash.

The witness, exact commands, statuses, and bounded residual are in
[`vacuity_witness.py`](evidence/vacuity_witness.py) and
[`stage6_nonvacuity.log`](evidence/stage6_nonvacuity.log). The candidate proof
is therefore result-sensitive and non-vacuous.

## 7. Proven versus assumed accounting

### What successful `kprove` establishes

Conditional on the candidate definition, K's reachability logic, and normal
execution in that model:

1. the exact `_has_pair_sum` body returns the structurally defined
   `hasPairWith` Boolean for every mathematical integer and finite integer
   suffix;
2. the exact entry body returns `hasZeroTriple` for every finite integer list;
3. the exact quoted module, from fresh function/result cells, consumes the
   computation and records `VBool(hasZeroTriple(IS))`.

By transparent structural inspection,
`memberInt` is list membership, `hasPairWith` chooses a later second position
and searches only later third positions, and `hasZeroTriple` chooses each first
position. This is exactly existence of indices `i < j < k` whose values sum to
zero.

The proof is partial correctness. It does not establish termination, resource
bounds, or absence of CPython exceptions.

### Trust ledger

| Boundary | Influence and dependents | Accounting |
|---|---|---|
| K parser/compiler, Haskell backend, `kore-exec`, and reachability logic | All three `#Top` results | Necessary low-level trusted computing base; fresh rebuild avoids candidate binaries. |
| Imported K `Int`, `Bool`, `String`, `Map`, and collection hooks | Arithmetic, equality, Boolean disjunction/negation, bindings | Acceptable standard primitives; mathematical integers match Python arbitrary-precision integer arithmetic on the formal domain. |
| Trusted mounted translator | Bridge from `solution.py` to submitted `solution.mpy` | Byte identity was checked. Translator correctness as a model of all CPython AST behavior is not formally proved here. |
| Quoted `solutionProgram`/bodies/functions | Pins claims to the translated tree | KORE identity and a body-sensitive mutation support this bridge; it is not an opaque oracle. |
| `memberInt`, `hasPairWith`, `hasZeroTriple` | Entire postcondition | Fully equational, total, disjoint, and decreasing; no opaque interpretation or empirical oracle. |
| Generated operational semantics | All program-execution claims | Audited rule by rule. Most target-path rules are faithful, but S22 and S39 have concrete false off-path conclusions; this is the decisive illegitimate boundary. |
| Normal-termination/ideal recursion model | Relation to actual CPython execution | K has unbounded mathematical recursion and no `RecursionError`; the 1,153-element witness shows the limitation. |
| Differential and concrete tests | Finite source/canonical/K bridge evidence | 138,275 bounded Python comparisons plus 16 fresh K runs support only tested inputs; they do not replace the universal K proof or repair false semantics rules. |
| Informal summary-to-English argument | Connects `hasZeroTriple` to the prompt's existential wording | Transparent structural induction, but not a separately stated K existential theorem. |

There are no opaque symbols, unconstrained fresh values, trusted
program-defined helpers, answer-encoding shortcuts, priority overrides, or
simplification axioms. The source helper is executed and has its own universal
connection claim.

### Gate accounting and final rationale

- Dynamic reconstruction: **PASS**.
- Real-program source/binding/result pin: **PASS**.
- Satisfiable preconditions and non-vacuity: **PASS**.
- Gate A, global generated-semantics soundness: **FAIL**, due to S22 and S39
  with concrete false-conclusion witnesses.
- Gate B, intent/model adequacy: **LIMITED**, because the theorem is partial
  correctness over ideal unbounded recursion while actual CPython can raise
  `RecursionError`; the existential summary itself matches the prompt.
- Gate C, evidence auditability: **PASS**; reviewer scripts and bounded command
  logs are preserved under `evidence/`.

Because the earliest failure is Gate A, successful `#Top`, exact source
pinning, and a passing non-vacuity mutation do not make the candidate a
legitimate proof under the required decision boundary.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
