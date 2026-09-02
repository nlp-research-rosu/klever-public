# Independent Stage 3/4 Audit: `11-string-xor`

## Scope and outcome

This audit covers HumanEval problem `11-string-xor`, condition
`kit-semantics`, semantics mode `SUPPLIED_SEMANTICS`. The launcher-recorded
mode is `CLASSIFICATION_ONLY`. Stage 4 selected
`KLEAN_NO_OBLIGATIONS`; `/candidate` is absent, and the launcher records no
Stage 5 workspace, invocation, result, or target. Therefore no Stage 5 Lean
proof, `Proof.final`, axiom print, or operational-bridge parameter definition
is applicable.

I independently reconstructed the Stage 1 rule inventory, reclassified every
entry from the frozen K source and operational semantics, rebuilt and reran
the two relevant K proofs, checked body and continuation sensitivity, verified
all launcher and manifest hashes, and reran the trusted Stage 4 preflight. The
protected Stage 3 classification is correct. The true `DOMAIN_LEMMA` set is
empty. Consequently, Stage 4's empty obligation map, null target, absent Stage
5 candidate, and `KLEAN_NO_OBLIGATIONS` status are legitimate.

## Producer provenance gate

This gate passed before any Stage 4 judgment:

- `/reference/generation-tools/klean_export.py` hashes to
  `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07`.
- `/reference/generation-tools/klean.py` hashes to
  `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d`.
- Those exact values occur in both `source-manifest.json` and
  `generator-manifest.json`.
- Both manifests bind them to immutable generator image
  `sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`.
- The producer bundle contains exactly `klean_export.py`, `klean.py`, and
  `source-manifest.json`. Its trusted tree hash is
  `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`,
  exactly the value in `/audit-input.json`.
- The producer-bundle path recorded by the launcher ends in the same immutable
  image digest.

Raw hashes and manifests are in
[`evidence/01_producer_and_manifest_provenance.txt`](evidence/01_producer_and_manifest_provenance.txt);
the trusted tree-hash recomputation is in
[`evidence/10_producer_tree_hash.txt`](evidence/10_producer_tree_hash.txt).
The consolidated independent check is
[`evidence/16_independent_integrity_check.log`](evidence/16_independent_integrity_check.log).
There is no producer-provenance `AUDIT_ERROR`.

## Inventory reconstruction and bijection

I invoked the trusted `tools.k_rule_inventory.inventory_verification` directly
with `PYTHONPATH=/reference`. It selected main module `VERIFICATION`, computed
the local module closure in source order as `VERIFICATION-BASE`,
`VERIFICATION`, and reconstructed 13 rules.

The reconstructed facts are:

- `verification.k` SHA-256:
  `6d0fd1cf687133f27b74b49c8812b8c5ec4c3d7bb16c011c0de00a41f335e16d`
- canonical inventory SHA-256:
  `5e9c7b1c2b4daaa9312cf8a80808008c934a4e555de06984522d3c157876a61d`
- 13 unique `source_rule_id` values, each exactly
  `rule-<normalized_sha256>`

The protected discovery manifest has exactly the same 13 identities in the
same order and the same inventory hash. There are no omitted, duplicated,
extra, reordered, or hash-changed rules. Exact reconstructed text, spans,
attributes, normalized hashes, and IDs are saved in
[`evidence/02_reconstructed_inventory.json`](evidence/02_reconstructed_inventory.json).
The comparison also checked all 790 Stage 1 per-file hashes and every
launcher-recorded tree hash; see
[`evidence/16_independent_integrity_check.log`](evidence/16_independent_integrity_check.log).

## Independent classification

Every entry was reclassified from its rule body rather than from its rationale
or prior verdict:

| Frozen span | `source_rule_id` | Independent classification |
|---|---|---|
| `verification.k:10-11` | `rule-4538d6857ba52cff8cae6b2e278d286d492b01573dd8d706da0da3935257ae55` | `DEFINITION` |
| `verification.k:12-13` | `rule-21882032133cb4faaa1b53cf472247ffaca30b4ae987d2593f882090d4f99481` | `DEFINITION` |
| `verification.k:14-19` | `rule-4aebdd6812ac9010d20f560b9d10799a11b7f633715366d5677cb05718f36635` | `DEFINITION` |
| `verification.k:20-25` | `rule-8252ab65315e868d5ecd0744ff49153573a6f162ecfdb9cc009289116b48f8a0` | `DEFINITION` |
| `verification.k:29-30` | `rule-c5b80d5cddaf8560e0c97ce4ee0569156df290323257b2e7a88f6aed2b045736` | `DEFINITION` |
| `verification.k:31-33` | `rule-9bfddc4002c6cf1d546624d22bf4e4d0545cd6ce2634192b6b863fed85e46cc3` | `DEFINITION` |
| `verification.k:38-39` | `rule-c2c382043eb8357e342d0d7f63c3918c98085483bf65f80ec57f2705b82b8e1d` | `DEFINITION` |
| `verification.k:40-41` | `rule-cdf8b296f852901897f478149d8cc0e2369f5565f852d2245f671e3c988e15fc` | `DEFINITION` |
| `verification.k:42-46` | `rule-80cc1ed716ed43cab86c9e9426481924274d8925a9f8feb6463f566ed47baba0` | `DEFINITION` |
| `verification.k:49-50` | `rule-4519e840f3abb9bc879fb9110ce9c189fdc58ee2a775aa03d25ed7ed89f9d224` | `DEFINITION` |
| `verification.k:51-52` | `rule-7904cb1a8bab042d3971f29ecc9168123382fe576dc0a2a5c47b80c78d036171` | `DEFINITION` |
| `verification.k:53-57` | `rule-5cceb78b618b0ccae42a64fb078067b800b9cc947d58a6f82b1cdab2b9aeff39` | `DEFINITION` |
| `verification.k:66-94` | `rule-26fc544a3a34446e7dde0573f648e03f5ed33bc32ff9f6826cbd2730d9208ef4` | `PROVED_DERIVED_LEMMA` |

The first four rules are the complete base/recursive definition of `xorAcc`.
The two base cases implement `zip` truncation. The recursive cases are
disjoint and exhaustive on integer-head equality, append character code 48
for equality or 49 for inequality, and descend on both tails. Their only
overlap, when both tails are empty, has the same right-hand side.

The next two rules structurally define `bitString`: empty is true and a cons is
valid exactly when its head is code 48 or 49 and its tail is valid. This names
the input-domain predicate used by the precondition; it does not assert an
independent property.

The three `lastX` and three `lastY` rules are named proof-term definitions for
the loop targets. Their base cases preserve the initial target when either
zipped side is empty, and their recursive cases update to the currently
yielded one-character string while descending on both tails. Overlapping empty
cases agree. Thus all 12 `[simplification]` rules are truthful structural
definitions with decreasing recurrences. None is a disguised domain theorem.

The operational semantics confirms that:

- `zip` on strings produces `zipObjS`;
- `#iterNext(zipObjS(...))` yields paired one-character strings and stops as
  soon as either side is empty;
- `For` lowers to `#loop`;
- string comparison uses equality of the code sequences; and
- string `+=` uses `seqConcat`.

The relevant frozen semantics excerpts are in
[`evidence/15_relevant_operational_semantics.txt`](evidence/15_relevant_operational_semantics.txt).
They align exactly with the source program and the four summaries above.

### Derived-loop rule check

The final rule is an operational acceleration, so it qualifies as
`PROVED_DERIVED_LEMMA` only because the stricter derivation condition holds:

1. Its normalized semantic body—from `<k>` through `</scopes>`, including the
   arbitrary continuation, environment, bindings, frames, and state
   updates—is identical to `LOOP-SPEC.loop-invariant`. Both independently
   hash to
   `e98bda1def784f804a345f92d8ab801509643697179ee91f8e1755f26d9b56e2`.
   Only the K sentence marker and the rule's scheduling attribute differ.
2. A fresh `VERIFICATION-BASE` build contains the 12 definitions but not this
   rule. Its `allRules.txt` has 838 lines; the fresh full `VERIFICATION` build
   has exactly one additional rule and 839 lines.
3. The loop claim proved as `#Top`, exit 0, against the fresh bridge-free base
   definition.
4. Only afterward, the entry claim proved as `#Top`, exit 0, against the full
   definition containing the derived rule.
5. An independently authored counterfactual with the equal/unequal branches
   swapped failed against the base definition with a stuck residual showing
   the conflicting `xorAcc` results.
6. Adversarial concrete runs passed under both base and full definitions for
   empty sides, equal and unequal heads, unequal lengths in both directions,
   all-equal inputs, characters outside the stated bit-string precondition,
   and an observable post-loop continuation. This is finite sensitivity
   evidence in addition to—not a replacement for—the universal base proof.

The exact identity comparison is
[`evidence/17_loop_rule_claim_identity.log`](evidence/17_loop_rule_claim_identity.log).
Fresh compile and proof outputs are
[`evidence/05_fresh_kompile_base.log`](evidence/05_fresh_kompile_base.log),
[`evidence/06_fresh_kompile_full.log`](evidence/06_fresh_kompile_full.log),
[`evidence/07_fresh_kprove_loop_base.log`](evidence/07_fresh_kprove_loop_base.log),
and
[`evidence/08_fresh_kprove_entry_full.log`](evidence/08_fresh_kprove_entry_full.log).
The rejected mutation is
[`evidence/18_loop_branch_mutation.log`](evidence/18_loop_branch_mutation.log);
the base/full continuation comparison is
[`evidence/21b_adversarial_continuation_base_vs_full.log`](evidence/21b_adversarial_continuation_base_vs_full.log).

The resulting independent class counts are:

- `DEFINITION`: 12
- `PROVED_DERIVED_LEMMA`: 1
- `OPERATIONAL_RULE`: 0
- `DOMAIN_LEMMA`: 0

All entries are relevant to the source loop, its input precondition, its
result summary, or the exact final loop state. There is no irrelevant claimed
domain theorem.

## Stage 4 structural integrity and mathematical judgment

The independently established true domain set is empty. The Stage 4 artifacts
correctly encode that fact:

- `input-manifest.json` partitions all 13 inventory rules exactly into the 12
  definitions and one proved-derived lemma.
- Its `source_rules` list is empty.
- `obligation-map.json` has empty `source_rules`, `obligations`, and
  `trust_parameters` lists.
- The obligation-map hash is
  `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`.
- The generator, export result, recorded preflight, rerun preflight, and
  launcher all report obligation count 0 and `KLEAN_NO_OBLIGATIONS`.
- The generator manifest, preflight, launcher, and independent generated-source
  parser all report target `null`.
- `Klean11StringXor.lean` contains only imports. There is no generated target
  declaration or target proposition to weaken, duplicate, or make vacuous.
- `/candidate` is absent, as required for this status and mode.

Thus the exact source-rule/obligation bijection is the empty bijection, and it
is mathematically justified rather than merely self-consistent. The generated
target identity is consistently null.

The generated tree hashes to
`79ecabcafc4df9c5c5dabeb055065aef33940911d39fdad6bbb388adea1b70c4`,
matching the generator manifest, export result, preflight, and audit input.
The whole selected Stage 4 tree hashes to
`b9a64fa61fb285185866641ca61b2ca85723d11289cda1c920d0f92d32947218`.
All toolchain fields match `/reference/klean-toolchain.lock.json`.

The generated support library contains 45 allowlisted executable
axiom/opaque declarations, but no proposition target and no proposition-trust
escape. The trusted preflight independently matched those declarations to
`trust-inventory.json`, rejected proof holes and proposition trust, and
successfully clean-built a fresh copy.

The required call to `tools.klean_preflight.check_generation` initially
reached `lake clean` but exposed a sandbox-specific Lean launcher issue:
Lean resolves its executable using `/proc/<pid>/exe`, while this audit
sandbox's PID namespace is not reflected in its mounted `/proc`. A narrow
audit-local preload shim redirected only that lookup to `/proc/self/exe`.
With the pinned Lean 4.22.0 toolchain then visible, the same trusted preflight
returned `KLEAN_NO_OBLIGATIONS`, performed `lake clean` and `lake build` with
exit code 0, and rechecked that every immutable input snapshot was unchanged.
The initial diagnostic and shim test are in
[`evidence/11_rerun_check_generation.log`](evidence/11_rerun_check_generation.log),
[`evidence/12_lean_environment_diagnostic.txt`](evidence/12_lean_environment_diagnostic.txt),
and
[`evidence/13_lean_proc_shim_test.log`](evidence/13_lean_proc_shim_test.log).
The successful returned evidence is
[`evidence/14_rerun_check_generation_with_proc_fix.log`](evidence/14_rerun_check_generation_with_proc_fix.log).

An independent scan of generated declarations and the exact empty obligation
map is in
[`evidence/22_generated_target_absence_scan.txt`](evidence/22_generated_target_absence_scan.txt).

## Final judgment

The Stage 3 inventory and classification are complete and mathematically
correct. No simplification rule is mislabeled, no domain theorem is hidden as
a definition or operational rule, and the sole proved-derived rule was first
proved against a bridge-free module with an exact statement before its later
use. Since the independently reconstructed domain-lemma set is genuinely
empty, deterministic Stage 4 correctly generated no obligations and no
target. The launcher correctly omitted Stage 5.

VERDICT: PASS
LEGITIMACY: LEGIT
