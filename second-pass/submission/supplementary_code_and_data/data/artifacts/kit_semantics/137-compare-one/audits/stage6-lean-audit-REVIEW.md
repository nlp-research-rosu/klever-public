# Independent Stage 3–5 Audit: HumanEval 137-compare-one

## Outcome

The selected `KLEAN_NO_OBLIGATIONS` result is legitimate. The local verification-module closure contains seven rules, all seven are genuine definitions of fresh summary or proof-term symbols, and none is a domain lemma. Consequently the true domain-lemma set is empty, Stage 4 correctly generated no obligations and no target, and the classification-only audit correctly has no Stage 5 candidate.

## Scope and audit mode

The launcher environment and `/audit-input.json` both record:

- problem: `137-compare-one`;
- condition: `kit-semantics`;
- semantics mode: `SUPPLIED_SEMANTICS`; and
- audit mode: `CLASSIFICATION_ONLY`.

`/candidate` is absent, including as a symlink. The Stage 5 proof-build, `Proof.final`, axiom-accounting, and target-parameter bridge procedures therefore do not apply. Their absence is required here rather than an omitted audit step.

I treated the Stage 1 and prior-review content as evidence only. I did not rely on a prior verdict or classification, did not execute either provenance `prove.sh` or its parser script, and used the trusted inventory and preflight implementations under `/reference/tools` for the required mechanical checks.

## Frozen-input integrity

I independently re-hashed all launcher-bound trees and the entire Stage 1 regular-file set. Every comparison succeeded:

| Binding | Observed SHA-256 |
|---|---|
| Stage 1 selected workspace tree | `1c2e2c466d8330d2c39b9d411a6c24afb1d5f36c2c8027ddac60b19788b4bb5d` |
| Stage 1 deterministic-export tree | `4e88755f7020448a98413367cd38dd934918d2199f48168b7fb88a4728c6bcc8` |
| Stage 2 selected audit tree | `1b49c90da97b4cf978edcccb398b7e47108cc6454cddd2ecfc83d3da296ff518` |
| Protected Stage 3 manifest | `230661ce4433aa0d4cd266082f92dec2afbd848f00e2b99fa9cfd2d7645063a1` |
| Selected Stage 4 generation tree | `d03becced0a796ee57dcdcb9378a6b53634760215e6090951e10f0d3047c7fef` |
| Generated Lean project tree | `a168e80c0377793daf4242deb67c8a9bc6e8337b462a977f9c66627fb93feda4` |
| Producer-source bundle tree | `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e` |

All 817 Stage 1 regular-file names and hashes exactly match `stage1_source_hashes`; there are no missing, extra, or mismatched files. The frozen `verification.k` hash is `c175ccb011bb85e7be021670f935620db8576c0b03bdc33c7c99fb942debc817`.

## Producer authentication

This gate passed before I judged Stage 4. The mounted producer bundle has exactly `source-manifest.json`, `klean_export.py`, and `klean.py`. The observed producer hashes are:

- `klean_export.py`: `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07`;
- `klean.py`: `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d`.

They exactly match both the source manifest and `generator-manifest.json`. The source manifest and generator provenance both name image `sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`, and the image key is exactly the basename of the producer-source path recorded in `/audit-input.json`. The complete producer bundle tree also matches the launcher's recorded hash. There is no producer-provenance infrastructure error.

## Inventory reconstruction and bijection

Running `tools.k_rule_inventory.inventory_verification` on the frozen workspace selected `VERIFICATION` as the verification module. Its local import closure contains only that module; `MPY` is supplied from a required external K file and is not another local module in `verification.k`.

The trusted inventory reconstructed seven source spans. I independently re-sliced those inclusive line spans, normalized each with whitespace joining, re-hashed each source string, re-derived each `source_rule_id` as `rule-<normalized_sha256>`, and re-hashed the canonical ordered rule-document list. Every text, span, hash, and ID check passed.

| Lines | Exact source rule ID | Attributes | Independent class |
|---|---|---|---|
| 8–25 | `rule-96a2b157eb261582571b58f8f4baca708344f5f934ab0dfd73a528a2cf06f6c3` | none | `DEFINITION` |
| 30 | `rule-6350669bfe107188f21ff8bcfb62369235f77456d1376006cebb32ea27e6f927` | none | `DEFINITION` |
| 31 | `rule-cb4eededb7164c4ac333f7b361070f4e5798d337f589fa27bb6097cb9ae3ab26` | none | `DEFINITION` |
| 32 | `rule-d42ee113ac1215c861819fe9dcefdf1fa290428f59dbaaed2952c8129135abb6` | none | `DEFINITION` |
| 37–38 | `rule-e2ace12cf9853e8f73043e00ef4021593fc0c87ff79e215abe9a4e1766c7adad` | none | `DEFINITION` |
| 39–41 | `rule-720e10405d2c95cf48ae7c5ffc80b5602085ca1a1b5cd84bc13950733f69d925` | none | `DEFINITION` |
| 42–44 | `rule-34489340280ac69ec4b5418b1966f3a449892bb755759a19583a03a3dd033c01` | none | `DEFINITION` |

The resulting whole-inventory hash is `1cd9fe93dd4e5f480fc8b0770b4cb85ca6a17dd249f6990ca5b632e97f3c8833`, exactly the protected Stage 3 value. The seven Stage 3 entries have the same IDs in the same order and are unique. There are no omitted, duplicated, extra, reordered, changed, or unclassified identities. Because all seven attribute lists are empty, the simplification-class restriction is satisfied vacuously.

## Independent classification judgment

### `solutionModule()`

The first rule is a nullary equation for a fresh `[function, total]` symbol whose right side is a `Module` constructor tree. It names a proof term and does not rewrite a `<k>` configuration, a call, a comparison, or any other source-program execution. The tree contains the two `isinstance(..., str)` branches, comma-to-dot replacements, `float` calls, two ordered comparisons, original-argument returns, and final `None`, exactly as in `solution.py`.

As an independent identity check, I evaluated `solution.mpy` and `solutionModule()` through the frozen compiled definition, using an audit-created parser for the latter. Both final KORE streams had SHA-256 `5fe0e823b82b904fe444236de38e5ebd2a04213a75393e7d0106e25181fa4ccc`. This is a named proof-term definition, not an operational bridge or domain fact.

### `numericValue`

The next three rules are constructor equations for the fresh summary symbol `numericValue`:

- on `Int`, the source takes the non-string branch and assigns the original integer;
- on `Float`, it likewise assigns the original float; and
- on `str(C)`, it yields `decStrToF(replaceC(C, 44, 46))`.

The string equation exactly follows the supplied operational semantics. `methods.k` implements the actual one-character call `replace(",", ".")` as `replaceC` with character codes 44 and 46, while `float.k` implements `applyBuiltin("float", str(CS), .Vals)` as `decStrToF(CS)`. The equation names that already supplied computation's value; it neither asserts an arithmetic property nor replaces program execution.

### `expectedCompare`

The last three rules define the fresh result-summary symbol `expectedCompare`. Let

- `p = applyCmp(">", numericValue(A), numericValue(B))`; and
- `q = applyCmp(">", numericValue(B), numericValue(A))`.

Their guards and results are `p -> A`, `not p and q -> B`, and `not p and not q -> noneV`. These cases are pairwise disjoint and exhaustive over the Boolean results. They exactly mirror the source's sequential control flow: return `A` on the first greater-than test, otherwise test the reverse and return `B`, otherwise return `None`. This remains an exact control-flow summary even for counterexamples to trichotomy such as an opaque/NaN-like comparison where both directions are false; no hidden antisymmetry, equality, or real-arithmetic lemma is assumed.

The supplied semantics dispatches `applyCmp(">", ...)` for Int/Int, Float/Float, and both mixed Int/Float directions. Thus these equations define what result name the specification uses; the Stage 1 reachability claims still have to execute the source body to establish equality with that summary. Swapping either returned original argument, changing either comparison direction, hard-coding a result, or changing the string normalization would immediately disagree with the frozen program. The rules are consequently definitions, not mislabeled domain lemmas.

### Classification totals

- `DEFINITION`: 7
- `OPERATIONAL_RULE`: 0
- `PROVED_DERIVED_LEMMA`: 0
- `DOMAIN_LEMMA`: 0

There is no claimed derived lemma requiring an earlier isolated Stage 1 proof, and no source/postcondition-relevant domain fact has been hidden in another category.

## Stage 4 structural and mathematical audit

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`, the three required paths, and `/reference/klean-toolchain.lock.json`. The first direct invocation exposed an audit-sandbox PID-namespace incompatibility: Lean tried to locate itself through `/proc/<getpid()>/exe`, which is absent in this namespace although `/proc/self/exe` works. I documented that failed output, compiled a narrow `readlink` compatibility shim that redirects only `/proc/*/exe` to `/proc/self/exe`, and passed it only to the Lake child processes. No K, Lean, generated, candidate, manifest, or trusted-tool source was modified.

With that environment compatibility in place, the required function completed and returned:

- status `KLEAN_NO_OBLIGATIONS`;
- Stage 1 hash `4e88755f7020448a98413367cd38dd934918d2199f48168b7fb88a4728c6bcc8`;
- Stage 3 hash `230661ce4433aa0d4cd266082f92dec2afbd848f00e2b99fa9cfd2d7645063a1`;
- generated-tree hash `a168e80c0377793daf4242deb67c8a9bc6e8337b462a977f9c66627fb93feda4`;
- obligation count 0;
- target `null`;
- `lake clean` exit 0; and
- `lake build` exit 0 with output hash `598adc4b37b14bcd33124c2d7469739b1445ca2f6d0e9e1f825c6a313cb0daf5`.

The returned object exactly equals the recorded `preflight.json` object and the launcher's `stage4_preflight` object. All independent manifest bindings also pass: Stage 1, Stage 3, `verification.k`, generated tree, obligation map, trust inventory, pinned toolchain, export result, generator provenance, and producer provenance.

The independently classified domain set is empty. Correspondingly:

- `input-manifest.json.source_rules` is `[]`;
- `obligation-map.json.source_rules` is `[]`;
- `obligation-map.json.obligations` is `[]`;
- `obligation-map.json.trust_parameters` is `[]`;
- both manifest obligation counts are zero; and
- the obligation-map hash is `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`.

This is an exact empty-set bijection. There can be no omission, duplicate, weakening, irrelevant obligation, or vacuous conjunct within an empty list. Importantly, the generator did not turn the empty conjunction into `True`: `tools.klean_export.expected_target_definition` returns `None`, `target_statement` returns `None`, every generator/preflight/launcher target is `null`, and `Klean137CompareOne/Lemmas.lean` contains an empty namespace with no proposition or theorem declaration.

## Deterministic regeneration

I regenerated Stage 4 below `/tmp/audit-work` using copies whose hashes exactly equal the authenticated generation-time `klean_export.py` and `klean.py`, the pinned toolchain lock, the frozen Stage 1 workspace, the protected Stage 3 manifest, the problem ID, and the recorded generator image ID.

The regenerated generated-project tree is byte-for-byte identical to the selected generated tree and has the same `a168e80...feda4` digest. The regenerated generator manifest, trust inventory, export result, and obligation map are byte-identical to the selected files. The regenerated input manifest differs only in `required_k_files`' unavoidable absolute mount prefix (`/reference/k-proof` during audit versus `/frozen-k` in the generator image); after removing that prefix, the ordered relative file list and every other JSON field are identical. This path-local provenance difference does not affect the generated project, target, obligation mapping, or any bound content hash.

## Target and Stage 5 identity

There is no generated target to weaken, duplicate, shadow, or prove vacuously. Because the legitimate domain set is empty, this absence is the required Stage 4 result. The classification-only launcher record has `lean_workspace`, `lean_invocation`, and their hashes set to `null`, and no `/candidate` is mounted. Therefore there is no `Proof.final`, no target parameter, and no candidate `def` or axiom list to reconcile. A Stage 5 proof in this mode would itself have been an error; none exists.

## Evidence index

- `evidence/01-context-hashes.txt`: launcher mode, tree hashes, 817-file check, and inventory totals.
- `evidence/inventory-reconstruction.json`: full trusted inventory with text, spans, attributes, hashes, IDs, and whole hash.
- `evidence/02-inventory-independent-checks.txt`: independent span/hash/ID recomputation and classification record.
- `evidence/03-producer-authentication.txt`: producer files, hashes, file set, image ID, and bundle hash.
- `evidence/04-preflight.txt`: failed ambient run, compatibility diagnosis, exact rerun command, and returned evidence.
- `evidence/05-obligation-target-checks.txt`: all manifest bindings, empty bijection, and target absence.
- `evidence/06-deterministic-regeneration.txt`: authenticated regeneration command and byte/tree comparisons.
- `evidence/07-ast-identity.txt`: independent KORE identity check for `solutionModule()`.
- Copied immutable JSON records and both audit-created compatibility/parser sources are also under `evidence/`.

VERDICT: PASS
LEGITIMACY: LEGIT
