# Independent audit: HumanEval 133-sum-squares

## Scope and result

The launcher-selected mode is `CLASSIFICATION_ONLY`; `AUDIT_MODE` and
`/audit-input.json` agree. The condition is `semantics` and the semantics mode
is `SUPPLIED_SEMANTICS`. There is no `/candidate`, so Stage 5 proof,
`#print axioms Proof.final`, and operational-bridge checks on candidate
parameter definitions are not applicable.

I treated the mounted Stage 1–4 artifacts, previous audit, logs, comments, and
classifications only as evidence. The classification below was reconstructed
from the frozen `verification.k`, source program, specification, and supplied
operational K semantics.

## Input and producer integrity

The trusted audit-input verifier recomputed
`resolved_input_sha256 =
2dc7e748da768a93f51df401abefcbbd23cd98b728552ef712b30d23dc141cbc`,
exactly matching `/audit-input.json`.

The recorded hashes all match when checked with their specified algorithms:

- Stage 1 workspace tree:
  `b1f7402db503d103321a3cbaac950b06929705bebd296f406c884b9c36420113`.
- Frozen Stage 1 export tree:
  `94bfe8876fd61141d50f7b14fc0bfc5e0612642419c1810fd3769d436d67f46a`.
- Stage 2 audit tree:
  `5998762725e102b82d73d084136234ee45730cd3bea9b309f47a7a72c72883ff`.
- Stage 3 manifest:
  `bb689cf055a11352114dc28091f14318ec014b62716ee1d5a6a639b233e8808b`.
- Stage 4 generation tree:
  `1ce44af981a5791581e65e8045590c8f99121114f289240d82a90f5278a4501a`.
- Generated-project export tree:
  `0f3fe489af446947fb881085b881cd02499a1540264e2cc50d76b87ecd65bba9`.
- Generation producer-source tree:
  `55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c`.

Every individual file in `stage1_source_hashes` also matches. The pipeline tree
hash and frozen-export tree hash intentionally use different canonical tree
algorithms; each was compared only with its corresponding recorded field.

Before judging Stage 4, I hashed both generation-time producer files:

| Producer | Recomputed SHA-256 |
|---|---|
| `klean_export.py` | `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0` |
| `klean.py` | `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1` |

Both values match `source-manifest.json` and `generator-manifest.json`.
The immutable image ID is also identical in the source manifest, generator
manifest, and the image-key component of the audit-input producer path:
`sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000`.
Thus no producer-source infrastructure error exists.

## Rule-inventory reconstruction

Using the trusted `tools.k_rule_inventory.inventory_verification` code, the
selected verification module is `SUM-SQUARES-VERIFICATION` and its local
verification-file closure, in source order, is:

1. `SUM-SQUARES-VERIFICATION-BASE`
2. `SUM-SQUARES-VERIFICATION`

The reconstructed inventory contains exactly five rules:

| Span | `source_rule_id` | Attributes | Independent class |
|---|---|---|---|
| 8–8 | `rule-3bbcffda73c7a5fa1b737b480c0bf40e3d7107b0414e1a301e6b0584a37498f2` | none | `DEFINITION` |
| 9–10 | `rule-f7dae20f9e539e513987a8e9d9bd6bc0d0e6edcd9b9e3703e1020ff937ddeaa1` | none | `DEFINITION` |
| 15–15 | `rule-2bc2a66c772aae97380ca3ab3abdcf702833b825027b9f8fc0da1fe4878d02ac` | none | `DEFINITION` |
| 16–17 | `rule-d51eea8592ab9aaeac0075e7adf2716fa54493fd8ace05402072151930790876` | none | `DEFINITION` |
| 27–55 | `rule-1a11afc07a69ef715908d8b2c198565b0dbe50b4471cb0f1473036bc47d7bf15` | `priority(40)` | `PROVED_DERIVED_LEMMA` |

For every entry, the source span, normalized source hash, and
`source_rule_id` match the protected Stage 3 manifest. The reconstructed
whole-inventory hash is
`bd165355783fb2112441edb679eaeab096d8e63b6d11308d5b6753496a59ad5e`.
The manifest has the same five identities in the same order, with no omission,
extra identity, or duplicate. No inventory rule has the `simplification`
attribute.

## Independent classification judgment

The first two rules are the base and structurally descending recurrence for
`sumSquaresFrom`. They name the left-to-right accumulator summary:
the empty sequence returns the accumulator, while a nonempty sequence adds
`ceilF(V) ^Int 2` and recurses on the tail. They are definitions, not imported
mathematical facts.

The next two rules similarly define `lastFrom`. The empty sequence retains the
current loop-target value; a nonempty sequence replaces it with the head and
recurses. This helper records the loop's final `number` binding so that the
complete scope update can be stated. It is a named structural definition, not
a domain lemma.

The final rule is valid as a proved derived lemma:

- The prior claim `SUM-SQUARES-LOOP-SPEC.loop-correct` has exactly the same
  LHS, RHS, arbitrary `CONT:K`, scope transformation, and guard after replacing
  the claim label by the rule keyword. Both normalized theorem bodies hash to
  `864a0e98484f63b8cd866021b8395eb000b6cdab2f8c30b9521ffaa72c89d381`.
  The rule's `priority(40)` and the claim's label are sentence metadata, not a
  change to the proved reachability formula.
- The first compilation uses main module
  `SUM-SQUARES-VERIFICATION-BASE`. Its local closure contains only the four
  definition rules; the promoted loop rule is absent.
- Only after proving the loop claim does `prove.sh` compile
  `SUM-SQUARES-VERIFICATION`, which contains the promoted rule, for the later
  end-to-end function proof.
- A fresh isolated rerun of the exact Stage 1 `prove.sh` exited 0 and emitted
  `#Top` first for the BASE-only loop proof and then `#Top` for the downstream
  function proof.

This classification also agrees with the operational semantics, independently
of the earlier success record. `For` enters `#loop`; list iteration yields the
head and tail or `#iterDone`; `#bindTgt` updates `number`; the intercepted
`math.ceil` call produces `ceilF(V)`; integer exponentiation and addition
update `result`; and the loop recurs on the tail. The two recurrences capture
exactly those state changes. The claim is quantified over the same arbitrary
continuation as the promoted rule, so it does not prove only a narrower
trailing context. The loop body has no heap, output, exception, or abrupt
control effect that the summary omits.

Boundary and counterfactual checks are discriminating:

- Empty input leaves the accumulator and current target unchanged.
- From accumulator `0`, input `[2]` produces `4`; a constant, identity, or
  exponent-one accumulator summary would disagree.
- Input `[-2.4]` uses ceiling `-2` and produces `4`; truncation or floor would
  disagree.
- Starting from `CURRENT`, a nonempty target sequence `[a, b]` ends at `b`;
  retaining `CURRENT` would disagree with `#bindTgt`.

The independently classified domain-lemma set is therefore genuinely empty.
No domain fact relevant to the program or postcondition has been hidden in one
of the other categories.

## Deterministic Stage 4 judgment

With `PYTHONPATH=/reference`, I reran the trusted
`tools.klean_preflight.check_generation` on `/reference/k-proof`,
`/reference/lemma-discovery.json`, and `/reference/klean-generation`, using
the trusted toolchain lock. It returned:

- status `KLEAN_NO_OBLIGATIONS`;
- obligation count `0`;
- target `null`;
- designated sorry count `0`;
- trust-declaration count `50`;
- successful `lake clean` and `lake build`.

The build output hash is
`7fa64f8af7e23352adb1a985e69b9090d0eb4cbd22ee6e03f44e42434ee78da8`,
exactly reproducing the recorded preflight. The entire returned document is
data-identical to both the selected Stage 4 `preflight.json` content
and `resolution.stage4_preflight` in `/audit-input.json`.

The audit sandbox initially made Lean's `IO.appPath` fail because Lean asks for
`/proc/<getpid()>/exe`, while this nested PID namespace exposes only the host
PID in `/proc`. I recorded the initial failure and diagnosis. The successful
rerun used an audit-only `LD_PRELOAD` shim that changes only numeric
`/proc/.../exe` readlink requests to `/proc/self/exe`. It did not modify any
frozen or generated input, and the trusted preflight's before/after snapshots
remained unchanged.

The independent manifest comparison is exact:

- Stage 4's definitions equal the four independently reconstructed
  definitions.
- Its operational-rule list is empty.
- Its proved-derived-lemma list equals the single independently validated loop
  lemma.
- Its domain `source_rules` list is empty.
- `obligation-map.json` has empty `source_rules`, `obligations`, and
  `trust_parameters`.
- The expected target definition is absent, the observed target is absent,
  no target file or target/final declaration exists, and
  `generator-manifest.json` records `target: null`.

Consequently there can be no omitted, duplicated, irrelevant, weakened, or
vacuous obligation conjunct. `KLEAN_NO_OBLIGATIONS` is the correct deterministic
Stage 4 result.

The 50 generated trust declarations are the allowlisted executable Klean
support boundary, not proposition assumptions or a hidden target. The trusted
preflight reconciled the declarations with `trust-inventory.json`, rejected
proposition trust, and found no `sorry`, `admit`, or `unsafe`.

## Stage 5

Stage 5 is correctly absent: the mode is `CLASSIFICATION_ONLY`, the true domain
set is empty, Stage 4 generated no target, `/candidate` does not exist, and the
audit input has null Stage 5 fields. A Lean proof or `Proof.final` in this mode
would itself have been inconsistent with the no-obligations result.

## Evidence index

- Launcher and mounted-file inventory:
  `evidence/00_environment_and_files.txt`
- Producer and Stage 4 manifests:
  `evidence/01_producer_and_stage4_manifests.txt`
- Reconstructed inventory and protected-manifest comparison:
  `evidence/03_reconstructed_inventory_and_manifest.txt`
- Frozen source, spec, and proof order:
  `evidence/04_frozen_source_and_proof_structure.txt`
- Relevant operational-semantics excerpts:
  `evidence/06_operational_semantics_excerpts.txt`,
  `evidence/07_operational_semantics_binding_arithmetic.txt`,
  `evidence/07b_bind_target_semantics.txt`
- Correct hash bindings and individual source hashes:
  `evidence/10b_correct_hash_bindings.txt`,
  `evidence/10_all_recorded_hashes.txt`
- Fresh exact Stage 1 rerun:
  `evidence/12_stage1_exact_recheck.txt`
- Derived-lemma formula equality, BASE exclusion, and proof order:
  `evidence/13_derived_lemma_exactness_and_order.txt`
- Successful trusted Stage 4 preflight rerun:
  `evidence/14_check_generation_success.txt`
- Preflight identity and target/candidate absence:
  `evidence/15_preflight_identity_and_absence_checks.txt`
- Producer-source and image assertions:
  `evidence/16_producer_provenance_assertions.txt`
- Audit-input digest verification:
  `evidence/17_audit_input_contract_verification.txt`
- Exact classification and obligation bijection:
  `evidence/18_classification_and_obligation_bijection.txt`
- Lean sandbox diagnosis and narrowly scoped workaround:
  `evidence/09_check_generation_rerun.txt`,
  `evidence/09r_procself_shim_validation.txt`

VERDICT: PASS
LEGITIMACY: LEGIT
