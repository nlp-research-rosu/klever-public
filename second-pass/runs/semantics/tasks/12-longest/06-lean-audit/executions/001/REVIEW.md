# Independent audit: HumanEval `12-longest`

## Result

The protected Stage 3 classification is complete and correct. The canonical
local rule inventory has nine rules: seven definitions, two operational
iterator observations, no proved derived lemmas, and no domain lemmas. The true
domain-lemma set is therefore genuinely empty.

The selected deterministic Stage 4 generation is authentic and structurally
consistent with that classification. Its status `KLEAN_NO_OBLIGATIONS` is
appropriate: the source-rule list, obligation list, and trust-parameter list
are all empty; the expected and actual generated targets are both absent; and
there is no Stage 5 candidate.

I treated every prior review, manifest conclusion, comment, and log as
untrusted evidence. The judgments below come from fresh reconstruction,
source inspection, hash verification, and a fresh mechanical preflight.

## Audit mode and immutable input bindings

`AUDIT_MODE` and the signed resolution both say `CLASSIFICATION_ONLY`.
`semantics_mode` is `SUPPLIED_SEMANTICS`. The signed resolution recomputes to
`fd46b31ee0b124e16282d124992ca3f8a0478f728b478064e6129972a1be7efa`,
exactly its recorded `resolved_input_sha256`.

All mounted provenance bindings recomputed successfully with the hash
algorithm associated with each field:

| Binding | Recomputed and recorded SHA-256 |
|---|---|
| Stage 1 workspace, pipeline tree | `5be7e78b32608569d40ad557bf52867062fe6e659a9b842080faefa609a899af` |
| Stage 1 frozen export, Klean tree | `33ce33b03ff462bb2e9e982e81b7e643eab1e344ae71a6bb1c5e6c0daa6160ea` |
| Stage 3 discovery manifest | `40b14ce6dbe70991f0f459ab4a8b218dfa55fcbc1f61a9153cd8d612c7d102bc` |
| Selected Stage 2 audit tree | `7ede77c9f634ceb7b8660fa1d4bc856796f00000ba80b84d29e9c760554a6159` |
| Selected Stage 4 generation tree | `5a4086199d074f0a77581b133a0d0fe76abf692667885b1b61e4dc2ee8a234ee` |
| Generated Lean project, Klean tree | `76c238360ea43619f240b0ac673b376487c83512a85ad7e8674b2d00ee732b55` |
| Generation-time producer-source tree | `55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c` |

The complete set of 36 Stage 1 regular files and their individual SHA-256
values matches `stage1_source_hashes` exactly, with no missing or extra file.
The selected-artifact hashes, all Stage 4 sidecar bindings, the generated-tree
hash, the trust-inventory hash, and the obligation-map hash also match.

The mechanical-checker lock file hashes to
`5f2476d09635fc2f32625592bd667dd87a374068cd5b6610d9513ee6dacc066f`,
as recorded in `/audit-input.json`. Every locked `/reference/tools` source
matches its per-file digest. The mounted toolchain lock is byte-identical in
hash to the image copy:
`a3dc0270ff7cab64550e91f605d8f2b5f6076b75f4ec49629a0e13894455fa9f`.

Raw results are in `evidence/recorded-hashes-and-mode.txt` and
`evidence/mechanical-checker-lock.txt`.

## Producer-source authentication

I performed this check before judging Stage 4.

| Producer | Recomputed SHA-256 |
|---|---|
| `klean_export.py` | `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0` |
| `klean.py` | `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1` |

Both values match the source manifest and `generator-manifest.json`. The
generator image ID is consistently
`sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000`
in the source manifest, generator manifest, and the image-key component of the
producer path signed into `/audit-input.json`. The producer bundle contains
exactly the two producers and its source manifest. There is no producer-source
infrastructure error.

Raw results are in `evidence/producer-authentication.txt`.

## Inventory reconstruction and bijection

Using the locked `tools.k_rule_inventory.inventory_verification`, I
reconstructed the local closure selected by `prove.sh`. The main module is
`VERIFICATION`; it is the only module defined in `verification.k` that is in
the local verification closure. The supplied `MPY` semantics is an external
required module, not an additional local module in this inventory.

The frozen `verification.k` SHA-256 is
`38c1e1de8abb57547abb3d9c5960edd042baf46a4bbbe5f1ccdfb1f108220e4e`.
For every rule I independently checked that:

- the recorded line slice equals the extracted frozen source text;
- the normalized hash equals SHA-256 of whitespace-normalized rule text;
- `source_rule_id` is exactly `rule-<normalized_sha256>`; and
- all identities are unique.

The reconstructed inventory hash is
`a98db69cb20a67dd7735e7d1757ee526843d1de0c0b6cebc046c726949021df4`.
It equals the protected Stage 3 inventory hash. The protected manifest has
exactly nine unique entries, and its identity sequence equals the canonical
inventory sequence—not merely the same set. Thus there are no omissions,
duplicates, extras, reordered identities, changed hashes, or unaccounted
classifications.

| Span | Normalized SHA-256 / source identity suffix | Independent class |
|---|---|---|
| 12-12 | `61a7e85b99e1fd517b3f029cca636566b11a786aa2f24d053db8e5dea4317820` | `DEFINITION` |
| 13-14 | `06cf824ccd2247d57e4141172b5e6494e4acc57dc1a88a94144097b09d59b0c1` | `DEFINITION` |
| 18-19 | `285b45564f2d7dce460b69dbde1ea9178bdc2bd530970d2320373eaba6467c80` | `OPERATIONAL_RULE` |
| 20-22 | `55d56cc27c981347c574d1ce91485262c24edb072a6b353a25dac39dfaa97e32` | `OPERATIONAL_RULE` |
| 27-27 | `f40c65506711d9264ce5e002c00c58e14bffb284ba0a0ef1e062022c850058fa` | `DEFINITION` |
| 28-29 | `4344ff90b2feb479d11bd8ad23e5a852fa65b2184ee2ab2a22a60b8b24b7a9ba` | `DEFINITION` |
| 30-32 | `0f388914c90471f2074c0ae8359e3fa11b9f73200e404e8cded4c53936bcd932` | `DEFINITION` |
| 33-35 | `370c2d5a71b42f964c5e0bc4fde658a3d2f206ee26b68793283aebc5d57f27f9` | `DEFINITION` |
| 40-57 | `1b6d53d96f4b4a82eb6b7f9bafc5577f204500d0110e04dbb065f0e26a91bc18` | `DEFINITION` |

The complete reconstruction, including source text and recomputed fields, is
in `evidence/inventory-reconstruction.txt`.

## Independent classification judgment

The two `stringVals` rules at lines 12-14 define the empty and constructor
cases of a structural embedding from `StringSeq` into the supplied semantics'
`ValSeq`. They are definition equations.

The two rules at lines 18-22 are ordinary operational observations of that
embedded sequence. Under the `stringVals` equations, they are exactly the two
supplied `MPY-LIST` iterator cases:

- `#iterNext(list(.ValSeq)) => #iterDone`; and
- `#iterNext(list(vCons(V, R))) => #iterYield(V, list(R))`.

They preserve the framed continuation and introduce no state effect. They are
therefore `OPERATIONAL_RULE`, not domain lemmas or unproved mathematical facts.

The four `longestAcc` rules at lines 27-35 define a named, terminating left-fold
recurrence:

- empty input returns the accumulator;
- the first string replaces `noneV`;
- a strictly longer head replaces the current string; and
- a shorter or tied head retains the earlier string.

The last two guards, `>` and `<=` on integer string lengths, are disjoint and
exhaustive. This recurrence exactly reflects the frozen source's branches and
its first-on-tie postcondition. Being program-specific does not turn these
equations into domain lemmas: they introduce and define the summary function
itself, which is precisely the permitted `DEFINITION` category.

The rule at lines 40-57 expands the `[macro]` name `longestSolution` to the
translated closure. It is a named proof-term definition.

No rule was first proved against a module omitting that exact rule and only
then used later. `prove.sh` compiles `verification.k` containing all nine rules
before proving claims from `spec.k`. Accordingly, none qualifies as
`PROVED_DERIVED_LEMMA`.

No inventory entry has a `simplification` attribute, so the simplification
classification restriction is satisfied vacuously. The final independent
totals are:

- 7 `DEFINITION`;
- 2 `OPERATIONAL_RULE`;
- 0 `PROVED_DERIVED_LEMMA`; and
- 0 `DOMAIN_LEMMA`.

The protected Stage 3 class and rationale for every ordered identity agree
with this result. Source and operational-semantics excerpts are in
`evidence/frozen-source-and-semantics.txt`; the rule-by-rule judgment is in
`evidence/classification-assessment.md`.

## Stage 4 manifest bijection and target identity

The Stage 4 input manifest's seven definitions, two operational rules, and
empty proved-derived list exactly equal the freshly validated inventory
records. Its domain-derived `source_rules` list is empty, matching the
independently empty domain set.

`generated/obligation-map.json` contains exactly:

- `source_rules: []`;
- `obligations: []`; and
- `trust_parameters: []`.

Its SHA-256 is
`cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`,
matching the generator manifest. The producer's expected target constructor
returns no definition for this empty map. Independent target parsing also
returns no target, and `generator-manifest.json`, `export-result.json`,
`preflight.json`, and `/audit-input.json` consistently record zero obligations
and a null target.

There are consequently no omitted, duplicated, weakened, irrelevant, or
vacuous conjuncts and no possible target substitution: the correct fixed
generated target is absent.

Raw comparisons are in `evidence/stage4-classification-binding.txt`,
`evidence/obligation-bijection-and-target.txt`, and
`evidence/generation-time-target-check.txt`.

## Fresh deterministic-generation preflight

I reran:

```text
PYTHONPATH=/reference python3
from tools.klean_preflight import check_generation
check_generation(
    /reference/k-proof,
    /reference/lemma-discovery.json,
    /reference/klean-generation,
    toolchain_lock=/reference/klean-toolchain.lock.json,
)
```

The audit sandbox exposes a host-PID `/proc` mount while `getpid()` returns a
nested namespace PID. Lean 4.22 resolves its executable through
`/proc/<getpid>/exe`, so the unadjusted ambient shim failed before compilation.
I preserved those failed attempts. For the successful rerun I used the small
auditable preload source in `evidence/proc_pid_compat.c`, which only makes
`getpid()` return `/proc/self`'s numeric host-PID target. It does not alter any
candidate, provenance input, Lean source, target, or checking logic.

The fresh returned evidence was:

```text
status: KLEAN_NO_OBLIGATIONS
obligation_count: 0
target: null
designated_sorry_count: 0
trust_declaration_count: 47
lake clean: exit 0
lake build: exit 0
✔ [2/9] Built Klean12Longest.Prelude
✔ [3/9] Built Klean12Longest.Sorts
✔ [4/9] Built Klean12Longest.Inj
✔ [5/9] Built Klean12Longest.Lemmas
✔ [6/9] Built Klean12Longest.Func
✔ [7/9] Built Klean12Longest.Rewrite
✔ [8/9] Built Klean12Longest
Build completed successfully.
```

The successful command and returned JSON are in
`evidence/fresh-check-generation.txt`. Environment diagnosis and the retained
failed attempts are also under `evidence/`; they do not indicate an input or
proof defect.

## Stage 5 applicability

Stage 5 is correctly absent. `/candidate` does not exist, the signed Lean
workspace and invocation hashes are null, `stage5_result` is null, and there is
no generated target to prove. A clean-build proof, `#print axioms Proof.final`,
candidate trust-escape scan, proof-identity check, and operational-bridge
parameter audit are therefore inapplicable in this `CLASSIFICATION_ONLY`
run—not omitted proof-mode checks.

## Evidence index

The principal raw artifacts are:

- `evidence/producer-authentication.txt`
- `evidence/mechanical-checker-lock.txt`
- `evidence/recorded-hashes-and-mode.txt`
- `evidence/inventory-reconstruction.txt`
- `evidence/frozen-source-and-semantics.txt`
- `evidence/generation-time-target-check.txt`
- `evidence/classification-assessment.md`
- `evidence/stage4-classification-binding.txt`
- `evidence/obligation-bijection-and-target.txt`
- `evidence/fresh-check-generation.txt`
- `evidence/proc_pid_compat.c`
- `evidence/proc-pid-compat-validation.txt`

VERDICT: PASS
LEGITIMACY: LEGIT
