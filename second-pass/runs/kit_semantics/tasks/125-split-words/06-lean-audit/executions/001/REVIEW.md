# Independent audit: `125-split-words`

## Scope and outcome

The launcher and `AUDIT_MODE` both select `CLASSIFICATION_ONLY` for condition
`kit-semantics` and semantics mode `SUPPLIED_SEMANTICS`. The Stage 3
classification and deterministic Stage 4 no-obligation result are legitimate.
There is no Stage 5 candidate to audit, as required by this mode.

I did not rely on the selected Stage 2 verdict, the Stage 3 rationales, prior
logs, or generated comments as authority. The rule inventory was reconstructed
from frozen `verification.k` with the trusted inventory implementation, each
rule was reclassified from its actual text and active operational semantics,
and Stage 4 was checked both with the trusted preflight and an independent
manifest/bijection checker.

The qualification is an independently confirmed boundary in the supplied K
semantics: its whitespace predicate recognizes only codes 9, 10, 13, and 32,
whereas the source runtime also treats vertical tab (11) as whitespace. This is
a supplied-model adequacy concern, not a hidden Stage 3 domain lemma and not an
omitted Stage 4 obligation.

## Producer provenance and immutable inputs

The mandatory producer-source check passed before Stage 4 was judged:

| Item | Recomputed SHA-256 | Recorded result |
|---|---|---|
| `generation-tools/klean_export.py` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` | Exact match in `source-manifest.json` and `generator-manifest.json` |
| `generation-tools/klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` | Exact match in `source-manifest.json` and `generator-manifest.json` |
| Producer-source tree | `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e` | Exact match in `/audit-input.json` |

The immutable generator image ID is
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`.
It is identical in the source manifest and generator manifest, and its digest
is the basename of the producer-source path recorded by `/audit-input.json`.
There is therefore no producer-source infrastructure error.

All launcher and nested manifest hashes were independently recomputed with the
appropriate trusted hash algorithm:

| Artifact | Recomputed hash |
|---|---|
| Pipeline Stage 1 workspace | `8c168d68fc601510217060b815743335d181781116c9cf32630f14cb7ac63ee4` |
| KLean frozen Stage 1 export | `ca217ad7bc611c928a843efee1ebd382ad7ff1e15374488fb5ed203a17bbbd4d` |
| Stage 2 selected audit | `265d6ac8e2fb30f3861577cd8c55edfe18dc15862474513452dd201b8e3e37f9` |
| Stage 3 discovery file | `2b1934a757f0f4a8b0a921d3d91cf5887e4fe9d64313b60cac7405933a474c8b` |
| Stage 4 selected generation | `ef6a8b653af7f0a6722d5b880c4fc358110c6a56052592bf0e8e0a313ffb72fd` |
| Generated Lean tree | `9eb9a540c8122e674bfc3b3f1a58deb226c82c99ab93cda2679cc297db928364` |
| Obligation map | `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048` |
| Trust inventory | `1f1805fbb42ae82bacfd0e92af048c111a573bad41b1ab9676ea2dac00256e97` |

The complete set of 821 Stage 1 regular files bijectively matched the 821
per-file hashes in `/audit-input.json`: no missing, extra, or changed file was
found. The selected artifact hashes, input manifest, generator provenance,
export result, recorded preflight, and launcher values all reconcile with the
same recomputed inputs. Full results are in
`evidence/01b_hash_recomputation_corrected.log`.

An earlier preserved hash attempt used the audit-contract tree framing instead
of the pipeline-v3 framing for four pipeline artifact fields. It consequently
reported four algorithm mismatches while all per-file hashes matched. The
corrected run calls the trusted `pipeline_contract.sha256_tree` used for those
fields and exits successfully; the distinction and commands are recorded in
`evidence/COMMANDS.md`.

## Canonical rule inventory reconstruction

Trusted `tools.k_rule_inventory.inventory_verification` resolved the local
verification-module closure to exactly `VERIFICATION`. Its results are:

- `verification.k` SHA-256:
  `c30fe9f1c88960cc6626aa2e6895fe1d51c9e4016bffcedd3acd4e3b31c648ea`;
- rule count: 2;
- inventory SHA-256:
  `3a844e06bb98623cebec0bc8d33bff0ee48cd1eea0e9f7e65cb1d75248df894a`.

For each rule I independently sliced the reported physical source span,
normalized it with whitespace joining, hashed the normalization, rebuilt
`source_rule_id` as `rule-<hash>`, and recomputed the canonical JSON inventory
hash:

| Order | Span | Normalized hash / source identity | Rule attributes |
|---:|---:|---|---|
| 0 | 8–75 | `rule-f119e21baa3b2f3f958217ae41d31a07cd861a77cd3db592e16dcd4824e16c2b` | none |
| 1 | 80–93 | `rule-fe0451a4b26ebe826c1c4ca94a4c96c37fda6ea9eb2e8665a649f842a712f5cb` | none |

Every source span, normalized hash, source ID, and the whole inventory hash
matched. The Stage 3 document has exactly the same two unique identities in
the same order. There are no omissions, extras, duplicates, reordered
identities, changed hashes, or unaccounted classifications. The full canonical
documents and consistency checks are in
`evidence/02_inventory_reconstruction.log`.

## Independent classification judgment

### `splitWordsBody`: `DEFINITION`

The first rule gives a sole, unconditional equation for the nullary
`[function,total]` symbol `splitWordsBody : Stmts`. Its right-hand side is the
complete constructor tree corresponding to the source solution: assign
`parts = txt.split()`, take the whitespace branch when appropriate, then the
comma branch, otherwise return the left-associated sum of the thirteen
`count` calls.

This rule does not match an operational cell, select a binding, return a value,
or bypass a continuation. It is a named proof term / macro-like AST definition.
After expansion, fixed call semantics binds and executes the body normally.
The source spelling and constructor tree agree in branch order, operands,
letters, and return structure.

### `oddAlphabetCount(CS)`: `DEFINITION`

The second rule gives the sole, unconditional, nonrecursive equation for the
summary function `oddAlphabetCount`. It expands to the sum of
`cntSub(CS,[98])`, `cntSub(CS,[100])`, through `cntSub(CS,[122])`, precisely
the codes for `b,d,...,z`.

This is a transparent summary definition, not a domain lemma. The source
program independently executes the thirteen string `count` method calls. The
fixed operational semantics routes `str.count` to `cntSub` in
`semantics/methods.k:33-40`, and routes integer `+` to `+Int` in
`semantics/int.k:9`. The equation therefore names the expression that ordinary
execution reaches; it does not equate independently defined concepts, assert
the desired theorem as a fact, or replace program execution.

Neither inventory rule carries `simplification`, and there are no local
operational rules, proved-derived lemmas, or domain lemmas. Stage 1 builds the
module containing both equations before its positive proof and contains no
earlier proof of either exact rule against a module from which that rule is
absent. Thus neither could qualify as `PROVED_DERIVED_LEMMA`, though both
already satisfy the direct definitional criterion.

The independently reconstructed classification is therefore exactly:

```text
rule-f119e21...  DEFINITION
rule-fe0451...  DEFINITION
```

The genuine domain-lemma set is empty. Detailed reasoning and the frozen
semantic slice are in `evidence/04_independent_classification.md` and
`evidence/04_stage3_semantic_slice.log`.

## Deterministic Stage 4 generation

I invoked `tools.klean_preflight.check_generation` with:

```text
frozen_input       = /reference/k-proof
discovery_manifest = /reference/lemma-discovery.json
generation         = /reference/klean-generation
toolchain_lock     = /reference/klean-toolchain.lock.json
PYTHONPATH          = /reference
```

The first run reached Lake and exposed a container-only procfs/PID namespace
issue: Lean attempted `readlink("/proc/<numeric-pid>/exe")`, which returned
`ENOENT`, while `/proc/self/exe` was available. The failed run is preserved in
`evidence/03_preflight_rerun.log`. A small interposition in
`evidence/proc_exe_shim.c` redirects only numeric `/proc/<pid>/exe` readlinks
to `/proc/self/exe`; it does not change any audit input, Lean source, command,
or proof behavior.

With that environment repair, the same trusted `check_generation` invocation
exited 0 and returned:

```text
status: KLEAN_NO_OBLIGATIONS
obligation_count: 0
target: null
designated_sorry_count: 0
trust_declaration_count: 44
```

Its fresh-copy `lake clean` exited 0 with empty output. `lake build` exited 0,
built all generated modules, and had output SHA-256
`ba8f919aacd73e1a3f3e5c28c1b62e6b26fb582fc0370512088565d588eadd27`,
exactly matching the recorded preflight diagnostic. The complete returned JSON
is `evidence/03b_preflight_rerun_corrected.log`.

I separately checked the mathematical source-rule/obligation bijection:

- independently expected domain IDs: `[]`;
- `input-manifest.json` domain `source_rules`: `[]`;
- `obligation-map.json` `source_rules`: `[]`;
- generated obligation IDs: `[]`;
- generated trust parameters: `[]`;
- both generator and export obligation counts: `0`.

The input manifest's definition IDs are exactly the two canonical rules in
inventory order. Hence no relevant domain lemma was omitted, duplicated,
weakened, replaced by a vacuous conjunct, or turned into an irrelevant
obligation. There are simply no mathematical domain obligations to lower.

Target identity is also exact for the no-obligation case. The generator
manifest, recorded preflight, export result, and `/audit-input.json` all record
`target: null`; trusted `klean_export.target_statement` independently returns
`None`; and the generated Lean tree contains no theorem or lemma declaration.
The fixed generated tree hash matches every manifest and launcher binding.
Full independent results are in `evidence/05_stage4_integrity.log`.

## Stage 5 disposition

Stage 5 is correctly absent. `/candidate` does not exist, the launcher records
null Lean workspace and invocation paths/hashes, and Stage 4 produced no target
to prove. Running a candidate clean build, scanning candidate definitions, or
asking Lean for `#print axioms Proof.final` would invent a proof stage forbidden
by `KLEAN_NO_OBLIGATIONS`. The generated project itself was nevertheless
clean-built by the mandatory Stage 4 preflight.

## Supplied-semantics qualification

The source runtime treats vertical tab `"\v"` as whitespace:
`"\v".isspace()` is true and `"\v".split()` is `[]`. The supplied K rule
`isWSC(C)` recognizes only 32, 9, 10, and 13. Under that fixed model, code 11
follows the non-whitespace split branch. This mismatch is directly evidenced
in `evidence/06_model_boundary.log`.

That boundary does not change either Stage 3 classification: `splitWordsBody`
still exactly defines the constructor body, and `oddAlphabetCount` still
exactly defines the count summary under the fixed operational rules. Nor does
it create a domain lemma that Lean should prove: Stage 4 translates
proof-local mathematical lemmas, not an adequacy theorem comparing the supplied
language model with CPython. It therefore warrants a qualified but legitimate
result, not `NOT_LEGIT`.

## Evidence index

- `evidence/COMMANDS.md`: exact commands and preserved-attempt explanation;
- `evidence/01b_hash_recomputation_corrected.log`: all input, producer,
  sidecar, and launcher hash checks;
- `evidence/02_inventory_reconstruction.log`: canonical inventory and ordered
  bijection;
- `evidence/03b_preflight_rerun_corrected.log`: exact trusted preflight return;
- `evidence/04_independent_classification.md`: rule-by-rule semantic judgment;
- `evidence/04_stage3_semantic_slice.log`: frozen source, spec, and active
  operational rules;
- `evidence/05_stage4_integrity.log`: independent empty-domain, obligation,
  target, and Stage 5-absence checks;
- `evidence/06_model_boundary.log`: independent supplied-model boundary
  witness.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
