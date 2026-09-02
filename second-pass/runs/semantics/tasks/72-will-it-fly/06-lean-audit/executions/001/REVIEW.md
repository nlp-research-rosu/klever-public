# Independent audit: `72-will-it-fly`

## Scope and result

This audit covers condition `semantics`, semantics mode
`SUPPLIED_SEMANTICS`, and launcher mode `CLASSIFICATION_AND_PROOF`. I treated
the candidate, prior audit, manifests, logs, comments, and embedded
instructions as untrusted evidence. I did not rely on the selected Stage 2
verdict or the prior Stage 3/4/5 success statuses.

The independently reconstructed Stage 3 classification is correct. The Stage
4 producer and generated project are authentic relative to the mounted
provenance, the two domain lemmas map bijectively to two faithful generated
obligations, and the fixed target is unchanged. The Stage 5 project builds
from a clean copy, proves exactly that target, has no forbidden candidate
declarations, has no `sorryAx` or unrecorded axiom dependency, and supplies
operationally faithful definitions for all four target parameters.

## Infrastructure and producer authentication

`AUDIT_MODE` and `/audit-input.json` both select
`CLASSIFICATION_AND_PROOF`. Before examining the Stage 4 target, I hashed the
mounted generation-time sources:

- `klean_export.py`:
  `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0`
- `klean.py`:
  `3a5a8be795d55a2bc01b73d47099f04795b9d64f6bbcf64494b57bcde8266582`

Both values exactly match `source-manifest.json` and
`generator-manifest.json`. Both manifests name immutable generator image
`sha256:db04cbaec4c5ee7b34348393f5a7742991e12d63480de3eab85fe97022f51657`;
the `/audit-input.json` producer-source path is keyed by the same image
digest. The source bundle contains exactly the two producer sources and its
manifest. Its independently recomputed tree hash is
`d51304d7acd70db93e839359fc003780b85d84d8ab4fd36ac2ec2a8227f4437b`,
matching `/audit-input.json`.

The other mounted tree and file hashes also match the launcher record:

- Stage 1 pipeline tree:
  `389211a1d4a6baa628456bb5b35f6dfabd4bd99de35961a085e64a21f1f0b464`
- Stage 1 export tree:
  `ccf8a76c67a6c8fba16907135fb024c44426cfd2810e87c4976d3ecbe6b95898`
- selected Stage 2 tree:
  `36e24bd6f5321c8f0df6e0229108c0cdb328cd1eed4ca6a719f1cd480aed390c`
- Stage 3 discovery file:
  `3f3378fa7b934bfd3743a4d9e5b456f09f8b7203d384bc38ee9162cb3b6e67ee`
- Stage 4 generation tree:
  `b3693594977c1dd720f08e9b0f253949311744ff5c37bd9d68abaa3fcd7b9396`
- generated project export tree:
  `db65aac49230bc1a315a0dd7534bb22e9583ec10463a445df4d720415372908f`
- candidate pipeline tree:
  `a8b9af024ce539a20b6ea3e4273cad4f068818e2c0cf2f83e3091933305e891b`

All 34 per-file Stage 1 hashes recorded in `/audit-input.json` were
recomputed with zero mismatches. The launcher-only Lean invocation is not a
mounted audit input, so its standalone tree cannot be rehashed here; the
mounted successful candidate workspace does match the recorded
`lean_workspace_sha256`. The trusted final gate also verified the signed
resolved-input digest
`af759ff53a52c889de319b84876737896822be3eed9e377a81f265da8ac745b7`.

Raw provenance and hash evidence is in
[`01_producer_provenance_raw.txt`](evidence/01_producer_provenance_raw.txt),
[`05_generation_source_manifest.txt`](evidence/05_generation_source_manifest.txt),
[`08_recomputed_tree_hashes.txt`](evidence/08_recomputed_tree_hashes.txt), and
[`46_independent_stage4_integrity_check.txt`](evidence/46_independent_stage4_integrity_check.txt).

## Stage 1 inventory reconstruction

I invoked the trusted `tools.k_rule_inventory.inventory_verification` on
`/reference/k-proof`, not on a prior audit's reconstructed data. `prove.sh`
selects `VERIFICATION`; its local verification-module closure contains only
that module. The canonical lexer found 14 rules in source order.

The frozen `verification.k` SHA-256 is
`fd1a4998485c613a031f9c9fb662704bba9cf0f285ebe1756f1fd6485ead7456`.
The recomputed canonical inventory hash is
`4d62e14326c0002105dc37206ba1963e972744781bf39d9a44f71ba3710b49c8`.
Both match the Stage 3 and Stage 4 records.

The comparison with `/reference/lemma-discovery.json` is bijective:

- inventory count: 14;
- discovery count: 14;
- no duplicate inventory or discovery IDs;
- no omitted IDs;
- no extra IDs;
- identical source order; and
- identical whole-inventory hash.

For every rule, the reconstruction recomputed its exact source span, text,
attributes, normalized source hash, and `source_rule_id`. The complete
machine-produced inventory is
[`12_reconstructed_inventory.json`](evidence/12_reconstructed_inventory.json);
the numbered frozen source is
[`13_verification_numbered.txt`](evidence/13_verification_numbered.txt); and
the explicit bijection result is
[`19_inventory_bijection_check.txt`](evidence/19_inventory_bijection_check.txt).

## Independent Stage 3 classification

I classified each entry from the frozen source and supplied operational
semantics:

| Frozen lines | Source rule ID | Independent class | Judgment |
|---|---|---|---|
| 8 | `rule-8277b118773512287e2b2b20da4dbf45607f85956623bafa9028b50596471d08` | `DEFINITION` | Empty-sequence base equation for `allInts`. |
| 9 | `rule-eb01b6f961218a9e5b8ece457a30b8c7cb8b55db7fb423d286186ba232f0aee3` | `DEFINITION` | Recursive integer-head equation for `allInts`. |
| 10–11 | `rule-571c5f5e487d813d7b511f60c911baa33380f2fcf106096134e0fb29fc85d948` | `DEFINITION` | Guarded non-integer case completing `allInts`. |
| 14 | `rule-54f4fd6c0759f5812a98a0df3c492a4d51892178432203d348728bb8e63486e0` | `DEFINITION` | Empty-sequence base equation for `sumIntVS`. |
| 15 | `rule-01e541a4f9625d93fed0c3da05caebc4267a821c55a48bd0f7d61899668ac08e` | `DEFINITION` | Recursive integer-sum equation. |
| 18 | `rule-becebddf142d7576a24cbe9dcc443d2914a5940ec4d344d1d179d0b17c2a8678` | `DEFINITION` | Empty-sequence base equation for `snocVS`. |
| 19–20 | `rule-a074558c6e6502d0ec637dab6d4ea3994203ef7eb07051486fef343a035c7b87` | `DEFINITION` | Structural recursive equation for `snocVS`. |
| 23 | `rule-76a248ec07038f0b4c6f37cc00b5e46a9544ae63d67acabfff3b08b42a437b4b` | `DEFINITION` | Empty-sequence base equation for `reverseVS`. |
| 24–25 | `rule-9a75b2367381745f16c1f23a52089299f9499ad0db56963f0de65e1b64ebaa84` | `DEFINITION` | Recursive reverse-through-snoc equation. |
| 30–32 | `rule-e8f739bf08317e883904eb65ce494f7a330c76031451acc8eea4e8073068f5e0` | `DOMAIN_LEMMA` | A proof shortcut for an existing supplied-semantics operation, not a definition or ordinary operational rule. |
| 34–36 | `rule-8c6fd5f43e6635bfa3e7668c921b0d8e3f46d6d1de6484989e3107ed21ffcc0c` | `DOMAIN_LEMMA` | A guarded whole-fold execution summary, not a definition or ordinary operational rule. |
| 39–49 | `rule-9b2c1d264a632bcb734a63c5c5afe47ce7c30f39f5fc22d0d5a730429dbd4197` | `DEFINITION` | Named proof-term expansion of the translated return expression. |
| 54–59 | `rule-124492e1edcf40a69e84f00bd5d3958b537e8531fa1d682cd6d327c1eceee41b` | `DEFINITION` | Named proof-term expansion of the translated module. |
| 62–63 | `rule-e9e6a90f2fb93ce00eb4643ca482c47f4a472b52cb3b28f078a2d97923c4e7df` | `DEFINITION` | Named proof-term expansion of the loaded closure value. |

Thus the independent totals are 12 `DEFINITION`, zero
`OPERATIONAL_RULE`, zero `PROVED_DERIVED_LEMMA`, and two `DOMAIN_LEMMA`.
Stage 1 does not first prove either domain rule against a module lacking it;
both are installed in `verification.k` before the three main claims. The
protected classification correctly does not call either one a proved derived
lemma.

Neither domain lemma is irrelevant:

- the source computes `q == q[::-1]`, and every spec branch describes
  balance using `reverseVS`;
- the source computes `sum(q) <= w`, and the balanced branches use
  `sumIntVS`.

The reverse-slice lemma agrees with the supplied semantics. For step `-1`,
`slStep` is `-1`, an omitted lower bound becomes `len(VS)-1`, an omitted
upper bound becomes `-1`, and `buildVS` selects indices in descending order.
Induction on `VS` equates that sequence with the frozen
reverse-through-`snocVS` definition.

The sum lemma also agrees with the supplied semantics on its complete guard.
`allInts(VS)` restricts every head to the `Int` injection; `#iterNext`
consumes a list head, `intOf` returns that integer, and `#sumAcc` updates the
accumulator. Induction plus associativity of integer addition yields
`sumIntVS(VS)` from initial accumulator zero. No heap, environment, control,
or other state cell changes in this fold.

No inventory rule has a `simplification` attribute. The requirement that
every simplification be a `DEFINITION` or `DOMAIN_LEMMA` is therefore
satisfied vacuously. The two domain rules have only `priority(40)`.

The source program, claims, and relevant operational rules are recorded in
[`15_stage1_program_spec_proof.txt`](evidence/15_stage1_program_spec_proof.txt),
[`17_focused_operational_semantics.txt`](evidence/17_focused_operational_semantics.txt),
and
[`18_sum_iterator_core_semantics.txt`](evidence/18_sum_iterator_core_semantics.txt).

## Deterministic Stage 4 generation

I reran
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`,
`/reference/k-proof`, `/reference/lemma-discovery.json`,
`/reference/klean-generation`, and the pinned
`/reference/klean-toolchain.lock.json`.

The first invocation reached the isolated build and failed because of the
audit sandbox, not the artifacts: the sandbox unshares PIDs while exposing
the outer `/proc`, and Lean's `/proc/<getpid()>/exe` lookup therefore could
not locate itself. Evidence
[`21_rerun_check_generation.json`](evidence/21_rerun_check_generation.json)
and
[`36_proc_exe_diagnostic.txt`](evidence/36_proc_exe_diagnostic.txt)
show the failure and cause.

I resolved this without modifying any input by compiling a narrow
`LD_PRELOAD` shim under `/tmp/audit-work` that makes `getpid()` return the PID
represented by `/proc/self` only for Lean/Lake subprocesses. With the shim,
Lean reported version 4.22.0 and commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, exactly the lock and generator
manifest. The shim source, digest, and validation are in
[`42_getpid_shim_compile.txt`](evidence/42_getpid_shim_compile.txt) and
[`43_getpid_shim_validation.txt`](evidence/43_getpid_shim_validation.txt).

The rerun preflight then returned `PASS`:

- `lake clean`: exit 0;
- `lake build`: exit 0;
- generated tree:
  `db65aac49230bc1a315a0dd7534bb22e9583ec10463a445df4d720415372908f`;
- obligation count: 2;
- trust declaration count: 92;
- generated sorry count: 0.

The returned evidence is
[`44_rerun_check_generation_with_proc_shim.json`](evidence/44_rerun_check_generation_with_proc_shim.json).

I separately checked the obligation map:

- independently classified domain IDs:
  `e8f739…f5e0`, then `8c6fd5…cc0c`;
- `source_rules` IDs: the same two, in the same order;
- `obligations` IDs: the same two, in the same order;
- no duplicates, omissions, or extras;
- both source texts, spans, normalized hashes, inventory hashes, and
  discovery hashes match the reconstructed source;
- both `lean_conjunct_sha256` values recompute exactly.

The first conjunct is the full universal equation for
`doSlice(list(VS), noB, noB, someB(-1)) = list(reverseVS(VS))`. The second
quantifies every generated configuration cell, an arbitrary continuation,
and `VS`; it preserves every cell and continuation, retains the exact
`allInts(VS) = true` guard, and asks for a `Rewrites` path from
`#sumAcc(list(VS), 0)` to `sumIntVS(VS)`. Empty and integer-list witnesses
satisfy the guard, so this is not an unsatisfiable source precondition.

The generated `Rewrites` relation contains no constructor for either exact
domain lemma. The candidate's sum proof instead uses the supplied operational
constructors for `#sumAcc`, list `#iterNext`, `#iterDone`, `#sumCont`, and the
integer-yield step. This rules out a circular proof that simply reuses the
Stage 1 shortcut. See
[`70_rewrite_circularity_and_used_constructors.txt`](evidence/70_rewrite_circularity_and_used_constructors.txt).

The fixed generated target is:

- declaration: `Klean72WillItFly.Lemmas.targetStatement`;
- statement SHA-256:
  `aa4cd227696c13a48f7f21e890a0fe34ea82454b1a914b730bd6563e978aace1`;
- definition SHA-256:
  `6abfebf3761ad15e09d53ee2d2e4fc21e20b2277016ad605806e4100550d4cce`;
- obligation-map SHA-256:
  `9fa07b276249987e98169ad258fd6f5213fde3e13d8512b63c23dcd160710814`.

The target parsed from the generated source equals the target in
`generator-manifest.json`, the saved Stage 4 preflight, the rerun preflight,
and `/audit-input.json`. The generated target file remained byte-identical
after the Stage 5 build. The detailed comparison is
[`46_independent_stage4_integrity_check.txt`](evidence/46_independent_stage4_integrity_check.txt).

The selected Stage 4 status is `PASS`, not `KLEAN_NO_OBLIGATIONS`; the
independently classified domain set is genuinely nonempty with exactly two
members.

## Stage 5 clean build and proof identity

I created the fresh workspace
`/tmp/audit-work/stage5-audit.RaxEg2`, copied only the candidate project
sources into it, and copied the immutable generated project to `Base`. Before
building, `Base` had the expected generated-tree hash
`db65aac49230bc1a315a0dd7534bb22e9583ec10463a445df4d720415372908f`.

Required fresh commands:

- `lake clean`: exit 0, complete output in
  [`51_stage5_lake_clean_complete.txt`](evidence/51_stage5_lake_clean_complete.txt);
- `lake build`: exit 0, complete output in
  [`52_stage5_lake_build_complete.txt`](evidence/52_stage5_lake_build_complete.txt).

The candidate contains exactly one definition for each target parameter and
exactly one `theorem final`. Its normalized theorem type is byte-for-byte the
manifest's fixed statement. It does not declare or shadow
`Klean72WillItFly.Lemmas.targetStatement`. Candidate Lean sources contain no
`sorry`, `admit`, `unsafe`, `axiom`, or `opaque`. The original candidate tree
still matches `/audit-input.json`; `Base` still matches the generator after
the build. See
[`68_candidate_target_identity_and_forbidden_check.txt`](evidence/68_candidate_target_identity_and_forbidden_check.txt).

`Proof.final` proves the fixed target directly:

- the reverse-slice conjunct reduces from the faithful parameter definitions;
- the sum conjunct is proved by structural induction on `VS` through the
  supplied operational `Rewrites` constructors, with `Int.add_assoc`.

There is no duplicated or weakened theorem substituted for the target.

The independent trusted Stage 5 checker returned `PASS`, and the full
audit-input-bound final mechanical gate also returned `PASS` in
`CLASSIFICATION_AND_PROOF` mode. Those results are
[`58_trusted_stage5_proof_candidate_check.json`](evidence/58_trusted_stage5_proof_candidate_check.json)
and
[`69_full_audit_input_bound_mechanical_gate.json`](evidence/69_full_audit_input_bound_mechanical_gate.json).

## Axiom accounting

I ran:

`lake env lean AxiomAudit.lean`

The audit source first checks `Proof.final` at the exact manifest statement
and then runs `#print axioms Proof.final`. The exact output is
[`57_stage5_print_axioms_complete.txt`](evidence/57_stage5_print_axioms_complete.txt).

The result lists 44 dependencies:

- three permitted Lean core principles: `Classical.choice`, `propext`, and
  `Quot.sound`;
- 41 generated axioms, each present with the same name, declaration kind,
  source, line, and type in the 92-entry `trust-inventory.json` allowlist.

The broad generated dependencies arise from the generated function and
`Rewrites` declaration closure; they include, among others, the recorded
`buildVS`, `buildIS`, collection-hook, map, float, and string conversion trust
boundaries. There is no `sorryAx` and no dependency outside the allowlist.
Every used name and its reconciled inventory record is enumerated in
[`67_axiom_reconciliation.txt`](evidence/67_axiom_reconciliation.txt).

## Operational-bridge audit of target parameters

The target binds four KORE symbols. I located their unique candidate
definitions and compared them with the bound source IDs, frozen rules,
source solution, and supplied semantics.

1. `allInts`

   The candidate returns true for `.ValSeq`, recurses only through an
   `inj_SortInt` head, and returns false for every other head. This is exactly
   frozen lines 8–11 and the supplied `isInt` discrimination. It has true
   witnesses (empty and nonempty integer lists), so the sum obligation is not
   made vacuous.

2. `reverseVS`

   The candidate's private `snocVS` and public `reverseVS` have the exact
   empty and recursive equations at frozen lines 18–25. It is neither
   constant nor identity: the three-element mixed-sign witness
   `[3, -2, 7]` reduces to `[7, -2, 3]`.

3. `doSlice`

   On the bound full reverse-list slice, the candidate returns a list of the
   faithful `reverseVS`, which is exactly the independently checked meaning
   of supplied `slStart`, `slStop`, `slStep`, and `buildVS`. On other
   arguments it delegates to the generated supplied-semantics
   `doSlice` implementation; `getD noneV` totalizes only values for which the
   frozen partial function has no operational rule. Defined list, tuple, and
   string cases remain delegated to their generated operational equations.

4. `sumIntVS`

   Empty is zero and an integer head is added recursively, exactly frozen
   lines 14–15. The wildcard totalization is outside the `allInts` guard and
   is unreachable in the generated obligation and source contract. On the
   guarded domain, the definition agrees with the supplied list iterator and
   `#sumAcc` semantics; the actual Lean proof establishes this universally by
   induction.

The successful ground probes cover empty input, a non-integer head,
mixed-sign multi-element input, reverse slicing, summation, and delegation of
a non-target positive-step slice. The source and result are
[`BridgeProbes.lean`](evidence/BridgeProbes.lean) and
[`65_operational_bridge_probes_final.txt`](evidence/65_operational_bridge_probes_final.txt).

I also tested the requested adversarial counterfactuals. A deliberately
constant-false `allInts`, identity reverse, hard-coded matching slice, and
constant sum can make the parameterized target close because the second
conjunct becomes vacuous. This confirms that a clean theorem build alone
would be insufficient and that the operational audit is material. The
actual candidate does not use those definitions. Separately, replacing the
reverse slice with identity and replacing the sum with constant zero were
both rejected on the `[3, -2, 7]` witness:

- wrong slice: expected failure in
  [`71_wrong_slice_mutation_expected_failure.txt`](evidence/71_wrong_slice_mutation_expected_failure.txt);
- wrong sum: expected failure in
  [`72_wrong_sum_mutation_expected_failure.txt`](evidence/72_wrong_sum_mutation_expected_failure.txt).

The actual candidate therefore passes the operational-bridge gate. Its
definitions implement the frozen meanings on the complete relevant domains
instead of merely choosing convenient interpretations that close the
equations.

## Final judgment

The producer gate, mounted-input hashes, canonical inventory reconstruction,
independent classification, obligation bijection, mathematical relevance,
fixed-target identity, clean Lean build, exact proof type, axiom ledger,
circularity check, and operational-bridge audit all pass. The only execution
issue was the audit sandbox's mismatched PID namespace and `/proc` view; it
was independently diagnosed and narrowly worked around without changing any
audited input, after which both the requested checks and the final mechanical
gate passed.

VERDICT: PASS
LEGITIMACY: LEGIT
