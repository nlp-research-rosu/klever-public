# Independent audit: `90-next-smallest`

## Scope and outcome

I audited Stage 3 classification, deterministic Stage 4 generation, and the
selected Stage 5 Lean proof independently of the prior reviews and recorded
outcomes. The launcher environment and the signed audit input both select
`CLASSIFICATION_AND_PROOF` for condition `kit-semantics` with
`SUPPLIED_SEMANTICS`. The resolved audit-input digest is
`b362022854319496b9ea5f32ded581fabd33a550d94876c1af5a79e6e2697c9f`.

The classification is mathematically sound, Stage 4 is a deterministic and
bijective export of the five genuine domain lemmas, and `Proof.final` proves
the unchanged generated target using honest source-relevant operational
bindings. I found no unrecorded trust escape or target substitution.

## Producer provenance and bound inputs

I hashed the mounted generation-time producer sources before judging Stage 4:

| Producer | Observed SHA-256 |
|---|---|
| `klean_export.py` | `74842302afea69a17a4815cf1213f080da4ac56d53b80d181f27196ec4112d63` |
| `klean.py` | `659c1d1c627ff2ca101ab8f9b5a1f1d73968e019e2a305f4ec1d1afa2d8c5a91` |

Both hashes match `generation-tools/source-manifest.json`, the generator
manifest, and their audit-input provenance. The immutable generator image ID
is consistently
`sha256:21e4151b8f48811e6c31994b3719c3e8a4a787856e1d3911ca9700e54a39c910`:
it is in both manifests and is the image-addressed component of the producer
path recorded in `/audit-input.json`. The producer-source pipeline tree hash
is `1e5faff11bfada41bad76e5f42fbbbc6101a6155bd2f81524eca8cd7c87cdab1`,
also exactly matching the audit input. There is therefore no producer-source
infrastructure error.

The trusted post-build binding check also recomputed and matched all relevant
pipeline hashes: Stage 1 workspace
`7a933b40e562a12f0c83540bbc10e0f46c9cf0d6e64cc955661ac66c43adb2cd`,
Stage 2 audit
`8c04bcc986e107374d26f37f1c0a046d33aa9107060719632d2491e774457f73`,
Stage 3 manifest
`7a553a7f85a708d7498a8bb06efe9632781adf86ca5e501cc74888a17afb6b21`,
Stage 4 directory
`b827ac4f09ebc6f4bd4b560c671165c98e427353edd715000cab4e4b4d876421`,
and candidate workspace
`289e38b94242170aa86815fdc63368ace3bddee3ba37a6ad6e13218b041a56f4`.

Evidence: `evidence/producer-source-hashes.log`,
`evidence/producer-provenance-crossrefs.log`,
`evidence/producer-sources-pipeline-tree-hash.log`, and
`evidence/post-build-bindings.log`.

## Stage 3 inventory reconstruction

I ran the trusted `tools.k_rule_inventory.inventory_verification` code on the
frozen `/reference/k-proof`, then independently re-extracted every recorded
source span from `verification.k`, normalized its whitespace, recomputed its
source hash and `source_rule_id`, and recomputed the canonical whole-inventory
hash. The local verification-module closure contains exactly module
`VERIFICATION` and exactly 32 rules in source order.

The frozen `verification.k` SHA-256 is
`39ef1863ae8c319165119661dba9507a3e58f9d177eba0f59b3d9df4420a3f3f`.
The reconstructed inventory hash is
`3958f6820b90d65233bc4d4a3ec51b55238409e271c26efe964ec46a14f39f5f`.
The 32 reconstructed identities match `/reference/lemma-discovery.json`
bijectively and in the same order. There are no omitted, duplicated, extra, or
reordered rules and no span, source hash, identity, or inventory-hash change.

### Independent classification judgment

The manifest's count of 27 `DEFINITION` and 5 `DOMAIN_LEMMA` entries is
correct:

| Frozen rules | Count | Judgment |
|---|---:|---|
| Lines 10–44: `nextSmallestLoopBody`, `nextSmallestBody`, `solutionProgram` | 3 | Definitions of named constructor-valued program terms |
| Lines 48–55: `allInts` equations and `definedProjectInt` | 3 | Definitions of named domain summaries/predicates |
| Lines 64–66 and 72–74: `projectIntTotal` equations | 3 | Definition of the named totalized projection on its specified domain, including its direct and idempotent equations |
| Lines 97–142: `scanStep`, `scanAfter`, and `scanVS` equations | 10 | Definitions of the mathematical recurrence/summary |
| Lines 149–152: four `scanState` accessors | 4 | Named summary projections |
| Lines 155–162: `lastInt` equations | 3 | Named recurrence |
| Lines 165–170: `nextSmallestSpec` | 1 | Named postcondition term |

The five domain lemmas are precisely:

1. `rule-031285...`, lines 60–62: definedness of the partial `Val`-to-`Int`
   projection.
2. `rule-22fa1e...`, lines 68–70: the guarded partial projection equals the
   named total projection.
3. `rule-3efffc...`, lines 78–81: guarded integer `applyBin("+")` dispatch.
4. `rule-d010c...`, lines 83–86: guarded integer `applyCmp("<")` dispatch.
5. `rule-d3f351...`, lines 88–91: guarded integer `applyCmp("!=")` dispatch.

These five rules do not define fresh summary names and are not ordinary
execution rules. They restate or connect imported operational semantics after
sort refinement, so classifying them as definitions or operational rules
would be wrong. They are also not proved-derived lemmas: Stage 1 compiles one
`VERIFICATION` module already containing them and then performs one later
`kprove`; there is no earlier proof of the exact rules against a module from
which they were absent.

All five are relevant. The frozen solution's loop executes `x + 0`, tests
`x < smallest`, tests `x != smallest`, and may test `x < second`; its contract
is a list of integers. The projection and three guarded dispatch equations are
exactly the bridges needed for those source operations. The imported
operational semantics independently gives
`applyBin("+", I1:Int, I2:Int) => I1 +Int I2` and the corresponding `<` and
`!=` rules. No irrelevant domain theorem is present.

Every rule marked `simplification` is one of these five domain lemmas or one
of the named definitions above. There are no locally classified
`OPERATIONAL_RULE` or `PROVED_DERIVED_LEMMA` entries.

Evidence: `evidence/reconstructed-rule-inventory.log`,
`evidence/audit-checks-result.log`, `evidence/verification-k-numbered.log`,
`evidence/stage1-prove-sh.log`, and
`evidence/operational-k-source-excerpts.log`.

## Stage 4 deterministic generation

I reran the exact trusted
`tools.klean_preflight.check_generation(/reference/k-proof,
/reference/lemma-discovery.json, /reference/klean-generation)` call with
`PYTHONPATH=/reference`. It returned `status: PASS`, rebuilt the generated
project after `lake clean`, found 5 obligations and 0 designated sorries, and
reported:

- Stage 1 export tree:
  `f448ab908c5b67708e7e2230307edaa4ee64aed020179b226969cfc0cf894338`.
- Generated tree:
  `139337fd5c01fe3f0a8fb7a6622b1814069c92facf163b46b1fa8a539c015460`.
- Stage 3 manifest:
  `7a553a7f85a708d7498a8bb06efe9632781adf86ca5e501cc74888a17afb6b21`.

The normal preflight's Lean launcher initially could not inspect a child
`/proc/<pid>/exe`, because numeric child PID entries are hidden in this audit
sandbox. I reran it with an audit-authored, narrow `readlink` shim that handles
only numeric `/proc/<pid>/exe` lookups and returns the pinned Lean executable.
It does not alter sources, declarations, elaboration, or the kernel. The
successful run used Lean 4.22.0 commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, exactly as locked in
`klean-toolchain.lock.json`. Both the failed environment diagnostic and the
complete successful transcript are retained.

I then independently checked each obligation record, source span/hash,
conjunct hash, parameter binding hash, and target hash. The five domain rule
IDs map one-to-one and in source order to five generated conjuncts: projection
definedness, guarded projection equality, integer addition dispatch, integer
less-than dispatch, and integer inequality dispatch. There are no omissions,
duplicates, irrelevant additions, reordered identities, or weakened source
guards.

The first generated formula contains an inner `∧ True`. This is not a padded
or vacuous top-level obligation: it is the exact Lean image of the frozen
source's `#And #Ceil(@V)`, where `@V` is already a well-sorted `Val`. The
remaining equivalence—successful `Int` projection iff
`definedProjectInt V = true`—is non-vacuous. The other four top-level
conjuncts are non-vacuous guarded equations. Thus the target has five genuine
obligations, not a fabricated count maintained with `True`.

The fixed target is:

- Declaration: `Klean90NextSmallest.Lemmas.targetStatement`
- Statement hash:
  `63819d1dd2623e6874489ae7d2e836b4b467d4c024fc1231beeace8c6b408a83`
- Definition hash:
  `1f53ff70601c3688ec45edd2aa4a4472ca17c3f11917590c820d5c0c79ac33b7`
- Parameters: 11, each with the exact recorded `kore_symbol`, type,
  `source_rule_ids`, and binding hash.

The generator manifest, audit input, reference generated source, expected
deterministic conjunction, and fresh `Base` copy all produce exactly those
values. This is not a `KLEAN_NO_OBLIGATIONS` case: the true domain set has five
entries and the generated target is present as required.

Evidence: `evidence/klean-check-generation-proc-shim.log`,
`evidence/audit_checks.py`, `evidence/audit-checks-result.log`,
`evidence/obligation-map.log`, and `evidence/generated-target-source.log`.

## Stage 5 Lean proof

I created a fresh project at
`/tmp/audit-work/stage5-90-next-smallest-audit-001`, copied the candidate-only
project into its root, and copied the immutable generated project into
`Base/`. The fresh `Base` tree retained the exact generated hash
`139337fd5c01fe3f0a8fb7a6622b1814069c92facf163b46b1fa8a539c015460`.

Both mandatory commands succeeded from that fresh root:

- `lake clean`: exit 0.
- `lake build`: exit 0, with every generated and candidate module rebuilt and
  `Build completed successfully.`

The source scan outside `Base` finds no `sorry`, `admit`, `unsafe`, `axiom`,
or `opaque`; there are no symlinks and no candidate declaration shadows
`targetStatement`. The trusted structural candidate gate finds every one of
the 11 exact parameter definitions once and finds exactly one `theorem final`
whose normalized statement is the generator-manifest statement. A separate
Lean `#check` elaborates `Proof.final` at exactly that target application, so
the proof is not a weakened, duplicated, or vacuous variant.

The exact axiom output is:

```text
'Proof.final' depends on axioms: [propext, Classical.choice, Quot.sound]
```

The trusted final-gate parser recognizes those three as Lean's permitted core
logical primitives. None of the 51 generated declarations in
`trust-inventory.json` is a dependency of `Proof.final`; `sorryAx` is absent,
and the set of unexpected dependencies is empty. The candidate therefore adds
and uses no proof trust escape.

Evidence: `evidence/fresh-lake-clean.log`,
`evidence/fresh-lake-build.log`, `evidence/post-build-bindings.log`,
`evidence/fresh-candidate-forbidden-token-scan.log`,
`evidence/fresh-candidate-target-shadow-scan-excluding-base.log`,
`evidence/proof-final-axioms.log`, and
`evidence/axiom-reconciliation.log`.

## Operational bridge audit

I located all 11 target bindings in `Proof.lean` and compared them with their
manifest `kore_symbol`, bound source rule IDs, frozen rules, source program,
and imported K operational semantics:

| Bindings | Independent operational judgment |
|---|---|
| `_andBool_`, `_<Int_`, `_=/=Int_`, `_+Int_` | Exact Lean `&&`, integer `<`, integer `!=`, and integer `+`; these match the K hooks used by the five rules. |
| `applyBin` | Delegates to a nonconstant dispatch model. Its source-relevant `"+"`/two-integer branch returns an injected integer sum exactly as `MPY-INT` line 9 requires. |
| `applyCmp` | Delegates to a nonconstant dispatch model. Its integer `"<"` and `"!="` branches exactly match `MPY-INT` lines 22 and 27. |
| `definedProjectInt` | True exactly for the `SortVal.inj_SortInt` constructor, matching `definedProjectInt(V) => isInt(V)`. |
| `isInt` | True exactly for a singleton K term containing an injected integer, matching the flattened K subsort membership used by the generated target. |
| `project:Int` | Returns the contained integer on precisely that projection domain. Its total Lean fallback is outside the source rule's honest guard. |
| `projectIntTotal` | Returns the contained integer for integer `Val`s. The fallback completes a K function whose operational equations leave non-integer inputs unspecified; every source use is guarded by `isInt`/`definedProjectInt`. |
| `project:Int?` | Returns `some` exactly on an injected integer K term and `none` otherwise, correctly exposing the partial K projection's definedness. |

The proof does not exploit the fallback values: for each arithmetic or
comparison equation it first derives that both guarded `Val`s are integer
constructors, substitutes their integer witnesses, and only then reduces the
operation. This rules out a default-value shortcut.

I compiled adversarial examples covering true/false conjunction, negative
integer arithmetic, `<` in both directions, equal and unequal `!=`, successful
and failed projections, integer and non-integer sort membership, and the
source dispatches. Counterfactual `"-"` and `">"` examples also succeed, so
the dispatch definitions are not hard-coded solely to the target's `+`, `<`,
and `!=` equations.

I separately compiled mutation refutations. With the honest conjunction and
integer recognizer, a constant-zero addition, a constant-false comparison,
and a constant-false definedness predicate each contradict the fixed target
on an explicit integer input. A constant-false conjunction would make the
three guarded dispatch equations vacuous; the candidate's actual `&&`
definition is explicitly distinguished from that attack. These checks confirm
why the operational bindings, rather than the clean build alone, make this
proof legitimate.

Evidence: `evidence/candidate-proof-numbered.log`,
`evidence/operational-bridge-probe-sources.log`,
`evidence/operational-bridge-adversarial.log`, and
`evidence/operational-bridge-mutations.log`. The principal commands and the
environment-only `/proc` workaround are documented in
`evidence/COMMANDS.md`.

VERDICT: PASS
LEGITIMACY: LEGIT
