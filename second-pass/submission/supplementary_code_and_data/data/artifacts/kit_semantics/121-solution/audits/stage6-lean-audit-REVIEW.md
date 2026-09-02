# Independent audit: HumanEval `121-solution`

## Scope and conclusion

This audit covers condition `kit-semantics` with supplied semantics (`SUPPLIED_SEMANTICS`). Both `AUDIT_MODE` and the signed launcher resolution say `CLASSIFICATION_ONLY`. The selected Stage 4 status is `KLEAN_NO_OBLIGATIONS`; `/candidate` is absent and all Stage 5 paths and results in `/audit-input.json` are null.

I independently reconstructed and classified the Stage 3 inventory, checked the immutable Stage 4 producer provenance, reconciled the mounted hashes, reran the trusted deterministic preflight, and checked the zero-obligation map and null target. The selected no-obligation result is legitimate because the independently determined `DOMAIN_LEMMA` set is genuinely empty.

## Producer and input integrity

The mandatory producer-source gate passed before Stage 4 was judged:

| Producer input | Recomputed SHA-256 | Recorded SHA-256 | Result |
|---|---:|---:|---|
| `klean_export.py` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` | same in the source and generator manifests | match |
| `klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` | same in the source and generator manifests | match |

The source manifest and generator manifest both bind those files to generator image `sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`. The image key is also the final component of the launcher-resolved producer-source path. The producer bundle tree hash recomputes to `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`, exactly as recorded in `/audit-input.json`.

All mounted content/tree bindings used by this audit matched: the Stage 1 pipeline tree hash, Stage 1 Klean export hash, discovery-manifest hash, selected Stage 2 tree hash, selected Stage 4 tree hash, and generated-project tree hash. The 805-entry `stage1_source_hashes` map had identical key sets and values, with no missing, extra, or changed file. The signed launcher resolution also passed its canonical envelope check; its recomputed digest is `c49fc4ccfba36e4fc07281e83cc6985e09ef3e5e97deaa707b6b275c64d6860e`.

The detailed reconciliation is in [06_recorded_hash_reconciliation.log](/audit-output/evidence/06_recorded_hash_reconciliation.log), with producer manifests in [02_producer_manifests.log](/audit-output/evidence/02_producer_manifests.log) and the signed-resolution check in [25_resolved_input_hash.log](/audit-output/evidence/25_resolved_input_hash.log).

## Inventory reconstruction and bijection

Using the trusted `tools.k_rule_inventory.inventory_verification` implementation on the frozen `/reference/k-proof` workspace produced:

- verification file SHA-256: `9c428c8a27eb0a26982004a221cb01a0fdb49c37a454797626a71df4afd9f9d4`;
- local verification-module closure: exactly `VERIFICATION`;
- rule count: one;
- inventory SHA-256: `1110ead8ae73844de04448028465295b04f1002ba4a020382352cf8a2a3c3001`.

The sole rule is at `verification.k:9-47`. Its normalized source hash is `61aeb3d85b68b0ecbd2dd5e4ea48a3c26d762d05db0e21e48b6ed02315486851`, giving source identity `rule-61aeb3d85b68b0ecbd2dd5e4ea48a3c26d762d05db0e21e48b6ed02315486851`. Its only attribute is `priority(40)`; it is not a `simplification` rule.

The protected discovery manifest contains exactly that one identity, in the same order, exactly once, and carries the same whole-inventory hash. There are no omissions, duplicates, extras, reordered identities, or unaccounted classifications. The canonical reconstruction, source span, text, hashes, and classification join are recorded in [04_inventory_reconstruction.json](/audit-output/evidence/04_inventory_reconstruction.json); the explicit ordered-list and Stage 4 bijection checks are in [19_independent_bijection_and_target.log](/audit-output/evidence/19_independent_bijection_and_target.log).

## Independent classification judgment

The one rule summarizes execution of the exact source `for` loop. It consumes `REST`, leaves the active continuation intact, and updates only the current scope's `position`, `result`, and `value` bindings according to `vsLen`, `oddAtEvenSum`, and `lastAfter`. Behaviorally it is an execution-accelerating bridge, not a mathematical domain assumption, a named definition, or an ordinary single-step operational rule.

The protected classification `PROVED_DERIVED_LEMMA` is nevertheless the correct category because the exact bridge proposition was first proved against a module that did not contain the bridge:

1. The 37 proposition lines at `verification.k:10-46` are byte-for-byte identical to `connection-spec.k:7-43`. Only the `rule` versus `claim [loop]:` introducer and the later proof-search priority attribute differ; neither changes the proposition. The exact comparison is in [20_exact_derived_statement_comparison.log](/audit-output/evidence/20_exact_derived_statement_comparison.log).
2. `CONNECTION-SPEC` requires and imports only `VERIFICATION-BASE`. That module imports fixed `MPY` semantics and contains recursive definitions for the integer-list domain predicate, guarded integer projection, the odd-at-even-position sum, and the final loop-variable value. It does not import `VERIFICATION` or contain the summary bridge. `verification.k` imports that base and installs the bridge only afterward.
3. I copied the frozen base sources to `/tmp/audit-work`, freshly compiled `VERIFICATION-BASE` with K 7.1.293, and reran `kprove connection-spec.k --definition base-kompiled --spec-module CONNECTION-SPEC`. Compilation exited 0 and the bridge-free proof returned `#Top` with exit 0. The full command and output are in [22_fresh_bridge_free_kprove.log](/audit-output/evidence/22_fresh_bridge_free_kprove.log).
4. The fixed semantics iterates lists through `#iterNext`, binds each yielded value with `#bindTgt`, executes the loop body, and returns to the residual `#loop`. Integer `+` and `%`, list iteration, scope writes, and `vsLen` agree with the recursive summary. The exact frozen operational rules reviewed are captured in [26_operational_semantics_bridge_review.log](/audit-output/evidence/26_operational_semantics_bridge_review.log).
5. As a counterfactual sensitivity check, I changed only the claimed final result to add an extra `1` and reran it against the same bridge-free compiled base. `kprove` exited 1 with a stuck implication exposing `ACC = ACC +Int 1`. The false variant was therefore rejected rather than closing vacuously; see [27_bridge_counterfactual.log](/audit-output/evidence/27_bridge_counterfactual.log).

The rule is thus an exact, bridge-free derived execution theorem over the same guard and matched context. It is relevant to the source loop and target postcondition, and it is not a mislabeled `DOMAIN_LEMMA`. The independently classified counts are: zero `DEFINITION`, zero `OPERATIONAL_RULE`, one `PROVED_DERIVED_LEMMA`, and zero `DOMAIN_LEMMA`.

## Deterministic Stage 4 judgment

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` on `/reference/k-proof`, `/reference/lemma-discovery.json`, and `/reference/klean-generation`, using `/reference/klean-toolchain.lock.json`.

The audit container exposes `/proc` from an outer PID namespace, while Lean 4.22 resolves its executable as `/proc/<getpid()>/exe`; the first attempt therefore failed before project evaluation with `could not detect the configuration of the Lake installation`. I diagnosed this mismatch and used a narrow audit-only `LD_PRELOAD` shim that returns the outer `NSpid` for `getpid()`. This changes only executable-path discovery for the Lean/Lake subprocesses. It did not modify any mounted input, generated source, project metadata, or toolchain. With the shim, the pinned binaries reported Lean 4.22.0 at commit `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05` and Lake 5.0.0, exactly matching the toolchain lock. The diagnosis and shim evidence are in [15_pid_namespace_evidence.log](/audit-output/evidence/15_pid_namespace_evidence.log) and [16_pid_shim_build_and_versions.log](/audit-output/evidence/16_pid_shim_build_and_versions.log).

The rerun then completed both fresh commands: `lake clean` exited 0, and `lake build` exited 0 after building all generated modules. The trusted checker returned:

- status `KLEAN_NO_OBLIGATIONS`;
- Stage 1/export hash `f4345a5c1a8960b7c9435381936db60430247a6496a11dcfdc3dfa0ffd2c8b7c`;
- discovery hash `c1cb90e696ce3111f75b8f7928a33cbbf2add661b332435764e059ce9026e5bb`;
- generated tree hash `39e21e8147a532c7288d4e43dfcd1f8a6aa4b27b91036320ef9815cbb128dc0b`;
- obligation count `0`;
- target `null`;
- no generated `sorry`.

The complete commands, build output, and returned JSON are in [17_check_generation_success.log](/audit-output/evidence/17_check_generation_success.log). The checker also re-snapshotted the read-only inputs after the build, so the compatibility workaround did not change them.

The original signed `stage4_preflight` object is data-identical to the mounted `preflight.json`. Both stored diagnostic hashes also recompute from their complete recorded output tails (including the empty `lake clean` output); see [30_stored_preflight_hashes.log](/audit-output/evidence/30_stored_preflight_hashes.log).

Independent of the preflight's structural judgment, the semantic source set and every Stage 4 representation agree exactly:

- independently classified domain source rules: `[]`;
- `input-manifest.json.source_rules`: `[]`;
- `obligation-map.json.source_rules`: `[]`;
- `obligation-map.json.obligations`: `[]`;
- `obligation-map.json.trust_parameters`: `[]`;
- generator and export obligation counts: `0`;
- expected target definition: absent;
- actual generated target, generator-manifest target, and signed audit-input target: all null.

The obligation-map and trust-inventory file hashes match their manifests, the generator toolchain exactly equals the trusted lock, and no vacuous conjunct exists because no conjunct or target exists. The generated scaffold contains 41 allowlisted executable collection-hook declarations, but no proposition trust and no theorem target; those declarations do not turn an empty domain set into a proof obligation. Full generated sources and sidecars are captured in [18_stage4_artifacts_and_absence.log](/audit-output/evidence/18_stage4_artifacts_and_absence.log).

## Stage 5

Stage 5 is correctly absent. The mode is not `CLASSIFICATION_AND_PROOF`, there is no generated target declaration to prove, `/candidate` does not exist, and the signed `lean_workspace`, `lean_invocation`, and `stage5_result` fields are null. Therefore candidate copying, `Proof.final`, axiom accounting, target-shadowing checks, and operational-parameter bridge checks are not applicable to this audit.

## Final assessment

The Stage 3 manifest bijectively classifies the sole local rule as a genuinely bridge-free proved derived lemma. The true domain-lemma set is empty. Stage 4 faithfully and deterministically represents that empty set with no obligations and no generated target, and Stage 5 is absent as required. No material classification, mathematical, provenance, target-identity, or legitimacy defect was found.

VERDICT: PASS
LEGITIMACY: LEGIT
