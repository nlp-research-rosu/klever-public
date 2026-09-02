# Independent Stage 3/4 audit: HumanEval 19-sort-numbers

## Scope and result

The launcher and `AUDIT_MODE` both select `CLASSIFICATION_ONLY` for condition
`kit-semantics` and semantics mode `SUPPLIED_SEMANTICS`. The signed launcher
resolution digest recomputes to
`4a16c1d07b6dde1d134b42a9850e77b3189522ab1f05f965d60ba38d101c115c`,
and the `/audit-input.json` and `/audit-output/audit-input.json` copies are
byte-identical. Stage 5 is therefore not applicable. The launcher has no Stage
5 result or Lean workspace/invocation hashes, `/candidate` is absent, and the
fixed Stage 4 target is null.

I did not rely on the selected Stage 2 review, prior classifications, comments,
or prior PASS-like results. I reconstructed the inventory with the trusted
`tools.k_rule_inventory` implementation, classified the frozen rules from
their source and the supplied operational semantics, independently checked
every content binding, and reran the trusted Stage 4 preflight.

The complete commands, command sources, and raw outputs are in
`/audit-output/evidence/`. In particular:

- `COMMANDS.md` records the exact commands;
- `producer-provenance.log` records the producer hashes and image provenance;
- `structural-checks.log` contains the reconstructed inventory and every
  structural/hash comparison (`all_checks_pass: true`);
- `operational-source.log` contains the line-numbered frozen source, main
  claim, and relevant supplied operational rules; and
- `fresh-preflight-compat.log` is the returned evidence from the fresh trusted
  `tools.klean_preflight.check_generation` run.

## Producer provenance gate

I hashed the generation-time producer sources before judging Stage 4:

| Producer | Observed SHA-256 | Required SHA-256 |
|---|---|---|
| `klean_export.py` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` | same |
| `klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` | same |

These values match both `source-manifest.json` and
`generator-manifest.json`. The producer bundle contains exactly those two
files plus `source-manifest.json`; its independently recomputed tree hash is
`388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`,
matching the signed audit input.

The immutable generator image ID is
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`.
It agrees between the generator manifest and source manifest, and its digest
component is exactly the producer-bundle path component recorded in the audit
input. This gate passes; there is no producer-source infrastructure error.

## Inventory reconstruction and manifest bijection

The trusted inventory selected module `VERIFICATION`. Its local
verification-module closure is exactly `["VERIFICATION"]`; imported `MPY` is
defined in the separately required supplied-semantics files rather than as a
local module in `verification.k`.

The reconstruction found exactly six rules. For each, I re-extracted the
physical source span, normalized it with the inventory algorithm, recomputed
the normalized SHA-256, and recomputed `source_rule_id = "rule-" + hash`.

| Order | Frozen span | Normalized SHA-256 / source identity | Attributes | Independent class |
|---:|---:|---|---|---|
| 1 | 8–27 | `e16b3241b5675fa807f7287fd8db8e3e71b24e7b7b130da84250149d7e166ca8` | none | `DEFINITION` |
| 2 | 30–40 | `5692cca793a2159c984323ca422a6e908349e27acd9f001a5718828b318b0c67` | none | `DEFINITION` |
| 3 | 45–55 | `9b835db36ee25ad7bebed412bf86771e90764ac448f5b8c18671f2ffdbd65747` | none | `DEFINITION` |
| 4 | 58–58 | `e47e06c71c6d44b8fb7a5471bbd23d7a1afd8a6499d2077f4bfcae6064ac294c` | none | `DEFINITION` |
| 5 | 59–60 | `fde315ba45836b08d40df28f6a9f608e17b9e5b5a70d717c5ecc140209f4ba29` | none | `DEFINITION` |
| 6 | 64–70 | `ea52da411b9ddcd44409f34ea1ec779091c47f11ec46ca66f711f60bd835a10b` | none | `DEFINITION` |

Every re-extracted span is byte-for-byte equal to the rule text recorded by
the trusted inventory. The whole rule-list inventory hash independently
recomputes to
`20c8738205fc5ef28c7bbff6183179d6c8d11652f47801ab429697222a78de1b`.

`lemma-discovery.json` has exactly the same six identities in exactly this
order and records the same inventory hash. The manifest has no duplicates,
omissions, extras, reordered identities, changed hashes, or unaccounted
classifications. Its file hash is
`820420814a05a5b97a226a2c54e5626a33d8c8060720c7eba1eaa80b53b3a87f`,
matching the signed audit input and every Stage 4 provenance binding.

## Independent classification judgment

The first two rules are exact named closure macros:

- `numberKeyClosure` expands to the `_number_key` parameter, body, and module
  environment shown by the translated frozen `solution.mpy`. Its tuple and
  `index` expression exactly match the source helper.
- `sortNumbersClosure` expands to the `sort_numbers` parameter, body, and
  module environment shown by the translated source. It preserves the nested
  `numbers.split()`, `sorted(..., key=_number_key)`, and `" ".join(...)`
  expression.

They name exact closure values. They do not rewrite a call, skip a function
frame, alter a continuation, or assert a fact about the result, so both are
`DEFINITION`, not operational bridges or domain lemmas.

`isNumberWord` is the defining total equation for a fresh predicate: it is
exactly the disjunction that its argument equals one of the ten numeral-word
values. It does not assert an ordering, permutation, key, or result property
about an existing symbol. It is a `DEFINITION`.

The two `allNumberWords` rules are the empty base case and strict-tail
constructor recurrence for another fresh predicate. Together they define the
claim's input-domain predicate and are `DEFINITION`s.

`expectedSortNumbers` is a fresh named summary whose sole equation expands to
the exact operational result term:

`str(joinCodes(" ", sortKeyVS(splitWS(CS), numberKeyClosure)))`.

This matches the supplied operational path:

1. the no-argument string `split` rule allocates
   `list(splitWS(CS, .IntSeq, .ValSeq))`;
2. supplied `sorted(..., key=KV)` allocates
   `list(sortKeyVS(VS, KV))`; and
3. supplied string `join` returns `str(joinCodes(separator, VS))`.

The supplied semantics deliberately keeps proof-mode `sortKeyVS` opaque while
the operational `sorted` rule returns that same symbol. The local
`expectedSortNumbers` rule neither defines nor assumes that sorting primitive's
mathematical correctness; it only names the exact symbolic operational result.
Accordingly it is a `DEFINITION`, not a result-property `DOMAIN_LEMMA`.
The distinction matters: this K claim is an execution theorem relative to the
supplied sorting primitive, not a new local axiom that the primitive is a
stable ascending sort.

No inventory entry is an ordinary execution/observation rule, so the true
`OPERATIONAL_RULE` set is empty. No inventory entry was first proved as an
exact bridge-free claim and later installed, so the true
`PROVED_DERIVED_LEMMA` set is empty. Most importantly, no rule states an
additional mathematical fact about sorting, keys, permutations, or the final
postcondition, so the true `DOMAIN_LEMMA` set is genuinely empty. There are no
explicit `simplification` attributes in the inventory; all six equations are
definitions in any event.

The independent classification therefore agrees exactly with the protected
Stage 3 classification.

## Recorded content hashes

The signed resolution's mounted-content hashes all recompute:

| Content | Recomputed and recorded hash |
|---|---|
| Full Stage 1 workspace tree | `8297db213157f04f55e67ee749ef0d92625dcaee72901773ae97fc39d03d0ba3` |
| Stage 1 deterministic-export tree | `277f6bb9b6d67b661146be368592db5d689afdf9c8752700f7429f2938b1fffe` |
| Stage 1 per-file map | 773 files, map digest `8296037a0aa7dcaa56bd6d09b8b02b64253fb0b0806533cc11b8bc4a330f2475`, zero mismatches |
| Selected Stage 2 tree | `9eae841f22a878385ec21b2fcb5e37d22fadc71f4dcee6e36a32469dbebd9f82` |
| Selected Stage 4 tree | `d5ad53419a6f50d924387ec3bcd65233db936d738cb51b093de7ce0c1254d062` |
| Generated project tree | `41d021d91ac53dd8ce72ade2c2e24aab901a3dd5337f159e4fd95056ecd1e947` |
| Producer source tree | `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e` |

The Stage 2 and Stage 4 selection artifact hashes equal their independently
recomputed trees. The Stage 1 verification file hash is
`b73cb66e355f82c46d6d3c2e6c8c86a06b5f401195ae4e74ebe414ba96ba5731`.
The input manifest, generator provenance, export result, preflight record, and
signed audit input all bind to the recomputed Stage 1, discovery, inventory,
generated-tree, obligation-map, and trust-inventory hashes. The generator
toolchain object exactly matches `/reference/klean-toolchain.lock.json`.

## Deterministic Stage 4 generation

The independently classified domain set is empty. The Stage 4 input manifest
therefore has zero `source_rules`. The generated `obligation-map.json` has:

- zero source rules;
- zero obligations;
- zero trust parameters; and
- SHA-256
  `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`,
  exactly as recorded by the generator manifest.

Thus the source-rule/obligation mapping is an exact empty bijection. There can
be no omitted, duplicated, weakened, irrelevant, or vacuous conjunct in that
mapping. Trusted target extraction returns null; the generator manifest,
launcher resolution, prior preflight record, and fresh preflight all also
record a null target. `Lemmas.lean` contains no theorem or target declaration.
There is no changed or alternate generated target.

The generated project contains 49 executable/collection-hook trust
declarations, all mechanically reconciled with `trust-inventory.json`; the
fresh preflight reports `trust_declaration_count: 49` and rejects proposition
trust independently. Since the true obligation set and target are empty,
these declarations are not assumptions of a generated theorem.

I invoked `tools.klean_preflight.check_generation` with
`PYTHONPATH=/reference` and exactly these inputs:

- `/reference/k-proof`;
- `/reference/lemma-discovery.json`;
- `/reference/klean-generation`; and
- `/reference/klean-toolchain.lock.json`.

The first invocation exposed an audit-sandbox PID-namespace issue before any
Lean build: Lean attempted `readlink("/proc/<namespace-pid>/exe")`, but the
mounted `/proc` did not contain that PID. The raw failure is preserved in
`fresh-preflight.log`, and `lean-path-diagnostic.log` records the failing
lookup. I applied the recorded narrow compatibility shim
`proc_exe_compat.c`, which changes only such a lookup to
`/proc/self/exe`. With it, both `lean` and `lake env lean` identify the pinned
Lean 4.22.0 commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`.

The exact trusted preflight was then rerun successfully. Its returned evidence
records:

- status `KLEAN_NO_OBLIGATIONS`;
- `lake clean`: exit 0, empty output;
- `lake build`: exit 0, output hash
  `959fd3c0903bc7923bf9a8be6ece2baebed63851d5e7cf88e27fff5753bb6f81`;
- all nine generated build steps completed successfully;
- obligation count 0;
- target null;
- the exact recomputed Stage 1, discovery, and generated-tree hashes; and
- no generated `sorry`.

The compatibility shim affects only discovery of the running executable path;
it does not alter the copied project, Lean sources, elaboration, trust scan,
target extraction, or proof terms. The trusted preflight's before/after
snapshots also confirm that all frozen inputs remained unchanged.

## Stage 5 and final judgment

Because the independently true domain-lemma set is empty,
`KLEAN_NO_OBLIGATIONS` is the correct Stage 4 outcome. Consistently, there is
no generated target, no launcher Stage 5 result, and no `/candidate` project.
The proof-mode target, candidate, `#print axioms Proof.final`, and
operational-bridge parameter checks are inapplicable rather than omitted.

The Stage 3 classification is complete and correct, and the selected Stage 4
generation is deterministic, provenance-bound, structurally exact, freshly
buildable, and mathematically appropriate for the genuinely empty domain set.

VERDICT: PASS
LEGITIMACY: LEGIT
