# Independent Stage 3/4 audit: `162-string-to-md5`

## Scope and result

This review independently audits condition `bare`, semantics mode
`GENERATED_SEMANTICS`, in launcher mode `CLASSIFICATION_ONLY`. I treated the
mounted candidate/provenance material, including the earlier Stage 2 review,
as untrusted evidence. I used the trusted rule-inventory and Klean preflight
code from `/reference/tools` and reconstructed the mathematical judgment from
the frozen K and Python sources.

The selected `KLEAN_NO_OBLIGATIONS` status is correct. The local
verification-module closure contains three rules; all three are genuine
definitions and none is a domain lemma. Consequently, the deterministic
Stage 4 source-rule set and obligation set are both genuinely empty, there is
no generated theorem target, and there is correctly no Stage 5 candidate.

## Producer authentication

I authenticated the Stage 4 producer before judging the generation:

| Artifact | Recomputed SHA-256 |
|---|---|
| `klean_export.py` | `235473b1324d2b203cb2a49ab94e36fb7c300084d506a57fca2228381f1bdec0` |
| `klean.py` | `ddec66db87398459ff0c2b5aad7121fe1029b58b8d576db4203c68bf5b647d13` |
| Producer-source tree | `363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0` |

The two file hashes exactly match both
`/reference/generation-tools/source-manifest.json` and
`generator-manifest.json`. The immutable image identity is consistently
`sha256:e18301a8220fb0b62fabf56feffcb5e621049daa7c7a0b79eacb60cae5e57fda`
in the source manifest and generator manifest, and the same digest is the
terminal component of the producer-source path signed by `/audit-input.json`.
The producer bundle has exactly the two producer files and its source
manifest. See
[02_producer_authentication.log](/audit-output/evidence/02_producer_authentication.log)
and
[26_manifest_bijection_target_and_internal_hashes.log](/audit-output/evidence/26_manifest_bijection_target_and_internal_hashes.log).
There is no producer-provenance infrastructure error.

## Inventory reconstruction and bijection

The trusted inventory code reconstructed the local closure of the frozen
`verification.k` as the single module `VERIFICATION`. Its results are:

- `verification.k` SHA-256:
  `afca64be72fd24753aae22c1057194277333bb6ad164eeaf054358c84752f301`
- ordered closure: `["VERIFICATION"]`
- rule count: `3`
- canonical whole-inventory SHA-256:
  `39818e66dd0fd80a6b9e2b9d89112d133c1c29c20b6ebeb80609dc768a13a57f`

The reconstructed entries are:

| Order | Source span | Normalized SHA-256 / `source_rule_id` | Independent class |
|---:|---|---|---|
| 1 | `verification.k:9-21` | `94c25ab8fa55e4a32d6644c52fa3be49b288dadeb7d44eed8cd9c05847112219` / `rule-94c25ab8fa55e4a32d6644c52fa3be49b288dadeb7d44eed8cd9c05847112219` | `DEFINITION` |
| 2 | `verification.k:24-27` | `355c7965a40e332089142b46c25dec21f1db8e383c1fc3f20a6de02381621f97` / `rule-355c7965a40e332089142b46c25dec21f1db8e383c1fc3f20a6de02381621f97` | `DEFINITION` |
| 3 | `verification.k:31` | `0e35f967958921b2696228779a3b13e82321fcfb461b86b6c3cbbee2e6ddf007` / `rule-0e35f967958921b2696228779a3b13e82321fcfb461b86b6c3cbbee2e6ddf007` | `DEFINITION` |

The protected Stage 3 manifest contains those exact three identities in that
exact order. Both identity lists are unique and equal; there are no
omissions, duplicates, extras, reorderings, changed normalized identities, or
unclassified rules. The manifest's inventory hash equals the independently
recomputed hash. The full reconstructed text, attributes, spans, and hashes
are in
[03_reconstructed_rule_inventory.log](/audit-output/evidence/03_reconstructed_rule_inventory.log);
the explicit ordered bijection is in
[05_stage3_bijection.log](/audit-output/evidence/05_stage3_bijection.log).

None of the three local rules has a `simplification` attribute. Thus there is
no local simplification rule assigned to a forbidden class.

## Independent classification judgment

I classified behavior rather than accepting names or comments:

1. `solutionBody` is a constructor-tree macro. Its right-hand side is the
   exact `Return(IfExp(...)) .Stmts` body translated from the frozen
   `solution.py`/`solution.mpy`. It names syntax; it neither states a
   mathematical fact nor skips a fixed operational transition.
2. `solutionProgram` is the corresponding program-AST macro. It expands to
   the frozen module containing `Import("hashlib")` and the
   `string_to_md5` function bound to `solutionBody`. Again this defines a
   named constructor tree rather than execution behavior.
3. `expectedMd5(S) => pyString(md5String(S))` is a named proof-result
   definition. On the nonempty branch, the fixed semantics evaluates
   `text.encode()` to `pyBytes(utf8Bytes(S))`, applies `hashlib.md5`, and
   evaluates `hexdigest` to `pyString(md5Bytes(utf8Bytes(S)))`.
   `md5String(S)` is defined in the frozen semantics as exactly
   `md5Bytes(utf8Bytes(S))`. The rule is therefore a transparent name for
   the operational result, not an additional MD5 theorem or an operational
   bridge.

There is no `OPERATIONAL_RULE` in the local closure: the ordinary loading,
invocation, evaluation, comparison, attribute, call, UTF-8, and MD5
transitions live in the imported frozen `SEMANTIC` module, not in a local
proof rule. There is no `PROVED_DERIVED_LEMMA`, and Stage 1 contains no
two-phase artifact that first proves one of these exact rules without it and
then imports it later. Most importantly, there is no `DOMAIN_LEMMA`.

The frozen source and complete numbered K sources are recorded in
[04_frozen_sources.log](/audit-output/evidence/04_frozen_sources.log).
Independent executions give `None` for the empty input and the expected
digests for `Hello world` and `abc`; both the exact Unicode-literal claim and
the symbolic nonempty claim close with `#Top`. See
[27_operational_witnesses.log](/audit-output/evidence/27_operational_witnesses.log)
and
[28_kprove_definition_linkage.log](/audit-output/evidence/28_kprove_definition_linkage.log).

One diagnostic detail does not change the classification: injecting `π`
through `krun -cTEXT` produced an input shown as the two byte-valued
characters `"\xcf\x80"` and therefore a double-encoded digest. The exact
K-source literal `"π"` in the frozen `unicode-utf8` claim closes to the
correct UTF-8 digest. This isolates the discrepancy to the concrete
configuration-variable front end used by that one witness, not to the
`expectedMd5` definition or the formal K claim.

## Signed hashes and manifest integrity

I recomputed every signed resolution/artifact hash using the trusted tree
algorithms:

| Signed artifact | Recomputed hash |
|---|---|
| Stage 1 workspace tree | `ef203d9121a51f9f2f8f58a9128ca78d47cc724be61b158573e4d8c364a2134e` |
| Stage 1 Klean export tree | `d8cdfc2baef9b71de8c47da8ae597d6e812ab592dfd0dfe1ec87184f2d89a071` |
| Stage 2 audit tree | `b3f19ca142b6124a3b4a5776ffb2457673980ff404300ed16ff0fc0114b7e36c` |
| Stage 3 manifest | `2c3b32d3f32207cf7b0e231bc6a3a038e60233607c5a255aa7ffe2366a1c18ab` |
| Stage 4 generation tree | `9b1ec380729eb632d0e612859e0854c4e7d8bd799edf6bdfd57aafa59a78c23d` |
| Generated Lean tree | `1cf83f4be57e92a2e984391f5212a4dbfe5feb50c44745022fc025d549803149` |
| Producer-source tree | `363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0` |

Both selection artifact hashes match. All 317 per-file Stage 1 hashes match
bijectively, with no missing, extra, or changed path. The signed resolution
digest recomputes to
`92a922e41c03c52822e9e5c6a6300ea48c8e32b282048171cce95cb7eff0a024`.
See
[25_audit_input_hash_recomputation.log](/audit-output/evidence/25_audit_input_hash_recomputation.log).

I also independently reconciled the generator's obligation-map hash, trust
inventory hash, generated-tree hash, frozen-input hash, discovery hash,
verification hash, inventory hash, producer hashes, and pinned toolchain.
The original preflight diagnostic output hashes equal the hashes of their
complete recorded output tails. All checks are enumerated in
[26_manifest_bijection_target_and_internal_hashes.log](/audit-output/evidence/26_manifest_bijection_target_and_internal_hashes.log).

## Preflight rerun

I invoked `tools.klean_preflight.check_generation` with
`PYTHONPATH=/reference` and the required frozen workspace, discovery
manifest, generation, and toolchain lock.

The first invocation reached the checker but the audit sandbox's PID
namespace made Lean's lookup of `/proc/<pid>/exe` return `ENOENT`, so
`lake clean` could not identify its installation. This is captured in
[06_klean_preflight_rerun.log](/audit-output/evidence/06_klean_preflight_rerun.log)
and the syscall probe in
[21_lean_path_probe.log](/audit-output/evidence/21_lean_path_probe.log).

I used the minimal compatibility shim preserved as
[lean_path_probe.c](/audit-output/evidence/lean_path_probe.c). It changes only
that failed PID-specific `readlink` to `/proc/self/exe`; all other calls pass
through and are logged. With the shim, the pinned compiler identifies itself
as Lean `4.22.0`, commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, and a fresh copied generated
project passes both `lake clean` and `lake build`. The independent build is
in
[22_lean_sandbox_compatibility.log](/audit-output/evidence/22_lean_sandbox_compatibility.log).

The required checker rerun then returned:

- status: `KLEAN_NO_OBLIGATIONS`
- frozen/Stage 1 export hash:
  `d8cdfc2baef9b71de8c47da8ae597d6e812ab592dfd0dfe1ec87184f2d89a071`
- Stage 3 manifest hash:
  `2c3b32d3f32207cf7b0e231bc6a3a038e60233607c5a255aa7ffe2366a1c18ab`
- generated tree hash:
  `1cf83f4be57e92a2e984391f5212a4dbfe5feb50c44745022fc025d549803149`
- obligation count: `0`
- target: `null`
- designated sorry count: `0`
- trust declaration count: `44`
- `lake clean`: exit `0`
- `lake build`: exit `0`

The complete returned evidence is
[23_klean_preflight_rerun_with_sandbox_shim.log](/audit-output/evidence/23_klean_preflight_rerun_with_sandbox_shim.log).
The shim does not edit any mounted input or generated source and cannot add,
remove, weaken, or prove a Lean proposition.

## Obligation bijection and target identity

My independently classified domain-rule ID list is `[]`.
`input-manifest.json` records `source_rules: []`;
`obligation-map.json` records `source_rules: []`, `obligations: []`, and
`trust_parameters: []`. These ordered lists are equal and duplicate-free.
All three Stage 3 definitions are copied exactly into the input manifest,
while its operational and proved-derived lists are also correctly empty.

With zero obligations:

- `klean_export.expected_target_definition(obligation_map)` returns `None`;
- `klean_export.target_statement(generated)` returns `None`;
- the generator manifest, saved preflight, and audit input all record
  `target: null`;
- `Klean162StringToMd5/Lemmas.lean` contains only imports and an empty
  namespace; and
- `/candidate` is absent, while every Stage 5 launcher field is `null`.

Thus there is no omission, duplicate obligation, weakened or irrelevant
conjunct, vacuous conjunct, changed target, or hidden target declaration.
The generic generated project contains 44 inventoried hook declarations, but
there is no proposition or proof for them to discharge in this mode. The raw
generation structure and trust inventory are in
[24_generation_structure_and_obligations.log](/audit-output/evidence/24_generation_structure_and_obligations.log).

## Stage 5 applicability

Stage 5 proof checks are not applicable. The launcher-selected mode is
`CLASSIFICATION_ONLY`; the genuinely empty domain set requires no generated
target; `/candidate` is absent; and the audit input contains no Lean
workspace, invocation, target, or Stage 5 result. Running `Proof.final`,
axiom accounting for it, or parameter bridge tests would fabricate a proof
target that the authenticated generator did not produce.

## Conclusion

The Stage 3 classification is complete, ordered, hash-bound, and
mathematically correct. The authenticated deterministic Stage 4 generation
is bijective with the independently empty domain-lemma set and correctly
produces neither obligations nor a target. The Stage 5 absence is required.
No issue affecting classification or legitimacy remains.

VERDICT: PASS
LEGITIMACY: LEGIT
