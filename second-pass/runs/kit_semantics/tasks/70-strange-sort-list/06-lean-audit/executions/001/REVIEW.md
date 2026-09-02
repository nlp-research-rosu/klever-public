# Independent Stage 3–5 audit: `70-strange-sort-list`

## Result

The protected Stage 3 classification is correct, and the Stage 4 artifacts are
deterministically tied to the frozen inputs. Nevertheless, Stage 4 is not
mathematically legitimate. The generated Lean target quantifies a value of
`SortScope`, but the generated declaration of `SortScope` has no constructors.
The frozen K semantics instead declares `Scope ::= scope(Map, Parent)` and uses
concrete scope values in the initial configuration and execution rules.

Consequently, the one generated domain-lemma conjunct is provable by eliminating
an impossible `SortScope`, for arbitrary implementations of all five bound
operations. This is a vacuous weakening of the frozen K rule's operational
domain. The candidate's clean build and clean axiom report cannot repair that
Stage 4 defect.

Audit mode was independently read as `CLASSIFICATION_AND_PROOF` from
`/audit-input.json` and `AUDIT_MODE`. All mounted candidate, provenance, log,
comment, and review content was treated only as untrusted evidence.

## Producer identity and frozen-input integrity

Before assessing generation, I hashed the mounted generation-time sources:

| Producer | Recomputed SHA-256 |
|---|---|
| `klean_export.py` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` |
| `klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` |

Both hashes match `generation-tools/source-manifest.json` and
`klean-generation/generator-manifest.json`. The immutable image ID is
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`;
it matches both manifests and the image-keyed producer path in
`/audit-input.json`. The producer bundle tree hash also recomputes exactly as
`388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`.
There is no producer-source infrastructure error.

The launcher-recorded Stage 1 K tree, Stage 1 export, Stage 2 audit, Stage 3
manifest, Stage 4 tree, generated project, producer bundle, and candidate tree
hashes all recompute exactly. All 774 recorded Stage 1 source-file hashes have
the exact recorded key set and values. The recorded Lean-invocation object was
not mounted, so its individual recorded hash could not be independently
recomputed; that does not affect the defect found in the mounted generated
source.

Raw evidence: `evidence/02_producer_hashes_and_manifests.txt`,
`evidence/03_producer_identity_crosscheck.txt`, and
`evidence/12_launcher_hash_recomputation.txt`.

## Stage 3 inventory reconstruction and classification

I ran the trusted local rule-inventory implementation against the frozen
`/reference/k-proof/verification.k`. Its local verification-module closure is
exactly `VERIFICATION`. The independently reconstructed inventory contains six
rules in the following order:

| Index | Source span | Recomputed `source_rule_id` | Independent class |
|---:|---:|---|---|
| 0 | 8 | `rule-8277b118773512287e2b2b20da4dbf45607f85956623bafa9028b50596471d08` | `DEFINITION` |
| 1 | 9 | `rule-bb65aed9f318cb650e6f3aaeb61b929864859d3dc05404f2b4a53b0d1f2058d0` | `DEFINITION` |
| 2 | 15–16 | `rule-7e05d593a11ac1688b57228d1e3402caa7bde6bf8a21122047627bf83e3662d2` | `DEFINITION` |
| 3 | 17–19 | `rule-e5cf5fe356747eca4563d29d41d439e5617c1c39a5f5f46120ed36322a8c30f3` | `DEFINITION` |
| 4 | 20–26 | `rule-ec00b8b164e1c0f6d16eef935ec05c2166e772018597863b95e7d0f0326eada7` | `DEFINITION` |
| 5 | 31–33 | `rule-565182bf10d31fb24d96318e023c71c80005ab90c1b99978f05bb734ef394503` | `DOMAIN_LEMMA` |

For every entry, the source slice, normalized source hash, `source_rule_id`,
module, span, and position match the Stage 3 manifest. IDs are unique. There
are no omissions, extras, duplicates, reordered identities, or unaccounted
classifications. The independently recomputed whole-inventory hash is
`da706790352d45b069c499d73417d4bd7022226e9a5a51632c2825c9366b3364`,
matching both the inventory and protected manifest.

The first two rules define the structural `allInts` predicate. The next three
define the guarded `strangeAcc` recurrence; the integer guards partition its
cases and the recursive case shrinks the interval. These are genuine named
summary/recurrence definitions, not domain facts.

The last rule states that deleting `K` from `M (K |-> V)` returns `M` when `K`
is absent from `M`. It is not an execution rule and does not define a named
summary. It is relevant to the frozen program semantics because `#pop` removes
the callee's scope location from the scopes map. Stage 1 compiles this rule into
the verification module before its proof invocations and does not first prove
the exact rule against a module that omits it, so it is not a
`PROVED_DERIVED_LEMMA`. `DOMAIN_LEMMA` is the correct independent
classification. It is the only `[simplification]` rule, satisfying the
requirement that simplifications be definitions or domain lemmas.

Raw evidence: `evidence/07_reconstructed_rule_inventory.json`,
`evidence/08_frozen_k_source_spec_solution_and_stage3.txt`,
`evidence/09_inventory_bijection_and_hash_recomputation.txt`, and
`evidence/11_operational_context_and_prior-proof_search.txt`.

## Stage 4 structural integrity

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`
and exactly the requested K workspace, discovery manifest, and selected
generation directory. The fresh result reports `PASS`, one obligation, zero
designated or other sorries, a clean generated-project build, and 43 recorded
trust declarations.

The first preflight attempt exposed a container-specific `/proc/<pid>/exe`
lookup failure in Lean 4.22: the sandbox-visible process ID had no matching
mounted procfs entry. I documented that failure and reran with a minimal
auditor-built `readlink` shim that redirects only numeric `/proc/<pid>/exe`
lookups to `/proc/self/exe`. Lean then reported its exact expected version and
the required clean/build checks succeeded. The shim changes neither source nor
proof artifacts.

The sole domain rule maps bijectively to one generated conjunct. There are no
omitted, extra, or duplicate source rules or obligations. The independently
recomputed hashes are:

| Object | SHA-256 |
|---|---|
| Generated project tree | `074c1333d2218574e13272f0e5afbb35e4f1bdbc78d326ebaaf92803bdd6e0b3` |
| Obligation map | `b5282b54071d64f8f6e4aa50a3d350c5bb63708992afe15ea39f20947a93665e` |
| Sole conjunct | `beb982d3d676f090b6f62a6e6ffa723b3556ba6ce0e5d72a9d3f65992e7942f2` |
| Target definition | `e2d8cb7b8fa23a1e8872dd6d1378d6460238926e5481ed82eb51e9ef1cd39171` |
| Target statement | `59c6a8cdae0d53bb890487b0c988dc380ed0e04d779f5cf1b2d696ba0b2a0bfc` |

The target is exactly
`Klean70StrangeSortList.Lemmas.targetStatement`, with the recorded five
parameters `_Map_`, map membership, map deletion, singleton-map construction,
and Boolean negation. Every parameter's binding hash, KORE symbol, and
`source_rule_ids` recomputes exactly. The declaration, statement, hashes, and
generated tree agree among the generated source, generator manifest,
obligation map, audit input, and fresh `Base` copy.

Raw evidence: `evidence/44_fresh_check_generation_pass.txt`,
`evidence/45_stage4_manifests_and_generated_target.txt`,
`evidence/50_target_and_binding_hash_algorithms.txt`, and
`evidence/51_fixed_target_and_hash_identity.txt`. The diagnosed environment
issue and shim are recorded in `evidence/13_fresh_check_generation.txt` and
`evidence/41_proc_readlink_diagnosis.txt` through
`evidence/43_proc_readlink_shim_success.txt`.

## Stage 4 mathematical rejection: empty operational domain

The generated target is:

```lean
∀ (K : SortInt) (_V : SortScope) (M : SortMap)
  (h : notBool_ (in_keys (inj K) M) = true),
  remove (concat M (element (inj K) (inj _V))) (inj K) = M
```

But the generated sort source says only:

```lean
inductive SortScope : Type
```

It has no constructors. A complete case analysis in fresh Lean confirms that
the type is empty. This contradicts the frozen operational K semantics:

```k
syntax Parent ::= "root" | parent(Int)
syntax Scope  ::= scope(Map, Parent)
```

The initial K configuration itself contains
`scope(.Map, parent(-1))`, and ordinary execution rules manipulate
`scope(M, P)`. Therefore this is not an intentionally empty or irrelevant
sort.

I constructed a fresh adversarial theorem with the exact generated target but
arbitrary values for all five operation parameters. Lean accepts:

```lean
intro _K impossibleScope _M _h
exact nomatch impossibleScope
```

`#print axioms` reports that this adversarial theorem depends on no axioms.
Thus the single generated conjunct says nothing about map concatenation,
membership, deletion, singleton construction, or Boolean negation. It does not
cover any real frozen-K scope value and is a vacuous weakening of the classified
domain lemma. This violates the required mathematical obligation and
operational-bridge checks even though every generation hash is internally
consistent.

Raw evidence: `evidence/46_target_and_candidate_source.txt`,
`evidence/64_empty_scope_vacuity_proof.txt`, and the direct source comparison
in `evidence/67_scope_domain_mismatch.txt`.

## Stage 5 clean build, proof identity, and trust accounting

I created `/tmp/audit-work/lean-audit-002`, copied the immutable generated
project into it as `Base`, and copied the candidate project sources. The copied
`Proof.lean` is byte-identical to `/candidate/Proof.lean`, with SHA-256
`371fc905de4e1643fec4f3672a13f1f195d70e64216db148a094867533848808`.
Fresh `lake clean` and `lake build` both exited 0.

The candidate does not redeclare or shadow the generated target. It contains no
`sorry`, `admit`, `unsafe`, new `axiom`, or new `opaque`. `#print Proof.final`
shows that `Proof.final` has exactly the fixed target applied to the candidate's
five definitions; it is not a duplicate or altered theorem.

The exact requested axiom output is:

```text
'Proof.final' depends on axioms: [propext, Classical.choice, Quot.sound]
```

There is no `sorryAx`. These three are Lean core logical dependencies, not
candidate declarations. None of the 43 generated declarations recorded in
`trust-inventory.json` appears in `Proof.final`'s axiom dependency list, and
the candidate introduced no unrecorded proof escape.

Raw evidence: `evidence/48_fresh_candidate_clean_build_pass.txt`,
`evidence/49_forbidden_constructs_and_trust_allowlist.txt`,
`evidence/52_print_axioms_proof_final.txt`,
`evidence/65_bridge_tests_sources_and_candidate_copy_identity.txt`, and
`evidence/66_print_proof_final.txt`.

## Operational-bridge review of all target parameters

I located each exact candidate definition and compared it with its bound KORE
symbol, source-rule binding, frozen Map/Bool hooks, and the operational use of
the rule:

| Parameter | Candidate definition | Operational assessment |
|---|---|---|
| `_Map_` / Map concatenation | concatenates the two association lists | Nonconstant and has the expected behavior on the guarded, disjoint-map case used by the rule; overlapping maps are merely totalized outside that case. |
| map `in_keys` | recursively compares keys | Produces true for a present key and false for an absent key, matching the frozen membership hook on valid map representations. |
| map deletion | recursively filters the selected key | Removes the target and preserves other entries on adversarial ground tests, matching the relevant frozen deletion behavior. |
| singleton Map element | constructs a one-pair list | Matches singleton construction on representable values. |
| `notBool` | Lean Boolean negation | Matches both Boolean cases. |

The fresh adversarial tests exercise present/absent membership, deletion with an
unrelated entry, nonidentity concatenation, singleton construction, and both
Boolean cases. They also demonstrate that identity concatenation/deletion and
a deliberately false guard can satisfy the target under counterfactual
bindings, so a build alone does not establish the bridge.

More importantly, no candidate definition can construct the value needed for
the source rule's `_V : Scope`: the generated `SortScope` has no inhabitants.
The candidate's seemingly reasonable list models are therefore never tested by
the fixed theorem on the actual operational case
`K |-> scope(M, Parent)`. The independent arbitrary-parameter proof above
confirms the failure without relying on candidate implementation details. This
is an operational-bridge failure and makes the proof not legitimate.

Raw evidence: `evidence/53_relevant_generated_sort_and_function_defs.txt`,
`evidence/54_generated_hook_models_and_kore_symbols.txt`,
`evidence/55_k_builtin_semantics_inventory.txt`,
`evidence/60_operational_bridge_adversarial_and_counterfactual_tests_pass.txt`,
and `evidence/65_bridge_tests_sources_and_candidate_copy_identity.txt`.

## Final judgment

Stage 3 is correctly and completely classified. Stage 4 passes deterministic
and mechanical integrity checks, and Stage 5 is a clean proof of the fixed
generated theorem with no unrecorded trust escape. However, the fixed theorem's
only obligation is vacuous because generation erased every constructor of an
operationally inhabited K sort. It therefore fails to express the frozen
domain lemma and cannot support a legitimate Stage 5 proof.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
