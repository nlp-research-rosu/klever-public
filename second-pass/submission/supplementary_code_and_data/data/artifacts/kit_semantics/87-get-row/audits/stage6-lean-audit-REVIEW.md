# Independent Stage 3–5 audit: HumanEval 87-get-row

## Scope and result

This audit independently evaluated condition `kit-semantics`, semantics mode
`SUPPLIED_SEMANTICS`. Both `AUDIT_MODE` and `/audit-input.json` record
`CLASSIFICATION_ONLY`. The selected Stage 4 status is
`KLEAN_NO_OBLIGATIONS`; `/candidate` is absent, and the recorded Lean workspace,
Lean invocation, and Stage 5 result are all null. Stage 5 proof checks are
therefore not applicable.

I treated the mounted Stage 1–4 artifacts and prior reviews as evidence, not as
authority. The canonical inventory and Stage 4 preflight were run from the
trusted `/reference/tools` code. I also rebuilt and reproved the material K
connection from frozen source in a fresh directory below `/tmp/audit-work`.

## Producer-source authentication and frozen hashes

Producer authentication passed before Stage 4 was judged:

| Item | Independently computed value | Recorded value(s) | Result |
|---|---|---|---|
| `generation-tools/klean_export.py` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` | Same in `source-manifest.json` and `generator-manifest.json` | Match |
| `generation-tools/klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` | Same in `source-manifest.json` and `generator-manifest.json` | Match |
| Generator image | `sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7` from the audit-input producer path | Same in the source and generator manifests | Match |
| Producer-source tree | `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e` | Same in `/audit-input.json` | Match |

Thus there is no producer-source infrastructure `AUDIT_ERROR`. Full values and
comparisons are in
[producer-authentication.json](/audit-output/evidence/producer-authentication.json).

The trusted Stage 6 audit-input verifier accepted the document and reconstructed
the same resolution. All independently recomputed input hashes matched:

| Hash | Value |
|---|---|
| Stage 1 pipeline tree | `a351438ad2d9db2d296a7f77e05f32af041e1ae28770a0ca5189edf8630b7f80` |
| Stage 1 export tree | `8300203166971359c9a39f0a8e2b0387e38e3b299bac629dcb0d39cd417f8369` |
| Stage 3 discovery manifest | `8ad8f4f11adfbe6714138d38ea8cef6da8a600b0a3505abdb6650d1796e606e9` |
| Selected Stage 2 audit tree | `251a532f4acbe3177d557c34b0b4c65f4793f8f6a6729f088576c219df5732c6` |
| Selected Stage 4 generation tree | `0f0b8b6cd96c9b650c2c103a70ad1c64539e896e065b9a902d697ed987bf8e24` |
| Generated project tree | `f478c2f6989c3f7155ac3bd94ea97cc3bcea216017193fe18800846cf59dfe14` |

The selected-artifact hashes also match their selection records. All 826
per-file Stage 1 hashes match exactly, with no missing or extra paths. Evidence:
[recorded-hash-comparison.json](/audit-output/evidence/recorded-hash-comparison.json)
and
[stage1-source-hashes.json](/audit-output/evidence/stage1-source-hashes.json).

## Canonical inventory reconstruction

Using `tools.k_rule_inventory.inventory_verification` with
`PYTHONPATH=/reference`, I resolved main module `VERIFICATION` and its local
in-file module closure `VERIFICATION-SYNTAX`, `VERIFICATION`. The frozen
`verification.k` SHA-256 is
`3190eb1293e60f64529009fef78338043277800fa4ffd49c4651b1efe10d3b60`.

The trusted inventory found exactly 13 rules. For every rule, I independently
re-sliced the stated source lines, normalized whitespace, recomputed the
normalized SHA-256, and confirmed that `source_rule_id` is exactly `rule-`
followed by that hash. The canonical whole-inventory hash is
`341c239f750211e8fd0165f2fec51a0237792c9f2ecb13194dc5a1c10de5135c`.

The protected Stage 3 manifest has exactly the same 13 IDs in the same order.
There are no duplicate, omitted, extra, reordered, or changed identities, and
its whole-inventory hash matches. See
[reconstructed-inventory.json](/audit-output/evidence/reconstructed-inventory.json)
and [inventory-bijection.json](/audit-output/evidence/inventory-bijection.json).

## Independent rule classification

The independent result is 12 `DEFINITION` rules, one
`PROVED_DERIVED_LEMMA`, no `OPERATIONAL_RULE` entries, and no `DOMAIN_LEMMA`
entries:

| Frozen lines and identity | Classification | Independent judgment |
|---|---|---|
| 21–24, `rule-884ba37529d334ff1536a797b79c37b0c1aec1517e50018bbcdd7e37dc667f49` | `PROVED_DERIVED_LEMMA` | Exact guarded `For`-to-`#loop` consequence of fixed semantics, proved first without importing `VERIFICATION`; details below. |
| 26, `rule-61639aeb3e4eded394e1d4b26f9ee1295448bf3ece5ac65e09a909061f5802ed` | `DEFINITION` | Empty-sequence base equation for the named `advanceIndex` recurrence. |
| 27–28, `rule-66ce320138cf211431fb75578ddb97ab1ae42b0641cbe44f60c87c594342d78b` | `DEFINITION` | Cons equation for `advanceIndex`, incrementing once and descending on the tail. |
| 30, `rule-c194ab0b0d5b805678184ae23956c929962cbe0d80d58f6329b819af01736b5b` | `DEFINITION` | Empty-row base equation for the named `scanAppend` summary. |
| 31–39, `rule-f34eeff932b7abe8c16eabf63b849ff14abedadb470e8cc2afef3c5432725a54` | `DEFINITION` | Matching-element recurrence: append current coordinate, increment column, descend. This is a truthful definitional `simplification` rule. |
| 40–44, `rule-4e4b59f2ee8e8937c5779283b3c612d56db07d5a6665f7d3c5cd3081cfe4c1ff` | `DEFINITION` | Complementary nonmatching recurrence: omit append, increment column, descend. This is a truthful definitional `simplification` rule. |
| 46, `rule-4812be0f87480004ec1d88555dc42724de85607ba560b55f59cc783b411b4b54` | `DEFINITION` | Empty-row-sequence base equation for `rowsAppend`. |
| 47–53, `rule-ca82d2906a1a64f2f30d91c523b1da3a97bdc91d39bf996607ba4b0eb8dedf1f` | `DEFINITION` | List-shaped-row recurrence: invoke the row scan at column zero, increment row, descend. This is a guarded definitional `simplification` rule. |
| 55–64, `rule-513effea58452b129f11e969f69b8b1ba4753f0475e7adccd0435ef28aa12dc3` | `DEFINITION` | `INNERBODY` macro names the exact membership/append/column-increment source AST. |
| 66–71, `rule-a5d752033c107eb7ed24b3bd20619e493bc116b42cee0b9c358ddef4a7846bce` | `DEFINITION` | `OUTERBODY` macro names the exact reset/inner-loop/row-increment source AST. |
| 73–89, `rule-f1c7c2f7e079aec7d74121119086f5ce9b88d758dc886ab637c02f5d1a3efff4` | `DEFINITION` | `GETROWBODY` macro names the exact function body, including both sort calls and return. |
| 91–95, `rule-f673c7a1de0fb731d8b8b9003d5b2dc47528b1ed6b2c77eea115e579be27e7f5` | `DEFINITION` | `COLUMNCLOSURE` names the exact `_column_desc` closure proof term. |
| 97–101, `rule-734823e8299b7b2d2a2ba3a8604e4912e0ff16f6d7012cabd5bf2251083265db` | `DEFINITION` | `ROWCLOSURE` names the exact `_row_asc` closure proof term. |

The complete rationales are preserved in
[independent-classification.json](/audit-output/evidence/independent-classification.json).
They agree entry-for-entry and in order with the protected classifications.

### Derived-rule check

The sole non-definition has exactly the required proof-before-use structure.
`SHAPE-CONNECTION-SPEC.for-list-shape` has the same LHS, RHS, guard, arbitrary
continuation, and framed configuration as the later rule. Its definition
imports `ROW-MODEL` and the fixed MPY semantics, not `VERIFICATION`. Fixed
semantics has
`For(T, OBJ, B) => #loop(OBJ, T, B)`; under the rule's guard
`V ==K list(rowContents(V))`, the claimed RHS is identical.

The frozen `prove.sh` proves this exact claim before compiling the later
verification module. I independently repeated that ordering in a fresh
workspace:

- Fresh bridge-free `kompile`: exit 0.
- Fresh bridge-free `kprove`: exit 0 and `#Top`.
- Fresh later `VERIFICATION` `kompile`: exit 0.
- Fresh later full `SPEC` `kprove`: exit 0 and `#Top`.
- Counterfactual claim that incorrectly drops the one-element loop: exit 1
  with `WarnStuckClaimState` and a residual that still binds and executes `7`.

Raw commands and outputs are in
[shape-recheck-kompile-command.json](/audit-output/evidence/shape-recheck-kompile-command.json),
[shape-recheck-kprove-command.json](/audit-output/evidence/shape-recheck-kprove-command.json),
[verification-recheck-kompile-command.json](/audit-output/evidence/verification-recheck-kompile-command.json),
[verification-recheck-kprove-command.json](/audit-output/evidence/verification-recheck-kprove-command.json),
and [shape-bad-kprove-command.json](/audit-output/evidence/shape-bad-kprove-command.json).

### Definition and relevance check

`advanceIndex`, `scanAppend`, and `rowsAppend` occur only as named mathematical
summaries in the loop claims; they do not match and replace program syntax.
Their equations follow the fixed list iterator, tuple-membership, append, and
assignment semantics step for step. The base/cons cases structurally descend;
the two `scanAppend` guards are complements; and every `rowsAppend` proof use is
under `listRows`. The body/closure macros expand to the frozen source AST and
are named proof terms.

As finite adversarial support for this source-level judgment, an independent
evaluator compared the recurrences with a separate operational reading over
196,923 exhaustive ragged integer-list cases and 5,000 seeded larger cases,
with zero mismatches. Constant, identity, off-by-one column, missing column
reset, and off-by-one row mutations all fail on the recorded witness. This
testing supports—but does not replace—the structural classification argument.
See [semantic-checks-command.json](/audit-output/evidence/semantic-checks-command.json)
and [source-slices-command.json](/audit-output/evidence/source-slices-command.json).

No rule asserts the desired coordinate property or ordering fact as an
unproved simplifier. There is consequently no hidden or irrelevant domain
lemma, and the true domain-lemma set is genuinely empty.

## Deterministic Stage 4 judgment

I reran `tools.klean_preflight.check_generation` directly with
`PYTHONPATH=/reference` on `/reference/k-proof`,
`/reference/lemma-discovery.json`, and `/reference/klean-generation`, using the
pinned `/reference/klean-toolchain.lock.json`.

The returned result is:

- status `KLEAN_NO_OBLIGATIONS`;
- obligation count 0;
- target `null`;
- generated tree hash
  `f478c2f6989c3f7155ac3bd94ea97cc3bcea216017193fe18800846cf59dfe14`;
- fresh `lake clean` exit 0; and
- fresh `lake build` exit 0, “Build completed successfully.”

The complete returned document is
[preflight-returned-evidence.json](/audit-output/evidence/preflight-returned-evidence.json),
and the invoking command is
[mechanical-audit-command-rerun.json](/audit-output/evidence/mechanical-audit-command-rerun.json).

An independent binding of my classifications to the Stage 4 files confirms:

- independent domain IDs: `[]`;
- `input-manifest.json` source-rule IDs: `[]`;
- obligation-map source-rule IDs: `[]`;
- generated obligation IDs: `[]`;
- all three classification partitions match the independent inventory;
- the obligation count is 0 in the map, generator manifest, and export result;
- the obligation-map hash is
  `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`;
- there are no conjuncts, hence no duplicate, weakened, irrelevant, or vacuous
  conjuncts;
- the observed target, generator-manifest target, audit-input target, and
  preflight target are all exactly `null`; and
- the generated `Lemmas.lean` contains only imports and an empty namespace,
  with no theorem or lemma declaration.

This is the exact empty-set source-rule/obligation bijection and exact fixed
generated target (absence of a target), not merely a self-consistent manifest.
The selected status and export status both say `KLEAN_NO_OBLIGATIONS`. There is
no Stage 5 candidate or result, as required. Full checks are in
[stage4-judgment-command.json](/audit-output/evidence/stage4-judgment-command.json).

The generated project contains 41 allowlisted executable hook declarations
from the Klean prelude. The trusted preflight reconciled them exactly with
`trust-inventory.json`, rejected proposition trust, and found zero designated or
other sorries. With no generated proposition, none supplies or weakens an
obligation.

### Lean tool environment note

The first preflight attempt reached its fresh build but failed because Lean
4.22 resolves its executable through `/proc/<getpid()>/exe`. In this sandbox,
`getpid()` reported inner PID 3 while numeric `/proc` entries used the outer
PID; `/proc/3/exe` therefore did not exist. This is recorded in
[mechanical-audit-command.json](/audit-output/evidence/mechanical-audit-command.json)
and [lean-environment-check-command.json](/audit-output/evidence/lean-environment-check-command.json).

I used the narrow compatibility shim in
[lean_getpid_compat.c](/audit-output/evidence/lean_getpid_compat.c), which returns
the outer `Pid` from `/proc/self/status` for Lean/Lake subprocesses. Without it,
`lean --version` exits 1; with it, Lean reports version 4.22.0 and pinned commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`. The shim does not alter mounted
inputs or Lean source/proof terms. After this environment repair, the exact
trusted preflight passed, and its before/after immutable snapshots remained
unchanged. The initial environment failure is therefore resolved rather than
an outstanding audit error.

## Stage 5

Stage 5 is correctly absent in `CLASSIFICATION_ONLY`. No generated target
exists, `/candidate` is absent, and all Stage 5 resolution fields are null.
Clean candidate rebuilding, target shadowing checks, `Proof.final`, axiom
printing, and operational-parameter bridge analysis are not applicable.

## Final judgment

The Stage 3 manifest is a complete ordered bijection with the independently
reconstructed inventory, and every classification is semantically correct.
The true domain-lemma set is empty. Authenticated deterministic Stage 4
therefore correctly emits no obligations and no target, and Stage 5 is
correctly absent.

VERDICT: PASS
LEGITIMACY: LEGIT
