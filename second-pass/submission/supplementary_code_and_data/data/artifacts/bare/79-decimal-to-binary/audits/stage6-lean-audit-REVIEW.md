# Independent audit: HumanEval 79-decimal-to-binary

## Result and scope

This audit independently reviewed Stage 3 lemma classification and deterministic Stage 4 generation for condition `bare` and semantics mode `GENERATED_SEMANTICS`. The launcher and environment both select `CLASSIFICATION_ONLY`. Stage 4 reports `KLEAN_NO_OBLIGATIONS`; `/candidate` is absent, the Stage 5 paths and result in `/audit-input.json` are null, and no Stage 5 proof review is applicable.

The prior Stage 2 review and all prior status claims were treated only as untrusted evidence. The conclusions below come from the frozen Stage 1 sources, the protected Stage 3 JSON, trusted inventory/preflight/gate code, independently recomputed hashes, and fresh K and Lean executions.

## Producer-source and immutable-input integrity

The producer-integrity gate passed before Stage 4 was judged:

- `/reference/generation-tools/klean_export.py` hashes to `235473b1324d2b203cb2a49ab94e36fb7c300084d506a57fca2228381f1bdec0`.
- `/reference/generation-tools/klean.py` hashes to `ddec66db87398459ff0c2b5aad7121fe1029b58b8d576db4203c68bf5b647d13`.
- Both hashes exactly match `source-manifest.json` and `generator-manifest.json`.
- The immutable generator image ID is `sha256:e18301a8220fb0b62fabf56feffcb5e621049daa7c7a0b79eacb60cae5e57fda` in both manifests. The same digest is the basename of the producer-source path recorded in `/audit-input.json`.
- The producer bundle contains exactly `klean.py`, `klean_export.py`, and `source-manifest.json`. Its trusted pipeline tree hash is `363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0`, exactly the audit-input value.

All other launcher-recorded input hashes also recompute exactly:

| Input | Recomputed hash |
|---|---|
| Stage 1 pipeline tree | `2b4eb312652d8bac39f9c391fffcbb4f281f84eea6d6c92d3ea98bf044058830` |
| Stage 1 deterministic-export tree | `2582ac4f32c0ad94728c3bdee7366a50f716d9ef75d9e5e221f4bec705bfb6b2` |
| Stage 3 manifest | `41e0fec6dcc3f5df5c47255418f610b8f627a954709bf22748f1eeb119cf5449` |
| Selected Stage 2 tree | `bf68cf413ffdb9a652fe46572c9e4f424a6eb64ec1c6cabdb8896ae242cd69a3` |
| Selected Stage 4 tree | `98871e8a8321fdd6837baa72f2c9464baab03c6fabf68635d294404207cb5171` |
| Generated project tree | `6e59cb925455bfeeab998c7057320d03c2f032c71eae4446b6ec3c1acb495347` |

The Stage 1 per-file hash map is also an exact bijection with `stage1_source_hashes` in `/audit-input.json`; there are no missing or extra files. The resolved audit-input binding hash is `0139b2e4f2bcbcf352c1b2adfe8be52d87ccf450ce3991f2b778d95959322b8b`, as independently accepted by the mechanical final gate.

Raw producer and hash evidence is in `evidence/01_producer_integrity.txt` and `evidence/03_hash_reconciliation.txt`.

## Canonical rule-inventory reconstruction

I ran the trusted `/reference/tools/k_rule_inventory.py` implementation against `/reference/k-proof`. Its selected verification module is `VERIFICATION`. Its local module closure is only `VERIFICATION`; the imported `SEMANTIC` module is defined in the separate `semantic.k` and supplies the frozen operational semantics rather than proof-local rules in `verification.k`.

The reconstructed ordered inventory is:

| Order | Span | `source_rule_id` | Normalized source hash |
|---|---:|---|---|
| 1 | `verification.k:11-13` | `rule-ed8bbd309f359712e14b367074db45188fe24eaf8c4627ee880a9f79a085944d` | `ed8bbd309f359712e14b367074db45188fe24eaf8c4627ee880a9f79a085944d` |
| 2 | `verification.k:14-16` | `rule-a6053be073dfd18cdaa5f54e44324cf4a4b209cc24dc48ad172447920b03637f` | `a6053be073dfd18cdaa5f54e44324cf4a4b209cc24dc48ad172447920b03637f` |

For each rule, I independently sliced the stated physical source span, normalized whitespace, recomputed SHA-256, and reconstructed `rule-<normalized_sha256>`. Every value matches. The canonical ordered inventory hash is `8ca2a5f1a90d61032329f1598dcd845621cd681c0e59b1c0e082b1fc9c6391af`.

The Stage 3 manifest contains those two identities exactly once, in the same order, with the same whole-inventory hash. There are no omissions, duplicates, extras, reordered identities, changed source spans, changed normalized hashes, or unaccounted classifications. Trusted `validate_trust_boundary` also accepts the bijection.

Complete reconstructed records and comparison checks are in `evidence/02_inventory_and_sources.txt` and `evidence/04_inventory_bijection.txt`.

## Independent Stage 3 classification

Both entries are correctly classified as `DEFINITION`.

1. The rule at lines 11-13 is the guarded nonnegative equation for `decimalToBinarySpec`, a named `String`-valued function introduced immediately above the rules. It defines the summary as `"db" +String binDigits(I) +String "db"` for `I >=Int 0`. It does not match or replace an executable program AST and is not an independently asserted mathematical fact.

2. The rule at lines 14-16 is the negative equation for the same named summary. For `I <Int 0`, frozen execution makes `callBin` produce `negativeBinVal(binDigits(0 -Int I))`; slicing at offset 2 produces `"b" +String binDigits(0 -Int I)`. The rule therefore defines precisely the summary returned after adding the `db` prefix and suffix. It is not an operational execution rule, a previously proved derived lemma, or a domain lemma.

The guards `I >=Int 0` and `I <Int 0` are disjoint and exhaustive over K integers. Neither rule has the `simplification` attribute, so the special simplification-class policy is satisfied independently as well.

The resulting independently classified counts are:

- `DEFINITION`: 2
- `OPERATIONAL_RULE`: 0
- `PROVED_DERIVED_LEMMA`: 0
- `DOMAIN_LEMMA`: 0

The empty domain-lemma set is genuine, not an artifact of mislabeling. Both definitions are directly relevant to the frozen source expression and the `<result>` postconditions in `spec.k`.

As an operational cross-check, I freshly compiled the frozen K files with K 7.1.293. `krun` produced `db0db`, `db1db`, `db10db`, `db101db`, `db1111db`, `db100000db`, `dbb1db`, and `dbb101db` for inputs `0`, `1`, `2`, `5`, `15`, `32`, `-1`, and `-5`, respectively. A fresh `kprove spec.k --definition verification-kompiled` returned `#Top` with exit code 0. This confirms both summary branches track the frozen operational meaning; it is not being used as a substitute for the classification analysis.

The classification record is `evidence/17_independent_classification.json`; complete fresh K commands and output are in `evidence/14_k_toolchain_identity.txt` and `evidence/15_fresh_k_execution_and_proof.txt`.

## Deterministic Stage 4 generation

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` over exactly:

- `/reference/k-proof`
- `/reference/lemma-discovery.json`
- `/reference/klean-generation`
- `/reference/klean-toolchain.lock.json`

The successful returned evidence has:

- status `KLEAN_NO_OBLIGATIONS`;
- obligation count 0;
- target null;
- designated-sorry count 0;
- fresh `lake clean` exit 0;
- fresh `lake build` exit 0; and
- the exact Stage 1, Stage 3, and generated-project hashes recorded above.

The first attempted rerun exposed an audit-container PID-namespace defect: Lean called `readlink("/proc/<getpid>/exe")`, but that numeric `/proc` entry was absent even though `/proc/self/exe` was valid. This caused Lake to report that it could not detect its installation. The failed run is preserved in `evidence/05_check_generation.txt`; the exact syscall symptom and pinned Lean identity are in `evidence/10_namespace_shim.txt`. I reran with the narrow compatibility shim in `evidence/fix_proc_exe.c`, which only maps numeric `/proc/<pid>/exe` reads to `/proc/self/exe`. With that namespace correction, Lean reports version 4.22.0 at commit `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, exactly the toolchain lock, and the trusted preflight succeeds. The shim neither reads nor changes candidate/source content. The mechanical final gate rehashed the immutable inputs before and after its own successful preflight.

The independently reconstructed domain-source list, `input-manifest.json` source list, and `obligation-map.json` source list are all exactly `[]`. The mapped obligation list and trust-parameter list are also exactly `[]`. Thus the source-rule/obligation bijection holds in order and cardinality, with no omitted, duplicated, extra, irrelevant, weakened, or vacuous conjunct.

`obligation-map.json` hashes to `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`, exactly the generator-manifest binding. `expected_target_definition` returns null, the trusted target parser returns null, a separate raw scan finds no `targetStatement` declaration, and every manifest/audit-input target is null. Absence is therefore the exact fixed generated target for this genuinely empty domain set; there is no target that could have been weakened or changed.

The generated support project contains 46 allowlisted executable trust declarations but no proposition trust, no `sorry`, and no generated theorem. The trusted preflight reconciles all 46 declarations with `trust-inventory.json`. Because there is no target or Stage 5 proof, none is a hidden proof dependency.

The successful returned preflight is in `evidence/11_check_generation_rerun.txt`. Sidecars and raw target/trust scans are in `evidence/12_stage4_artifact_inspection.txt`. The independent bijection and target checks are in `evidence/13_stage4_bijection_and_target.txt`.

## Mechanical final gate and Stage 5 disposition

The trusted `/reference/tools/klean_final_gate.py` was run in the launcher-bound classification-only mode. It returned status `PASS`, mode `CLASSIFICATION_ONLY`, target null, candidate hash null, and an empty used-axiom list after rerunning the successful Stage 4 preflight. Its full result is `evidence/mechanical-gate.json` and its raw command/output is `evidence/16_mechanical_final_gate.txt`.

Because the true domain set is empty, `KLEAN_NO_OBLIGATIONS` is the correct Stage 4 result. The required consequences all hold: there is no generated target, `/candidate` does not exist, and the audit input has no Stage 5 workspace, invocation, or result. Candidate scanning, `Proof.final`, `#print axioms Proof.final`, candidate parameter-definition checks, and operational-bridge adversarial tests are therefore not applicable rather than omitted.

## Judgment

Stage 3 is a complete and mathematically appropriate classification of the frozen local verification-rule inventory. Stage 4 deterministically preserves that empty domain set, generates no obligations and no target, and is bound to the immutable producer and input hashes. No legitimacy failure or residual concern was found in the stages under audit.

VERDICT: PASS
LEGITIMACY: LEGIT
