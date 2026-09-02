import Klean72WillItFly.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean72WillItFly.Lemmas

def targetStatement
    («allInts(_)_VERIFICATION_Bool_ValSeq» : SortValSeq → SortBool)
    («doSlice(_,_,_,_)_MPY-SUBSCRIPT_Val_Val_OptInt_OptInt_OptInt» : SortVal → SortOptInt → SortOptInt → SortOptInt → SortVal)
    («reverseVS(_)_VERIFICATION_ValSeq_ValSeq» : SortValSeq → SortValSeq)
    («sumIntVS(_)_VERIFICATION_Int_ValSeq» : SortValSeq → SortInt)
    : Prop :=
    (∀ (VS : SortValSeq), («doSlice(_,_,_,_)_MPY-SUBSCRIPT_Val_Val_OptInt_OptInt_OptInt» (SortVal.inj_SortIterable (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» VS)) SortOptInt.«noB_MPY-SUBSCRIPT_OptInt» SortOptInt.«noB_MPY-SUBSCRIPT_OptInt» (SortOptInt.«someB(_)_MPY-SUBSCRIPT_OptInt_Int» (-1)) : SortVal) = (SortVal.inj_SortIterable (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» («reverseVS(_)_VERIFICATION_ValSeq_ValSeq» VS)) : SortVal))
    ∧ (∀ (_Gen9 : SortGeneratedCounterCell) (_Gen8 : SortExitCodeCell) (_Gen7 : SortExcCell) (_Gen6 : SortRetCell) (_Gen5 : SortStackCell) (_Gen4 : SortHeapLocCell) (_Gen3 : SortHeapCell) (_Gen2 : SortScopeLocCell) (_Gen1 : SortScopesCell) (_Gen0 : SortEnvCell) (_DotVar1 : SortK) (VS : SortValSeq) (h : «allInts(_)_VERIFICATION_Bool_ValSeq» VS = true), ({ k := { val := SortK.kseq (SortKItem.«#sumAcc(_,_)_MPY-BUILTINS_KItem_Iterable_Int» (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» VS) 0) _DotVar1 }, env := _Gen0, scopes := _Gen1, scopeLoc := _Gen2, heap := _Gen3, heapLoc := _Gen4, stack := _Gen5, ret := _Gen6, exc := _Gen7, exitCode := _Gen8, generatedCounter := _Gen9 } : SortGeneratedTopCell) = ({ k := { val := SortK.kseq (SortKItem.inj_SortInt («sumIntVS(_)_VERIFICATION_Int_ValSeq» VS)) _DotVar1 }, env := _Gen0, scopes := _Gen1, scopeLoc := _Gen2, heap := _Gen3, heapLoc := _Gen4, stack := _Gen5, ret := _Gen6, exc := _Gen7, exitCode := _Gen8, generatedCounter := _Gen9 } : SortGeneratedTopCell))

end Klean72WillItFly.Lemmas
