# Independent adversarial review: 142-sum-squares

## Audit outcome

The candidate contains a legitimate, result-constraining partial-correctness
proof of the submitted `sum_squares` function for arbitrary finite lists of
mathematical integers under the supplied MPY semantics. The proof was rebuilt
from trusted source in clean scratch; its loop, body, and main claims each
closed independently with exit status 0 and `#Top`; the formal domain is not
bounded; and a fresh false-result claim was rejected after executing the real
function.

There is one non-fatal limitation. The universal claim represents an arbitrary
list with the proof-local constructor `list(intVals(IS))`, and two exhaustive
iterator rules give that constructor the same head/tail behavior as fixed
`list(vCons(...))` lists. This is a transparent structural representation, not
an oracle, and no false conclusion is enabled. However, the candidate does not
include a bridge-free, machine-checked universal equivalence theorem between
the two representations. Ground K checks, concrete execution, and differential
tests support the bridge but cannot make it universal. Under the benchmark's
decision boundary, this is an informal evidence/intent bridge warranting a
concern while the proof remains legitimate.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- problem `142-sum-squares`;
- condition `semantics`;
- semantics mode `SUPPLIED_SEMANTICS`;
- record layout `legacy-selected-stage1`;
- complete input provenance.

The mode and mounts are consistent: `/reference/reference-semantics` is
present. This is not an infrastructure-error case.

I compared `/audit-input.json`'s `audit_campaign` object structurally with
`/audit-campaign-lock.json`; they are equal. The independently computed lock
hash is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
which equals the launcher-declared hash. Every launcher `container_paths`
entry exists, is readable, has the expected file/directory type, and is not a
symlink.

For the declared legacy layout I read and independently hashed:

- `/run.json`;
- `/task.json`;
- `/generation-result.json`;
- `/generation-evidence/invocation.json`;
- `/generation-evidence/metrics.json`;
- `/generation-evidence/usage.json`;
- `/generation-evidence/codex-last.txt`;
- `/generation-evidence/codex-output.log`;
- `/generation-evidence/prompt.txt`;
- the complete structured trace under
  `/generation-evidence/codex-trace/`.

The trace consists of one regular JSONL file with 452 valid records and no
invalid JSON or links. The 28,136-line generation log, trace, final text, and
all JSON record hashes match their launcher/invocation records. Generation
claims include prior `#Top` and `KPROVE_PASSED` assertions; I treated all of
them solely as untrusted history and did not rely on them. For this
`legacy-selected-stage1` record, absent historical
`runtime-metrics.json` is expressly not required.

The candidate's `prompt.py` and `py2mpy.py` are byte-identical to
`/reference/prompt.py` and `/reference/py2mpy.py`. Recursive comparison of
`/candidate/reference-semantics` with the trusted tree found 25 matching
entries (24 K files plus the helper directory), with identical types, modes,
and bytes and no missing, additional, changed, mistyped, or linked entries.

Evidence:

- `/audit-output/evidence/integrity_check.py`
- `/audit-output/evidence/stage1-integrity.log` (`failure_count=0`, exit 0)
- `/audit-output/evidence/generation_record_summary.py`
- `/audit-output/evidence/stage1-generation-record-summary.log`
- `/audit-output/evidence/mounted-file-sha256.txt`

Stage result: integrity passes; no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For a finite list of integers, visit entries by zero-based index. Square an
entry when its index is a multiple of 3. Otherwise cube it when its index is a
multiple of 4. Leave all other entries unchanged. Return the sum. Thus an
index divisible by both 3 and 4 uses the square branch. Required examples are
`[1,2,3] -> 6`, `[] -> 0`, and
`[-1,-5,2,-1,-5] -> -126`.

The trusted canonical implementation constructs the transformed list with
exactly those branches and returns its sum. The candidate uses an accumulator
and explicit index but implements the same branch order and arithmetic. It
does not mutate its argument.

From clean scratch, this exact command used the trusted translator:

```text
python3 py2mpy.py solution.py > regenerated-solution.mpy
```

It exited 0. `cmp -s regenerated-solution.mpy solution.mpy` exited 0, and both
files have SHA-256
`13c68b0fc50ba93b60389fadabdcdfda4aa2b9130fec6f602fa9b859bd6c08cc`.

The independent differential script separately imported
`/reference/canonical.py` and the scratch copy of candidate `solution.py`, and
also evaluated a reviewer-written contract oracle. Its 57,092 inputs comprise:

- all three documented examples;
- lengths 0 through 14 around every early branch boundary;
- signed/zero branch-isolating values at each index 0 through 13;
- the complete Cartesian product of six values for lengths 0 through 6;
- 1,000 deterministic generated lists of lengths 0 through 50;
- arbitrary-size integer cases up to 100 decimal digits.

There were zero result or input-mutation mismatches. The encoded input corpus
hash is
`5ead82b747366155fdb0da21939b5db182badb1eee633e396c9da958f6e37817`.
These are finite fidelity checks, not a proof.

Evidence:

- `/audit-output/evidence/stage2_commands.sh`
- `/audit-output/evidence/differential_test.py`
- `/audit-output/evidence/stage2-fidelity-differential.log`

Stage result: source, translation, examples, branches, and representative
intended-domain behavior agree.

## 3. Clean proof reconstruction

I copied only candidate source proof artifacts, the trusted translator, and the
trusted supplied semantics to `/tmp/audit-work/reconstruction`. No
`*-kompiled` directory existed before reconstruction. Candidate-provided
definitions, caches, `prove.log`, and `spec.json` were neither copied nor
used. Installed `kompile` and `kprove` both report K v7.1.293.

A reviewer-authored concrete harness embeds an AST-identical copy of the
submitted function and exercises empty, normal, branch-boundary, overlap, and
large-integer inputs. The following fresh commands were run:

| Command | Result |
|---|---|
| `kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition audit-runtime-kompiled` | exit 0 |
| `krun audit-concrete-tests.mpy --definition audit-runtime-kompiled --output pretty` | exit 0; final `.K`, `NoExc`, `<exit-code> 0` |
| `kompile verification.k --backend haskell --main-module SUM-SQUARES-VERIFICATION --syntax-module MPY-SYNTAX --output-definition audit-verification-kompiled` | exit 0 |
| `kprove spec.k --definition audit-verification-kompiled --spec-module SUM-SQUARES-SPEC --claims SUM-SQUARES-SPEC.loop --output pretty` | exit 0; `#Top` |
| `kprove spec.k --definition audit-verification-kompiled --spec-module SUM-SQUARES-SPEC --claims SUM-SQUARES-SPEC.body,SUM-SQUARES-SPEC.loop --trusted SUM-SQUARES-SPEC.loop --output pretty` | exit 0; `#Top` |
| `kprove spec.k --definition audit-verification-kompiled --spec-module SUM-SQUARES-SPEC --claims SUM-SQUARES-SPEC.main,SUM-SQUARES-SPEC.body --trusted SUM-SQUARES-SPEC.body --output pretty` | exit 0; `#Top` |

The trusted labels in the second and third proof commands were used only after
the identical loop and body claims had respectively been proved in the
preceding commands. This is explicit theorem composition, not reliance on the
generation run.

The compiler emitted non-exhaustiveness warnings for unrelated supplied
functions and unused-variable warnings in string comparison rules. None is
reachable from this integer-list proof, and every build/proof exited as
reported.

Evidence:

- `/audit-output/evidence/k_concrete_tests.py`
- `/audit-output/evidence/concrete_ast_identity.py`
- `/audit-output/evidence/stage3-prebuild.log`
- `/audit-output/evidence/stage3-llvm-kompile.log`
- `/audit-output/evidence/stage3-krun.log`
- `/audit-output/evidence/stage3-haskell-kompile.log`
- `/audit-output/evidence/stage3-kprove-loop.log`
- `/audit-output/evidence/stage3-kprove-body.log`
- `/audit-output/evidence/stage3-kprove-main.log`

Stage result: every positive target claim closes in a clean reconstruction.

## 4. Adequacy and real-program pinning

### Plain-language claim statements

`loop` starts with a remaining symbolic integer sequence `IS`, arbitrary
continuation, and an exact local frame containing original `lst`, current
`value`, accumulator `total=ACC`, and `index=I`. It executes the actual loop
body until iteration ends. The post-frame preserves `lst`, sets `value` to the
last yielded element (or preserves the old value when empty), sets `index` to
`I + length(IS)`, and sets `total` to the recursive sum of the contract
contributions beginning at `I`.

`body` starts after the submitted function's two initialization assignments:
the exact local frame contains `lst`, `total=0`, and `index=0`, and the exact
call stack/frame cells are pinned. It runs the actual loop and return, restores
the caller frame, and produces `sumSquares(IS,0,0)`.

`main` starts at an actual `Call(Name("sum_squares"), ...)` in the exact module
scope where `"sum_squares"` is bound to a one-argument closure whose body is
`sumSquaresFunctionBody`. It returns exactly `sumSquares(IS,0,0)`, with all
other configuration cells pinned/restored. The result is not a free variable,
tautology, or one-way implication.

### Mechanical program identity

I used `kast --expand-macros --output json` on the trusted regenerated
`solution.mpy` and independently on both candidate macros. A reviewer script
located the sole translated `FuncDef`, checked the name `"sum_squares"` and
sole parameter `"lst"`, then compared KAST constructor trees:

- translated function body and expanded `sumSquaresFunctionBody` are equal;
  both stable term hashes are
  `75bccb54dc3ec98157f35164575831dda37e7e367219b402808e84fd72e0d6a5`;
- translated `For` body and expanded `sumSquaresLoopBody` are equal; both term
  hashes are
  `8cc17e9db41c9c72f03bc99f114e14d5cbf6db99f5f694914eaf7bbe5ebbd2cb`.

The claim therefore executes the submitted binding and body, not a rewritten
algorithm or external oracle. Starting at the bound call rather than replaying
module loading is a mechanically justified, semantically inert normalization.

### Satisfiable preconditions and concrete substitutions

All entry preconditions have explicit ground witnesses:

- `main` and `body`: `IS=[1,2,3]` in `Ints` form, exact scopes/cells from the
  claims; claimed result 6; both Python implementations return 6.
- `loop`: a real state after prefix `[1,2,3,2]`, with
  `I=4`, `ACC=10`, `OLD=2`, and remaining `[2,-3,4]`; claimed final total 31,
  end index 7, and final value 4. Both Python implementations return 31 on the
  full list.

`Ints` is an unbounded inductive sequence sort and each element is an unbounded
K `Int`. Thus the theorem ranges over every finite list length and integer
magnitude in the source contract; it is not example-only, bounded, or
unrolled to a fixed size.

### Body sensitivity

In scratch I changed the square expression in the macro actually stored in
the claimed closure from `value*value` to `value*value+1`, rebuilt successfully,
and reran the untrusted-free loop proof. It exited 1 with
`WarnStuckClaimState`; the residual specifically required equality between
the unchanged summary and accumulators containing `X*X+1` versus `X*X`.
Changing an external source file alone was not used.

Evidence:

- `/audit-output/evidence/stage4_commands.sh`
- `/audit-output/evidence/program_term_compare.py`
- `/audit-output/evidence/solution-kast.json`
- `/audit-output/evidence/function-body-kast.json`
- `/audit-output/evidence/loop-body-kast.json`
- `/audit-output/evidence/claim_witnesses.py`
- `/audit-output/evidence/stage4-pinning-witnesses.log`
- `/audit-output/evidence/verification-body-mutated.k`
- `/audit-output/evidence/stage5-body-mutation-build.log`
- `/audit-output/evidence/stage5-body-mutation-proof.log`

Stage result: the claims are satisfiable, result-constraining, full-domain, and
mechanically pinned to the submitted body.

## 5. Rule-by-rule static soundness review

The exhaustive inventory covers all 24 trusted K source files plus
`verification.k` and `spec.k`:

| Record class | Count |
|---|---:|
| Syntax declarations | 235 |
| Rules | 708 |
| Evaluation contexts | 5 |
| Configuration | 1 |
| Reachability claims | 3 |
| Total | 952 |

It records full normalized text, source/module/line, attributes,
classification, target reachability, and an assessment for every record.
There are no `functional` or `simplification` attributes. Twenty-five syntax
records are opaque/symbol declarations (22 use `no-evaluators`); all are in
unused float, sort, or digest functionality, and none influences target
control, state, or result.

The target's constructors map to fixed syntax/rules for function calls and
frames, left-to-right argument/operator evaluation, exact local lookup and
update, `For/#loop/#bindTgt`, `If`, integer `%/==/+/*`, `Return`, and frame
restoration. The exact reachable mapping and all candidate-local decisions are
in `/audit-output/evidence/static-soundness-review.md`.

Candidate-local conclusions:

- `.Ints/intCons` is an ordinary finite free sequence.
- `contribution`'s three guards are exhaustive and pairwise disjoint; their
  square/cube/identity equations are true.
- `sumSquares`, `endIndex`, and `endValue` cover both `Ints` constructors and
  strictly descend.
- Both macros are mechanically identical to the translated program.
- The two priority-40 `intVals` iterator cases cover empty/nonempty sequences,
  are mutually disjoint, and are constructor-disjoint from fixed
  `list(.ValSeq)` and `list(vCons(...))` rules. They rewrite only the current
  iterator request, preserve every continuation and other cell, introduce no
  return/exception/frame effect, yield the actual head, and strictly descend.
  Their priorities cannot preempt a fixed list rule on an overlapping term.

No candidate rule rewrites a call directly to the answer, replaces a
program-derived computation with an unconstrained symbol, fabricates an
unmodeled used operation, or introduces a false equality. No unsound rule was
identified; therefore there is no unsoundness assertion requiring a
false-conclusion witness.

The evidence gap is narrower: no candidate K theorem universally connects the
new `intVals` representation to fixed concrete `vCons` lists. Structural
induction establishes the intended correspondence informally because the two
empty/cons iterator definitions agree and iteration is the only observation
the program makes. A fresh ground K spec additionally proved both the abstract
and fixed one-step rules with a preserved trailing continuation, and proved
the complete program returns 6 for `[1,2,3]` under each representation. This
finite check exited 0 with `#Top`; it is support, not a universal theorem.

Evidence:

- `/audit-output/evidence/rule_inventory.py`
- `/audit-output/evidence/rule-inventory.tsv`
- `/audit-output/evidence/stage5-inventory.log`
- `/audit-output/evidence/static-soundness-review.md`
- `/audit-output/evidence/bridge-ground-spec.k`
- `/audit-output/evidence/stage7-bridge-ground.log`

Stage result: no material semantic or proof-rule unsoundness; one documented
universal-connection evidence limitation.

## 6. Fresh non-vacuity test

I ignored any candidate mutation evidence and wrote a fresh ground mutation in
`spec-vacuity.k`. It uses the exact submitted closure and exact main
configuration on the satisfiable empty-list input, but changes the
result-constraining destination from the true 0 to false value 1.

The parsing/build command

```text
kprove spec-vacuity.k --definition audit-verification-kompiled --spec-module SUM-SQUARES-SPEC-VACUITY --claims SUM-SQUARES-SPEC-VACUITY.main-false-empty --dry-run
```

exited 0 and emitted the backend command, so the mutation built successfully.
The same proof without `--dry-run` exited 1 with
`WarnStuckClaimState`. Its final exact configuration has `<k> 0 ~> .K </k>`
and cannot unify with destination 1. This is the expected unmet result
obligation after real execution, not a parse failure, missing import, timeout,
or unrelated crash.

Evidence:

- `/audit-output/evidence/spec-vacuity.k`
- `/audit-output/evidence/stage6-vacuity-dry-run.log`
- `/audit-output/evidence/stage6-vacuity-proof.log`

Stage result: the proof is non-vacuous and discriminates false results.

## 7. Proven versus assumed accounting

### Machine-checked

Under the supplied MPY definition plus the candidate's transparent
`Ints/intVals` representation and recursive mathematical functions:

1. For arbitrary `IS:Ints`, the actual submitted loop transforms
   `total/index/value` according to every remaining element and preserves the
   exact stated frame.
2. From initialized locals, the actual submitted body returns
   `sumSquares(IS,0,0)` and restores the exact caller state.
3. The exact submitted `sum_squares` binding called on
   `list(intVals(IS))` returns `sumSquares(IS,0,0)`.
4. The three arithmetic branches in that summary exactly implement the prompt
   formula over arbitrary K integers and arbitrary finite sequence length.
5. The false empty-list destination 1 is not derivable.

This is a partial-correctness reachability result. The structurally decreasing
finite iterator also supplies termination on the formal domain, but no claim
is made about behavior outside the prompt's finite-list-of-integers contract.

### Trusted or informal boundaries

| Boundary | Influence and dependents | Judgment/evidence |
|---|---|---|
| K compiler, Haskell/LLVM backends, K reachability logic, and builtin `Int/Bool/Map/List` hooks | All builds, symbolic execution, and arithmetic | Standard unavoidable toolchain trust; version recorded; fresh positive and negative runs succeeded. |
| Launcher-supplied MPY semantics | Call/control/state/evaluation behavior of all claims | Required benchmark semantics; integrity was exact. The complete inventory was reviewed, with the target slice checked in detail. |
| Trusted `py2mpy.py` translation | Link from Python source to submitted constructor term | Candidate translator matches trusted bytes; trusted regeneration is byte-identical; macro constructor identity is mechanical. |
| MPY subset versus CPython on the stated operations | Human-facing interpretation of K integer/control behavior | Material target operations are simple unbounded integer arithmetic and finite list iteration. Concrete K checks and 57,092 Python differential inputs agree, but finite tests are not a semantics theorem. |
| `intVals(IS)` versus fixed `vCons` list representation | Universal input-domain bridge; therefore the main result | Equations are exhaustive, head/tail exact, and non-oracular; structural correspondence is informally clear. Ground fixed/abstract K checks and concrete tests agree. Missing universal K connection theorem is the sole concern. |
| Previously proved `loop` and `body` labels admitted by later commands | Closure of body and main, respectively | Acceptable explicit theorem composition: each identical claim was first independently proved with exit 0 and `#Top`. |

No reachable opaque symbol, empirical result oracle, external-state primitive,
or unproved task-answer axiom contributes to the returned value.

### Overall decision

The concern does not narrow the HumanEval domain, admit a wrong result, or
substitute a different function body. The formal theorem covers arbitrary
finite sizes and arbitrary integer magnitudes, and its input representation
has a truthful total structural meaning for every case the program observes.
The missing universal representation-connection artifact is therefore a
non-fatal auditability limitation, not grounds for rejecting the proof.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
