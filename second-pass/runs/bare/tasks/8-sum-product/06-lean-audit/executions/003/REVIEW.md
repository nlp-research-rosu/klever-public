# Independent Stage 3–5 Audit: `8-sum-product` / `bare`

## Scope and audit mode

The launcher and `/audit-input.json` both record:

- problem: `8-sum-product`;
- condition: `bare`;
- semantics mode: `GENERATED_SEMANTICS`; and
- audit mode: `CLASSIFICATION_ONLY`.

The selected Stage 4 status is `KLEAN_NO_OBLIGATIONS`. There is no selected
Stage 5 result, no Lean workspace or invocation in the signed audit input, and
`/candidate` is absent. Consequently, the Stage 5 candidate build,
`#print axioms Proof.final`, proof-identity, and parameter-bridge checks are not
applicable. I did not rely on the prior K audit's review or verdict.

## Stage 4 producer provenance gate

I performed this gate before judging the generated output. The mounted producer
files hash to:

| Producer | Recomputed SHA-256 |
|---|---|
| `klean_export.py` | `235473b1324d2b203cb2a49ab94e36fb7c300084d506a57fca2228381f1bdec0` |
| `klean.py` | `ddec66db87398459ff0c2b5aad7121fe1029b58b8d576db4203c68bf5b647d13` |

These are exactly the `exporter_sha256` and `klean_py_sha256` values in
`generator-manifest.json` and the two entries in
`generation-tools/source-manifest.json`. The source bundle contains exactly
those two sources and the source manifest.

The generator manifest and source manifest both record immutable generator
image
`sha256:e18301a8220fb0b62fabf56feffcb5e621049daa7c7a0b79eacb60cae5e57fda`.
The signed audit input's producer-source path ends in the same image digest, and
the recomputed mounted bundle tree hash
`363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0`
equals its recorded hash. Producer provenance therefore passes; there is no
infrastructure `AUDIT_ERROR`.

Evidence:

- `evidence/06_stage4_manifests.log`
- `evidence/09_hashes_and_producer_provenance.log`
- `evidence/29_target_and_stage5_absence.log`

## Independent rule-inventory reconstruction

I invoked the trusted inventory implementation on the frozen
`/reference/k-proof` workspace. `prove.sh` selects module `VERIFICATION`. The
local module closure represented inside `verification.k` is exactly
`["VERIFICATION"]`. The reconstruction found exactly one rule:

| Field | Reconstructed value |
|---|---|
| module | `VERIFICATION` |
| source span | lines 9–10 |
| normalized SHA-256 | `08e473cc777c3fe3dfbffc47a89f7ed00a323ab5af8be120c20538dd19dbc3e1` |
| source rule ID | `rule-08e473cc777c3fe3dfbffc47a89f7ed00a323ab5af8be120c20538dd19dbc3e1` |
| attributes | none |

The exact frozen text is:

```k
  rule expectedSumProduct(IS)
       => PyTuple(PyInt(sumInts(IS)), PyInt(productInts(IS)))
```

The recomputed `verification.k` SHA-256 is
`f862f6f645a2bf62a530087f0ced39b85a998b8be1be82566b5e86cc73e95d44`.
The canonical whole-inventory hash is
`e8b2af5d56d43143bcb41185878698b73f7fef8d96887a96fd2fbafe09431f9e`.

The protected Stage 3 manifest contains exactly this one identity in this
order, exactly once, and records the same inventory hash. Its own file hash is
`d529a4c1e08a7455591481e774b5eda00b9e800038dd70d1d0d204f98fac84ed`.
There are no omitted, duplicated, extra, reordered, changed-hash, or
unclassified entries.

Evidence:

- `evidence/01_trusted_rule_inventory_tool.log` through
  `evidence/01c_trusted_rule_inventory_tool.log`
- `evidence/02_frozen_sources_and_discovery.log`
- `evidence/05_inventory_reconstruction.log`

## Independent classification judgment

The sole rule is correctly a `DEFINITION`.

`verification.k` first declares
`expectedSumProduct(Ints) : PyVal` with `[function, total]`. The rule is its
single unconditional defining equation. It expands a named postcondition term
to a tuple containing the already defined `sumInts` and `productInts`
summaries. It is therefore a named proof-term/macro definition under the
classification contract.

This conclusion also follows from the frozen operational semantics:

1. The program module registers the `sum_product` closure and invokes it on the
   input value.
2. The closure body evaluates `TupleExpr(Call(sum, numbers),
   Call(prod, numbers))`.
3. Lookup returns the input `PyList(IS)`.
4. The two call rules return `PyInt(sumInts(IS))` and
   `PyInt(productInts(IS))`.
5. The tuple evaluator constructs exactly the value named by
   `expectedSumProduct(IS)`.
6. The base and step rules for `sumInts` and `productInts` give the specified
   empty results `0` and `1` and ordinary recursive sum/product behavior.

The proof-local rule does not match a configuration cell, invocation,
evaluation step, binding, continuation, or state transition, so it is not an
`OPERATIONAL_RULE` or operational bridge. Stage 1 does not first prove this
same rule in a module that omits it, so it is not a
`PROVED_DERIVED_LEMMA`. It asserts no auxiliary arithmetic fact and is simply
the defining expansion of the postcondition name, so it is not a
`DOMAIN_LEMMA`. It has no `simplification` attribute.

The independently reconstructed domain-lemma set is therefore genuinely empty.
The Stage 3 classification and rationale are relevant to the source program and
postcondition and are accepted.

Evidence:

- `evidence/02_frozen_sources_and_discovery.log`
- `evidence/31_stage4_mapping_judgment.log`

## Recorded hash audit

The signed resolution digest was recomputed using its canonical JSON contract.
Every launcher-recorded artifact hash was then recomputed:

| Artifact | Recomputed and recorded SHA-256 |
|---|---|
| Stage 1 workspace tree | `65461e9d38e144f5c6fb7e3d5b64c3b53d169b09bcbe625f8113e743f31b72a3` |
| Stage 1 export tree | `371cde27d62c71b300d9febf459275aa9d3e14e3013635e53cc44e7753a4e219` |
| Stage 3 discovery manifest | `d529a4c1e08a7455591481e774b5eda00b9e800038dd70d1d0d204f98fac84ed` |
| Selected Stage 2 K audit tree | `a0b84a7941d5fa39430955d457d3c29e895e6d0bea63c220360a8de21b03cec2` |
| Selected Stage 4 generation tree | `9ae1580e8db0457cb6fe5250bd7c5f1aaa55a2a8a2df44332623e31566269bc7` |
| Producer-source bundle tree | `363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0` |
| Generated Lean project tree | `1599353254d79bd4c6a13fe8063d91d5ba1e6900df86e943671f14dcb4377a29` |

The recorded Lean workspace and invocation hashes are both correctly `null`.
Every individual Stage 1 source hash also matches the signed map. The generator
and input manifests, export result, obligation-map hash, trust-inventory hash,
Stage 1 provenance, Stage 3 provenance, inventory provenance, and generated
tree hash are mutually exact.

Evidence: `evidence/09_hashes_and_producer_provenance.log`.

## Deterministic Stage 4 mapping and target identity

The complete independently judged Stage 3 partition maps as follows:

- `definitions`: exactly the reconstructed `expectedSumProduct` rule;
- `operational_rules`: empty;
- `proved_derived_lemmas`: empty; and
- `DOMAIN_LEMMA` source rules: empty.

The input manifest records exactly that partition and the exact summary
signature `expectedSumProduct : Ints → PyVal`.

The generated `obligation-map.json` is exactly:

```json
{
  "obligations": [],
  "schema_version": 3,
  "source_rules": [],
  "trust_parameters": []
}
```

Its SHA-256
`cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`
matches the generator manifest. Thus the ordered source-rule/obligation
bijection is exactly `[] ↔ []`: it has no omissions or duplicates because the
true domain set is empty. With no obligations there are no irrelevant,
weakened, or vacuous conjuncts.

The expected generated target is `null`. Independent source scanning found no
`targetStatement` declaration. The generator manifest, signed audit input,
recorded preflight, trusted target parser, and exact target-construction
function all agree that the fixed target is absent. This is the required target
identity for `KLEAN_NO_OBLIGATIONS`.

Evidence:

- `evidence/06_stage4_manifests.log`
- `evidence/29_target_and_stage5_absence.log`
- `evidence/31_stage4_mapping_judgment.log`

## Trusted preflight rerun

I reran `tools.klean_preflight.check_generation` with
`PYTHONPATH=/reference` and exactly these semantic inputs:

- `/reference/k-proof`;
- `/reference/lemma-discovery.json`;
- `/reference/klean-generation`; and
- `/reference/klean-toolchain.lock.json`.

The initial run reached Lake but failed before project compilation because this
audit sandbox hides `/proc/<pid>/exe`, which Lean 4.22 uses to locate its
installation. The raw failure is retained in
`evidence/10_stage4_preflight_rerun.log`, with diagnosis in evidence files
11–26.

To complete the required check, I compiled the narrow
`evidence/app_path_shim.c`. It intercepts only `readlink`/`readlinkat` requests
for `/proc/*/exe` and supplies the path in the already pinned Lean 4.22
toolchain directory. It does not alter the generated project, producer inputs,
Lean/Lake binaries, declarations, or build output. Its source SHA-256 is
`24f86516e4fe18855b94f15c13634ed03fc379bb68bf48dcee1f385deda351ea`.
The shim exposed the pinned Lean binary as version 4.22.0, commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, exactly matching the lock.

Using the trusted preflight's supported `run_command` hook solely to apply that
sandbox workaround, the rerun returned:

- status: `KLEAN_NO_OBLIGATIONS`;
- `lake clean`: exit 0, empty output hash
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`;
- `lake build`: exit 0, output hash
  `91173c4611c2c6d1f4c648f6763ec5f6f18ea21a8449a3c5403786e93c1a0c79`;
- obligation count: 0;
- target: `null`;
- designated sorry count: 0; and
- trust declaration count: 44.

The returned diagnostics and hashes exactly match the selected Stage 4
preflight. The 44 generated executable/runtime trust declarations match
`trust-inventory.json`; the preflight independently rejects proposition trust.
There is no target theorem or Stage 5 proof that could depend on those
declarations in this classification-only result.

Evidence:

- `evidence/27_app_path_shim_build_and_probe.log`
- `evidence/28_stage4_preflight_rerun_with_shim.log`

## Final judgment

The Stage 3 inventory and classification are complete and mathematically
correct. The true domain-lemma set is empty. Stage 4 preserves the exact frozen
provenance, maps that empty set bijectively to no obligations, generates no
target, and clean-builds under the pinned toolchain. The absence of a Stage 5
candidate is required by this mode and status. No concern or legitimacy failure
was found.

VERDICT: PASS
LEGITIMACY: LEGIT
