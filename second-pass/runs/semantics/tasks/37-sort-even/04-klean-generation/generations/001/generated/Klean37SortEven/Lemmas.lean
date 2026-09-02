import Klean37SortEven.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean37SortEven.Lemmas

def targetStatement
    (_Map_ : SortMap → SortMap → SortMap)
    («_in_keys(_)_MAP_Bool_KItem_Map» : SortKItem → SortMap → SortBool)
    («_|->_» : SortKItem → SortKItem → SortMap)
    («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» : SortValSeq → SortValSeq → SortValSeq)
    : Prop :=
    (∀ (VS : SortValSeq), «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» VS SortValSeq.«.ValSeq_MPY-CORE_ValSeq» = VS)
    ∧ (∀ (A : SortValSeq) (B : SortValSeq) (C : SortValSeq), «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» A B) C = «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» A («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» B C))
    ∧ (∀ (_EV : SortVal) (_OV : SortVal) (_RV : SortVal) (_IV : SortVal) (_ODD : SortVal) (M : SortMap), «_in_keys(_)_MAP_Bool_KItem_Map» (SortKItem.inj_SortString "$cells") (_Map_ (_Map_ (_Map_ (_Map_ (_Map_ («_|->_» (SortKItem.inj_SortString "evens") (SortKItem.inj_SortVal _EV)) («_|->_» (SortKItem.inj_SortString "odds") (SortKItem.inj_SortVal _OV))) («_|->_» (SortKItem.inj_SortString "result") (SortKItem.inj_SortVal _RV))) («_|->_» (SortKItem.inj_SortString "i") (SortKItem.inj_SortVal _IV))) («_|->_» (SortKItem.inj_SortString "odd") (SortKItem.inj_SortVal _ODD))) M) = «_in_keys(_)_MAP_Bool_KItem_Map» (SortKItem.inj_SortString "$cells") M)

end Klean37SortEven.Lemmas
