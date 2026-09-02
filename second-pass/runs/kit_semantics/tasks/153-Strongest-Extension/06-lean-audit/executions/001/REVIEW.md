# Independent audit: 153-Strongest-Extension

## Scope and result

I audited condition `kit-semantics` in `SUPPLIED_SEMANTICS` mode. The launcher
binding and `AUDIT_MODE` both select `CLASSIFICATION_AND_PROOF`. I treated the
mounted Stage 1–5 material as evidence only and based the structural checks on
the trusted tools under `/reference/tools`.

The result is PASS. The Stage 3 inventory is complete and its classifications
are mathematically appropriate; Stage 4 contains exactly five nontrivial
domain obligations and the fixed generated target is unchanged; and the Stage
5 candidate clean-builds, proves exactly that target, uses no project-specific
axioms, and supplies operationally honest definitions for all six target
parameters.

## Inventory reconstruction and identity

I ran the trusted `tools.k_rule_inventory.inventory_verification` directly on
the frozen `/reference/k-proof`. It reconstructed the local module closure

1. `VERIFICATION-BASE`
2. `VERIFICATION`
3. `TARGET-VERIFICATION`

from `verification.k`, whose SHA-256 is
`8977dbcde71e8b6950a74d4be323014b48ef457ce3b430ea7863dd459663de01`.
The reconstruction contains 42 rules and 42 distinct `source_rule_id` values.
Its canonical whole-inventory hash is
`c04282fc757603f0913951a3cb0f2efdda4db8509cb2b8147081a93a2fafd6a5`.

The ordered identities in `lemma-discovery.json` are bijective with that
reconstruction. Every recorded identity is `rule-` followed by the
independently normalized source hash. Source module, start/end line, exact
source text, normalized hash, and classification also agree bijectively with
the Stage 4 input manifest. There are no omissions, extras, duplicates, or
reordered identities. The full reconstructed inventory is in
`evidence/03-reconstructed-rule-inventory.json`; the 396-check independent
hash/bijection run ends with `failed=0` in
`evidence/47-independent-hash-and-bijection-results.txt`.

The same check independently reproduced all 874 Stage 1 regular-file path/hash
pairs, the mounted Stage 1, Stage 2, Stage 4, Stage 5, and producer tree hashes,
the deterministic Stage 1 export hash, the generated tree hash, the discovery
hash, the canonical audit-input digest, and the toolchain lock. The recorded
Stage 5 invocation directory itself is not mounted by design, so its
launcher-only invocation hash cannot be re-read; the mounted candidate tree
and every candidate file were independently hashed.

## Independent rule classification

The independently determined counts are:

- 34 `DEFINITION`
- 5 `DOMAIN_LEMMA`
- 3 `PROVED_DERIVED_LEMMA`
- 0 `OPERATIONAL_RULE`

Every one of the 42 ordered entries is accounted for below. “Entry” refers to
the order in the reconstructed inventory.

| Entries | Source lines | Count | Classification | Independent reason |
|---|---:|---:|---|---|
| 1–3 | 9–55 | 3 | `DEFINITION` | Macros naming the exact inner, outer, and whole-function statement blocks. |
| 4–6 | 60–65 | 3 | `DEFINITION` | Exhaustive guarded cases defining character strength. |
| 7–10 | 68–77 | 4 | `DEFINITION` | Base/cons recurrences for extension strength and final character. |
| 11–15 | 80–91 | 5 | `DEFINITION` | Constructor cases and recurrences defining string-domain predicates and the named projection guard. |
| 16 | 96–101 | 1 | `DOMAIN_LEMMA` | Definedness characterization of the partial `Val`-to-`Str` projection. |
| 17 | 103–105 | 1 | `DEFINITION` | Guarded evaluator defining the named `projectStrTotal` proof term through the operational projection. |
| 18 | 107–109 | 1 | `DOMAIN_LEMMA` | Reverse projection-to-summary bridge; it is not a left-headed definition of the named function. |
| 19 | 111–112 | 1 | `DEFINITION` | Constructor-domain identity evaluator for `projectStrTotal`. |
| 20–22 | 114–124 | 3 | `DOMAIN_LEMMA` | Idempotence and two datatype/domain characterizations not established by ordinary evaluation. |
| 23–25 | 127–135 | 3 | `DEFINITION` | Constructor extraction plus guarded defining representations of the code/projection proof terms. |
| 26–31 | 140–176 | 6 | `DEFINITION` | Base, update, and no-update recurrences for the best extension and best score. Strict `>Int` preserves the first extension on ties, matching the source. |
| 32–37 | 180–201 | 6 | `DEFINITION` | Base/cons recurrences summarizing the final extension, strength, and character variables. |
| 38–39 | 206–219 | 2 | `DEFINITION` | Empty/nonempty cases defining the whole-function mathematical result. |
| 40–41 | 227–272 | 2 | `PROVED_DERIVED_LEMMA` | Exact yield and inner-loop transitions first proved against `VERIFICATION-BASE`, which contains neither rule. |
| 42 | 280–313 | 1 | `PROVED_DERIVED_LEMMA` | Exact outer-loop transition first proved against `VERIFICATION`, before `TARGET-VERIFICATION` adds it. |

The macros and mathematical recurrences are summaries or named proof terms,
so they meet the requested `DEFINITION` criterion. The five projection facts
are genuine domain reasoning: they neither define an ordinary evaluator nor
belong to the supplied MPY execution semantics. They are directly relevant
because the frozen source iterates over string-valued extensions, while the K
loop machinery yields `Val` values and the verification summaries consume
their string/code projections. No domain lemma was disguised as a definition,
operational rule, or derived lemma.

There are 12 rules carrying a `simplification` attribute. Seven are defining
evaluators/recurrences and five are the domain lemmas above; none has an
impermissible classification.

The three derived rules were checked more strongly than their prior logs. I
normalized each later rule body and its earlier claim after removing only the
`rule`/`claim` header and later priority attribute; body, cells, transition,
and `requires` clause are byte-equivalent after whitespace normalization.
That comparison is recorded in
`evidence/60-derived-claim-exact-body-comparison.txt`. I then made a fresh
Stage 1 source copy and independently ran:

- `kompile` for `VERIFICATION-BASE`, followed by `kprove` of
  `CONNECTION-SPEC`; result `#Top`.
- `kompile` for `VERIFICATION`, followed by `kprove` of
  `OUTER-CONNECTION-SPEC`; result `#Top`.

Thus the yield and inner rules are proved before `VERIFICATION` adds them, and
the outer rule is proved before `TARGET-VERIFICATION` adds it. Complete output
is in evidence files `42`–`45`.

## Stage 4 provenance, obligations, and fixed target

Before judging generation, I independently hashed the immutable producer
sources:

- `klean_export.py`:
  `7cb3ed0da718d6b07560a910b8a2b3d9295cfb330b02bf52f0a8e1129f188752`
- `klean.py`:
  `50ca6b06c1387c7fd0a31354f65a31546227cf63ed35acd5386bef8fa118e346`

Both match `generator-manifest.json` and the producer source manifest. The
producer tree hash is
`bf8ab7d57561461dce9bffa6786f6cf2f7158cc274f2c4c8b26f79a20154b35e`,
matching `/audit-input.json`. The source manifest, generator manifest, and the
basename bound by `/audit-input.json` all identify the immutable generator
image as
`sha256:1b835aff66132f7ce282a7c2489b068f07401e58dc0af481344242c0e33d7ef6`.
There is no producer-provenance `AUDIT_ERROR`.

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`
using the required frozen workspace, discovery file, generation, and
toolchain lock. The audit sandbox hides `/proc/<pid>/exe`, which Lean 4.22 uses
to locate itself. I diagnosed this without changing any mounted input, then
used a narrow `readlink` shim that redirects only the current process’s
`/proc/<pid>/exe` request to the equivalent visible `/proc/self/exe`. The shim
validation and complete diagnosis are in evidence files `14`–`36`.

With that environment compatibility in place, preflight returned `PASS`:

- frozen/export hash:
  `dfb4720bce8129a4865899fa412b066dcab986484e5ab603701cb906404747a0`
- discovery hash:
  `2d9e4faf42d6b2f276b5173374acc5263c897ad35400b6977d8bcb3a9e8c0788`
- generated tree:
  `3cacfbed2ba8b1e9ca1ddd86682c3e611dcf4c0ab5ebccaaf67806f5090b048d`
- obligations: 5
- generated trust declarations: 42
- designated sorries: 0

The returned evidence is saved verbatim in
`evidence/37-check-generation-returned-evidence-success.json`.

The independently reclassified domain set is nonempty and contains exactly
these five ordered rules:

1. `rule-5d8f9b167e5284a82cd2a8ee7541fd69dfe8a2bfa3b401b3e610658fe9b05de3`
   — partial projection definedness.
2. `rule-db9d27e9548a05d29d1ed50dae5699e3007e66b4be241553668c21d60b3a10ae`
   — guarded partial/total projection agreement.
3. `rule-f85e27b93f985712e161e1d9f93c9edc4bb9b998f80b67e076ae37e57255f5e0`
   — total-projection idempotence.
4. `rule-334fd615c749b4780fa187ec0618b959d5589b042350fb2e8ff133c457d4d2f1`
   — equality with the projected string exactly characterizes string values.
5. `rule-10e1728036a93b9cdbc0c9743281a9e89436ffbf8433c0b87d6741769b463133`
   — equality with the string reconstructed from `codesProject` exactly
   characterizes string values.

The obligation map has those five identities in exactly that order, once
each. Every source span, normalized hash, discovery hash, inventory hash, and
Lean-conjunct hash agrees. Each generated conjunct is the direct typed
translation of its source rule and is needed to connect the `Val`, `Str`,
code-sequence, and partial-projection representations used by the frozen
program proof.

The first conjunct visibly contains `∧ True`. I specifically checked this for
vacuity: it is the exact Lean image of the source rule’s `#And #Ceil(@V)`.
Because the generated binder already has total Lean type `SortVal`,
`#Ceil(@V)` translates to `True`. The remaining equivalence still constrains
partial-projection definedness in both directions. This is neither an inserted
padding obligation nor a weakening of the source fact.

The generated target is
`Klean153StrongestExtension.Lemmas.targetStatement` with:

- definition hash:
  `a91235cd53302ca782e09edc323b5e2a1464be775552e2387173223e3b34c420`
- statement hash:
  `80e9122f393a0e7517a88d577b27623a14f7190c9516dff2b53656004f9d78e8`

Its declaration, file, statement, six ordered parameters, KORE-symbol
bindings, source-rule bindings, binding hashes, and both target hashes match
the generator manifest, fresh preflight result, copied `Base`, and
`/audit-input.json`. There is no omitted, duplicated, irrelevant, or changed
obligation and no target substitution.

## Stage 5 clean build, proof identity, and trust

I created `/tmp/audit-work/stage5-rebuild-153`, copied the immutable generated
project into it as `Base`, copied the candidate project files, and verified
both copies before building. I ran both required commands:

- `lake clean`: exit 0
- `lake build`: exit 0, “Build completed successfully.”

Complete output is in `evidence/49-stage5-lake-clean.txt` and
`evidence/50-stage5-lake-build.txt`. The trusted Stage 5 checker and trusted
final mechanical gate independently returned `PASS` as recorded in evidence
files `52` and `58`.

The candidate has exactly six parameter `def`s and theorem `Proof.final`. It
does not declare or shadow `targetStatement`; it imports and applies the fixed
qualified declaration. A case-insensitive scan of candidate Lean sources
found no `sorry`, `admit`, `unsafe`, `axiom`, or `opaque`. The copied `Base`
remained byte-identical to the selected generated project after the build.

Lean’s printed type of `Proof.final` is exactly:

`Klean153StrongestExtension.Lemmas.targetStatement`
applied to the candidate’s six ordered bound definitions. It is not a
duplicated, weakened, or separately stated theorem. The complete elaborated
print and axiom command are in
`evidence/53-print-proof-type-and-axioms.txt`.

`#print axioms Proof.final` reports exactly `[propext]`. It reports no
`sorryAx` and none of the 42 project-specific declarations recorded in
`trust-inventory.json`. `propext` is a Lean core logical axiom explicitly
allowed by the trusted final gate alongside the other fixed Lean core axioms;
it is not a candidate declaration or an unrecorded project trust escape.
Therefore the intersection of the proof’s dependencies with the generated
trust inventory is empty, all project-specific dependencies are accounted
for, and no new proof trust was introduced.

## Operational bridge audit

I compared each target parameter’s exact candidate `def` with its bound KORE
symbol, bound source-rule IDs, frozen rules, the supplied operational
semantics, and the source program:

| Parameter | Independent operational judgment |
|---|---|
| `codesProject` | Extracts the exact `IntSeq` payload from every `Str`-injected `Val`, matching `codesProject(str(CS)) => CS`. The empty result is used only off the K rule’s string domain. |
| `definedProjectStr` | Returns true exactly for `SortVal.inj_SortStr`, matching its defining equality to `isStringVal`. |
| `isStringVal` | Returns true exactly for the string constructor and false for every other `Val` constructor, matching the positive and `owise` K rules. |
| `project:Str` | On a singleton K sequence containing a string item, returns that exact string. Other K shapes receive only the total Lean codomain fallback; the frozen K projection is partial there and the target uses it only under the domain guard. |
| `projectStrTotal` | Is identity on every string payload, including nonempty payloads. Its empty fallback is confined to non-string values, where the no-evaluator K proof term leaves the result unconstrained. It is therefore a legitimate total model, not a constant implementation. |
| `project:Str?` | Returns `some` of the exact string only for the singleton string K shape and `none` for non-string, empty, or multi-item K shapes, faithfully representing the partial projection’s definedness. |

The source and postcondition operate on finite lists of strings. Consequently,
the off-domain totalizations cannot replace or evade the operational behavior
used by the frozen program; all on-domain payloads, including arbitrary
nonempty strings, are preserved.

I added an audit-only Lean file with concrete positive and adversarial
witnesses for all six definitions: a nonempty one-code string, an integer
value, empty K, singleton string K, and a multi-item K sequence. I also proved
that the fixed target rejects a constant/hard-coded mutation of each of the
six parameters individually. The audit file is
`evidence/56-operational-bridge-adversarial-and-mutation-checks.lean`; Lean
accepted it with exit 0 as recorded in evidence file `55`.

## Evidence index

`evidence/61-command-index.md` lists the material commands. The principal raw
results are:

- `03`, `04`, `47`: reconstructed inventory and complete identity/hash checks.
- `42`–`45`, `60`: fresh K proof replay and exact claim/rule comparison.
- `09`–`12`, `37`, `38`: producer provenance, manifests, preflight, and
  generated obligations.
- `48`–`50`, `52`–`54`: fresh project, clean build, mechanical check, fixed
  target, forbidden-token, and shadow checks.
- `53`, `57`, `58`: exact proof type, axiom output, and trusted final gate.
- `55`, `56`: operational adversarial examples and counterfactual mutations.

VERDICT: PASS
LEGITIMACY: LEGIT
