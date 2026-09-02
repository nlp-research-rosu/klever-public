# Independent audit: 112-reverse-delete

## Scope and outcome

I independently audited Stage 3 lemma classification, deterministic Stage 4
generation, and the Stage 5 Lean proof for condition `semantics` and semantics
mode `SUPPLIED_SEMANTICS`. `/audit-input.json` and `AUDIT_MODE` both select
`CLASSIFICATION_AND_PROOF`.

The audit passes. The frozen local K inventory has eight genuine definitions
and one relevant domain lemma. Stage 4 generated exactly one non-vacuous
obligation for that domain lemma, and the Stage 5 candidate proves the exact
fixed target with operationally faithful definitions and no unrecorded trust
escape.

## Producer and input provenance

I hashed the mounted Stage 4 producer sources before judging the generation:

- `klean_export.py`:
  `6d620b92d4de6a051dea0ef5ed4670a77d76199648a7b64808b91286b3dd20c0`
- `klean.py`:
  `1ba065b19feb2fb0a48abe80bc2cf0d0afd3d72289374303745e0d5a59f0bccc`
- producer bundle:
  `83415436ab900e1a996037f6c97d291e693e705c9de30342d3e142bd264dfbfb`
- immutable generator image:
  `sha256:9552b3eb7f21ae17e7ade215d2115ed1f2232426ba7ebc2af7c8784215780274`

The two file hashes agree exactly across
`/reference/generation-tools/source-manifest.json`,
`generator-manifest.json`, and the producer bundle. The image ID agrees
between both manifests and the image-qualified path recorded in
`/audit-input.json`. The trusted pipeline tree hash of the producer bundle also
matches the audit input. Producer provenance is therefore complete and does
not raise `AUDIT_ERROR`.

I also independently reproduced every launcher-bound tree hash:

| Input | Recomputed hash |
|---|---|
| Stage 1 pipeline tree | `3c3537a0dada32706f815e6f55c87e5fe9f3347678a128926ce3ae1c9a4ac67e` |
| Stage 1 export tree | `27b360fd781cde88aa1bd89cd038a6d9aeddfc7e7c7e168d0a48000411e90221` |
| selected Stage 2 K audit | `d5189a874b5dbb86d235bb806ee1d911a862b5b02dfa4251ea91ae00be3cc181` |
| protected Stage 3 manifest | `b3f792d4c3237a283f84976fb1c8e44dcdc28111dc49371f1381821395f04e2f` |
| selected Stage 4 generation | `16643e37bb52d2256d279588aed89d29202f6dd68b8192502af2415c9ee6c1c3` |
| generated Lean tree | `395cb53b4446c62d01d54cad93fc2acf31a210d170d1068b8984ebdeb69c9e8f` |
| Stage 5 candidate | `86ecc8e6693eb7a2dcd01a7158764bc61bbed06680333bd2b6b192116b861fce` |

All individual Stage 1 file hashes recorded in the audit input also match.

## Inventory reconstruction

I ran the trusted `tools.k_rule_inventory.inventory_verification` on the
frozen Stage 1 workspace, starting at `verification.k`. Its local module
closure is exactly:

1. `MPY-VERIFICATION-BASE`
2. `MPY-VERIFICATION`

The independent reconstruction contains nine ordered rules and has inventory
hash:

`8d773464b6ba1618516dc7e1ba14d5b5733793366f9b690fdefefb5b18542ce3`

For every rule I recomputed the module, source span, normalized text,
normalized SHA-256, attributes, and `source_rule_id`. The ordered identities
are:

| Span | Recomputed `source_rule_id` | Classification |
|---|---|---|
| 9 | `rule-da05db292ede4977e2f8dca6f4c4ec4a6ba1012a3b2324065a54884686090e69` | `DEFINITION` |
| 10–13 | `rule-8dabe4e5ba506a18e8f420ef6977b74364a21649a135c5e932448f564eae2cf4` | `DEFINITION` |
| 14–17 | `rule-2a3470225284c385207d0a787669634f02e0009537282ba0e597f6b9733fd3e2` | `DEFINITION` |
| 21 | `rule-8701e016697ef59d7e253060fec27e6fefded740d188dbe40e6336ff80793506` | `DEFINITION` |
| 22–25 | `rule-91f03b074131c410d0eaddc0da0c9bc32c8b0de1ab0beadd9766a7b84d2236c1` | `DEFINITION` |
| 26–29 | `rule-7c28fce0e994b0447c8a502a721980d549046c72958a26c09c586358979601c1` | `DEFINITION` |
| 34 | `rule-f5d5f2b86fa99f091525498737953025cdc37dae5d16525d9518676dd1458039` | `DEFINITION` |
| 35–36 | `rule-d1657638146236c8516ea3509cc0589925a50f176c4eed9da939c79f30d87ffd` | `DEFINITION` |
| 44–79 | `rule-00095a0636462ee35f07d6cfe2315557d18e9db58d43983c60cf4c9478d9c6f6` | `DOMAIN_LEMMA` |

The reconstructed list and `/reference/lemma-discovery.json` agree
bijectively and in order. The Stage 4 input manifest's eight `definitions`
plus one `source_rules` entry are another exact bijection with the
reconstruction. There are no omissions, duplicates, extras, reordered
identities, changed hashes, or unaccounted classifications.

## Independent Stage 3 classification

The classifications are mathematically correct:

- Lines 9–17 are the base equation and two conditional recurrence equations
  defining `keptAcc`. They delete a character when its one-character string
  occurs in `c`; otherwise they append it to the forward accumulator.
- Lines 21–29 analogously define `reversedKeptAcc`, except that a retained
  character is prepended to the reverse accumulator.
- Lines 34–36 define `lastCharacter`: empty iteration preserves the previous
  target value, and nonempty iteration recursively leaves the last
  one-character string.

These eight rules define named total summaries. All four rules bearing the
`simplification` attribute are therefore valid `DEFINITION` entries; no
`simplification` rule is classified as operational or proved-derived.

The priority-40 rule at lines 44–79 summarizes an entire `#loop` execution. It
is not an ordinary execution/observation rule and is not a definition. It is
also not a valid `PROVED_DERIVED_LEMMA`: `prove.sh` compiles
`verification.k` with `MPY-VERIFICATION` as the main module before running
`LOOP-SPEC`, so the compiled definition already contains this exact rule.
The later `kprove` invocation does not first prove it against a definition
that excludes it. The protected `DOMAIN_LEMMA` classification is therefore
the only permissible one.

The domain lemma is relevant. The frozen solution iterates over `s`, deletes
each character found in `c`, appends retained characters to `result`,
prepends them to `reversed_result`, and leaves `character` at the last
iteration value. The supplied operational semantics lowers `For` to `#loop`,
iterates strings as one-character strings, implements `"not in"` through
`notBool strContains`, implements string `+` through `seqConcat`, and updates
the current scope. The lemma records exactly those three loop effects and
preserves all unrelated cells. It is neither an unrelated algebraic fact nor
a disguised operational rule.

## Stage 4 obligation and target

I reran the mandated
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and the
three mounted paths. Lean initially failed before compilation because this
audit sandbox virtualizes `getpid()` while its mounted `/proc` lacks that
virtual PID; Lean 4.22 calls `readlink("/proc/<pid>/exe")`. I retained that
failed attempt, then used the narrow audited `readlink` shim in
`evidence/proc-self-exe-fix.c`, which redirects only such paths to
`/proc/self/exe`. The shim changes no proof or generated input. The rerun used
the pinned Lean 4.22.0 toolchain and returned:

- status `PASS`;
- one obligation;
- zero designated sorries;
- 78 generated trust declarations;
- clean and build exit codes both zero;
- the exact recorded Stage 1, Stage 3, and generated-tree hashes.

The true independent domain set has one member, so `OK` with one obligation
is required; `KLEAN_NO_OBLIGATIONS` would have been incorrect.

The obligation map has one source rule and one obligation, both uniquely
bound to
`rule-00095a0636462ee35f07d6cfe2315557d18e9db58d43983c60cf4c9478d9c6f6`.
Their normalized hash, source span 44–79, inventory hash, discovery hash, and
text identity all match. The Lean conjunct hash is:

`39cb08636e4e87ec503b042d7dcbe0669f1c41e52749baec6fd828d93fda86be`

I independently rendered the target from the obligation and its five
bindings and compared that text to the sole generated `targetStatement`.
The result matches the generator manifest, launcher preflight, and audit
input exactly:

- declaration:
  `Klean112ReverseDelete.Lemmas.targetStatement`
- definition hash:
  `dba40f467ddda5dd0f19be88d96838faf895ca7deb7fe7c2d1399d50b13df970`
- applied-statement hash:
  `e9b7a4314eeb09e7d0111fba1ceb606be6c89198e01f8cb69020d4788353e625`

The five parameters are `_Map_`, `«_|->_»`, `keptAcc`,
`lastCharacter`, and `reversedKeptAcc`; every binding hash recomputes and
every binding points to the one domain rule. The target is the full
universally quantified rewrite from the exact loop configuration to the
exact summarized configuration. It preserves the continuation, original
string, deletion string, parent, environment, and all eight other cells. It
is not `True`, does not discard a postcondition, contains no unused conjunct,
and is neither weakened nor duplicated.

## Stage 5 clean build and proof identity

I made the fresh persistent project
`/tmp/audit-work/proof-audit-112`, copied the immutable generated project into
it as `Base`, and ran both required commands:

- `lake clean`: exit 0;
- `lake build`: exit 0, including `Proof`.

The warnings are only unused-variable and simplifier lints. Complete output is
saved in `evidence/fresh-proof-lake-clean.log` and
`evidence/fresh-proof-lake-build.log`.

The trusted independent proof gate also passed after making its own temporary
copy, replacing `Base`, cleaning, building, and checking the theorem. The
candidate:

- does not define or shadow `targetStatement`;
- defines every required target parameter exactly once;
- contains exactly one `theorem final`;
- states the exact fixed generated target after whitespace normalization;
- contains no `sorry`, `admit`, `unsafe`, new `axiom`, or new `opaque`.

`Proof.final` is a structural induction on the remaining string. The proof
uses the generated ordinary `Rewrites` constructors for string iteration,
target binding, comparison, branch selection, forward update, reverse
assignment, loop continuation, and termination. It does not assume the
selected domain rule or prove a separate weaker theorem.

## Operational-bridge audit

I compared each exact candidate definition with its `kore_symbol`, the bound
source rule, all relevant frozen definition rules, the Python solution, and
the supplied operational semantics:

1. `_Map_` calls the generated partial K map-concatenation model. Whenever
   that model returns `some result`, the bridge returns exactly `result`.
   Its fallback is used only when K map concatenation is undefined because
   keys conflict. Thus it is a total extension, not an identity or constant
   replacement of defined K behavior.
2. `«_|->_»` constructs the exact singleton map. Its one-layer
   `normalizeKItem` implements canonical K subsort injection: generated
   `inj_SortVal` values that are concretely strings, integers, and so on are
   represented by their canonical KItem injection. It preserves all already
   canonical keys and values and is not a hard-coded map.
3. `keptAcc` implements lines 9–17 exactly: base accumulator, deletion by
   character membership, and left-to-right append through a recursive
   concatenation matching `seqConcat`.
4. `lastCharacter` implements lines 34–36 exactly: preserve the prior value
   for empty input, otherwise return the last one-character string.
5. `reversedKeptAcc` implements lines 21–29 exactly: base accumulator,
   deletion by membership, and prepending of each retained character.

I compiled additional adversarial Lean examples. For source codes
`[97,98,97]`, deletion codes `[97]`, and initial accumulator `[120]`, the
candidate computes forward `[120,98]`, reverse `[98,120]`, and last character
`[97]`. Empty input preserves both accumulators and the previous character.
Distinct singleton-map inputs remain distinct, a wrapped `Val` string is
canonically injected, and disjoint map concatenation retains both entries in
order. These examples distinguish the definitions from identity,
constant/empty, forward-only reverse, and previous-character mutations. The
adversarial audit file exits zero.

## Axiom accounting

I ran Lean directly with exactly `#print axioms Proof.final`. It reports 32
dependencies. Three are Lean logical foundations:

`Classical.choice`, `propext`, and `Quot.sound`.

The remaining 29 are all exact entries in the generated
`trust-inventory.json` allowlist:

`md5hexCodes`, `sortKeyVS`, `«Float2Int(_)_FLOAT_Int_Float»`,
`«Int2Float(_,_,_)_FLOAT_Float_Int_Int_Int»`,
`«Int2String(_)_STRING-COMMON_String_Int»`,
`«_*Float__FLOAT_Float_Float_Float»`,
`«_+Float__FLOAT_Float_Float_Float»`,
`«_-Float__FLOAT_Float_Float_Float»`,
`«_/Float__FLOAT_Float_Float_Float»`,
`«_<Float__FLOAT_Bool_Float_Float»`, `«_==Bool_»`, `«_==Float_»`,
`«_==K_»`, `«_==String__STRING-COMMON_Bool_String_String»`,
`«_>=Float__FLOAT_Bool_Float_Float»`,
`«_>Float__FLOAT_Bool_Float_Float»`,
`«_^Float__FLOAT_Float_Float_Float»`, `«_^Int_»`,
`«absFloat(_)_FLOAT_Float_Float»`,
`«absInt(_)_INT-COMMON_Int_Int»`,
`«binAcc(_,_)_MPY-BUILTINS_IntSeq_Int_IntSeq»`,
`«buildVS(_,_,_,_)_MPY-SUBSCRIPT_ValSeq_ValSeq_Int_Int_Int»`,
`«ceilFloat(_)_FLOAT_Float_Float»`,
`«cntSub(_,_)_MPY-METHODS_Int_IntSeq_IntSeq»`,
`«floorFloat(_)_FLOAT_Float_Float»`,
`«maxFloat(_,_)_FLOAT_Float_Float_Float»`,
`«minFloat(_,_)_FLOAT_Float_Float_Float»`,
`«rootFloat(_,_)_FLOAT_Float_Float_Int»`, and
`«strToCodes(_)_MPY-STR_IntSeq_String»`.

Each of the 29 is a recorded non-propositional generated function axiom, with
its exact source, line, and type shown in
`evidence/proof-axiom-reconciliation.log`. There is no `sorryAx`, no
unrecorded dependency, and no candidate-added trust declaration.

## Evidence index

- Commands and environment note: `evidence/COMMANDS.md`
- Producer hashes and manifest reconciliation:
  `evidence/producer-provenance-check.log`
- Full reconstructed inventory:
  `evidence/inventory-reconstruction.log`
- Frozen K source and proof driver:
  `evidence/frozen-verification-source.log`,
  `evidence/stage1-proof-driver.log`
- Operational semantics excerpts:
  `evidence/operational-controls-source.log`,
  `evidence/operational-string-source.log`
- Successful Stage 4 preflight:
  `evidence/stage4-preflight-rerun-fixed.log`
- Independent hashes, bijection, target, and candidate identity:
  `evidence/stage4-candidate-integrity-fixed.log`
- Fresh proof clean/build:
  `evidence/fresh-proof-lake-clean.log`,
  `evidence/fresh-proof-lake-build.log`
- Independent proof gate:
  `evidence/proof-mechanical-gate.log`
- Exact `#print axioms` output and reconciliation:
  `evidence/proof-final-axioms-exact.log`,
  `evidence/proof-axiom-reconciliation.log`
- Successful adversarial operational-bridge check:
  `evidence/operational-bridge-adversarial-lean-with-map-fixed.log`

VERDICT: PASS
LEGITIMACY: LEGIT
