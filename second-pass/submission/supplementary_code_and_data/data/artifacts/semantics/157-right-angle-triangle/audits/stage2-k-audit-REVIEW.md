# Independent adversarial review: 157-right-angle-triangle

This review treats every candidate and generation artifact as untrusted. All
builds and mutations were performed under `/tmp/audit-work/reconstruction`
from copied source. No candidate-provided compiled definition or cache was
used. Reviewer scripts and bounded logs are under
[`evidence/`](evidence/).

## 1. Input and provenance integrity

The launcher record declares:

- record layout: `legacy-selected-stage1`;
- generation condition: `semantics`;
- semantics mode: `SUPPLIED_SEMANTICS`;
- candidate mount: `/candidate`;
- trusted prompt, canonical, translator, and supplied semantics under
  `/reference`.

The supplied-mode boundary is internally consistent:
`/reference/reference-semantics` is present and is a real directory.
`/candidate/reference-semantics` recursively has exactly the same one
subdirectory and 24 regular files. Every corresponding file is byte-identical,
and neither tree contains a symlink. Candidate `prompt.py` and `py2mpy.py` are
also byte-identical to their trusted versions.

The campaign lock JSON exactly equals the `audit_campaign` block in
`/audit-input.json`; its SHA-256 is the recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
Independent SHA-256 checks match the recorded run manifest, task manifest,
stage-1 result, invocation, generation metrics, usage, prompt, last message,
output log, canonical, prompt, translator, and every evidence file declared by
`generation-result.json`. The structured trace has one regular JSONL file; all
196 lines parse. The full type/size inventory found no required symlink or
mistyped entry.

For this historical layout, `runtime-metrics.json` is not required and was
not reconstructed. The required `usage.json` is present and was inspected.
`run.json`, `task.json`, `generation-result.json`, `invocation.json`,
`metrics.json`, `usage.json`, `legacy-run-input.json`,
`legacy-metrics.json`, `codex-last.txt`, `codex-output.log`, `prompt.txt`, and
the structured trace were read. Their prior `KPROVE_PASSED` and `#Top` reports
were not relied upon.

Evidence:

- [`stage1-integrity-check.log`](evidence/stage1-integrity-check.log)
- [`stage1-file-hashes.log`](evidence/stage1-file-hashes.log)
- [`stage1-mounted-inventory.log`](evidence/stage1-mounted-inventory.log)
- [`stage1-provenance-records.log`](evidence/stage1-provenance-records.log)
- [`stage1-generation-evidence-inspection.log`](evidence/stage1-generation-evidence-inspection.log)
- reviewer checker: [`provenance_check.py`](evidence/provenance_check.py)

Stage 1 result: PASS. No infrastructure breach was found.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The trusted prompt says to return whether three given side lengths form a
right-angled triangle. For valid positive side lengths, the trusted canonical
returns true exactly when one of the three Pythagorean equalities holds, with
the hypotenuse allowed in any argument position.

The prompt provides no type annotations and does not explicitly state behavior
for zero or negative arguments. The phrase “sides of a triangle” ordinarily
excludes non-positive lengths. The formal proof adopts integer side lengths.
That domain interpretation is recorded as a limitation below rather than
silently treated as a theorem about arbitrary Python numeric objects.

### Submitted implementation and translation

`solution.py` first returns false if any argument is non-positive, then checks
the three Pythagorean equalities, then returns false. Regeneration with the
trusted `/reference/py2mpy.py` exits 0. The regenerated and submitted
`solution.mpy` are byte-identical, both with SHA-256
`703f3585497535059c241e012e8e977109876df7bf20c9821a17b359c1061ad7`.

Evidence: [`stage2-regeneration.log`](evidence/stage2-regeneration.log).

### Independent differential test

The reviewer-authored test imports `/reference/canonical.py` and
`/candidate/solution.py` independently. It covers both documented examples,
all three possible hypotenuse positions, the false positive-domain branch,
zero and negative boundaries in every argument position, large integers,
representative floats, empty/short/long arities, and all 68,921 integer triples
in `[-20,20]^3`.

Results:

- zero mismatches on all 8,000 strictly positive triples in `[1,20]^3`;
- documented examples and all positive named cases match;
- all four arity/empty cases raise the same `TypeError`;
- 493 mismatches over the whole signed cube;
- representative mismatches are `(0,3,3)` and `(-3,4,5)`, for which the
  canonical returns true because it squares the non-positive value, while the
  candidate returns false.

The differential command intentionally exits 1 because mismatches were found.
They are not hidden. I judge the signed mismatches outside the natural
precondition that the arguments are triangle side lengths; the candidate's
false result is the natural contract result for such invalid sides. However,
the canonical has a broader algebraic extension, and the prompt's lack of an
explicit integer type makes this a real audit qualification.

Evidence:

- script: [`differential_test.py`](evidence/differential_test.py)
- complete bounded result: [`stage2-differential.log`](evidence/stage2-differential.log)
- source/proof artifact listing:
  [`stage2-source-and-proof-artifacts.log`](evidence/stage2-source-and-proof-artifacts.log)

Stage 2 result: PASS for valid positive integer side lengths, with the
documented domain/canonical qualification.

## 3. Clean proof reconstruction

The independently installed live K tools are version 7.1.293. `kup` is absent,
but `kompile`, `krun`, and `kprove` are independently available and runnable.

From the scratch copy:

1. The trusted supplied semantics was compiled with LLVM as `MPY-KRUN`.
2. The exact submitted `solution.mpy` was run. It terminates with `.K`,
   `NoExc`, exit code 0, and the expected module binding to the submitted
   closure body.
3. A reviewer script mechanically appended assertions to the exact submitted
   `solution.py`, translated the result with the trusted translator, and ran it
   under the fresh LLVM definition. It covers every return branch, zero and
   negative boundaries, and a large Pythagorean triple; it also terminates with
   `.K`, `NoExc`, and exit code 0.
4. `verification.k` was compiled from source with the Haskell backend.
5. The unmodified seven-claim `spec.k` was proved in one run: exit 0 and
   `#Top`.
6. To make per-claim status unambiguous, a scratch-only copy added labels but
   changed no claim term, precondition, or postcondition. All seven claims were
   then selected and run separately. Each exits 0 and prints `#Top`.

The LLVM compiler's non-exhaustiveness warnings concern unused operations
(`mapStrVS`, several Float helpers, `joinCodes`, and empty `valSeqAt`).
None is reachable from this integer-only target. The Haskell proof definition
builds successfully; its only displayed source warnings are unused pattern
variables in imported string comparison rules.

Evidence:

- [`stage3-toolchain.log`](evidence/stage3-toolchain.log)
- [`stage3-kompile-llvm.log`](evidence/stage3-kompile-llvm.log)
- [`stage3-krun-solution.log`](evidence/stage3-krun-solution.log)
- [`stage3-concrete-driver-generation.log`](evidence/stage3-concrete-driver-generation.log)
- [`stage3-krun-concrete-audit.log`](evidence/stage3-krun-concrete-audit.log)
- [`stage3-kompile-haskell.log`](evidence/stage3-kompile-haskell.log)
- [`stage3-kprove-all.log`](evidence/stage3-kprove-all.log)
- mechanically labeled copy:
  [`spec-labeled.k`](evidence/spec-labeled.k)
- seven individual proof logs:
  [`positive-c`](evidence/stage3-kprove-positive-hypotenuse-c.log),
  [`positive-b`](evidence/stage3-kprove-positive-hypotenuse-b.log),
  [`positive-a`](evidence/stage3-kprove-positive-hypotenuse-a.log),
  [`nonpositive-a`](evidence/stage3-kprove-nonpositive-a.log),
  [`nonpositive-b`](evidence/stage3-kprove-nonpositive-b.log),
  [`nonpositive-c`](evidence/stage3-kprove-nonpositive-c.log), and
  [`positive-no-equality`](evidence/stage3-kprove-positive-no-equality.log).

Stage 3 result: PASS.

## 4. Adequacy and real-program pinning

### Plain-language meaning of every entry claim

All claims start in the same clean module/call state: environment 0; an empty
module scope whose parent is the supplied builtins scope; allocator 1; empty
heap and call stack; `noRet`; `NoExc`; and exit code 0.

1. If `A,B,C > 0` and `A²+B²=C²`, the call returns `true`.
2. If `A,B,C > 0` and `A²+C²=B²`, the call returns `true`.
3. If `A,B,C > 0` and `B²+C²=A²`, the call returns `true`.
4. If `A <= 0`, the call returns `false`.
5. If `A > 0` and `B <= 0`, the call returns `false`.
6. If `A > 0`, `B > 0`, and `C <= 0`, the call returns `false`.
7. If all three are positive and none of the three equalities holds, the call
   returns `false`.

These cases cover every K integer triple: the first non-positive argument
selects claims 4-6; otherwise at least one equality selects claims 1-3, or none
selects claim 7. The result is a ground Boolean in every destination, not a
free variable, implication-only postcondition, or tautology. All other cells
must return to their initial values.

### Mechanical program identity

`verification.k` does not load the whole module. It defines the exact body as a
nullary K function, constructs
`closureVal(("a","b","c"), BODY, 0)`, and rewrites the adapter to a normal fixed
semantics `Call`.

This is a permitted direct-function normalization, not a summary oracle:

- trusted regeneration pins `solution.py` to `solution.mpy`;
- a reviewer extractor takes the `FuncDef` body from that submitted
  `solution.mpy` and the rule RHS from `verification.k`;
- both are parsed by the fresh K definition as `Stmts`;
- the only normalization replaces rule-language `.Stmts` with the external
  parser's omitted empty `Stmts` production;
- the resulting KORE files are byte-identical, both SHA-256
  `5cf698c5c229b9209e52d805346cc16c38e8e87b952042d59993e0abc266d054`;
- fixed `FuncDef` semantics produces the same parameter tuple, body, and
  defining environment 0 as the proof-local closure.

The adapter preserves its continuation and delegates argument evaluation,
binding, control, return, and all cells to the supplied semantics.

Evidence:

- [`stage4-constructor-comparison.log`](evidence/stage4-constructor-comparison.log)
- extracted submitted body: [`solution-body.mpy`](evidence/solution-body.mpy)
- raw and parser-normalized proof body:
  [`verification-rule-body.raw`](evidence/verification-rule-body.raw) and
  [`verification-rule-body.mpy`](evidence/verification-rule-body.mpy)
- canonical KORE terms:
  [`solution-body.kore`](evidence/solution-body.kore) and
  [`verification-rule-body.kore`](evidence/verification-rule-body.kore)
- extractor: [`extract_program_terms.py`](evidence/extract_program_terms.py)

### Satisfiability, ground substitution, and body sensitivity

Ground witnesses for claims 1-7 are respectively `(3,4,5)`, `(3,5,4)`,
`(5,3,4)`, `(0,1,2)`, `(1,0,2)`, `(1,2,0)`, and `(1,2,3)`. Each satisfies its
precondition, and the claimed result agrees with both Python implementations.
The same evidence explicitly records the broader non-positive boundary
`(-3,4,5)`, where the candidate and canonical differ.

A separate body-sensitivity mutation changed the first true return to false in
the actual `verification.k` body executed by the claim. The mutated definition
builds successfully, but the corresponding positive claim exits 1 with
`WarnStuckClaimState`; its residual contains `false` where the destination
requires `true`. This changes the proof-executed program term itself, not merely
an external source file.

Evidence:

- [`claim_witnesses.py`](evidence/claim_witnesses.py) and
  [`stage4-claim-witnesses.log`](evidence/stage4-claim-witnesses.log)
- [`verification-body-mutation.k`](evidence/verification-body-mutation.k)
- [`spec-body-mutation.k`](evidence/spec-body-mutation.k)
- [`stage4-body-mutation-kompile.log`](evidence/stage4-body-mutation-kompile.log)
- [`stage4-body-mutation-kprove.log`](evidence/stage4-body-mutation-kprove.log)

Stage 4 result: PASS.

## 5. Rule-by-rule static soundness review

The exhaustive inventory covers `semantics.k`, all 23 helper files, and
`verification.k`: 25 files, 934 declarations, 230 syntax declarations, one
configuration, five contexts, and 698 rules. It records every local function,
all 107 `total` declarations, all 25 `symbol` declarations, all 45 priority
rules, all 26 `owise` rules, all 35 concrete rules, and every ordinary rule.
There are no `simplification` or `functional` declarations.

Each inventory row has an explicit decision:

- `ACCEPTED_MATERIAL` for the 72 declarations on the exact parse, load,
  call, argument, binding, lookup, arithmetic, comparison, branch, and return
  slice;
- `ACCEPTED_NONMATERIAL` for the remaining 862 declarations whose constructor,
  value sort, operator literal, or unreachable helper continuation separates
  them from every target redex. Those remain in the fixed supplied-semantics
  trust boundary and cannot enable a target-domain false conclusion.

The target uses:

`Module`, `FuncDef`, `Params`, `Stmts`, `Call`, `Name`, `Int`, `Bool`,
`BinOp`, `Compare`, `CmpOp`, `If`, and `Return`.

For these constructs:

- `BinOp` is `seqstrict(2,3)`; `Compare` contexts evaluate left before right;
  `If` and `Return` evaluate their expression first; call semantics evaluates
  the callee and arguments left-to-right.
- A call allocates one plain callee scope, pushes the exact continuation and
  caller environment, binds `a,b,c`, executes the real body, and pops back to
  the unchanged initial cells.
- `Name` lookup finds the bound integers in that callee scope. Higher-priority
  cell rules require `"$cells"` and cannot match the plain target frame.
- Heap-reference priority rules cannot match because the heap is empty and all
  material operands are integers or Booleans.
- Integer `+`, `*`, `<=`, and `==` equations are unique on `Int,Int`; competing
  Float, Bool, collection, membership, and `None` equations are sort- or
  operator-disjoint. K and Python integers are unbounded.
- The material `appendVal` total equations are disjoint, exhaustive, and
  structurally descending. `builtinsScope` and both proof-local nullary
  functions have one exhaustive ground equation each.
- `Return(V) ~> _` correctly discards only the remainder of the current
  function, records `V`, and delegates restoration to the saved frame.

`verification.k` itself has exactly three syntax declarations and three rules:
the exact body equation, exact closure equation, and adapter-to-`Call` rewrite.
It has no opaque term, fresh value, priority rule, simplification, concrete
equation, result summary, task-answer rule, or state-changing bridge. Nothing
replaces the arithmetic or branch computation.

The 25 `symbol(...)` declarations are Float helpers, sorting helpers, and MD5;
all are unreachable here. `MPY-CONCRETE` is not imported into the proof.
Compiler warnings about non-exhaustive unused total functions are therefore a
global limitation of the supplied subset, not a target proof rule and not a
false-conclusion witness for any satisfying target state.

No inventoried rule supplies a concrete or symbolic witness enabling a false
target-domain conclusion. Accordingly, no rule is labeled unsound merely from
an unused-semantics evidence gap.

Evidence:

- full row-by-row inventory: [`rule-inventory.md`](evidence/rule-inventory.md)
- target slice and overlap analysis:
  [`static-slice-review.md`](evidence/static-slice-review.md)
- source declaration index:
  [`stage5-declaration-index.log`](evidence/stage5-declaration-index.log)
- special attributes:
  [`stage5-special-attributes.log`](evidence/stage5-special-attributes.log)
- complete material source listing:
  [`stage5-material-semantics-source.log`](evidence/stage5-material-semantics-source.log)
- complete remaining source listing:
  [`stage5-nonmaterial-semantics-source.log`](evidence/stage5-nonmaterial-semantics-source.log)

Stage 5 result: PASS.

## 6. Fresh non-vacuity test

The reviewer-created `spec-vacuity-audit.k` changes the first positive result
from `true` to `false` while retaining the satisfiable precondition
`A,B,C > 0` and `A²+B²=C²`. The concrete witness `(3,4,5)` makes the mutation
false.

`kprove --dry-run` exits 0, establishing that the mutation parses and builds
against the fresh proof definition. The actual proof then exits 1 with
`WarnStuckClaimState`. Its residual has `true ~> .K`, while the destination
requires `false`, under the original positive Pythagorean constraints. This is
the expected unmet result obligation, not a parser error, timeout, missing
import, unrelated crash, or unreachable mutation.

Evidence:

- mutation: [`spec-vacuity-audit.k`](evidence/spec-vacuity-audit.k)
- [`stage6-vacuity-dry-run.log`](evidence/stage6-vacuity-dry-run.log)
- [`stage6-vacuity-kprove.log`](evidence/stage6-vacuity-kprove.log)

Stage 6 result: PASS.

## 7. Proven versus assumed accounting

### What the reachability proof establishes

Under the supplied MPY semantics and the stated clean initial configuration,
executing the exact submitted `right_angle_triangle` body on any K integer
triple terminates through one of the seven claim cases and returns:

- `false` if any argument is non-positive;
- otherwise `true` if and only if one of the three Pythagorean equalities
  holds;
- otherwise `false`.

The call returns with the caller environment, scopes, allocators, empty heap,
empty stack, `noRet`, `NoExc`, and exit code 0 restored exactly as specified.
This is result-constraining, non-vacuous, and body-sensitive.

### Trust ledger

1. **Trusted supplied MPY semantics.** The immutable candidate copy matches the
   trusted mounted tree exactly. The material rules were statically reviewed;
   unused subset operations, including opaque Float/sort/MD5 symbols and the
   compiler's unused totality gaps, are outside this theorem.
2. **K implementation and built-in mathematics.** Correctness of K 7.1.293,
   its parser, Haskell/LLVM backends, reachability engine, maps/lists, and
   unbounded integer/Boolean hooks is trusted.
3. **Trusted translator.** The mounted translator is trusted by the task;
   byte-identical regeneration establishes the source-to-constructor bridge.
4. **Direct function-binding bridge.** This is not assumed empirically:
   parameter names, body, and defining environment are mechanically compared
   to fixed `FuncDef` behavior and byte-identical KORE.
5. **Pythagorean intent bridge.** Ordinary mathematics is used informally to
   identify the disjunction of the three square equalities with a right angle
   for positive side lengths. K proves execution of that algebraic test; it
   does not formalize Euclidean geometry.
6. **Input-domain interpretation.** The formal theorem is over K integers. The
   natural phrase “triangle side lengths” supplies positivity. The trusted
   prompt has no type annotation, so arbitrary positive Python floats or other
   numeric classes are not formally covered even though finite positive-float
   differential examples agree. This is the principal non-fatal limitation.
7. **Canonical comparison.** Finite differential testing supports agreement
   over positive integers only; it is not a universal proof. The signed-input
   disagreement is explicitly excluded from the valid-side precondition and
   remains visible in the evidence.
8. **Termination framing.** The audit reports the requested partial-correctness
   result. The straight-line symbolic executions close for every formal case;
   no separate general CPython termination or exception theorem is claimed.

### Gate accounting and decision

- Gate A, real-program soundness: PASS.
- Gate B, intent adequacy: PASS for the material positive-integer side-length
  domain, with an explicit untyped-domain/canonical-extension qualification.
- Gate C, trust and reproducible evidence: PASS.

The proof is legitimate: it is fresh-reconstructed, exact-body-pinned,
result-constraining, non-vacuous, and free of proof-local semantic shortcuts.
I select `CONCERNS` rather than `PASS` because the untyped prompt does not itself
prove that integer side lengths are the entire Python-facing source domain, and
because the trusted canonical has a different algebraic extension on
non-positive integers. These do not make a false conclusion provable for valid
positive integer triangle sides and do not invalidate the theorem about the
real submitted program.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
