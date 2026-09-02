# Independent audit: 56-correct-bracketing

## Scope and result

The launcher environment and `/audit-input.json` both select
`CLASSIFICATION_ONLY` for condition `semantics` in
`SUPPLIED_SEMANTICS` mode. `/candidate` is absent, as required in this mode.
I treated the mounted Stage 1–4 artifacts and the prior Stage 2 review only as
untrusted evidence and did not rely on any prior verdict or classification.

The protected Stage 3 classification is correct. The independently reconstructed
domain-lemma set is genuinely empty, so the deterministic Stage 4 status
`KLEAN_NO_OBLIGATIONS`, the empty obligation map, and the absence of a generated
target are legitimate. Stage 5 proof checks are not applicable.

## Producer provenance and frozen inputs

I hashed the generation-time producer files before judging Stage 4:

| Producer | Recomputed SHA-256 |
|---|---|
| `klean_export.py` | `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0` |
| `klean.py` | `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1` |

Both hashes match `generator-manifest.json` and
`generation-tools/source-manifest.json`. The immutable generator image identity
is consistently
`sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000`
in the generator manifest, source manifest, and the basename of the
launcher-recorded producer-source path. The producer bundle has exactly the two
producer files plus `source-manifest.json`; its recomputed pipeline tree hash
`55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c`
matches `/audit-input.json`.

All other recorded hashes were independently recomputed with the hash algorithm
appropriate to each manifest field:

- the 34 Stage 1 regular-file paths and every individual file hash match
  `stage1_source_hashes`;
- Stage 1 pipeline tree:
  `23d82f7a5769ddf7e1ad2b000cb8be1ec02c86cdf836610606cde655ab117709`;
- Stage 1 exporter tree:
  `4ad16265916e0054592f6fc9e289f75814ca2d7f8b41a0e94137a772cf160cca`;
- selected Stage 2 tree:
  `7db16703362dfccf49bb2ce9c42ce154f7c78781e8697448f57b0d7c086609f4`;
- Stage 3 manifest:
  `890ca00b94e4ffa18d45c55106a3417f24afd15c52d29cf0b56de9ea31d4a5b9`;
- whole Stage 4 generation:
  `49cfd6832290049941bf396606cb937000ee32697a38fb0f69bf1628b160682c`;
- generated project:
  `683720fe2d55e43759ccd443a2d34295fa81faad85417f7c4fe7d2c6e55bd6f3`;
- obligation map:
  `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`;
- trust inventory:
  `6b4bb48e9707e8f7938d9b87fc3af2c7046dd15e3d9f42a523a7addc178b332d`.

Every comparison is recorded as true in
`evidence/04b_recomputed_integrity_pipeline_hashes.txt`.

## Inventory reconstruction and bijection

I ran the trusted `tools.k_rule_inventory.inventory_verification` directly on
the frozen `/reference/k-proof`. `prove.sh` selects `VERIFICATION`; the local
verification-module closure contains only that module. The reconstruction found
17 rules in source order and reproduced:

- `verification.k` SHA-256
  `230cb99f6a534326556beb6f1ef2385752e56d1544b6e67d8d5f67022e6f7281`;
- inventory SHA-256
  `e3f58226e37acb7e0c5b36cb997d22117d54afe906492f0de33c894ec694a1e6`.

For every entry, I recomputed the exact source span, whitespace-normalized rule
text hash, and `source_rule_id = "rule-" + normalized_sha256`. The protected
manifest has exactly the same 17 identities in exactly the same order. The IDs
are unique; there are no omitted, duplicated, extra, or reordered identities.
The Stage 4 input-manifest partitions are also a bijection over the same
canonical records, with identical spans, attributes, normalized hashes, and
texts. The complete reconstructed records are in
`evidence/02_reconstructed_rule_inventory.txt`, and the explicit ordered checks
are in `evidence/10_inventory_bijection.txt`.

## Independent classification

### Definitions

The eight rules at `verification.k` lines 12–35 all define the newly named
`bracketResult(IntSeq, Int)` summary:

| Lines | Meaning |
|---|---|
| 12 | empty suffix at depth zero is true |
| 13–15 | empty suffix at positive depth is false |
| 16–18 | empty suffix at negative depth is false |
| 20–22 | an opening bracket at depth zero consumes the character and starts depth one |
| 23–25 | a non-opening character at depth zero fails |
| 27–29 | an opening bracket at positive depth increments the depth |
| 30–32 | a non-opening character at positive depth decrements the depth |
| 33–35 | negative depth is absorbing false |

These are exhaustive, guarded, pairwise compatible recurrence equations for a
named proof summary, so `DEFINITION` is the correct classification. All five
rules bearing `simplification` are in this group; none is labeled operational
or derived.

The recurrence matches the frozen program, not merely the prompt examples. Both
start at depth zero, increment on `"<"`, decrement on every other character,
reject immediately when the depth becomes negative, and otherwise return
whether the final depth is zero. Induction on the remaining string establishes
the connection. The prompt restricts inputs to `"<"` and `">"`; treating any
other character as closing additionally agrees with the frozen source's `else`
branch. As finite secondary evidence, an independent implementation comparison
checked all 9,841 strings of lengths 0–8 over `<>x` with zero mismatches. Mutating
early-negative rejection, the opening action, or the final zero test produced
distinguishing witnesses.

### Operational rules

The nine rules at lines 41–168 are ordinary execution or observation
macro-steps, not mathematical domain facts:

| Lines | Fixed-semantics operation represented |
|---|---|
| 41–43 | evaluate a Boolean literal and execute `Return(Val)` |
| 45–59 | look up integer `depth`, evaluate `depth == 0`, and return it |
| 61–76 | look up the one-character `bracket`, compare it with `"<"`, and select the true branch |
| 78–93 | the corresponding unequal-character observation and false branch |
| 95–106 | execute integer `depth += 1` in the pinned plain local scope |
| 108–119 | execute integer `depth -= 1` in that scope |
| 121–136 | observe `depth < 0` and select the true branch |
| 138–153 | observe nonnegative depth and select the false branch |
| 159–168 | execute frame pop and normalize deletion of the fresh callee scope |

I compared these rules directly with the supplied operational semantics:

- `core.k` supplies literal evaluation and name lookup;
- `operators.k`, `int.k`, and `str.k` supply comparison/arithmetic dispatch;
- `controls.k` supplies `AugAssign`, `If`, and `#branch`;
- `functions.k` supplies `Return` and `#pop`.

The comparison preserves the accepted contexts and effects. The return
macro-steps discard the continuation exactly as the fixed `Return(V) ~> _`
rule does. Branch and assignment rules preserve the arbitrary continuation and
frame all unrelated cells. Their scope pattern pins plain integer/string
bindings, so cell-reference or alternate-binding behavior is not silently
skipped. The pop rule restores the continuation, caller environment, stack,
return state, and scope location exactly as the fixed rule does; its freshness
guard `notBool L in_keys(SC)` is precisely what makes
`(L |-> frame SC)[L <- undef]` normalize to `SC`.

Thus these rules accelerate concrete execution/observation without asserting an
independent property of brackets. `OPERATIONAL_RULE` is the correct
classification for all nine.

There is no `PROVED_DERIVED_LEMMA`: Stage 1 does not first prove any of these
exact rules in a module that excludes it and then import it for a later proof.
There is also no `DOMAIN_LEMMA`: no inventory rule states a standalone
mathematical fact beyond defining `bracketResult` or performing/observing the
frozen execution. The independently reconstructed counts are therefore:

| Classification | Count |
|---|---:|
| `DEFINITION` | 8 |
| `OPERATIONAL_RULE` | 9 |
| `PROVED_DERIVED_LEMMA` | 0 |
| `DOMAIN_LEMMA` | 0 |

## Deterministic Stage 4 generation

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`
against the required frozen workspace, Stage 3 manifest, Stage 4 generation,
and trusted toolchain lock.

The audit sandbox exposes `/proc/self/exe` but not Lean 4.22's attempted
`/proc/<numeric-pid>/exe` lookup. The first run reached the clean-build phase
and recorded that infrastructure error. I then used the narrow
`evidence/lean_proc_exe_shim.c` preload shim, which redirects only that
executable-path lookup to `/proc/self/exe`; it does not alter Lean, Lake, the
project, or any audited input. With that sandbox compatibility measure, the
same trusted function returned:

- status `KLEAN_NO_OBLIGATIONS`;
- `lake clean`: exit 0, empty-output SHA-256
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`;
- `lake build`: exit 0, output SHA-256
  `9e2445c8d255d1f3672b2829e80a343ada636ab98ed2f53d2ea13b9eb0131399`;
- obligation count 0;
- target `null`;
- 47 trust declarations and zero designated sorries.

The returned hashes and build diagnostics exactly equal the launcher-recorded
preflight. The trusted function also resnapshotted all immutable inputs after
the build. Its exact output is in
`evidence/06b_fresh_check_generation_with_sandbox_shim.txt`.

I separately inspected the source/obligation mapping. The input manifest's
domain `source_rules` list is empty. `generated/obligation-map.json` has empty
`source_rules`, `obligations`, and `trust_parameters` arrays. Obligation count
is zero in the generator manifest, export result, preflight, and audit input.
The generator manifest, preflight, and audit input all fix the target to
`null`; `Lemmas.lean` contains only an empty namespace and there is no generated
target declaration. This is an empty-to-empty bijection, not a weakened theorem
or a vacuous `True` conjunct. There are no omitted, duplicate, irrelevant, or
weakened obligations because the independently valid domain-lemma set is empty.

## Optional Stage 5

This is not `CLASSIFICATION_AND_PROOF`. `/audit-input.json` records no Lean
invocation or Lean workspace, the fixed target is absent, and `/candidate` is
absent. Consequently a `Base` copy, candidate clean build, `Proof.final`,
`#print axioms`, target-shadowing review, and operational-bridge parameter
checks are correctly inapplicable. Their absence is consistent with the
legitimate `KLEAN_NO_OBLIGATIONS` result.

## Evidence index

Exact commands are indexed in `evidence/COMMANDS.md`. Raw outputs, including
the preserved initial environment diagnostics and the authoritative successful
reruns, are under `evidence/`.

VERDICT: PASS
LEGITIMACY: LEGIT
