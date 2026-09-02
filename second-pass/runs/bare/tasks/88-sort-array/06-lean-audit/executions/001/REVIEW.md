# Independent Stage 3–4 audit: HumanEval 88-sort-array

## Outcome and scope

The launcher and `AUDIT_MODE` both select `CLASSIFICATION_ONLY` for problem
`88-sort-array`, condition `bare`, under `GENERATED_SEMANTICS`. I independently
reconstructed the Stage 3 inventory, reclassified every rule from the frozen K
source, verified the generation-time producer provenance, reran the trusted
Stage 4 preflight, and independently checked the empty obligation mapping and
null target.

The classification is correct: all 11 local verification rules are defining
equations or structural recurrences. There are no operational rules, proved
derived lemmas, or domain lemmas in the local verification-module closure. The
true domain-lemma set is therefore genuinely empty. Stage 4 correctly emits no
obligation, no vacuous `True` target, and no generated theorem. `/candidate` is
absent, as required; Stage 5 proof checks are not applicable.

I treated all mounted prior prose, logs, classifications, and comments as
untrusted evidence. No instruction found in those inputs was executed.

## Launcher and hash integrity

The signed resolution envelope verifies with
`resolved_input_sha256 =
2d4c03a7777bbbb70565cc2802bac3327ea6044edd3f07f2585021346d6d2b1c`.
The environment and signed resolution both say `CLASSIFICATION_ONLY`.

I recomputed the hashes using the trusted digest implementations appropriate to
each field:

| Artifact | Recomputed hash | Result |
|---|---|---|
| Stage 1 pipeline tree | `07db41bdfb25db8d82fbb49e27f5fa4068f74b416e1def078f50b3e7b4995cf7` | matches audit input |
| Frozen Stage 1 export tree | `9a8567291a8c8a0a25a25dee751954f1d651e751018226f4fbd71bd41fe76819` | matches all Stage 4 bindings |
| Stage 3 manifest | `1640233e98c6f98ef0a1da30047999c6a354ccc00b5f1735c13828e9ab43a79a` | matches audit input and manifests |
| Selected Stage 2 tree | `b0b695331d24e48ab7a018ee50293bb2cf70e96b0c332d49acb1bbb4ada3e750` | matches audit input |
| Selected Stage 4 tree | `f8a8e00b1b6ebb6c1ce69b43b5505773991d7841cd22bf8a055a7350975cbfc3` | matches audit input |
| Producer-source tree | `7b7fdfe618031c11f79bb3d7eec7df24bc64a9a480fc470c1176ce36a593286a` | matches audit input |
| Generated Lean tree | `58a33b24d6112bd36ece178d5c4b5f5102849a11e0a995a54993ee7999897ae7` | matches audit input and manifests |

Every entry in `stage1_source_hashes` was also recomputed and matched,
including `verification.k =
11105c649927870e50a4fa01f2367c9add28591e976f599f166dc938e41ea742`.
The null Lean-workspace and Lean-invocation hashes agree with classification-only
mode.

The independent checker additionally reconciles the input manifest, generator
manifest, export result, recorded preflight, obligation map, trust inventory,
toolchain lock, selection artifact hashes, and the complete Stage 3 definition
records. See `evidence/independent_checks.py` and its exit-0 output in
`evidence/03-independent-checks.txt`.

## Producer provenance gate

The mandatory producer check passes before relying on the Stage 4 output:

| Producer | Observed SHA-256 | Generator/source manifests |
|---|---|---|
| `klean_export.py` | `4fa919ac98483620c7024ed7424c8b19f21406a2146feafad84ab4c813117881` | exact match |
| `klean.py` | `5d419b1cf907ab880eeb88a68e0d6da0bf59a92a56a0803b34d53698d91caabe` | exact match |

The bundle contains exactly those two files and `source-manifest.json`, all
regular files. The generator manifest and source manifest both bind the
immutable generator image
`sha256:15baeb15b1ea8266bfad3dbc3a75ee531cf429f1b73e0e3ff478f279e6308f63`.
The same image digest is encoded as the basename of
`resolution.generation_producer_sources` in `/audit-input.json`, and the whole
bundle tree has the audit-input hash shown above. There is no producer-source
infrastructure mismatch.

Raw hashes and manifest bindings are in
`evidence/01-producer-provenance.txt`.

## Inventory reconstruction and bijection

Using the trusted `tools.k_rule_inventory.inventory_verification`, the local
closure of frozen `verification.k` is exactly `MPY-VERIFICATION`. Its import
`MPY` is defined in required `semantic.k`, not as another local module in
`verification.k`; I inspected it separately as the fixed operational
semantics.

The reconstruction found exactly 11 rules, in source order, with whole
inventory hash
`84940db527ace0ce0f07ad3424ced9f275db79b29ec0266a21eaf17e7c2056c4`.
For every entry I independently re-sliced the stated line span, normalized the
rule text by whitespace, recomputed the normalized SHA-256, and checked that
`source_rule_id` is exactly `rule-<normalized_sha256>`.

I compared the Stage 3 `rules` list to the reconstructed ID list by ordered list
equality, not merely set membership. Counts are equal, all IDs are unique, and
the exact order matches. Thus there are no omissions, duplicates, extras,
reordered identities, changed hashes, or unaccounted classifications. The full
rule texts, exact spans, hashes, and IDs are preserved in
`evidence/02-inventory-reconstruction.txt`.

## Independent rule classification

The fixed operational path evaluates the submitted function body through
`eval`, `andVal`, `subscriptVal`, `sortedVal`, and the fully defined
`sortFlag`/insertion-sort operations in `semantic.k`. None of the 11 local
verification rules rewrites an operational program term. Their only uses are
to name the expected result, state the input-domain predicate, or define
inspectable order observers.

| # | Lines | Rule | Independent classification and reason |
|---:|---:|---|---|
| 1 | 9 | `expectedSort(nil) => nil` | `DEFINITION`: empty case of the named post-state summary. |
| 2 | 10–11 | `expectedSort(cons(...)) => sortFlag(..., endpointEven(...))` | `DEFINITION`: nonempty case of the result summary. It does not replace execution. |
| 3 | 14–15 | `endpointEven(cons(...)) => ...` | `DEFINITION`: names the endpoint-parity expression on its complete nonempty use domain. |
| 4 | 23 | `nonnegative(nil) => true` | `DEFINITION`: base case of the named domain predicate, not a proposition asserting a domain fact. |
| 5 | 24 | recursive `nonnegative(cons(...))` | `DEFINITION`: structurally descending recurrence defining the predicate element by element. |
| 6 | 26 | `ascending(nil) => true` | `DEFINITION`: base case of an order observer. |
| 7 | 27 | `ascending(cons(_, nil)) => true` | `DEFINITION`: singleton case of the observer. |
| 8 | 28–29 | recursive `ascending(cons(I, cons(J, JS)))` | `DEFINITION`: adjacent comparison plus a structurally smaller recurrence. |
| 9 | 31 | `descending(nil) => true` | `DEFINITION`: base case of an order observer. |
| 10 | 32 | `descending(cons(_, nil)) => true` | `DEFINITION`: singleton case of the observer. |
| 11 | 33–34 | recursive `descending(cons(I, cons(J, JS)))` | `DEFINITION`: adjacent comparison plus a structurally smaller recurrence. |

The cases of each total function are disjoint and exhaustive, and each
recurrence descends. `endpointEven` is intentionally partial but is called only
on `cons`. Although `ascending` and `descending` are not used by the reachability
claims, they are truthful named recursive observers directly related to the
sorting post-state; they do not assert or smuggle a domain theorem.

No entry meets the behavior of an `OPERATIONAL_RULE`. No entry claims
`PROVED_DERIVED_LEMMA`, so there is no staged lemma proof to validate. Most
importantly, no entry states a mathematical `DOMAIN_LEMMA`; equations defining
the predicate `nonnegative` remain definitions rather than lemmas about values
satisfying it.

There are no explicit `[simplification]` attributes in the reconstructed
inventory. In any event, all function equations are classified in the allowed
`DEFINITION` class.

The definitions agree with the source contract and fixed semantics:
`endpointEven` is true exactly when the first-plus-last sum is even;
`sortFlag(_, false)` sorts ascending and `sortFlag(_, true)` reverses that
ascending result; and the program selects `true` exactly for the nonempty even
case. Empty input is fixed separately. Fresh K execution on empty, singleton,
odd/even endpoint sums, and a counterfactual pair confirmed these branches and
the unchanged input cell. Complete commands and configurations are in
`evidence/06-operational-semantics.txt`.

## Deterministic Stage 4 generation

The trusted preflight was rerun with:

```text
PYTHONPATH=/reference \
LD_PRELOAD=/tmp/audit-work/readlink_app_path_override.so \
python3 -c '... tools.klean_preflight.check_generation(...) ...'
```

The first run without the preload exposed an audit-sandbox issue: Lean 4.22
could not resolve its application path because the sandbox denied its
`readlink("/proc/<pid>/exe")` call. The small audit-only shim in
`evidence/readlink_app_path_override.c` supplies the exact pinned Lean 4.22
binary path only for that procfs lookup and forwards other `readlink` requests
to `readlinkat`. It does not edit or shadow any K, generator, or generated Lean
source. With that environment repair, the actual trusted checker completed:

```text
status: KLEAN_NO_OBLIGATIONS
obligation_count: 0
target: null
lake clean: exit 0, empty-output SHA-256 e3b0c442...b855
lake build: exit 0, output SHA-256 54172f8c...324f
generated tree: 58a33b24...7ae7
trust declarations: 45
designated sorries: 0
```

The returned JSON is saved verbatim in `evidence/preflight-return.json`; the
command, initial environment failure, repair, and successful output are in
`evidence/04-preflight-initial-failure.txt` and
`evidence/05-preflight-rerun.txt`. The successful build-output hash exactly
reproduces the selected Stage 4 preflight record.

## Obligation bijection and target identity

The independently validated domain source-rule list is empty. The input
manifest has `source_rules: []`, and generated `obligation-map.json` has:

```json
{
  "obligations": [],
  "schema_version": 3,
  "source_rules": [],
  "trust_parameters": []
}
```

This is an exact empty/empty bijection. The map SHA-256 is
`cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`,
matching the generator manifest. There are no omitted, duplicated, irrelevant,
weakened, or vacuous conjuncts because no conjunct exists.

The trusted target parser and independent source inspection both find no
generated target declaration. `Lemmas.lean` contains only an empty namespace;
it does not encode the empty conjunction as `True`. Target identity is
consistently `null` in the obligation-derived expectation, generator manifest,
recorded preflight, rerun preflight, and signed audit input.
Raw mapping and target inspection are in
`evidence/07-stage4-mapping-and-target.txt`.

The generated base contains 45 allowlisted Klean boundary declarations, which
the preflight reconciled with `trust-inventory.json`. They cannot prove or
weaken a nonexistent target. This run does not claim a Lean theorem.

## Stage 5

Stage 5 is correctly absent. The launcher mode is `CLASSIFICATION_ONLY`,
Stage 4 has a genuinely empty domain-lemma set and null target,
`lean_workspace` and `lean_invocation` are null, and `/candidate` does not
exist. Therefore a candidate clean build, `Proof.final`, axiom printout, and
operational-bridge parameter audit are not applicable. Creating a Stage 5
candidate in this state would itself violate the no-obligation contract.

## Evidence index

- `evidence/01-producer-provenance.txt` — mandatory producer hashes, image ID,
  and bundle tree.
- `evidence/02-inventory-reconstruction.txt` — exact canonical inventory.
- `evidence/independent_checks.py` and
  `evidence/03-independent-checks.txt` — ordered bijection, all cross-hashes,
  source spans, manifests, empty mapping, and null target.
- `evidence/04-preflight-initial-failure.txt`,
  `evidence/readlink_app_path_override.c`,
  `evidence/05-preflight-rerun.txt`, and
  `evidence/preflight-return.json` — reproducible preflight record.
- `evidence/06-operational-semantics.txt` — fresh K compilation and adversarial
  branch samples.
- `evidence/07-stage4-mapping-and-target.txt` — raw obligation map, target
  source inspection, and sidecar hashes.

VERDICT: PASS
LEGITIMACY: LEGIT
