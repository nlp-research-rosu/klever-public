# Independent audit: HumanEval 106-f

## Result

I independently audited Stage 3 classification, deterministic Stage 4
generation, and the Stage 5 Lean proof for condition `kit-semantics` and
semantics mode `SUPPLIED_SEMANTICS`.  The launcher-selected mode was
`CLASSIFICATION_AND_PROOF`.

The protected Stage 3 classification is complete and mathematically correct:
the 14-rule local `VERIFICATION` closure contains ten definitions and four
genuine, relevant domain lemmas.  Stage 4 maps those four domain lemmas
bijectively to four exact, non-vacuous Lean obligations.  The Stage 5
candidate defines every bridge symbol with its frozen operational meaning and
proves exactly the immutable generated target without a proof trust escape.

## Input and producer integrity

I treated all mounted candidate, provenance, comments, prior verdicts, and
logs as untrusted evidence.  I used the mounted trusted inventory, preflight,
hash-contract, and final-gate implementations to reconstruct facts from the
read-only artifacts.

Before judging generation, I obtained these direct producer hashes:

| Producer | SHA-256 |
|---|---|
| `klean_export.py` | `0e653377b007bc1a742bbd8fa0dcfdf956ebb2ef2432a7137d032b0a70d59c1b` |
| `klean.py` | `0e6dba9d9f456574b3bf4f4bf06933d774e9125f4d12c5a90b7314d8dd5c33a4` |

Both hashes match `source-manifest.json` and `generator-manifest.json`.
The producer tree hash
`94ba4c012f48b7135094fefcc4517f5c9a5c1052fc304449c5505ddb4dca91b4`
matches `/audit-input.json`.  The immutable generator image identity is
consistently
`sha256:b377a4d6ce1a4210c17d7e862e3737d2c348cc4be96dfaca72ef9274846f4afc`
in the source manifest, generator manifest, and the image-addressed producer
path recorded by the launcher.  The full selected generation tree hash is
`783403541f8c57f0abf31a215e48faafb8de94740cad34e4a9464d26ecf92661`;
the generated-project tree hash is
`c577390a99b798f99dcf83d67a4e155c27b9456a170f0e0218b82ad99c5a3719`.
All match their launcher records.

I also verified the launcher resolution digest, all eight hashes whose
artifacts are mounted, the exact 777-file Stage 1 source-hash map, both
selected-artifact hashes, and the cross-recorded Stage 4 and Stage 5
workspace hashes.  There are no missing, extra, or mismatched Stage 1 files.
The only top-level recorded artifact not independently rehashed is
`lean_invocation_sha256`, because the launcher did not mount the Stage 5
invocation/log directory; it mounted the successful Lean workspace instead,
whose tree and source hashes were verified.  No judgment relies on that
unmounted invocation hash.

Raw evidence:

- `evidence/06d_producer_and_input_hash_checks_correct_algorithms.txt`
- `evidence/22_all_mounted_recorded_hashes.txt`
- `evidence/00_context_and_producer_hashes.txt`
- `evidence/06_launcher_hash_algorithm_trace.txt`

The first provenance attempt used the wrong tree-hash algorithm and is
retained in `05b_producer_and_input_hash_checks.txt`; `06d` is the corrected
check using the exact launcher implementations.  This was an auditor-side
diagnostic error, not an input mismatch.

## Stage 3 inventory reconstruction

The frozen `verification.k` file hash is
`964869333598044f520042148fc3c3ae1123a75cb85dea3aac01dc7dc1efb56c`.
The trusted rule-inventory code reconstructed one local verification module,
`VERIFICATION`, with 14 rules.  For every rule I independently recomputed the
source span, normalized text hash, and `source_rule_id` (the ID is `rule-`
followed by that normalized SHA-256).  The whole reconstructed inventory hash
is
`ed9455742263e4ffcb296214aa731ac41511e0935ee388f6e3e45782ae9df00f`.

The following is the ordered reconstructed inventory and my independent
classification:

| Order | Lines | `source_rule_id` | Classification | Judgment |
|---:|---:|---|---|---|
| 1 | 10–12 | `rule-f6a44ca73f98b73343ed781fb0f5923f0dc5c4c49fe58cfd6e068a218cdac844` | `DEFINITION` | `factRun` guarded recursive step |
| 2 | 13–15 | `rule-bfbc5495b691995b569b051b9e1bcfc76d084f272d918a037d39536101cac940` | `DEFINITION` | `factRun` base result |
| 3 | 16–18 | `rule-ab7cbb359dda1a6c9c1a14fe5b45df7a4f54c5eced049f1d2c5066c92c667ec7` | `DOMAIN_LEMMA` | reverse `factRun` fold |
| 4 | 19–21 | `rule-7308a5851a2b284aa3dbac50d2f7cd50bcd709c1dae19c5ff89643a3db66b4ca` | `DEFINITION` | simplification copy of the base equation |
| 5 | 26–28 | `rule-23fa583cbda6e500fb140af409899711574cfb2e8e40900eea23dea425a03d7b` | `DEFINITION` | `totalRun` guarded recursive step |
| 6 | 29–31 | `rule-69dab32a72476eefefe5f091a5f3b750498f5f7ecd83eec93d6d4bec3291fb66` | `DEFINITION` | `totalRun` base result |
| 7 | 32–34 | `rule-5aa051dcb3d8aa1545bc998933e91b5adea53c25b6565ff7e8213e15b8ba1b66` | `DOMAIN_LEMMA` | reverse `totalRun` fold |
| 8 | 35–37 | `rule-5d22076434cc8e4e4becd2bff94c413dbbaf575f7a64d05a738a24a09858a97d` | `DEFINITION` | simplification copy of the base equation |
| 9 | 44–52 | `rule-69501e1c731d0f3c8e8c7fa0d5598996b25f29cb5ae72f5e94a27a0aaf916680` | `DEFINITION` | even `resultRun` recurrence |
| 10 | 53–63 | `rule-e5081bd4cee79173c7202998fcb1e25abb7ecbb7f638e6a69740ac8de310e9e9` | `DEFINITION` | odd `resultRun` recurrence |
| 11 | 64–66 | `rule-fc30da05d622ab17da2f4032050110c02a0d0eb32b8614f68ec43efba6450aa4` | `DEFINITION` | `resultRun` base result |
| 12 | 68–76 | `rule-cd588e1b203a59d4324edead96d5948bf0c1c5b2173430eda0466e8f903d55f7` | `DOMAIN_LEMMA` | reverse even `resultRun` fold |
| 13 | 77–85 | `rule-fb668e722ce1e9413ff23f2c2ed84482db6011cd49f97844b2747538201651ac` | `DOMAIN_LEMMA` | reverse odd `resultRun` fold |
| 14 | 86–88 | `rule-cc6f2ca1b001e1f70590a752c7ad3113f15f59b676b5357e85a7cf4963cac878` | `DEFINITION` | simplification copy of the base equation |

The protected classification has the same 14 unique IDs in the same order
and the same whole-inventory hash.  Thus there are no omissions, duplicates,
extras, reordered identities, changed hashes, or unaccounted rules.

The four reverse-step simplification rules are domain lemmas, not definitions:
the forward equations define the terminating summary functions, while the
reverse rules fold an advanced summary state back to the current state for
proof closure.  They are not `PROVED_DERIVED_LEMMA`s because Stage 1 compiles
the module containing them before any `kprove` call and never first proves
the exact rule against a module from which it is absent.  They are relevant:
they are precisely the product, sum, even-list, and odd-list loop folds needed
by the invariant and final list postcondition.  The remaining simplification
rules are duplicate base equations and therefore definitions.  Consequently
every simplification rule is either `DEFINITION` or `DOMAIN_LEMMA`.

No entry is an ordinary configuration execution/observation rule, so there
are no `OPERATIONAL_RULE` entries in this summary-module inventory.  There
are no proved-derived entries.  The true domain set is nonempty and has size
four, so `KLEAN_NO_OBLIGATIONS` would have been illegitimate here.

Raw evidence:

- `evidence/04b_inventory_reconstruction_pass.txt`
- `evidence/03_frozen_sources_and_provenance_refs.txt`

## Stage 4 generation and mathematical identity

I reran `tools.klean_preflight.check_generation` with
`PYTHONPATH=/reference` and exactly the frozen K workspace, protected
classification, and selected generation.  It returned `PASS`, four
obligations, zero designated sorries, the expected frozen-input and generated
tree hashes, and the fixed target.

I then separately checked the ordered bijection.  In order, the generated
obligations are:

1. guarded reverse `factRun` step;
2. guarded reverse `totalRun` step;
3. guarded even `resultRun` step, including append of `F * I`; and
4. guarded odd `resultRun` step, including append of `T + I`.

Each obligation carries the exact source span, normalized source hash,
inventory hash, discovery-manifest hash, and conjunct hash of its source
domain lemma.  The other ten inventory rules form the exact ordered
definition partition.  There are no missing or duplicate obligations.

Mathematically, each Lean conjunct preserves the K guard, variables,
arithmetic update, list append, recurrence arguments, and equality
orientation.  There is no weakened condition, discarded update, irrelevant
lemma, `True`/`False` conjunct, biconditional substitution, or other vacuity.
The four quantified conjuncts are the exact four independently classified
domain lemmas.

The generated declaration is
`Klean106F.Lemmas.targetStatement`.  Its definition hash is
`99ded2b687817173ef1b33b5625cc9d7db16a28d6632aeb4d718a82aade6d02f`
and its fixed instantiated-statement hash is
`d624465aeddd44361faf200cd31f9589f3fdbc6e230b289bbe06a45b8ce6cadb`.
The declaration, full statement, both hashes, all eleven parameter bindings,
and generated tree match the generator manifest and `/audit-input.json`.

Raw evidence:

- `evidence/09_stage4_preflight_rerun_pass.txt`
- `evidence/11b_stage4_bijection_and_target_checks_pass.txt`
- `evidence/10c_relevant_generated_functions_and_obligations.txt`

The initial preflight run in `07_stage4_preflight_rerun.txt` exposed a sandbox
PID-namespace issue: Lean queried `/proc/<its namespace pid>/exe`, which did
not exist in the mounted `/proc`, so Lake could not locate its configuration.
The syscall evidence is in `08o_lean_path_syscall_trace.txt`.  I used a
minimal compatibility interposer that maps only numeric `/proc/*/exe`
`readlink` requests to `/proc/self/exe`; its complete source is
`evidence/lean_proc_compat.c`.  With the pinned Lean 4.22.0 binaries, Lake
then ran normally.  The generated source tree was hash-identical before and
after.  This compatibility step does not alter Lean source, elaboration,
kernel checking, or the generated/candidate artifacts.

## Stage 5 target, build, and proof identity

I copied the candidate into the fresh project
`/tmp/audit-work/stage5-audit.VpzibW`, installed the exact generated project
as `Base`, and ran both `lake clean` and `lake build`.  Both exited 0.  The
complete build transcript is saved; its only diagnostics are unused-variable
lint warnings in the generated target.  The trusted final gate independently
made another temporary copy, replaced `Base` with the selected generated
tree, repeated clean/build, checked the exact theorem type, and returned
`PASS`.

The candidate workspace hash is
`863b684737c1c9d571ba5c0780c34b3679f3b9b153f46a5bec458dd2e26396ce`,
matching `/audit-input.json`.  Its `Proof.lean` hash is
`0a048422cedcb9e66427778661766b9492138c2b9e74ba116b4dc55e8133b313`.
The fresh `Base` remains exactly
`c577390a99b798f99dcf83d67a4e155c27b9456a170f0e0218b82ad99c5a3719`.

Static and elaborated checks establish that:

- each of the eleven target parameters has exactly one candidate `def`;
- there is exactly one `Proof.final`;
- its type is exactly the fixed instantiated generated statement;
- the candidate neither declares nor shadows `targetStatement`;
- the candidate does not modify generated `Base`; and
- candidate Lean sources contain no `sorry`, `admit`, `unsafe`, new `axiom`,
  or new `opaque`.

This is an exact proof of the fixed theorem, not a duplicate, weakened, or
vacuous variant.

Raw evidence:

- `evidence/13_stage5_fresh_clean_build_full.txt`
- `evidence/21_candidate_target_identity_and_shadow_checks.txt`
- `evidence/20_trusted_stage5_final_gate.txt`

## Axiom accounting

Running Lean with `#print axioms Proof.final` produced exactly:

`[propext, Classical.choice, Quot.sound]`

There is no `sorryAx`.  None of the 48 generated declarations in
`trust-inventory.json` is a dependency of `Proof.final`.  The three reported
names are the standard Lean core axioms that the trusted final-gate policy
adds to the trust-inventory allowlist baseline.  The final gate parsed the
exact output, compared every dependency with that policy plus the inventory,
found no unexpected dependency, and returned `PASS`.  There is therefore no
unrecorded candidate or generated proof escape.

Raw evidence:

- `evidence/14_print_axioms_proof_final.txt`
- `evidence/15_axiom_trust_inventory_reconciliation_raw.txt`
- `evidence/15b_trusted_stage5_axiom_policy.txt`
- `evidence/20_trusted_stage5_final_gate.txt`

## Operational bridge audit

I compared every target parameter to its `kore_symbol`, bound source-rule IDs,
frozen rules, source program, and supplied operational semantics:

| Parameter group | Independent judgment |
|---|---|
| `_andBool_` | exact Boolean conjunction used by the even/odd guards |
| `«_<=Int_»`, `«_==Int_»`, `«_=/=Int_»` | exact integer comparison/equality/inequality semantics |
| `«_+Int_»`, `«_*Int_»` | exact integer addition and multiplication |
| `factRun` | exact guarded product recurrence and base state from frozen `verification.k` |
| `totalRun` | exact guarded sum recurrence and base state |
| `pyMod` | exact K formula `((value %Int modulus) +Int modulus) %Int modulus`, implemented with Lean truncated remainder; in all bound rules and the source program the divisor is the literal `2` |
| `valSeqConcat` | exact structural `.ValSeq`/`vCons` concatenation rules |
| `resultRun` | exact even/odd append behavior, index/product/sum updates, and terminated state |

I freshly compiled the supplied K semantics with the LLVM backend and ran
independent programs.  The frozen source returns an empty list for `n = -3`
and `n = 0`, and `[1, 2, 6, 24, 15]` for `n = 5`.  A counterfactual source
mutation changing the initial `total` from `0` to `100` returns
`[101, 2, 106, 24, 115]`, demonstrating that the odd-result summary is
load-bearing.

Independent Lean examples cover true and false guards, negative arithmetic,
Python modulo on negative values, terminated and multi-step summaries,
nonempty concatenation, and both branches of `resultRun`.  The submitted
definitions evaluate to:

- `pyMod (-3) 2 = 1`;
- `factRun 1 5 1 = 120`;
- `totalRun 1 5 0 = 15`;
- `resultRun .ValSeq 1 5 1 0 = [1, 2, 6, 24, 15]`;
- the counterfactual summary state with `T = 100` gives
  `[101, 2, 106, 24, 115]`; and
- an adversarial negative summary start gives
  `[-2, -3, 0, -2, 0]`.

The examples also prove the submitted functions differ from constant
product/sum/result/modulo and identity-concatenation counterfactuals.

As a stronger counterfactual, I made a separate copy and replaced only
`pyMod` by constant zero.  `lake clean` and `lake build` still succeeded,
showing that the structural recurrence theorem alone cannot certify the
operational bridge.  The discriminating frozen-semantics check
`pyMod (-3) 2 = 1` then failed as expected.  The actual submitted formula
passes this check.  This directly rules out the convenient but dishonest
constant bridge and confirms that the submitted proof is legitimate for the
right operational reason.

Raw evidence:

- `evidence/16b_semantics_int_list_bool_exact.txt`
- `evidence/17_fresh_k_operational_smokes.txt`
- `evidence/17b_k_operational_results_concise.txt`
- `evidence/18b_lean_operational_bridge_tests_pass.txt`
- `evidence/OperationalTests.lean`
- `evidence/19b_pymod_counterfactual_mutation_pass.txt`

The failed `18_...` transcript is an initial test-file name-resolution
ambiguity corrected by namespace qualification in `18b`; the evaluated
values were already the same.  The failed `19_...` transcript records an
initial nested `Base/generated` copy layout corrected in `19b`.  Neither was
a candidate or proof failure.

## Final judgment

All provenance bindings, reconstructed rule identities, classifications,
obligation mappings, target hashes, build checks, axiom checks, theorem
identity checks, and operational bridge checks pass.  I found no concern that
changes the proof claim or its trust boundary.

VERDICT: PASS
LEGITIMACY: LEGIT
