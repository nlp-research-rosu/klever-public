# Independent Stage 3–5 audit: HumanEval `33-sort-third`

## Scope and result

I audited condition `semantics`, semantics mode `SUPPLIED_SEMANTICS`.
`AUDIT_MODE` and the signed launcher resolution both select
`CLASSIFICATION_ONLY`. The selected Stage 4 status is
`KLEAN_NO_OBLIGATIONS`; `/candidate` is absent, and all Stage 5 paths,
hashes, results, and target fields are null. Accordingly, this review covers
the Stage 3 classification and deterministic Stage 4 generation. No Stage 5
Lean proof or `Proof.final` exists to audit.

I treated the mounted workspaces, manifests, logs, and earlier reviews only as
untrusted evidence. Generation-time producer files were hashed but never
imported or executed. Mechanical reconstruction and checking used the trusted
code under `/reference/tools`.

## Producer provenance gate

This gate passed before judging Stage 4.

| Item | Independently observed SHA-256 |
|---|---|
| `/reference/generation-tools/klean_export.py` | `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0` |
| `/reference/generation-tools/klean.py` | `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1` |
| Producer bundle, launcher tree-hash algorithm | `55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c` |

The two file hashes agree exactly with both
`source-manifest.json` and `generator-manifest.json`. The bundle contains
exactly `klean_export.py`, `klean.py`, and `source-manifest.json`, with no
linked or unsupported entries. Both manifests record generator image
`sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000`;
the launcher-recorded producer-source path has the same immutable image key.
The bundle hash also equals
`resolution.hashes.generation_producer_sources_sha256`.

Raw evidence is in
[producer-provenance-hashes.log](evidence/producer-provenance-hashes.log) and
the `producer_checks` section of
[structural-checks.json](evidence/structural-checks.json).

## Rule-inventory reconstruction

I ran `tools.k_rule_inventory.inventory_verification` on the frozen
`/reference/k-proof` workspace. `prove.sh` selects `VERIFICATION` as the main
module. The local verification-module closure contains exactly that module;
`MPY` is an imported supplied-semantics module, not another module locally
defined in `verification.k`.

Reconstruction produced:

- `verification.k` SHA-256:
  `9bff2a4c229f69dd127eeed47cb06a72b941b5291ae5c2d8cce1d1abd7fd5011`;
- 11 rules in source order;
- inventory SHA-256:
  `ff2dfd05c27c0c19c89ed681e9803475687013606f4a417144f2d015eb50c7d4`.

For each rule, I recomputed the physical source span, normalized text,
normalized SHA-256, and `source_rule_id`. Every identifier is exactly
`rule-<normalized_sha256>`.

| Lines | `source_rule_id` | Independent classification |
|---|---|---|
| 7–21 | `rule-30f896f4a78788a4df1bfd241f27a89c6a07e729eefa54e20e31be5cceb2c6bb` | `DEFINITION` |
| 24–36 | `rule-21093175dbb8f2943626cf550979b0da747b2af38d29798aa0321b8a05e4bb0c` | `DEFINITION` |
| 39–40 | `rule-7c593d3abb10208b9212ec827fa30fc4ff49f3dfa4acc1d6d12a35777a7a8b39` | `DEFINITION` |
| 45–50 | `rule-10b3747ff64f7edc5c2b2739b560b4381fc410dad54630e3f5c2a3f0a1b3d3de` | `DEFINITION` |
| 56–58 | `rule-6bf57cc70b116bf57d62cb53019c3bc3a8afd519690929ee08b6bb00a2334384` | `DEFINITION` |
| 59–60 | `rule-d67c9157105f75b20f186a8416a8374e66a206669477ae93c784de085518a12d` | `DEFINITION` |
| 64 | `rule-265d11e00e4fbf524925232abb23c7127d163ff9a4a0fb40c8dd70453168070e` | `DEFINITION` |
| 65–73 | `rule-48d8e0a8b82574ed851e8ab7b2c422bde84aba1f278d3e73a9ee43b27ebff908` | `DEFINITION` |
| 76 | `rule-5003da3d7156c8d67318d1d506c428d29a27f6057012a2b10ef5b4a0bc66f7a0` | `DEFINITION` |
| 77–78 | `rule-7b6f7fc609a2303132cffc76dbf0fb13227389bda8ad1906153b016750d88a66` | `DEFINITION` |
| 81–86 | `rule-784a582d08c3bf5c89efdcf597adcf9e84c7d8e69114ac1324c993790561826b` | `DEFINITION` |

The protected Stage 3 manifest contains exactly these 11 identities, once
each and in this exact order. There are no omissions, extras, duplicates,
reordered identities, hash changes, or unaccounted classifications. Its
inventory hash matches the independent value. The Stage 4 input manifest's
full ordered definition records—including spans, rule text, hashes,
classifications, and rationales—also equal the independently validated
records.

The complete reconstructed text and per-rule calculations are in
[structural-checks.json](evidence/structural-checks.json); the frozen source is
captured in [verification-source.log](evidence/verification-source.log).

## Independent classification judgment

The true classification counts are:

| Classification | Count |
|---|---:|
| `DEFINITION` | 11 |
| `OPERATIONAL_RULE` | 0 |
| `PROVED_DERIVED_LEMMA` | 0 |
| `DOMAIN_LEMMA` | 0 |

The first four rules define named proof terms for the exact translated
program:

- `sortThirdBody` expands to the loop body;
- `sortThirdFunctionBody` expands to the complete function statements;
- `sortThirdClosure` names the corresponding closure value; and
- `sortThirdModule` names the module containing that function.

They introduce fresh nullary symbols and expand them to AST/value terms. They
do not match or shortcut a running `<k>` configuration and therefore are
definitions, not operational rules or domain facts. Comparison with
`solution.py` and `solution.mpy` confirms the expansions include the same
slice, sort call, initialization, loop branch, append operations, index
increment, and return.

The remaining seven rules define four fresh mathematical summaries:

- The two guarded `thirdValue` equations define its divisible-by-three and
  complementary branches. Supplied `int.k` defines `%` as `pyMod` and `//` as
  `(I - pyMod(I, 3)) / 3`, so the selected sorted-list index is exactly the
  source expression `i // 3`.
- The base and recursive `sortThirdAcc` equations define a structural fold
  over the original input. The recursive step advances `I` by one and appends
  exactly `thirdValue(V, SORTED, I)`. This mirrors the supplied `For`
  transition and the in-place `list.append` heap rule.
- The two `lastLoopValue` equations define the structurally last loop-bound
  value (or preserve the old value for an empty suffix), exactly the state
  component used by the loop claim.
- `sortThird` defines the top-level summary by starting the fold at index zero
  with an empty accumulator and
  `sortVS(buildVS(INPUT, 0, vsLen(INPUT), 3))`. Supplied subscript semantics
  defines the positive-step slice with `buildVS`; supplied sort semantics
  routes `sorted(list(VS))` to the frozen opaque primitive `sortVS(VS)`.

These equations introduce and define fresh summary functions. None asserts a
property of an existing arithmetic, sequence, sorting, or operational symbol;
none is a disguised domain theorem. The recurrences structurally decrease on
their first sequence argument, and the `thirdValue` guards (`pyMod == 0` and
`pyMod =/= 0`) are complementary. The rules' independently reconstructed
attribute lists are all empty, so there is no unclassified
`simplification` rule; in any event, every inventory rule is classified as
the permitted `DEFINITION`.

There is no claimed derived lemma, so the “prove first without the rule, then
use later” criterion is not invoked. There is no claimed domain lemma to test
for relevance. Most importantly for the no-obligation result, independent
classification finds no true domain lemma hidden among the definitions.

The operational-semantics excerpts used for this judgment are retained in
[semantics-values.log](evidence/semantics-values.log) and
[semantics-execution.log](evidence/semantics-execution.log). Source, formal
claim, and proof-driver excerpts are in
[program-spec-proof-driver.log](evidence/program-spec-proof-driver.log).

## Hash and manifest integrity

Every launcher-recorded top-level hash recomputed exactly:

| Artifact/hash scheme | Observed and recorded SHA-256 |
|---|---|
| Stage 1 workspace, pipeline tree | `3fc5c84a395d17041f73de989b36a1348c10f8557960870e682fb7c3e2831891` |
| Frozen Stage 1 export, Klean tree | `c9308e9f17484dccd728040fb9acadf95acac569753906baee8e5cff9a29b39b` |
| Stage 3 discovery manifest | `8bb08e686df0a040f57dec6376e193bae2dcc993dfe51595a4be3efe1ca7847e` |
| Selected Stage 2 audit tree | `9a950bc9008e561b2d0e2210ba72cee9763ba24a57abcf1dbcf3f21dbbc4cdc1` |
| Selected Stage 4 generation tree | `f6aedddcef6affd4ea01d3ae01e87b30fcadb4e83249c583994dde8180c0045f` |
| Producer-source bundle tree | `55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c` |
| Generated Lean project, Klean tree | `18048b99729240ac89eecb9c0a989e84dbf09dd82c531dc0748df9c574bedea3` |

All per-file Stage 1 source hashes also match. The signed audit-input envelope
and its canonical resolution digest validate, and the copy under
`/audit-output` is byte-identical to `/audit-input.json`.

The generator toolchain record equals
`/reference/klean-toolchain.lock.json`. Generator, input, export, obligation,
and trust-inventory hashes agree across the sidecars and launcher input. The
obligation-map file hash is
`cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`.

## Trusted Stage 4 preflight

I reran `tools.klean_preflight.check_generation` with
`PYTHONPATH=/reference` and exactly these inputs:

```text
frozen_input       = /reference/k-proof
discovery_manifest = /reference/lemma-discovery.json
generation         = /reference/klean-generation
toolchain_lock     = /reference/klean-toolchain.lock.json
```

The first invocation exposed an audit-container PID-namespace issue: Lean
4.22 reads `/proc/<getpid>/exe`, while this container exposes only the
equivalent `/proc/self/exe`. That attempt and error are preserved. I compiled
a 20-line preload shim that changes only this failing `readlink` argument;
the shim source and hash are retained. It does not alter the generated
project, producer sources, Lean inputs, or checker. With this environment
repair, the same trusted preflight completed.

Returned result:

```text
status                  = KLEAN_NO_OBLIGATIONS
obligation_count        = 0
target                  = null
trust_declaration_count = 51
designated_sorry_count  = 0
lake clean              = exit 0, empty output
lake build              = exit 0
```

The build output SHA-256 is
`647163f0e5b5c5443e3108b4d0bdc854505d0b3f97c6102bcabe54a38ef2f901`.
Only four unused-variable linter warnings were emitted. The returned JSON is
exactly equal to both the published Stage 4 preflight and the launcher-recorded
preflight.

Evidence:

- [preflight-result.json](evidence/preflight-result.json)
- [preflight-lake-clean.log](evidence/preflight-lake-clean.log)
- [preflight-lake-build.log](evidence/preflight-lake-build.log)
- [preflight-comparison.log](evidence/preflight-comparison.log)
- [preflight-command.log](evidence/preflight-command.log) (initial
  environment failure)
- [preflight-command-rerun.log](evidence/preflight-command-rerun.log)
- [lean_app_path_shim.c](evidence/lean_app_path_shim.c)
- [lean-shim-validation.log](evidence/lean-shim-validation.log)

## Obligation bijection and target identity

The independently classified domain set is genuinely empty. Each Stage 4
representation agrees exactly:

```text
independent DOMAIN_LEMMA source rules = []
input-manifest source_rules           = []
obligation-map source_rules           = []
obligation-map obligations            = []
obligation-map trust_parameters       = []
generator obligation_count            = 0
export obligation_count               = 0
```

Thus the source-rule/obligation mapping is a true empty bijection. There can
be no omission, duplicate, reordering, irrelevant obligation, weakened
conjunct, or vacuous generated conjunct because there is no eligible source
rule or conjunct.

`tools.klean_export.expected_target_definition` returned null, and
`tools.klean_export.target_statement` found no generated target. The generator
manifest and launcher audit input also record target null. A direct generated
source scan found no `KleanTarget`, `Proof.final`, final theorem, `sorry`,
`admit`, or `unsafe`. This is exactly the required fixed result for a genuine
zero-domain-lemma set. See
[generated-target-scan.log](evidence/generated-target-scan.log).

The trusted model-free final gate also returned `status: PASS`,
`mode: CLASSIFICATION_ONLY`, target null, an empty `used_axioms` list, and no
diagnostics. Its `semantic_classification` is deliberately
`NOT_EVALUATED`; that mechanical gate does not replace the independent
classification judgment above. See
[mechanical-final-gate.json](evidence/mechanical-final-gate.json) and
[mechanical-final-gate.log](evidence/mechanical-final-gate.log).

## Stage 5 applicability

Stage 5 is correctly absent:

- audit mode is `CLASSIFICATION_ONLY`;
- the selected Stage 4 result is `KLEAN_NO_OBLIGATIONS`;
- no target was generated;
- the launcher records no Lean workspace, invocation, result, or hashes; and
- `/candidate` does not exist.

Therefore no clean candidate build, target-shadowing check,
`#print axioms Proof.final`, proof-identity check, or operational-bridge
parameter audit is applicable. Creating or accepting a Stage 5 proof in this
mode would itself violate the contract.

## Conclusion

The protected Stage 3 manifest is a complete, ordered, hash-exact
classification of the frozen local verification-rule closure. Independent
semantic review confirms that all 11 rules are genuine definitions and that
the true domain-lemma set is empty. Producer provenance, all recorded hashes,
the deterministic generation manifests, the empty source-rule/obligation
bijection, and the absence of a generated target all check out. The trusted
preflight reproduces `KLEAN_NO_OBLIGATIONS` with a clean build. No Stage 5
candidate is required or permitted.

VERDICT: PASS
LEGITIMACY: LEGIT
