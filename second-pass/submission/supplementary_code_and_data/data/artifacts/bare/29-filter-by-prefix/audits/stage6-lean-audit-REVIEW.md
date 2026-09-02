# Independent Stage 3–5 audit: `29-filter-by-prefix`

## Scope and result

The launcher and `AUDIT_MODE` both record `CLASSIFICATION_ONLY` for condition
`bare` and semantics mode `GENERATED_SEMANTICS`. I independently audited the
frozen Stage 1 rule inventory, every Stage 3 classification, producer
provenance, deterministic Stage 4 generation, the source-rule/obligation
bijection, and target identity. I did not rely on the selected Stage 2 verdict,
its review, or any earlier classification or PASS.

The independent classification has six `DEFINITION` rules and no
`DOMAIN_LEMMA`, `OPERATIONAL_RULE`, or `PROVED_DERIVED_LEMMA` rules. Therefore
the true domain-lemma set is empty. Stage 4 correctly has zero obligations, no
generated target, and no Stage 5 candidate.

Raw commands, scripts, complete outputs, and exit codes are under
`/audit-output/evidence/`; `evidence/COMMANDS.md` is the index.

## Producer provenance and immutable inputs

I hashed the two required producer files before judging Stage 4:

| Producer | Observed and expected SHA-256 |
|---|---|
| `klean_export.py` | `4fa919ac98483620c7024ed7424c8b19f21406a2146feafad84ab4c813117881` |
| `klean.py` | `b8bcddc01151a647e69b336435af38cd8dd94239a3ac96da0d45c2aa60bbb6f0` |

Those hashes agree exactly with `generator-manifest.json` and
`source-manifest.json`. The source manifest has exactly the expected three-file
bundle (`klean_export.py`, `klean.py`, and the source manifest itself), and its
image ID is
`sha256:686134aa922debe485b0e3bb0a6476ca48e04c580ceb66d0f01003c97cdcab65`.
That is also the generator manifest provenance image ID and the final component
of the producer-source path recorded in `/audit-input.json`. The complete
producer bundle reproduces the launcher-recorded artifact hash
`5e674104ca65fed1c0a0004d3011762dcd335fa0f6620bac310ec19f1f143cbc`.
Producer provenance therefore passes; there is no infrastructure
`AUDIT_ERROR`.

The trusted launcher contract accepted `/audit-input.json`, and its recomputed
resolved-input digest is
`8968143ddf229410e81c483830650206806733362e6ac9dd11410bc9aaaf87d0`.
All recorded artifact hashes reproduce:

| Frozen artifact | Recomputed SHA-256 |
|---|---|
| Stage 1 selected workspace | `12c02e9aacde66dfeb724fcbb166d582e1caebc8bf2325940f085e7e8c57b032` |
| Stage 1 deterministic-export tree | `ef674ed91872f711a6e7277686d77196414c31940b02cccd1cdd6f6cc40204e2` |
| Stage 2 selected audit | `0ce14ede1718bf8340b609c9ab782404c216bd128c815056572e311819aee86b` |
| Stage 3 discovery manifest | `f78d1361ed303b9bbdb5f58572f6f89311d1bd2f47495916f0f77a9311db20b0` |
| Stage 4 selected generation | `cba74d5b4762668cbba223e3d209702afc9d098af8a3d5f6b74610d17668a2f6` |
| Stage 4 generated project | `4eef76e85b4ab2259ceb6df8cfcd3635998c48047c99367e39f3db1b97e29964` |

The complete per-file Stage 1 hash map also equals `stage1_source_hashes` in the
audit input. In particular, frozen `verification.k` is
`21bcc986ec2e12d8f7d353e965ca3c3d66783a742f586831923681796cb1fb53`.
The Lean workspace and invocation hashes are correctly null in this mode.

Evidence: `00_provenance_check.py` and `00_provenance_check.log`.

## Inventory reconstruction

I ran the trusted canonical inventory code against
`/reference/k-proof/verification.k`. The selected module is `VERIFICATION`; its
local file closure is exactly `["VERIFICATION"]`. The code reconstructed six
rules in physical source order. For each rule I independently re-sliced the
reported physical lines, normalized the exact text by whitespace joining,
recomputed the normalized SHA-256, and reconstructed
`source_rule_id = "rule-" + normalized_sha256`.

The canonical rule sequence is:

| Lines | Normalized SHA-256 (and `rule-` source identity) | Attributes | Independent class |
|---:|---|---|---|
| 9 | `ac0ad2ee8798223b8d0e68f0c8edbc98f7bc9e543cfba6d48da1cb3944018a09` | none | `DEFINITION` |
| 10 | `06feaa8530d12459c98e102bb67013c17f71df32409bc8a99a2f757e94c488e4` | none | `DEFINITION` |
| 11–13 | `01b01b51ccb5f30e112b181d8839f4789ef0b9fcc3d5f02a98fb2f9bc4993603` | `simplification` | `DEFINITION` |
| 14–16 | `47fea1538ad0507cb91d9ff53c08576f802ff5036458e5bb1455a1df4a263e0f` | `simplification` | `DEFINITION` |
| 24–27 | `95ab8d93624db21de3cda929dad814e59f3f67a33233478cbd9d06222bf7e749` | none | `DEFINITION` |
| 29–35 | `11b0160cb56a842bbc83e22736af7b949ed225b38ba35c6c68f048a2c056b8a0` | none | `DEFINITION` |

The whole reconstructed inventory hash is
`3ecb060b882616a370eae5419482adde58064f9a3c6374dbc81a0471bc36511e`.
It matches `/reference/lemma-discovery.json`.

The manifest has exactly six distinct identities. Its identity list is exactly
the canonical list above, including order; there are no omissions, duplicates,
extras, reordered entries, changed hashes, or unaccounted classifications.
The trusted Stage 3 boundary validator also accepts the exact manifest schema
and keys.

Evidence: `01_inventory_check.py`, `01_inventory_check.log`, and
`04_frozen_source_listing.log`.

## Independent classification judgment

I classified by the frozen rule text and its role in the operational
semantics, not by the manifest rationales:

1. Line 9 defines the fresh mathematical summary `filterByPrefix` by invoking
   `filterAcc` with the empty accumulator. It is a definition, not a fact about
   pre-existing operations.
2. Line 10 is the base recurrence for the fresh `filterAcc` summary.
3. Lines 11–13 are the matching-head recurrence. It consumes the input tail and
   appends the head to the accumulator.
4. Lines 14–16 are the nonmatching-head recurrence. It consumes the input tail
   without changing the accumulator.
5. Lines 24–27 define the named proof term/macro `loopBody()` as the exact
   translated `If`/`append` statement sequence.
6. Lines 29–35 define the named proof term/macro `solutionProgram()` as the
   translated module executed by the end-to-end claim.

The two simplification rules are therefore both `DEFINITION`, as required.
Their guards are exhaustive and disjoint once the total K function
`startsWith` returns a Boolean, and recursion strictly descends through the
remaining list.

None of the six rules is an ordinary execution/observation rule: the actual
environment, call, sequencing, loop, condition, append, and return rules are in
the frozen `MPY` operational semantics. None is a derived lemma about existing
symbols, and Stage 3 claims no `PROVED_DERIVED_LEMMA`; consequently there is no
claim that needs the special “prove it first without the rule, then use it”
history. None is a `DOMAIN_LEMMA`: the first four introduce a fresh summary and
its recurrence, and the last two introduce named syntax terms. There is
therefore no domain lemma hidden under another class and no irrelevant claimed
domain lemma.

The definitions are relevant to the exact program and postcondition.
`solutionProgram()` expands to the same import, function, initialization,
loop, prefix test, append, and return structure as frozen `solution.mpy` and
`solution.py`; omitted concrete list tails elaborate to `.Strings` and
`.Stmts`. The spec's loop claim returns `filterAcc(INPUT, PREFIX, ACC)`, and
the end-to-end claim returns `filterByPrefix(INPUT, PREFIX)`.

Operationally, `appendOne` appends at the list end, `startsWith` implements the
length/slice prefix test, the loop visits each input head in order, and the
append call updates `result` only on the true branch. Structural induction on
the remaining list proves the `filterAcc` recurrence matches that loop:
the empty case returns the incoming accumulator; each cons case takes the same
Boolean branch, performs the same append or no-op, and applies the induction
hypothesis to the tail. Thus the summary preserves order and duplicates and
drops exactly the nonmatching strings.

As finite adversarial support, an independent model of those frozen K rules
checked 112,344 combinations with zero mismatches. Cases include empty input,
empty prefix, a longer prefix, duplicates, embedded NUL, and non-ASCII strings.
Constant-empty, identity, and prepend/reversal counterfactual summaries are
distinguished by explicit witnesses. This finite run supports, but does not
replace, the structural argument above.

Evidence: `04_semantic_model_check.py` and
`04_semantic_model_check.log`.

## Deterministic Stage 4 generation

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`
on the mandated Stage 1 workspace, Stage 3 manifest, Stage 4 generation, and
pinned lock file. The first attempt exposed an audit-image launcher issue:
Elan could report Lake's version but could not detect the Lake installation or
resolve Lean's application path. I preserved that failure. I then used a
temporary sysroot and a local launcher linked to the pinned Lean 4.22 shared
library; it only restores CLI dispatch and search-path initialization, and
does not modify any mounted or generated input. An intermediate option-parser
failure is also preserved.

The final rerun executes the unchanged trusted preflight function successfully.
Its returned JSON is byte-for-byte equal as a parsed document to
`resolution.stage4_preflight` in `/audit-input.json`:

- `lake clean`: exit 0, empty output hash
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`;
- `lake build`: exit 0, complete output hash
  `273cedf04decaa030497f7ce2fd79ba55c5ab82632879a47c0cbd316c8fcfbca`;
- generated tree:
  `4eef76e85b4ab2259ceb6df8cfcd3635998c48047c99367e39f3db1b97e29964`;
- status: `KLEAN_NO_OBLIGATIONS`;
- obligation count: 0;
- target: null;
- generated proof holes: 0; and
- recorded non-propositional trust declarations: 44.

The successful build output lists all seven generated modules and ends
`Build completed successfully.` The exact returned evidence is
`02_preflight_return.json`; complete failed and successful transcripts and the
launcher source are preserved beside it.

I also independently recomputed the Stage 4 mapping:

- independently classified domain source rules: `[]`;
- `input-manifest.json` source rules: `[]`;
- `obligation-map.json` source rules: `[]`;
- generated obligations: `[]`;
- obligation IDs: `[]`;
- trust parameters: `[]`.

This is an exact empty-to-empty bijection. There can be no omitted eligible
rule because the independently reconstructed domain set is empty; there are no
duplicates, irrelevant or weakened obligations, and no conjunct—vacuous or
otherwise. The obligation-map hash is
`cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`,
and the trust-inventory hash is
`e728c634a0c5896547187f3c957ca173ff58391725f697fb73a9b79062088f3e`.
Both match their binding manifests.

`expected_target_definition(obligation-map)` is null, the trusted generated
target extractor returns null, `generator-manifest.json` has target null,
`/audit-input.json` has target null, and the generated `Lemmas.lean` declares
no target. The fixed generated target is therefore genuinely absent rather
than weakened, replaced, duplicated, or made vacuous.

Evidence: `02_preflight_rerun.py`, `02_preflight_rerun.log`,
`02_preflight_rerun_success.log`,
`02_preflight_rerun_success_2.log`, `02_preflight_return.json`,
`02_lean_environment_wrapper.c`, `03_manifest_bijection_check.py`, and
`03_manifest_bijection_check_2.log`.

## Stage 5 applicability

Stage 5 is not applicable. `AUDIT_MODE` and the resolved mode are both
`CLASSIFICATION_ONLY`; the audit input has null Stage 5 result, workspace,
invocation, target, and Lean hashes. `/candidate` is absent. This is exactly
the required shape for a genuinely empty domain-lemma set and
`KLEAN_NO_OBLIGATIONS`. No clean candidate build, `#print axioms Proof.final`,
proof-identity check, or operational-bridge parameter audit is called for in
this mode.

## Conclusion

Stage 3 is complete, bijective, order-preserving, and mathematically correctly
classified. Stage 4 is producer-authentic, hash-bound to the frozen inputs,
mechanically reproducible, and correctly emits neither obligations nor a
target. The selected `KLEAN_NO_OBLIGATIONS` status is justified by a genuinely
empty independently classified domain set, and the absence of Stage 5 is
correct.

VERDICT: PASS
LEGITIMACY: LEGIT
