# Independent Stage 3–4 audit: `25-factorize`

## Result and scope

The protected classification and deterministic generation are legitimate. The
launcher envelope, `AUDIT_MODE`, and mounted artifacts all record
`CLASSIFICATION_ONLY` with `SUPPLIED_SEMANTICS`. The independently reconstructed
domain-lemma set is genuinely empty, Stage 4 has no generated target, and
`/candidate` is absent. Stage 5 proof, axiom, and operational-parameter checks
therefore do not apply.

This judgment does not rely on the Stage 1 report, the selected Stage 2 review,
or any prior classification rationale. Candidate and provenance text was
treated as evidence only.

## Input and producer integrity

The signed Stage 6 envelope validates with resolved-input digest
`aba2c27fdeda422cd68f72ed983761fe5576b4b6ecc5e40f3d4cfbba5783d01b`.
`/audit-input.json` and its mounted output copy are byte-identical. Every
resolution-level hash recomputed with the trusted hash implementations matches:

- Stage 1 workspace tree:
  `5a6500781bf3a49ff0fd5851b76d3a9f01ac614a940b0fc7151e040bcbd5f91c`;
- Stage 1 deterministic-export tree:
  `bdb76124cb0bda5c889913bc731fb3ec8a89a6325ca736789899174a0a639388`;
- Stage 2 selected audit tree:
  `72ecc2079957f0a1bbdb418b90f56c94e343505d7649304c074729de9d107991`;
- Stage 3 manifest:
  `6218a22c255cda1ddc70a66ea699ed5682143e8b44dba473bff1ea1a45dd789a`;
- Stage 4 selected-generation tree:
  `9b9110d254903e51c894c1063e2415f725c3dad582863fd5caada72aa1da2def`;
- generated-project tree:
  `60a68b92c85377e1d0e3b43c2dce8ba0d61f3fad974ea05d5ed36e8efbf92a36`;
- producer-source bundle:
  `94ba4c012f48b7135094fefcc4517f5c9a5c1052fc304449c5505ddb4dca91b4`.

All 769 recorded Stage 1 per-file hashes were present and equal, with no
unrecorded file. Both selected artifact hashes also equal their reconstructed
trees. Full comparisons are in
`evidence/hash_and_manifest_audit.log`.

The mandatory producer-source gate passes:

- `klean_export.py` hashes to
  `0e653377b007bc1a742bbd8fa0dcfdf956ebb2ef2432a7137d032b0a70d59c1b`;
- `klean.py` hashes to
  `0e6dba9d9f456574b3bf4f4bf06933d774e9125f4d12c5a90b7314d8dd5c33a4`.

Those values agree exactly with `generator-manifest.json` and
`source-manifest.json`. The bundle contains exactly those two sources plus its
source manifest. Both manifests record immutable generator image
`sha256:b377a4d6ce1a4210c17d7e862e3737d2c348cc4be96dfaca72ef9274846f4afc`,
and the same image key is the terminal component of the producer path signed
in `/audit-input.json`. There is no producer-source infrastructure error.

## Inventory reconstruction and bijection

I ran `tools.k_rule_inventory.inventory_verification` from the trusted
`/reference/tools` with `PYTHONPATH=/reference`. The selected local
verification-module closure is exactly `VERIFICATION`; its `MPY` import is
supplied by required external semantics files and introduces no additional
module local to `verification.k`.

The canonical inventory has exactly these three entries, in source order:

| Span | Recomputed normalized SHA-256 | Recomputed identity | Independent class |
|---|---|---|---|
| 10–11 | `dbfc0d4c3175b4500c8cf75aa233cec5e0c9c3cee743890140512a0182f4cafa` | `rule-dbfc0d4c3175b4500c8cf75aa233cec5e0c9c3cee743890140512a0182f4cafa` | `DEFINITION` |
| 13–18 | `a835c97bf031675f196bffdf44a60757b87fcba3d1c37ef34f793bef42ba0e65` | `rule-a835c97bf031675f196bffdf44a60757b87fcba3d1c37ef34f793bef42ba0e65` | `DEFINITION` |
| 20–22 | `5fab523961a49385350dd07993fa3e83246b724eb1f40138964ce039d42a8f55` | `rule-5fab523961a49385350dd07993fa3e83246b724eb1f40138964ce039d42a8f55` | `DEFINITION` |

For every entry, the independently selected source slice equals the inventory
text exactly, and `source_rule_id` is `rule-` followed by the independently
normalized source hash. The recomputed whole-inventory hash is
`e17602520f8ca9cac84016d69445f8528428a15c15c715a3633e69379a0d50a2`.

The protected Stage 3 manifest has exactly three unique identities, in that
same order, and the same whole-inventory hash. There are no omissions,
duplicates, extras, reordered entries, changed spans, or changed hashes.
Trusted `validate_trust_boundary` also passes. The raw reconstruction is in
`evidence/inventory_audit.log`.

## Independent classification judgment

`factorAcc` is declared as a pure `ValSeq` function of an accumulator, a
remaining integer, and a candidate divisor. None of its rules matches a
`<k>` cell, invocation, continuation, environment, heap, or other execution
configuration. The rules therefore do not execute or bypass the source
program.

Each rule is a genuine clause of one summary recurrence:

1. Lines 10–11 are the base equation. When `N < D`, it returns the accumulated
   sequence.
2. Lines 13–18 are the divisible step. It appends `D`, replaces `N` by the
   supplied-semantics floor quotient, and recurs with the same divisor.
3. Lines 20–22 are the non-divisible step. It preserves the accumulator and
   remainder and recurs at `D + 1`.

On every use in the frozen proof, `N >= 1` and `D >= 2`. The guards
`N < D`, `D <= N ∧ pyMod(N,D) = 0`, and
`D <= N ∧ pyMod(N,D) ≠ 0` are exhaustive and pairwise disjoint there, and
zero division is excluded. The divisible step strictly reduces positive `N`
when it fires; failed divisibility advances `D` toward the base case.

This recurrence matches the frozen source and operational semantics
constructor-for-constructor:

- a false `D <= N` while condition exits and returns the current list;
- list `append` mutates the list by
  `valSeqConcat(A, vCons(D, .ValSeq))`;
- integer `%` is `pyMod`;
- integer `//` is `(N - pyMod(N,D)) /Int D`;
- the two branches respectively preserve `D` or assign `D + 1`.

The relevant frozen source and supplied-semantics excerpts are preserved in
`evidence/operational_source_excerpts.log`; the exact claim contexts and
preconditions are in `evidence/formal_claim_excerpts.log`. An independently
implemented recurrence/source-loop comparison over `1..2000` plus prime,
prime-power, repeated-factor, square, and mixed-factor witnesses found zero
sequence mismatches and zero order/primality/product failures. That finite
check is supporting adversarial evidence, not the basis for the universal
classification; see `evidence/summary_semantics_check.log`.

No rule asserts primality, ordering, product equality, divisibility theory, or
another human-facing fact about an already defined result. Consequently none
is a `DOMAIN_LEMMA`. No rule is an ordinary execution/observation rule, so none
is an `OPERATIONAL_RULE`. No rule is first proved in a module omitting it and
later reused, so none is a `PROVED_DERIVED_LEMMA`. There are no explicit
`simplification` attributes; in any event, all three function equations have
the permitted `DEFINITION` classification.

The protected Stage 3 classification of three definitions and zero domain
lemmas is therefore mathematically correct and relevant to the source program
and its factorization result.

## Deterministic Stage 4 generation

The generation-time source shows that only validated `DOMAIN_LEMMA` entries
become source rules and Lean obligations. With the independently confirmed
empty domain set, all four structural collections are exactly empty:

- `input-manifest.json.source_rules`;
- `obligation-map.json.source_rules`;
- `obligation-map.json.obligations`;
- `obligation-map.json.trust_parameters`.

Thus the source-rule/obligation mapping is an exact empty-to-empty bijection,
not an omission. All manifests report obligation count `0`. There are no
conjuncts that could be irrelevant, weakened, duplicated, or vacuous.

The obligation-map file hashes to
`cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`,
matching the generator manifest. The trust inventory hashes to
`7a636fe731ed534d607dcc8aba84f913db242b636f0e144464868077ac54bbe6`,
matching the export result. The generator toolchain object equals the pinned
lock byte-for-value at the JSON level; the lock file itself hashes to
`a3dc0270ff7cab64550e91f605d8f2b5f6076b75f4ec49629a0e13894455fa9f`.
The verification, discovery, Stage 1 export, generated tree, and all sidecar
bindings also match.

For zero obligations, the fixed expected target is no target. Independent
`expected_target_definition` and `target_statement` calls both returned
`null`; the generator manifest and signed audit input also contain
`target: null`. A direct scan found no `targetStatement` declaration and no
`sorry`, `admit`, or `unsafe` token in generated Lean sources. Those scan
results are in `evidence/generated_target_scan.log`.

## Trusted preflight rerun

I directly invoked `tools.klean_preflight.check_generation` with:

```text
PYTHONPATH=/reference
input=/reference/k-proof
discovery_manifest=/reference/lemma-discovery.json
generation=/reference/klean-generation
toolchain_lock=/reference/klean-toolchain.lock.json
```

The first invocation exposed a sandbox compatibility issue: Lean 4.22 asks
procfs for `/proc/<numeric-pid>/exe`, while this managed audit sandbox exposes
only `/proc/self/exe`. The exact failure is retained in
`evidence/generation_preflight_rerun.log`. I compiled the narrow compatibility
shim in `evidence/proc_exe_compat.c`, which redirects only numeric
`/proc/<pid>/exe` `readlink` requests to `/proc/self/exe`, and reran the same
trusted function. It does not modify Lean source, the generated project, or
checker logic.

The rerun returned `KLEAN_NO_OBLIGATIONS`, obligation count `0`, target `null`,
and zero designated sorries. Its fresh-copy commands both succeeded:

- `lake clean`: exit `0`, empty-output SHA-256
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`;
- `lake build`: exit `0`, output SHA-256
  `e1f281f8580dcfb8d56d6e12cd47626784f6e863248a029b08a262ea28e48339`.

The build output hash exactly reproduces the recorded Stage 4 preflight. The
checker also reconciled all 44 generated non-propositional trust declarations
with `trust-inventory.json` and rejected proposition trust by policy. Its full
returned evidence is in `evidence/generation_preflight_rerun_compat.log`.
Post-preflight hashes remained unchanged, as recorded in
`evidence/post_preflight_integrity.log`.

## Stage 5 applicability and conclusion

`CLASSIFICATION_ONLY` is the correct launcher mode because the true domain set
is empty. There is no generated theorem to prove, no target parameter requiring
an operational bridge, and no Stage 5 candidate. Creating `Base`, building a
candidate, printing `Proof.final` axioms, or auditing candidate definitions
would fabricate a proof stage that the signed pipeline explicitly excludes.

The mechanical gates establish structural integrity; the independent
source-and-semantics analysis above establishes the material mathematical
judgment. Stage 3 has not mislabeled a domain theorem, and Stage 4 has neither
lost nor weakened an obligation.

VERDICT: PASS
LEGITIMACY: LEGIT
