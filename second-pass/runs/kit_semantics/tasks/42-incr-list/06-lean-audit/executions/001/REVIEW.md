# Independent audit: `42-incr-list`, `kit-semantics`

## Result and scope

This audit covers the protected Stage 3 lemma classification and the selected deterministic Stage 4 generation for HumanEval problem `42-incr-list` under `SUPPLIED_SEMANTICS`. Both the `AUDIT_MODE` environment variable and `/audit-input.json` record `CLASSIFICATION_ONLY`. `/candidate` is absent, so Stage 5 proof, axiom, theorem-identity, and operational-bridge checks are not applicable.

I treated all candidate/provenance reports and comments as untrusted evidence. The conclusions below come from the frozen sources, the trusted inventory and preflight code, direct hash reconstruction, and an independent semantic reading.

## Producer provenance gate

I hashed the two producer files before judging Stage 4:

| Producer | Actual SHA-256 | Source manifest | Generator manifest |
|---|---|---|---|
| `klean_export.py` | `0e653377b007bc1a742bbd8fa0dcfdf956ebb2ef2432a7137d032b0a70d59c1b` | match | match |
| `klean.py` | `0e6dba9d9f456574b3bf4f4bf06933d774e9125f4d12c5a90b7314d8dd5c33a4` | match | match |

The immutable image ID is `sha256:b377a4d6ce1a4210c17d7e862e3737d2c348cc4be96dfaca72ef9274846f4afc` in both `source-manifest.json` and `generator-manifest.json`. The image key is also the basename of the generation-producer-source path recorded in `/audit-input.json`. The whole mounted producer-source tree hash is `94ba4c012f48b7135094fefcc4517f5c9a5c1052fc304449c5505ddb4dca91b4`, exactly the audit-input value. The infrastructure provenance gate therefore passes.

Raw evidence: [producer integrity](/audit-output/evidence/01_producer_integrity.txt) and [hash reconciliation](/audit-output/evidence/05_hash_and_bijection_reconciliation.txt).

## Frozen-input integrity

Independent recomputation matched every relevant recorded hash:

| Artifact/hash convention | Recomputed SHA-256 |
|---|---|
| Stage 1 selected workspace tree | `37bbb1b4cabebf3da9f03dc0cc747d8c10b09a54383bda9c7aff855789a1ee3b` |
| Stage 1 exporter tree digest | `07e010f6fb6c20b806be86d11e7ef69f43f63c5c61e1c4a7616767cf33864a1c` |
| Stage 3 discovery file | `58f6b2942c240e02fd24e7316e2ee543e3f473afa1f0952b24c555b42c8c1263` |
| Selected Stage 2 audit tree | `57624be6d6f3305daf57d4148dee9c9867688ced7248aea62b2fc74e3bc924b1` |
| Selected Stage 4 artifact tree | `6f14c8ff5c13f60ebd97a1554a6c5f77a2de0c20bbf0fcbd2ce6a293db5819cb` |
| Generated-project exporter tree digest | `cc8eb11abd453c282d0136ed1ff88b256d8b1121aff59290f8c94bb4d994dd16` |

The audit input enumerates 784 Stage 1 file hashes. The frozen workspace also contains 784 regular files: there are no missing or extra paths and no content-hash mismatches.

## Inventory reconstruction and bijection

I ran trusted `tools.k_rule_inventory.inventory_verification` against the frozen `/reference/k-proof`. The local verification-module closure is exactly the single module `VERIFICATION`; imported supplied-semantics modules are not local proof-extension modules. The frozen `verification.k` SHA-256 is `32858026273941e4ef743d7b8c36cf3bf160466dc5d151ca0c0e35e7e0311d04`.

The trusted reconstruction found these eight rules, in source order:

| Span | `source_rule_id` / normalized SHA-256 | Independent class | Rule role |
|---|---|---|---|
| 9 | `rule-ea9ef756a199853827a586359d8f870476c308a30f0eeddad81ed1ced5c1534f` | `DEFINITION` | `isNumericVal` case for `Int` |
| 10 | `rule-eb56166732daec8d40953b1a816a0c32e93ece7bbf820f66cac61cfed1f4ca23` | `DEFINITION` | `isNumericVal` case for `Bool` |
| 11 | `rule-f1ada8e553470df79e923850e9a82e4ade7d8b82de56eded497f90ba526c9b0a` | `DEFINITION` | `isNumericVal` case for `Float` |
| 12 | `rule-304ee5c0da386cdc923ba4c73cc1f6dd81caf237937dabfdc90aeed8214fa4c2` | `DEFINITION` | `isNumericVal` `owise` case |
| 15 | `rule-f75f569f79b2c115362441fba7806717279c1238ce0191528cc1eb8220a50c99` | `DEFINITION` | `allNumeric` empty-sequence case |
| 16 | `rule-0599900824f5015e8454b006675aebe384009350a1ba7e6c7f893c8f3f2c7fff` | `DEFINITION` | `allNumeric` structural recurrence |
| 21 | `rule-dfc5044ec376f017835fd3fb82e8d9f45dd942408b63f2e73bf8d69e88ec62f1` | `DEFINITION` | `incrAcc` empty-remainder case |
| 22–25 | `rule-2c9fbc7cd6f99b65dbc48f9711be674cb9780c46cb33ec56bd27b7846bb99640` | `DEFINITION` | `incrAcc` structural recurrence |

For each entry, `source_rule_id` is `rule-` followed by its recomputed normalized source hash. The canonical whole-inventory hash is `e5ea14caf9f22c1087c2aa07a466c55d4997f2cd117345f37fa56fb8353ec40b`.

The protected Stage 3 manifest contains exactly eight unique IDs in the same order. Its inventory hash matches. Set and sequence comparison found no omission, duplication, extra ID, reordering, changed identity, or unaccounted rule. Trusted `validate_trust_boundary` also accepted the structural contract, returning counts `8 definition / 0 operational / 0 proved-derived / 0 domain`.

Raw evidence: [complete reconstructed inventory](/audit-output/evidence/02_reconstructed_inventory.json.txt), [frozen sources and Stage 3 manifest](/audit-output/evidence/03_stage1_sources_and_stage3.txt), and [bijection checks](/audit-output/evidence/05_hash_and_bijection_reconciliation.txt).

## Independent classification judgment

All eight Stage 3 labels are mathematically and operationally correct:

- Lines 9–12 are exhaustive constructor equations for the named proof-domain predicate `isNumericVal`. They assert no output property and replace no program execution. The supplied `Val` sort includes `Int`, `Bool`, and `Float`; supplied operator dispatch has `applyBin("+", V, 1)` cases for each of those sorts. The `owise` case excludes other represented values on which this expression has no matching supplied operator case.

- Lines 15–16 structurally define `allNumeric` on the two `ValSeq` constructors. This is a terminating recurrence used as the theorem precondition, not an assumed theorem about the program result.

- Lines 21–25 structurally define `incrAcc`. The empty case returns the accumulated sequence. The nonempty case appends exactly `applyBin("+", V, 1)` through the supplied `valSeqConcat` and recurses on the strict tail. This is an exact summary recurrence. It neither rewrites a `<k>` execution state nor asserts the postcondition independently. The separate Stage 1 loop-invariant claim connects actual list iteration, operator dispatch, and `append` heap mutation to this summary.

The recurrence is sensitive to order, input values, and length: replacing it by a constant, identity, hard-coded result, or by omission of `applyBin` would disagree already on a singleton input and would not match the loop-invariant heap transition. The empty and nonempty equations are disjoint and exhaustive on `ValSeq`, and both recurrences descend structurally.

There are no `[simplification]` rules, no claimed `PROVED_DERIVED_LEMMA` requiring an earlier independent K proof, and no ordinary operational rules in the local verification closure. None of the eight rules is a disguised `DOMAIN_LEMMA`: they define named predicates or a named recurrence, while the execution-to-summary fact is stated and proved as a reachability claim in `spec.k`. All three definitions are directly relevant to the frozen program's numeric-input domain and result list.

Operational trace evidence: [supplied semantics excerpts](/audit-output/evidence/04_operational_semantics_trace.txt).

## Stage 4 generation and fixed target

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and the required frozen input, discovery manifest, selected generation, and pinned toolchain lock.

The first attempt exposed an audit-sandbox issue before project evaluation: the PID namespace and host-mounted `/proc` made Lean 4.22 unable to locate `/proc/<getpid()>/exe`. Direct diagnostics reproduced `error: failed to locate application`. I compiled a narrow preload shim under `/tmp/audit-work` that returns the host-visible PID obtained from `/proc/self`; it changes no frozen or generated input. With that shim, the pinned executable identified itself as Lean `4.22.0`, commit `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, exactly the lock. The unchanged preflight then completed its fresh copied `lake clean` and `lake build`, both exit 0. The build compiled all seven generated Lean modules successfully.

The returned fresh evidence is:

- status: `KLEAN_NO_OBLIGATIONS`;
- Stage 1 exporter digest: `07e010f6fb6c20b806be86d11e7ef69f43f63c5c61e1c4a7616767cf33864a1c`;
- Stage 3 digest: `58f6b2942c240e02fd24e7316e2ee543e3f473afa1f0952b24c555b42c8c1263`;
- generated tree digest: `cc8eb11abd453c282d0136ed1ff88b256d8b1121aff59290f8c94bb4d994dd16`;
- obligation count: `0`;
- target: `null`;
- generated proof holes: `0`;
- allowlisted generated trust declarations: `49`.

The 49 declarations belong to the generic generated semantics prelude; the preflight verified their exact allowlist. No theorem target exists that could depend on them in this no-obligation generation.

I separately reconstructed the manifest mapping rather than relying on preflight alone. `input-manifest.json` reproduces the eight validated definitions exactly and contains no domain `source_rules`. `obligation-map.json` contains empty `source_rules`, `obligations`, and `trust_parameters`. Thus the source-rule/obligation bijection is exactly the empty bijection required by the independently empty domain set. The obligation-map raw hash is `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`, and the trust-inventory raw hash is `6e5009587cf50d49fc0578eae93c510e197c1db42686fb8aa35886c97f2a9e5e`; both match their manifests.

`generator-manifest.json` has `target: null`, an independent call to `target_statement` returned `None`, and a declaration search found no target-, obligation-, or final-like theorem. There are no conjuncts to weaken, duplicate, omit, or make vacuous. The generated Lean sources contain no `sorry`, `admit`, or `unsafe`. `/candidate` is absent. Therefore the selected `KLEAN_NO_OBLIGATIONS` status, lack of a generated target, and lack of Stage 5 proof are all required and legitimate.

Raw evidence: [initial environment failure](/audit-output/evidence/06_fresh_klean_preflight.txt), [Lean diagnostics](/audit-output/evidence/07_lean_environment_diagnostics.txt), [PID shim source and pinned Lean check](/audit-output/evidence/10_lean_pid_shim_test.txt), [successful fresh preflight](/audit-output/evidence/11_fresh_klean_preflight_success.txt), [complete Stage 4 manifests/sources](/audit-output/evidence/12_stage4_manifests_and_sources.txt), and [independent Stage 4 audit](/audit-output/evidence/13_independent_stage4_audit.txt).

## Final judgment

Stage 3 is complete, bijective, and correctly classifies all local proof-extension rules as definitions. The true domain-lemma set is genuinely empty. Stage 4 preserves every frozen identity and hash, generates the exact empty obligation mapping, changes no target, and correctly selects `KLEAN_NO_OBLIGATIONS`. No Stage 5 artifact is permitted or present in this audit mode.

VERDICT: PASS
LEGITIMACY: LEGIT
