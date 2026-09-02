# Independent audit: HumanEval `116-sort-array`

## Scope and result

This audit covers condition `semantics`, semantics mode
`SUPPLIED_SEMANTICS`, for:

1. the protected Stage 3 rule classification;
2. the selected deterministic Stage 4 K-to-Lean generation; and
3. Stage 5 only if the launcher selected proof mode.

Both `AUDIT_MODE` and the signed `/audit-input.json` resolution say
`CLASSIFICATION_ONLY`. The signed Stage 5 workspace and invocation hashes are
`null`, the selected Stage 4 target is `null`, and `/candidate` is absent.
Therefore no Stage 5 proof, target-parameter bridge, or axiom audit is
applicable in this run.

The independently reconstructed domain-lemma set is empty. The selected
`KLEAN_NO_OBLIGATIONS` generation is therefore mathematically appropriate,
contains no generated target, and requires no Stage 5 candidate.

## Input and producer authentication

The signed audit-input envelope validates with resolved-input SHA-256
`8d293a902dc2e10bb4da7e05cd27cc445052b242a937e80ec909c68081bd77fe`.
All recorded mounted-input hashes were recomputed with the trusted hash
implementations and matched, including:

| Binding | Recomputed value |
|---|---|
| Stage 1 workspace artifact tree | `53cc1c94f09f97079dbc8961f2c4a7f0371e52bc29629175077d2f941d32cfd9` |
| Stage 1 deterministic-export tree | `ccc000c78b9101630b41e011d9fa53465982e83efbdb289ca5ca599a60e436bb` |
| Stage 3 manifest file | `14c99832bbb94a7c34e73705e1f78b35bd614af09aae5d8037593c30bcdd3ec5` |
| selected Stage 2 audit tree | `30e2a863212b2ca023efa0904947fa2d1457aeee23f8e9a946622bbc643bacf6` |
| selected Stage 4 generation tree | `ea23555bf829f58db4335eeb54e1a3dc1a0740a846eb4f5c2abba8d8da0f396d` |
| generated project tree | `a5297aa66093a095ad19fb3a916910c94b488e0ac72d0bf2a566b4d092f8fcc3` |
| producer-source bundle tree | `55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c` |

Every per-file Stage 1 source hash also matches the signed
`stage1_source_hashes` map. The Stage 2 and Stage 4 selection hashes match
their recomputed artifact trees.

Before judging Stage 4, I directly hashed the immutable generation-time
producer sources:

| Producer | Recomputed SHA-256 |
|---|---|
| `klean_export.py` | `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0` |
| `klean.py` | `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1` |

Both values exactly match `source-manifest.json` and
`generator-manifest.json`. The bundle contains exactly those two sources plus
the source manifest. The generator image ID is consistently
`sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000`
in the source manifest and generator manifest; the same digest is the basename
of the producer-source path signed in `/audit-input.json`. There is no producer
provenance mismatch or infrastructure `AUDIT_ERROR`.

## Canonical inventory reconstruction

I ran the trusted `tools.k_rule_inventory.inventory_verification` over the
frozen `/reference/k-proof` workspace rather than trusting an earlier review.
The `prove.sh` main-module selection resolves to
`SORT-ARRAY-VERIFICATION`. Its verification-file-local closure contains only
that module: the imported `MPY` module is supplied from another file and is not
a local module in `verification.k`.

The reconstruction yielded:

- verification SHA-256:
  `545e6858013ff4c70613e0d4661ea47f3fc321553abee6e4273897549c4678f6`;
- nine rules, in source order;
- nine unique normalized hashes and `source_rule_id` values; and
- whole inventory SHA-256:
  `eccfd900deb5bd2e770e87ac8a5ef0f70d5914d1f4e1c06add840b54c6662b7f`.

The protected Stage 3 manifest contains exactly the same nine identities in
the same order. It has no duplicate, omitted, extra, or reordered identity,
and its inventory hash matches. The trusted Stage 3 contract validator also
accepts the complete bijection. The reconstructed spans are:

| Index | Span | Normalized SHA-256 / identity |
|---:|---:|---|
| 0 | 9–19 | `91969a44ebe81e8440544191d47e4d0c77497a01622cf2780ccd6a32cc927b0f` |
| 1 | 22–27 | `3394773e65cd3c685efe7b67a2e0712e9b8385d9cc4918b3d923519206a36953` |
| 2 | 30–31 | `1b6b20077ea79be1ae3b91368bba7358d1c81ca17220a6b219ea9a3d990854f0` |
| 3 | 34–35 | `8c3d1fd428ed4fd5551785b792097861c53d170392cd4e0e6e035ef41fdaffca` |
| 4 | 41–52 | `0d67eed4009d8768a79d1e4380a4bfda4237eea93a5b37e43a19e4a8fcea24a4` |
| 5 | 55–56 | `a3f1073813f699e9d521caadc3d9c55f9986dec43437ca84e8c209de8bea4a7b` |
| 6 | 59 | `e0a2c939ef190cae703a15286afeaedd08d0a4bb51e417bb7225c258617c3b93` |
| 7 | 60–61 | `d9e43013916651d6e2605735e1ab4130026a357ac29da8a57141d13b82a5f557` |
| 8 | 62 | `f8d3af040db5b70e848575e68e26451a99858586005b55415778a6bcdeb17e3c` |

Each `source_rule_id` is `rule-` followed by the corresponding normalized
SHA-256.

## Independent Stage 3 classification

I reclassified each entry from the frozen rule text, source program, claim,
and supplied operational semantics:

| Rule(s) | Independent class | Reason |
|---|---|---|
| `sortArrayLambda` (9–19) | `DEFINITION` | Expands a fresh nullary name to the exact annotated lambda AST from `solution.mpy`; it is a named proof/syntax term and does not match operational `<k>` state. |
| `sortArrayBody` (22–27) | `DEFINITION` | Expands a fresh name to the exact nested `sorted(sorted(arr), key=...)` return body. |
| `sortArrayClosure` (30–31) | `DEFINITION` | Names the exact closure value for the parameter, body, and module environment. It does not rewrite calls or skip frame semantics. |
| `sortArrayModule` (34–35) | `DEFINITION` | Names the exact module/`FuncDef` AST for the source solution. |
| `popcountKeyClosure` (41–52) | `DEFINITION` | Names the exact annotated-lambda closure value. Under `functions.k`, the empty-cell/free-variable lambda reduces through `#mkLambda` to this `closureValC`; the local rule does not preempt that reduction. |
| `sortArraySpec` (55–56) | `DEFINITION` | Defines a fresh output-summary symbol as `sortKeyVS(sortVS(VS), popcountKeyClosure)`. It states no law about an existing operation. |
| three `allNonNegativeInts` equations (59–62) | `DEFINITION` | They are the base, integer-head recurrence, and `[owise]` non-integer case of a structural domain predicate. |

Operationally, the inner `sorted` call allocates `list(sortVS(VS))`, and the
outer keyed call allocates `list(sortKeyVS(sortVS(VS), KV))`; this confirms
the summary's relevance and exact shape. For the key closure, supplied
semantics maps non-negative `N` through `binCodes(N)` and string `count` to
`cntSub`, matching the frozen lambda body. The opaque `sortVS` and
`sortKeyVS` boundary belongs to the supplied semantics, not to a local
verification rule masquerading as a lemma.

The independent totals are:

- `DEFINITION`: 9
- `OPERATIONAL_RULE`: 0
- `PROVED_DERIVED_LEMMA`: 0
- `DOMAIN_LEMMA`: 0

No inventory entry has the `simplification` attribute. Hence there is no
misclassified simplification rule, no purported derived lemma needing a prior
bridge-free proof, and no local domain lemma—relevant or irrelevant—hidden
under another category.

Counterfactual checks support the behavioral classification: replacing
`sortArraySpec` by an identity, constant, or single sort would no longer
summarize the two frozen operational sorts; replacing
`popcountKeyClosure` by a constant or identity closure would no longer be the
value produced by the source lambda. The actual equations contain the required
program structure rather than a convenient proof shortcut.

## Deterministic Stage 4 generation

Because the true domain-lemma set is empty, the exact expected Stage 4 source
rule and obligation sets are both empty. Independent static checks found:

- `input-manifest.source_rules = []`;
- `obligation-map.source_rules = []`;
- `obligation-map.obligations = []`;
- `obligation-map.trust_parameters = []`;
- generator and export obligation counts both `0`;
- export status `KLEAN_NO_OBLIGATIONS`;
- expected generated target `null`;
- actual target discovered by the trusted parser `null`;
- generator-manifest target `null`; and
- audit-input target `null`.

The obligation-map file hash is
`cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`,
matching the generator manifest. There are no duplicate or omitted source
rules, no generated conjuncts (vacuous or otherwise), no trust parameters, and
no `targetStatement` declaration anywhere in the generated Lean sources.
The generated sources also contain no `sorry`, `admit`, or `unsafe`; the
trusted proposition-trust and import checks pass.

All cross-bindings among the input manifest, generator manifest, export
result, generated tree, trust inventory, Stage 1 tree, Stage 3 manifest, and
signed audit input match. The fixed target identity is therefore the required
absence of a target, not a weakened replacement theorem.

## Fresh trusted preflight

The required command was run using the trusted checker:

```text
PYTHONPATH=/reference ... tools.klean_preflight.check_generation(
  /reference/k-proof,
  /reference/lemma-discovery.json,
  /reference/klean-generation,
  toolchain_lock=/reference/klean-toolchain.lock.json)
```

The audit container initially exposed a PID/proc namespace mismatch:
Lean attempted to resolve `/proc/<reported-pid>/exe`, which was absent, while
`/proc/self/exe` was available. This caused the first preflight attempt to stop
at `lake clean` before compiling any project source. I diagnosed the exact
failed `readlink` and used a narrow, recorded `/tmp` compatibility shim that
only retries a failed `/proc/*/exe` lookup as `/proc/self/exe`. It does not
modify or override any candidate, provenance, Lean, or K source. With the shim,
the pinned toolchain reports Lean 4.22.0 at commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`.

The fresh checker then copied the generated project to a temporary directory,
ran `lake clean` and `lake build`, and returned:

- status `KLEAN_NO_OBLIGATIONS`;
- `lake clean` exit `0`, empty-output hash
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`;
- `lake build` exit `0`, output hash
  `5f537dfeea6ca3f9f1346d28288ff276d81be17f404482380f0bffb69e5b5760`;
- obligation count `0`;
- target `null`;
- designated-sorry count `0`; and
- trust-declaration count `49`.

The complete fresh result exactly matches the recorded preflight object,
including both command-output hashes. The only build diagnostics are four
unused-variable warnings in generated `Func.lean`; the build completes
successfully. The checker also verifies that all immutable inputs and sidecars
remain unchanged across the build.

## Stage 5 disposition

Stage 5 is intentionally absent in `CLASSIFICATION_ONLY` mode, and an empty
domain set must have no target or proof candidate. Accordingly:

- no candidate clean build is required beyond the Stage 4 preflight build;
- no `Proof.final` exists or should exist;
- no `#print axioms Proof.final` run is applicable;
- there are no target parameters or operational bridges to audit; and
- the absence of `/candidate` is correct rather than an omission.

## Evidence

Raw commands and outputs are under `/audit-output/evidence/`. Key records are:

- `00-audit-input-and-mode.log`: signed input, mode, and candidate absence;
- `01-frozen-source-and-spec.log`: frozen program, K translation, verification,
  and claims;
- `02-inventory-reconstruction-and-contract.log`: full canonical inventory and
  trusted Stage 3 grouping;
- `03-stage3-manifest-and-bijection.log`: protected manifest and exact
  order/uniqueness/coverage comparison;
- `05-exact-relevant-semantics.log`: closure, call, sort, `bin`, and `count`
  operational rules;
- `06-stage4-manifests-and-producer-hashes.log`: producer hashes and all Stage 4
  manifests;
- `07-recorded-hash-recomputation.log`: complete signed-hash recomputation;
- `08-fresh-klean-preflight.log`: preserved initial environment failure;
- `09`–`13`: toolchain diagnosis and the narrow proc compatibility validation;
- `12-stage4-static-structure.log`: independent empty-bijection and target
  checks;
- `14-fresh-klean-preflight-with-proc-compat.log`: successful fresh trusted
  preflight and complete returned evidence;
- `15-trusted-vs-generation-producer-source.log`: direct source hashes and
  fresh preflight evidence hash; and
- `16-independent-classification.md`: full rule-by-rule semantic judgment and
  counterfactual checks.

The Stage 3 classification is complete and correct, the true domain set is
empty, and the deterministic Stage 4 `KLEAN_NO_OBLIGATIONS` result has exact
provenance, structure, target identity, and a successful fresh clean build.

VERDICT: PASS
LEGITIMACY: LEGIT
