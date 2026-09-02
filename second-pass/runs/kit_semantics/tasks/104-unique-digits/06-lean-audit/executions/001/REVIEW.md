# Independent audit: `104-unique-digits`, `kit-semantics`

## Scope and result

The launcher and `/audit-input.json` both record `CLASSIFICATION_ONLY` with `SUPPLIED_SEMANTICS`. `/candidate` is absent, as required in this mode. I therefore audited Stage 3 classification and deterministic Stage 4 generation. Stage 5 Lean proof identity, operational bridges, and `#print axioms Proof.final` are not applicable.

I treated all mounted candidate/provenance artifacts as evidence only and did not rely on the selected Stage 2 verdict or any earlier review. The frozen source, trusted inventory implementation, trusted preflight implementation, manifests, and generated tree were checked directly. Raw commands and outputs are indexed in `evidence/COMMANDS.md`.

## Producer-source integrity gate

This gate was completed before judging Stage 4.

| Item | Recomputed value | Recorded agreement |
|---|---|---|
| `generation-tools/klean_export.py` | `0e653377b007bc1a742bbd8fa0dcfdf956ebb2ef2432a7137d032b0a70d59c1b` | source manifest and generator manifest |
| `generation-tools/klean.py` | `0e6dba9d9f456574b3bf4f4bf06933d774e9125f4d12c5a90b7314d8dd5c33a4` | source manifest and generator manifest |
| Producer source tree | `94ba4c012f48b7135094fefcc4517f5c9a5c1052fc304449c5505ddb4dca91b4` | `/audit-input.json` |
| Immutable generator image | `sha256:b377a4d6ce1a4210c17d7e862e3737d2c348cc4be96dfaca72ef9274846f4afc` | source manifest, generator manifest, and the producer-source path recorded in `/audit-input.json` |

There is no missing or mismatched generation-time producer source. Evidence: `01b_producer_and_generator_manifests.log`, `06_independent_tree_hashes.log`, and `26_independent_structural_checks.log`.

## Independent Stage 3 inventory reconstruction

I ran `tools.k_rule_inventory.inventory_verification` from the trusted `/reference/tools` code against `/reference/k-proof`. The locally defined closure selected by `prove.sh` is exactly `VERIFICATION-SYNTAX` plus `VERIFICATION`. Imported `MPY` modules are supplied semantics, not locally defined modules in `verification.k`.

The reconstruction found 15 rules. The frozen `verification.k` hash is `97274568e5781b7c9e033f1b0ee018067c385c796d2d7454b9ec7f201cd59f73`; the canonical whole-inventory hash is `32bb0f36be98d96562f1768dc23748ba3c4cda812d63bfd210f22e1017c522c7`.

For every entry, the trusted reconstruction supplied the source span and rule text. I separately normalized the text with whitespace joining, recomputed SHA-256, and required `source_rule_id = "rule-" + normalized_sha256`. The result is:

| # | Lines | Defined head | Normalized SHA-256 | Independent class |
|---:|---:|---|---|---|
| 1 | 25 | `integerVals(.ValSeq)` | `fb45f6c21602bcf45c317e9243ab74c0e4d150dfe3405c24eac94cb927907858` | `DEFINITION` |
| 2 | 26–27 | `integerVals(vCons(...))` | `0fdf311e95699768f6653655fbcb75f1495794a6f4af7637ef16c68028a6dec8` | `DEFINITION` |
| 3 | 30–31 | `scanBad` base | `198caddd4e44844a4182afdc12cbe8b847068f235ba70560ca4acbb72b403a9c` | `DEFINITION` |
| 4 | 32–36 | `scanBad` recurrence | `deac1092831d0f56a57b5d50d5bb50905bd4181b70079af78ff6c94b96c9b9ed` | `DEFINITION` |
| 5 | 38–39 | `scanNumber` | `0c8212d872266a65f9628509b5e1ac121627dcc197e58d169331630d950d6ea4` | `DEFINITION` |
| 6 | 41–44 | `appendCandidate` append branch | `d0916ab1075ee30abc9bb69f741540c1aba4289fd887a7bf3041fd19926825f4` | `DEFINITION` |
| 7 | 45–47 | `appendCandidate` reject branch | `9e5adb33c787aab59ead767c0c33455c05defb2160117d4c0940e26577caf9a6` | `DEFINITION` |
| 8 | 50 | `collect` base | `282ed41406ab13eb82b75217914e68692e6094a01c85eeb1866659cbe295ca65` | `DEFINITION` |
| 9 | 51–53 | `collect` recurrence | `68f7dc46d6f6ba285ff86612d5bf5920c4bb5b391b302eec660c347e42802807` | `DEFINITION` |
| 10 | 56 | `afterValue` base | `e86655f5dac9607527040fcf3e3137fe2eb24adeced3f6ce55069aa63d8b3976` | `DEFINITION` |
| 11 | 57–58 | `afterValue` recurrence | `20b0fef7038d8a2ae37d334bd943372f2de264539aa1fa5c7adfe7f6332d1325` | `DEFINITION` |
| 12 | 60 | `afterNumber` base | `7dbd72f534f8827fae1ca749560e74c0b2851f710376eaaf6b43468df83bf7dd` | `DEFINITION` |
| 13 | 61–63 | `afterNumber` recurrence | `2cdae319e0d7f6b8ee7164bab66368ec7935956f067feb5fa8959dff5b035d0b` | `DEFINITION` |
| 14 | 65 | `afterBad` base | `3b5df8b88e16b28463ee3c71c8e6ccbb3f47c567782514a03d885de4a71144d9` | `DEFINITION` |
| 15 | 66–68 | `afterBad` recurrence | `1dc1bf365d06a0db8dd6cb05935a8779e9b0e53ff37f93aba8d009b0cf224660` | `DEFINITION` |

The protected discovery manifest contains these same 15 identities exactly once and in this exact order. Its inventory hash is identical. There are no omissions, duplicates, extras, reordered identities, changed hashes, or unaccounted classifications. Evidence: `05_reconstructed_inventory.log` and `26_independent_structural_checks.log`.

## Classification judgment

All 15 rules are genuinely definitional:

- `integerVals` is the constructor-recursive input predicate used to guard the loop claims.
- `scanBad` is a guarded, descending recurrence for the bad-digit counter. `scanNumber` defines the number local remaining after the while-loop.
- `appendCandidate` defines the two complementary accumulator branches, and `collect` is the constructor-recursive outer fold.
- `afterValue`, `afterNumber`, and `afterBad` define the persistent local values after consuming a list suffix.

Each head symbol is freshly declared as a K `[function]` in `VERIFICATION-SYNTAX`. The rules reduce only those named summary functions. None contains a `<k>` cell, rewrites a source-language AST node, skips or replaces an operational step, or shadows a supplied-semantics rule. A source-wide occurrence check found these summary symbols only in their declarations/equations and in the Stage 1 claims that relate actual execution to the summaries; they do not occur in the supplied operational semantics.

The operational comparison used the actual supplied rules for assignment, for/while iteration, `sum((value,))`, integer `%` and `//`, list `append`, and `sorted`. The definitions agree with that behavior: the scan descends by the decimal quotient and increments on even parity; the collect fold retains exactly values whose scan counter is zero; and the three `after*` folds retain Python's persistent loop locals. Finite boundary checks covered empty and duplicate lists, zero, negative integers (the Stage 1 claim's integer superdomain), one- and multi-digit positives, all-odd values, and values with one or several even digits. All checks passed; this is supporting evidence, not a substitute for the K claims. Evidence: `27_summary_usage_and_semantics_index.log`, `28_relevant_operational_semantics.log`, and `29_summary_semantic_checks.log`.

No rule is an `OPERATIONAL_RULE`, `PROVED_DERIVED_LEMMA`, or `DOMAIN_LEMMA`. In particular, no rule asserts a finished-result property as a derived fact; the domain-specific computation is introduced by recurrences and folds, while the Stage 1 reachability claims connect operational execution to them. `prove.sh` contains no earlier proof of a rule followed by later installation of that rule, so there is also no candidate for `PROVED_DERIVED_LEMMA`. Every reconstructed rule has an empty attribute list, so there are no `[simplification]` rules requiring a `DEFINITION`/`DOMAIN_LEMMA` check.

The true independently classified domain-lemma set is therefore empty.

## Stage 4 hashes, bijection, and fixed target

Independent tree and file hashing produced:

| Artifact | Recomputed hash | Match |
|---|---|---|
| Selected Stage 1 tree | `d0e48191b1bc10e9bce764f867586ca62a040223e19b7943a9b39692b2523af4` | `/audit-input.json` |
| Stage 1 deterministic-export digest | `9bb80aa5c7a6e31d4cc6e88d48e04ea9f00006caf73ded8b168e83e80affa1b8` | audit input and Stage 4 manifests |
| Protected Stage 3 manifest | `268ecb791f0571789c70ad51533d88c9a355743d0f14c2c3388b3c91b2fcc608` | audit input and Stage 4 manifests |
| Selected Stage 4 tree | `dadbf5baab7a5c29f4ad2099a0a764c9713f11be005ff6c7a6b2c066397fd9cb` | `/audit-input.json` |
| Generated project tree | `701aadbbd958948468ad492e6894fb6c540f4156a8e213b422d1a845f6dd3bc4` | audit input and generator manifest |
| Obligation map | `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048` | generator manifest |

The Stage 4 input manifest's `definitions` list exactly enriches the reconstructed 15-rule inventory with the protected classifications/rationales. Its domain `source_rules` list is empty. The generated `obligation-map.json` has exactly empty `source_rules`, `obligations`, and `trust_parameters` lists. Counts are zero in the generator manifest and export result. Thus the source-rule/obligation mapping is an exact empty-to-empty bijection: there is no omitted, duplicated, irrelevant, weakened, or vacuous conjunct.

The generator manifest and `/audit-input.json` both record `target: null`. The trusted target parser returned `null`, the expected-target constructor returned `null`, and an independent Lean declaration scan found no generated target. Because the independently classified domain set is genuinely empty, `KLEAN_NO_OBLIGATIONS` is the correct status rather than an evasion of a material lemma. There is no Stage 5 candidate.

## Fresh trusted preflight

I invoked `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and the exact required Stage 1, Stage 3, Stage 4, and toolchain-lock paths. The first invocation exposed an audit-sandbox infrastructure quirk: Lean's `/proc/<getpid>/exe` lookup failed although `/proc/self/exe` worked. I recorded the failure and used a minimal local `LD_PRELOAD` shim that only retries that exact failed self-executable lookup through `/proc/self/exe`. It does not alter any mounted input, command argument, compiler input, theorem, or compiler output. The pinned toolchain then identified itself as Lean 4.22.0 commit `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`.

The unchanged trusted checker then returned:

- status `KLEAN_NO_OBLIGATIONS`;
- obligation count `0`;
- target `null`;
- all Stage 1, Stage 3, and generated-tree snapshot hashes equal to the independently recomputed values;
- `lake clean` exit `0`; and
- `lake build` exit `0`, ending `Build completed successfully.`

The checker also found zero designated/other sorries and 43 generated trust declarations. Those declarations are exactly the generated skeleton's recorded allowlist; there is no target theorem or Stage 5 proof depending on them in this audit mode. The exact returned evidence is `evidence/preflight-return.json`; raw attempts and diagnostics are in `07_fresh_check_generation.log` and `24_fresh_check_generation_configured.log`.

## Final judgment

Stage 3 is complete and correctly classifies every locally inventoried rule as a definition. Stage 4 is provenance-consistent, deterministic, structurally intact, and correctly has no obligations or generated target. The classification-only mode correctly has no Stage 5 candidate.

VERDICT: PASS
LEGITIMACY: LEGIT
