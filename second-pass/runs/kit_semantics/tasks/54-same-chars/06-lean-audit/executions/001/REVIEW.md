# Independent Stage 3–5 Audit: HumanEval `54-same-chars`

## Result

The protected Stage 3 classification and the selected deterministic Stage 4 `KLEAN_NO_OBLIGATIONS` result are legitimate. The canonical verification-local rule inventory is genuinely empty, so the exact domain-lemma set is empty. Stage 4 preserves that empty set bijectively, generates no obligation or target theorem, and correctly has no Stage 5 candidate.

This was a fresh audit. Candidate and provenance prose, logs, prior verdicts, and comments were treated only as untrusted evidence. No earlier PASS or classification was used as an authority. Executed audit logic came from `/reference/tools`; the Stage 4 producer sources were hashed before Stage 4 was judged.

## Scope and mode

Both `AUDIT_MODE` and `/audit-input.json` record `CLASSIFICATION_ONLY`. The launcher record identifies problem `54-same-chars`, condition `kit-semantics`, and semantics mode `SUPPLIED_SEMANTICS`. Its Stage 4 selection is `KLEAN_NO_OBLIGATIONS`. The launcher record has `target: null`, `lean_workspace: null`, `lean_invocation: null`, and null Stage 5 hashes. `/candidate` does not exist.

Consequently, proof-mode-only work—copying a Stage 5 project as `Base`, building a candidate, printing `Proof.final` axioms, and auditing candidate parameter definitions—does not apply. In this mode, the required consistency condition is instead that a genuinely empty independently classified domain set has no generated target and no Stage 5 candidate; that condition holds.

## Producer and mounted-input integrity

The generation-time producer bundle contains exactly `klean_export.py`, `klean.py`, and `source-manifest.json`. Direct SHA-256 results were:

| Producer | Observed SHA-256 | Recorded SHA-256 | Result |
|---|---|---|---|
| `klean_export.py` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` | same in source and generator manifests | match |
| `klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` | same in source and generator manifests | match |

The producer bundle tree hash is `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`, matching `/audit-input.json`. The immutable generator image ID is `sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7` in `generator-manifest.json` and `source-manifest.json`; the launcher-recorded producer path has the same image digest as its terminal component. This clears the mandatory producer-provenance infrastructure gate.

The trusted launcher-input validator accepted `/audit-input.json`. Recomputed mounted hashes all matched:

| Binding | Recomputed and recorded SHA-256 |
|---|---|
| Stage 1 selected workspace tree | `0a2322c31c80ab54f0db2b1d40773d2ff46649a514ef95aedc4f7cbb8fa68ebd` |
| Stage 1 deterministic-export tree | `144ae655d09769629eb86ab56fd32e24bd36edfd07d9d2636ed8b6c1f90dfa13` |
| selected Stage 2 audit tree | `0aa823bdfd1759d764f4a4359c246c4160695e4f093bd483c1409e5cfc5bd91a` |
| Stage 3 manifest file | `e13c01259eb807dd465c4db3e29a0727d9ce0eb8df88d145e8977e70f5b7fcf3` |
| selected Stage 4 generation tree | `0ce0f09bafe0c907fcb12bc5d04d8a950308009a2ec7d1aee472d92e995a8812` |
| generated-project deterministic tree | `e0d7fca3eed49edb9c516589c077c9e5fc6aaffc2681f905df506ed37f875f78` |
| producer-source bundle tree | `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e` |

All 770 Stage 1 regular-file paths and per-file hashes also matched the launcher manifest bijectively.

## Stage 3 inventory reconstruction

I invoked `tools.k_rule_inventory.inventory_verification` on `/reference/k-proof`, then independently compared the result with `/reference/lemma-discovery.json` and invoked `tools.lemma_discovery_contract.validate_trust_boundary`.

Frozen `verification.k` has SHA-256 `ef48556fde781a8ca6e4e1986b701ccdf330897621c6658bd831ff4c17516ab4` and consists only of:

```k
requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY
endmodule
```

The trusted inventory selected `VERIFICATION`. Its local module closure is exactly `['VERIFICATION']`: `MPY` is supplied by the frozen external semantics, not defined as another local module in `verification.k`. The reconstructed ordered rule list is exactly `[]`. Therefore there are no source spans, normalized source hashes, or `source_rule_id` values to omit, duplicate, reorder, or alter. Canonical hashing of the empty rule document gives:

```text
4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945
```

That exactly matches the Stage 3 manifest, whose ordered rule list is also `[]`. Extra IDs and omitted IDs are both empty, both identity lists are unique, and the trusted contract validator passes.

## Independent classification and mathematical judgment

The complete independently reconstructed inventory contains:

| Classification | Count |
|---|---:|
| `DEFINITION` | 0 |
| `OPERATIONAL_RULE` | 0 |
| `PROVED_DERIVED_LEMMA` | 0 |
| `DOMAIN_LEMMA` | 0 |

There are no simplification rules, so none can be mislabeled as operational or proved-derived. There are no claimed proved-derived lemmas whose two-phase proof history must be established, and no local rule that assumes or entails the requested postcondition.

The empty domain set is mathematically genuine, not merely structurally self-consistent. The source body is `return set(s0) == set(s1)`. The frozen K claim loads that same function body and requires `result` to become `sameSet(dedupCodes(S0), dedupCodes(S1))`. The supplied operational semantics directly provides:

```k
rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS))
rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B)
```

The same supplied semantics gives terminating recursive definitions for `codeIn`, `dedupCodes`/`dedupFrom`, `snocCode`, `subsetCodes`, and `sameSet`; `sameSet(A,B)` is mutual subset. These rules implement the frozen meaning of set construction and set equality. They are fixed supplied-semantic definitions and operations, not proof-local extensions in the Stage 3 inventory. The requested result follows through ordinary frozen execution to exactly the postcondition expression; no separate mathematical domain fact has been inserted or omitted. Constant, identity, or hard-coded behavior would not have this operational path—for example, duplicate removal makes `"aab"` and `"ab"` equal as sets while differing strings such as `"ab"` and `"ac"` remain unequal.

## Stage 4 preflight and independent manifest audit

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` using the required Stage 1 workspace, Stage 3 manifest, selected Stage 4 generation, and `/reference/klean-toolchain.lock.json`.

The first attempt exposed an audit-container issue: Lean 4.22 reads `/proc/<getpid()>/exe`, while this PID namespace exposes `/proc/self/exe` but not `/proc/<namespace-pid>/exe`. Thus the initial `lake clean` exited 1 with `could not detect the configuration of the Lake installation`. This is preserved in `evidence/preflight_initial_failure.txt`.

I used the recorded, narrowly scoped compatibility shim in `evidence/lean_proc_exe_shim.c`, which redirects only `/proc/<pid>/exe` `readlink` requests to `/proc/self/exe`. It does not alter any mounted input, producer, trusted checker, generated file, or toolchain file. With that sandbox correction, `lean --version` reports Lean 4.22.0 at commit `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, matching the lock.

The unchanged trusted preflight then produced:

```text
lake clean: exit 0, empty output
lake build: exit 0
✔ [2/9] Built Klean54SameChars.Prelude
✔ [3/9] Built Klean54SameChars.Sorts
✔ [4/9] Built Klean54SameChars.Inj
✔ [5/9] Built Klean54SameChars.Func
✔ [6/9] Built Klean54SameChars.Lemmas
✔ [7/9] Built Klean54SameChars.Rewrite
✔ [8/9] Built Klean54SameChars
Build completed successfully.
```

Returned status is `KLEAN_NO_OBLIGATIONS`, obligation count is 0, target is null, sorry counts are 0, and the post-run immutable-input snapshot matches. The 41 generated executable-hook trust declarations are all recorded in `trust-inventory.json`; there is no target theorem or proof depending on them in this no-obligation mode.

Independent Stage 4 checks establish:

- `input-manifest.json`, generator provenance, and the independently validated Stage 3 inventory all bind the same inventory hash.
- Independently derived domain source rules, input-manifest source rules, and obligation-map source rules are all the exact ordered list `[]`.
- Expected source-rule IDs and observed obligation IDs are both `[]`; uniqueness and ordered bijection hold.
- `obligations` and `trust_parameters` are both empty. Counts in the map, generator manifest, export result, recorded preflight, and fresh preflight are all 0.
- `obligation-map.json` has observed and recorded SHA-256 `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`.
- The observed trust-inventory SHA-256 is `2c2a5ad44e1b9771992d3a4870e0e490cfd2e534c2fe052fb68bb660f09156cb`, exactly matching the export result.
- The generator toolchain object exactly equals `/reference/klean-toolchain.lock.json`.
- `expected_target_definition` is `None`; the observed generated target, generator-manifest target, and launcher target are all null. No `Target.lean` exists, and `Lemmas.lean` contains only an empty namespace.
- Export result, recorded preflight, Stage 4 selection, and fresh preflight consistently report `KLEAN_NO_OBLIGATIONS`.

There are no omitted, duplicated, irrelevant, weakened, or vacuous conjuncts: there are zero source obligations and zero generated conjuncts. Generating a theorem anyway would have been an unauthorized target change; none was generated.

## Stage 5 consistency

No Stage 5 proof exists or is permitted for this selected status. `/candidate` is absent, all launcher Stage 5 paths and hashes are null, the generated target is null, and the obligation map has no target parameters. This is exactly the required state for a legitimate `KLEAN_NO_OBLIGATIONS` result. `Proof.final`, candidate shadowing, candidate trust escapes, candidate axioms, and operational-bridge definitions therefore do not exist to audit.

## Evidence index

- `evidence/commands.txt`: exact reproducible command list.
- `evidence/provenance_check.py` and `evidence/provenance_hashes.txt`: launcher validation, mounted hashes, per-source hash comparison, and producer/image checks.
- `evidence/stage3_check.py` and `evidence/stage3_inventory.txt`: canonical inventory, identity-order comparison, whole-inventory hash, and classification counts.
- `evidence/operational_meaning.txt`: numbered source, claim, and supplied-semantic rules establishing the mathematical judgment.
- `evidence/preflight_check.py`, `evidence/preflight_initial_failure.txt`, and `evidence/preflight_rerun.txt`: exact trusted preflight invocation, complete subcommand outputs, sandbox diagnosis, and successful returned evidence.
- `evidence/lean_proc_exe_shim.c`: complete source of the sandbox-only compatibility shim.
- `evidence/stage4_check.py` and `evidence/stage4_bijection_target.txt`: sidecar hashes, source/obligation bijection, status, target identity, and Stage 5 absence checks.
- `evidence/final_check.py` and `evidence/final_integrity.txt`: final-mode, candidate-absence, preflight-result, and verdict-pair consistency checks.

VERDICT: PASS
LEGITIMACY: LEGIT
