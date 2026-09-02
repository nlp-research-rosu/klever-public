# Independent audit: HumanEval 151 `double_the_difference`

## Scope and result

This audit covers condition `semantics`, semantics mode
`SUPPLIED_SEMANTICS`, and launcher mode `CLASSIFICATION_ONLY`. The value of
`AUDIT_MODE` and `/audit-input.json` both say `CLASSIFICATION_ONLY`.

I independently reconstructed and classified the Stage 1 rule inventory,
checked the Stage 3 manifest as an ordered bijection, verified Stage 4 producer
provenance before judging the generation, reran the trusted Stage 4 preflight,
and independently checked the empty obligation map and absent target. I did not
rely on the selected Stage 2 review or any prior verdict.

The classification is correct: the true domain-lemma set is empty. Therefore
`KLEAN_NO_OBLIGATIONS`, no generated target, and no Stage 5 candidate are the
correct outcomes.

## Frozen-input and producer integrity

All launcher-recorded hashes recomputed successfully:

| Artifact | Recomputed SHA-256 |
|---|---|
| Stage 1 pipeline tree | `5251dc75600543f6a2a22547737c10dd60d9eb6320f693e596e7a17b1e1fc08c` |
| Stage 1 export tree | `9ef85610e30abb61fae24a61a5ca98d3bbf09e624243d1d90dc6d41a2033cc80` |
| selected Stage 2 audit tree | `f39642d8a0141b6332eb47caf82646f4f1be175319c48cee64f411867fc38677` |
| Stage 3 manifest | `b3866f644f3fa7f04e9e228677f0398d364873b1b4d523b8194b81cdc9d733e9` |
| generated Lean tree | `1f5689f19f3dac581188ea7768ce3c9a57814ee949f6b20a094ab5b3dc569d7e` |
| selected Stage 4 tree | `706984a3b0988f1677c45b1956a3348e103c2f39876dcbf7e6aff9f872803ca8` |
| producer-source bundle tree | `55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c` |

The 764 individual Stage 1 source hashes in `/audit-input.json` form an exact
file-name and hash match: no missing, extra, or mismatched source file.

Before assessing Stage 4, I hashed the two mounted generation-time producer
files:

- `klean_export.py`:
  `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0`
- `klean.py`:
  `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1`

Both values match `generator-manifest.json` and
`generation-tools/source-manifest.json`. The immutable image ID is
`sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000`
in both manifests, and its digest component exactly matches the
image-addressed producer path recorded in `/audit-input.json`. The bundle
contains only the two producer files and its source manifest. Thus there is no
producer-provenance `AUDIT_ERROR`.

Raw recomputation is in
[`03-hash-audit.log`](/audit-output/evidence/03-hash-audit.log); the auditable
driver is [`hash_audit.py`](/audit-output/evidence/hash_audit.py).

## Inventory reconstruction and Stage 3 bijection

Using the trusted `tools.k_rule_inventory.inventory_verification` on the frozen
workspace selected `DOUBLE-THE-DIFFERENCE-VERIFICATION` from `prove.sh`. Its
local verification-file closure contains that one module and exactly ten
rules. The reconstructed values are:

- `verification.k` SHA-256:
  `1a27d700c21e24ef281501b9b054c0106b0e8c615727011975f6b6bac88fceec`
- canonical inventory SHA-256:
  `02212329e16923774f59936013dba11e53f137877b36d944612fd0c75aa283aa`
- source spans, in order:
  `16–17`, `18–19`, `20–21`, `24–28`, `31`, `32–33`, `34–35`,
  `38`, `39`, `40`

For every rule, the trusted inventory recomputed its exact source text,
normalized source SHA-256, `source_rule_id`, attributes, and span. The Stage 3
manifest has exactly the same ten unique IDs in exactly the same order and the
same whole-inventory hash. There are no omissions, duplicates, extras,
reordered identities, changed hashes, or unaccounted classifications.

The complete reconstructed records are in
[`01-reconstructed-inventory.log`](/audit-output/evidence/01-reconstructed-inventory.log).
The trusted boundary validation result is in
[`02-stage3-bijection.log`](/audit-output/evidence/02-stage3-bijection.log).

## Independent classification judgment

I classified from the frozen rule text and supplied MPY semantics, not from the
Stage 3 rationales.

| Frozen lines | Independent class | Judgment |
|---|---|---|
| 16–17 | `OPERATIONAL_RULE` | Empty observation for the added `numVals` list representation: `#iterNext` produces `#iterDone`. |
| 18–19 | `OPERATIONAL_RULE` | Integer-head observation: yield the head and the represented tail. |
| 20–21 | `OPERATIONAL_RULE` | Float-head observation: yield the head and the represented tail. |
| 24–28 | `DEFINITION` | Defining equation for the named total summary `oddSquare`. |
| 31 | `DEFINITION` | Empty base case for the named `doubleDifferenceSpec` fold. |
| 32–33 | `DEFINITION` | Integer-head recurrence for `doubleDifferenceSpec`. |
| 34–35 | `DEFINITION` | Float-head recurrence for `doubleDifferenceSpec`. |
| 38 | `DEFINITION` | Empty base case for the named loop proof term `finalNumber`. |
| 39 | `DEFINITION` | Integer-head recurrence for `finalNumber`. |
| 40 | `DEFINITION` | Float-head recurrence for `finalNumber`. |

The first three rules are ordinary execution/observation rules. The supplied
list semantics defines the same two `#iterNext` outcomes for native
`.ValSeq`/`vCons` lists. The new cases are disjoint and structurally
homomorphic: empty yields done, while either typed head yields that head and
the tail. They change only the active computation and do not state a
mathematical proposition.

The other seven rules are genuine definitions of declared named functions or
proof terms. For an integer head, `oddSquare` contributes `I * I` exactly when
`I > 0` and Python modulo by 2 is 1; otherwise it contributes zero.
`doubleDifferenceSpec` folds those contributions and ignores float heads.
`finalNumber` tracks the loop-target binding required by the loop invariant.
These equations align with the source program, the final claim, integer
arithmetic, `isinstance`, modulo, and loop iteration in the supplied semantics.

There is no separately proved-then-imported rule, so the
`PROVED_DERIVED_LEMMA` set is correctly empty. No inventory rule has a
`simplification` attribute, so the simplification classification restriction
is satisfied trivially. Most importantly, no rule asserts an independent
mathematical fact about the program result: the true `DOMAIN_LEMMA` set is
empty. There is therefore no hidden or irrelevant domain lemma.

The per-rule IDs, hashes, classifications, and judgments are in
[`11-independent-classification.log`](/audit-output/evidence/11-independent-classification.log),
with the relevant frozen source and operational semantics in
[`12-classification-source-context.log`](/audit-output/evidence/12-classification-source-context.log).

## Stage 4 generation and obligation audit

I invoked the required trusted function:

```text
PYTHONPATH=/reference python3 -c '
from tools.klean_preflight import check_generation
check_generation(
  /reference/k-proof,
  /reference/lemma-discovery.json,
  /reference/klean-generation,
  toolchain_lock=/reference/klean-toolchain.lock.json
)'
```

The first attempt exposed a container-only toolchain issue: this process runs
as namespace PID 2 while `/proc/2/exe` is absent, so Lake/Lean could not locate
its own executable. Supplying the pinned installation paths let `lake clean`
run, but Lean still failed on that `/proc` lookup. I then used the narrow
compatibility shim recorded in
[`lean_proc_compat.c`](/audit-output/evidence/lean_proc_compat.c), which only
redirects a failed `/proc/<pid>/exe` `readlink` to `/proc/self/exe`. It does
not alter the generated sources, manifests, Lean arguments, or frozen inputs.

With `PYTHONPATH=/reference` and that compatibility shim, the unchanged trusted
`check_generation` completed successfully:

- fresh `lake clean`: exit 0, empty-output SHA-256
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`;
- fresh `lake build`: exit 0, output SHA-256
  `208db0a3f72247a2982c8523fe0a21a218e5be75b16144851ea58b88d7ed666f`;
- status: `KLEAN_NO_OBLIGATIONS`;
- obligation count: 0;
- target: `null`;
- generated trust declarations: 48, exactly reconciled by the trusted
  preflight with `trust-inventory.json`;
- designated sorry count: 0.

The successful complete output is
[`06-rerun-check-generation-proc-compatible.log`](/audit-output/evidence/06-rerun-check-generation-proc-compatible.log).
The two environmental failure traces remain visible in
[`04-rerun-check-generation.log`](/audit-output/evidence/04-rerun-check-generation.log)
and
[`05-rerun-check-generation-with-pinned-env.log`](/audit-output/evidence/05-rerun-check-generation-with-pinned-env.log).

I also independently checked the Stage 4 records with trusted code:

- the input manifest exactly carries the reconstructed definitions,
  operational rules, proved-derived set, and empty domain-source set;
- all 25 required K files match the resolved closure after rebasing the
  generation-time `/frozen-k` mount to `/reference/k-proof`;
- the summary-function inventory and every source hash match;
- `obligation-map.json` is exactly
  `{"schema_version":3,"source_rules":[],"obligations":[],"trust_parameters":[]}`
  modulo JSON formatting;
- its SHA-256,
  `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`,
  matches the generator manifest;
- the ordered true-domain/input/map/obligation ID lists are all the same empty
  list, with no duplicates or vacuous conjunct;
- the generator toolchain equals the pinned lock, all generated and sidecar
  hashes reconcile, and the export-result trust-inventory hash matches.

These checks are recorded in
[`10-stage4-structural-audit.log`](/audit-output/evidence/10-stage4-structural-audit.log);
the driver is
[`stage4_audit.py`](/audit-output/evidence/stage4_audit.py).

## Fixed target and Stage 5

An empty true domain set requires no generated target. Independent scanning
found zero `targetStatement` declarations. Trusted target reconstruction,
`generator-manifest.json`, and `preflight.json` all report `null`. Thus there
is no weakened, duplicated, changed, or vacuous target.

Stage 5 is correctly absent: `/candidate` does not exist, and both Stage 5
hashes in `/audit-input.json` are `null`. Because the launcher mode is
`CLASSIFICATION_ONLY`, clean-building a candidate, printing
`#print axioms Proof.final`, and auditing candidate parameter definitions are
not applicable.

## Final judgment

Stage 3 correctly classifies every frozen local rule, the mathematically true
domain-lemma set is genuinely empty, and Stage 4 deterministically binds that
empty set to no obligations and no target. All provenance, source, tree,
manifest, obligation-map, and fixed-target checks pass. The selected
`KLEAN_NO_OBLIGATIONS` result is legitimate.

VERDICT: PASS
LEGITIMACY: LEGIT
