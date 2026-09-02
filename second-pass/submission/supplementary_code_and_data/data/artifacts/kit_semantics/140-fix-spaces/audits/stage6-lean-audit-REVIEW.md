# Independent audit: HumanEval 140-fix-spaces

## Scope and result

I independently audited Stage 3 classification and deterministic Stage 4
generation for condition `kit-semantics` with `SUPPLIED_SEMANTICS`. Both the
launcher environment and `/audit-input.json` record `CLASSIFICATION_ONLY`.
Consequently Stage 5 is outside this audit instance: the launcher records null
Lean workspace and invocation hashes, `/candidate` is absent, and Stage 4 has no
generated theorem.

I treated all mounted candidate/provenance prose and prior verdicts as untrusted
evidence. The affirmative findings below come from frozen-source inspection,
trusted inventory/preflight code, independent recomputation, and exact
regeneration. The complete command ledger is in `evidence/COMMANDS.md`.

## Producer and provenance integrity

I hashed the protected producer sources before judging Stage 4:

| Producer | SHA-256 |
|---|---|
| `klean_export.py` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` |
| `klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` |

Both values match the generation source manifest and
`generator-manifest.json`. The immutable generator image is
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`;
it matches both manifests and the image-keyed producer-source path recorded in
`/audit-input.json`. The protected source bundle contains exactly the three
manifested files and has pipeline tree hash
`388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`.

All 25 independent provenance checks passed, including the complete Stage 1
per-file hash map and these launcher-bound tree hashes:

| Artifact | Recomputed SHA-256 |
|---|---|
| Stage 1 pipeline workspace | `fdc05e9172174bb7981c928757711a135c95132c133e48d01871aaedced7fd86` |
| selected Stage 2 audit | `04383cfe9065bb37bbf09bc2892c3b19558988e8d60afaa69cafbb605eeeddea` |
| Stage 1 exported proof input | `365a6b6b83847d59991e7ae4855c6fe6ec65f27a73cd4fa0a8a8425700c79cd7` |
| Stage 3 discovery manifest | `5740afa88f5fa6b62339192a6daccbf7094d702fa35f8ca6161b259e377762c8` |
| selected Stage 4 directory | `a786eb01aa6cd92c9cd8b1cbf08eae41a17c1c10db24bd3a7df30ed38642e38d` |
| generated project tree | `d96615dce84ebae88402c8f31e3306b87287eab716490765d2fc96778ea1b176` |

Raw result: `evidence/01-hash-integrity.log`.

## Rule-inventory reconstruction

Using the trusted `k_rule_inventory.py` implementation on frozen
`verification.k`, I reconstructed the local verification-module closure as the
single local module `VERIFICATION`. The imported MPY semantics are external to
that local-file closure. The frozen file hash is
`7eb12264691e0c22fce723b204c196680cbfb4910a586452c879975f5b3f9ed4`
and the canonical whole-inventory hash is
`5441f1019df2fff08e7d49cef4c2328a260cfe74823aaf96249b80c5cc44d8e7`.

The inventory has exactly 14 rules. The table gives every exact source span and
whitespace-normalized source hash; each exact `source_rule_id` is
`rule-<normalized SHA-256>`.

| # | Lines | Head/case | Normalized SHA-256 | Independent class |
|---:|---:|---|---|---|
| 1 | 8–22 | `#fixSpacesLoopBody` | `7dc592a20c66d31fde205bd8af3de4982b746dfed8dce3a211f2213a9b1648c8` | `DEFINITION` |
| 2 | 25–30 | `#fixSpacesBody` | `60a2e41e7abd89a4705ed1bfe8f7231134a75a383f497a10a89f02ddcddcc407` | `DEFINITION` |
| 3 | 34–36 | `pendingSpace`, `__` | `14a4162ef746a7b1514f1437363b58b37917f4d4e3d88fefed3c57ad2805fc1c` | `DEFINITION` |
| 4 | 37–40 | `pendingSpace`, `-` | `3a1617f33a2052cf0e47d921ef5d9d446c818e4e28613c67cb7e98fd12477ce5` | `DEFINITION` |
| 5 | 41–44 | `pendingSpace`, other | `4a9240ff48e39b4f7ca7cdf130ac4cc929faa5a1db52064fce7d072847973398` | `DEFINITION` |
| 6 | 48 | `resultAfter`, empty | `cb3f7e78e89867dea79ff1da3d0ba357a2f19ba166a3105d0bfb180249bcef15` | `DEFINITION` |
| 7 | 49–50 | `resultAfter`, space | `ab4d5becfd8d470f186d1f245d2ab65f5bf113c326562df2b5ed37d0ab7ad93f` | `DEFINITION` |
| 8 | 51–57 | `resultAfter`, non-space; `simplification` | `2474ff592cce4297eb234f57f5266cadd5c79784f4555511da449c9dc39aecd8` | `DEFINITION` |
| 9 | 60 | `pendingAfter`, empty | `914d02541b0edb3ef3039272a8847fb5d5859793d3bc8e6b5d81637111b9ec0f` | `DEFINITION` |
| 10 | 61–62 | `pendingAfter`, space | `abb763d32b8c0b7f1f499857f237890d9e7325671320addc7babf2323b088c8b` | `DEFINITION` |
| 11 | 63–66 | `pendingAfter`, non-space; `simplification` | `38a7a54771406f0fcf4f53d56873c51b354f06859365120b1441f6bd9ad3b4a8` | `DEFINITION` |
| 12 | 69 | `charAfter`, empty | `a1cc403dbcce337ddeafd5bfaaf336abab04bc666cabf437ea542f2b3720af14` | `DEFINITION` |
| 13 | 70–71 | `charAfter`, step | `9c34344a0ea1cb0299269885158d8750178870205348fe7c9d6179fad345aa02` | `DEFINITION` |
| 14 | 74–77 | `fixedSpaces` | `ab0ca6a8cd8575cfb385c12e545c1f7abe205f28060972c8e6873b21bee131d5` | `DEFINITION` |

The reconstructed ordered identities match the protected discovery manifest
bijection exactly. There are no missing, extra, duplicated, reordered, or
changed rules. Every inventory entry has exactly one classification, the
manifested source spans and normalized texts match, and Stage 4's definition
documents account for the same 14 identities once each. All 53 mechanical
inventory comparisons passed. Raw reconstruction and comparisons are in
`evidence/02-rule-inventory.log`.

## Independent classification and mathematical judgment

The protected classification is substantively correct, not merely
self-consistent:

- `#fixSpacesLoopBody` and `#fixSpacesBody` are named proof-term/AST macros.
  They reproduce the translated loop and function body from frozen
  `solution.py`.
- The three `pendingSpace` equations define the complete and disjoint state
  transition for a current run of spaces: `__` becomes `-`, `-` remains
  absorbing, and every other state appends `_`.
- `resultAfter`, `pendingAfter`, and `charAfter` are structural recurrences on
  the remaining input sequence. Their recursive calls consume one sequence
  constructor. The two rules tagged `simplification` are defining non-space
  recurrence cases and therefore satisfy the required simplification policy.
- `fixedSpaces` is the named summary combining the final emitted result and
  pending suffix.

None is an `OPERATIONAL_RULE`: no rule rewrites a configuration or `<k>` cell,
and each rule is headed by a newly introduced pure summary/macro symbol. None is
a `DOMAIN_LEMMA`: no entry asserts an independent property of pre-existing
operations; each supplies an equation of the symbol it defines. None is a
`PROVED_DERIVED_LEMMA`: Stage 1 separately proves a loop-invariant claim and
then the full specification, but it does not first prove any exact inventory
rule in a module excluding that rule and later install it.

I checked these definitions against the supplied operational semantics rather
than relying on their names. The relevant semantics make expressions/statements
strict, lower `For` through `#loop`/`#iterNext`, iterate a string one character
at a time, bind the loop target, implement string concatenation and equality,
apply assignment/augmented assignment in sequence, and return the final value.
Under those rules the source program maps a run of one or two spaces to one or
two underscores and a run of at least three spaces to one dash, including
leading and trailing runs. The summary equations implement exactly that state
machine and flush pending output before each non-space and at return.

As additional falsification evidence, an independent source state machine, a
literal implementation of the K recurrences, and an independent run-contract
oracle agreed on all 87,381 strings of length 0 through 8 over
`[space, A, _, -]`, plus adversarial integer-code examples. Counterfactuals for
premature dash conversion, a non-absorbing dash, omitted pending flush, and
discarded trailing pending output were each separated by concrete witnesses.
This finite testing supplements, but does not replace, the direct operational
analysis. Raw classifications and cases are in
`evidence/03-semantic-reclassification.log`; frozen source excerpts are in
`evidence/11-frozen-source-operational-semantics.log`.

The independently determined true domain-lemma set is therefore genuinely
empty.

## Stage 4 preflight, bijection, and target identity

I invoked `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`
and exactly the requested Stage 1, discovery, Stage 4, and toolchain-lock paths.
The final call returned:

- status `KLEAN_NO_OBLIGATIONS`;
- zero obligations;
- null target;
- exact frozen, discovery, and generated-tree hashes shown above;
- `lake clean` exit 0 and `lake build` exit 0, with all nine generated modules
  built;
- zero designated `sorry` occurrences.

The initial call exposed an audit-container PID-namespace issue: Lean tried to
read `/proc/<namespace-pid>/exe`, which this procfs mount did not expose. I
diagnosed this explicitly and reran through a preserved, reviewable shim that
only aliases such reads to `/proc/self/exe`. It reported Lean 4.22.0 at commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05` and K/pyk 7.1.293, exactly matching
the trusted lock. This changes executable-path discovery, not generated source,
Lean logic, or proof content. The failed diagnostic run is retained in
`evidence/04-klean-preflight-check-generation.log`, the diagnosis and shim
source in `evidence/09-toolchain-namespace-diagnosis.log` and
`evidence/lean_proc_self_shim.c`, and the complete successful API result in
`evidence/10-klean-preflight-final.log`.

I then ran the exact protected exporter sources independently in scratch. It
again produced `KLEAN_NO_OBLIGATIONS`, zero obligations, a null target, and the
same generated-tree hash. The generated tree and
`generator-manifest.json`, `trust-inventory.json`, and `export-result.json`
were byte-identical to the selected Stage 4 artifacts. The regenerated input
manifest became identical after normalizing only the recorded absolute input
mount prefix (`/reference/k-proof` versus the generation-time `/frozen-k`).

The independently expected source-rule/obligation bijection is empty-to-empty:

- independent `DOMAIN_LEMMA` identities: `[]`;
- Stage 4 input source rules: `[]`;
- `obligation-map.json` source rules: `[]`;
- generated obligations: `[]`;
- trust parameters: `[]`.

The obligation-map hash is
`cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`.
There are no omissions, duplicates, irrelevant or weakened obligations, hidden
`targetStatement`, vacuous conjuncts, or target changes. The exact producer,
selected manifest, and launcher all bind the target to null. The trust inventory
hash is `1cd9660e29540618d9c6b9ad1e116a948f2879fb2315e20af8515902729ab082`;
preflight accounts for its 42 generated data/function trust declarations and
finds no proof holes. With no proposition target or proof candidate, none can be
used to evade a generated obligation.

Exact regeneration is in `evidence/06-exact-stage4-regeneration.log`; all 33
manual manifest, lock, bijection, target, and absence checks are in
`evidence/08-stage4-manual-audit-rerun.log`.

## Stage 5 disposition

Stage 5 proof checks are correctly inapplicable. Audit mode is
`CLASSIFICATION_ONLY`, the true domain set and obligation set are empty, the
generated target is null, `/candidate` does not exist, and the launcher records
no Stage 5 workspace or invocation. Therefore there is no `Proof.final`, target
parameter, operational bridge, candidate axiom list, or candidate shadowing to
audit. The absence of a Stage 5 candidate is required for this
`KLEAN_NO_OBLIGATIONS` result and was independently confirmed.

## Conclusion

The protected Stage 3 manifest is complete and correctly classifies all 14
rules as definitions. The domain-lemma set is genuinely empty. Protected Stage
4 producer provenance is intact, exact regeneration is deterministic, the
empty obligation bijection is mathematically appropriate, and all representations
agree that no generated target exists. I found no soundness, relevance,
omission, weakening, trust-boundary, or operational-bridge defect.

VERDICT: PASS
LEGITIMACY: LEGIT
