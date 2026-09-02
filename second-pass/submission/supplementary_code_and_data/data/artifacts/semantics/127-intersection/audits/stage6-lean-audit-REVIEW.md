# Independent audit: HumanEval 127-intersection

## Scope and result

I audited condition `semantics`, semantics mode `SUPPLIED_SEMANTICS`, in launcher mode `CLASSIFICATION_AND_PROOF`. I treated the Stage 1–5 workspaces, manifests, prior logs, comments, and classifications as untrusted evidence.

The Stage 3 inventory and classifications are sound, and the Stage 4 artifact is byte-for-byte deterministic and correctly bound to its recorded producer. Nevertheless, the generated Lean obligation is semantically vacuous: the frozen K semantics has inhabited `Scope` terms, while Stage 4 generated `SortScope` as an inductive type with no constructors. The candidate exploits precisely that defect with `nomatch frame`; it never proves the Map deletion law. An axiom-free counterfactual test proves the same target with five deliberately dishonest bridge functions.

This is the kind of vacuous generated target the audit instructions require rejecting. It makes both the selected Stage 4 target and the Stage 5 proof not legitimate.

## Producer and input integrity

Before judging generation, I hashed the mounted generation-time sources:

- `klean_export.py`: `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0`
- `klean.py`: `3a5a8be795d55a2bc01b73d47099f04795b9d64f6bbcf64494b57bcde8266582`

Both equal the hashes in `generator-manifest.json` and `source-manifest.json`. The generator image identity is consistently
`sha256:db04cbaec4c5ee7b34348393f5a7742991e12d63480de3eab85fe97022f51657`,
and the audit-input producer selector names that same immutable image. The producer-source launcher tree hash is
`d51304d7acd70db93e839359fc003780b85d84d8ab4fd36ac2ec2a8227f4437b`.
There is no producer-provenance `AUDIT_ERROR`.

All mounted launcher tree hashes match `/audit-input.json`:

- Stage 1: `6dd07c235aae5781b4dd6a5f926270b9db9cd4572c977b450abbbfdefe0cc8f9`
- Stage 2: `0d0b641f10ebaafc2baa53a5952405c43190470697e1af65b883a610d7ed0b6d`
- producer sources: `d51304d7acd70db93e839359fc003780b85d84d8ab4fd36ac2ec2a8227f4437b`
- Stage 4: `827deb5a1dec4f77446a80f7fc7f06d1e2f40856654a589eca61d1d4a099ff9f`
- Stage 5 workspace: `ceee0f3d4c195443e7859faa6290adccc9c45344583822e0b42c67cdd59eea04`

All 35 individually recorded frozen Stage 1 source hashes also match. The generation-specific Stage 1 export hash is
`43e122367c3fa138cd7b368c1dfc4a647fc76627f78a320e9f70fc804e305ad5`,
and the generated project hash is
`ea57bbe9b9d904f91a8e4ef8939cb3b77800bc7449d76d20728d35646d9c09b6`.
The complete recomputation is in `evidence/37_stage4_hash_and_bijection_audit.txt`.

One preliminary record, `evidence/16_producer_provenance_crosscheck.txt`, compared the exporter's internal tree-digest algorithm to a launcher tree hash and is superseded by `evidence/17_producer_tree_hash_contract.txt`, `evidence/18_producer_provenance_correct_hash_contract.txt`, and the complete successful cross-check above. It is not a source mismatch.

## Stage 3 inventory reconstruction

Using the trusted rule-inventory implementation against the frozen `verification.k`, I reconstructed the local verification-module closure in source order:

1. `VERIFICATION-BASE`
2. `VERIFICATION`

The frozen `verification.k` SHA-256 is
`5eec610010347c9a2846f3382cc02cd6d26abfce341dc6a75783e6a9f1a78385`.
The reconstruction contains 12 rules, and its canonical inventory hash is
`2b8a9ab9483d01691862d6f17b9f749f531528c3930e42996b1feddba2790f04`.
That equals the protected manifest's inventory hash. The protected manifest itself hashes to
`887abeff1f4abb1472dd076af3400fd08e1e7624065f1e0cdf4e2f4777195bba`.

The reconstructed and recorded `source_rule_id` lists are identical in order. There are no omissions, additions, duplicate identities, reordered identities, source-span differences, normalized-hash differences, or unclassified entries. `evidence/04_inventory_reconstruction.txt` records every reconstructed span, text, normalized source hash, and identity.

## Independent rule classification

The independent classifications agree with Stage 3:

| Lines | Source rule identity | Classification | Judgment |
|---:|---|---|---|
| 9–10 | `rule-5cdc3db730891902bebfc52c9ef2d3ed5f0ac955c8c9731b0522f080198846d0` | `DOMAIN_LEMMA` | Disjoint K Map deletion fact |
| 16–35 | `rule-788e85236d4fdb02bfae01e44eb7dc4848a2c7aeefa5e5f3978eddefac276591` | `DEFINITION` | Expands named `intersectionBody` |
| 38–43 | `rule-e477e6a18711be5148d01c441315717c292c1b231770c99911dfff771362bf01` | `DEFINITION` | Expands named `divisorBody` |
| 48 | `rule-c894f081fa5f052cfc3c27ba0bb963e894757b2ed6e27e947ef205d1503985dc` | `DEFINITION` | Defines named result `yesV` |
| 49 | `rule-030fd8a67c53b44e20b4cb2ccc77df8f8167452e91b4e41d6a92f017edbed4db` | `DEFINITION` | Defines named result `noV` |
| 55–56 | `rule-218fea2aa535c30ea2fd59ec59079a3980d99783c8971e0dc8770578ae00e579` | `DEFINITION` | `primeFrom` terminal-success equation |
| 57–58 | `rule-481982f7fb0f64a26b0ba203c55547f80e5afbe032144345b7ce7c1c5ae195d9` | `DEFINITION` | `primeFrom` terminal-composite equation |
| 59–60 | `rule-0d1d13596c71ab1f337e58b76564e5f6430e3bc305f977f4e988d03d32fdfeb5` | `DEFINITION` | `primeFrom` recursive equation |
| 62–63 | `rule-54a4a387ef9d190235a844c018259e195e0102c7268712b1fff478181c9828a9` | `DEFINITION` | `primeResult` non-prime equation |
| 64–65 | `rule-1bb0b0bdef9968fad2cf78239c1ddca2b6acf02567365de96909a8f1978fac32` | `DEFINITION` | `primeResult` recurrence entry |
| 68–69 | `rule-0c9edd4e23025de56e77c15f109ea9a7d86609c63e5f44e9d3c83c10c12c43a2` | `DEFINITION` | Defines named mathematical summary `overlapLength` |
| 78–106 | `rule-3564ec1a0c7873a21e248d06a49acdb05fe46af166b68d498bbff1afc2702e72` | `PROVED_DERIVED_LEMMA` | Exact two-phase loop-summary rule |

The ten definitions are genuine named macros, proof terms, or recursive summary equations. None is an ordinary operational rule or a hidden domain fact.

The line 9 Map rule is a genuine domain lemma:

```k
rule (1 |-> _FRAME:Scope REST:Map) [1 <- undef] => REST
  requires notBool (1 in_keys(REST))
```

It states a collection-algebra fact rather than defining a name or executing a source-language construct. It is relevant: the frozen operational `#pop` rule deallocates a call frame with `SC [ L <- undef ]`, and the source solution returns from `intersection`, so the final proof must remove the frame at location 1. The installed K Map theory contains the corresponding symbolic deletion law. It therefore is neither irrelevant nor mislabeled.

The loop summary satisfies the stronger `PROVED_DERIVED_LEMMA` condition. In a fresh Stage 1 copy I compiled `VERIFICATION-BASE`, which does not contain the loop-summary rule, and proved the exact `LOOP-SPEC.loop-correct` claim to `#Top`. I then compiled `VERIFICATION`, which adds that same rule, and proved `SPEC.intersection-correct` to `#Top`. Compiled-source comparison confirms that the only normalization is expansion of the named `divisorBody` definition and alpha-renaming of unused variables. A full-proof rewrite trace records an application at `verification.k:79:5-105:58`. See `evidence/09_two_phase_k_proof.txt`, `evidence/10_normalized_loop_claim_identity.txt`, `evidence/11_compiled_loop_identity.txt`, and `evidence/15_derived_rule_application_excerpt.txt`.

There are no `simplification` rules classified outside `DEFINITION` or `DOMAIN_LEMMA`.

## Stage 4 structural generation audit

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`, using exactly the frozen Stage 1 workspace, protected discovery manifest, and selected generation. It returned `PASS`, one obligation, zero designated sorries, the expected frozen/export hashes, and the expected target. The local sandbox does not expose `/proc/<child-pid>/exe`, which initially prevented Lean from locating its executable. I used an audit-local compatibility wrapper that redirects only such `readlink` calls to `/proc/self/exe`; it does not change any mounted input, Lean source, proof, or generated file. The wrapper source and toolchain check are in `evidence/28_proc_compat_shim_and_toolchain_test.txt`; the successful exact preflight result is in `evidence/29_stage4_preflight_rerun_with_compat.txt`.

The independently reconstructed true domain set has exactly one entry, so `KLEAN_NO_OBLIGATIONS` would have been wrong. Stage 4 instead generated exactly one source rule, one obligation, and one target. Their ordered IDs are all:

`rule-5cdc3db730891902bebfc52c9ef2d3ed5f0ac955c8c9731b0522f080198846d0`

The source span, normalized hash, inventory hash, discovery-manifest hash, and obligation hash all match. The obligation-map byte hash is
`d376a51806582d3f7c2146ef58bbfab59a5177f3bccc62bb24573c7d9566ad90`.
There are no omitted, duplicate, extra, or reordered obligations.

The fixed target is structurally identical across generated source, generator manifest, preflight, and audit input:

- declaration: `Klean127Intersection.Lemmas.targetStatement`
- definition hash: `77c6099db84e920d1ac90e53fe6c583c39d3ad2a53e0c8c9425a0e6f9a7f9d21`
- statement hash: `6ab235a1c3e7a25f39ee53429c5800ce59682e43165ee9b123fe076761ad9935`
- statement: `Klean127Intersection.Lemmas.targetStatement _Map_ «_in_keys(_)_MAP_Bool_KItem_Map» «_[_<-undef]» «_|->_» notBool_`

All five parameter binding hashes recompute exactly and all bind to the one domain-rule identity. Thus the producer and manifests are internally deterministic.

### Fatal mathematical defect in the generated target

Structural integrity does not preserve the operational meaning here. The frozen K semantics declares the inhabited constructor:

```k
syntax Scope ::= scope(Map, Parent)
```

and constructs scopes in the initial configuration, on function entry, and in both proof claims. It also defines the total `builtinsScope`, which rewrites to a `scope(...)`.

Stage 4 instead generated:

```lean
inductive SortScope : Type
```

with no constructors. The sole target universally quantifies `_FRAME : SortScope`. Consequently its quantifier domain is empty, and the whole Map law is true independently of its guard and independently of every one of its five function arguments. The generated target is therefore a vacuous weakening of the frozen K domain lemma, despite its matching text and hashes.

This is directly checked in `evidence/39_vacuity_and_counterfactual_lean_test.txt`. An audit theorem proves `∀ frame : SortScope, False`; then five deliberately false bindings—left projection for Map concatenation, constant `false` membership, identity deletion, empty-map element, and constant `true` negation—still prove the exact generated `targetStatement` with no axioms. That counterexample establishes semantic vacuity without relying on the candidate.

The side-by-side frozen and generated sources are in `evidence/40_scope_vacuity_and_bridge_sources.txt`.

## Stage 5 proof audit

I created `/tmp/audit-work/stage5-proof-audit`, copied the candidate project, and copied the selected generated project into it as `Base`. I then ran both required commands from that fresh project:

```text
LD_PRELOAD=/tmp/audit-work/proc_exe_compat.so lake clean
lake_clean_exit=0

LD_PRELOAD=/tmp/audit-work/proc_exe_compat.so lake build
lake_build_exit=0
```

The complete build output is `evidence/34_stage5_clean_build.txt`. The fresh `Base/Klean127Intersection/Lemmas.lean` is byte-identical to the immutable generated file, with raw file SHA-256
`d3bbd204eb02cc73757fd61da1d42863d12aa05c95af2125c3cc2513f2951c26`.
The candidate has one non-Base Lean proof source, defines each required binding exactly once, has exactly one `Proof.final`, does not declare or shadow `targetStatement`, and contains no `sorry`, `admit`, `unsafe`, new `axiom`, or new `opaque`. See `evidence/36_trusted_stage5_mechanical_gate.txt` and `evidence/42_candidate_integrity_and_forbidden_scan.txt`.

`#check` and `#print` confirm that `Proof.final` has the exact fixed generated statement. It is not a separately named or syntactically weakened theorem. Its proof term, however, is:

```lean
fun _REST frame => nomatch frame
```

It eliminates the impossible `SortScope` argument and uses no Map premise or operation.

The exact `#print axioms Proof.final` output is:

```text
'Proof.final' depends on axioms: [propext, Classical.choice, Quot.sound]
```

There is no `sorryAx`. These are Lean's three standard core dependencies, which the trusted final gate explicitly permits in addition to names in `trust-inventory.json`; none of the 50 generated project axioms is a dependency of `Proof.final`, and the candidate introduces no axiom. The complete printout and elaborated proof term are in `evidence/35_print_axioms_proof_final.txt`. The trusted mechanical gate independently accepts this accounting, but—as the audit instructions emphasize—that gate does not establish theorem relevance or non-vacuity.

## Operational bridge comparison

Every binding below is associated with the exact one domain rule above.

| Target parameter / KORE symbol | Candidate definition | Independent operational judgment |
|---|---|---|
| `_Map_` / `Lbl'Unds'Map'Unds'` | Concatenates the two backing lists | Models disjoint list concatenation only. It is not an honest total K Map implementation: K Maps forbid duplicate keys and the generated Map hook represents overlapping concatenation with `Option`; the candidate silently accepts overlap. The adversarial test concatenates the same singleton-key map with itself and reduces its length to `2`. |
| `«_in_keys(_)_MAP_Bool_KItem_Map»` / `Lbl'Unds'in'Unds'keys'LParUndsRParUnds'MAP'Unds'Bool'Unds'KItem'Unds'Map` | `List.any` using structural K-item equality | Agrees with key membership on a valid unique-key list representation; it is not constant or hard-coded. |
| `«_[_<-undef]»` / `Lbl'UndsLSqBUnds-LT-'-undef'RSqB'` | Filters every matching key from the backing list | Agrees with deletion on valid unique-key maps. On invalid duplicate lists it deletes all copies, but such lists have no K Map meaning. |
| `«_|->_»` / `Lbl'UndsPipe'-'-GT-Unds'` | A singleton key/value backing list | Agrees with a singleton K Map element on the list representation. |
| `notBool_` / `LblnotBool'Unds'` | Boolean negation | Agrees with operational `notBool`. |

These operations support the frame-removal step produced by returning from the frozen source solution; they are not definitions of the source algorithm itself. Four definitions are reasonable on valid list-encoded maps, while `_Map_` fails the full overlapping-key behavior. More importantly, none is connected to the proof: replacing all five by blatant constants or projections still proves the exact target. Therefore the bridge as a whole fails the required operational-faithfulness test, even though the project builds and several individual definitions look plausible.

## Final judgment

The Stage 3 classification is legitimate and the Stage 4 provenance, hashes, bijections, and fixed textual target are structurally sound. The mathematical translation is not: it erases every constructor of a frozen, inhabited operational sort and turns the only true domain obligation into a proposition over an empty type. Stage 5 then proves that vacuous proposition by impossible elimination. This does not prove the frozen Map law and cannot certify the Stage 1 proof's domain assumption.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
