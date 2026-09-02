# Target-parameter operational bridge judgment

| Target parameter | Frozen binding and rules | Candidate definition | Judgment |
|---|---|---|---|
| `«_<=Int_»` | KORE `Lbl'Unds-LT-Eqls'Int'Unds'`; guard of rule `684bef...` | `decide (left ≤ right)` | Faithful Boolean interpretation of K integer `<=`. |
| `«sortThirdResult(_)_VERIFICATION_ValSeq_ValSeq»` | KORE `LblsortThirdResult...`; definition is `mergeThirdFrom(VS, sortVS(buildVS(VS,0,vsLen(VS),3)),0,vsLen(VS))`; rule `684bef...` | Extracts every third item, sorts only pairs of `inj_SortInt`, preserves every non-integer insertion order, then weaves | **Failure.** It does not implement the supplied `sortVS`/source `sorted` meaning over the stated value domain. The Boolean witness in `13b-lean-operational-adversary.log` reduces to the unchanged unsorted result, while `14b-source-oracle-adversary.log` returns the sorted result. The frozen K string witness in `16-krun-operational-string.log` also sorts normally. |
| `«valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»` | KORE `LblvalSeqConcat...`; rules `a1197a...` and `d101e7...`; frozen `list.k` lines 18-20 | Structural recursion on the left sequence with empty and `vCons` cases | Faithful to both frozen equations. |
| `«vsLen(_)_MPY-CORE_Int_ValSeq»` | KORE `LblvsLen...`; guard of rule `684bef...`; frozen `core.k` lines 223-225 | Structural `Nat` length converted with `Int.ofNat` | Faithful to the frozen zero/successor equations. |

The operational failure is independently sensitivity-tested:
`18d-mutation-diff.log` replaces `sortThirdResult` by the constant empty
sequence, and the fresh `lake clean`/`lake build` in
`18e-mutation-clean.log` and `18f-mutation-build.log` still succeeds. Thus
`Proof.final` checks only the empty guarded case and cannot validate the
candidate's nonempty operational meaning.

There is also a Stage 4 domain bridge failure. Frozen `core.k` declares
`Str ::= str(IntSeq)` and includes `Str` in `Iterable`; frozen `sort.k` has
concrete lexicographic string-sort equations. Generated `SortIterable` has no
`Str`/string constructor, as recorded in `17-lean-domain-bridge.log`.
Consequently the universal Lean obligations range over a strict subset of the
frozen K `ValSeq` values.
