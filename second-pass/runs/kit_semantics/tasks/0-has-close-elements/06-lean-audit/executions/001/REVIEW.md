# Independent Stage 3–5 audit: `0-has-close-elements`

## Conclusion

The selected Stage 3 classification, deterministic Stage 4 generation, and
Stage 5 Lean proof pass this independent audit. The audit ran in
`CLASSIFICATION_AND_PROOF` mode with `SUPPLIED_SEMANTICS`. I did not rely on
the earlier Stage 2 opinion, Stage 3 rationales, Stage 4 PASS, Stage 5 success,
or candidate comments as authority.

## Input and producer integrity

The launcher mode in `AUDIT_MODE` and `/audit-input.json` agrees. Rehashing the
mounted inputs with the trusted digest implementations produced:

| Input | Recorded and observed SHA-256 |
|---|---|
| Stage 1 pipeline tree | `093b0555b87f7e222e1c37c9a425fe56482cbf9bdf3a7bfe71069bdddc0a106a` |
| Stage 1 export tree | `acf83dc5c18a945c7fef8cacd85c1074adbe544df5463e3c2ddc10f0eba2cc2e` |
| Stage 3 discovery file | `36893417da13986eb5865bc738424129445ca8354a1d7d9277435d1adb5b9ba9` |
| Selected Stage 2 tree | `4ce7b90174dbdfc3791d6c55d2a66478f7d77bbdd0c19fb003cfb896465bf530` |
| Selected Stage 4 tree | `61a4ce840ea78be495609341c2da8c1821527820544bdd681c9ea9d183d91178` |
| Producer-source bundle | `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e` |
| Generated Lean tree | `2cb5dfda0ff1e32b63762daad4089db931da09efd56ab09b6dfb553fbb6bea37` |
| Stage 5 candidate tree | `acee161091ba7c7b00b8dfc8502efbb3290536d749efa750fcfdc59c4ce3e159` |

All 793 launcher-recorded Stage 1 file hashes were present and equal, with no
extra or missing files.

Before judging Stage 4, I hashed the mounted producer files:

- `klean_export.py`:
  `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07`
- `klean.py`:
  `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d`

These values agree exactly with both `generator-manifest.json` and
`/reference/generation-tools/source-manifest.json`. The source manifest image
ID, generator provenance image ID, and the image-key component recorded in
`/audit-input.json` all identify
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`.
The bundle contains exactly the two producer files and its source manifest.
There is therefore no producer-source infrastructure error.

The pinned tools were K 7.1.293 and Lean 4.22.0 at commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, matching the lock and generator
manifest.

## Canonical rule reconstruction

I ran the trusted `tools.k_rule_inventory.inventory_verification` directly on
the frozen Stage 1 workspace. The selected local module is `VERIFICATION`;
its local verification-module closure contains only that module. The tool
reconstructed ten rules in source order from `verification.k`, with
verification source hash
`45f7bdfd11b35730795fc6e23cb8b2eb64c73b3cb683764550d7f68b0e519a8a`.

The reconstructed canonical inventory hash is
`01ad50c6b45f648f63d18deb81f4a81f3c96e68c877d124351958a5b6a7d6c75`.
It equals the protected Stage 3 value. The comparison found ten versus ten
rules, identical identity order, no duplicate identity in either side, no
omission, and no extra identity. Each source span, normalized hash, and
`source_rule_id` below comes from the frozen source reconstruction:

| Lines | Normalized SHA-256 | Independent class | Reason |
|---:|---|---|---|
| 8 | `dc6da0bab4bb59bc7bc1f84e094e20bfb08eaabdfb63f4029d3dcd8d203f8b96` | `DEFINITION` | Empty `allFloats` base equation. |
| 9 | `9e498a0552e6771e74565791899fe40f49d034087ac6ccb7f8bd852cdd51a7d5` | `DEFINITION` | Constructor recurrence for `allFloats`. |
| 13 | `1ccd7704e0d880500af6b7bbc2f25393776cecf9972be7883d55005af75dba48` | `DEFINITION` | Names the `pairNear` proof term as `floatLt(absF(subF(...)), T)`. |
| 16 | `3b93d4976b7182c91d2a2f37ff4a4b4aeb87b2cae0b70e16583b7653e50137f0` | `DEFINITION` | Float branch of the named `asFloat` projection. |
| 17–18 | `67ea2306e1ec02d05f832f6fc3d1c1df7b074395565220a88d327b4244b3dfd5` | `DEFINITION` | Guarded non-Float totalization branch of `asFloat`. |
| 21–23 | `fc66c723d628ad8e811c12c35a08f3b4345486c0dfef2593966c9dbe4c211ecf` | `DOMAIN_LEMMA` | Guarded simplification for the imported `applyBin` symbol. |
| 28 | `906f23375bc3037477bb4865bd82b1acd088f6c92c84fba22886fbcdb4f2e980` | `DEFINITION` | Empty `rowAcc` base equation. |
| 29–35 | `4e163f4813de9404688e2d18f89122e640ce937ff1c79d5b2ab228fe5b081efb` | `DEFINITION` | Structurally descending `rowAcc` recurrence. |
| 40 | `9f5405faf27ef5ff3d4f3497a2b19c0aae403765801d6da99715fd17f685269c` | `DEFINITION` | Empty `outerAcc` base equation. |
| 41–43 | `69dccad157e90642e223828bfe9d6780f595e93cc0d6e5f205e123d520ccb3da` | `DEFINITION` | Structurally descending `outerAcc` recurrence. |

The nine definitions genuinely introduce summaries, recurrences, or named
proof terms. None is an ordinary program execution rule. The sole
`[simplification]` sentence is correctly a domain lemma rather than a
definition or operational rule: its head is the already imported
`applyBin("-", A:Val, B:Val)`, and it supplies the guarded, dynamic-sort
elimination

```text
isFloat(A) andBool isFloat(B)
  => applyBin("-", A, B) = subF(asFloat(A), asFloat(B)).
```

It is not a `PROVED_DERIVED_LEMMA`. Stage 1 first proves only
`applyBin("-", A:Float, B:Float) => subF(A,B)` in the bridge-free
`CONNECTION-VERIFICATION` module. That is not the exact Val-typed,
`isFloat`-guarded, `asFloat`-bearing rule later installed in
`VERIFICATION`.

The domain lemma is materially relevant. The frozen solution computes
`number1 - number2`; both loop variables are drawn from the input list as
`Val`, while the proof precondition conveys their Float status through
`allFloats`. The inner-loop claim summarizes the same subtraction through
`rowAcc` and `pairNear`. Thus the rule connects the source expression and
postcondition summary; it is not an unrelated mathematical fact. There are
no independently valid `OPERATIONAL_RULE` or `PROVED_DERIVED_LEMMA` entries.
The protected Stage 3 classifications agree with this independent result.

## Deterministic Stage 4 generation

I reran:

```text
PYTHONPATH=/reference python3
  tools.klean_preflight.check_generation(
    /reference/k-proof,
    /reference/lemma-discovery.json,
    /reference/klean-generation,
    toolchain_lock=/reference/klean-toolchain.lock.json)
```

The returned result is `PASS`, with one obligation, zero designated sorries,
44 inventoried generated trust declarations, and generated tree hash
`2cb5df...`. Its temporary `lake clean` and `lake build` both exited zero.
The build output SHA-256 is the recorded
`68465adc2ad9e681ecb9f5616497d4aafd307297559c9f7f40562fb4687a8512`.

The audit container exposes a mismatched nested PID namespace, so the first
attempt failed before project elaboration when Lean tried to resolve
`/proc/<getpid>/exe`. I preserved that output. A narrow, auditable
`LD_PRELOAD` shim rewrote only numeric `/proc/.../exe` `readlink` requests to
the working `/proc/self/exe`. With that environment-only correction, the
same trusted function completed and reproduced the recorded output hash.
The shim does not alter Lean terms, source, elaboration, or kernel checking.

The independently determined domain set contains exactly
`rule-fc66c723...`. `obligation-map.json` contains exactly one obligation
with that ID and no duplicate. Its source span is 21–23, normalized hash is
the reconstructed hash above, and its inventory and discovery hashes agree.
The source-rule list is byte-for-byte the Stage 4 input-manifest list. The
conjunct hash recomputes to
`afb5efe1f23c9e67a9604e5402bc22b84f1c887f606462d7a04b655ac6602a85`.
All five parameter binding hashes independently recompute. The obligation-map
file hash recomputes to
`2e40a4d590b7d38254051cd042d1e2d1a03774f0fa6ea61b1ecbd578316be05a`.

Mathematically, the generated conjunct is the same guarded equation as the K
rule: for arbitrary `A B : SortVal`, if both dynamically inject as Float, the
`"-"` application equals the Float injection of
`subF(asFloat A, asFloat B)`. It preserves the strict guard, operator,
argument order, result injection, and equality. It does not add an irrelevant
conjunct, weaken the result, or duplicate an obligation.

The target is the exact one-conjunct definition generated from that map:

- declaration:
  `Klean0HasCloseElements.Lemmas.targetStatement`
- definition SHA-256:
  `a33436ffed8ae0222db28a26e8ed02aeb73958a50865f3942c7dfda2033866bc`
- applied-statement SHA-256:
  `283d6bb5a1a47c958a67b623afc4ca89fe3e4ebd664caff475fd5298e48a717d`

The recomputed target object equals the generator manifest, recorded
preflight, and `/audit-input.json`. The target is not vacuous under the
candidate meanings: Float injections for 5.5 and 2.0 satisfy the guard, and
an uncoordinated addition mutation produces 7.5 while the required
subtraction side produces 3.5.

## Fresh Stage 5 build and target identity

I created `/tmp/audit-work/proof-audit.2wTFR1`, copied the generated project
into it as `Base`, and copied the candidate at the project root. I then ran
both required commands:

```text
lake clean
lake build
```

Both exited zero; the complete terminal output is preserved. After the clean
build, all 12 immutable generated source/metadata files in `Base` still match
the selected Stage 4 generation byte-for-byte. The rebuilt target object
still has the exact declaration, statement, parameter bindings, and hashes
listed above.

The candidate has two Lean source files, `Proof.lean` and `lakefile.lean`.
Static inspection found no `sorry`, `admit`, `unsafe`, new `axiom`, or new
`opaque`, and no declaration named `targetStatement`. The package imports the
fixed `Base`; it neither replaces nor shadows the generated target.

Lean reports the type of `Proof.final` as exactly:

```text
Klean0HasCloseElements.Lemmas.targetStatement
  Proof._andBool_
  Proof.«applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val»
  Proof.«asFloat(_)_VERIFICATION_Float_Val»
  Proof.isFloat
  Proof.subF
```

This is the fixed applied statement from the manifest, not a copied,
weakened, or separately declared proposition.

## Axiom accounting

Running Lean with `#print axioms Proof.final` produced exactly:

```text
'Proof.final' depends on axioms: [propext, Classical.choice, Quot.sound]
```

These are Lean's standard logical/kernel trust dependencies. No generated
Klean axiom from the 44-entry `trust-inventory.json` allowlist occurs in the
dependency list. There is no `sorryAx`, no automatic axiomatization, no
designated or other sorry, and no unreconciled dependency. The generated
inventory still exactly accounts for generated source-level trust
declarations; none is used to prove `Proof.final`.

## Operational-bridge audit

I printed the elaborated candidate definitions and compared each one with its
manifest `kore_symbol`, bound source rule, frozen K source, and operational
meaning:

| Target parameter | Candidate meaning | Independent judgment |
|---|---|---|
| `_andBool_` | `lhs && rhs` | Exact K Boolean conjunction; all four ground cases agree. |
| `applyBin` | On `"-"` and two Float-injected `SortVal`s, returns the Float injection of `lhs - rhs`. | Exact match for the complete guarded source-rule domain and fixed Float dispatch. Other candidate branches are outside this obligation; the partial-symbol fallback is unreachable under its guard and contributes nothing to the proof. |
| `asFloat` | Extracts a Float injection; otherwise returns `0.0`. | Exact two-branch definition at verification.k lines 16–18. Float 5.5 maps to 5.5; an Int maps to 0.0. |
| `isFloat` | True exactly for a singleton `SortK` containing a Float-injected K item; false otherwise. | Exact generated sort-predicate behavior. Float, Int, and nonempty-continuation boundary witnesses returned true, false, and false. |
| `subF` | `lhs - rhs` on Lean `Float`. | Implements the concrete operational twin `subF(F1,F2) => F1 -Float F2`; the K symbol remains opaque only to symbolic evaluators. |

Ground Lean evaluations gave `5.5 - 2.0 = 3.5`,
`-1.25 - 2.75 = -4.0`, and `0.0 - 0.0 = 0.0`, both through `subF` and the
relevant `applyBin` branch. A separate frozen-K `krun` program asserted the
same three computations and terminated at `.K`, `NoExc`, exit code 0.

I also tested the theorem's sensitivity rather than inferring honesty from a
clean build:

1. Replacing `isFloat` with constant false makes the implication provable
   vacuously. That counterfactual compiled, while the submitted `isFloat`
   has explicit satisfiable Float witnesses and matches the K sort predicate.
2. Coordinating wrong addition interpretations for both `applyBin` and
   `subF` also proves the relational target. That counterfactual compiled,
   demonstrating that agreement between the two parameters alone is
   insufficient.
3. Holding the submitted subtraction `subF` fixed while changing `applyBin`
   to addition produced the concrete disagreement `7.5 != 3.5`.

These counterfactuals expose the exact shortcuts the operational audit must
reject. The submitted definitions do not take them: each load-bearing
definition independently implements the frozen K meaning on the complete
source-rule domain. `Proof.final` is therefore non-vacuous and is an honest
proof of the fixed generated obligation.

## Evidence

- Integrity, producer comparison, all Stage 1 source hashes, and full
  reconstructed inventory:
  `evidence/01_integrity_inventory.log`
- Initial preflight environment failure and successful trusted retry:
  `evidence/02_preflight.log`, `evidence/02_preflight_retry.log`
- Complete fresh clean/build output:
  `evidence/04_lake_clean.log`, `evidence/05_lake_build.log`
- Exact `#print axioms` output and reconciliation:
  `evidence/06_print_axioms.log`,
  `evidence/12_axiom_reconciliation.log`
- Independent obligation, binding, target, Base-copy, and forbidden-token
  checks: `evidence/07_stage4_target_static.log`
- Elaborated parameter definitions and exact `Proof.final`:
  `evidence/08_print_definitions_and_final.log`
- Lean operational witnesses and counterfactual mutations:
  `evidence/09_bridge_adversarial.log`
- Frozen-K operational witnesses:
  `evidence/10_k_operational_witnesses.mpy`,
  `evidence/10_k_operational_witnesses.log`
- Pinned versions, mode, and direct producer hashes:
  `evidence/13_versions_and_mode.log`

VERDICT: PASS
LEGITIMACY: LEGIT
