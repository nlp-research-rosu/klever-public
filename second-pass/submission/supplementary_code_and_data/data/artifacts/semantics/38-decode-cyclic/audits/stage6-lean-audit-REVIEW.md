# Independent audit: `38-decode-cyclic`, `semantics`, `SUPPLIED_SEMANTICS`

## Executive judgment

This audit rejects the result. Stage 3 is correctly classified and Stage 4 is
structurally reproducible, but Stage 4 gives the supplied K sort `Scope` an
empty Lean carrier. Consequently, two of the six domain-lemma obligations are
vacuous. The Stage 5 candidate proves both by eliminating the impossible
`SortScope` argument with `nomatch`, rather than proving map update and
deletion for the concrete scopes used by the frozen program.

This is a fixed-target semantic-generation and operational-bridge failure.
The clean build, exact target hashes, and clean axiom list are necessary
integrity checks, but they cannot make vacuous obligations faithful to the
frozen operational semantics.

The launcher-recorded audit mode is `CLASSIFICATION_AND_PROOF`, consistent
with `AUDIT_MODE`, so all five requested stages were audited.

## Producer provenance

Before judging Stage 4, I hashed the two mounted generation-time producers:

| Producer | Mounted SHA-256 |
|---|---|
| `klean_export.py` | `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0` |
| `klean.py` | `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1` |

Both hashes match `generator-manifest.json`, the producer
`source-manifest.json`, and `/audit-input.json`. All three bind the producer
to immutable generator image
`sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000`.
The required pipeline-contract tree hash is
`55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c`,
also an exact audit-input match. There is therefore no producer-provenance
`AUDIT_ERROR`.

Raw provenance is in
[`01-producer-provenance.log`](/audit-output/evidence/01-producer-provenance.log)
and
[`02-producer-bundle-contract-hash.log`](/audit-output/evidence/02-producer-bundle-contract-hash.log).

## Stage 3 inventory reconstruction and classification

I reconstructed the complete local verification-module closure of frozen
`verification.k` with the trusted `tools.k_rule_inventory` implementation.
The closure contains the single local module `VERIFICATION` and exactly
twelve rules. The frozen file hash is
`718cd222892dcfd5ca6073d833a1ad08a329489e1c61cbc77a8f2db31918d658`;
the canonical inventory hash is
`2d1bb15a83a481f9a192bb6a344c4c0e039ecb5585e165a2e171d459401cfc47`.

Independent classifications are:

| Frozen lines | Rule ID prefix | Attributes | Judgment | Reason |
|---:|---|---|---|---|
| 8–24 | `d56a068e4235` | none | `DEFINITION` | Defines the named translated `decodeBody` proof term. |
| 27 | `3f60be28f9a7` | none | `DEFINITION` | Defines the named `decodeClosure`. |
| 35–36 | `b1b7e1ad3003` | none | `DEFINITION` | Base equation of the `decodeCodes` summary. |
| 37–43 | `0ed947467c58` | none | `DEFINITION` | Recursive equation of the `decodeCodes` summary. |
| 47–53 | `4281e752ff9a` | `simplification` | `DOMAIN_LEMMA` | Imported slice-length fact, inserted before proof rather than first proved without itself. |
| 55–57 | `e4afafd317ff` | `simplification` | `DOMAIN_LEMMA` | Imported `clampHi` fact under the length guard. |
| 62 | `dd1b844f1c32` | none | `DEFINITION` | Base equation defining `keysBelow`. |
| 63–64 | `d293ed9920d4` | none | `DEFINITION` | Recursive equation defining `keysBelow`. |
| 66–68 | `12b6390dc702` | `simplification` | `DOMAIN_LEMMA` | Monotonicity of `keysBelow`. |
| 70–72 | `75fa33282a96` | `simplification` | `DOMAIN_LEMMA` | A bound key is absent from the map. |
| 74–76 | `f0db16212bf5` | `simplification` | `DOMAIN_LEMMA` | Fresh-scope map update normalization. |
| 78–80 | `d7d11f1fc9fe` | `simplification` | `DOMAIN_LEMMA` | Deletion of the maximal allocated scope. |

There are six definitions and six domain lemmas, with no local operational
rules and no proved-derived lemmas. Stage 1 compiles all six simplification
rules into its verification definition before the one `kprove` invocation;
it does not first prove any exact rule against a module that omits it.
Therefore none qualifies as `PROVED_DERIVED_LEMMA`.

The six domain lemmas are relevant. The first two support the recursive
three-code slicing used by `decode_cyclic`. The last four maintain the scope
store's fresh-location invariant during call-frame allocation and deletion,
which is explicit in the supplied semantics and the reachability
precondition. Every `simplification` rule is classified as a domain lemma.

The reconstructed identities, order, source spans, normalized hashes, and
inventory hash match `/reference/lemma-discovery.json` bijectively. There are
no omissions, duplicates, extras, reordered identities, or unaccounted
classifications. The complete source and comparison are in
[`03-reconstructed-rule-inventory.log`](/audit-output/evidence/03-reconstructed-rule-inventory.log)
and
[`04-stage3-bijection-validation.log`](/audit-output/evidence/04-stage3-bijection-validation.log).

## Stage 4 structural integrity

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`
on the three specified inputs. The first invocation encountered an audit
container `/proc` PID-namespace incompatibility in Lean, recorded in
[`05-stage4-check-generation.log`](/audit-output/evidence/05-stage4-check-generation.log)
and diagnosed in
[`06-lean-proc-namespace-diagnostic.log`](/audit-output/evidence/06-lean-proc-namespace-diagnostic.log).
A minimal readlink compatibility shim, limited to resolving Lean's own
`/proc/<pid>/exe` lookup through `/proc/self/exe`, allowed the identical
trusted check to run. It returned `PASS`, generated tree hash
`130e2e74d464087a8fd6e6843d6cf251eefabb7e12367669bc58804401ffbee8`,
and six obligations. The complete successful return value is
[`07-stage4-check-generation-rerun.log`](/audit-output/evidence/07-stage4-check-generation-rerun.log).

I separately checked every audit-input/source/generation/candidate tree and
file hash. I also checked that:

- the six independently identified domain-rule IDs occur exactly once and in
  source order in the obligation map;
- every obligation retains the exact source span, normalized source hash,
  inventory hash, discovery hash, and Lean-conjunct hash;
- there are no omitted, duplicate, or extra obligations;
- the generated target is exactly the six recorded conjuncts;
- the selected generated tree and target are unchanged after the Stage 5
  build.

All mechanical checks are true in
[`09-hashes-bijections-target-corrected.log`](/audit-output/evidence/09-hashes-bijections-target-corrected.log).
The fixed declaration is
`Klean38DecodeCyclic.Lemmas.targetStatement`, with definition hash
`c1a743472c014d67b548bc65702a6cb1ac7f92480d47d23e525f13da1668e7a0`
and applied-statement hash
`30ed5d255be9b99e8d03a7b8d8539bbd409425b7d933472e7c00a775ef7f8cec`.
This case is not `KLEAN_NO_OBLIGATIONS`; its true Stage 3 domain set has six
entries.

## Fatal Stage 4 semantic defect

Structural integrity does not establish faithful meaning. Frozen supplied
semantics declares:

```k
syntax Scope ::= scope(Map, Parent)
```

and operational rules construct concrete values such as
`scope(.Map, parent(DEFL))`; the initial and specification configurations also
contain populated `scope(...)` values. The sort is therefore inhabited and
operationally central.

The generated Lean project instead contains:

```lean
inductive SortScope : Type
```

with no constructors. Yet target conjuncts five and six universally quantify
over `S : SortScope` to express fresh-scope map update and deletion. Those
quantifiers range over no values. The candidate exposes the defect directly:

```lean
· intro S
  exact nomatch S
· intro N M S
  exact nomatch S
```

I independently proved in Lean, without axioms, that `SortScope` is empty and
that both generated obligations hold for arbitrary map operations solely by
eliminating `S`. See
[`22-generated-scope-vacuity-lean.log`](/audit-output/evidence/22-generated-scope-vacuity-lean.log).
This is a vacuous-conjunct failure in the fixed generated target, not a mere
proof-style concern.

Two counterfactuals confirm causality:

1. Replacing `_Map_`, singleton, update, and deletion with constant empty-map
   functions still clean-builds the proof. The exact mutation and successful
   result are
   [`20-vacuity-counterfactual-diff.log`](/audit-output/evidence/20-vacuity-counterfactual-diff.log)
   and
   [`21-vacuity-counterfactual-build.log`](/audit-output/evidence/21-vacuity-counterfactual-build.log).
2. Adding one constructor `SortScope.auditWitness` without changing the
   target makes both `nomatch` branches fail with “Missing cases:
   `SortScope.auditWitness`.” See
   [`30-nonempty-scope-counterfactual-build.log`](/audit-output/evidence/30-nonempty-scope-counterfactual-build.log).

Thus the last two generated conjuncts do not encode the corresponding frozen
K rules on any operational `scope(Map, Parent)` value.

## Stage 5 build, identity, and trust

I copied `/candidate` into the fresh project
`/tmp/audit-work/proof-audit-002`, copied the selected generated project into
its `Base`, and ran both `lake clean` and `lake build`. Both exited zero; full
outputs are
[`13-stage5-lake-clean.log`](/audit-output/evidence/13-stage5-lake-clean.log)
and
[`14-stage5-lake-build.log`](/audit-output/evidence/14-stage5-lake-build.log).

The generated `Base` tree remained byte-identical to the selected Stage 4
tree, and its target declaration, definition, statement, and hashes remained
exact matches for both manifests and `/audit-input.json`; see
[`23-postbuild-target-identity.log`](/audit-output/evidence/23-postbuild-target-identity.log).
The candidate references the generated target and does not redeclare or
shadow it. A lexical scan found no `sorry`, `admit`, `unsafe`, new `axiom`, or
new `opaque`; see
[`12-candidate-forbidden-shadow-scan.log`](/audit-output/evidence/12-candidate-forbidden-shadow-scan.log).

Lean reports the exact type of `Proof.final` as the fixed target applied to
the twelve candidate definitions:
[`24-proof-final-identity.log`](/audit-output/evidence/24-proof-final-identity.log).
Its exact axiom output is:

```text
'Proof.final' depends on axioms: [propext, Classical.choice, Quot.sound]
```

These are the expected Lean core logical axioms. There is no `sorryAx`, no
dependency on any of the 53 generated trust-allowlist declarations, and no
unrecorded dependency. The exact output and reconciliation are
[`19-print-axioms-proof-final-exact.log`](/audit-output/evidence/19-print-axioms-proof-final-exact.log)
and
[`25-axiom-reconciliation.log`](/audit-output/evidence/25-axiom-reconciliation.log).

## Operational-bridge audit of every target parameter

Each target parameter has exactly one candidate `def`; every KORE symbol,
binding hash, and associated source-rule ID matches the generator manifest.
Exact definitions and locations are recorded in
[`27-parameter-definition-locations.log`](/audit-output/evidence/27-parameter-definition-locations.log).

| Parameter | Candidate meaning and independent judgment |
|---|---|
| `_-Int_` | Lean integer subtraction; faithful to K `-Int`. |
| `_Map_` | Concatenates list-backed entries; models disjoint K map union on the guarded canonical inputs, but its Scope-bearing use is never exercised because `SortScope` is empty. |
| `_in_keys(_)_MAP_Bool_KItem_Map` | Extensional key membership using decidable `SortKItem` equality; faithful on represented maps. |
| `_>=Int_` | Lean integer greater-than-or-equal; faithful. |
| `_[_<-undef]` | Removes all entries with the selected key; faithful to deletion on canonical K maps, but the target's Scope deletion case is vacuous. |
| `_|->_` | Constructs a one-entry list-backed map; locally faithful, but no operational Scope value can be its target value. |
| `_+Int_` | Lean integer addition; faithful. |
| `Map:update` | Removes the old key and prepends the new pair; faithful to overwrite on canonical K maps, but the target's Scope update case is vacuous. |
| `buildIS(_,_,_,_)` | Builds the strided subsequence, with a direct unit-step case. Concrete `+1`, positive-stride, negative-stride, and boundary tests agree with the frozen recurrence on its in-range operational inputs. |
| `clampHi(_,_,_)` | Implements the frozen positive/negative-step upper-bound clamp; the target specialization is faithful. |
| `isLen(_)` | Recursively converts the generated sequence and returns its constructor length; faithful. |
| `keysBelow(_,_)` | Checks that every represented map key is an integer below the bound. This realizes the invariant on intended integer-to-Scope maps, but Stage 4 provides no Scope values and therefore no such nonempty operational map. |

Concrete bridge examples are in
[`29-operational-bridge-examples-corrected.log`](/audit-output/evidence/29-operational-bridge-examples-corrected.log).
The scalar and sequence definitions are substantive, and the list-backed map
definitions are plausible locally. Nevertheless, a collection of locally
plausible operations cannot bridge an omitted source datatype. The decisive
counterfactual shows that the theorem places no semantic constraint at all on
the Scope update/deletion behavior.

## Conclusion

Stage 3 passes independent classification and bijection review. Stage 4
passes producer provenance and deterministic structural checks, and Stage 5
passes clean-build, target-identity, lexical trust, and axiom-accounting
checks. The overall result nevertheless fails because the generated target
replaces an inhabited operational K sort with an empty Lean sort, making two
required domain lemmas vacuous. `Proof.final` therefore does not prove the
fresh-scope update and deletion facts for the frozen supplied semantics.

The raw command ledger is
[`COMMANDS.md`](/audit-output/evidence/COMMANDS.md).

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
