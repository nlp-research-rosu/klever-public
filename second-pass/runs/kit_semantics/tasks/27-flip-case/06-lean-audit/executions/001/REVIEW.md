# Independent Stage 3–4 audit: HumanEval 27-flip-case

## Scope and result

I independently audited problem `27-flip-case`, condition `kit-semantics`,
semantics mode `SUPPLIED_SEMANTICS`. Both `AUDIT_MODE` and the signed
`/audit-input.json` resolution select `CLASSIFICATION_ONLY`. Accordingly,
Stage 5 is not in scope for this run, and the required Stage 5 inputs are
absent: `lean_workspace`, `lean_invocation`, `stage5_result`, and the fixed
target are null, and `/candidate` does not exist.

The Stage 3 classification is complete and mathematically appropriate. The
true local domain-lemma set is genuinely empty. The deterministic Stage 4
result `KLEAN_NO_OBLIGATIONS` is therefore correct, with no generated target
and no Stage 5 project.

## Input and producer integrity

I treated every mounted artifact as untrusted evidence and recomputed its
bindings. The signed Stage 6 envelope validates, including
`resolved_input_sha256 =
09eda31efae10fc1b7a945ce60930f3ff3f06738bb1c89025e002fc550d5eb28`.
All audit-input tree hashes match their mounted inputs:

- Stage 1 pipeline tree:
  `5b70c5e08d1887218f0001526d74dd4d599dcc6037a144818bde83fd6ea6bd8c`
- Stage 1 export tree:
  `82d7cf8eaaa88f794130c35824c0c1c6e7cebb8cd3574bf0098d4415a4f50c26`
- Stage 2 audit tree:
  `88143421945829fc12411eca2ee9f1561135cc4f6d5279611f6a9172adbd47f5`
- Stage 3 manifest:
  `e13c01259eb807dd465c4db3e29a0727d9ce0eb8df88d145e8977e70f5b7fcf3`
- Stage 4 publication tree:
  `bab3d1eb85788b1f6a633bc3928f58ee791c00a4d40cc18535504f3e5cd682d1`
- Generated project:
  `3209de0e4f3498631c1ca838864aaa96ad309dd84855f2bb0b879e1eb9a24c46`
- Producer-source bundle:
  `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`

The complete Stage 1 source-hash map has exactly 772 entries. I found no
missing files, unexpected files, or content-hash mismatches.

Before judging Stage 4, I directly hashed the two mounted generation-time
producer files:

- `klean_export.py`:
  `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07`
- `klean.py`:
  `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d`

Those hashes match both `source-manifest.json` and
`generator-manifest.json`. The producer bundle contains exactly those two
sources plus its source manifest. The immutable generator image ID is
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`
in the generator manifest and source manifest, and it matches the image-key
component of the producer-source path signed into `/audit-input.json`.
Therefore there is no producer-provenance `AUDIT_ERROR`.

The full recomputation is recorded in
`evidence/02-hash-verification.log`, with its executable checker in
`evidence/verify_recorded_hashes.py`.

## Rule-inventory reconstruction and Stage 3 bijection

I ran the trusted `tools.k_rule_inventory.inventory_verification` against the
frozen `/reference/k-proof` workspace. `prove.sh` selects `VERIFICATION` as
the main module. The trusted lexical closure algorithm reconstructs only
modules defined locally in `verification.k`; its closure is exactly
`["VERIFICATION"]`.

The frozen file is only:

```k
requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY
endmodule
```

There are no local rule sentences. Consequently there are no source spans,
normalized rule hashes, or `source_rule_id` values to omit, duplicate,
reorder, or alter. The independently reconstructed inventory is:

```text
verification_sha256 =
  ef48556fde781a8ca6e4e1986b701ccdf330897621c6658bd831ff4c17516ab4
verification_modules = ["VERIFICATION"]
rules = []
inventory_sha256 =
  4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945
```

I also independently reproduced the inventory hash as SHA-256 of the
canonical JSON bytes `[]`. The protected Stage 3 manifest has the same
inventory hash and exactly `rules: []`. Thus the comparison is a bijection in
both order and identity, with no unaccounted classifications. The trusted
Stage 3 contract validator independently returns empty `definitions`,
`operational_rules`, `proved_derived_lemmas`, and `domain_lemmas`.

Raw reconstruction and validator output are in
`evidence/03-rule-inventory.log`.

## Independent classification judgment

There are zero local inventory entries to classify. In particular:

- no local rule defines a summary, recurrence, macro, or named proof term;
- no local rule acts as an ordinary operational or observation rule;
- no local rule claims the stricter `PROVED_DERIVED_LEMMA` history;
- no local rule states mathematical content needing classification as a
  `DOMAIN_LEMMA`; and
- there are no local `[simplification]` rules, so the requirement that each
  such rule be a `DEFINITION` or `DOMAIN_LEMMA` is satisfied.

This empty classification is also correct mathematically, not merely
structurally. The source body is exactly:

```python
return string.swapcase()
```

The frozen spec asks fixed K execution to return `str(mapSwap(CS))`. The
supplied operational semantics itself contains:

```k
rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS))
```

and defines `mapSwap` by the empty and cons recurrences, with `swapC` handling
upper case, lower case, and the `owise` identity case. These are rules of the
frozen supplied `MPY` semantics, not proof-local extensions in the
verification-module closure. The postcondition repeats the exact operational
result; it does not assert an additional algebraic or human-facing property
such as involution, length preservation, or character classification that
would require a domain lemma. Therefore the true Stage 3 domain set is
genuinely empty.

Relevant frozen-source excerpts are in
`evidence/04-semantics-source-excerpts.log`.

## Deterministic Stage 4 generation

I reran the required call to
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and the
three mandated inputs. The first invocation exposed a sandbox-specific Lean
startup issue: Lean/libuv used the inner namespace PID to read
`/proc/<pid>/exe`, while the mounted `/proc` did not expose that entry. A
readlink trace confirmed the exact failure. I repaired only that process-path
lookup by interposing a redirect from numeric `/proc/<pid>/exe` to
`/proc/self/exe`; the source is preserved as
`evidence/proc_self_compat.c`. This did not modify any input, generator,
generated Lean source, proof term, or project file.

With that environment repair, the same trusted checker returned:

```text
status = KLEAN_NO_OBLIGATIONS
obligation_count = 0
target = null
designated_sorry_count = 0
trust_declaration_count = 41
stage1_workspace_sha256 =
  82d7cf8eaaa88f794130c35824c0c1c6e7cebb8cd3574bf0098d4415a4f50c26
stage3_discovery_manifest_sha256 =
  e13c01259eb807dd465c4db3e29a0727d9ce0eb8df88d145e8977e70f5b7fcf3
generated_tree_sha256 =
  3209de0e4f3498631c1ca838864aaa96ad309dd84855f2bb0b879e1eb9a24c46
```

Its isolated `lake clean` exited 0. Its isolated `lake build` exited 0 and
reproduced the recorded output hash
`d4435c1b43b543e476b83e9efbcd217521737b7299e839224ec513ecd3cad812`.
I also compared the generator manifest's complete toolchain object directly
with `/reference/klean-toolchain.lock.json`; they are exactly equal.
The initial failure, environment diagnosis, and complete successful returned
evidence are preserved in `evidence/05-preflight-initial-failure.log`,
`evidence/06-lean-environment-repair.log`, and
`evidence/07-preflight-rerun.log`.

I separately checked the Stage 4 mapping without relying on the preflight
conclusion:

- Stage 3 true `DOMAIN_LEMMA` rules: `[]`
- `input-manifest.json` source rules: `[]`
- `obligation-map.json` source rules: `[]`
- generated obligations: `[]`
- trust parameters: `[]`

This is an exact zero-to-zero ordered bijection. There are no duplicates,
omissions, irrelevant obligations, weakened formulas, or conjuncts—vacuous or
otherwise. `obligation-map.json` hashes to the value fixed in the generator
manifest:
`cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`.

The fixed target is absence of a target. The generator manifest, recorded
preflight, and signed audit input consistently report `target: null`; the
export result agrees that there are zero obligations. An independent scan of
every generated Lean file found no `targetStatement` declaration of any kind.
The generated `Lemmas.lean` contains only its import and an empty namespace.
Thus there is no changed, weakened, duplicated, or vacuous target.

The independent mapping and target check is in
`evidence/08-stage4-structure.log`, with its checker in
`evidence/verify_stage4_structure.py`.

## Stage 5

Stage 5 checks are intentionally not run. This is `CLASSIFICATION_ONLY`, the
true domain set is empty, Stage 4 generated no target, and `/candidate` is
absent. Running a proof build, `#print axioms Proof.final`, target-parameter
bridge analysis, or candidate token scan would require a proof candidate and
target that must not exist for this valid `KLEAN_NO_OBLIGATIONS` result.

## Conclusion

The protected Stage 3 manifest is a complete and correct classification of
the frozen local rule inventory. Producer provenance and all recorded hashes
are intact. Deterministic Stage 4 generation preserves the exact empty
domain-rule set as an empty obligation set, generates no target, and passes
the trusted mechanical preflight after a fully accounted sandbox environment
repair. No legitimacy defect or unresolved concern remains.

VERDICT: PASS
LEGITIMACY: LEGIT
