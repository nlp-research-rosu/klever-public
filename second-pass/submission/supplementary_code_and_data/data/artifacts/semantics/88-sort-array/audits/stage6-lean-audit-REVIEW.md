# Independent Stage 3–5 audit: HumanEval `88-sort-array`

## Scope and result

The launcher-selected mode is `CLASSIFICATION_AND_PROOF`; the condition is
`semantics` and the semantics mode is `SUPPLIED_SEMANTICS`. I treated the
candidate, earlier reviews, comments, logs, and manifests as evidence rather
than authority. The conclusions below come from the frozen source, the trusted
inventory/preflight code, independent hash reconstruction, a fresh Lean build,
and an operational comparison of the one Stage 5 parameter.

The Stage 3 classification is complete and mathematically appropriate. Stage 4
is a deterministic, provenance-correct generation with one relevant,
non-vacuous obligation and an unchanged target. The Stage 5 candidate cleanly
proves exactly that target and its parameter implements the frozen `snocVS`
recurrence rather than a convenient substitute.

## Input and producer integrity

`/audit-input.json` passes the trusted Stage 6 input contract. Its recomputed
resolved-input digest is
`2bf7cf4877e190988dc43d1f5188eb2b2fcc944d57b7dc76c019cefb8b922a26`,
exactly the recorded value. All 35 individually recorded Stage 1 source hashes
also match.

Before judging Stage 4, I hashed the mounted generation-time producer sources:

| Producer | Observed SHA-256 | Manifest SHA-256 |
|---|---|---|
| `klean_export.py` | `0502c621a70a19a851cc2971bf9927f38fd5cb452f42849efa23b6cde5740cd7` | same |
| `klean.py` | `1ba065b19feb2fb0a48abe80bc2cf0d0afd3d72289374303745e0d5a59f0bccc` | same |

The source manifest and generator manifest both name immutable generator image
`sha256:a9d22db785bb0037bdc2ddb97ba95c9c13087febc9739cd864142872965a4510`.
The bundle path selected by the audit input uses the same image key, and the
producer bundle tree hash is
`18b826bb3071ceaaf8133e451648a7fd33f2b977c46df66edead63955ecbbf12`,
exactly the audit-input value. The source bundle has precisely the two producer
files plus `source-manifest.json`.

Using the pipeline's actual tree-hash algorithm, rather than a similarly named
but differently framed legacy helper, every accessible audit-input hash
matches:

| Input | Recomputed hash |
|---|---|
| Stage 1 workspace | `1186711ffec317932b5b43d729a57c16a71027823b91aa10c5176d2cf6e9474b` |
| Stage 1 export tree | `abed19e37436b034f2240d067f17624c847cf381f03a3331a5b964fd534868c0` |
| Stage 2 selected audit | `00be356a3ce25240532e75751391e96955a5160ec21a95d95db4b6c95ab71c96` |
| Stage 3 manifest | `ee735df649b9c8f80d86dcf75293b4bef617c98707a9cb31cf20e0d09adc235b` |
| Stage 4 generation | `d7d1dfffbe52fe0e2ded7633ef7a958f08217bf319c5d4ad2fe61ec68947644e` |
| Generated project | `a55312e4f5b7d24be08f3c87cff463f1526117cbe793ef50e363eefee95d481f` |
| Stage 5 candidate | `fe65f1f3e53ee2b28e9955b0c457f00bb2463a2e46225786a45b795be9aa1201` |

## Independent inventory reconstruction

I ran `tools.k_rule_inventory.inventory_verification` from
`PYTHONPATH=/reference` on `/reference/k-proof`. The local
verification-module closure contains only module `VERIFICATION`; its external
`MPY` import is supplied by the frozen semantics tree. The reconstruction found
exactly nine rules. Each `source_rule_id` is `rule-` followed by the recomputed
normalized-source SHA-256.

| Lines | Normalized SHA-256 | Independent class |
|---|---|---|
| 10–31 | `263bd15cb4ec361038ce827fc81456896d90f6704755944c2de296883bce1485` | `DEFINITION` |
| 34–35 | `14d4ccfe4563a625070d0aba326cb259d3cdce5e8e8e45d5dbcc3ecbadd201a9` | `DEFINITION` |
| 39 | `0d4c46a7163f5c5ee21b30bb397721cb0628a5455c22404392aa20e5e8d42cb8` | `DEFINITION` |
| 40 | `5d37caabd948d738dd2dcc088a48c04f3cd6d66f0ae83ccf8ee0b133c09faae2` | `DEFINITION` |
| 43 | `03661db14f885c490255229be7866dfea6edcd71783c1e638ae5d2e6bfabdc91` | `DEFINITION` |
| 44–45 | `3ba97f4ae1b69bd9ddfe88cafba9dfe0564e263c89af2db957db5f8b413286b1` | `DEFINITION` |
| 51 | `becebddf142d7576a24cbe9dcc443d2914a5940ec4d344d1d179d0b17c2a8678` | `DEFINITION` |
| 52–53 | `a074558c6e6502d0ec637dab6d4ea3994203ef7eb07051486fef343a035c7b87` | `DEFINITION` |
| 55–62 | `ab4b49bc5cb4d2f873e2b399b9cb8d81a81689b74a6ddc22dfb813e2f897e479` | `DOMAIN_LEMMA` |

The whole reconstructed inventory hash is
`1a6b21a7676e43880fde0ba9e4ba918fcee5f47deff206d181a5ba6184f837b3`.
The protected Stage 3 manifest has the same hash and the same nine IDs in the
same order. Both sides have unique IDs. There are no omissions, extras,
duplicates, reordered identities, or changed normalized hashes.

## Classification judgment

The first two rules name the exact translated source body and its closure. The
next six are the exhaustive base/recursive equations for `intsVS`,
`nonNegativeIS`, and `snocVS`. These are definitions in the required sense:
named proof terms, structural conversions, predicates, and recurrences.

The last rule is not part of the supplied MPY execution semantics. It is a
proof-local shortcut stating that negative-one indexing of
`list(vCons(F, snocVS(M,L)))` yields `L`. Stage 1 does not first prove this exact
rule in a module that omits it, so it is not a `PROVED_DERIVED_LEMMA`, despite
the informal source comment calling it “derived.” It is also not an ordinary
language execution/observation rule: it is specialized to the proof summary
`snocVS` and exists to avoid symbolic unfolding of an arbitrary middle
segment. `DOMAIN_LEMMA` is therefore the correct class.

The domain lemma is materially relevant. `solution.py` branches on
`array[-1]`, while the two length-at-least-two claims in `spec.k` represent the
input as `vCons(F, snocVS(intsVS(MIDDLE),L))`. Under the frozen semantics,
`UnaryOp("-",Int(1))` evaluates to `-1`; `vsLen`, `normIdx`, and `valSeqAt`
then select the appended last element. The lemma states that exact fact.

No reconstructed rule has a `simplification` attribute, so there is no
misclassified simplification rule. The resulting independent counts are eight
definitions, zero operational rules, zero proved-derived lemmas, and one
domain lemma.

## Deterministic Stage 4 generation

I reran the required function directly:

```text
PYTHONPATH=/reference python3 -c '... tools.klean_preflight.check_generation(
  /reference/k-proof,
  /reference/lemma-discovery.json,
  /reference/klean-generation,
  toolchain_lock=/reference/klean-toolchain.lock.json) ...'
```

The first attempt exposed an audit-sandbox PID-namespace problem: Lean 4.22
constructs `/proc/<getpid()>/exe`, but this sandbox has an unshared PID namespace
without a matching procfs remount. I verified the behavior in the installed
Lean runtime and used a narrow `LD_PRELOAD` shim that redirects only those
executable-path `readlink` calls to `/proc/self/exe`. The shim does not alter
Lean evaluation, candidate source, generated source, or any frozen input. With
that environment correction, the required call returned:

```text
status: PASS
obligation_count: 1
generated_tree_sha256: a55312e4f5b7d24be08f3c87cff463f1526117cbe793ef50e363eefee95d481f
lake clean: exit 0
lake build: exit 0
```

Its output, including build-output hash
`c8b7c90fb129c35b98ff1b80455a35445fa1b5d37bfeaf9777e9834d26959734`,
exactly reproduces the recorded Stage 4 preflight.

The one independently classified domain rule maps bijectively to the one
obligation. The obligation repeats its source ID, lines 55–62, normalized hash,
inventory hash, and discovery-manifest hash. There are no duplicate or omitted
source IDs. Its conjunct hash is
`80a4ef6bc96cfb9ed3e275d0fceb8c8ed2f74134950f0e22a1a20a8ed936772b`.

Mathematically, the conjunct is the exact operational reachability form of the
source rule:

- the equality premise binds the lowered tail `KleanDef0` to
  `snocVS(_M,L)`;
- the LHS preserves `Subscript`, the concrete nonempty list, the first and last
  integer injections, and the unevaluated `UnaryOp("-",Int(1))`;
- the RHS is exactly `L`;
- the arbitrary continuation and every other configuration cell are preserved;
  and
- there is no source guard to omit.

The equality premise is satisfiable by choosing `KleanDef0` to be the displayed
`snocVS` value, and `Proof.final` uses it by equality elimination. It is not a
vacuous conjunct. The source priority attribute controls Stage 1 rule
selection; it is not a separate proposition that should appear in the Lean
goal.

The generated target independently reconstructed from the immutable project is
identical to both the generator manifest and the audit input:

```text
declaration: Klean88SortArray.Lemmas.targetStatement
definition_sha256: c94f07307675b519990b3e2496a7a8b27b961259d309786db5150dbe5a974b0f
statement: Klean88SortArray.Lemmas.targetStatement «snocVS(_,_)_VERIFICATION_ValSeq_ValSeq_Val»
statement_sha256: 9dad0679665c702f7aff55974eeaebe8fcfb1e329dadbb179267e17e3ee8513e
```

## Stage 5 clean build and theorem identity

I created a fresh project at
`/tmp/audit-work/88-sort-array-proof-audit`, copied the candidate into it, and
copied `/reference/klean-generation/generated` into it as `Base`. The copied
Base digest is
`a55312e4f5b7d24be08f3c87cff463f1526117cbe793ef50e363eefee95d481f`,
the exact immutable generated-tree digest.

I then ran both mandatory commands in that fresh project:

```text
LD_PRELOAD=/tmp/audit-work/proc_exe_shim.so lake clean
LD_PRELOAD=/tmp/audit-work/proc_exe_shim.so lake build
```

Both exited 0. The complete clean-build transcript ends with `Built Proof` and
`Build completed successfully.` The warnings are generated-file unused-variable
linters; there are no proof holes or build errors.

The trusted candidate gate independently passes. Outside immutable `Base`, the
candidate has no `sorry`, `admit`, `unsafe`, `axiom`, or `opaque`. It contains
exactly one `def` for the required parameter and exactly one `theorem final`.
It neither changes nor shadows
`Klean88SortArray.Lemmas.targetStatement`. The normalized type of `Proof.final`
is exactly the fixed statement above, not a duplicate or a weakened variant.
The trusted `check_proof_candidate` cross-check also returned `PASS` after its
own isolated clean build and axiom query.

## Axiom accounting

Running Lean on:

```lean
import Proof
#print axioms Proof.final
```

reports 44 dependencies. There is no `sorryAx`. Three are Lean core logical
principles allowed by the trusted gate:

```text
propext
Classical.choice
Quot.sound
```

Every other dependency is an exact name in `trust-inventory.json`:

```text
«.Map»
«Float2Int(_)_FLOAT_Int_Float»
«Int2Float(_,_,_)_FLOAT_Float_Int_Int_Int»
«Int2String(_)_STRING-COMMON_String_Int»
ListItem
«Map:lookup»
«Map:update»
«_%Int_»
«_*Float__FLOAT_Float_Float_Float»
«_+Float__FLOAT_Float_Float_Float»
«_-Float__FLOAT_Float_Float_Float»
«_/Float__FLOAT_Float_Float_Float»
«_<Float__FLOAT_Bool_Float_Float»
«_==Bool_»
«_==Float_»
«_==K_»
«_==String__STRING-COMMON_Bool_String_String»
«_>=Float__FLOAT_Bool_Float_Float»
«_>Float__FLOAT_Bool_Float_Float»
_List_
_Map_
«_[_<-undef]»
«_^Float__FLOAT_Float_Float_Float»
«_^Int_»
«_in_keys(_)_MAP_Bool_KItem_Map»
«_|->_»
«absFloat(_)_FLOAT_Float_Float»
«absInt(_)_INT-COMMON_Int_Int»
append
«binAcc(_,_)_MPY-BUILTINS_IntSeq_Int_IntSeq»
«buildIS(_,_,_,_)_MPY-SUBSCRIPT_IntSeq_IntSeq_Int_Int_Int»
«buildVS(_,_,_,_)_MPY-SUBSCRIPT_ValSeq_ValSeq_Int_Int_Int»
«ceilFloat(_)_FLOAT_Float_Float»
«cntSub(_,_)_MPY-METHODS_Int_IntSeq_IntSeq»
«floorFloat(_)_FLOAT_Float_Float»
«maxFloat(_,_)_FLOAT_Float_Float_Float»
md5hexCodes
«minFloat(_,_)_FLOAT_Float_Float_Float»
«rootFloat(_,_)_FLOAT_Float_Float_Int»
sortKeyVS
«strToCodes(_)_MPY-STR_IntSeq_String»
```

These are all recorded data/function trust declarations, not unrecorded
propositions or candidate-added proof escapes. The evidence reconciliation
records the inventory kind, source, line, type, and reason for each one.

## Operational bridge audit

The only `target.parameters` entry is:

```text
name: «snocVS(_,_)_VERIFICATION_ValSeq_ValSeq_Val»
type: SortValSeq → SortVal → SortValSeq
kore_symbol: LblsnocVS'LParUndsCommUndsRParUnds'VERIFICATION'Unds'ValSeq'Unds'ValSeq'Unds'Val
binding_sha256: a90d456f08946e6d516c0e6f71669d651e586971c0434ec355dbecccfe2a83a0
source_rule_ids: [rule-ab4b49bc5cb4d2f873e2b399b9cb8d81a81689b74a6ddc22dfb813e2f897e479]
```

The candidate's exact definition is structural recursion:

```text
snocVS(.ValSeq, value) = vCons(value, .ValSeq)
snocVS(vCons(head, tail), value) = vCons(head, snocVS(tail, value))
```

This is constructor-for-constructor identical to frozen `verification.k` lines
51–53, whose defining IDs are
`rule-becebddf142d7576a24cbe9dcc443d2914a5940ec4d344d1d179d0b17c2a8678`
and
`rule-a074558c6e6502d0ec637dab6d4ea3994203ef7eb07051486fef343a035c7b87`.
It preserves all middle elements in order and appends the supplied value last.
That is exactly the operational meaning required by `solution.py`'s
`array[-1]` and by the domain rule named in the parameter.

The proof does not invoke the domain lemma as a generated rewrite shortcut. It
derives the target through the generated heat/cool steps, integer unary-minus
rule, generic `Subscript` rule, and the frozen `applyIndex`/`vsLen`/`normIdx`/
`valSeqAt` equations. The arbitrary continuation and all non-`k` cells remain
unchanged.

Adversarial checks compiled exact results for:

- appending to empty;
- appending to a one-element middle;
- appending to a two-element middle; and
- generic negative-one indexing for arbitrary first value, last value, and
  middle sequence.

Counterfactual body mutations were then checked independently. An identity
implementation that ignores the appended value exits 1, failing the length and
last-element obligations. A singleton implementation that ignores the middle
also exits 1, failing the recursive length and positional obligations. Thus the
submitted proof is sensitive to preservation of the middle and is not using a
constant, identity, hard-coded, or vacuous bridge.

## Evidence index

The raw and structured evidence is under `evidence/`. Principal records are:

- `01_producer_hashes_and_manifests.txt` — producer hashes, image ID, and
  manifests;
- `03_inventory_reconstruction.json` — all reconstructed spans, normalized
  hashes, IDs, and bijection checks;
- `04c_required_check_generation_success.json` — required trusted preflight
  result;
- `07b_recorded_hash_verification_correct_algorithm.json` and
  `19_audit_input_and_stage1_source_hashes.json` — input/hash reconciliation;
- `08_independent_classification.json` — per-rule independent classification;
- `09_stage5_lake_clean.txt` and `10_stage5_lake_build.txt` — complete fresh
  clean-build transcripts and exit statuses;
- `11_print_axioms_Proof_final.txt` and `12_axiom_reconciliation.json` — exact
  axiom output and per-dependency accounting;
- `13_candidate_gate_and_target_identity.json` — forbidden-token, binding, and
  exact-target checks;
- `14b_operational_bridge_examples_success.txt`,
  `15_counterfactual_identity_compile.txt`, and
  `16_counterfactual_singleton_compile.txt` — operational/adversarial checks;
- `17_trusted_check_proof_candidate.json` — independent trusted final checker;
  and
- `18_operational_semantics_and_binding.txt`,
  `20_stage4_mathematical_judgment.json`, and
  `21_operational_bridge_judgment.json` — frozen semantics and mathematical
  judgments.

VERDICT: PASS
LEGITIMACY: LEGIT
