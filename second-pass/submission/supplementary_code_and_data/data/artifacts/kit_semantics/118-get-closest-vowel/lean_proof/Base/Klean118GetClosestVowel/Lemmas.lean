import Klean118GetClosestVowel.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean118GetClosestVowel.Lemmas

def targetStatement
    (_andBool_ : SortBool → SortBool → SortBool)
    («_>=Int_» : SortInt → SortInt → SortBool)
    («_<Int_» : SortInt → SortInt → SortBool)
    («_<=Int_» : SortInt → SortInt → SortBool)
    («_+Int_» : SortInt → SortInt → SortInt)
    («isLen(_)_MPY-CORE_Int_IntSeq» : SortIntSeq → SortInt)
    («closestScan(_,_,_,_)_FOUNDATION-SYNTAX_IntSeq_IntSeq_Int_IntSeq_Bool?» : SortIntSeq → SortInt → SortIntSeq → SortBool → Option SortIntSeq)
    («intSeqAt(_,_)_MPY-SUBSCRIPT_Int_IntSeq_Int?» : SortIntSeq → SortInt → Option SortInt)
    : Prop :=
    (∀ (I : SortInt) (CS : SortIntSeq) (h : (_andBool_ («_<=Int_» 0 I) («_<Int_» I («isLen(_)_MPY-CORE_Int_IntSeq» CS))) = true), ((«intSeqAt(_,_)_MPY-SUBSCRIPT_Int_IntSeq_Int?» CS I).isSome = true) ↔ (True))
    ∧ (∀ (F : SortBool) (R : SortIntSeq) (I : SortInt) (CS : SortIntSeq) (h : (_andBool_ («_>=Int_» I 0) («_<Int_» («_+Int_» I 1) («isLen(_)_MPY-CORE_Int_IntSeq» CS))) = true), ((«closestScan(_,_,_,_)_FOUNDATION-SYNTAX_IntSeq_IntSeq_Int_IntSeq_Bool?» CS I R F).isSome = true) ↔ (True))

end Klean118GetClosestVowel.Lemmas
