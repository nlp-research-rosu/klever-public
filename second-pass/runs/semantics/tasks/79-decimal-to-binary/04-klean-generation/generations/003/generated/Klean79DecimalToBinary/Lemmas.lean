import Klean79DecimalToBinary.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean79DecimalToBinary.Lemmas

def targetStatement
    («doSlice(_,_,_,_)_MPY-SUBSCRIPT_Val_Val_OptInt_OptInt_OptInt» : SortVal → SortOptInt → SortOptInt → SortOptInt → SortVal)
    : Prop :=
    (∀ (REST : SortIntSeq) (_SECOND : SortInt) (_FIRST : SortInt), («doSlice(_,_,_,_)_MPY-SUBSCRIPT_Val_Val_OptInt_OptInt_OptInt» (SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _FIRST (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _SECOND REST)))) (SortOptInt.«someB(_)_MPY-SUBSCRIPT_OptInt_Int» 2) SortOptInt.«noB_MPY-SUBSCRIPT_OptInt» SortOptInt.«noB_MPY-SUBSCRIPT_OptInt» : SortVal) = (SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» REST) : SortVal))

end Klean79DecimalToBinary.Lemmas
