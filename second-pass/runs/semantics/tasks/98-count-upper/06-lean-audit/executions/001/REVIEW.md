# Independent Stage 3–5 audit: HumanEval `98-count-upper`

## Outcome and scope

The launcher-bound mode is `CLASSIFICATION_ONLY`, for condition `semantics`
and semantics mode `SUPPLIED_SEMANTICS`. There is no mounted `/candidate`,
and the signed audit input records no Stage 5 workspace or invocation. I
therefore audited the protected Stage 3 classification and deterministic
Stage 4 `KLEAN_NO_OBLIGATIONS` result. The Stage 5 proof-specific checks are
not applicable.

I did not rely on the selected Stage 2 verdict, prior reviews, comments, or
logs as authority. They were treated only as hashed provenance. The
classification below was reconstructed from frozen `verification.k`, the
source solution and postcondition, and the supplied operational semantics.

## Audit-input and immutable-input binding

The audit-input envelope verifies with resolved-input SHA-256
`7dfb913a68950bdc92dfcfe72dee5443491cf9eb34d2ac547b7dc25f73af6c14`.
`AUDIT_MODE` and the signed resolution both say `CLASSIFICATION_ONLY`.

The independent hash checker performed 70 comparisons with zero failures.
In particular:

- Stage 1 workspace tree:
  `cd7c02ec1081ac6ac0464582e35aebd7c46a3cf5c5f9e1cdcbcdfc70adbcbce6`;
- Stage 1 deterministic-export tree:
  `cb5bae5dbd8d4db7194f8319795807b563f3270099e34c388497f756680802c9`;
- discovery manifest:
  `4602e3665d16573eb0aa54aa387f50e9777629395197f3181a964962e2bfff8b`;
- selected Stage 2 tree:
  `8d3c11a95601ef3c2668af3ade8fd772ffca365add77d0593a826d27850b3b30`;
- selected Stage 4 tree:
  `38ce21d37941f2fa68197809ac76eefc1e38ae020db0b83219929726d3e14e71`;
- generated project tree:
  `b4416efb8217d0b02641074b1418bb9bda9b16755aec249794330ed258330196`;
  and
- producer-source bundle tree:
  `55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c`.

All 765 regular-file names and SHA-256 values in
`stage1_source_hashes` were also recomputed; there were no missing, extra, or
mismatched entries. The complete observed map is preserved as
`evidence/actual-stage1-source-hashes.json`.

## Producer-source provenance gate

This gate passed before accepting any Stage 4 result.

| Producer | Observed SHA-256 | Recorded SHA-256 |
|---|---|---|
| `klean_export.py` | `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0` | same in source and generator manifests |
| `klean.py` | `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1` | same in source and generator manifests |

The producer bundle contains exactly those two files plus
`source-manifest.json`. The generator manifest and source manifest both bind
the immutable image
`sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000`;
the image-key component of the producer-source path recorded in
`/audit-input.json` is the same digest. The generator toolchain object also
equals `/reference/klean-toolchain.lock.json`.

No producer source was executed. The trusted `/reference/tools` inventory,
preflight, and mechanical-gate implementations were used for reconstruction
and checking.

## Inventory reconstruction and bijection

The trusted rule-inventory code selected
`COUNT-UPPER-VERIFICATION`, matching the last `kompile verification.k
--main-module` in `prove.sh`. Its local verification-module closure contains
only that module; `MPY` is supplied semantics rather than another local module
in `verification.k`.

The frozen `verification.k` SHA-256 is
`7187ac44023122049185672e4116e0fe8ee5242762f3468ba7db6e2d2a009657`.
Canonical reconstruction produced exactly two rules and whole-inventory hash
`384e5e1caf7ce9b5b798eca057b4ee29341aa7151afac3dc975f5aa42599ac23`.

| Source span | Normalized SHA-256 / `source_rule_id` | Attributes | Independent class |
|---|---|---|---|
| line 10 | `10b63a2e2225cd457dcf51887aec2f5c265ce7e5117c82e30a96da4d69dce4ab` / `rule-10b63a2e2225cd457dcf51887aec2f5c265ce7e5117c82e30a96da4d69dce4ab` | none | `DEFINITION` |
| lines 11–16 | `dbe614f8b007441a5b97fefaac5825ae89bddf38faf17cc47420c3c905ada5d1` / `rule-dbe614f8b007441a5b97fefaac5825ae89bddf38faf17cc47420c3c905ada5d1` | none | `DEFINITION` |

For each rule I separately normalized the reconstructed source text, hashed
it, and rebuilt `source_rule_id`. The discovery manifest has exactly the same
two unique identities in the same order and the same inventory hash. Thus
there is no omission, duplicate, extra rule, reordered identity, changed
hash, or unclassified rule. The Stage 4 input manifest also reproduces both
complete source records, spans, hashes, classifications, and rationales in
that order.

## Independent classification judgment

Both labels are correct:

1. The line-10 rule is the empty-`IntSeq` base equation for the fresh,
   named total summary `countUpperFrom(IntSeq, Bool)`.
2. The lines-11–16 rule is its constructor-decreasing recurrence. It adds
   one exactly when the current one-character string is an uppercase vowel
   and the incoming parity flag is true, then recurses on the strict tail
   with the parity flag negated.

These are definitions, not ordinary execution rules: their left-hand sides
are applications of the new mathematical summary symbol and contain no
operational configuration or `<k>` rewrite. They are not
`PROVED_DERIVED_LEMMA` claims, and Stage 3 makes no proof-first/later-use claim
for them. They are not facts over a pre-existing domain operation, so
classifying them as `DOMAIN_LEMMA` would be wrong.

The recurrence also matches the supplied operational meaning:

- `IntSeq` string iteration yields a one-character `str(iCons(C,.IntSeq))`
  and the remaining string;
- string `in` is `strContains`, so a one-character code is counted exactly
  when it occurs in the literal code sequence for `"AEIOU"`;
- the program initializes `even` to `true`, uses value-returning Boolean
  `and`, and `applyBin("+", Int, Bool)` adds one for `true` and zero for
  `false`; and
- the body negates `even` after each character, exactly as the recurrence
  passes `notBool EVEN` to the strict tail.

The summary is directly relevant to both the loop invariant and the
end-to-end postcondition `countUpperFrom(S, true)`. It is neither a convenient
constant nor disconnected mathematics. A supporting differential check
compared separately implemented recursive-summary and operational-scan
calculations on 3,122 cases, including empty, parity-boundary, lowercase, and
non-ASCII witnesses, with zero mismatches. Constant-zero, all-index,
pre-toggle, and lowercase-inclusive counterfactuals each produced many
mismatches. This finite check supports, but does not replace, the source-level
semantic judgment.

Neither inventory rule has a `simplification` attribute, so the
simplification-class restriction has no additional case to discharge.

The independently classified true `DOMAIN_LEMMA` set is therefore genuinely
empty.

## Deterministic Stage 4 judgment

The Stage 4 source-rule/obligation mapping is the exact empty bijection:

- independently classified domain rules: `[]`;
- input-manifest `source_rules`: `[]`;
- obligation-map `source_rules`: `[]`;
- obligation-map `obligations`: `[]`; and
- obligation-map `trust_parameters`: `[]`.

All three recorded obligation counts are zero. The obligation-map file hash is
`cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`.
There is no weakened, duplicated, irrelevant, or vacuous conjunct: no
conjunct was generated at all.

The fixed generated target is exactly absent. The generator manifest,
preflight, audit input, and trusted target parser all report `null`; the
generated top-level module contains imports only. This is the required target
identity for a genuinely empty domain set, not a theorem set to `True`.
There is also no Stage 5 candidate.

I reran `tools.klean_preflight.check_generation` with
`PYTHONPATH=/reference` against the mandated three inputs. It returned:

- status `KLEAN_NO_OBLIGATIONS`;
- obligation count `0`;
- target `null`;
- designated-sorry count `0`;
- trust declaration count `53`;
- `lake clean` exit `0`; and
- `lake build` exit `0`.

The clean/build output hashes and tails exactly reproduce the stored preflight
record. The independent trusted mechanical final gate also returned `PASS` in
`CLASSIFICATION_ONLY` mode with no candidate, no target, and no used axioms.
These mechanical results establish structural integrity; the empty-domain
conclusion above is my independent mathematical classification.

### Sandbox compatibility note

An initial Lake attempt exposed an audit-container restriction: Lean 4.22
queries `/proc/<current numeric pid>/exe`, while the sandbox permits the
equivalent `/proc/self/exe` path. The raw failure is preserved. I compiled a
small recorded `LD_PRELOAD` shim that rewrites only that one self-executable
`readlink` request and delegates every other request unchanged. With it, the
pinned Lean binary reported version 4.22.0 and commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, and the unchanged trusted
preflight completed successfully. The shim did not alter any mounted input,
Lean source, generated project, theorem, or hash.

## Stage 5

Not applicable. The signed mode is `CLASSIFICATION_ONLY`, the legitimate
domain-obligation set is empty, the fixed target is absent, and `/candidate`
is absent. Consequently there is no `Proof.final`, candidate clean build,
axiom printout, target shadowing question, or target-parameter operational
bridge to audit.

## Evidence

- `evidence/01_frozen_sources_and_trusted_inventory_code.log`: frozen source,
  spec, solution, and trusted inventory implementation.
- `evidence/reconstructed-inventory.json` and
  `evidence/02_reconstruct_inventory.log`: independent canonical inventory.
- `evidence/04_semantics_search_and_proof_driver.log` and
  `evidence/05_relevant_operational_semantics.log`: relevant supplied
  operational semantics.
- `evidence/06_stage4_manifests_and_generated_target.log`: producer hashes,
  Stage 4 manifests, obligation map, and generated top module.
- `evidence/recorded-hash-and-bijection-check.json` and
  `evidence/07_verify_recorded_hashes_and_bijections.log`: the 70 independent
  hash, inventory, classification-record, mapping, and target checks.
- `evidence/rerun-preflight-result.json` and
  `evidence/08_rerun_klean_preflight.log`: mandated trusted preflight rerun.
- `evidence/09_lake_environment_diagnostic.log`,
  `evidence/11_build_and_test_proc_shim.log`, and
  `evidence/proc_self_readlink_shim.c`: sandbox diagnosis and narrowly scoped
  compatibility evidence.
- `evidence/mechanical-final-gate-result.json` and
  `evidence/12_run_mechanical_final_gate.log`: independent trusted mechanical
  final gate.
- `evidence/13_semantic_reclassification_checks.log`: adversarial examples and
  counterfactual supporting tests.
- `evidence/COMMANDS.md`: exact principal invocations and command-source
  locations.

VERDICT: PASS
LEGITIMACY: LEGIT
