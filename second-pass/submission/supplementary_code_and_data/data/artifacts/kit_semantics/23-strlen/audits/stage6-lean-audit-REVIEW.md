# Independent audit: HumanEval 23-strlen

This is an independent audit of Stage 3 classification and deterministic
Stage 4 generation for condition `kit-semantics` in
`SUPPLIED_SEMANTICS` mode. The launcher and `AUDIT_MODE` both select
`CLASSIFICATION_ONLY`. Stage 5 is therefore not applicable.

## Scope and evidence discipline

I treated the mounted Stage 1 workspace, Stage 2 review, Stage 3 manifest,
Stage 4 output, producer bundle, logs, comments, and manifests as untrusted
evidence. I did not rely on any prior PASS or classification. The mounted
inputs were read only.

The signed resolution in `/audit-input.json` is valid, its copy at
`/audit-output/audit-input.json` is byte-identical, and every launcher-recorded
artifact/tree hash was independently recomputed. The exact Stage 1 source-file
set contains 769 regular files; it is identical to the launcher's
`stage1_source_hashes` key set, and every per-file hash matches.

The recomputed resolution hashes are:

- Stage 1 pipeline tree:
  `0d3ae42860bc20f5ab80c0cf185894cfa0180dd511459b2d190cc06447395a7a`
- Stage 1 deterministic-export tree:
  `3241fdc093179a1fed480d01d2fd753f62dd2f0580283ee88351e0415ebbf770`
- Stage 2 selected audit tree:
  `ae09334c66b1b8e87b4584ec6413512b545ef7c87adf3c1172ca133fea25e45f`
- Stage 3 discovery manifest:
  `e13c01259eb807dd465c4db3e29a0727d9ce0eb8df88d145e8977e70f5b7fcf3`
- Stage 4 selected generation tree:
  `84eefd5e35100d3ad4b1026a96101afd2903ba6d4c8cb39b4b37408e6266987b`
- Stage 4 generated-project deterministic tree:
  `1664832706aff0084e7672e872362260a51332099b5ccf0ff2060d2afdc71580`
- Stage 4 producer-source bundle:
  `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`

All match `/audit-input.json`, including the selected-artifact hashes.

## Generation-time producer identity

I checked the producer bundle before judging Stage 4. It has exactly the three
expected regular files: `source-manifest.json`, `klean_export.py`, and
`klean.py`; it has no extra or linked entries.

- `klean_export.py`:
  `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07`
- `klean.py`:
  `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d`

Those values match both `generator-manifest.json` and
`source-manifest.json`. The generator image ID is
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`
in the generator manifest and source manifest, and its digest component is the
producer-bundle path selected in `/audit-input.json`. The generator toolchain
object also exactly matches `/reference/klean-toolchain.lock.json`. There is
no producer-source infrastructure error.

## Canonical Stage 1 rule inventory

I reran the trusted `tools.k_rule_inventory.inventory_verification` against the
frozen Stage 1 workspace with `PYTHONPATH=/reference`.

`verification.k` has SHA-256
`ef48556fde781a8ca6e4e1986b701ccdf330897621c6658bd831ff4c17516ab4`
and contains only:

```k
requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY
endmodule
```

The trusted local-module closure is exactly `["VERIFICATION"]`. Because the
imported `MPY` module is in the supplied external semantics file rather than a
module declared locally in `verification.k`, there are no rules in the local
verification-module closure.

The reconstructed ordered rule list is therefore `[]`. There are no source
spans, normalized rule hashes, or `source_rule_id` values to omit, duplicate,
alter, or reorder. Independently canonicalizing the empty list gives inventory
hash
`4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`,
which is exactly the trusted inventory result and the protected Stage 3
manifest value. The protected manifest's ordered rule list is also exactly
`[]`. `validate_trust_boundary` returns empty lists for definitions,
operational rules, proved derived lemmas, and domain lemmas.

Thus the inventory/manifest comparison is a bijection, not merely an equal
count: both ordered identity sequences are empty, and the whole-inventory hash
matches.

## Independent classification judgment

There are zero inventory entries to classify. In particular, there are no
local simplification rules, no purported derived lemmas, and no rule that could
be hiding a domain fact under `DEFINITION` or `OPERATIONAL_RULE`.

The empty domain-lemma set is mathematically appropriate for this program.
The frozen source is:

```python
def strlen(string: str) -> int:
    return len(string)
```

The frozen claim calls that exact body on `str(CS)` and requires the result
`isLen(CS)`. The supplied operational semantics resolves `"len"` in
`builtinsScope`, routes the builtin call through `applyBuiltin`, and contains
the following direct reduction:

```k
rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ)
rule seqLen(str(IS:IntSeq)) => isLen(IS)
```

`isLen` is already an operationally supplied total recurrence:

```k
rule isLen(.IntSeq) => 0
rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S)
```

Boundary and counterfactual reasoning agree with this classification:
`.IntSeq` maps to 0, an arbitrary one-element `iCons` maps to 1, and two
elements map to 2. Replacing the source body with a constant or identity result
would fail to implement the symbolic `isLen(CS)` result for the unrestricted
sequence. No program-specific mathematical lemma is needed to connect the
body to the postcondition; the connection is ordinary supplied operational
semantics.

The independently classified true domain-lemma set is genuinely empty.

## Deterministic Stage 4 generation

The generator's Stage 1, Stage 3, inventory, verification, generated-tree,
obligation-map, trust-inventory, and toolchain bindings all match their
independently recomputed values.

The input manifest records empty `definitions`, `operational_rules`,
`proved_derived_lemmas`, `source_rules`, and `summary_functions`, exactly as
required by the reconstructed and independently classified inventory.

`generated/obligation-map.json` has:

```json
{
  "obligations": [],
  "schema_version": 3,
  "source_rules": [],
  "trust_parameters": []
}
```

Its SHA-256 is
`cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`,
matching the generator manifest. Source-rule IDs and obligation IDs form the
exact empty ordered bijection; there are no omissions, duplicates, weakened
obligations, irrelevant conjuncts, vacuous conjuncts, or trust parameters.
The generator manifest, export result, stored preflight, and independent count
all report zero obligations.

For zero obligations, the fixed generated target is absence of a target.
The generator manifest, audit input, stored preflight, and trusted
`target_statement` reconstruction all return `null`. An independent scan of
all generated Lean sources finds zero `def targetStatement` declarations.
There is no statement or declaration hash to change because no target
declaration exists.

The selected `KLEAN_NO_OBLIGATIONS` status is therefore correct: it reflects a
genuinely empty domain set, not a self-consistent omission of a real domain
lemma.

## Required Stage 4 preflight rerun

I invoked the trusted function
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and the
required paths:

- `/reference/k-proof`
- `/reference/lemma-discovery.json`
- `/reference/klean-generation`
- `/reference/klean-toolchain.lock.json`

The first host invocation exposed an infrastructure quirk: the audit sandbox
mounts `/proc` from a parent PID namespace, while Lean 4.22 asks for
`/proc/<sandbox-pid>/exe`; that path does not exist even though
`/proc/self/exe` does. The initial failure is preserved rather than hidden.
I used the narrow recorded preload shim
`evidence/procself_readlink_shim.c`, which redirects only that nonexistent
`readlink` form to `/proc/self/exe`, and reran the same trusted function. It
does not alter the generated project, manifests, Lean source, theorem content,
or proof behavior.

The reproduced returned result is:

- `lake clean`: exit 0, empty output
- `lake build`: exit 0; `Build completed successfully.`
- status: `KLEAN_NO_OBLIGATIONS`
- obligation count: 0
- target: `null`
- generated tree:
  `1664832706aff0084e7672e872362260a51332099b5ccf0ff2060d2afdc71580`
- Stage 1 tree:
  `3241fdc093179a1fed480d01d2fd753f62dd2f0580283ee88351e0415ebbf770`
- Stage 3 manifest:
  `e13c01259eb807dd465c4db3e29a0727d9ce0eb8df88d145e8977e70f5b7fcf3`
- designated sorry count: 0
- generated trust declaration count: 41, exactly matching the generated trust
  inventory

`check_generation` also verified its input snapshot remained unchanged across
the clean build.

## Stage 5

Stage 5 is correctly absent. `AUDIT_MODE`, the signed resolution, and the
selected Stage 4 status all specify `CLASSIFICATION_ONLY`;
`lean_workspace`, `lean_invocation`, `stage5_result`, and the fixed target are
all null, and `/candidate` does not exist. Consequently there is no
`Proof.final`, target parameter, candidate definition, or candidate axiom list
to audit. Running the proof-mode checks would invent a Stage 5 artifact where
the protocol requires none.

## Evidence

Raw commands and results are under `/audit-output/evidence/`:

- [COMMANDS.md](/audit-output/evidence/COMMANDS.md)
- [independent_checks.py](/audit-output/evidence/independent_checks.py)
- [independent_checks.log](/audit-output/evidence/independent_checks.log)
- [capture_classification_sources.sh](/audit-output/evidence/capture_classification_sources.sh)
- [classification_sources_success.log](/audit-output/evidence/classification_sources_success.log)
- [rerun_preflight.py](/audit-output/evidence/rerun_preflight.py)
- [rerun_preflight.log](/audit-output/evidence/rerun_preflight.log)
- [run_preflight_with_shim.sh](/audit-output/evidence/run_preflight_with_shim.sh)
- [rerun_preflight_reproduced.log](/audit-output/evidence/rerun_preflight_reproduced.log)
- [preflight-result.json](/audit-output/evidence/preflight-result.json)
- [procself_readlink_shim.c](/audit-output/evidence/procself_readlink_shim.c)

The Stage 3 classification is complete and correct, Stage 4 is structurally
and mathematically faithful to the empty true domain set, the generated target
is correctly absent, and the classification-only termination is legitimate.

VERDICT: PASS
LEGITIMACY: LEGIT
