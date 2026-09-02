import Klean113OddCount.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean113OddCount.Lemmas

def targetStatement
    («applyMethod(_,_,_)_MPY-METHODS_Val_Val_String_Vals» : SortVal → SortString → SortVals → SortVal)
    («cntSub(_,_)_MPY-METHODS_Int_IntSeq_IntSeq» : SortIntSeq → SortIntSeq → SortInt)
    («isStringVal(_)_VERIFICATION-SYNTAX_Bool_Val» : SortVal → SortBool)
    (stringCodes : SortVal → SortIntSeq)
    : Prop :=
    (∀ (PATTERN : SortIntSeq) (V : SortVal) (h : («isStringVal(_)_VERIFICATION-SYNTAX_Bool_Val» V) = true), («applyMethod(_,_,_)_MPY-METHODS_Val_Val_String_Vals» V "count" (SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» PATTERN)) SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals») : SortVal) = (SortVal.inj_SortInt («cntSub(_,_)_MPY-METHODS_Int_IntSeq_IntSeq» (stringCodes V) PATTERN) : SortVal))

end Klean113OddCount.Lemmas
