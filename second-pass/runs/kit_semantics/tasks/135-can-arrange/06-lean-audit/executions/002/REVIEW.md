# Independent audit: HumanEval 135-can-arrange

## Scope and result

I audited condition `kit-semantics`, semantics mode `SUPPLIED_SEMANTICS`, in `CLASSIFICATION_AND_PROOF` mode. The mode in `AUDIT_MODE` agrees with `/audit-input.json`. I treated the candidate, prior reviews, logs, comments, and manifests only as evidence and reconstructed the relevant facts from the frozen source and trusted tooling.

The Stage 3 classification is correct, and Stage 4 is structurally deterministic and bound to that classification. The fixed Stage 4 Lean target is nevertheless semantically weaker than the frozen K domain because its generated `SortStr` has no constructors. The Stage 5 project builds cleanly and `Proof.final` has an empty axiom closure, but it does not establish an independent operational bridge: its `applyCmp(">=")` implementation calls the same candidate `orderablePair` and `orderGe` helpers that appear on the other side of the theorem. Materially false counterfactual implementations therefore continue to prove the unchanged target. This is an operational-bridge failure.

| Component | Judgment |
| --- | --- |
| Stage 3 inventory and classification | Pass |
| Stage 4 producer authentication and structural generation | Pass |
| Stage 4 mathematical coverage of frozen K values | Fail: K strings are erased by constructor-free `SortStr` |
| Stage 5 build, target identity, syntax scan, axiom closure | Pass |
| Stage 5 operational bridge | Fail: circular/vacuous proof survives false mutations |

## Input and producer authentication

The signed audit-input envelope recomputes to `27c843f88771cee2945d75420ecc174f2df81c5f8a30e8fc06ad73d8e2c45974`. I independently recomputed every recorded hash for which the launcher supplies a mounted artifact:

- Stage 1 pipeline tree: `0f35450b3e4540b5f0fd10797f93d80a21640feeb8065e21b8cb9c6bbd58db56`.
- Stage 1 export tree: `1b3dd0a9969538031ffe5ae120ffe22df07388f253b5e6234def725583cb4dbf`.
- Stage 3 manifest: `aafc91d063f2bf10a1025b189e023aa40814f6c46eaa293b97bc1e6e67cb1beb`.
- Selected Stage 2 audit tree: `eeee623ac1af013c0dde182495cb3d1b83109b3cf907c0c4e6a8957c0a1656f6`.
- Selected Stage 4 generation tree: `f44f6fbef8d695cecfdf53d7dda430d6581f9b7250dcb815cabd6f5d7a9a64c5`.
- Generated Lean project: `3385ac6364d0b8e9436c7956e6dc7dec10fcb838ccb0c447cd8075cf70622641`.
- Generation producer source tree: `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`.
- Candidate Lean workspace: `0f9b050892f50734180361bb394c17bb09cdd4b94525f119cc3efdd03af623b4`.

All 835 Stage 1 per-file source hashes also match bijectively: no missing, extra, or changed path. The recorded `lean_invocation_sha256` has no corresponding mounted invocation artifact, so I did not use that provenance claim; the mounted candidate workspace itself matches its recorded hash and was rebuilt independently.

Before assessing Stage 4, I hashed the exact mounted producer sources:

- `klean_export.py`: `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07`.
- `klean.py`: `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d`.

These match both `source-manifest.json` and the top-level producer hashes in `generator-manifest.json`. The immutable image ID is `sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`; it agrees between the producer source manifest, the generator manifest, and the immutable producer directory selected in `/audit-input.json`. Producer authentication therefore passes and there is no producer-source `AUDIT_ERROR`.

Full values and comparisons are in `evidence/06_producer_authentication.typescript`, `evidence/08_producer_pipeline_tree_hash.typescript`, and `evidence/30_recorded_hashes.typescript`.

## Stage 3: reconstructed inventory and independent classification

Using the trusted rule-inventory implementation on the frozen `/reference/k-proof/verification.k`, I reconstructed verification module `VERIFICATION` and its local closure, in order:

1. `VERIFICATION-BASE`
2. `VERIFICATION`

The frozen `verification.k` SHA-256 is `e67f2b057b77184651c67f8fc12a9646e58483fd881ba0ec8ced3df979e493f3`. The reconstruction contains exactly 23 rules, and the canonical inventory hash is `f5b69f74b12f0505988375faf85089ef4d83ccca0e2946d2e4e09f482da52564`.

The reconstructed sequence is bijective with `/reference/lemma-discovery.json`: all 23 ordered identities, source spans, normalized hashes, and `source_rule_id` values match. Both sides have unique IDs. There are no omissions, duplicates, extras, reorderings, or unaccounted classifications. The complete per-rule reconstruction is in `evidence/05_reconstructed_inventory.typescript`; the ordered comparison is in `evidence/10_inventory_bijection_and_classification_counts.typescript`.

My classification of the source rules is:

| Frozen lines | Rules | Classification | Reason |
| --- | ---: | --- | --- |
| 7-8 | 1 | `DEFINITION` | Defines the named summary `isNumericVal`. |
| 11-13 | 1 | `DEFINITION` | Defines the named summary `orderablePair`. |
| 20-32 | 4 | `DEFINITION` | Base and recursive cases defining `scanDefined`. |
| 38-68 | 11 | `DEFINITION` | Exhaustive typed cases and the non-orderable fallback defining the named summary `orderGe`. |
| 76-98 | 5 | `DEFINITION` | Base and recursive cases defining the mathematical scan `arrangeSeq`. |
| 106-108 | 1 | `DOMAIN_LEMMA` | Guarded equality connecting pre-existing operational `applyCmp` to the independently named summary `orderGe`. |

Thus the independent counts are 22 `DEFINITION`, zero `OPERATIONAL_RULE`, zero `PROVED_DERIVED_LEMMA`, and one `DOMAIN_LEMMA`. Every rule marked `[simplification]` is either one of the definitions above or the sole domain lemma.

The domain lemma is exactly:

```k
rule applyCmp(">=", V:Val, W:Val) => orderGe(V, W)
  requires orderablePair(V, W)
  [simplification]
```

Its ID is `rule-2fd1883e1dbbdfd9717b1321447ac996a4962a56a877371e6e1bee92b5b19050`, its span is 106-108, and its normalized hash is the ID suffix.

It is not a definition: `applyCmp` is declared and operationally defined in the supplied MPY semantics, while this rule connects that existing observation to a proof summary. It is not an ordinary execution rule for the source program. It is not a proved-derived lemma under the required standard: `connection-spec.k` imports only `VERIFICATION-BASE` and proves ten separately typed cases, but Stage 1 never first proves this exact guarded dynamic rule against a module lacking it and then uses that exact rule later.

The lemma is relevant, not incidental. The source program's central test is `if not value >= previous`, and `arrangeSeq` uses `orderGe(V,P)` to model precisely whether that test updates the answer. The supplied operational semantics has the matching ten `applyCmp(">=")` cases: integer, Boolean promotions, float, both mixed integer/float directions including Boolean promotion, and string lexicographic comparison. A nonempty domain set is therefore required; `KLEAN_NO_OBLIGATIONS` would have been illegitimate here.

## Stage 4: deterministic generation and target identity

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and the required frozen inputs. Lean 4.22 initially could not locate its installation because this sandbox's PID namespace does not expose `/proc/<namespace-pid>`. I preserved that failure. I then used the audit-local compatibility shim in `evidence/scripts/proc_pid_compat.c`, which changes only `getpid()` to the host PID already exposed by `/proc/self`; it does not alter Lean source, the generated project, or proof behavior. The required preflight then returned `PASS`, with internal `lake clean` and `lake build` exit code 0, obligation count 1, designated-sorry count 0, and trust-declaration count 44. See `evidence/11_preflight_rerun.typescript` and `evidence/15_preflight_rerun_with_pid_compat.typescript`.

The independently classified domain-ID list, the discovery domain-ID list, `obligation-map.json.source_rules`, and `obligation-map.json.obligations` are all the same one-element ordered list. The entries are unique. The source span and normalized hash match the reconstructed source. The obligation-map file hash is `b810ff3614a4b526554d9bb44e08fe759df914b1ed3ddbc557acf857d9be45ae`, and the Lean conjunct hash is `02b175511f3c0b83ae64f5b7c84c0e610236789cc28c505e2f4e6b574b34eb1d`; both recompute exactly.

The sole generated obligation has the correct guarded equation:

```lean
∀ (W V : SortVal)
  (h : orderablePair V W = true),
  applyCmp ">=" V W = orderGe V W
```

It is directly relevant to the source comparison and is neither duplicated nor omitted. In the intended K domain its guard is satisfiable for every numeric pair and every string pair, so the source obligation itself is not a vacuous conjunct.

All three target parameters (`applyCmp`, `orderGe`, and `orderablePair`) are bound to the same source-rule ID and the expected KORE symbols. The fixed target is exactly `Klean135CanArrange.Lemmas.targetStatement`. Its definition hash is `29c9d56b6c41f072e1ffbf7a268135fe25c7df1e7221ad70d5f8d0796d516fc3`; its application statement hash is `f6546a0c884ecb415a7b6dffde624a2418ff099073c317144ff6bc9b0d5340d0`. Both match the generator manifest and audit input, and the generated `Lemmas.lean` bytes copied into `Base` are identical. See `evidence/21_target_identity_and_hashes.typescript` and `evidence/32_stage4_bijection_and_relevance.typescript`.

There is, however, a mathematical coverage defect in the fixed generated Lean universe. Frozen K declares `syntax Str ::= str(IntSeq)`, uses that constructor in the `orderGe` definition, proves a string/string connection case, and permits the source list to contain strings. Generated `Sorts.lean` instead contains the constructor-free declaration `inductive SortStr : Type`. Consequently no Lean `SortVal.inj_SortStr` value can be constructed, and the generated target cannot quantify over the frozen K string cases. The target is source-exact in equation shape but weakened in value coverage.

## Stage 5: clean build, target, and trust boundary

I made a fresh workspace at `/tmp/audit-work/lean-audit.EpMip4`, copied the candidate into it, and copied the immutable generated project into `Base`. The first attempted fresh-copy layout was wrong and is transparently preserved in `evidence/17_fresh_candidate_lake_clean.typescript`; I discarded it and used the correctly constructed workspace for all judgments.

In the correct workspace:

- `lake clean` exited 0.
- `lake build` exited 0 and built both `Base` and `Proof`.
- The copied `Base/Klean135CanArrange/Lemmas.lean` hash is `747802744cbc1cdeaf0fbe298526decb2ded24aca359c1deecbfcc09ce9bc627`, identical to the immutable generated file.
- The candidate does not declare or shadow `targetStatement`.
- Candidate-owned Lean files contain no `sorry`, `admit`, `unsafe`, `axiom`, or `opaque` token.

Complete output is in `evidence/18_fresh_candidate_lake_clean.typescript`, `evidence/19_fresh_candidate_lake_build.typescript`, `evidence/20_target_and_forbidden_token_checks.typescript`, and `evidence/31_candidate_static_and_trust_reconciliation.typescript`.

Running Lean with `#print axioms Proof.final` produced exactly:

```text
'Proof.final' does not depend on any axioms
```

The trust inventory contains 44 generated declarations, but none occurs in `Proof.final`'s dependency closure. There is no `sorryAx` and no unrecorded proof dependency. The exact output is in `evidence/22_print_axioms_proof_final.typescript`.

`#check` and `#print` show that `Proof.final` proves exactly the fixed target applied to the candidate definitions, not a duplicate declaration or a syntactically changed target. Its elaborated proof reduces to two `if_pos` rewrites followed by `Eq.refl (operationalOrderGe V W)`. See `evidence/23_print_proof_final.typescript`.

## Stage 5 operational-bridge audit

I located and checked each exact definition bound by `target.parameters`:

- `orderablePair` delegates to `operationalOrderablePair`, which recognizes numeric/numeric and string/string pairs. Its numeric behavior agrees with the K summary, but its string arm is uninhabited because generated `SortStr` is empty.
- `orderGe` delegates to `operationalOrderGe`. Its nine representable numeric/Boolean/float combinations follow the frozen summary, and its non-orderable fallback is false. Its frozen string/string case is implemented only as `nomatch` and therefore has no operational content.
- `applyCmp` delegates to `operationalApplyCmp`. On the exact operator appearing in the obligation it does not independently implement the supplied operational K rules. Instead it executes `if operationalOrderablePair left right then operationalOrderGe left right else false`.

That last definition bakes the desired lemma into the implementation being audited. `applyCmp`, the guard, and the right-hand summary share the same candidate helpers, so the theorem checks their internal consistency rather than connecting the frozen operational dispatcher to the summary.

Ground tests on the unmodified candidate give expected representable examples (`2 >= 1`, `1 >= 2`, and `true >= false`), but examples cannot repair the universal operational-bridge gap. The audit-local declaration `generatedSortStrIsEmpty : SortStr → False := nomatch` confirms that no string adversarial example can even be stated in this generated universe. See `evidence/25_original_adversarial_examples.typescript`.

The counterfactual checks are decisive:

1. I replaced `operationalOrderGe` by the constant-false definition `| _, _ => false`, leaving `Proof.final` unchanged. The project still built. On the concrete orderable pair `(2,1)`, the guard remained `true`, while both `orderGe` and `applyCmp(">=")` became `false`; `Proof.final` still had the exact fixed target type. Thus a materially incorrect order operation survives because `applyCmp` shares the mutated helper. Evidence: `evidence/24_counterfactual_orderge_constant_false.typescript` and `evidence/26_mutation_ground_witness.typescript`.
2. I replaced `operationalOrderablePair` by constant `false`, again leaving `Proof.final` unchanged. The project still built, even though the guard now reports `false` for the orderable integer pair `(2,1)`. The obligation becomes vacuous because the same false guard controls both the theorem premise and the candidate `applyCmp` branch. Evidence: `evidence/27_counterfactual_orderable_constant_false.typescript` and `evidence/29_orderable_mutation_witness_success.typescript`.

These are not weaknesses in Lean's kernel or its axiom accounting; they expose the candidate definition strategy. A constant, vacuous, circular, or otherwise convenient definition is expressly insufficient unless it independently implements the frozen operational meaning. Here the unchanged proof accepts both a false comparison implementation and a false orderability predicate, while the actual candidate also cannot implement the frozen string cases. Therefore the Stage 5 proof is kernel-valid for its chosen Lean definitions but is not a legitimate proof of the required operational bridge.

## Evidence record

`evidence/COMMANDS.md` records the principal commands and maps them to complete stdout/stderr captures. Audit helper sources, including the PID compatibility source and independent hash/bijection scripts, are under `evidence/scripts/`. Failed audit setup probes are retained and explicitly superseded rather than hidden.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
