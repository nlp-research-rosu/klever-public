# Independent audit: HumanEval `55-fib`

This audit covers condition `kit-semantics`, semantics mode
`SUPPLIED_SEMANTICS`, and launcher mode `CLASSIFICATION_AND_PROOF`. I treated
the mounted candidate, prior reviews, logs, comments, and classifications as
untrusted evidence. The judgment below comes from reconstructed inventories,
recomputed hashes, fresh mechanical checks, frozen source semantics, and
independent Lean checks.

## Provenance and frozen inputs

The two exact generation-time producer sources are present and match all
available provenance:

- `klean_export.py`:
  `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07`
- `klean.py`:
  `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d`
- immutable generator image:
  `sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`

Those file hashes agree with `generator-manifest.json` and
`source-manifest.json`. The image ID agrees between those manifests and with
the image key in the launcher-selected producer-source path. The producer
bundle has exactly the expected three files, and its recomputed framed tree
hash is
`388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`,
matching `/audit-input.json`.

All recorded Stage 4 hash fields in the input, generator, export, preflight,
source, and launcher manifests were independently recomputed and matched. In
addition:

- all 769 per-file Stage 1 source hashes matched;
- Stage 1 framed tree:
  `04012b97dddd6c04f537af64d5312d57b1e23f50ac1afd195919e80bee60d347`;
- Stage 1 generator content tree:
  `2a8e92d63df96d6f8c5d0bda589bdf07a408baecb1f13d9e479206b5fad0cf30`;
- Stage 2 audit framed tree:
  `fa7712521352c40d0b56828525132dbb48972c268599100eb7e99e694578514f`;
- Stage 3 discovery file:
  `5b881da32bcb48b4c09f2b70dd5575850f35b58e2a685e083bf05e85ec893536`;
- full Stage 4 generation framed tree:
  `735bb045563ed78ffce381e0c52f59612e76c69e7423abd362ce26b4ee26b084`;
- generated-project content tree:
  `55791b2e084958ef4ccd51eddee0cdbd8df74ef7956e3f835f531bc145c0d8d4`;
- Stage 5 candidate framed tree:
  `deb8cf4644792c10715c2c0fef0dec18a9c3a9f4c8426e9eb8218a383d3499e8`.

The launcher resolution’s canonical digest recomputes to its recorded
`2b6f7f977d9645b1397901633e073012721787a28529b53f0721f6cdcf8b819a`.
The generator toolchain object is exactly equal to
`/reference/klean-toolchain.lock.json`. The launcher field
`audit.mechanical_checker_lock_sha256` is audit-image metadata, not the file
hash of that Lean toolchain JSON; the attempted comparison is documented and
corrected in the evidence.

Evidence: `01_manifests_and_producer_hashes.log`,
`06_recomputed_provenance_hashes.log`,
`32_launcher_and_toolchain_binding_clarification.log`, and
`34_exhaustive_stage4_hash_reconciliation.log`.

## Stage 3 inventory reconstruction

Using `/reference/tools/k_rule_inventory.py`, I reconstructed the local
verification-module closure as `VERIFICATION-SYNTAX` followed by
`VERIFICATION`. The syntax module has no rules. The exact inventory is:

| Span | Source rule ID / normalized SHA-256 | Independent class |
|---:|---|---|
| 18–19 | `rule-0151c94749b8017ab1ca7d238620beed0c8ae98bf6d0591e136a99bf3f95d944` | `DEFINITION` |
| 21–22 | `rule-c122a6c58de509694010cd1eeb7f5ecbec714b80ca196cf36fe97c8480fb570a` | `DEFINITION` |
| 24 | `rule-3937e2183350f860b8052e715b9784df8e149714f99e2077f426b8adaae07193` | `DOMAIN_LEMMA` |

The suffix of each `source_rule_id` is its independently recomputed normalized
source hash. The frozen `verification.k` hash is
`18abf12307cd9f1202675f2d40d6963a45738be59b07c1be9bd7bd9c76ea6bf1`.
The whole ordered inventory hash is
`7a8023c3b8bec86f0b00d2cce4a8ab35baa1a6a7b47c608ce8f154d9f2d1d923`.

The protected Stage 3 document contains exactly these three IDs in this order,
with no duplicate, omission, or extra ID, and the same whole-inventory hash.
The trusted `validate_trust_boundary` reconstruction also returns the same
source spans, text, attributes, and classifications. The raw first diagnostic
in `08_inventory_reconstruction.log` incorrectly expected the compact Stage 3
schema to duplicate source fields; the corrected ordered-ID/hash bijection is
recorded in `09_stage3_bijection_and_frozen_source.log`.

## Independent classification judgment

The two `fibFrom` rules are definitions. `fibFrom` is a named mathematical
summary declared as a total function. Its guards `N <=Int 0` and `N >Int 0`
are disjoint and exhaustive over K integers, and the positive equation
decreases `N`. The symbol is used by the proof specification and is not a
rewrite that intercepts the source program.

The rule

```text
(A:Int +Int B:Int) -Int A => B [simplification]
```

is a domain lemma. It does not define a new summary and is not an ordinary
program-execution rule. It is not a proved derived lemma: `prove.sh` compiles
the rule into `verification-kompiled` before every `kprove`, and Stage 1 never
first proves the exact rule against a module that omits it.

The lemma is relevant rather than ornamental. The frozen source loop performs
`b = a + b` and then `a = b - a`. Supplied semantics dispatch integer `BinOp`
to `applyBin`, then define the two cases with K’s hooked `+Int` and `-Int`.
The lemma is precisely the fact that the second assignment restores old `b`,
which aligns one operational loop iteration with the recursive `fibFrom`
summary used in the invariant and call postcondition. It is also the only
`[simplification]` rule, so every simplification rule is classified as either
a definition or domain lemma as required.

Evidence: `09_stage3_bijection_and_frozen_source.log`,
`10_operational_semantics_source.log`, and
`11_independent_classification.md`.

## Deterministic Stage 4 generation

I reran the required check:

```text
PYTHONPATH=/reference python3
tools.klean_preflight.check_generation(
  /reference/k-proof,
  /reference/lemma-discovery.json,
  /reference/klean-generation,
  toolchain_lock=/reference/klean-toolchain.lock.json)
```

The audit sandbox exposes a `/proc` mount from a different PID namespace, so
the first invocation reached the fresh build and then Lake could not locate
its own installation. I diagnosed this independently. A local `LD_PRELOAD`
shim rewrites only `/proc/<digits>/exe` reads to `/proc/self/exe`; it does not
change Lean, the project, imports, declarations, or theorem checking. With the
shim, the frozen toolchain gate reported K 7.1.293, pyk/Klean 7.1.293, Lean
4.22.0 at commit `ba2cbbf...`, and Codex 0.144.6. The rerun returned `PASS`,
with successful `lake clean` and `lake build`, one obligation, zero designated
sorries, 43 generated trust declarations, and the recorded generated-tree
hash. The shim source, binary hashes, initial failure, and successful rerun
are all preserved in `13`–`18`.

There is one genuine domain lemma and exactly one generated obligation:

```text
∀ (A : SortInt) (B : SortInt),
  («_-Int_» («_+Int_» A B) A : SortInt) = (B : SortInt)
```

Its rule ID, source span, normalized hash, inventory hash, discovery hash, and
conjunct hash all match. The source-rule list, obligation list, and
obligation-map source list form the same ordered singleton bijection. Both
quantified variables materially occur; the equality is not a reflexive or
constant conjunct. It is the exact Lean translation of the frozen K arithmetic
identity, with no omitted guard, weakened conclusion, extra rule, or duplicate.

The target occurs exactly once:

```text
Klean55Fib.Lemmas.targetStatement «_-Int_» «_+Int_»
```

Its declaration is in `Klean55Fib/Lemmas.lean`. The independently regenerated
definition hash is
`18151bc47642a5dd78d25f321e0039bedbcd347bb9c280550a6bda22113a14bc`,
and the statement hash is
`2405f80f137462c57eba4892261cb6f18eb9431062c1f4b03a192092d0e35614`.
The extracted target equals the generator manifest, recorded preflight, and
launcher target byte-for-byte and field-for-field.

Evidence: `18_preflight_rerun_with_toolchain_shim.log` and
`23_independent_stage4_bijection_target.log`.

## Stage 5 Lean proof

I created `/tmp/audit-work/lean-proof-audit`, copied the candidate, and copied
the immutable generated project into it as `Base`. Before building, the fresh
`Base` content-tree hash exactly matched the immutable generated tree. I then
ran:

```text
LD_PRELOAD=/tmp/audit-work/proc_exe_shim.so lake clean
LD_PRELOAD=/tmp/audit-work/proc_exe_shim.so lake build
```

Both exited 0; the complete output is in
`25_fresh_lake_clean_build.log`. After the build, the target source in `Base`
remained byte-identical to the reference target.

The candidate:

- contains no `sorry`, `admit`, `unsafe`, `axiom`, or `opaque`;
- defines each required parameter exactly once;
- does not enter or shadow `Klean55Fib.Lemmas`;
- has exactly one `theorem final`;
- states `Proof.final` with the exact fixed generated target, not a copy or
  weakened variant.

The exact axiom query returned:

```text
'Proof.final' depends on axioms: [propext]
```

`sorryAx` is absent. `propext` is Lean core logical trust explicitly recognized
by the trusted final-gate policy alongside `Classical.choice` and `Quot.sound`;
it is not a new candidate or generated application axiom. None of the 43
generated trust-inventory declarations is used by `Proof.final`, and there is
no unapproved dependency. The trusted full final gate independently returned
`PASS`, the exact target, and `used_axioms: ["propext"]`.

Evidence: `24_fresh_proof_copy.log`,
`25_fresh_lake_clean_build.log`, `26_candidate_static_target_gate.log`,
`27_print_axioms_exact.log`, `28_trusted_final_mechanical_gate.log`, and
`29_axiom_reconciliation.log`.

## Operational bridge for target parameters

Both target parameters have honest total implementations:

| KORE symbol | Binding hash | Candidate definition | Frozen operational meaning |
|---|---|---|---|
| `Lbl'Unds'-Int'Unds'` | `72b40ba2c4e2f74b451341b4a76c70a39bc3f8a6a5347c41815bba2ea467e939` | `x - y` | hooked `INT.sub` / K `x -Int y` |
| `Lbl'UndsPlus'Int'Unds'` | `cf0ccb3a658b4844aae3fb4fb85f5b56762665a951b3afb5ae211f96cd7c3a20` | `x + y` | hooked `INT.add` / K `x +Int y` |

Both bind to the exact singleton source-rule ID. Compiled KORE confirms the
symbols are total hooked `INT.sub` and `INT.add`. Frozen `int.k` uses them for
integer `applyBin("-")` and `applyBin("+")`; the source solution uses exactly
those operations. Generated Lean defines `SortInt := Int` and models the same
hooks as `some (x - y)` and `some (x + y)`.

Lean independently checked, for arbitrary `x` and `y`, that each candidate
definition is definitionally equal both to the corresponding Lean integer
operation and to the generated root hook model. Adversarial negative, zero,
mixed-sign, and large-magnitude examples produced `-3`, `-11`, `1`, and
`-24691357802469135780` as expected.

A counterfactual projection implementation
`badAdd _ y := y; badSub x _ := x` proves the parameterized target by `rfl`
while disagreeing with integer arithmetic. This demonstrates that a clean
proof of the equation alone would not establish the operational bridge. The
submitted candidate does not use that shortcut: its universal definitional
equalities establish the exact bridge. A constant-zero counterfactual was also
rejected by Lean on the fixed target.

Evidence: `30_operational_bridge_adversarial_tests.log` and
`31_operational_bridge_source_binding.log`.

## Final judgment

The protected classification is complete and independently correct; the
nonempty true domain-lemma set is represented by an exact, nonvacuous Stage 4
obligation and immutable target; and the Stage 5 candidate cleanly proves that
exact target with fully faithful integer-operation bindings and no unrecorded
trust escape.

VERDICT: PASS
LEGITIMACY: LEGIT
