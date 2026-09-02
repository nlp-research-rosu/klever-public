# Independent audit: `109-move-one-ball`

Audit mode: `CLASSIFICATION_ONLY`  
Condition: `bare`  
Semantics mode: `GENERATED_SEMANTICS`

The Stage 3 classification is correct, and the selected Stage 4
`KLEAN_NO_OBLIGATIONS` status is legitimate. The independently reconstructed
domain-lemma set is genuinely empty. Stage 4 maps that empty set to zero
obligations and no generated target; it does not replace the empty conjunction
with a vacuous theorem. Stage 5 is correctly absent in this audit mode.

I treated the mounted Stage 1–4 artifacts, prior audit, manifests, comments, and
rationales as untrusted evidence. I did not use the prior Stage 2 conclusion or
the Stage 3 rationales as authority and did not execute any mounted provenance
script. Mechanical reconstruction and preflight used only the mounted trusted
tools under `/reference/tools`.

## Producer-source identity gate

This gate passed before Stage 4 was judged.

| Producer input | Recomputed SHA-256 | Recorded SHA-256 | Result |
|---|---|---|---|
| `generation-tools/klean_export.py` | `235473b1324d2b203cb2a49ab94e36fb7c300084d506a57fca2228381f1bdec0` | same in `source-manifest.json` and `generator-manifest.json` | match |
| `generation-tools/klean.py` | `ddec66db87398459ff0c2b5aad7121fe1029b58b8d576db4203c68bf5b647d13` | same in `source-manifest.json` and `generator-manifest.json` | match |

The immutable generator image ID is
`sha256:e18301a8220fb0b62fabf56feffcb5e621049daa7c7a0b79eacb60cae5e57fda`.
It agrees among `source-manifest.json`,
`generator-manifest.json.provenance.generator_image_id`, and the basename of
the launcher-recorded `generation_producer_sources` path. The mounted producer
bundle's recomputed tree hash is
`363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0`,
also exactly matching `/audit-input.json`.

Raw evidence: `evidence/01_producer_identity.txt`,
`evidence/07_all_recorded_input_hashes.txt`, and
`evidence/22_stage4_independent_bindings.txt`.

## Inventory reconstruction and bijection

I invoked:

```text
PYTHONPATH=/reference python3
from tools.k_rule_inventory import inventory_verification
inventory_verification(Path("/reference/k-proof"))
```

The trusted inventory code selected the local closure of
`HUMAN-EVAL-VERIFICATION` in `verification.k`. That closure contains 11 rules.
The recomputed `verification.k` hash is
`50955228c086e49262966326b584eb35c8809ff90426865addff6d39090a58a6`.
The canonical whole-inventory hash is
`fc6b11367b9788862c8e36c18f6299b90f40ef0a9372a8250f3e806ab15b07c3`.

For each entry, the normalized source hash was recomputed from the frozen
source text and its `source_rule_id` was independently checked to be
`rule-<normalized SHA-256>`. The protected Stage 3 JSON has exactly 11 unique
identities, in the reconstructed order. There are no omitted, extra,
duplicated, or reordered identities. Every source span and normalized hash
matches. The protected whole-inventory hash and the Stage 4 input-manifest
inventory hash both match the reconstruction.

Raw inventory and comparison evidence:
`evidence/04_reconstructed_rule_inventory.json.txt`,
`evidence/08_inventory_bijection_and_hashes.txt`, and
`evidence/24_trusted_stage3_contract_validation.txt`.

## Independent classification judgment

The following table reclassifies every reconstructed entry. The hash column is
the full normalized source hash; the exact `source_rule_id` is `rule-` followed
by that hash.

| Lines | Normalized SHA-256 | Frozen equation | Independent class |
|---:|---|---|---|
| 16 | `469d3f727fbbd991b638f2792c972ba21976e292536f53369213fb11cf57aa0c` | `length(.IList) => 0` | `DEFINITION` |
| 17 | `49c7bfa9a893c096eca27b22e8f8013e0bb4f61c91cd0cb2c127e6b652f997a0` | `length(_I :: IS) => 1 +Int length(IS)` | `DEFINITION` |
| 19 | `eb18ebfe1bef3a8e5845419e0db6436dbf613d43ba1626d3d657cc6167887346` | `last(I :: .IList) => I` | `DEFINITION` |
| 20 | `0182de46a89cb752ba4c1ba38e8cbed4fb65e27054fcc1ec278a81c594a63133` | `last(_I :: J :: IS) => last(J :: IS)` | `DEFINITION` |
| 22 | `f2441b27d9ca0e8cf4815f11ae1e52bfcbb547564db965dfdc67419ef193ec9d` | `dropBit(I, J) => 1 requires I >Int J` | `DEFINITION` |
| 23 | `c33dc687b614870b61be730222227af70e4a20ed12ca4cfabdcd07a8a7e26c54` | `dropBit(I, J) => 0 requires I <=Int J` | `DEFINITION` |
| 25 | `5d2150480d24dc6cc10f89c3e79f0b609b0e5f8efe67b353a82a6c46e973bb3c` | `dropsFrom(_PREVIOUS, .IList) => 0` | `DEFINITION` |
| 26–27 | `07b829b14b1b024287a1eada911a5774f61b32b5b77fcecffb7f6e3f5401e973` | recursive `dropsFrom` fold | `DEFINITION` |
| 29 | `e6dd199630a5b507f5420c0ab6fbb876b682cfcc6e594ddc96c6804638c60eae` | `cyclicDrops(.IList) => 0` | `DEFINITION` |
| 30 | `1c850036dae607a5779c09c5ef77e650377125f3b6acbc86e076ce9d5dda1b57` | `cyclicDrops(I :: IS) => dropsFrom(last(I :: IS), I :: IS)` | `DEFINITION` |
| 34 | `d9a4f79540b673928e811904ac141039899c7dd8c054edc90ec741fb2719e749` | `rotationSortable(L) => cyclicDrops(L) <=Int 1` | `DEFINITION` |

The first ten entries are base or structurally decreasing recursive equations
for newly declared summaries. The two `dropBit` guards are disjoint and
exhaustive over K mathematical integers. `last` is intentionally partial and
is used only on nonempty lists. The final entry defines the newly declared
named proof predicate `rotationSortable`; it does not assert a theorem in
pre-existing vocabulary.

None is an `OPERATIONAL_RULE`: no entry matches a K cell or advances an
execution configuration. The execution rules are in `semantic.k`, outside this
local inventory closure. None is a `PROVED_DERIVED_LEMMA`: `verification.k`
contains no claim and no prior proof of the exact rule in a module omitting it.
None is a `DOMAIN_LEMMA`: every left-hand side introduces one of the six named
helper symbols. The explanatory comment about sorted rotations is not a rule.
No inventory entry has a `simplification` attribute.

The classification is also operationally relevant. For a nonempty list
`[x₁, …, xₙ]`, the recurrences define

```text
cyclicDrops = [xₙ > x₁] + Σᵢ₌₁ⁿ⁻¹ [xᵢ > xᵢ₊₁].
```

That is exactly the frozen source loop: `previous` starts at the last element,
each iteration increments on `previous > value`, then updates `previous`. The
frozen K semantics connects `arr[-1]` to `last`, its exact loop summary to
`dropsFrom`, and the postcondition to `cyclicDrops` and
`rotationSortable`.

For the prompt's distinct-integer domain, a sorted rotation exists exactly
when there is at most one circular strict descent. Necessity follows because a
linear rotation removes only its circular boundary edge. Sufficiency follows
by rotating to begin immediately after the sole descent. Empty and singleton
cases agree separately. Thus the helper definitions are relevant to both the
program and the postcondition; no irrelevant domain fact is hidden among them.

As finite supporting evidence, an independently written enumerator that did
not import or execute the mounted solution found:

- zero recurrence/source-loop mismatches over all 874 permutations through
  length six;
- zero source-result/sorted-rotation mismatches over those 874 lists;
- zero recurrence/source-loop mismatches over 364 repeated-value lists; and
- immediate counterexamples to mutations that omit the wraparound comparison
  or reverse the comparison.

The universal classification judgment rests on the equations and semantics,
not on this finite test. Full reasoning and output are in
`evidence/12_independent_classification.md` and
`evidence/11_independent_semantic_crosscheck.txt`.

## Recorded hash reconciliation

All content hashes recorded for the selected inputs and Stage 4 generation
recompute exactly:

| Binding | Recomputed value |
|---|---|
| canonical launcher `resolution` | `59c903868ffce604f6aa9b2aa3de49141797bf3070046246fb2b29846e429350` |
| Stage 1 pipeline workspace tree | `d23e4cefc3d249c949d905af4c0eac2b3c7bfbf064a138ae7b6c750cd844e11f` |
| frozen Stage 1 export tree | `8e0ba078f90bded861732a23cbb5bc03214629fac95b8b730d499fb99b7cf1cd` |
| selected Stage 2 audit tree | `d36f7ca2d66f852434a767ec13ace406ae0564ea17c914059ee999669a57c287` |
| protected Stage 3 JSON | `37ef6e230a4f0e409aa7a4ceef14574762ffcefa50069c6b2fe3129eb44a654d` |
| producer-source bundle tree | `363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0` |
| generated Lean tree | `1dc37fdd5a39ed3923094869809cb20f25d67277aa7a603d4bfa6c8ca09ba916` |
| complete selected Stage 4 tree | `5a914d722cbef6837edc2dfde257fc9775e48cbc2d41680404a9a72f06518100` |
| obligation map | `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048` |
| trust inventory | `721f01d3ef37e9e040b5fa2482e49354497b1d82d29839ef2fa11beebd632688` |

Every individual Stage 1 source-file hash also matches the launcher record.
The generator toolchain object is byte-for-byte equivalent as JSON to the
pinned `/reference/klean-toolchain.lock.json`. The recorded Stage 4 preflight
document is exactly equal to the launcher copy.

Evidence: `evidence/07_all_recorded_input_hashes.txt`,
`evidence/22_stage4_independent_bindings.txt`, and
`evidence/25_audit_input_internal_hash.txt`.

## Trusted Stage 4 preflight

The required call was made against:

```text
/reference/k-proof
/reference/lemma-discovery.json
/reference/klean-generation
```

The audit container initially caused `lake clean` to fail with “could not
detect the configuration of the Lake installation.” This was not an input or
producer mismatch. Lean 4.22 calls `readlink("/proc/<pid>/exe")`, while this
container exposes `/proc/self/exe` but hides numeric PID paths. A 44-line
`LD_PRELOAD` shim under `/tmp/audit-work` redirected only numeric
`/proc/<pid>/exe` requests to `/proc/self/exe`. Its source and binary hashes,
diagnosis, and sanity checks are recorded in
`evidence/14_lake_environment_diagnosis.txt` through
`evidence/20_check_generation_rerun_with_proc_shim.txt`. The shim changed no
audit input, manifest, generated source, checker logic, or compiler output.

With that environment repair, the unchanged trusted invocation

```text
LD_PRELOAD=/tmp/audit-work/proc_exe_readlink_shim.so \
PYTHONPATH=/reference \
tools.klean_preflight.check_generation(...)
```

returned:

```text
status: KLEAN_NO_OBLIGATIONS
obligation_count: 0
target: null
designated_sorry_count: 0
trust_declaration_count: 41
lake clean exit: 0
lake build exit: 0
lake clean output SHA-256:
  e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
lake build output SHA-256:
  04090817846b6d7e4aeba6b02dfd4b5b270c946b2c31c31b05a154e186cb7db2
```

These values exactly reproduce the generation-time preflight recorded in both
`preflight.json` and `/audit-input.json`. The complete returned document is
`evidence/20_check_generation_rerun_with_proc_shim.txt`.

## Obligation bijection and target identity

The independent classification yields:

```text
true DOMAIN_LEMMA set = []
```

The Stage 4 input manifest, generated `obligation-map.json`, generator
manifest, export result, and launcher record yield:

```text
input source_rules       = []
map source_rules         = []
map obligations          = []
map trust_parameters     = []
generator obligation_count = 0
export obligation_count    = 0
```

This is an exact source-rule/obligation bijection. There can be no omission,
duplicate, reordering, irrelevant conjunct, or weakened conjunct within the
empty map. Crucially, the generator did not turn the empty map into a theorem
of `True`: `expected_target_definition(obligation-map)` returns `None`,
`target_statement(generated)` returns `None`, the generator manifest and audit
input both record `target: null`, and `Lemmas.lean` contains only an empty
namespace. Therefore the fixed generated target is correctly absent rather
than changed or vacuous.

The generated support library contains 41 allowlisted executable hook axioms,
all reconciled by the trusted preflight with `trust-inventory.json`; it contains
no proposition axiom or proof hole. Because there is no target proposition or
Stage 5 proof, those support declarations cannot be used to discharge a
purported theorem here.

Raw evidence: `evidence/21_generated_tree_and_obligation_map.txt`,
`evidence/22_stage4_independent_bindings.txt`, and
`evidence/23_generated_target_absence.txt`.

## Stage 5 applicability

`AUDIT_MODE`, `/audit-input.json.resolution.mode`, and the absence of Stage 5
bindings all say `CLASSIFICATION_ONLY`. The audit input records
`stage5_result: null`, `target: null`, and null Lean workspace/invocation
hashes. `/candidate` is absent. This is exactly required for a genuine
`KLEAN_NO_OBLIGATIONS` result, so no candidate copy, `Proof.final`, axiom print,
or operational-bridge parameter audit applies.

VERDICT: PASS
LEGITIMACY: LEGIT
