import Klean123GetOddCollatz.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean123GetOddCollatz.Lemmas

def targetStatement
    (_andBool_ : SortBool → SortBool → SortBool)
    («_==Int_» : SortInt → SortInt → SortBool)
    («_==K_» : SortK → SortK → SortBool)
    («collatzNext(_)_VERIFICATION-SYNTAX_Int_Int» : SortInt → SortInt)
    («maybeOdd(_)_VERIFICATION-SYNTAX_ValSeq_Int» : SortInt → SortValSeq)
    (notBool_ : SortBool → SortBool)
    («oddWithoutLast(_)_VERIFICATION-SYNTAX_ValSeq_ValSeq» : SortValSeq → SortValSeq)
    («traceFirstInt(_)_VERIFICATION-SYNTAX_Int_ValSeq» : SortValSeq → SortInt)
    («traceLastInt(_)_VERIFICATION-SYNTAX_Int_ValSeq» : SortValSeq → SortInt)
    («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» : SortValSeq → SortValSeq → SortValSeq)
    («validCollatzTrace(_)_VERIFICATION-SYNTAX_Bool_ValSeq» : SortValSeq → SortBool)
    : Prop :=
    (∀ (A : SortValSeq), («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» A SortValSeq.«.ValSeq_MPY-CORE_ValSeq» : SortValSeq) = (A : SortValSeq))
    ∧ (∀ (C : SortValSeq) (B : SortValSeq) (A : SortValSeq), («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» A B) C : SortValSeq) = («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» A («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» B C) : SortValSeq))
    ∧ (∀ (_Gen2 : SortValSeq) (_Gen1 : SortVal) (_Gen0 : SortValSeq), («_==K_» (SortK.kseq (SortKItem.inj_SortValSeq («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» _Gen0 (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _Gen1 _Gen2))) SortK.dotk) (SortK.kseq (SortKItem.inj_SortValSeq SortValSeq.«.ValSeq_MPY-CORE_ValSeq») SortK.dotk) : SortBool) = (false : SortBool))
    ∧ (∀ (_Gen2 : SortValSeq) (_Gen1 : SortVal) (_Gen0 : SortValSeq), («_==K_» (SortK.kseq (SortKItem.inj_SortValSeq SortValSeq.«.ValSeq_MPY-CORE_ValSeq») SortK.dotk) (SortK.kseq (SortKItem.inj_SortValSeq («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» _Gen0 (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _Gen1 _Gen2))) SortK.dotk) : SortBool) = (false : SortBool))
    ∧ (∀ (J : SortInt) (T : SortValSeq) (h : (notBool_ («_==K_» (SortK.kseq (SortKItem.inj_SortValSeq T) SortK.dotk) (SortK.kseq (SortKItem.inj_SortValSeq SortValSeq.«.ValSeq_MPY-CORE_ValSeq») SortK.dotk))) = true), («traceFirstInt(_)_VERIFICATION-SYNTAX_Int_ValSeq» («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» T (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortInt J) SortValSeq.«.ValSeq_MPY-CORE_ValSeq»)) : SortInt) = («traceFirstInt(_)_VERIFICATION-SYNTAX_Int_ValSeq» T : SortInt))
    ∧ (∀ (J : SortInt) (_Gen0 : SortValSeq), («traceLastInt(_)_VERIFICATION-SYNTAX_Int_ValSeq» («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» _Gen0 (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortInt J) SortValSeq.«.ValSeq_MPY-CORE_ValSeq»)) : SortInt) = (J : SortInt))
    ∧ (∀ (J : SortInt) (T : SortValSeq) (h : (notBool_ («_==K_» (SortK.kseq (SortKItem.inj_SortValSeq T) SortK.dotk) (SortK.kseq (SortKItem.inj_SortValSeq SortValSeq.«.ValSeq_MPY-CORE_ValSeq») SortK.dotk))) = true), («validCollatzTrace(_)_VERIFICATION-SYNTAX_Bool_ValSeq» («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» T (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortInt J) SortValSeq.«.ValSeq_MPY-CORE_ValSeq»)) : SortBool) = (_andBool_ («validCollatzTrace(_)_VERIFICATION-SYNTAX_Bool_ValSeq» T) («_==Int_» J («collatzNext(_)_VERIFICATION-SYNTAX_Int_Int» («traceLastInt(_)_VERIFICATION-SYNTAX_Int_ValSeq» T))) : SortBool))
    ∧ (∀ (_Gen0 : SortInt) (T : SortValSeq) (h : («validCollatzTrace(_)_VERIFICATION-SYNTAX_Bool_ValSeq» T) = true), («oddWithoutLast(_)_VERIFICATION-SYNTAX_ValSeq_ValSeq» («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» T (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortInt _Gen0) SortValSeq.«.ValSeq_MPY-CORE_ValSeq»)) : SortValSeq) = («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» («oddWithoutLast(_)_VERIFICATION-SYNTAX_ValSeq_ValSeq» T) («maybeOdd(_)_VERIFICATION-SYNTAX_ValSeq_Int» («traceLastInt(_)_VERIFICATION-SYNTAX_Int_ValSeq» T)) : SortValSeq))

end Klean123GetOddCollatz.Lemmas
