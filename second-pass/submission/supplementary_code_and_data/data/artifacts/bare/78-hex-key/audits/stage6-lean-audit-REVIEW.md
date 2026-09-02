# Independent audit: HumanEval 78-hex-key

## Audit scope and result

The launcher envelope is valid and has signed-resolution digest
`c79fa8e18bf1a58d3eabeed6b66b4eca310d27300be45495d49a9ad3d30feb52`.
Both `AUDIT_MODE` and `/audit-input.json` select `CLASSIFICATION_ONLY` for
condition `bare` and semantics mode `GENERATED_SEMANTICS`. There is no
`/candidate`, Lean workspace, Lean invocation, Stage 5 result, or generated
target. Accordingly, the Stage 5 proof, candidate-source, `Proof.final`, and
axiom-accounting checks are not applicable.

I treated the mounted Stage 1–Stage 4 files and prior reviews as untrusted
evidence. The findings below come from fresh reconstruction, source inspection,
hash recomputation, and a fresh run of the trusted preflight function.

## Producer-source provenance

Before judging Stage 4, I hashed the two mounted generation-time producer
files:

| File | Observed SHA-256 |
|---|---|
| `klean_export.py` | `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0` |
| `klean.py` | `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1` |

These values exactly match `generator-manifest.json` and
`source-manifest.json`. The generator image ID is consistently
`sha256:033f32de4a3cfe366b7391b1bf7da8bd1422f198853e93adb1a49f7eeb1e607c`
in both manifests; its hex component is also the producer-bundle path component
signed in `/audit-input.json`. The trusted launcher artifact hash for the
three-file producer bundle recomputes to
`7304929c6854f25574040a39ef0f06dba1e0f230199c2b63a00fe58ae83788ef`,
exactly the audit-input value. The bundle contains only the two producer files
and its source manifest. There is no producer-source infrastructure mismatch.

## Rule-inventory reconstruction and Stage 3 bijection

I ran the trusted `tools.k_rule_inventory.inventory_verification` on the frozen
`/reference/k-proof` workspace. `prove.sh` selects `VERIFICATION` as the main
module. The local verification-module closure inside `verification.k` is
exactly `["VERIFICATION"]`.

The reconstructed inventory has exactly one rule:

| Field | Reconstructed value |
|---|---|
| Module | `VERIFICATION` |
| Source span | `verification.k:10-16` |
| Attributes | `[]` |
| Normalized SHA-256 | `c3ab2878674aa2f645784b82238d257700a7250a3ecf4a8047ddb95328b1fdc9` |
| Source rule ID | `rule-c3ab2878674aa2f645784b82238d257700a7250a3ecf4a8047ddb95328b1fdc9` |

The whole canonical inventory hash is
`0c8f881f193c44642817eaf09f5ab9bb8b739a7da839af8355d6e83641d36f11`.
I also independently re-extracted lines 10–16, normalized whitespace, and
recomputed the same rule hash and ID.

`/reference/lemma-discovery.json` contains exactly this one identity, once, in
the same order, with the same inventory hash. The trusted Stage 3 boundary
validator reconstructed the same source text, span, attributes, hashes, and
identity. Thus there are no omitted, duplicated, extra, reordered, or
unaccounted rules.

## Independent classification judgment

The sole rule is correctly classified `DEFINITION`.

Immediately before it, `verification.k` declares
`primeHexCount(String) : Int` with `[function, total]`. The rule gives its
unconditional defining equation: the sum of
`countAllOccurrences(S, digit)` for the six digits `2`, `3`, `5`, `7`, `B`,
and `D`. This names the mathematical summary used in the postcondition. It
does not match or replace a program term, configuration cell, continuation,
binding, return, or other operational transition. It is therefore neither an
`OPERATIONAL_RULE` nor an operational bridge.

It is not a `PROVED_DERIVED_LEMMA`: it is a direct defining equation, and no
separate earlier proof is claimed or needed. It is not a `DOMAIN_LEMMA`: it
does not assert an auxiliary mathematical fact about pre-existing terms; it
defines the newly named summary itself. Its attributes contain no
`simplification`, so the simplification-class restriction is satisfied
vacuously.

The classification is also semantically adequate:

1. The source solution and frozen constructor program return five nested
   integer additions over six `num.count` calls for exactly those six
   one-character strings.
2. The frozen operational semantics binds `num` to the input string, binds
   attribute `count` to that receiver, evaluates each call as
   `countAllOccurrences(receiver, argument)`, evaluates `+` as `+Int`, and
   places the evaluated return value in `<result>`.
3. K's installed string semantics declares
   `countAllOccurrences` total and gives the expected zero/recursive equations;
   the backend implementation counts matches. For distinct one-character
   needles, summing the six results is exactly the number of prime hexadecimal
   digits.
4. The postcondition is `intVal(primeHexCount(S))`, so the definition is
   directly relevant to both the source computation and requested property.

The independent classification partition is therefore:

- `DEFINITION`: the one reconstructed rule;
- `OPERATIONAL_RULE`: none;
- `PROVED_DERIVED_LEMMA`: none;
- `DOMAIN_LEMMA`: none.

The true domain-lemma set is genuinely empty.

## Hash and manifest integrity

Fresh recomputation matched every signed hash used by this audit:

- Stage 1 pipeline tree:
  `504d481954e44c8dd2c8ac79fcbbb55b8f9f5d50280ec42cdd25a250d4e6161d`;
- Stage 1 export tree:
  `4b613f71450b9ca1c70e701a1bc166fa8c499c93f7f8443af60e68e3c34e3016`;
- Stage 3 manifest:
  `383ed686b5f335e48a9c55dfb1c734a36780cc99006e9e2e6508865716b16fc1`;
- selected Stage 2 artifact:
  `607dd616e5b0caf9e7ac0e211886fc08be7f4425f3b2b5ec6b0a9a69f83a814d`;
- selected Stage 4 artifact:
  `4a71e4eb73d6e370c36c6837203ff6f3bb512f61b37ffb45ac19f7cbaed3ba42`;
- generated project tree:
  `2732c4d83bbb9fb04d62dff3f568b2bd41ee8239b014122e562d7b3985151f43`;
- producer-source bundle:
  `7304929c6854f25574040a39ef0f06dba1e0f230199c2b63a00fe58ae83788ef`.

The per-file Stage 1 source-hash map also matches exactly. Generator provenance
binds the same Stage 1, Stage 3, inventory, producer, toolchain, and generated
tree values. The input-manifest `verification.k` hash is
`650a8ea4f81407b7b58a04b97a7a1884e5b3b47f046be50570afaef8f6a46ee6`,
matching the frozen file.

## Deterministic Stage 4 generation

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`
and exactly:

- frozen input `/reference/k-proof`;
- discovery manifest `/reference/lemma-discovery.json`;
- generation `/reference/klean-generation`;
- lock `/reference/klean-toolchain.lock.json`.

The fresh result is exactly equal as a JSON object to both
`/reference/klean-generation/preflight.json` and the signed
`stage4_preflight` in `/audit-input.json`. It reports:

- status `KLEAN_NO_OBLIGATIONS`;
- zero obligations;
- null target;
- zero designated sorries;
- 49 non-propositional generated trust declarations;
- `lake clean` exit 0 with empty-output hash
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`;
- `lake build` exit 0 with output hash
  `28ec64d2a30606bb98b87391dd4af956121339bf334149d0b0b7e2c42ef472a8`.

The exact source-rule/obligation chain is:

`independently classified DOMAIN_LEMMA []`
→ `input-manifest source_rules []`
→ `obligation-map source_rules []`
→ `obligations []`.

The obligation map has exactly the expected schema keys, an empty trust
parameter list, and SHA-256
`cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`,
matching the generator manifest. The trusted target parser returns `None`, the
expected target definition is `None`, and a raw scan finds zero
`targetStatement` declarations. The generator manifest, export result,
launcher target, and preflight target all agree. With no true domain lemmas,
there are no omitted, duplicated, irrelevant, weakened, or vacuous obligations
and no target change.

`KLEAN_NO_OBLIGATIONS` is therefore the correct deterministic Stage 4 result,
and the required absence of a Stage 5 candidate is confirmed.

## Audit-environment note

The first preflight attempt failed before compilation because this sandbox
reports namespace PIDs while exposing host `/proc`; Lean 4.22 consequently
could not resolve `/proc/<getpid()>/exe`. The failed output is preserved. I
used a local `LD_PRELOAD` compatibility shim that redirects only numeric
`/proc/.../exe` `readlink` calls to `/proc/self/exe`. `lean --version` then
reported the pinned commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, and the unchanged trusted
preflight passed with the exact original build-output hash. The shim source is
preserved in `evidence/proc-self-exe-shim.c`; it did not modify any frozen or
generated input.

## Evidence

Raw command transcripts and results are under `evidence/`:

- `audit-input-and-mode.log`;
- `producer-source-hashes.log`;
- `producer-bundle-artifact-hash.log`;
- `reconstructed-rule-inventory.log`;
- `stage3-bijection-validation.log`;
- `frozen-source-and-semantics.log`;
- `k-count-hook-semantics.log`;
- `hash_audit.py` and `hash-audit.log`;
- `stage4-manifests-and-target.log`;
- `fresh-klean-preflight.log` (initial environment failure);
- `lean-environment-shim-validation.log`;
- `fresh-klean-preflight-success.log`;
- `stage4_structure_audit.py` and `stage4-structure-audit.log`;
- `proc-self-exe-shim.c`.

VERDICT: PASS
LEGITIMACY: LEGIT
