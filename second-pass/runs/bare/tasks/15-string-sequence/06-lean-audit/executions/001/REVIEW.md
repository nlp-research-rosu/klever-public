# Independent Stage 3–5 audit: HumanEval 15-string-sequence

## Result

The protected Stage 3 classification is complete and mathematically
appropriate. All 11 rules in the local verification-module closure are genuine
definitions of summaries or named proof terms. None is an operational rule, a
proved-derived lemma, or a domain lemma. The independently determined domain
set is therefore genuinely empty.

The deterministic Stage 4 generation is correctly bound to its producer
sources and frozen inputs. Its source-rule/obligation relation is the exact
empty bijection, its status is correctly `KLEAN_NO_OBLIGATIONS`, and it has no
generated target. The signed audit mode is `CLASSIFICATION_ONLY`; no Stage 5
candidate is mounted or recorded.

No earlier review, verdict, rationale, or log was treated as authoritative.
Prior artifacts were used only as evidence after independent source,
provenance, hash, semantic, and mechanical checks.

## Audit mode and signed inputs

`AUDIT_MODE` and the signed resolution in `/audit-input.json` both say
`CLASSIFICATION_ONLY`. The condition is `bare` and the semantics mode is
`GENERATED_SEMANTICS`. The signed resolution digest recomputes to
`78a0d70f8efcd1ed91035bca9656b9426916b003f11863df4d7e92cc8bff3e32`.

Every recorded hash that is applicable in this mode was independently
recomputed:

| Input | Recomputed SHA-256 | Result |
|---|---|---|
| Stage 1 workspace tree | `4dcd159bc8476ee9fbe842d41c046f39bd87b97adf3fc9fe1332fa9df8d62159` | matches |
| Stage 1 deterministic export tree | `459999394a3f057558622ff8d982dfe33a5ffcc9b8b66b6efd069f3894010d9f` | matches |
| Stage 3 discovery manifest | `f27eba8f22657d031987898b81793e15ad2211f557551837e03fa186d07d86a0` | matches |
| Selected Stage 2 audit tree | `ae43231fae12c1b7f4ebf1d52f544911cbccd2f5687cabeff71d7abf35e7a1a4` | matches |
| Stage 4 generation tree | `34446e04bb8da15929f195739b04e22fc2507902f40dfb833cc2e27982b531c4` | matches |
| Producer-source tree | `363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0` | matches |
| Generated Lean tree | `db7a770ed33df3d7bc2d8fdc1aa4cf14b7b85a3efdde68d99a84b1ceecc7bca7` | matches |
| Lean workspace/invocation | `null` / `null` | matches classification-only mode |

All nine per-file Stage 1 hashes also match `stage1_source_hashes` in the
signed input. The exact check output is in
[`evidence/independent-checks.log`](evidence/independent-checks.log).

## Inventory reconstruction and bijection

I ran the trusted `tools.k_rule_inventory.inventory_verification` against
`/reference/k-proof`. `prove.sh` selects `VERIFICATION`; the local
verification-module closure declared in `verification.k` is exactly
`["VERIFICATION"]`. The imported operational module `MPY` is supplied by
`semantic.k` and is not an additional locally declared module in
`verification.k`.

The reconstruction found 11 rules. For every entry I independently checked
that:

- the recorded start and end lines select the exact frozen source text;
- whitespace normalization and SHA-256 reproduce `normalized_sha256`;
- `source_rule_id` is exactly `rule-` followed by that hash;
- IDs are unique; and
- canonical JSON hashing of the ordered rule documents reproduces the whole
  inventory hash.

The frozen `verification.k` hash is
`0bef4aaff8cd41856c484371283b3a00cbe6ea0399050557fc3d1be25eb1ec3a`.
The reconstructed inventory hash is
`2c31d4f86cf6d3216794496df5040f95f97f451aa01ab5ef3cebb274c122fdd5`.

The protected manifest contains exactly those 11 unique IDs, in exactly the
same order, and binds the same inventory hash. There are no omissions,
duplicates, extra IDs, reordered IDs, span changes, or hash changes. The full
reconstruction is in
[`evidence/inventory-reconstructed.json`](evidence/inventory-reconstructed.json).

## Independent classification judgment

The frozen source declares each affected symbol as a K `[function]`. The
following is my classification from the rule text, the source program, and the
operational rules in `semantic.k`, rather than from the protected rationales.
Each displayed hash is also the suffix of its exact `source_rule_id`.

| Lines | Normalized source hash | Independent class | Judgment |
|---|---|---|---|
| 15–17 | `65e45ee166a36988401c233ab025a60dc5f7ca33b995557930a684acccdd79f1` | `DEFINITION` | Recursive equation for the new string summary `sequenceFrom`; it appends the current index and advances it. |
| 18–19 | `466c7c2be7c323e7fc25fae5fb18a9313e58b62baca45d7a17e64da30511bc69` | `DEFINITION` | Base equation for `sequenceFrom`; it returns the accumulator after the index passes the bound. |
| 21 | `bd2d5c2971252b0333e76ed865a392d7c7611daa95430d0e3b7113bbfa086403` | `DEFINITION` | Negative-input equation for the new top-level summary `sequence`. |
| 22 | `955fb0e47bc2733ce751bd16d68fe9cd228472af7797f42840d90a3ac1bdde00` | `DEFINITION` | Nonnegative-input equation defining `sequence` through `sequenceFrom`. |
| 24–25 | `9a07e06ad4b37739dc081e70175fbe9fa0cc141044523aac86a6736a3d375aa9` | `DEFINITION` | Recursive equation for the new final-index summary `indexAfter`. |
| 26–27 | `4b2d1db7ff9a010e4cc93841df519bedb924d9d7353da56bec38f801e3c18c86` | `DEFINITION` | Base equation for `indexAfter`. |
| 29–30 | `4be6d834df0a8ee3bb5d58a2a5bb59649a9cae271802ea3bd5625e3ac813ad59` | `DEFINITION` | Macro-like definition of the named loop-condition AST. |
| 32–39 | `349054d85fb69df15a640b595d022a79d84dbe678a7d13629b1d43873ffb9b01` | `DEFINITION` | Macro-like definition of the named two-statement loop-body AST. |
| 41–49 | `fb6161a8b67f7d15461a9dae303daf34e9e07a0cb359e367e07282d505d6e0cb` | `DEFINITION` | Macro-like definition of the complete function-body AST. |
| 51 | `846ae1a1be4929fd20806aa97162cfc70d521aa036599a1adb0e3ea4011bc257` | `DEFINITION` | Definition of the named function value from its parameter and body. |
| 52–53 | `7750c9cf52bae245157c0466c48fb5cd0fc1f39fd67e1b1998b7fd35d7c71e14` | `DEFINITION` | Definition of the named module AST containing `string_sequence`. |

The first six rules introduce and exhaustively define three summary functions.
For K integers, each pair of guards is disjoint and exhaustive. The recursive
cases strictly advance `I`, and their changes agree with the frozen operational
semantics:

- `While` evaluates `i <= n`; the true branch runs the body and loops, while
  the false branch stops.
- The body evaluates left-to-right, stores
  `result + " " + str(i)`, and then stores `i + 1`.
- `str(i)` is operationally `Int2String(i)`.

Thus `sequenceFrom` and `indexAfter` describe exactly the two changed
environment entries at the loop boundary. `sequence` mirrors the source's
negative return, nonnegative initialization to `"0"` and `1`, and the same
loop summary.

The remaining five rules do not replace `exec`, `eval`, assignment, control,
return, call, or any other operational transition. They expand newly named
proof terms to the exact AST in frozen `solution.mpy`: the inclusive `<=`
condition, append-then-increment body, negative early return, initial values,
function parameter/name, and module wrapper all match.

Useful boundary and counterfactual witnesses include `n = -1` for the negative
branch, `n = 0` for the zero-iteration path, and `I = N = 1` for the inclusive
loop boundary. Changing `""`, the initial `"0"`/`1`, `<=`, the appended index,
or the increment is observable on one of these witnesses. A fresh K rebuild
produced `""`, `"0"`, `"0 1 2 3 4 5"`, and
`"0 1 2 3 4 5 6 7 8 9 10 11 12"` for inputs `-3`, `0`, `5`, and `12`;
the frozen claims independently rebuilt to `#Top`. This is corroborating
operational evidence, not a substitute for the source classification.

No inventory rule has a `simplification` attribute. No rule is an ordinary
operational rule. No rule purports to be a previously proved derived lemma,
so the special two-stage derivation requirement is not invoked. No rule states
an additional fact about an existing domain operation. Consequently there is
no hidden or irrelevant `DOMAIN_LEMMA`, and the true domain-lemma set is empty.

## Generation producer provenance

The producer bundle contains exactly three regular files:
`klean_export.py`, `klean.py`, and `source-manifest.json`.

| Producer | Recomputed SHA-256 |
|---|---|
| `klean_export.py` | `235473b1324d2b203cb2a49ab94e36fb7c300084d506a57fca2228381f1bdec0` |
| `klean.py` | `ddec66db87398459ff0c2b5aad7121fe1029b58b8d576db4203c68bf5b647d13` |

Both hashes match the source manifest and the corresponding
`exporter_sha256` / `klean_py_sha256` fields in `generator-manifest.json`.
Both manifests bind generator image
`sha256:e18301a8220fb0b62fabf56feffcb5e621049daa7c7a0b79eacb60cae5e57fda`.
The producer path signed in `/audit-input.json` is keyed by the same image
digest, and its full tree hash is the matching
`363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0`.
The required producer-source infrastructure gate therefore passes.

## Deterministic Stage 4 and fixed-target identity

I called `tools.klean_preflight.check_generation` with
`PYTHONPATH=/reference`, the frozen K workspace, protected discovery manifest,
selected generation, and trusted toolchain lock.

The initial Lake subprocess exposed an audit-sandbox PID-namespace issue:
Lean 4.22 asks for `/proc/<getpid>/exe`, while this sandbox reports an inner
PID from `getpid()` but exposes `/proc` from the outer namespace. I preserved
that failure and used the narrow preload shim in
[`evidence/outerpid.c`](evidence/outerpid.c) to return the outer PID exposed by
`/proc/self`. The shim changes no proof input or preflight logic. With it, the
direct `check_generation` call completed successfully. The full caller and
subprocess output are preserved in
[`evidence/run_preflight.py`](evidence/run_preflight.py),
[`evidence/preflight-rerun-success.log`](evidence/preflight-rerun-success.log),
and [`evidence/preflight-build-full.log`](evidence/preflight-build-full.log).

The returned result is byte-for-data identical to both the selected
`preflight.json` document and the `stage4_preflight` object signed in
`/audit-input.json`:

- status: `KLEAN_NO_OBLIGATIONS`;
- obligation count: `0`;
- target: `null`;
- designated sorry count: `0`;
- trust declaration count: `53`;
- `lake clean`: exit 0, empty-output hash;
- `lake build`: exit 0, output hash
  `74cd9720e59c0e508a4fe835eea8fc577296d5cbd3d881712a0abf52e0680140`.

The generator toolchain exactly equals the trusted lock. The generator
manifest binds the generated tree and the obligation-map hash
`cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`.
The export result also binds the frozen input, discovery manifest, generated
tree, and trust-inventory hash.

Most importantly, the mathematical classification above independently yields
no domain rules. `input-manifest.json` therefore correctly records
`source_rules: []`, and `obligation-map.json` is exactly:

```json
{
  "obligations": [],
  "schema_version": 3,
  "source_rules": [],
  "trust_parameters": []
}
```

This is the exact source-rule/obligation bijection. There are no omitted or
duplicated obligations, no irrelevant or weakened obligation, and no conjunct
that could be vacuous. The generator's expected target definition is absent;
independent target parsing finds no target declaration; and the generator
manifest, preflight result, and signed audit input all record `target: null`.
The fixed generated target is therefore consistently the absence of a target,
as required for a genuine no-obligation result.

The generated project contains 53 allowlisted executable-semantics trust
declarations, but no proposition target or proof. They cannot discharge a
nonexistent obligation and do not turn an empty domain set into a proof claim.

## Stage 5

Stage 5 proof checks are intentionally inapplicable. The signed mode is
`CLASSIFICATION_ONLY`, `/candidate` does not exist, and the signed Lean
workspace, Lean invocation, and Stage 5 result fields are all `null`. This is
exactly the required state for `KLEAN_NO_OBLIGATIONS`; there is no candidate
that could shadow a target, introduce trust escapes, or prove a weakened
variant.

## Evidence index

Raw commands, outputs, failed and successful preflight attempts, reconstructed
inventory, live K results, and exact audit helper sources are indexed in
[`evidence/COMMANDS.md`](evidence/COMMANDS.md).

VERDICT: PASS
LEGITIMACY: LEGIT
