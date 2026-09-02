# Independent adversarial audit: 109-move-one-ball

The candidate reconstructs cleanly, executes the submitted function body, and
has a discriminating postcondition. It nevertheless is not a legitimate proof
of the real program because its proof-only symbolic-list encoding is not
connected to ordinary semantic lists and includes a globally false operational
rule: every nonempty encoded list has `len == 1`. A two-element false-conclusion
witness closes under the rebuilt theory.

## 1. Input and provenance integrity

The launcher declares:

- problem `109-move-one-ball`;
- condition `semantics`;
- semantics mode `SUPPLIED_SEMANTICS`;
- record layout `legacy-selected-stage1`.

There is no semantics-mode contradiction: `/reference/reference-semantics` is
present. The required legacy-selected-stage1 records are all real readable
files/directories. Historical `runtime-metrics.json` is absent, as permitted
for this layout; `usage.json` is present and was inspected.

I read `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
`/task.json`, `/generation-result.json`, all required generation records,
`usage.json`, both present legacy records, `codex-output.log`, and all 349 JSON
records in the structured trace. Those generation records were treated only
as claims. The trace is valid JSONL and its recorded raw file hash matches.

Independent checks establish:

- the campaign-lock JSON object is exactly the `audit_campaign` block and its
  SHA-256 is the recorded
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`;
- all direct trusted/manifest/generation file hashes checked by
  [stage1_integrity.py](evidence/stage1_integrity.py) match `/audit-input.json`;
- every file recorded in `generation-result.json.outputs.evidence` has its
  recorded hash;
- the candidate prompt and translator are byte-identical to their trusted
  mounts;
- recursive type/name/content inventories of candidate and trusted
  `reference-semantics/` are identical: 25 non-root entries, no missing or
  additional entry, no changed file, and no symlink/unsupported node;
- the independently implemented pipeline tree digest is
  `4e06397a...d3789f` for each semantics tree, matching the recorded semantics
  manifest digest;
- the candidate workspace digest is `72f6e988...a5071c9c`, matching both
  `generation-result.json` and `invocation.json`;
- the structured-trace digest is `6b6d0a04...08a6`, matching `usage.json`.

The launcher’s additional legacy/current aggregate hash fields and integrity
booleans were also read; their equality relationships are consistent with the
direct byte/type inventory above. There is no infrastructure breach.

Evidence: [stage1-integrity.log](evidence/stage1-integrity.log),
[stage1_integrity.py](evidence/stage1_integrity.py).

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For a finite list of unique integers, return `True` exactly when some number of
right cyclic shifts makes the list nondecreasing. Return `True` for the empty
list.

The submitted implementation counts strict descents between adjacent elements,
then counts the last-to-first circular descent. It returns whether the circular
sequence has fewer than two descents. On unique elements, this is equivalent to
being a rotation of ascending order. It does not mutate the input.

Trusted regeneration:

```text
python3 /reference/py2mpy.py /candidate/solution.py \
  > /tmp/audit-work/reconstruction/solution.regenerated.mpy
cmp .../solution.regenerated.mpy /candidate/solution.mpy
```

exited 0. Both files have SHA-256
`f7554210119c8a42792c645561475c851dcf773ef0d3b0d68a752a31dae6d6af`.

The independent differential script imports the trusted canonical entry point
and submitted entry point and uses a separately written cyclic-rotation oracle.
It checked:

- 18 documented/boundary cases, including empty/singleton, both examples,
  negative values, very large integers, one-descent and two-descent boundaries;
- all 46,234 permutations of lengths 0 through 8;
- 2,000 deterministic seed-109 random unique lists of lengths 0 through 64.

All 48,252 intended-domain cases had zero mismatches among oracle, canonical,
and generated implementation. An explicitly out-of-contract duplicate probe
found 140 canonical/oracle divergences among 3,280 cases; the prompt guarantees
unique elements, and the generated implementation agreed with the direct
operation on those examples. This does not narrow the audited source domain.

Evidence: [translator-regeneration.log](evidence/translator-regeneration.log),
[differential_test.py](evidence/differential_test.py),
[differential-test.log](evidence/differential-test.log). The initial exploratory
nonzero run, before out-of-contract cases were separated from the pass
criterion, remains in
[differential-test-exploratory.log](evidence/differential-test-exploratory.log).

## 3. Clean proof reconstruction

I copied only source artifacts to `/tmp/audit-work/reconstruction`, replacing
the semantics copy with the trusted mount, and did not copy or reuse any
compiled definition/cache. The observed toolchain is K `v7.1.293`.

Fresh commands and results:

| Purpose | Command summary | Result |
|---|---|---|
| Concrete definition | `kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-kompiled` | exit 0 |
| Concrete harness | trusted regeneration, then `krun concrete-tests.regenerated.mpy --definition runtime-kompiled --output pretty` | exit 0; final `.K`, `NoExc`, exit-code 0 |
| Proof definition | `kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-kompiled` | exit 0 |
| Loop induction | `kprove ... --claims SPEC.move-one-ball-loop-induction` | `#Top`, exit 0 |
| Loop entry with dependency | `kprove ... --claims SPEC.move-one-ball-loop-induction,SPEC.move-one-ball-loop-entry` | `#Top`, exit 0 |
| Functional claim with dependencies | `kprove ... --claims SPEC.move-one-ball-loop-induction,SPEC.move-one-ball-loop-entry,SPEC.move-one-ball-correct` | `#Top`, exit 0 |
| Unfiltered target | `kprove spec.k --definition verification-kompiled --spec-module SPEC --output pretty` | `#Top`, exit 0 |

The entry claim is intentionally dependent on the induction circularity. A
diagnostic that filtered the induction claim away was interrupted with status
130 and is not used as proof evidence; the dependency-complete command above is
the independent positive target run.

Evidence: [tool-versions.log](evidence/tool-versions.log),
[concrete-kompile.log](evidence/concrete-kompile.log),
[concrete-regeneration.log](evidence/concrete-regeneration.log),
[concrete-krun.log](evidence/concrete-krun.log),
[proof-kompile.log](evidence/proof-kompile.log),
[kprove-loop-induction.log](evidence/kprove-loop-induction.log),
[kprove-loop-entry.log](evidence/kprove-loop-entry.log),
[kprove-correct.log](evidence/kprove-correct.log), and
[kprove-all.log](evidence/kprove-all.log).

Clean reconstruction therefore passes. The prior generated `#Top` was not
trusted.

## 4. Adequacy and real-program pinning

### Claims in plain language

`move-one-ball-loop-induction` starts at a loop head with a nonempty remaining
typed integer sequence and an already-bound `current`. For arbitrary integer
`drops`/`previous`, it reaches the same continuation after consuming the
sequence, with `drops`, `previous`, and `current` set to `scanDrops`/`scanLast`.

`move-one-ball-loop-entry` states the same store transformation when `current`
is initially absent. Its first concrete target binding makes the induction
claim applicable.

`move-one-ball-correct` starts an actual call of `move_one_ball` from an exact
initial module configuration and says its resulting value is
`moveOneBallSpec(intVals(IS))` for arbitrary finite `IntSeq IS`. Empty maps to
`true`; nonempty maps to “strict circular descent count is below 2.” The result
is constrained, not a right-hand free variable or implication-only
postcondition.

The exact maps/cells and sort constraints constitute the preconditions; there
are no hidden `requires` clauses. Concrete satisfying witnesses include:

- induction: `C=4`, `IS=iCons(1,.IntSeq)`, `D=0`, `P=5`, `F=5`,
  old `current=99`, `KONT=.K`; the post-store has drops 2 and
  previous/current 1;
- entry: the same state with `current` absent;
- functional: the exact initial cells in `spec.k` and inputs `[]`,
  `[3,4,5,1,2]`, `[3,5,4,1,2]`, or `[2,3,1]`.

For those functional witnesses, the K summary and both Python implementations
agree (`True`, `True`, `False`, `True` respectively). See
[claim-witnesses.log](evidence/claim-witnesses.log).

### Mechanical body identity

I parsed the submitted `solution.mpy` and an independently constructed module
whose function body is `MOVE-ONE-BALL-BODY` with the fresh verification
definition, executed both modules, and compared their final KORE
configurations. The input constructor terms differ as expected, but the final
configurations are byte-identical (both SHA-256
`d9ec243a...46e08`). This demonstrates that the claim’s closure binding and
body are the translated submitted function, rather than a substituted
algorithm. See [claim-program.mpy](evidence/claim-program.mpy) and
[program-pinning.log](evidence/program-pinning.log).

The source-to-proof transcription is manual, which is a maintenance
observation rather than a defect in this immutable candidate. A body-sensitivity
mutation changed the actual executed body from `drops < 2` to `drops < 3`,
rebuilt successfully, and made the functional claim fail with a
`WarnStuckClaimState` residual comparing the two thresholds. Input
`[3,5,4,1,2]` witnesses the semantic difference. Evidence:
[body-sensitivity.patch](evidence/body-sensitivity.patch),
[body-mutation-kompile.log](evidence/body-mutation-kompile.log), and
[body-mutation-kprove.log](evidence/body-mutation-kprove.log).

Program-body pinning and result adequacy pass. They do not validate the
proof-only input representation, addressed next.

## 5. Rule-by-rule static soundness review

The mechanical inventory contains all 236 syntax declarations, 717 rules, five
contexts, one configuration, and three claims across every supplied K source,
`verification.k`, and `spec.k`. It records all 154 `[function]`, 112 `[total]`,
25 opaque-symbol, 35 `[concrete]`, 26 `[owise]`, 50 priority, five macro, and
zero candidate simplification/`functional` declarations, with complete
multiline guards and attributes.

Evidence: [rule-inventory.md](evidence/rule-inventory.md), generated by
[build_rule_inventory.py](evidence/build_rule_inventory.py). The exhaustive
file-by-file disposition, construct map, candidate-extension classification,
overlap/coverage/descent assessment, state footprints, and value/control
influence are in
[static-soundness-assessment.md](evidence/static-soundness-assessment.md).

The used fixed-semantics path is faithful: call lookup and argument order,
plain closure-frame allocation, parameter binding, statement sequencing,
integer comparison/addition, assignment, iterator control, target binding,
return, and frame restoration all match the submitted program. Supplied opaque
float/sort/MD5 primitives are unreachable and do not affect any target value,
branch, cell, or postcondition. `MPY-CONCRETE` is not imported into the proof.

The proof-specific inventory contains:

- three exact nullary body/closure definitions;
- the fresh `intVals(IntSeq)` constructor;
- five priority-40 operational bridges for iteration, `len`, and index zero;
- `addDrop`, four `scanDrops`, four `scanLast`, `circularDrops`, and four
  `moveOneBallSpec` equations.

The mathematical helper equations are constructor-disjoint and structurally
descending on integer sequences. `scanDrops`, `scanLast`, and
`moveOneBallSpec` are declared total over all `ValSeq` but omit non-integer
`vCons` heads; that is an over-broad totality declaration, although no wrong
value witness arises on the formal `IntSeq` domain.

### Material unsoundness

`intVals` is described as a typed encoding of an ordinary finite Python integer
list, but there is no bridge-free universal theorem connecting it to the
supplied `.ValSeq`/`vCons` representation. The loop claims cannot provide that
connection because they themselves rely on the proposed bridges.

More decisively, `/candidate/verification.k:53-56` rewrites

```k
#applyK(toCall(builtinV("len")),
        (list(intVals(iCons(_I, _IS))), .Vals))
```

to `1` for every nonempty sequence, under an arbitrary continuation. This is
not Python length and is not an exact supplied-semantics step. The candidate’s
comment says it is only a zero/nonzero abstraction, but the rule’s match
context does not enforce comparison with zero.

Concrete false-conclusion witness:

- the fixed representation of `[7,8]`,
  `list(vCons(7,vCons(8,.ValSeq)))`, reduces to length `2`;
- the candidate’s claimed encoding of `[7,8]`,
  `list(intVals(iCons(7,iCons(8,.IntSeq))))`, reduces to length `1`.

Both reachability conclusions prove to aggregate `#Top` in
[bridge-witness.k](evidence/bridge-witness.k) using the freshly rebuilt
definition; see [bridge-witness.log](evidence/bridge-witness.log). A
continuation that returns/stores the length or tests equality with 2 observes
the disagreement. This is the required concrete false conclusion enabled by
the rule.

If `intVals` is taken to denote the corresponding real list, the length bridge
is globally false. If it is not, the entry claim quantifies over alien
proof-defined values rather than real Python lists. The current target’s
`len(arr) == 0` context happens to be insensitive to the difference between 1
and larger positive lengths, but that context is not part of the bridge’s
match, and unreachable-bad-context reasoning cannot validate a globally false
exact rewrite.

Gate A real-program soundness therefore fails. This is material proof-rule
unsoundness, not merely thin testing or an informal but truthful intent bridge.

## 6. Fresh non-vacuity test

There was no candidate `spec-vacuity.k` to trust. I copied `spec.k` in scratch,
renamed its module, retained both loop dependencies, and changed only the
functional postcondition:

```k
Call(Name("move_one_ball"), list(intVals(IS:IntSeq)))
=> true
```

This is false for the satisfying intended-domain input `[3,5,4,1,2]`, for which
the real and submitted Python functions return `False`.

`kprove ... --dry-run` exited 0, establishing that the mutation parsed and
built. The real proof command exited 1 with `WarnStuckClaimState`; its residual
is the expected unmet equality between `true` and the computed
`scanDrops(...) <Int 2`, not a parser error, missing import, timeout, or
unrelated crash.

Evidence: [spec-vacuity-audit.k](evidence/spec-vacuity-audit.k),
[vacuity-dry-run.log](evidence/vacuity-dry-run.log), and
[vacuity-kprove.log](evidence/vacuity-kprove.log).

Non-vacuity passes.

## 7. Proven versus assumed accounting

### What the successful K run establishes

Under the supplied `MPY` rules *plus all candidate rules*, K proves two
loop-store summaries and proves that the pinned submitted closure, when called
on the proof-defined term `list(intVals(IS))`, returns
`moveOneBallSpec(intVals(IS))`. This is a result-constraining partial-correctness
statement. The run does not by itself prove termination, nor does it prove that
the candidate extension is a sound model of real lists.

### Trust ledger

| Boundary | Influence | Assessment |
|---|---|---|
| K compiler, Haskell/LLVM backends, builtin Int/Bool/Map theories | Proof checking and primitive mathematics | Ordinary unavoidable checker boundary. |
| Trusted translator | Program constructor identity | Byte regeneration plus constructor/final-configuration comparison support it. |
| Supplied semantics | Used call/control/state behavior | Required fixed baseline; exact integrity verified and material rules statically reviewed. |
| Supplied opaque float, sort, MD5 symbols | None on this theorem | Inert; no target dependency. |
| `intVals` representation and iteration/index bridges | Formal input domain, loop control, values | Program-derived and lacks the required bridge-free connection theorem. |
| Nonempty `intVals` length bridge | Empty/nonempty branch and arbitrary other continuations | Illegitimate: machine-checked false-conclusion witness. |
| `[total]` on scans/spec over all `ValSeq` | Definedness reasoning | Over-broad; integer target paths have equations, non-integer paths do not. |
| Circular-descent characterization of cyclic sortability | Human-facing adequacy | Mathematically valid for the unique-integer contract and strongly differentially supported, but not separately proved in K. |
| Differential tests | Implementation/intent bridge on finite samples | Empirical only; never substituted for the K proof. |

Gate results:

- reconstruction/verification: pass;
- Gate A real-program soundness: fail;
- intent-domain coverage considered in isolation: full unique-integer domain,
  no finite-size restriction;
- evidence/non-vacuity considered in isolation: pass;
- final legitimacy: fail because the result depends on a materially unsound,
  unconnected operational abstraction.

The successful `#Top` is therefore a theorem only of the candidate-extended
theory, not a legitimate partial-correctness proof of the real generated
program over the source-contract domain.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
