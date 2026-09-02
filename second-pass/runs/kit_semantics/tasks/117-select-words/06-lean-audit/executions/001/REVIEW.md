# Independent Stage 3–5 audit: `117-select-words`

## Scope and decision

The launcher records:

- problem `117-select-words`;
- condition `kit-semantics`;
- semantics mode `SUPPLIED_SEMANTICS`; and
- audit mode `CLASSIFICATION_ONLY`.

I treated all mounted candidate/provenance text and prior verdicts as
untrusted evidence. I used the trusted inventory and preflight code under
`/reference/tools`, inspected the frozen source and supplied operational
semantics directly, and did not execute `solution.py` or any prior-review
script.

The result is a clean classification-only pass. The independently reconstructed
domain-lemma set is genuinely empty, Stage 4 contains no obligations or target,
and no Stage 5 project is present.

## Producer-source authentication

I authenticated the Stage 4 sources before judging generation:

| File | Observed SHA-256 | Expected in both manifests |
|---|---|---|
| `klean_export.py` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` | same |
| `klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` | same |

`generator-manifest.json` provenance and `source-manifest.json` both identify
the immutable image
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`.
The basename of the producer-source path recorded in `/audit-input.json` is
that image digest. The producer bundle contains exactly the two sources plus
`source-manifest.json`; its independently recomputed pipeline tree hash is
`388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`,
matching `/audit-input.json`.

There is therefore no producer-provenance `AUDIT_ERROR`. Full evidence is in
[01-producer-authentication.log](/audit-output/evidence/01-producer-authentication.log).

## Inventory reconstruction and bijection

Using `tools.k_rule_inventory.inventory_verification`, I reconstructed the
local module closure from the frozen `verification.k`, rather than adopting the
protected classification. The result is:

- verification file SHA-256:
  `744f6ac85a22b27f87c484c6d52075aab78ad4f272966ae61e701713b2b4d203`;
- selected module: `VERIFICATION`;
- local closure, in source order: `VERIFICATION-SYNTAX`, `VERIFICATION`;
- rule count: 22; and
- canonical whole-inventory SHA-256:
  `b8a651c082f47c4331d73fb06595968cd0537666f9d79a596a98bb456cea6f9e`.

For every rule, the trusted reconstruction recomputed the physical source span,
whitespace-normalized text SHA-256, and `source_rule_id` of the form
`rule-<normalized_sha256>`. The protected manifest has exactly 22 unique IDs in
the same order. Its ID set and sequence both equal the reconstructed set and
sequence, and its inventory hash equals the recomputed canonical hash. There
are no omissions, duplicates, extras, reordered identities, changed embedded
hashes, invalid spans, or unaccounted classifications. The complete source
text, spans, full hashes, IDs, manifest entries, and Boolean comparison results
are in [02-inventory-reconstruction.log](/audit-output/evidence/02-inventory-reconstruction.log).

## Independent classification

My per-rule result is:

| Inventory entries | Frozen spans | Independent class | Reason |
|---|---|---|---|
| 1–3 | 31–49, 51–59, 61–67 | `DEFINITION` | Nullary `[function,total]` names for the exact loop body, post-loop statements, and complete function-body AST. |
| 4–6 | 70–72, 73–75, 76–79 | `DEFINITION` | Exhaustive defining equations for final conditional emission by `flushSelected`. |
| 7 | 81–87 | `DEFINITION` | Defines `selectScan` as scan state followed by the final flush. |
| 8–13 | 90–92, 93–97, 98–102, 103–111, 115–122, 123–131 | `DEFINITION` | Base and recursive equations for the selected-word accumulator. |
| 14–16 | 135–136, 137–140, 141–144 | `DEFINITION` | Base/space/nonspace recurrence for the final current word. |
| 17–20 | 146–147, 148–151, 152–157, 158–163 | `DEFINITION` | Base/space/vowel/nonvowel recurrence for the final count. |
| 21–22 | 165–166, 167–169 | `DEFINITION` | Base/cons recurrence for the final loop character. |

Thus the exact independent counts are:

- `DEFINITION`: 22;
- `OPERATIONAL_RULE`: 0;
- `PROVED_DERIVED_LEMMA`: 0; and
- `DOMAIN_LEMMA`: 0.

This agrees entry-for-entry with `/reference/lemma-discovery.json`. All 19
rules marked `[simplification]` are definitions, satisfying the required
simplification policy. No rule needs the special two-phase
`PROVED_DERIVED_LEMMA` justification because that class is empty.

These are definitions rather than mislabeled domain lemmas: every summary rule
has a proof-local summary symbol at its left-hand head and gives a base case,
recurrence, or composition for that symbol. None states an independent
human-facing fact about a pre-existing term or directly assumes the desired
postcondition. They are also not ordinary execution rules: none of the summary
rules rewrites an MPY `<k>` configuration or preempts a supplied execution
step. The three AST rules are specifically named proof terms, which the stated
classification policy includes as definitions.

The exact independent row for every source ID is preserved in
[06-independent-classification.log](/audit-output/evidence/06-independent-classification.log).

## Mathematical and operational judgment

The definitions are relevant and match the frozen program and postcondition:

- `charLoopBody`, `afterCharLoop`, and `selectWordsBody` reproduce the source's
  initialization, single left-to-right loop, space branch, nonspace branch,
  append, final flush, and return. They are the bodies used by the loop and
  whole-program claims.
- Supplied string iteration yields one-character strings and the remaining
  suffix. Supplied `not in` on strings reduces to the negation of
  `strContains`, exactly matching the summary guards against
  `"aeiouAEIOU"`.
- Supplied string `+` uses `seqConcat`; supplied list `append` mutates the same
  heap list using `valSeqConcat`. Those are the constructors used in the
  recurrences.
- `scanAccum` appends only at spaces; `flushSelected` performs the post-loop
  emission. `wordAfter`, `countAfter`, and `charAfter` separately describe the
  three loop-local post-states required by the loop claim. `selectScan` combines
  the accumulated list with that final word/count state exactly as the source
  does.

The cases are exhaustive and disjoint: empty/cons; space/nonspace;
equal/unequal count; empty/nonempty word; and vowel/nonvowel. Every recursive
equation consumes one `iCons`, while `flushSelected` is nonrecursive and
`selectScan` expands once. There is no totality gap, contradictory overlap,
constant answer, identity shortcut, hard-coded example, or irrelevant
result-characterizing assertion.

As finite adversarial support for this static judgment, I compared the summary
state with a separately written direct loop transition over 109,200 combinations
of suffixes, natural counts, nonempty prior words, nonzero prior counts,
nonempty prior accumulators, and old loop-character values. There were zero
mismatches. Counterfactual mutations were distinguished by concrete witnesses:
`("a",0)` for incrementing vowels, `(" ",0)` for emitting empty words,
`("b",1)` for dropping the final flush, and `("b a",1)` for failing to reset
the count. This finite check supports but does not replace the rule-by-rule
semantic analysis. See [07-semantic-adversarial-check.log](/audit-output/evidence/07-semantic-adversarial-check.log) and the frozen semantic excerpts
[05c](/audit-output/evidence/05c-operational-loop-semantics.log),
[05d](/audit-output/evidence/05d-operational-string-semantics.log),
[05e](/audit-output/evidence/05e-operational-list-semantics.log), and
[05f](/audit-output/evidence/05f-operational-operator-semantics.log).

## Stage 4 hashes, bijection, and fixed target

I verified the launcher document's own resolved-input hash and all recorded
top-level artifact hashes with the appropriate trusted digest functions. I also
rehashed the exact set of 782 Stage 1 files: there are no missing files, extra
files, or per-file hash mismatches. Key independently observed hashes are:

| Artifact | Observed SHA-256 |
|---|---|
| resolved launcher input | `b41c1ddba5f0a6ffcb19303c1f94a94dd237adfe96e488b0dc132e1c6643c0e8` |
| Stage 1 pipeline tree | `96b156445ff2fa8747611ddda4e9ddb8c65102e1dc57c14235fac737cb8de1f2` |
| Stage 1 export tree | `3974774386643ca2a9c55a5d36352b827182f34c0153a3782f2fc4c84498c4cb` |
| protected Stage 3 manifest | `b32494cba4d2a64621622f2061728cbacd3b45a47ce6b26875283e6304decaf7` |
| selected Stage 4 pipeline tree | `4a9f831112dad61c030e248b0e02c93707afb96a91eecdacce8c6e102e0ee778` |
| generated project tree | `64266c11feb8978573668f6278e8beaecde9dad66c8ffac3014a775c3aa2597f` |
| obligation map | `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048` |
| trust inventory | `87d7e53baee699aa6461cf5be8b0583f9776f444fc5eaf9a8495f460a5bb89b6` |

The input manifest's 22 definitions are exactly the independently reconstructed
and classified rules. Its operational, proved-derived, and domain-source-rule
lists are all exactly empty. The authenticated producer selects only validated
`domain_lemmas` for trust obligations and enforces their ordered ID bijection.
Because the true domain set is empty, the exact Stage 4 mapping is:

```text
source_rules    = []
obligations     = []
trust_parameters = []
```

All three recorded obligation counts are zero. The selection, preflight, and
export statuses all say `KLEAN_NO_OBLIGATIONS`. The audit input, embedded
preflight, generator manifest, standalone preflight, and an independent scan
all report no target. `Lemmas.lean` contains no `targetStatement`; therefore
there is no omitted, duplicated, weakened, irrelevant, vacuous, or changed
conjunct and no generated theorem identity to mismatch. Evidence is in
[04-hashes-generation-bijection.log](/audit-output/evidence/04-hashes-generation-bijection.log),
[08a-generation-obligation-routing.log](/audit-output/evidence/08a-generation-obligation-routing.log),
[08b-generated-target-absence.log](/audit-output/evidence/08b-generated-target-absence.log), and
[08c-obligation-map.log](/audit-output/evidence/08c-obligation-map.log).

## Required preflight rerun

I called `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`
and the required Stage 1, Stage 3, and Stage 4 paths. The initial call exposed a
container-only procfs mismatch: Lean asks for `/proc/<namespace-pid>/exe`, while
this sandbox exposes `/proc/self/exe`. I preserved that failure. I then compiled
the documented 29-line compatibility shim
[proc_self_exe_fix.c](/audit-output/evidence/proc_self_exe_fix.c), which redirects
only that exact procfs lookup to `/proc/self/exe`; it does not alter any input,
project file, Lean declaration, or compiler result.

With the shim, the unchanged pinned tools reported Lean 4.22.0 commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05` and Lake 5.0.0. The required
preflight returned `KLEAN_NO_OBLIGATIONS`; its isolated `lake clean` and
`lake build` both exited 0. The clean output hash is the empty SHA-256 and the
build output hash is
`52b3d1c0727f3e10597bc9827134f33a4e706d1d17f968721d115b6a85c4c39a`,
exactly matching the generation-time and launcher-recorded diagnostics. The
complete returned evidence is [03-preflight-rerun.log](/audit-output/evidence/03-preflight-rerun.log); the resolved setup issue is preserved in
[03a](/audit-output/evidence/03a-preflight-initial-procfs-failure.log) and
[03b](/audit-output/evidence/03b-lean-procfs-workaround.log).

## Stage 5 applicability

Stage 5 proof auditing is not applicable. `AUDIT_MODE` and the launcher both
say `CLASSIFICATION_ONLY`; the launcher has null Lean workspace, invocation,
result, and target fields; `/candidate` does not exist. This is exactly the
required state for a genuine `KLEAN_NO_OBLIGATIONS` generation. Accordingly,
there is no `Base` copy, `Proof.final`, axiom printout, or operational parameter
bridge to audit. Attempting to manufacture any of those would introduce a
target or candidate forbidden by this mode.

The raw command/result index is [COMMANDS.md](/audit-output/evidence/COMMANDS.md).

VERDICT: PASS
LEGITIMACY: LEGIT
