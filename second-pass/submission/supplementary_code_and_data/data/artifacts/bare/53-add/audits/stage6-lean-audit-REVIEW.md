# Independent audit: HumanEval 53-add, bare, GENERATED_SEMANTICS

## Outcome

The protected Stage 3 classification and selected deterministic Stage 4
generation are legitimate. The independently reconstructed local
verification-module inventory is genuinely empty, so the true domain-lemma set
is empty. Stage 4 therefore correctly reports `KLEAN_NO_OBLIGATIONS`, generates
no target theorem, and has no Stage 5 proof candidate.

The launcher and `/audit-input.json` both select `CLASSIFICATION_ONLY`.
Consequently, Stage 5 Lean proof, `Proof.final`, axiom-dependency, and
operational-bridge parameter checks are not applicable.

## Input and producer integrity

The signed audit-input envelope validates with resolved-input SHA-256
`a3a1eb181b1caf74fc2dc00934c0bf193897b539ebe39792a3335cf1423c1790`.
Independent recomputation matched every `resolution.hashes` entry, every
Stage 1 source-file hash, both selected-artifact hashes, the complete recorded
Stage 4 preflight object, and the `CLASSIFICATION_ONLY` environment mode. The
complete comparison is in `evidence/hash_audit.log`.

The required generation-time producer checks passed before the Stage 4
judgment:

- `klean_export.py`:
  `235473b1324d2b203cb2a49ab94e36fb7c300084d506a57fca2228381f1bdec0`
- `klean.py`:
  `ddec66db87398459ff0c2b5aad7121fe1029b58b8d576db4203c68bf5b647d13`

These are the exact hashes in both `source-manifest.json` and
`generator-manifest.json`. Both manifests identify immutable generator image
`sha256:e18301a8220fb0b62fabf56feffcb5e621049daa7c7a0b79eacb60cae5e57fda`.
The signed audit input binds the producer bundle through a path whose final
component is that same image digest, and its independently recomputed bundle
tree hash is
`363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0`.
There is no producer-source infrastructure error.

Other important recomputed hashes also match:

- Stage 1 canonical export tree:
  `653dedf138d76cb5d56669e32db3c7fe306525aa2c49c474da3e8c2e83533f5f`
- protected discovery manifest:
  `e13c01259eb807dd465c4db3e29a0727d9ce0eb8df88d145e8977e70f5b7fcf3`
- generated project tree:
  `fed9029716dec47e2b2de8fd67011564b392e8c86f099af5c110784adb44453d`
- selected Stage 4 artifact:
  `6c9899ab6388f04b4e15c5c07c9cb5aafa55b724c09718b3f6b106121e667369`

## Inventory reconstruction and Stage 3 classification

The trusted `tools.k_rule_inventory.inventory_verification` scanner selected
`VERIFICATION`, as fixed by the Stage 1 compile command, and reconstructed its
local in-file import closure as the one-element sequence `[VERIFICATION]`.
`verification.k` has exactly five lines: it requires `semantic.k`, declares
`VERIFICATION`, imports `SEMANTIC`, and ends the module. It contains no `rule`
sentence. Imported `SEMANTIC` is in the separately required `semantic.k`, not a
module declared in `verification.k`, so it is not a proof-local rule in the
scanner's local verification-file closure.

The canonical reconstruction is therefore:

- rule sequence: `[]`
- per-rule source spans: none
- per-rule normalized hashes: none
- per-rule `source_rule_id` values: none
- verification SHA-256:
  `4d68669eca55334e7ec3686ae3eb2dc6c166a9120d2a5cffe5fb43c16555061f`
- whole inventory SHA-256, the canonical hash of `[]`:
  `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`

The protected `lemma-discovery.json` contains the same inventory hash and the
same empty ordered rule sequence. The trusted Stage 3 boundary validator
reconstructed empty `definitions`, `operational_rules`,
`proved_derived_lemmas`, and `domain_lemmas`. Thus the comparison is bijective:
there are no omitted, duplicated, extra, reordered, hash-changed, or
unclassified identities.

There are no inventory entries to mislabel as `DEFINITION`,
`OPERATIONAL_RULE`, `PROVED_DERIVED_LEMMA`, or `DOMAIN_LEMMA`; there are also no
`simplification` attributes. In particular, no derived-lemma claim needs the
two-phase Stage 1 provenance test.

I separately inspected the frozen operational semantics rather than inferring
mathematical legitimacy from the empty manifest. Its eleven rules at
`semantic.k` lines 41-70 perform ordinary execution or observation:
module loading, function installation, invocation and parameter binding,
return-expression evaluation, integer and name evaluation, left-to-right
binary-addition evaluation, built-in `+Int`, and final result storage. None is
a summary, recurrence, macro, named proof term, algebraic shortcut, or
source/postcondition-specific domain lemma. The `+Int` rule is an operational
continuation step that computes the program's addition result.

This matches the frozen source `return x + y` and the exact postcondition
`result = X +Int Y`. Direct symbolic execution needs no mathematical fact beyond
the fixed K integer hook. Hence the independently classified true domain set is
genuinely empty; no relevant domain lemma has been hidden by the empty local
inventory.

As additional validation, I compiled a fresh copy with K 7.1.293 and reran the
unmodified claim. `kprove` returned `#Top`. Concrete executions produced `0`
for `(0,0)`, `-5` for `(-8,3)`, `0` for `(91,-91)`, and
`1111111110111111111011111111100` for the recorded large-integer pair. A false
postcondition mutation to `X +Int Y +Int 1` was rejected with the expected
stuck equality, and a body mutation to `return x` was rejected with residual
`X = X +Int Y`. These runs corroborate result constraint and body sensitivity;
they are not being used as a substitute for the inventory proof.

## Stage 4 generation, bijection, and target identity

The Stage 4 input manifest binds the verified Stage 1 and Stage 3 hashes and has
empty lists for definitions, operational rules, proved derived lemmas, source
rules, and summary functions. Independently deriving the Stage 4 source set
from the true `DOMAIN_LEMMA` set gives `[]`.

The generated `obligation-map.json` has:

- `source_rules = []`
- `obligations = []`
- `trust_parameters = []`
- SHA-256
  `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`

That hash equals `generator-manifest.json.obligation_map_sha256`.
The exact ordered source-rule/obligation bijection is therefore
`[] ↔ []`, with no duplicate IDs, omissions, weakened obligations,
irrelevant conjuncts, or vacuous conjuncts. Because the mathematical domain set
is empty, the zero-obligation result is substantive rather than a manifest-only
coincidence.

Target identity is also exact. The generator manifest, signed audit input, and
both preflight results all record `target: null`; an independent scan found
zero `def targetStatement` declarations in the generated Lean sources. No fixed
target was generated or changed. `export-result.json` consistently reports
`KLEAN_NO_OBLIGATIONS`.

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`
and the required three mounted inputs and pinned toolchain lock. The first run
exposed a sandbox-only installation-detection issue: child PIDs are absent from
this container's `/proc`, while Lean 4.22 uses `/proc/<pid>/exe` to find its
installation. I preserved that failure in `evidence/preflight_rerun.log`, then
used the narrowly scoped, fully recorded `evidence/proc_exe_shim.c` to answer
only that executable-path query from the already-installed pinned toolchain.
Lean then reported version 4.22.0 and commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, exactly matching the lock.

The unchanged trusted preflight then completed successfully:

- `lake clean`: exit 0
- `lake build`: exit 0
- status: `KLEAN_NO_OBLIGATIONS`
- obligation count: 0
- target: null
- designated sorry count: 0
- generated trust declarations: 44, exactly reconciled by the preflight's
  non-proposition trust allowlist gate

The preflight takes and rechecks immutable snapshots around its temporary clean
build, so the mounted Stage 1, Stage 3, and Stage 4 artifacts were not modified.
The successful returned evidence is
`evidence/preflight_rerun_with_proc_shim.log`; the separate manual structural
gate is `evidence/stage4_structure_audit.log`.

## Stage 5 absence

`/candidate` does not exist. The signed audit input records no Lean workspace,
no Lean invocation, no Stage 5 result, and no target. This is exactly the
required state for a legitimate `KLEAN_NO_OBLIGATIONS` selection. No Lean proof
or axiom-accounting claim is made in this audit mode.

## Evidence index

`evidence/COMMANDS.md` records the exact commands and maps them to complete raw
outputs. Key evidence includes:

- `inventory_reconstruction.log`
- `stage3_bijection.log`
- `hash_audit.log`
- `producer_sha256.log`
- `generator_manifest.log`
- `obligation_map.log`
- `preflight_rerun.log`
- `preflight_rerun_with_proc_shim.log`
- `stage4_structure_audit.log`
- `stage1_fresh_kprove.log`
- `stage1_false_postcondition.log`
- `stage1_body_mutation.log`

VERDICT: PASS
LEGITIMACY: LEGIT
