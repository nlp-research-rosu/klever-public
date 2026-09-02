# Independent audit: `20-find-closest-elements`

## Scope and conclusion

I audited condition `kit-semantics`, semantics mode `SUPPLIED_SEMANTICS`, in
launcher mode `CLASSIFICATION_AND_PROOF`. I treated candidate files, comments,
logs, and prior verdicts as untrusted evidence. The frozen Stage 3
classification is complete and mathematically correct; deterministic Stage 4
generates exactly the three necessary domain obligations; and the Stage 5
candidate honestly implements the six operational bridge parameters and proves
the unchanged generated target without an unrecorded trust escape.

The proof-validation workflow influenced the audit by requiring a proof-local
definition review, an exact axiom query, concrete adversarial examples, and
counterfactual constant implementations in addition to clean builds.

Raw transcripts and helper sources are under `evidence/`; `evidence/INDEX.md`
maps the significant files.

## Producer provenance and mounted-input hashes

Before evaluating Stage 4, I hashed the mounted producer sources:

| Producer | Actual SHA-256 |
|---|---|
| `klean_export.py` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` |
| `klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` |

Both values exactly match `source-manifest.json` and
`generator-manifest.json`. The source manifest and generator manifest also
agree on immutable image
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`;
the image digest is the terminal component of the producer path recorded in
`/audit-input.json`. The producer tree hash is
`388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`,
also exactly the audit-input value. Producer provenance is therefore intact;
there is no infrastructure `AUDIT_ERROR`.

I also recomputed the mounted pipeline hashes with the trusted hash contract:

| Mounted input | Recomputed hash | Audit-input match |
|---|---|---|
| Stage 1 K workspace | `4b35e13b900f11aee5d7e5eb3a0830f3015dce2000584dc093dfe3c1097c3061` | yes |
| Stage 2 K audit | `0fea36929353dfdb36ec454ac93adce80bd36fbbdf54b5d8d218e62081c9c596` | yes |
| Stage 3 manifest | `11a42ca925f8bd9f3e0132a62ba15afa05f1d2567c5778dc634b8900e9878606` | yes |
| Stage 4 generation | `49efbfc3cf6e2f7222b19ea0d2d904b55a765312fcd2e01bb5b3b58c6b3c28c7` | yes |
| Generated export tree | `5f644afebd1db37fe6bfe4fb8513ee9735ab4ef0b00d8a6e66d68086d4735794` | yes |
| Stage 5 candidate workspace | `aa470de95f5bd6271edecd96e05f56f37fe01bcc25b2caeea371947b866a2cea` | yes |

The Stage 1 export-tree hash independently used by preflight is
`3d0a13610aea07976345ac28e3749f69244afe4d3c70c5d21c14b4ec8be3d864`,
matching both generator provenance and audit input.

## Inventory reconstruction and bijection

I ran the trusted rule-inventory implementation against the frozen
`/reference/k-proof`, allowing it to select the verification module from the
frozen `prove.sh`. The local verification-module closure, in source order, is:

1. `VERIFICATION-SYNTAX`
2. `VERIFICATION-BASE`
3. `VERIFICATION`

The frozen `verification.k` SHA-256 is
`b9e764e3facf84d15b16528150cbb78129c41bd7263b334a38b2ddfe5f510be9`.
Reconstruction found 36 rules and produced inventory hash
`3182719aa6a75a97355b7da5124d9c650a433fe9651a56b982053fc2b391951e`.
For every rule, the reconstruction recomputed its module, start and end line,
text, attributes, normalized source hash, and `source_rule_id`.

The protected Stage 3 manifest also contains 36 unique identities. Its identity
sequence is exactly equal to the reconstructed sequence, and its inventory hash
is exact. There are no missing, extra, duplicate, or reordered rules. The full
reconstruction is in `evidence/reconstructed-inventory.json`; all identities
and spans are in `evidence/13_inventory_classification_index.log`.

## Independent classification judgment

I independently classified all 36 entries from `verification.k`, the imported
operational rules, the source solution, and the postcondition. The per-entry
ledger is `evidence/independent-classification.md`. The resulting counts are:

| Class | Count | Inventory entries |
|---|---:|---|
| `DEFINITION` | 32 | 1–11 and 15–35 |
| `OPERATIONAL_RULE` | 0 | none |
| `DOMAIN_LEMMA` | 3 | 12–14 |
| `PROVED_DERIVED_LEMMA` | 1 | 36 |

Entries 1–4 expand named source/proof terms (`innerBody`, `outerBody`,
`findBody`, and `solutionModule`). Entries 5–11 define structural recognizers
and projections. Entries 15–35 are the exhaustive branches, base cases, and
strictly recursive equations defining the ordered-pair and loop-fold summaries.
These are genuine macros, summaries, projections, and recurrences, rather than
ordinary execution rules.

The three domain lemmas are exactly:

- `rule-db9d3a3e81dee21bb05c9f3240b23092771092e55e7bb6f53dc9fdcfa44b3188`
  (`verification.k` lines 141–147): canonical tuple index 0 agrees with
  `itemIndex`.
- `rule-c31085d90cc1a95717c3310bccb50623ab127a57e9e6010eb23e0aa2e4377dc7`
  (lines 148–154): canonical tuple index 1 agrees with `itemFloat`.
- `rule-1be94e05a1b1440cd44a316053a753efc65fc522fcdf2fd8218e40d546231a89`
  (lines 156–159): enumeration preserves the all-float item invariant.

These are cross-symbol mathematical facts, not definitions of `applyIndex`,
`enumVS`, or either recognizer. They are relevant: the frozen program constructs
`items = list(enumerate(numbers))`, then repeatedly accesses enumerated items at
indices 0 and 1; the loop summary requires the resulting sequence to contain
canonical `(Int, Float)` items. All three rules carry `[simplification]`, and
there are no other simplification rules. Thus every simplification is correctly
classified as a domain lemma.

Entry 36, lines 255–316, is legitimately `PROVED_DERIVED_LEMMA`. Frozen
`prove.sh` first compiles `VERIFICATION-BASE`, which excludes that rule, and
proves `CONNECTION-SPEC` against it. The claim has the same loop transition,
cells, updates, and precondition; its `builtinsScope` is definitionally the
exact explicit builtins map written in the later rule. Only after this proof
does `prove.sh` compile `VERIFICATION`, which adds the rule, and use it in the
main proof. I independently reran that connection proof with K 7.1.293; it
returned `#Top` with exit code 0. No domain lemma is hidden under another
classification.

## Deterministic Stage 4 generation

I reran the required
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and the
three specified mounted inputs. It returned `PASS`, clean/build exit codes 0,
three obligations, zero designated sorries, 45 generated trust declarations,
and the expected hashes and target.

The independently selected domain set is nonempty, so
`KLEAN_NO_OBLIGATIONS` would have been wrong. The selected generation instead
contains exactly three source rules and exactly three obligations, with this
source-order bijection:

1. index-0 projection rule → guarded Lean equation
   `applyIndex V 0 = Int(itemIndex V)`;
2. index-1 projection rule → guarded Lean equation
   `applyIndex V 1 = Float(itemFloat V)`;
3. enumeration-preservation rule → guarded Lean equation
   `allFloatItems (enumVS VS start) = true`.

Each obligation repeats the exact source identity, span, normalized hash,
inventory hash, and discovery-manifest hash. Each Lean conjunct hash recomputes.
There are no extra, omitted, duplicated, or reordered obligations.

This is also mathematically faithful. The first two hypotheses equate the
injection of `V` with the injection of the canonical two-field tuple. Generated
`Inj SortVal SortKItem` maps an iterable-valued `SortVal` to the same
`SortKItem.inj_SortIterable` constructor, so canonical tuples satisfy the
hypotheses; they are not constructor-disjoint or vacuous. The third hypothesis
is the nontrivial all-float premise. None of the conjuncts is `True`, and each
is used by the frozen program invariant.

The obligation-map SHA-256 is
`3fb056b7b0269531d34c8bdb323d006f6ac9ae8edee301eae7d6aa8a64e9273a`.
All six parameter binding hashes recompute, their source-rule sets cover exactly
the three domain rules, and no parameter is unbound. Reconstructing the target
directly from the map yields the sole declaration
`Klean20FindClosestElements.Lemmas.targetStatement`, in this parameter order:

1. `allFloatItems`
2. `allFloatVS`
3. `applyIndex`
4. `enumVS`
5. `itemFloat`
6. `itemIndex`

The target definition hash is
`313f47d21624e36298278b262834a258ce9cbd00fa46254efb2df924d562c640`;
the fully applied statement hash is
`30dce5110f47337e8188766053cce7584b98f33ec418e650e021cc9f362c30bb`.
Those values and the complete normalized target object are identical in the
obligation map, generator manifest, required preflight result, and
`/audit-input.json`. `evidence/independent_stage4_check.py` performs a separate
stdlib-only reconstruction; its successful output is
`evidence/46_independent_stage4_check.log`.

## Lean environment and clean build

The sandbox exposes a PID namespace that is not mirrored by its read-only
`/proc`, causing Lean's attempt to read `/proc/<pid>/exe` to fail before source
elaboration. I retained all failed probes. To exercise the pinned toolchain, I
compiled the narrow, auditable shim in `evidence/lean_app_path_shim.c`; it only
intercepts that `/proc/*/exe` `readlink` and supplies
`/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lean`. Its source SHA-256
is `f582679c4e88a97aac7458584ee8710132424b9b96b82e72e10462b1a2137de6`.
It does not alter Lean source, generated files, theorem statements, or kernel
checking. The invoked toolchain reported Lean 4.22.0, commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, as locked.

I created fresh project
`/tmp/audit-work/stage5-proof-audit.H39UY0`, copied the candidate source into
it, and copied the exact generated project as `Base`. With the pinned
executable-path workaround, both `lake clean` and `lake build` exited 0.
Pre- and post-build hashes were identical for `Proof.lean`, `lakefile.lean`,
`lean-toolchain`, the generated `Base` target file, and
`Base/obligation-map.json`. The only output was the generated target's harmless
unused-hypothesis linter warning.

The candidate contains no `sorry`, `admit`, `unsafe`, new `axiom`, or new
`opaque`. It defines each of the six required parameters exactly once in
namespace `Proof`; it neither changes nor shadows the generated target.
`Proof.final` is unique and its printed type is exactly the fully applied fixed
target above, not a copy, weakening, or alternate proposition. The trusted
Stage 5 mechanical gate independently returned `PASS`.

## Axiom accounting and proof identity

The exact `#print axioms Proof.final` output was:

```text
'Proof.final' depends on axioms: [propext, Classical.choice, Quot.sound]
```

There is no `sorryAx`. `trust-inventory.json` records 45 generated Klean
trust-boundary axioms and no designated or other sorries. The trusted final-gate
contract forms the allowable set from those recorded declarations plus the
three standard Lean logical foundations `propext`, `Classical.choice`, and
`Quot.sound`. `Proof.final` uses exactly those three foundations and none of
the 45 generated Klean axioms. It introduces no candidate axiom or opaque
declaration. Thus every dependency is accounted for and there is no unrecorded
proof trust escape.

The proof itself establishes the two projection conjuncts by using injectivity
of the generated `SortVal → SortKItem` injection to recover the exact canonical
tuple from each guard, then reducing the honest definitions. It establishes
the enumeration conjunct by structural recursion over `SortValSeq`, rejecting
non-floats from the premise and incrementing the enumeration index. This is
exactly the generated three-conjunct proposition.

## Operational-bridge audit

I compared every target parameter with its exact KORE symbol and source-rule
bindings, the defining and domain rules in frozen `verification.k`, the
operational `subscript.k` and `builtins.k` rules, and the source program.

| Parameter | Independent operational judgment |
|---|---|
| `allFloatItems` | Empty is true; a nonempty sequence is accepted exactly when its head is a two-field `(Int, Float)` tuple and its tail is accepted. This is the concrete meaning of the K canonical-item equality and recurrence. |
| `allFloatVS` | Empty is true; a nonempty sequence is accepted exactly when its head is a float and its tail is accepted, matching `floatProjection` and the K recurrence. |
| `applyIndex` | Lists and tuples use the frozen `normIdx` rule, including negative indices, followed by structural `valSeqAt`. This covers every representable operational case used by the frozen source. |
| `enumVS` | Empty maps to empty; a head becomes `(currentIndex, value)` and recursion continues at `currentIndex + 1`, exactly matching `builtins.k`. |
| `itemFloat` | Returns the float component of exactly a canonical `(Int, Float)` tuple. |
| `itemIndex` | Returns the integer component of exactly a canonical `(Int, Float)` tuple. |

The frozen total projection functions do not constrain results outside their
canonical-tuple equations, and frozen total `valSeqAt` deliberately leaves
out-of-bounds or opaque results abstract. The candidate's `0`, `0.0`, and
`noneV` residual values merely choose total representatives for those
unconstrained/no-rule cases. They do not change any defined operational case
or help discharge a reachable source case. The exported `SortVal` has no
string-value constructor, while the source solution indexes only its input
float list, enumerated tuples, and the two-float `closest` tuple; all relevant
list/tuple cases are implemented.

I compiled 15 independent examples: empty and multi-float recognizers, rejection
of an integer and a malformed tuple, two distinct integer projections, two
distinct float projections, list indices 0 and 1, negative list indices -1 and
-2, tuple index 1, and enumeration beginning at 7. All checked successfully.
Six counterfactual constant implementations—one per target parameter—were then
tested on separating witnesses; all six proposed equalities failed to compile,
as expected. These results rule out constant, identity, hard-coded, and
vacuous bridge implementations in the candidate.

## Final judgment

The inventory and classification are bijective and correct; Stage 4 preserves
exactly the true domain-lemma set and fixed target; the clean Lean proof proves
that target with fully accounted foundations; and every operational parameter
implements the frozen reachable semantics. No concern affecting soundness,
relevance, identity, or provenance remains.

VERDICT: PASS
LEGITIMACY: LEGIT
