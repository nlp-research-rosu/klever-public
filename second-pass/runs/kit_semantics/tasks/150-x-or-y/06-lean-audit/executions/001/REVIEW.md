# Independent audit: HumanEval 150-x-or-y

## Outcome

The Stage 3 classification and deterministic Stage 4 `KLEAN_NO_OBLIGATIONS` result are correct. The local verification closure contains five rules, all of which are guarded equations defining the named summaries `trialChoice` and `xOrYSpec`. There is no operational rule, proved-derived rule, simplification rule, or domain lemma in that inventory. The genuinely empty domain-lemma set therefore maps bijectively to zero Lean obligations and no generated target.

The launcher and environment both record `CLASSIFICATION_ONLY`, so Stage 5 is inapplicable. `/candidate` is absent, and the signed Lean workspace, invocation, result, hashes, and target fields are null.

## Scope and trust treatment

I treated every mounted candidate/provenance comment, report, log, and claimed prior outcome as untrusted evidence. I did not accept the selected Stage 2 `CONCERNS`, the protected Stage 3 classifications, or the prior Stage 4 preflight as conclusions. Reconstruction used `/reference/tools/k_rule_inventory.py`; structural generation checking used `/reference/tools/klean_preflight.py`; the mathematical classification below was made independently from the frozen K source, source program, proof claims, and supplied operational semantics.

The signed audit-input digest is `1ea14ffa414548baaab35911c912003d69c8dddcac558650c4c19d994decdba1`, and its problem, condition, and semantics mode are respectively `150-x-or-y`, `kit-semantics`, and `SUPPLIED_SEMANTICS`.

## Producer provenance gate

I hashed the two required generation-time producer files before judging Stage 4:

| Producer | Observed SHA-256 | Recorded SHA-256 |
|---|---|---|
| `klean_export.py` | `0e653377b007bc1a742bbd8fa0dcfdf956ebb2ef2432a7137d032b0a70d59c1b` | same in `source-manifest.json` and `generator-manifest.json` |
| `klean.py` | `0e6dba9d9f456574b3bf4f4bf06933d774e9125f4d12c5a90b7314d8dd5c33a4` | same in `source-manifest.json` and `generator-manifest.json` |

The producer bundle contains exactly those two files plus `source-manifest.json`. Its pipeline tree hash is `94ba4c012f48b7135094fefcc4517f5c9a5c1052fc304449c5505ddb4dca91b4`, exactly the value in `/audit-input.json`.

The immutable generator image ID is consistently `sha256:b377a4d6ce1a4210c17d7e862e3737d2c348cc4be96dfaca72ef9274846f4afc` in `generator-manifest.json` and `source-manifest.json`. The signed audit-input producer path ends in the same digest, binding the mounted producer bundle to that image. This gate passes; there is no producer-source `AUDIT_ERROR`.

I also independently reproduced every mounted-tree hash recorded by the launcher:

| Input | Observed and recorded hash |
|---|---|
| Stage 1 pipeline tree | `9dc5d71b32aa9db54f988e46797f812f3879d84047bdc42e96d2bc3448459e6d` |
| Stage 1 export tree | `e2c2f35cedfca5020dd4d7764816d5f702a9bb7acc98d5416c3e108efa16f46f` |
| Stage 2 selected audit tree | `d9d0cfef1bd90b1343ff030797c617287ab5b4eabbddee25ccfdb7b72364d5da` |
| Protected Stage 3 manifest | `895e6040382ba24ece1de544593ff3d189547a253c1af1b5fd4e80e22bc5ea81` |
| Full selected Stage 4 generation | `790987b82d6810892ff2e6a444e2c1ecf00bd02517c44b56fa1cbd24a7ca1cd7` |
| Generated project | `7947e8194122e5d9d489405b86fc3dac8658e977770b842cad4c29c5f935f61c` |

All 771 Stage 1 regular-file names and individual SHA-256 values match `stage1_source_hashes` exactly. Manifest-side hashes for `verification.k`, the obligation map, generated tree, trust inventory, Stage 1, and Stage 3 also match. Full machine-readable results are in [hash-checks-result.json](/audit-output/evidence/hash-checks-result.json) and [producer-sha256sum.txt](/audit-output/evidence/producer-sha256sum.txt).

## Inventory reconstruction and Stage 3 bijection

The trusted inventory code selected `VERIFICATION` from the frozen `prove.sh`. Its local `verification.k` closure is `VERIFICATION-SYNTAX` followed by `VERIFICATION`; imported supplied-semantics modules are external to this local-file module closure. The frozen `verification.k` SHA-256 is `1058dbd13e2344ec9db0536cfc81ffee58b3d6dda40714c3bf741c77c0eb9ff9`.

The reconstruction found exactly these five rules, in source order:

| Lines | `source_rule_id` / normalized SHA-256 | Independent class | Role |
|---|---|---|---|
| 17–18 | `rule-cfb2314df4ea697cded9cf0262c9f9148799f41b14471c7e9e6718139a0df7cb` | `DEFINITION` | `trialChoice` base equation: when `I >= N` on `I >= 2`, return carried `R`. |
| 20–22 | `rule-7877c000c080d739794dbb3915705fc950212640a5d2b537a5a03a482090b6b0` | `DEFINITION` | Divisor branch of the recurrence: increment `I` and carry `Y`. |
| 24–26 | `rule-8c56ab5c7a8fcd164fb0d555a596cba2218ac3044885d21f8baf67a9b169c995` | `DEFINITION` | Non-divisor branch: increment `I` and preserve `R`. |
| 28–29 | `rule-a0b42dd3540472c0a1673da37721faef739d8c78131d66bce39a209f91709162` | `DEFINITION` | `xOrYSpec` base branch for `N < 2`, returning `Y`. |
| 31–32 | `rule-9fda901ff7675dee4a02c075bdb95e6d8c069630f55a40d4ecadca1361519e44` | `DEFINITION` | `xOrYSpec` branch for `N >= 2`, starting `trialChoice(N, 2, X, Y)`. |

For every entry, the normalized hash is the suffix of its `source_rule_id`. The canonical whole-inventory hash is `246b3d350a4a29f82f499272a975210b22fa01970cdb82b8256b92534fc98419`, which matches the protected manifest.

The protected Stage 3 ID list equals the reconstructed list exactly, including order. Both lists have five unique IDs. There are no omissions, duplicates, extras, changed spans, changed normalized hashes, or unaccounted classifications. Trusted schema/partition validation yields: 5 definitions, 0 operational rules, 0 proved-derived lemmas, and 0 domain lemmas. See [reconstructed-inventory.json](/audit-output/evidence/reconstructed-inventory.json).

## Independent classification judgment

These are definitions by behavior, not by their names alone:

- Each left-hand side is headed by a newly declared named summary symbol, `trialChoice` or `xOrYSpec`. No rule matches `<k>`, an invocation, a source-language statement, a scope, or any operational configuration cell. Thus none replaces or accelerates fixed program execution.

- The first three rules are a terminating recurrence on `I`: the two recursive branches apply only for `I < N` and replace `I` by `I + 1`; the base applies for `I >= N`. On the declared `I >= 2` domain, the divisor and non-divisor guards are complementary and disjoint because `pyMod(N,I)` is either zero or nonzero.

- The last two rules are complementary and exhaustive guarded equations for the total summary `xOrYSpec`, split at `N < 2` versus `N >= 2`.

- None states a standalone mathematical property of a completed program result. In particular, no rule asserts primality, divisor absence, or the requested result as an independent theorem. The equations define the proof term against which the operational loop is related by the `trial-loop` reachability claim in `spec.k`.

- No inventory entry has the `simplification` attribute. The special constraint on simplification classifications is therefore satisfied vacuously.

- No entry is `PROVED_DERIVED_LEMMA`. Stage 1 compiles one `VERIFICATION` module containing all five equations before running its proof claims; it does not first prove any exact rule in a module that omits that rule and later import it.

The supplied operational semantics evaluates name lookup and assignment through the scope map, unfolds `While` to repeated condition/body execution, dispatches integer `<` and `==`, and defines `%` through `pyMod(I1,I2) = ((I1 %Int I2) +Int I2) %Int I2`. Because the loop index is always at least 2 when modulo is evaluated, the recurrence and operational loop use the same defined positive-divisor behavior.

Mathematically, for `N >= 2`, the recurrence examines exactly `2, 3, ..., N-1`, changes the carried value from `X` to `Y` if a divisor is encountered, and never changes it back. It therefore returns `X` exactly when that range contains no divisor and otherwise returns `Y`; for `N < 2`, it returns `Y`. This matches both the frozen source body and the HumanEval prime/non-prime contract.

As finite supporting evidence, an independently coded recurrence and a literal operational loop agreed for every integer `N` from -25 through 100 with distinguishable `X` and `Y`. Boundary/adversarial witnesses included -5, 0, 1, 2, 3, 4, 7, 15, and 49. Flipping the source divisor test was detected at `N = 7`: the frozen body and summary return `X`, while the counterfactual returns `Y`. These tests support, but do not replace, the structural and mathematical argument above. See [classification-result.json](/audit-output/evidence/classification-result.json).

Accordingly, the protected classification is independently confirmed: all five entries are `DEFINITION`, and the true domain-lemma set is empty.

## Deterministic Stage 4 generation

I invoked `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`, `/reference/k-proof`, `/reference/lemma-discovery.json`, `/reference/klean-generation`, and `/reference/klean-toolchain.lock.json`.

The literal first run reached Lake but exposed an audit-container installation-detection problem: processes use an inner PID namespace while `/proc` is mounted from the outer namespace, so Lean could not resolve `/proc/<getpid()>/exe`. The exact failure is saved in [preflight-initial-failure.txt](/audit-output/evidence/preflight-initial-failure.txt). I reran the same trusted checker with a narrow local preload shim that changes only numeric `/proc/.../exe` readlink requests to `/proc/self/exe`; its complete source is [proc_exe_readlink_shim.c](/audit-output/evidence/proc_exe_readlink_shim.c). This did not alter the checker, K input, discovery manifest, generated project, or toolchain. The checker's before/after immutable snapshots remained identical.

The repaired run returned:

- status `KLEAN_NO_OBLIGATIONS`;
- Stage 1/export hash `e2c2f35cedfca5020dd4d7764816d5f702a9bb7acc98d5416c3e108efa16f46f`;
- Stage 3 hash `895e6040382ba24ece1de544593ff3d189547a253c1af1b5fd4e80e22bc5ea81`;
- generated-tree hash `7947e8194122e5d9d489405b86fc3dac8658e977770b842cad4c29c5f935f61c`;
- obligation count 0 and target null;
- designated sorry count 0;
- `lake clean` exit 0; and
- `lake build` exit 0, building all seven generated modules and reporting success.

The exact returned evidence, including build output and command-output hashes, is [preflight-result.json](/audit-output/evidence/preflight-result.json).

I separately reconstructed the Stage 4 bijection rather than relying on that result:

- `input-manifest.json` contains the exact five canonical classified rules, in order, under `definitions`; its operational and proved-derived lists are empty.

- The independently expected domain-rule ID list is empty. It equals `input-manifest.json`'s `source_rules`, `obligation-map.json`'s `source_rules`, and the list of obligation `source_rule_id` values exactly.

- `obligation-map.json` contains zero obligations and zero trust parameters. Hence there is no omitted, duplicated, reordered, irrelevant, weakened, or vacuous conjunct. This is a genuine empty set, not a generated `True` stand-in.

- `generator-manifest.json`, `export-result.json`, the recorded preflight, the rerun preflight, the selected Stage 4 status, and the signed audit input all agree on zero obligations and `KLEAN_NO_OBLIGATIONS`.

- `generator-manifest.json` matches the trusted toolchain lock. Its target is null. Independent parsing of the generated project returns no target, and `Klean150XOrY/Lemmas.lean` contains no proposition, theorem, lemma, axiom, or opaque declaration after comments are removed.

- The audit-input copy of the recorded Stage 4 preflight is byte-content equivalent as JSON, and all fixed hashes and target fields agree. The detailed check is [stage4-manifest-result.json](/audit-output/evidence/stage4-manifest-result.json).

Thus the fixed generated target is correctly absent. There is no theorem statement or parameter list to weaken, shadow, or bind incorrectly.

## Stage 5 applicability

Stage 5 proof checks are not applicable in this audit mode. `AUDIT_MODE` and the signed resolution both say `CLASSIFICATION_ONLY`; `/candidate` does not exist; `lean_workspace`, `lean_invocation`, their hashes, `stage5_result`, and `target` are all null. This is exactly the required state for a legitimate no-obligation generation. Running a candidate clean build, `#print axioms Proof.final`, target-shadowing scan, or operational-bridge parameter audit would invent a Stage 5 artifact that the signed resolution explicitly says does not exist.

## Evidence index

- [COMMANDS.md](/audit-output/evidence/COMMANDS.md): exact principal commands, exit statuses, and result-file mapping.
- [hash-checks-result.json](/audit-output/evidence/hash-checks-result.json): signed envelope, all recorded tree/file hashes, producer bundle, image binding, and manifest hash checks.
- [reconstructed-inventory.json](/audit-output/evidence/reconstructed-inventory.json): canonical spans, texts, normalized hashes, IDs, order, whole-inventory hash, and partition counts.
- [classification-result.json](/audit-output/evidence/classification-result.json): independent per-rule judgments, guard checks, adversarial witnesses, differential range, and counterfactual.
- [preflight-result.json](/audit-output/evidence/preflight-result.json): exact successful `check_generation` return value.
- [stage4-manifest-result.json](/audit-output/evidence/stage4-manifest-result.json): independent source-rule/obligation/target and Stage 5-absence checks.

VERDICT: PASS
LEGITIMACY: LEGIT
