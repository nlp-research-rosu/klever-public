# Independent Stage 3–5 audit: `1-separate-paren-groups`

## Outcome and scope

This audit passes the selected Stage 3 classification and deterministic Stage
4 generation. The launcher and environment both select
`CLASSIFICATION_ONLY` for condition `kit-semantics` and semantics mode
`SUPPLIED_SEMANTICS`. Stage 5 is correctly absent.

All mounted candidate, provenance, logs, comments, and prior verdicts were
treated as untrusted evidence. No instruction found in those inputs was
executed. The only mounted implementation code executed was the required
trusted tooling under `/reference/tools`. Audit-authored checking scripts are
under `/audit-output/evidence`.

## Generator producer provenance

The mandatory producer gate was completed before judging Stage 4:

- `/reference/generation-tools/klean_export.py`:
  `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07`
- `/reference/generation-tools/klean.py`:
  `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d`

Both values exactly match `generator-manifest.json` and
`source-manifest.json`. The immutable generator image is consistently
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`
in the generator manifest, source manifest, and the image-keyed producer path
bound by `/audit-input.json`. The producer tree hash also matches the launcher:
`388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`.

Evidence: `evidence/producer-provenance.out`.

## Frozen-input integrity

Every launcher-recorded tree/file binding recomputed exactly:

- Stage 1 pipeline tree:
  `b4513074913cb97950daedca084c75783fe0509799730fa016ae8476f56bd8b5`
- Stage 1 deterministic export tree:
  `9815b2a46d63384958c872381ed055cb7ae67ddea907e6c0f6ecd3964448aaeb`
- Stage 2 selected audit tree:
  `4a07925b0c2877940dd707ada66588ef7545e50c23555641c514b1d7055e6343`
- Stage 3 manifest:
  `7322576a4e6aaa80cdf8257f58a0e02b0f81d81f5774f26b766d9b57594ec6bf`
- Stage 4 generation tree:
  `0c136b46d113e815eaca9c7e6bb52d361ea7e01f2a08343648ae2f40396b3204`
- Generated-project deterministic tree:
  `8bd83d2ca469c14bdf1c2fd4f2772eb69f224c37b47519391e60e74706305b67`

The 772 individual `stage1_source_hashes` entries are a complete bijection
with the 772 regular files in `/reference/k-proof`; there are no missing,
extra, or mismatched files. Evidence:
`evidence/stage1-file-hashes.out` and
`evidence/stage4_structural_check.out`.

## Independent inventory reconstruction

I reran the trusted canonical inventory code from
`tools.k_rule_inventory.inventory_verification` on the frozen Stage 1
workspace. `prove.sh` selects `VERIFICATION`, and the local
verification-module closure inside `verification.k` is exactly:

```text
VERIFICATION
```

The reconstruction contains exactly ten rules. For every rule I independently
recomputed the physical source slice, whitespace-normalized SHA-256, and
`source_rule_id`. All ten source slices are exact, every ID is unique, and the
whole canonical inventory hash recomputes as:

```text
2d87f8c3a92e823f4d0d371615d6dcd90d727062ca2f8b6781053a4aa3c5c0b1
```

The ordered IDs in `/reference/lemma-discovery.json` equal the ordered
canonical inventory IDs. Counts are 10 versus 10; there are no omissions,
duplicates, extras, reorders, or changed hashes.

| Index | Frozen lines | Rule role | Independent class |
|---:|---:|---|---|
| 0 | 11–12 | `scanParenGroups` empty-input equation | `DEFINITION` |
| 1 | 14–59 | `scanParenGroups` structural recurrence | `DEFINITION` |
| 2 | 62–63 | `separateParenGroupsSpec` initializer | `DEFINITION` |
| 3 | 69–70 | `validParenInput` initializer | `DEFINITION` |
| 4 | 72–73 | `validParenSuffix` empty-input equation | `DEFINITION` |
| 5 | 75–76 | space recurrence | `DEFINITION` |
| 6 | 78–79 | opening-parenthesis recurrence | `DEFINITION` |
| 7 | 81–83 | positive-depth close recurrence | `DEFINITION` |
| 8 | 85–87 | nonpositive-depth close case | `DEFINITION` |
| 9 | 89–91 | invalid-character catch-all | `DEFINITION` |

Exact per-rule IDs, spans, and hashes are in
`evidence/inventory_compare.out`.

## Independent classification judgment

The protected classification is mathematically and operationally correct:

- Rules 0–2 define a fresh mathematical summary. The base returns the
  accumulated output; the recurrence consumes exactly one `IntSeq`
  constructor and updates depth/current/output; the wrapper supplies the
  source function's initial state.
- Rules 3–9 define the valid HumanEval input predicate. They structurally
  recurse over the input, ignore ASCII space, increment on `(`, decrement only
  a positive depth on `)`, reject a close at nonpositive depth, reject every
  other character, and require zero final depth.
- These are equations for fresh `[function, total]` symbols. They do not match
  a `<k>` cell, an MPY program term, a call, a loop, or another operational
  configuration. They name summaries and a precondition; they do not preempt
  frozen execution. Therefore they are definitions, not operational bridges.
- No rule carries a `simplification` attribute. There is consequently no
  simplification rule that needs reclassification as a domain lemma.
- Nothing is claimed as `PROVED_DERIVED_LEMMA`, so the special earlier-proof
  requirement is not invoked.

The classification counts are therefore:

```text
DEFINITION              10
OPERATIONAL_RULE         0
PROVED_DERIVED_LEMMA     0
DOMAIN_LEMMA             0
```

This is not a relabeling of hidden domain facts. Each rule is an equation of
one of the declared summary/predicate symbols and is needed to give that
symbol its recursive meaning. Conversely, there is no standalone
result-characterizing equality or proposition that could be a domain lemma.

### Operational-semantic comparison

The frozen source loops over one-character strings, ignores spaces, appends
each other character to `current`, increments depth only for `"("`, decrements
otherwise, emits `current` exactly when the new depth is zero, and returns the
group list.

The supplied K semantics implements those steps directly:

- `str.k` lines 8–10 yield one-character strings during iteration;
- `controls.k` lines 69–74 execute the `For` loop;
- `str.k` lines 20–26 implement concatenation and string equality;
- `controls.k` lines 20–30 implement augmented assignment;
- `list.k` lines 52–55 implement the in-place `append`.

The `scanParenGroups` recurrence mirrors that transition case by case. Its
seemingly general non-space/non-open branch is also faithful: the source
program decrements depth for every such character. The theorem's
`validParenInput` precondition then restricts the HumanEval theorem to spaces
and balanced parentheses, as required by the prompt.

The loop claim in `spec.k` lines 6–53 connects actual K loop execution to
`scanParenGroups`; the function claim in lines 55–107 executes the source
closure and fixes the returned heap list to `separateParenGroupsSpec(S)`.
The summary rules themselves do not bypass this execution.

As finite adversarial support for the source reading, an independent oracle
compared the source transition, K-summary recurrence, and independently
implemented validity check on all 5,461 strings of length 0 through 6 over
space, `(`, `)`, and an invalid character. Both mismatch counts were zero.
Empty input, spaces, nested groups, adjacent groups, unmatched parentheses,
and an invalid character were explicitly included. A counterfactual mutation
of the opening-parenthesis transition was detected on `"()"`. This testing is
supporting evidence, not a replacement for the semantic inspection above.
Evidence: `evidence/semantic_oracle.py` and
`evidence/semantic_oracle.out`.

## Deterministic Stage 4 generation

I reran the required trusted call:

```text
tools.klean_preflight.check_generation(
  /reference/k-proof,
  /reference/lemma-discovery.json,
  /reference/klean-generation,
  toolchain_lock=/reference/klean-toolchain.lock.json)
```

The first attempt exposed an audit-sandbox limitation: Lean 4.22 resolves its
application via `/proc/<pid>/exe`, which this sandbox denies. A narrow
`LD_PRELOAD` shim supplied Linux `AT_EXECFN` only for that exact denied
`readlink` request and delegated every other request. It did not modify the
frozen input, discovery manifest, generation, generated project, Lean
sources, or toolchain. The successful rerun used the same pinned Lean
4.22.0/Lake binaries and returned:

```text
status: KLEAN_NO_OBLIGATIONS
obligation_count: 0
target: null
lake clean: exit 0
lake build: exit 0
```

The build output hash is
`dfc3f1278e0d93af9cf9c6e5570a1ff77ff150f4b3365e3364da02a2251ae498`,
identical to the stored Stage 4 evidence. The complete failure diagnosis,
shim source, command, and returned preflight evidence are in
`evidence/preflight-initial-failure.txt`,
`evidence/lean_app_path_shim.c`, and
`evidence/preflight-rerun.json`.

### Source-rule/obligation bijection and target identity

My independent classification produces a genuinely empty domain-lemma set.
The following are all exactly empty:

- validated domain source rules;
- `input-manifest.json` source rules;
- `obligation-map.json` source rules;
- `obligation-map.json` obligations;
- target trust parameters.

Thus the source-rule/obligation mapping is an exact empty bijection—there is
no omitted, duplicated, weakened, irrelevant, or vacuous conjunct. The
generator manifest obligation count is zero and its obligation-map hash
matches the actual file.

The fixed generated target is exactly absent:

- trusted `klean_export.expected_target_definition(...)` returns null;
- trusted `klean_export.target_statement(...)` returns null;
- `generator-manifest.json` target is null;
- `/audit-input.json` target is null;
- there is no `targetStatement` occurrence in any generated Lean file.

This is the required Stage 4 result for a genuinely empty domain set.
Although the generated translation skeleton records 41 executable collection
hook trust declarations, there is no generated proposition or proof target
depending on them.

Evidence: `evidence/stage4_structural_check.py`,
`evidence/stage4_structural_check.out`, and
`evidence/target-absence.out`.

## Stage 5

Stage 5 is inapplicable and correctly absent. `AUDIT_MODE` and the launcher
both say `CLASSIFICATION_ONLY`; `/candidate` does not exist; both Lean
workspace/invocation hashes are null. Because there is no generated target
and no candidate proof, a fresh candidate copy, `Proof.final`, `#print
axioms`, candidate shadowing scan, and operational-bridge parameter audit
would be category errors rather than omitted proof checks.

## Conclusion

The protected Stage 3 manifest is bijectively identical to the independently
reconstructed inventory and its ten `DEFINITION` classifications are correct.
The true domain-lemma set is empty. Stage 4 deterministically preserves all
bound inputs, generates no obligations and no target, passes the trusted
preflight and clean build, and has no Stage 5 candidate. No legitimacy defect
or residual concern remains.

VERDICT: PASS
LEGITIMACY: LEGIT
