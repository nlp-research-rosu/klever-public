# Operational-bridge audit

The four target parameters occur exactly once as `def`s in `Proof.lean`.

| KORE binding | Candidate behavior | Independent judgment |
|---|---|---|
| `Lbl'Unds-LT-Eqls'Int'Unds'` | `decide (left ≤ right)` | Exact Boolean form of K `_<=Int_`; negative and false-boundary examples reduce. |
| `LblvsLen'LParUndsRParUnds'MPY-CORE'Unds'Int'Unds'ValSeq` | Structural length, converted from `Nat` to `Int` | Exact match for the two `vsLen` rules. |
| `LblvalSeqConcat'LParUndsCommUndsRParUnds'MPY-LIST'Unds'ValSeq'Unds'ValSeq'Unds'ValSeq` | Structural recursion on the first sequence | Exact match for both supplied `valSeqConcat` equations. |
| `LblsortThirdResult'LParUndsRParUnds'VERIFICATION'Unds'ValSeq'Unds'ValSeq` | Select indices `0,3,6,…`, stable-sort them, and merge them back into precisely those positions | Matches the source solution and the `buildVS`/`sortVS`/`mergeThirdFrom` summary. Its insertion direction agrees with the concrete K integer rule (`X ≤ Y`) and string `strLt` rule. |

Fresh K compilation and execution passed the integer, boundary, negative, and
string cases in `concrete_test.mpy`. Independent Lean reductions passed the
same nontrivial integer and string examples plus primitive boundary checks.
The source implementation also matched an independent slice-assignment oracle
on 895 cases.

The supplied semantics intentionally leaves symbolic `sortVS` opaque and gives
concrete equations for integer and string sequences. The candidate matches
those fixed equations; its additional comparison cases are a deterministic
implementation of the source operation on further comparable represented
values, with a stable totalization where the supplied opaque primitive has no
concrete equation.

As a sensitivity check, `Counterfactual.lean` proves that a constant-empty
replacement also satisfies the generated three-domain-lemma proposition. This
is expected evidence that the Lean theorem alone does not validate the bridge.
The candidate is not that counterfactual: its nonempty HumanEval example and
other adversarial reductions produce the operational result, so the manual
bridge gate passes.
