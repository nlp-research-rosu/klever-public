# Independent audit: HumanEval 75-is-multiply-prime

## Scope and mode

This audit covers the protected Stage 3 rule classification and selected
deterministic Stage 4 generation for condition `bare` and semantics mode
`GENERATED_SEMANTICS`. The launcher and environment both record
`CLASSIFICATION_ONLY`. `/candidate` is absent, as required, so Stage 5 proof
construction, `Proof.final`, `#print axioms`, and operational-parameter checks
are not applicable.

All mounted candidate, provenance, review, log, and comment content was treated
as untrusted evidence. The prior Stage 2 verdict was not used as a premise; its
selected tree hash was only recomputed against `/audit-input.json`.

## Producer provenance gate

The required producer-source gate passed before the Stage 4 judgment:

| Artifact | Recomputed SHA-256 |
|---|---|
| `/reference/generation-tools/klean_export.py` | `235473b1324d2b203cb2a49ab94e36fb7c300084d506a57fca2228381f1bdec0` |
| `/reference/generation-tools/klean.py` | `ddec66db87398459ff0c2b5aad7121fe1029b58b8d576db4203c68bf5b647d13` |
| Producer-source tree | `363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0` |

The two file hashes agree exactly with both `source-manifest.json` and
`generator-manifest.json`. The producer-source tree hash agrees with
`/audit-input.json`. Both manifests record generator image
`sha256:e18301a8220fb0b62fabf56feffcb5e621049daa7c7a0b79eacb60cae5e57fda`;
the immutable producer-source path recorded by `/audit-input.json` has the same
image-hash basename. There is therefore no producer-source infrastructure
error.

## Inventory reconstruction and Stage 3 bijection

I ran the trusted `tools.k_rule_inventory.inventory_verification` against the
frozen `/reference/k-proof`. The local verification-module closure is exactly
`VERIFICATION`. It contains one rule:

| Field | Reconstructed value |
|---|---|
| Module | `VERIFICATION` |
| Source span | lines 11–34 of `verification.k` |
| Attributes | `[simplification]` |
| Normalized SHA-256 | `42e3d1013e958ee69b67f3151bd6928b3cf7deebc75764f9d52633a30ba4514c` |
| `source_rule_id` | `rule-42e3d1013e958ee69b67f3151bd6928b3cf7deebc75764f9d52633a30ba4514c` |

The whole reconstructed inventory hash is
`8a50c25e51f43344edb8669c842b3a74cfd0db6f67078c4875653fbe93a69e77`.
I independently recomputed the rule normalization, rule hash, derived ID, and
canonical inventory hash.

`/reference/lemma-discovery.json` contains exactly that one identity in the
same order, exactly once, and its inventory hash matches. There are no omitted,
duplicated, extra, reordered, or changed identities. The trusted
`lemma_discovery_contract.validate_trust_boundary` also accepted the
bijection.

## Independent classification judgment

The sole rule is correctly classified as `DEFINITION`.

Immediately before the rule, `verification.k` introduces the fresh function
symbol:

`isThreePrimeProductBelow100(Int) : Bool`

The rule unconditionally expands that symbol to a finite Boolean disjunction.
Its right-hand side is non-recursive and consists only of integer products,
integer equality, and Boolean disjunction. It therefore defines a named
mathematical summary and terminates. It is not:

- an operational rule, because it matches no `<k>`, environment, result, or
  other execution cell and replaces no source-program computation;
- a proved derived lemma, because it is a defining equation rather than a rule
  first proved in a module excluding itself; or
- a domain lemma, because it does not assert a new theorem about previously
  defined symbols—it supplies the meaning of the newly introduced summary
  symbol.

The `[simplification]` attribute is therefore consistent with the required
policy that simplification rules be `DEFINITION` or `DOMAIN_LEMMA`.

The operational K semantics confirms the separation. `solutionProgram`
expands to the complete translated source AST. The `Module` execution rule
binds the unary parameter, `execute(Return(E))` evaluates the body through
`evalBool`, and `evalOr` implements the equality chain with short-circuit
`orElseBool`. The verification definition neither preempts nor shortcuts those
steps; it reduces only the summary predicate used in the destination
`<result>` cell.

The definition is relevant: `spec.k` requires the final result to be
`Bool(isThreePrimeProductBelow100(A))`.

I also constructed an independent trial-division oracle and enumerated all
nondecreasing prime triples whose product is below 100. The oracle, the source
program, and the definition all produce exactly:

`8, 12, 18, 20, 27, 28, 30, 42, 44, 45, 50, 52, 63, 66, 68, 70, 75, 76, 78, 92, 98, 99`.

Adversarial witnesses `-7, 0, 1, 7, 8, 12, 30, 49, 97, 98, 99, 100` agree
across all three interpretations. This checks negative inputs, small
non-products, valid products, prime and composite near-misses, the upper valid
values, and the out-of-contract boundary.

Consequently the independent domain-lemma set is genuinely empty.

## Recorded-hash verification

All launcher-recorded and manifest-bound hashes checked in this audit agree:

| Binding | Recomputed hash |
|---|---|
| Signed resolved-input digest | `08af5ec928bec9e42f4cf18eea2400987949caec21a30998b643306d74b9301d` |
| Full Stage 1 workspace tree | `3e3adf6ec1d061b5091ee3021b87196af35fa5805041369f5d54c67a274b7c2b` |
| Stage 1 deterministic export | `0d17a627d6f2810115cf1acb28aee8983a36cb1749fa07fd560690478eb73274` |
| Selected Stage 2 audit tree | `3223340fa6749f6340082dfcb01baea7f6a02e270b783a43a214d1aa92c5c776` |
| Stage 3 manifest file | `50a2282ffa01743e1a3fad74ae31c872f89915dd996637e2cfe94bc5c3fa2c6e` |
| Selected Stage 4 generation tree | `2f1aee60a5fd8f3dd12dcba9dc2baabb2ffc6814822f3aec83cd545cfa766b2d` |
| Generated project tree | `8856da228309b113e96939938818fea2fbe8afba61518ddf71fc9a9ffcf331e9` |
| Obligation map file | `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048` |
| Trust inventory file | `b0098667a06e130d249eddbc988e425ebb3d49e78c921289d7b4db1a40ebfebc` |

Every per-file Stage 1 hash in `/audit-input.json` also matches the mounted
file, with no missing or extra regular files.

## Stage 4 preflight, obligation bijection, and target identity

I reran the unmodified trusted
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and the
required Stage 1, Stage 3, Stage 4, and toolchain-lock paths.

The first invocation exposed a sandbox PID-namespace issue: Lean tried to
resolve `/proc/<namespace-pid>/exe`, which does not exist in this launcher,
although `/proc/self/exe` is valid. Raw diagnosis is preserved. I used a narrow
`LD_PRELOAD` compatibility shim that retries only that failed executable-path
lookup through `/proc/self/exe`; it does not alter project files, Lean inputs,
commands, outputs, or exit codes. With the shim, Lean identifies the pinned
version and commit exactly:

`Lean 4.22.0, commit ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`.

The trusted preflight then returned:

- status `KLEAN_NO_OBLIGATIONS`;
- Stage 1 export hash
  `0d17a627d6f2810115cf1acb28aee8983a36cb1749fa07fd560690478eb73274`;
- Stage 3 manifest hash
  `50a2282ffa01743e1a3fad74ae31c872f89915dd996637e2cfe94bc5c3fa2c6e`;
- generated tree hash
  `8856da228309b113e96939938818fea2fbe8afba61518ddf71fc9a9ffcf331e9`;
- obligation count `0`;
- target `null`;
- designated-sorry count `0`;
- trust-declaration count `44`; and
- exit code `0` for both `lake clean` and `lake build`.

The 44 generated trust declarations are structurally reconciled with
`trust-inventory.json` by the preflight and contain no proposition trust. They
do not prove a Stage 5 target because no target exists.

The exact source-rule/obligation comparison is:

| Collection | Value |
|---|---|
| Independently classified domain rules | `[]` |
| `input-manifest.json.source_rules` | `[]` |
| `obligation-map.json.source_rules` | `[]` |
| `obligation-map.json.obligations` | `[]` |
| `obligation-map.json.trust_parameters` | `[]` |

Thus the mapping is an exact empty bijection. There are no omitted, duplicated,
irrelevant, weakened, or vacuous conjuncts.

`tools.klean_export.target_statement` independently returns `None`.
`generator-manifest.json`, `/audit-input.json`, and the launcher-recorded
preflight all record target `null`, and `Lemmas.lean` contains no target
declaration. This is the required fixed target for a genuine
`KLEAN_NO_OBLIGATIONS` generation.

## Stage 5 disposition

Stage 5 is correctly absent in `CLASSIFICATION_ONLY` mode. `/candidate` does
not exist, the launcher records null Stage 5 paths and hashes, and there is no
generated theorem for a candidate to prove. A clean candidate build,
`#print axioms Proof.final`, candidate trust scan, proof identity check, and
parameter operational-bridge tests would be required only in
`CLASSIFICATION_AND_PROOF`.

## Evidence

Raw commands and results are under `/audit-output/evidence/`. The principal
records are:

- `00_inputs_and_producer_hashes.txt`
- `03_frozen_stage1_sources.txt`
- `04_inventory_reconstruction.txt`
- `05_generated_project_and_sidecars.txt`
- `06_check_generation.log` through `30_check_generation_success.log`
- `32_recomputed_tree_hashes.txt`
- `39_independent_audit_checks_final.log`
- `independent_audit_checks.py`

The failed environment attempts remain preserved rather than being hidden; the
successful trusted preflight and exact PID-namespace diagnosis are in
`28_pathtrace.txt`, `29_pid_namespace_compatibility.txt`, and
`30_check_generation_success.log`.

VERDICT: PASS
LEGITIMACY: LEGIT
