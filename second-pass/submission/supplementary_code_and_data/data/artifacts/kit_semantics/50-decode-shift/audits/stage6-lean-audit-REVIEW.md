# Independent audit: `50-decode-shift`

## Scope and result

This audit covers condition `kit-semantics`, semantics mode
`SUPPLIED_SEMANTICS`. Both `AUDIT_MODE` and the signed resolution in
`/audit-input.json` say `CLASSIFICATION_ONLY`; the resolution digest
`647b603b85281bdc7f4e8838840bfb3e976aabe8b38d5b9dadd8315270cd3151`
recomputes correctly. `/candidate` is absent, `stage5_result` is null, and no
Stage 5 proof audit is applicable.

I independently reconstructed and classified the Stage 1 verification-rule
inventory. The true `DOMAIN_LEMMA` set is empty. Stage 4 therefore correctly
generated no obligations, no target proposition, and no Stage 5 handoff. The
trusted preflight and final mechanical gate both pass after a narrow
audit-environment compatibility workaround described below.

## Input and producer integrity

Every hash recorded in the signed resolution matches the mounted input under
the same trusted hash function used by the pipeline:

| Binding | Recomputed hash |
|---|---|
| Stage 1 workspace tree | `2a5edf00bdcb8c91d225bf4344e53ceee8640586ed80955d92d9164ce19c2830` |
| Stage 1 export tree | `1f9bec4e005a203efce55af468f332e1b6a68fcd83f2daaa50ee441bf57371ef` |
| Stage 2 K audit tree | `8786f1928a8bd756228c77a2eee11b9101d257c98cca8daac67e707180e6a02a` |
| Stage 3 manifest | `02addbd319c2b8115e328a30fd22546c237fb2762c545fa1575dfb4b35e19457` |
| Stage 4 generation tree | `e1f2cb0c08033cbb6f52a1c8485c2ee8ad53ea86ce11dbdb5cb2bf1202246412` |
| Generated-project tree | `962b43e932d87bde60ba17840d2fa63e7ab55c340f64789f169d799c2bb440ae` |
| Producer-source tree | `94ba4c012f48b7135094fefcc4517f5c9a5c1052fc304449c5505ddb4dca91b4` |
| Lean workspace/invocation | null/null, as recorded |

The per-file Stage 1 check is also exact: 770 recorded files, 770 observed
files, with no missing, extra, or mismatched entry.

Before making any Stage 4 judgment, I hashed both generation-time producers:

| Producer | Recomputed SHA-256 |
|---|---|
| `klean_export.py` | `0e653377b007bc1a742bbd8fa0dcfdf956ebb2ef2432a7137d032b0a70d59c1b` |
| `klean.py` | `0e6dba9d9f456574b3bf4f4bf06933d774e9125f4d12c5a90b7314d8dd5c33a4` |

Both values exactly match `source-manifest.json` and
`generator-manifest.json`. The image ID
`sha256:b377a4d6ce1a4210c17d7e862e3737d2c348cc4be96dfaca72ef9274846f4afc`
matches the source manifest, generator provenance, and the immutable producer
path component recorded in `/audit-input.json`. The generator toolchain object
also exactly matches `/reference/klean-toolchain.lock.json`. There is no
producer-source infrastructure error.

## Inventory reconstruction and bijection

Using the trusted `/reference/tools/k_rule_inventory.py` afresh on
`/reference/k-proof`, the selected main module is `VERIFICATION` and its local
verification-file closure is `VERIFICATION-SYNTAX`, `VERIFICATION`. The source
file hash is
`48ac03fce5b49d7a0535804ee577f75705af5e8e34eee64835324ccae7807ac9`.
The closure contains exactly these six rules, in source order:

| Lines | Symbol/case | Recomputed normalized SHA-256 | Classification |
|---|---|---|---|
| 17 | `decodeCode` | `91f09bc0f6ee846bbb22bc465c28ab2aee02a1084802c3ee379d9125ea824503` | `DEFINITION` |
| 20 | `encodeCode` | `c94b951365f26a181ad36212cc3bb2b9d82c1b0cf3f2c4281ce5b4d5e1d1332d` | `DEFINITION` |
| 23 | `decodeAcc`, empty | `20d3ab22276c5c40ff4d0d544eb7238f4fe30978c8fea2e71dc0912a582c7eee` | `DEFINITION` |
| 24–25 | `decodeAcc`, constructor | `e8da530e6906e2fd553848c88580186768ca9b9d321811af17377b09a5a7e384` | `DEFINITION` |
| 28 | `lowerCodes`, empty | `6a42619ac3350b1ffbbe69d54b2a6ef1dc6fc53c3b306864e2cd40d6db9dc96b` | `DEFINITION` |
| 29–30 | `lowerCodes`, constructor | `0dc99c16b055c88c85278d8830bce591f967b98564ba178b2d7453c517f2aa59` | `DEFINITION` |

For each row, the source span reproduces the exact rule text, the normalized
hash is the SHA-256 of whitespace-normalized text, and `source_rule_id` is
exactly `rule-` followed by that hash. The canonical whole-inventory hash is
`6a12a2f6c846652079e924de9ebe4396c9acfdc86d2c7106bad8a7d7d4e616b0`.
It matches the protected manifest and both Stage 4 manifests.

The protected Stage 3 list has six unique IDs. Its identity set and its order
both exactly equal the reconstructed list. There are no omissions, duplicates,
extras, reordered identities, changed hashes, or unaccounted rules. The trusted
Stage 3 contract validator also succeeds.

## Independent classification judgment

All six rules are genuine definitions under the frozen operational semantics:

- `decodeCode(C) = pyMod(C - 102, 26) + 97` names the source loop's
  per-character result. In the source, `ord("a") = 97`, so
  `C - 5 - ord("a")` is exactly `C - 102`. The supplied semantics defines
  Python-style `pyMod`, singleton-string `ord`/`chr`, and string concatenation;
  this helper does not match an AST term or configuration and does not bypass
  execution.

- `encodeCode(C) = pyMod(C - 92, 26) + 97` names the prompt encoder because
  `C + 5 - 97 = C - 92`. It is a mathematical summary used by the separate
  inverse claim, not an operational rewrite or an assumed inverse property.

- The two `decodeAcc` rules are the empty and constructor equations of a
  structurally descending recurrence. The constructor appends
  `decodeCode(C)` via `seqConcat` and recurs on `REST`, matching the source
  loop and the supplied string `+` semantics.

- The two `lowerCodes` rules are the empty and constructor equations of a
  named domain predicate. They define the predicate by structural recursion;
  they do not assert an independent fact about program output.

The equations have constructor-disjoint coverage, and the recursive cases
descend on the sequence tail. No rule has a `simplification` attribute, so the
simplification-class restriction is vacuously satisfied. None matches `<k>`,
`Call`, `#loop`, bindings, or state cells, so none is an
`OPERATIONAL_RULE`. `verification.k` contains no staged derived rule, and
`prove.sh` does not first prove a rule in a bridge-free module and later install
that exact rule; therefore no entry qualifies as `PROVED_DERIVED_LEMMA`.

Most importantly, no equation states an independent program/postcondition
fact. The independently reconstructed counts are six definitions, zero
operational rules, zero proved-derived lemmas, and zero domain lemmas. Thus no
`DOMAIN_LEMMA` has been hidden under another label.

As adversarial finite evidence, the defining equations match the source
arithmetic for every integer from -1000 through 1000; the inverse holds for all
26 lowercase ASCII codes; sequence witnesses including empty, wraparound, and
the full alphabet match the source loop. The input `f` (code 102) decodes to
`a` (97), while changing the source shift from 5 to 4 produces `b` (98), so the
summary is sensitive to a material source mutation. These checks support, but
are not substituted for, the direct equational and operational-semantic
comparison above.

## Deterministic Stage 4 and target identity

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`
using exactly `/reference/k-proof`, `/reference/lemma-discovery.json`,
`/reference/klean-generation`, and the trusted toolchain lock. It returned:

- status `KLEAN_NO_OBLIGATIONS`;
- obligation count 0;
- target null;
- generated tree hash
  `962b43e932d87bde60ba17840d2fa63e7ab55c340f64789f169d799c2bb440ae`;
- 41 generated trust declarations, exactly reconciled with the generated trust
  inventory and with no proposition trust;
- `lake clean` exit 0 with empty output; and
- `lake build` exit 0 with output hash
  `e07d26ec145e1d06f35a3ff1cc93b721254b01c25f2b1d8d1e1e20ad1e45c700`.

The returned document exactly equals both the recorded `preflight.json` and
the preflight embedded in `/audit-input.json`.

Independently of that preflight, `input-manifest.json` has `source_rules: []`.
`obligation-map.json` has exactly `source_rules: []`, `obligations: []`, and
`trust_parameters: []`. The generator and export result both record count 0.
The trusted target constructor returns no expected definition, the target
parser finds no declaration, the generator manifest and audit input both bind
target null, and `Klean50DecodeShift/Lemmas.lean` contains an empty namespace
with no declaration. Thus the source-rule/obligation mapping is an exact empty
bijection: there is no omission, duplicate, weakened obligation, irrelevant
conjunct, vacuous `True` target, alternate target, or changed target.

Because the mathematical reclassification also yields an empty true domain
set, `KLEAN_NO_OBLIGATIONS` is substantively correct rather than merely
self-consistent. No Stage 5 project may accompany it, and none does. The trusted
final mechanical gate independently reports `PASS`, mode
`CLASSIFICATION_ONLY`, target null, candidate null, and no used axioms. Its
`semantic_classification: NOT_EVALUATED` field is expected; the semantic
classification is supplied by the independent analysis above.

## Audit-environment note

The first fresh preflight attempt failed before project processing because this
sandbox exposes `/proc/self/exe` but not `/proc/<namespace-pid>/exe`, while Lean
4.22 uses the latter for `IO.appPath`. Merely selecting the pinned toolchain did
not fix it. I preserved both failures, then used a narrow audit-local
`LD_PRELOAD` shim that redirects only numeric `/proc/<pid>/exe` `readlink`
calls to `/proc/self/exe`. With that compatibility shim, the pinned Lean binary
reported version 4.22.0 and commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`; the unchanged trusted preflight
completed and reproduced the recorded clean/build output hashes exactly. The
shim changes executable-path discovery only, not the mounted inputs, generated
project, Lean kernel, declarations, or theorem content. This was a recovered
launcher-environment defect, not a proof or provenance discrepancy.

## Evidence

- `evidence/01_reconstructed_inventory.json`: complete reconstructed rules,
  spans, texts, normalized hashes, IDs, order, and inventory hash.
- `evidence/02_classification_analysis.json`: per-rule semantic judgment and
  adversarial/counterfactual witnesses.
- `evidence/03_stage4_integrity_preflight.json`: producer authentication, all
  signed hash comparisons, all 770 Stage 1 hashes, structural bijection checks,
  and returned preflight evidence.
- `evidence/03c_preflight_command_1.log` and
  `evidence/03c_preflight_command_2.log`: complete fresh `lake clean` and
  `lake build` outputs.
- `evidence/03a_*` and `evidence/03b_*`: preserved initial launcher failures;
  `evidence/03_lean_app_path_shim.c` and `.log` document the narrow recovery.
- `evidence/04_target_absence_audit.json`: independent empty-bijection and
  target-absence scan.
- `evidence/05_mechanical_gate.json`: trusted final mechanical-gate result.
- `evidence/COMMANDS.md`: exact commands and result-file mapping.

VERDICT: PASS
LEGITIMACY: LEGIT
