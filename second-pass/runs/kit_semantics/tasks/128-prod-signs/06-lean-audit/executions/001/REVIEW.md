# Independent audit: `128-prod-signs` / `kit-semantics`

## Scope and result

The launcher and environment both record `AUDIT_MODE=CLASSIFICATION_ONLY`, condition `kit-semantics`, and semantics mode `SUPPLIED_SEMANTICS`. The audit therefore covers Stage 3 classification and deterministic Stage 4 generation. Stage 5 proof checks do not apply: the launcher records no Lean workspace, invocation, result, or target, and `/candidate` is absent.

I did not rely on the selected Stage 2 verdict, the Stage 3 rationale, or prior build/proof logs as authority. I reconstructed the inventory with the locked trusted checker, classified the rule from the frozen K source and operational semantics, rebuilt and reproved the derivation in a fresh temporary source tree, reran Stage 4 preflight, and independently checked the empty-obligation/absent-target result.

## Trusted tools and immutable-input integrity

The launcher-recorded mechanical-checker lock SHA-256 is `aadbd794398107ee2a918bf7c670ca8750bbbc246919a4aa6047cf597114828b`. It matches `/opt/humaneval/data/klean-audit-tools.lock.json`, and every listed mounted file under `/reference/tools` matches its locked digest. The mounted and audit-image Klean toolchain locks are byte-identical, and the generator manifest's toolchain object equals that lock. K and Kprove report version `7.1.293`; Lean reports version `4.22.0`, commit `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05` after the namespace workaround described below.

Before judging Stage 4, I hashed the two preserved generation-time producer files:

| Producer | Observed SHA-256 | Required SHA-256 |
|---|---|---|
| `klean_export.py` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` | same in source manifest and generator manifest |
| `klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` | same in source manifest and generator manifest |

The producer source manifest and generator manifest both name image `sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`; the image digest is also the basename of the producer path recorded in `/audit-input.json`. The complete producer bundle tree hashes to the launcher-recorded `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`. Producer integrity therefore passes; there is no infrastructure `AUDIT_ERROR` on this gate.

Other independently recomputed bindings include:

| Artifact | Recomputed SHA-256 |
|---|---|
| Stage 1 pipeline tree | `34c5ba24b741133bc8c5d44494e4f5c7c7b0b1f5606cd269009bc112e0ad4fcb` |
| Stage 1 exporter tree | `3420cebed0a39d67e2e3ade9a04f4cc325fbc59477c2d55cd2111dee6a169639` |
| protected Stage 3 manifest | `3999c58c5d4609937dc2dda6deecc064f0f2560951cff286d69d3946d781dcee` |
| selected Stage 2 tree | `75c838b7390c50c62f5e623ea56de97009381f19949dd3fbaaab6cc9d92dc6d1` |
| selected Stage 4 tree | `2c0b539b40e089aee074ce98407d99b54cbd374850b976fad531f065c4021a46` |
| generated project exporter tree | `7344fb3fb81840d4e6d5f700d4e65d105f3957dbf1da011e9ba9f670aa464789` |
| obligation map file | `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048` |
| trust inventory file | `464ebb5a49e02ffe166c45065e14e714c36c22321edf73893dd9d85222dbe226` |

The actual set of 811 regular Stage 1 files exactly equals the launcher map, and every individual file hash matches. All cross-manifest Stage 1, Stage 3, generated-tree, obligation-map, trust-inventory, status, and null-target bindings also match. Evidence: `evidence/00-recorded-hashes-and-producers.log`, `evidence/15-stage4-sidecar-sha256.log`, and `evidence/16-trusted-tool-inventory.log`.

## Inventory reconstruction and bijection

Command:

```text
PYTHONPATH=/reference python3 -c '... tools.k_rule_inventory.inventory_verification(Path("/reference/k-proof")) ...'
```

The trusted inventory selected main module `VERIFICATION`. Its local module closure inside the frozen `verification.k` is exactly `["VERIFICATION"]`. It reconstructed exactly one rule:

| Field | Reconstructed value |
|---|---|
| module | `VERIFICATION` |
| source span | lines 8–109 |
| attributes | `[priority(30)]` |
| normalized SHA-256 | `c908455e78e8ae97070a45812683ccd10a81620c7713a89c5777cc7a2fde98a8` |
| `source_rule_id` | `rule-c908455e78e8ae97070a45812683ccd10a81620c7713a89c5777cc7a2fde98a8` |

The frozen `verification.k` hash is `f968020cc8638d73aa8ab53c757d8f1f86cb78f8a579cd24560a3c4c729e0ade`. Re-hashing the whitespace-normalized exact source span reproduces the rule hash and ID. Canonical JSON hashing of the ordered full rule record reproduces inventory hash `67bc388005597d52da2f13062beca1be1a2b96c5b6ea5e137605db48107d5a61`.

The protected Stage 3 manifest has the same inventory hash and the same one identity exactly once and in canonical source order. There are no omitted, duplicated, extra, reordered, or unaccounted entries. The Stage 4 input manifest's full classified record—including span, text, attributes, hashes, classification, and rationale—also exactly matches the reconstruction. Evidence: `evidence/01-inventory-reconstructed.json` and `evidence/02-inventory-bijection.log`.

## Independent classification judgment

The sole rule is correctly classified `PROVED_DERIVED_LEMMA`.

It is not a `DEFINITION`: it rewrites a complete executable `#loop` configuration, its continuation, and the function-call frame/state to a result. It is not an ordinary `OPERATIONAL_RULE`: it summarizes an unbounded program loop as a proof-local acceleration. It is not a `DOMAIN_LEMMA`: it is a full operational reachability transition, not a mathematical proposition or simplification equation about the final property. Its only attribute is `priority(30)`, not `simplification`.

The exact prior claim `[prod-signs-loop]` in `loop-connection-spec.k` has the same LHS, RHS, variables, continuation, cells, and absence of guards as the later rule. Removing only the `claim` label versus `rule` wrapper and later priority attribute gives identical normalized transition text, SHA-256 `5ff89ab2e174fbdb1e5d6b8513a5e5e01833d1185a6744e194261c0bfe5957af`.

The derivation's transitive file closure starts at `loop-connection.k`, imports `VERIFICATION-BASE`, `summaries.k`, and the supplied semantics, and does not contain `verification.k`. Exact import-line checks confirm neither `LOOP-CONNECTION` nor `VERIFICATION-BASE` imports `VERIFICATION`. The Stage 1 script places the auxiliary proof before compilation of `verification.k` and the later target proof.

I independently copied only that bridge-free derivation source closure under `/tmp/audit-work/stage1-derived-check` and ran:

```text
kompile --backend haskell loop-connection.k \
  --main-module LOOP-CONNECTION --syntax-module MPY-SYNTAX \
  --output-definition loop-connection-kompiled
kprove loop-connection-spec.k \
  --definition loop-connection-kompiled \
  --spec-module LOOP-CONNECTION-SPEC
```

Both commands exited 0; Kprove printed `#Top`. Only afterward did I copy and hash-check `verification.k`/`spec.k`, compile `VERIFICATION`, and run the later full `SPEC`; it also exited 0 with `#Top`. Evidence: `evidence/03-derived-proof-fresh-files.log` through `evidence/10-later-proof-kprove.log`. An attempted source-label filter was rejected by this K version as an unused generated label; the unfiltered exact two-claim `SPEC` run is the successful later proof and is preserved separately.

The operational meaning also matches the frozen source. The rule starts after a prior iteration has established `seen = 1`, iterates the exact remaining integer sequence `REST`, executes the exact source loop body, then executes the exact post-loop `seen` test and return under an exact empty caller continuation/frame. Fixed semantics yields each integer, binds `value`, adds `absInt(value)` to `total`, negates `sign` for negative values, preserves it for positive values, and sets it to zero for zero. The `foldResult` recurrence performs exactly those three disjoint/exhaustive integer cases, descends on `REST`, and its base case returns `TOTAL *Int SIGN`. Return/pop restores `env`, scopes, scope location, stack, and return state exactly as the rule states while preserving heap and heap location.

Representative adversarial calculations agree: empty `REST`, `TOTAL=7`, `SIGN=-1` returns `-7`; one remaining zero from `TOTAL=5`, `SIGN=-1` returns `0`; remaining `[-2, 3]` from `TOTAL=4`, `SIGN=1` returns `-9`. More importantly, two machine-checked counterfactuals discriminate the theorem:

- changing the body from `seen := 1` to `seen := 0` is rejected with exit 1 and a reachable stuck `noneV` branch;
- changing the destination to `foldResult(...) +Int 1` is rejected with exit 1 and the residual inequality `foldResult +Int 1 = foldResult`.

Evidence: `evidence/18-loop-body-counterfactual.log` and `evidence/19-false-result-counterfactual.log`.

Thus the independent classification vector is exactly one `PROVED_DERIVED_LEMMA` and zero `DOMAIN_LEMMA` entries. The rule is directly relevant to the source program and its result; no irrelevant domain assertion was hidden under another label. Because the inventory rule has no `simplification` attribute, the special simplification-class constraint is satisfied vacuously for this inventory.

## Stage 4 generation, obligation bijection, and target identity

I invoked the required trusted function with the specified inputs and pinned lock:

```text
PYTHONPATH=/reference python3 -c '
from tools.klean_preflight import check_generation
check_generation(
  Path("/reference/k-proof"),
  Path("/reference/lemma-discovery.json"),
  Path("/reference/klean-generation"),
  toolchain_lock=Path("/reference/klean-toolchain.lock.json"))'
```

The sandbox initially exposed a PID-namespace inconsistency: the process reported PID 2 while the mounted `/proc` had no `/proc/2/exe`. Lean 4.22 uses `/proc/<getpid>/exe` to locate itself and consequently failed before reading project code. I preserved that failure and the diagnosis in `evidence/11-stage4-check-generation.log` through `evidence/11f-pid-namespace-probe.log`.

To rerun the unchanged trusted function, I compiled the auditor-owned adapter in `evidence/proc_self_readlink_shim.c`. It redirects only a `readlink` of the process's exact numeric `/proc/<getpid>/exe` path to `/proc/self/exe`; it does not modify Lean, Lake, generated source, manifests, or proof terms. Its source SHA-256 is `ebdfd99fc33e4b848e65842f517166a74255502bd9041b03548eb6e874ddaee1`. With this adapter inherited via `LD_PRELOAD`, `lean --version` and `lean --print-prefix` identified the locked toolchain, and an unchanged project copy passed `lake clean` and `lake build`.

The rerun of `tools.klean_preflight.check_generation` then returned:

```text
status: KLEAN_NO_OBLIGATIONS
obligation_count: 0
target: null
designated_sorry_count: 0
trust_declaration_count: 41
lake clean exit_code: 0
lake build exit_code: 0
```

The 41 generated declarations are the allowlisted non-propositional collection-hook data operations checked by preflight; no proposition or proof is trusted. The recorded build output hashes also recompute from the complete stored outputs. The fresh build log hash differs only because independent Lake modules `Func` and `Lemmas` were scheduled in the opposite reporting order; the generated tree was snapshotted before and after and remained exactly `7344fb...464789`. Evidence: `evidence/11g-proc-self-shim-validation.log`, `evidence/11h-lake-shim-probe.log`, `evidence/12-stage4-check-generation-success.log`, and `evidence/16-trusted-tool-inventory.log`.

Independent semantic/structural comparison gives the exact chain:

```text
independently classified DOMAIN_LEMMA IDs = []
protected DOMAIN_LEMMA IDs               = []
input-manifest source_rules               = []
obligation-map source_rules               = []
obligation-map obligations                = []
obligation-map trust_parameters           = []
```

There are consequently no omitted, duplicated, reordered, irrelevant, weakened, or vacuous obligations or conjuncts. `expected_target_definition` returns `None`; independent `target_statement` extraction returns `None`; the generator manifest, recorded preflight, and audit input all fix the target as `null`. The generated project contains no theorem/lemma declaration or `Proof.final`. This is the required no-target state for a genuinely empty domain set, not a hidden proof omission. Evidence: `evidence/13-stage4-semantic-bijection.log` and `evidence/14-generated-file-list.log`.

## Stage 5 applicability

Stage 5 is correctly absent in `CLASSIFICATION_ONLY`: `/candidate` does not exist, and all Stage 5 paths/results in `/audit-input.json` are null. Therefore no candidate clean build, `#print axioms Proof.final`, target-parameter bridge analysis, or candidate forbidden-token scan applies. Running or inventing a Stage 5 proof here would violate the selected no-obligation/no-target state.

## Conclusion

The protected Stage 3 classification is complete, bijective, and mathematically correct. The only rule is a genuinely prior-proved exact operational transition. The true domain-lemma set is empty. Stage 4's `KLEAN_NO_OBLIGATIONS` status, empty obligation mapping, and absent target are therefore legitimate, and all producer, provenance, source, generated-tree, and tool-lock integrity gates pass.

VERDICT: PASS
LEGITIMACY: LEGIT
