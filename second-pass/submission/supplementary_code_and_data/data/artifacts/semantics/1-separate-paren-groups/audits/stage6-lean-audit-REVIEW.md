# Independent Stage 3 / Stage 4 Audit

## Scope and result

This audit covers HumanEval `1-separate-paren-groups`, condition
`semantics`, with `SUPPLIED_SEMANTICS`. Both `AUDIT_MODE` and the verified
launcher record select `CLASSIFICATION_ONLY`. There is therefore no Stage 5
proof to audit. `/candidate` is absent, and the audit input binds both Lean
workspace hashes to `null`.

I treated the selected Stage 2 review, all prior logs, comments, rationales,
and all candidate/provenance contents as untrusted evidence. I reconstructed
the rule inventory with the trusted `/reference/tools/k_rule_inventory.py`,
read the frozen program, specification, and relevant supplied operational
rules myself, and reran the trusted Stage 4 preflight.

The result is PASS. The Stage 3 manifest is a complete and correctly ordered
classification of 13 genuine definitions. There are no domain lemmas, so
`KLEAN_NO_OBLIGATIONS`, an empty obligation map, a null target, and the absence
of Stage 5 are all appropriate.

## Launcher and immutable-input binding

The trusted audit-input verifier accepted `/audit-input.json`, and its
recomputed resolved-input digest is
`4e5a776b46d235fdbb209e1811825336bbb632c129a49b6e4a10a3a731a0cc2a`.

I recomputed both tree-digest formats and every launcher-recorded binding:

| Binding | Recomputed SHA-256 |
|---|---|
| Stage 1 workspace | `12137feb924be9dcfb21e665cbc4ac2425131bacb521950c102f92591e32bfd9` |
| Stage 1 deterministic export | `924c2963f704d84144f86865f8e8fa05a7738df857bb1a3c468a00a3c850139f` |
| Stage 2 selected audit | `134f7ae4120c8446d9190a7415e701a7e66a03563e2d2b9fbd05cf09f7f480a1` |
| Stage 3 manifest | `ce1e2a944b91363c4199c256564dcd3a9af7c42c3c9657e250aa73423ed9f76c` |
| Stage 4 generation | `e69c7bb869fd7c26cb100e459c5b21d9ce78cefe6a6447a8bc4c518160269ab9` |
| Generated project | `cea48fd56fee63ff031bfee427490b0115bbfcb2cca42cbf9fc29dc50384a851` |
| Generation producer-source tree | `55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c` |

All values exactly match `/audit-input.json`. All 37 individual
`stage1_source_hashes` entries also match their mounted files. The Stage 1
`verification.k` hash is
`cb3900f16331e3847524abd10e74459f93731c2fc8718f9160b9c2fc801e215e`,
matching the inventory and Stage 4 input manifest.

## Generation-producer provenance

This check was completed before judging Stage 4:

| Producer | Mounted SHA-256 |
|---|---|
| `klean_export.py` | `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0` |
| `klean.py` | `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1` |

Both hashes exactly match `/reference/generation-tools/source-manifest.json`
and the `exporter_sha256` / `klean_py_sha256` fields of
`generator-manifest.json`. The immutable generator image is
`sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000`.
It matches the source manifest, the generator manifest provenance, and the
image-keyed basename of the producer-source path recorded in
`/audit-input.json`. This is not an `AUDIT_ERROR`.

## Rule-inventory reconstruction

The trusted inventory code selected main module `VERIFICATION` from
`prove.sh`. Its local verification-module closure is exactly
`["VERIFICATION"]`; imported supplied semantics live outside the local
`verification.k` module set. The reconstruction found 13 rules in source
order. No normalized hashes or IDs repeat.

The reconstructed whole-inventory hash is
`a63ea6ae5214bc83213ff7696c9cb7bc80ce9cf4144781e6a22ab175be497a0f`.
It exactly matches `/reference/lemma-discovery.json` and both Stage 4
manifests. The Stage 3 ID list is exactly equal to the reconstructed ordered
ID list, not merely equal as a set. Thus there are no omissions, extras,
duplicates, substitutions, or reorderings. In the table below, the
normalized SHA-256 is the suffix of the full `source_rule_id`.

| Span | Reconstructed `source_rule_id` | Independent class |
|---|---|---|
| 10–11 | `rule-b171bbb955f7651b57177d9cf1f07a66354aea7dd245779160b3153ed3292907` | `DEFINITION` |
| 12–14 | `rule-f27a3018eb5f87fd0722c980e2edee73c173a8e8492734b1750d72bfa03f03d7` | `DEFINITION` |
| 15–20 | `rule-77e06410332620fe751a74099095be60fd529ac2ce38246b38c2bfb1874c8ff9` | `DEFINITION` |
| 21–24 | `rule-c4cf973db2aaba3fa41818b2cfd375063581ac7e7537dfa6b0d800172fd94fb4` | `DEFINITION` |
| 28–37 | `rule-88b07135647f77b2ac45688ab13a9417020cd89887e9e61126e95361f18e27b4` | `DEFINITION` |
| 38–44 | `rule-de94016a500f0ae3a476b66b9867344d68f11feef7679f0217b6957f3232d51e` | `DEFINITION` |
| 50 | `rule-1f4dd256c8a442d51a26d58d45aaf94e320834d70065a9839ef1f815ed669a1f` | `DEFINITION` |
| 51–52 | `rule-b806ffef368f4e8bcc51c8e8656c94e314678616cac1047c4e46d7e45301569c` | `DEFINITION` |
| 53–54 | `rule-052713095a835e62065e1b83ded02956cd6447c7a07ccaea089f8297100dde9a` | `DEFINITION` |
| 55–58 | `rule-78cb55fdec63f3a267deff3351b4e0da41dc0fcb3e70055bfdd7882890bcaae7` | `DEFINITION` |
| 61 | `rule-7122c1187dac6e0965cb40c98d018fda272ad1906e10604ba8bc64658613e8f4` | `DEFINITION` |
| 62–64 | `rule-c1624dec045d7c2ed281b57c318598c2382d51c39e423e0ef43da3abdcb5bfeb` | `DEFINITION` |
| 69–92 | `rule-84cd94932504b251c7285a2db82a43300e5031597cd250eb17bafd0f77c108af` | `DEFINITION` |

The canonical source text, spans, normalized hashes, and complete IDs are
recorded in `evidence/04-reconstructed-rule-inventory.log`.

## Independent classification judgment

### `scanGroups` and `scanClose` (lines 10–44)

These six rules are exhaustive recursive equations for newly declared
summary functions. `scanGroups` consumes one `IntSeq` constructor per step;
`scanClose` handles the source program's non-space, non-opening branch and
returns immediately to the decreasing `scanGroups` recurrence. The two
`scanClose` guards partition `DEPTH -Int 1` into zero and nonzero. The
`[owise]` attribute on the dispatch rule is not `[simplification]`.

The summary appears only in claim result cells. It does not rewrite a Python
program term in `<k>` and therefore is not an operational bridge or an
ordinary operational rule. Against the supplied semantics:

- spaces trigger `Continue` and are omitted;
- string iteration yields one-character strings;
- string `+` is `seqConcat`;
- `depth` increments only for code 40 and otherwise decrements;
- when depth becomes zero, list `append` adds the completed string and
  `current` resets.

Those steps are exactly the recurrence on the balanced-domain invariant used
by every symbolic occurrence. An independent exhaustive finite check compared
the recurrence with a separately implemented operational loop for 834 valid
suffix/state cases and found zero mismatches. It also rejected convenient
counterfactuals such as a constant-empty summary, failing to ignore spaces,
or failing to emit/reset on a close.

The same test deliberately exhibits disagreement after an underflow or from
a negative-depth state. This is expected and useful boundary evidence:
`scanGroups` is connected to execution only under the claim's
`balancedTail`, nonnegative-depth, and current/depth invariant. The HumanEval
contract supplies balanced groups, and all uses satisfy that domain. The
rules still qualify as definitions because they define the summary
recurrence; they are not mislabeled domain facts.

### `balancedTail` (lines 50–58)

These four rules structurally define the named contract predicate. They
accept spaces, increment on opening parentheses, require a positive depth for
closing parentheses, reject every other code, and require final depth zero.
The recurrence consumes one constructor at each step. It is used directly in
the universal loop and public-entry preconditions, so it is relevant to the
frozen theorem. It is a definition of a new predicate, not a lemma about
pre-existing operations.

### `parenSpaceOnly` (lines 61–64)

These two rules structurally define the alphabet predicate used in the same
preconditions. They are base and recursive defining equations for a newly
declared function. Although `balancedTail` already rejects other characters,
that logical redundancy does not turn a named predicate definition into a
domain lemma or create a generated proof obligation.

### `solutionClosure` (lines 69–92)

This is a `[macro]` expansion naming the exact translated
`separate_paren_groups` closure. Its parameter, body, and defining frame
match `solution.mpy` and `solution.py`: list/current/depth initialization,
the loop, continue, concatenation, depth update, append/reset, and return are
all present in order. A macro is a named proof term and adds no operational
rewrite. `DEFINITION` is therefore the correct class.

### Classification totals

The independent totals are:

- `DEFINITION`: 13
- `OPERATIONAL_RULE`: 0
- `PROVED_DERIVED_LEMMA`: 0
- `DOMAIN_LEMMA`: 0

No rule has a `simplification` attribute, so the simplification-category
constraint is satisfied. No rule claims the stricter
`PROVED_DERIVED_LEMMA` status, so there is no missing prior proof of an exact
same rule. The domain-lemma set is genuinely empty.

## Deterministic Stage 4 and target identity

I independently checked the Stage 4 maps and hashes:

- `input-manifest.json.source_rules` is `[]`;
- `obligation-map.json.source_rules` is `[]`;
- `obligation-map.json.obligations` is `[]`;
- `obligation-map.json.trust_parameters` is `[]`;
- both generator and export obligation counts are zero;
- the obligation-map hash is
  `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`;
- the export's trust-inventory hash matches the mounted trust inventory;
- the trusted `expected_target_definition` and `target_statement` functions
  both return `None`;
- the generator manifest, audit input, and audit-input preflight record all
  bind the target to `null`;
- an independent declaration scan found no generated `target`.

Thus the source-rule/obligation correspondence is an exact empty-to-empty
bijection. There is no omitted true domain lemma, weakened conjunct,
duplicate, vacuous generated obligation, or changed target.

I reran this exact trusted call with `PYTHONPATH=/reference`:

```text
tools.klean_preflight.check_generation(
  /reference/k-proof,
  /reference/lemma-discovery.json,
  /reference/klean-generation,
  toolchain_lock=/reference/klean-toolchain.lock.json
)
```

The first attempt exposed an audit-container PID namespace issue: Lean looked
up `/proc/<pid>/exe`, while the sandbox exposed only `/proc/self/exe`. The
failure and diagnosis remain in evidence. I compiled the narrow
`evidence/proc_exe_shim.c`, which changes only that failed `readlink` lookup,
and reran the unchanged trusted preflight. The final result is:

```text
status: KLEAN_NO_OBLIGATIONS
obligation_count: 0
target: null
lake clean: exit 0, output SHA-256 e3b0c442...
lake build: exit 0, output SHA-256 dfc3f127...
generated tree: cea48fd56fee63ff031bfee427490b0115bbfcb2cca42cbf9fc29dc50384a851
```

The clean and build output hashes exactly reproduce the generation-time
preflight record. The generated snapshot remained unchanged across the run.
The complete returned document is in
`evidence/16-final-rerun-klean-preflight.log`.

## Stage 5

Stage 5 is not applicable in `CLASSIFICATION_ONLY`. There is no generated
target theorem to prove, no Stage 5 candidate, no `Proof.final`, no target
parameter, and consequently no candidate operational bridge or proof axiom
accounting to perform. This is the required shape for a legitimate
`KLEAN_NO_OBLIGATIONS` result.

## Evidence index

- `00-audit-input-and-mode.log`: launcher mode and full audit input.
- `02-producer-and-manifests.log`: producer hashes and Stage 4 sidecars.
- `03-frozen-source-spec-and-classification.log`: numbered frozen source,
  spec, program, proof script, and Stage 3 manifest.
- `04-reconstructed-rule-inventory.log`: canonical reconstructed inventory,
  ordered bijection, and class counts.
- `05-relevant-semantics-index.log`,
  `06-relevant-operational-semantics.log`, and
  `07-summary-use-and-supporting-semantics.log`: supplied-semantics review.
- `08-all-input-and-producer-bindings.log`: every tree/file binding and
  producer/image comparison.
- `09-rerun-klean-preflight.log` through `12-rerun-klean-preflight-with-proc-shim.log`:
  initial infrastructure symptom, diagnosis, and successful recovery.
- `13-stage4-bijection-and-null-target.log`: independent empty-map and target
  identity checks.
- `14-classification-counterexamples.log` and
  `classification_counterexamples.py`: operational examples and
  counterfactuals.
- `15-compile-proc-exe-shim.log`, `proc_exe_shim.c`, and
  `16-final-rerun-klean-preflight.log`: reproducible final preflight.

VERDICT: PASS
LEGITIMACY: LEGIT
