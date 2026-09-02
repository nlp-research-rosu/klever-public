# Independent audit: HumanEval `94-skjkasdkd`

## Scope and result

This audit used the launcher-selected mode
`CLASSIFICATION_AND_PROOF`; `/audit-input.json` and `AUDIT_MODE`
agree.  The condition is `semantics` and the semantics mode is
`SUPPLIED_SEMANTICS`.

Stage 3's classification and Stage 4's deterministic two-obligation
generation are structurally and mathematically consistent with the frozen K
source.  The Stage 5 project clean-builds and `Proof.final` has exactly the
fixed generated type.  Nevertheless, Stage 5 is not legitimate: its
interpretation of K's `_Map_` symbol is order-sensitive list append, whereas
the supplied K Map operation is associative and commutative and rejects
overlapping keys.  The required operational bridge therefore fails.

## Producer provenance gate

I hashed the two mounted generation-time sources before using the generated
artifacts:

- `klean_export.py`:
  `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0`
- `klean.py`:
  `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1`

Both hashes equal the values in `source-manifest.json` and
`generator-manifest.json`.  The source manifest, generator manifest, and the
generator-source path recorded by `/audit-input.json` all identify immutable
image
`sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000`.
The producer bundle's pipeline tree hash is
`55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c`,
exactly the audit-input value.  There are exactly three bundle files:
the two sources and their source manifest.  Thus there is no producer-source
infrastructure error.  Raw evidence is in
`evidence/00_producer_provenance.*`.

## Inventory reconstruction

I ran the trusted `tools.k_rule_inventory.inventory_verification` over the
frozen `/reference/k-proof`, whose `prove.sh` selects local module
`VERIFICATION`.  The reconstructed local verification-module closure has 45
rules.  For each rule the evidence records its module, exact line span, text,
attributes, normalized source hash, and `source_rule_id`.

The canonical inventory hash is:

`769afab15f5d428eaaf9d32871c2abaea87d2d1409d96299a634905c782c18ea`

The protected Stage 3 manifest also has 45 unique IDs.  Its ID sequence is
identical to the canonical sequence, not merely set-equal, and its inventory
hash matches.  There are no omissions, extras, duplicates, or reordered
identities.  The trusted Stage 3 boundary validator accepts the exact
bijection.  Full reconstruction is in
`evidence/01_reconstruct_inventory.result.json`.

All mounted tree and file hashes were also independently recomputed.  The
Stage 1 pipeline tree, Stage 1 export tree, 35 individual Stage 1 source
hashes, Stage 2 audit tree, Stage 3 manifest, Stage 4 generation tree,
generated project tree, producer bundle, and Stage 5 candidate tree all match
their available `/audit-input.json` records.  See
`evidence/06_hash_bijection_target.result.json`.

## Independent classification

I classified all 45 entries from their frozen text and the imported MPY/K
semantics:

| Frozen spans | Count | Classification | Judgment |
|---|---:|---|---|
| `verification.k:7-12` | 2 | `DOMAIN_LEMMA` | Fresh-key Map deletion and update algebra; no named symbol is defined, neither rule was first proved without itself, and both carry `simplification`. |
| `verification.k:18-190` | 20 | `OPERATIONAL_RULE` | Ordinary configuration execution/observation: lookup, assignment, loop binding, normalized comparison/control/call dispatch, and iterator steps. |
| `verification.k:195-248` | 15 | `DEFINITION` | Guarded equations defining the named summaries `trialPrime`, `trialDivisor`, `isPrime`, `largestPrime`, `digitAcc`, and `digitSum`. |
| `verification.k:252-302` | 6 | `DEFINITION` | Macro equations defining the named AST fragments taken from the translated source. |
| `verification.k:307-339` | 1 | `OPERATIONAL_RULE` | A composed but bounded call-entry execution rule over control, environment, scopes, scope allocation, and stack.  It is operational, not a mathematical lemma or named definition. |
| `verification.k:342-343` | 1 | `DEFINITION` | Macro definition of the named `solutionModule` term. |

There are 22 definitions, 21 operational rules, no
`PROVED_DERIVED_LEMMA`, and 2 domain lemmas.  The separately proved claims in
`spec.k` are not rules in this inventory, and no inventory rule satisfies the
required prove-first/use-later criterion.

The two domain rules are relevant rather than decorative:

- `rule-75f08d…6854` removes a fresh explicit binding during the supplied
  semantics' function-frame teardown (`functions.k`'s `#pop` rule).
- `rule-cd6fef…413b` normalizes fresh Map updates used for function-frame
  allocation, parameter/local binding, assignment, and loop-target updates in
  this source program.

Every rule carrying `simplification` was independently classified as either
`DEFINITION` or `DOMAIN_LEMMA`.  My per-entry result matches the protected
manifest for all 45 entries; this is recorded, rule by rule, in
`evidence/10_independent_classification.result.json`.

## Deterministic Stage 4 generation

I reran `tools.klean_preflight.check_generation` with
`PYTHONPATH=/reference` over the required frozen inputs.  It returned `PASS`
with:

- Stage 1/export hash:
  `255910dea5f46f5689df568abe570ad3634b9ff248fd82421607474b6351dd78`
- Stage 3 manifest hash:
  `682c966e6c8e264d9efd83ca7ac16233426daeeb02cca342688362689b2f5081`
- generated tree hash:
  `cc49a04d09f4d1a0839610c0ff39ce5905de720e4d4a72bf8b9a9805846131c1`
- obligation count: 2
- generated trust declarations: 48
- generated `sorry` count: 0

The first preflight attempt exposed a container PID/proc mismatch that stopped
Lean before it read a project.  I retained that output.  A narrowly scoped
`readlink` shim redirects only a missing `/proc/<pid>/exe` lookup to
`/proc/self/exe`; with it, the pinned binaries reported Lean 4.22.0 commit
`ba2cbbf…` and Lake 5.0.0, and preflight completed.  The workaround and both
outputs are preserved in `evidence/lean_environment_workaround.*` and
`evidence/02_stage4_preflight*`.

The independently reconstructed domain-ID sequence, generated
`source_rules` sequence, and obligation sequence are exactly:

1. `rule-75f08df4443da8a48ee02cff10c65980b5cd03f6f6f15985f63ba60ad2f96854`
2. `rule-cd6fef5d8c48828cab2f7185fc582c06349b39cd6c4a267fac6bc46b6ba7413b`

They are unique and in the same order.  Each obligation's span, normalized
hash, inventory hash, discovery hash, and Lean-conjunct hash matches its
source record.  The obligation-map hash
`4a89a96228a7746b638e66a67dc54514ad6f6cddfab7184177a275e716f1ac92`
matches the generator manifest.

The generated theorem is exactly the conjunction of:

1. deleting an explicit `X |-> value` from its disjoint union with a map not
   containing `X` restores that map; and
2. updating a map at a fresh key equals adjoining the explicit fresh binding.

These are the two relevant K Map facts and neither conjunct is duplicated,
irrelevant, a literal truth, or an omitted domain obligation.  Their
freshness hypotheses are semantically necessary.  The fixed target is:

`Klean94Skjkasdkd.Lemmas.targetStatement _Map_ «_in_keys(_)_MAP_Bool_KItem_Map» «_[_<-undef]» «_|->_» «Map:update» notBool_`

Its statement hash is
`8e9438767b4800bdfcfe71d48f7d611f28c29de94cd98aba26163a0654ee31ba`
and its definition hash is
`fba30fd8cff118c661e58e70c75c586ebf75cfa5cf277d74a9653dbe8079704c`.
The actual generated target, expected target reconstructed from the
obligation map, generator manifest, Stage 4 preflight record, audit input, and
fresh `Base` copy all agree exactly.

## Stage 5 build, target identity, and trust

I created `/tmp/audit-work/94-skjkasdkd-stage6-proof`, copied the candidate
there, and copied the immutable generated project into its `Base`.  Both
`lake clean` and `lake build` exited 0.  The complete outputs are in
`evidence/04_lake_clean.result.txt` and
`evidence/05_lake_build.result.txt`.  The `Base` tree remained exactly
`cc49a0…c1` after the build.

Outside `Base`, the candidate contains no `sorry`, `admit`, `unsafe`, new
`axiom`, or new `opaque`.  It does not declare or shadow `targetStatement`.
Each of the six target parameters is defined exactly once.  The trusted proof
mechanical gate independently returned `PASS`; see
`evidence/12_trusted_proof_mechanical_gate.result.json`.

`#check` confirms `Proof.final` has the exact generated target type, rather
than a copy or weakened theorem.  Exact `#print axioms Proof.final` output was:

`'Proof.final' depends on axioms: [propext, Classical.choice, Quot.sound]`

There is no `sorryAx`.  The 48 generated declarations in
`trust-inventory.json` are accounted for, and none is a dependency of
`Proof.final`.  The three reported names are the pinned Lean core baseline
explicitly admitted by the trusted mechanical gate: propositional
extensionality, classical choice (used for key equality), and quotient
soundness.  The candidate adds no unrecorded axiom or opaque declaration.
Raw output and reconciliation are in `evidence/07_print_axioms*` and
`evidence/11_axiom_accounting.result.json`.

## Operational-bridge audit

The source program scans its input, computes the largest prime, and returns
that prime's decimal digit sum.  The generated parameters do not implement
that algorithm; they bind the K Map operations used by the two domain
obligations.  I compared every parameter with its recorded KORE symbol,
source-rule IDs, frozen rules, and the supplied K hooks:

| Parameter | Candidate meaning | Independent judgment |
|---|---|---|
| `_Map_` | raw list append | **Failure**: order-sensitive and total, unlike K `MAP.concat`, which is associative/commutative and fails on overlapping keys. |
| `«_in_keys(_)_MAP_Bool_KItem_Map»` | `List.any` using mathematical key equality | Extensionally aligned only when a list is already a valid unique-key Map representation. |
| `«_[_<-undef]»` | filter out the key | Extensionally aligned on valid unique-key lists. |
| `«_|->_»` | singleton key/value list | Aligned as a singleton element representation. |
| `«Map:update»` | filter old key and prepend new pair | Extensionally aligned on valid unique-key lists, but embedded in the noncanonical, order-sensitive representation. |
| `notBool_` | Lean Boolean negation | Aligned with K `BOOL.not`. |

The supplied K definition states that Maps are generalized associative arrays
with no duplicate keys; `_Map_` is declared with `assoc`, `comm`, and
`unit(.Map)`, and overlapping concatenation produces failure.  The candidate
instead defines `SortMap` as an unrestricted raw list and `_Map_` as
`left.coll ++ right.coll`.

This mismatch is executable, not stylistic:

- The compiled K witness compares two disjoint singleton maps after swapping
  their order and evaluates to `true`
  (`evidence/09_k_map_witness.second-rerun.result.txt`).
- The compiled Lean theorem
  `candidate_Map_is_not_commutative` proves that the same swapped singleton
  inputs produce unequal values under `Proof._Map_`
  (`evidence/AuditBridge.lean` and
  `evidence/08_bridge_adversarial.result.txt`).

Thus the candidate does not implement the frozen operational meaning even on
disjoint, valid singleton maps.  It also returns an ordinary `SortMap` for
overlapping keys, where K concatenation is undefined/failing.

As a counterfactual sensitivity test, I replaced the six interpretations with
a right-projection `badMap`, constant-false membership, identity deletion and
update, and an empty singleton constructor.  Lean still proves the exact
generated target.  The compiled test is
`evidence/AuditDegenerate.lean`.  This does not invalidate the two source
obligations; it shows that the parametric theorem alone cannot establish its
own operational bridge.  The Stage 5 semantic audit is essential, and the
actual candidate's convenient list-append interpretation fails it.

Because the instructions require any constant, identity, hard-coded,
vacuous, or otherwise convenient non-operational interpretation to be an
operational-bridge failure, the clean build and clean axiom list cannot rescue
this proof.

## Evidence index

All commands and complete results are under `/audit-output/evidence/`.
Notable files are:

- `00_producer_provenance.*`: producer hashes, image, and bundle binding.
- `01_reconstruct_inventory.*`: complete canonical 45-rule inventory.
- `02_stage4_preflight*`: failed environment-only attempt and successful
  deterministic preflight.
- `06_hash_bijection_target.*`: all mounted hashes, obligation bijection, and
  target identity.
- `10_independent_classification.*`: all 45 independent classifications.
- `04_lake_clean.*`, `05_lake_build.*`, and
  `12_trusted_proof_mechanical_gate.*`: clean proof build and mechanical gate.
- `07_print_axioms*` and `11_axiom_accounting.*`: exact axiom output and
  accounting.
- `08_bridge_adversarial.*`, `09_k_map_witness*`,
  `AuditBridge.lean`, and `AuditDegenerate.lean`: operational counterexamples
  and counterfactual mutation.
- `13_source_semantics_excerpt.*` and
  `14_parameter_bridge_judgment.*`: frozen source excerpts and per-parameter
  bridge judgment.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
