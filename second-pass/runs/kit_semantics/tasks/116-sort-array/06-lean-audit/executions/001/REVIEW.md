# Independent Stage 3–5 audit: `116-sort-array`

## Result and scope

The launcher records `CLASSIFICATION_ONLY`, condition `kit-semantics`, and
semantics mode `SUPPLIED_SEMANTICS`. I therefore audited the Stage 3
classification and deterministic Stage 4 generation. Stage 5 proof checks are
not applicable: `/candidate` is absent, the generated target is absent, and the
selected Stage 4 status is `KLEAN_NO_OBLIGATIONS`.

I treated all mounted candidate/provenance prose and logs as untrusted evidence.
The conclusions below come from the frozen sources, the trusted rule-inventory
and preflight code, recomputed hashes, and fresh commands. The command index is
[evidence/COMMANDS.md](/audit-output/evidence/COMMANDS.md).

## Producer provenance and immutable inputs

Before judging generation, I hashed the exact mounted producer sources:

| Producer | Recomputed SHA-256 |
|---|---|
| `klean_export.py` | `0e653377b007bc1a742bbd8fa0dcfdf956ebb2ef2432a7137d032b0a70d59c1b` |
| `klean.py` | `0e6dba9d9f456574b3bf4f4bf06933d774e9125f4d12c5a90b7314d8dd5c33a4` |

Both hashes exactly match `source-manifest.json` and
`generator-manifest.json`. The generator image ID is consistently
`sha256:b377a4d6ce1a4210c17d7e862e3737d2c348cc4be96dfaca72ef9274846f4afc`
in both manifests, and `/audit-input.json` binds the producer-source path to the
same digest as its final path component. The complete producer tree hash is
`94ba4c012f48b7135094fefcc4517f5c9a5c1052fc304449c5505ddb4dca91b4`,
matching the audit input. Evidence:
[01_producer_and_manifests.log](/audit-output/evidence/01_producer_and_manifests.log),
[04_producer_provenance_crosscheck.log](/audit-output/evidence/04_producer_provenance_crosscheck.log),
and [29_recorded_hashes_complete.log](/audit-output/evidence/29_recorded_hashes_complete.log).

I also recomputed all launcher resolution tree/file hashes, the canonical
`resolved_input_sha256`, both selected-artifact bindings, every one of the 771
recorded Stage 1 source hashes, the generated obligation-map hash, the trust
inventory hash, and all cross-manifest Stage 1, Stage 3, and generated-tree
bindings. There were no mismatches. The principal hashes were:

| Artifact | Recomputed hash |
|---|---|
| Frozen Stage 1 export | `868472ef4f7bb79756afc934d16dd4ecbbd1c65bf0f6ea3d6b883c0417fa8fde` |
| Stage 1 selected workspace tree | `4673eef6746187c6cc7d375b0cae5708546ef9da0a514a16ac66f5487b937f15` |
| Stage 2 selected audit tree | `be4784e66b25dec74de4462c8caacfa52fef0f48ada2842de216bf73b5d887a5` |
| Stage 3 discovery manifest | `4a424a8360f09aa136db98718ee61792ecd45e4de19b473b1f52143b71086a9c` |
| Generated project tree | `580fcf278ef6e8f4edf7f94b4591b0bbcc3a276bd08b25836a934a2ad756b8b7` |
| Selected Stage 4 generation tree | `b903d8551afa6399d4187ec12ef9feb6f3b3bff9580546169dd90f1ab0576a5b` |

## Inventory reconstruction

Using `tools.k_rule_inventory.inventory_verification` with
`PYTHONPATH=/reference`, I reconstructed the local verification-module closure
from the frozen `/reference/k-proof/verification.k`. The trusted inventory
selected module `VERIFICATION`; its local closure contains only that module and
exactly four rules. Its recomputed whole-inventory hash is
`dc118fb2034590e8e04149fd7a07acea6f25a1a3a3647e0f86dec6fe34a96c14`.

| Span | Normalized SHA-256 / source rule ID | Attributes |
|---|---|---|
| line 8 | `f5c7b761ec71892275f909c07e8f29124daca7a634e74c5709cda21666d9b165` / `rule-f5c7b761ec71892275f909c07e8f29124daca7a634e74c5709cda21666d9b165` | none |
| lines 9–10 | `581f4df071fdd7d974c5141cf36a1e876f38b798cc51952636578533c09a0f8a` / `rule-581f4df071fdd7d974c5141cf36a1e876f38b798cc51952636578533c09a0f8a` | none |
| lines 15–17 | `7a08aa58034b9a659c1e60660998e0b301a0f3e3408204cc84b658c58946b4d0` / `rule-7a08aa58034b9a659c1e60660998e0b301a0f3e3408204cc84b658c58946b4d0` | none |
| lines 18–20 | `caabcce04b85453cd68f8e2e64ab67393a09fdfcffd4cf6a5de838b958201752` / `rule-caabcce04b85453cd68f8e2e64ab67393a09fdfcffd4cf6a5de838b958201752` | none |

The reconstructed IDs are unique, each ID is exactly `rule-` plus its
normalized source hash, and their order exactly matches
`/reference/lemma-discovery.json`. The discovery IDs are also unique, the rule
counts and sets agree, and the whole-inventory hash agrees. Thus there are no
omitted, duplicated, extra, reordered, changed, or unclassified rules. Full
rule text and comparison output are in
[06_inventory_reconstruction.log](/audit-output/evidence/06_inventory_reconstruction.log).

## Independent classification judgment

I independently classify all four entries as `DEFINITION`, agreeing with Stage
3:

1. `allIntVS(.ValSeq) => true` is the base equation for the newly declared
   `allIntVS` summary.
2. The `vCons` equation is its structural recurrence, testing the head and
   recurring on the strict `ValSeq` tail.
3. The nonnegative `popcountAbs` equation defines the named summary using the
   frozen `binCodes` and `cntSub` functions.
4. The negative equation is the complementary defining case, first taking the
   integer magnitude and then applying the same frozen functions.

This classification follows behavior, not names. The first two rules define a
predicate used as the whole-program claim's integer-list precondition. The last
two define the summary used by the separately proved exact key-lambda execution
claims. In the supplied semantics, `binCodes(0)` is the code sequence for `0`,
positive inputs recurse through `binAcc`, negative `bin` execution applies
`binCodes(0 -Int N)`, and `cntSub` is the recursive non-overlapping substring
counter. Code point 49 is `"1"`. The guards `I >=Int 0` and `I <Int 0` are
disjoint and exhaustive over K integers.

None of these rules rewrites a program configuration or observes ordinary
execution, so none is an `OPERATIONAL_RULE`. None states a consequence about
pre-existing terms that Stage 1 would have to prove before later use, so none is
a `PROVED_DERIVED_LEMMA`. Most importantly, none asserts an independent
human-facing property such as sortedness, permutation, stability, or a
popcount theorem about an already defined result; each supplies an equation for
a freshly named summary. Thus none is a `DOMAIN_LEMMA`, mislabeled or otherwise.
All four are relevant to the frozen program or the claim precondition. There
are no `[simplification]` attributes, so the simplification-class restriction
is satisfied vacuously.

Relevant frozen semantics excerpts are captured in
[08_relevant_operational_semantics.log](/audit-output/evidence/08_relevant_operational_semantics.log).
Ground boundary checks cover zero, both signs, large magnitudes, empty and mixed
lists, and the supplied example shapes. Replacing code point 49 with 48 changes
the output on `[1,2,3,4]`; removing the magnitude conversion leaves
`binCodes(-6)` outside every frozen equation. These counterfactuals confirm that
the defining details are operationally material. See
[31_definition_witnesses.log](/audit-output/evidence/31_definition_witnesses.log).

## Stage 4 structural and mathematical audit

I directly invoked `tools.klean_preflight.check_generation` with
`PYTHONPATH=/reference`, the frozen Stage 1 workspace, protected discovery
manifest, selected generation, and trusted toolchain lock. The first attempt
exposed an audit-sandbox PID-namespace issue: Lean 4.22 reads
`/proc/<getpid()>/exe`, while the mounted `/proc` exposes host PIDs. I documented
the failure and used a minimal `LD_PRELOAD` shim that maps `getpid()` to the
host-visible numeric `/proc/self` target. This changes no K input, generated
file, checker code, Lean declaration, or theorem; it only lets the pinned Lean
binary locate its immutable sysroot. The pinned binary then reported Lean
4.22.0 at commit `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`.

With that environment repair, the unchanged trusted checker returned:

- status `KLEAN_NO_OBLIGATIONS`;
- obligation count `0`;
- target `null`;
- `lake clean` exit `0` with empty output;
- `lake build` exit `0` with output hash
  `a1e847341e738cf1ba9661c0e0251e5d3c3225c0c81eb52ad9108f85ceaaacec`;
- the same Stage 1, Stage 3, and generated-tree hashes recomputed above; and
- no designated sorries.

The complete fresh result is
[26_check_generation_rerun.log](/audit-output/evidence/26_check_generation_rerun.log).
It is exactly equal as a JSON value to both the immutable Stage 4 preflight
sidecar and the launcher-recorded `stage4_preflight` object, as shown by
[30_preflight_evidence_comparison.log](/audit-output/evidence/30_preflight_evidence_comparison.log).

The independent mathematical domain set is empty. Consistently:

- discovery has zero `DOMAIN_LEMMA` entries;
- `input-manifest.json` has no `source_rules`;
- `obligation-map.json` has no source rules, obligations, or trust parameters;
- the obligation IDs form an exact empty bijection with the independently
  classified domain set;
- all obligation counts are zero;
- `klean_export.target_statement` returns `None`;
- `generator-manifest.json` and `/audit-input.json` both record target `null`;
  and
- `/candidate` does not exist.

Therefore there is no omitted or duplicate obligation, no irrelevant or
weakened obligation, no vacuous conjunct, and no target mutation. In the empty
case there must be no generated target or Stage 5 candidate, and both are
absent. The independent check is in
[28_bijection_and_target.log](/audit-output/evidence/28_bijection_and_target.log);
the raw generated surface is in
[27_generated_obligation_and_target_surface.log](/audit-output/evidence/27_generated_obligation_and_target_surface.log).

## Stage 5 applicability

Stage 5 is not selected in `CLASSIFICATION_ONLY`, and the legitimately empty
domain set produces no theorem to prove. Consequently there is no `Base` copy,
candidate clean build, `Proof.final`, axiom print, target-parameter bridge, or
candidate trust escape to audit. Running any of those checks would require a
target and candidate that the protocol expressly forbids in this no-obligation
case.

VERDICT: PASS
LEGITIMACY: LEGIT
