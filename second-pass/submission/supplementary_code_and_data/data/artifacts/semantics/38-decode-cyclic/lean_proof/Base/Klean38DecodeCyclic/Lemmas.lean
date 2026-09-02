import Klean38DecodeCyclic.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean38DecodeCyclic.Lemmas

def targetStatement
    («_-Int_» : SortInt → SortInt → SortInt)
    (_Map_ : SortMap → SortMap → SortMap)
    («_in_keys(_)_MAP_Bool_KItem_Map» : SortKItem → SortMap → SortBool)
    («_>=Int_» : SortInt → SortInt → SortBool)
    («_[_<-undef]» : SortMap → SortKItem → SortMap)
    («_|->_» : SortKItem → SortKItem → SortMap)
    («_+Int_» : SortInt → SortInt → SortInt)
    («Map:update» : SortMap → SortKItem → SortKItem → SortMap)
    («buildIS(_,_,_,_)_MPY-SUBSCRIPT_IntSeq_IntSeq_Int_Int_Int» : SortIntSeq → SortInt → SortInt → SortInt → SortIntSeq)
    («clampHi(_,_,_)_MPY-SUBSCRIPT_Int_Int_Int_Int» : SortInt → SortInt → SortInt → SortInt)
    («isLen(_)_MPY-CORE_Int_IntSeq» : SortIntSeq → SortInt)
    («keysBelow(_,_)_VERIFICATION_Bool_Map_Int» : SortMap → SortInt → SortBool)
    : Prop :=
    (∀ (CS : SortIntSeq) (h : «_>=Int_» («isLen(_)_MPY-CORE_Int_IntSeq» CS) 3 = true), («isLen(_)_MPY-CORE_Int_IntSeq» («buildIS(_,_,_,_)_MPY-SUBSCRIPT_IntSeq_IntSeq_Int_Int_Int» CS («clampHi(_,_,_)_MPY-SUBSCRIPT_Int_Int_Int_Int» 3 («isLen(_)_MPY-CORE_Int_IntSeq» CS) 1) («isLen(_)_MPY-CORE_Int_IntSeq» CS) 1) : SortInt) = («_-Int_» («isLen(_)_MPY-CORE_Int_IntSeq» CS) 3 : SortInt))
    ∧ (∀ (CS : SortIntSeq) (h : «_>=Int_» («isLen(_)_MPY-CORE_Int_IntSeq» CS) 3 = true), («clampHi(_,_,_)_MPY-SUBSCRIPT_Int_Int_Int_Int» 3 («isLen(_)_MPY-CORE_Int_IntSeq» CS) 1 : SortInt) = (3 : SortInt))
    ∧ (∀ (N : SortInt) (M : SortMap) (h : «keysBelow(_,_)_VERIFICATION_Bool_Map_Int» M N = true), («keysBelow(_,_)_VERIFICATION_Bool_Map_Int» M («_+Int_» N 1) : SortBool) = (true : SortBool))
    ∧ (∀ (M : SortMap) (N : SortInt) (h : «keysBelow(_,_)_VERIFICATION_Bool_Map_Int» M N = true), («_in_keys(_)_MAP_Bool_KItem_Map» (SortKItem.inj_SortInt N) M : SortBool) = (false : SortBool))
    ∧ (∀ (S : SortScope) (N : SortInt) (M : SortMap) (h : «keysBelow(_,_)_VERIFICATION_Bool_Map_Int» M N = true), («Map:update» M (SortKItem.inj_SortInt N) (SortKItem.inj_SortScope S) : SortMap) = (_Map_ («_|->_» (SortKItem.inj_SortInt N) (SortKItem.inj_SortScope S)) M : SortMap))
    ∧ (∀ (N : SortInt) (M : SortMap) (_S : SortScope) (h : «keysBelow(_,_)_VERIFICATION_Bool_Map_Int» M N = true), («_[_<-undef]» (_Map_ («_|->_» (SortKItem.inj_SortInt N) (SortKItem.inj_SortScope _S)) M) (SortKItem.inj_SortInt N) : SortMap) = (M : SortMap))

end Klean38DecodeCyclic.Lemmas
