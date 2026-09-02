# Independent Stage 3–5 audit: HumanEval 159-eat

## Scope and outcome

The launcher and `AUDIT_MODE` both select `CLASSIFICATION_ONLY` for condition
`semantics` in `SUPPLIED_SEMANTICS` mode. The selected Stage 4 status is
`KLEAN_NO_OBLIGATIONS`; the audit input records no target, no Stage 5 result,
and null Stage 5 workspace/invocation hashes. `/candidate` is absent, as
required.

I independently reconstructed the Stage 3 rule inventory, reclassified its
only entry from the frozen K source and supplied operational semantics, checked
the exact Stage 3/Stage 4 bijections, and reran the trusted Stage 4 preflight.
The domain-lemma set is genuinely empty. No classification, generation, or
legitimacy defect was found.

## Producer-source and input provenance

I hashed the generation-time producer sources before judging Stage 4:

- `klean_export.py`:
  `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0`
- `klean.py`:
  `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1`

Both match `source-manifest.json` and `generator-manifest.json`. The immutable
generator image is
`sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000`
in both manifests, and its digest is also the basename of the producer-source
path recorded in `/audit-input.json`. The producer tree's pipeline hash is
`55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c`,
exactly the launcher-recorded value. Thus the required producer source is
present and consistent; no infrastructure `AUDIT_ERROR` applies.

The trusted hash reconstruction also matched:

- resolved audit input:
  `2e42766164678f151dc4a3bf41abc322cf884aabdfaf4eb8a191d2288e6efe63`
- Stage 1 pipeline tree:
  `6a0f0fcc4bd36fc082cbb6cc9bcf0b2f20805d36569fb222efdce4c6d33f3afc`
- frozen Stage 1 export tree:
  `a2410c2a198a171d7598da5b2f9a313f4dc08f6c4323f50a9b11170176b6f68b`
- Stage 3 manifest:
  `8b493c3aaab2a5ff661572594a9d4959b2ceea6b02d737d7e95fe5955d1e6cbc`
- selected Stage 2 tree:
  `bd9e7a25863b38b32a756235e6c4a1c7690bbd07d0254fa5f395a73ca0fe954d`
- selected Stage 4 tree:
  `8aa604d5fa1fa85ba050212e7c035c84d61cf35686e44360520b4b55da2d9d39`
- generated project export tree:
  `a0cf5eaf9aadf116db3b0ed44a53ffa14c8b73ee420d06ed82f314d3a5fff2ca`

All 34 individual `stage1_source_hashes` also matched. The selected artifact
hashes, sidecar bindings, toolchain lock, trust-inventory binding, obligation
map hash, and export-result bindings passed the trusted preflight. Full
machine-readable comparisons are in
`evidence/integrity-and-inventory.log`.

## Inventory reconstruction and bijection

Using the trusted `tools.k_rule_inventory.inventory_verification` on the frozen
workspace, `prove.sh` selects `EAT-VERIFICATION`. Its local module closure in
`verification.k` is exactly `["EAT-VERIFICATION"]`; the imported `MPY` module
is supplied by the required external semantics file and is not another module
declared locally in `verification.k`.

The closure contains exactly one rule:

- source span: lines 11–27
- module: `EAT-VERIFICATION`
- attributes: none
- normalized SHA-256:
  `0f9e6b9b44ef2a0419c9cc81385d08d4b41683c3674748beb8711d590083294b`
- source identity:
  `rule-0f9e6b9b44ef2a0419c9cc81385d08d4b41683c3674748beb8711d590083294b`

I separately joined the physical source lines, normalized whitespace, and
recomputed the same normalized hash and identity. Canonical JSON hashing of
the reconstructed rule list yields inventory hash
`7d0c83364859d0c5924b2ba19d1065780895e6dbeb4e9fa7000d1beb784fa695`.

`lemma-discovery.json` has exactly one entry in that same order and with that
identity. Its inventory hash matches. There are no omissions, extras,
duplicates, reordered identities, or changed hashes. The trusted Stage 3
contract validation independently returned the same one-entry definition set
and empty operational-rule, proved-derived-lemma, and domain-lemma sets.

## Independent classification judgment

The only rule expands the nullary symbol `eatClosure` into
`closureVal(("number", "need", "remaining"), BODY, 0)`. It is correctly a
`DEFINITION`, specifically a named proof term:

1. The parameter names and complete statement tree exactly match the frozen
   translation of `solution.py`: compare `need <= remaining`; in the true
   branch return `[number + need, remaining - need]`; otherwise return
   `[number + remaining, 0]`.
2. The supplied `FuncDef` rule installs exactly
   `closureVal(PNS, BODY, L)` in the defining scope. The source function is a
   module-level definition at location `0`, matching the final closure
   argument in `eatClosure`.
3. The spec merely binds `"eat"` to this exact closure value in scope `0`.
   Ordinary supplied semantics then performs name lookup, left-to-right
   argument evaluation, closure-frame creation, parameter binding, execution
   of the `If` and `Return`, integer comparison/arithmetic, list construction,
   heap allocation, and frame pop.

The rule does not rewrite a `<k>` configuration, intercept `Call`, skip the
function body, assert a result equation, or summarize carrot arithmetic. It is
therefore not an `OPERATIONAL_RULE` or operational bridge. There is no
proof-first/use-later sequence, so it is not a `PROVED_DERIVED_LEMMA`. It
states no additional mathematical fact and has no output-oriented guard, so
it is not a `DOMAIN_LEMMA`. It also has no `simplification` attribute.

The source and postcondition are body-sensitive. For example, `(1, 10, 10)`
distinguishes `<=` from `<` at the equality boundary; `(5, 6, 10)`
distinguishes adding `need` from hard-coding or adding `remaining`; and
`(2, 11, 5)` exercises the insufficient-stock branch. Those counterfactuals
would change the exact AST definition and the operational result. The two K
claims use `NEED <= REMAINING` and `REMAINING < NEED`, respectively, which are
disjoint and exhaustive over the bounded integer input domain stated by the
HumanEval prompt. The ordinary K integer and control rules suffice; no
problem-specific mathematical lemma is hidden by the classification.

Relevant frozen source and operational-semantics slices are preserved in
`evidence/semantic-source-slices.log`.

## Deterministic Stage 4 generation

The matched generation-time producer selects only independently classified
`domain_lemmas` as source obligations. Since that set is empty:

- `input-manifest.json` has one definition and `source_rules: []`;
- `obligation-map.json` has `source_rules: []`, `obligations: []`, and
  `trust_parameters: []`;
- the generator records obligation count `0`;
- the obligation map hash is
  `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`;
- the generator manifest, recorded preflight, audit input, and independent
  target parser all report `target: null`.

Thus the source-rule/obligation mapping is an exact empty-to-empty bijection.
There is no omitted or duplicated domain rule, no irrelevant or weakened
conjunct, no vacuous empty conjunction masquerading as a theorem, and no
generated target whose identity could drift.

I reran
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` against
the required three mounted inputs and the trusted lock. It exited zero after
fresh temporary `lake clean` and `lake build`, returning:

- status `KLEAN_NO_OBLIGATIONS`;
- obligation count `0`;
- target `null`;
- designated sorry count `0`;
- trust declaration count `47`;
- the exact frozen-input, discovery-manifest, and generated-tree hashes above.

The first invocation exposed a command-sandbox PID-namespace defect: Lean
4.22's executable discovery queried `/proc/<inner-pid>/exe`, while the sandbox
mounted the parent namespace's `/proc`. The initial failure is preserved. I
used the audit-authored `evidence/outer_pid_preload.c` only to make `getpid()`
return the outer `Pid:` already exposed by `/proc/self/status`; this permitted
the pinned immutable Lean executable to resolve itself and did not modify,
interpret, or weaken any candidate or generated source. The successful exact
preflight return is in `evidence/stage4-preflight.log`, and the environment
diagnosis is in `evidence/lean-environment.log`.

A later successful rerun emitted the independent `Lemmas` and `Rewrite` Lake
build lines in the opposite parallel order, changing only the diagnostic
output hash. The first successful rerun reproduced the recorded diagnostic
hash exactly; both runs returned identical structural hashes, target, counts,
command exit codes, and status. This does not affect deterministic generated
source identity.

## Stage 5 disposition

Because the independently classified true domain set is empty, the selected
`KLEAN_NO_OBLIGATIONS` path is correct. There must be no generated target and
no Stage 5 proof candidate; both conditions hold. Consequently a `Base` copy,
candidate clean build, `#print axioms Proof.final`, final-proof identity check,
and target-parameter operational-bridge audit are not applicable in this
launcher-selected mode.

Raw commands and results are indexed in `evidence/COMMANDS.md`.

VERDICT: PASS
LEGITIMACY: LEGIT
