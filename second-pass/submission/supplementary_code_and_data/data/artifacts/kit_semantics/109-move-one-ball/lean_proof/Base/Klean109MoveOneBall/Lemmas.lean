import Klean109MoveOneBall.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean109MoveOneBall.Lemmas

def targetStatement
    (_andBool_ : SortBool → SortBool → SortBool)
    («_<Int_» : SortInt → SortInt → SortBool)
    («allInts(_)_VERIFICATION_Bool_ValSeq» : SortValSeq → SortBool)
    («applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» : SortString → SortVal → SortVal → SortBool)
    (isInt : SortK → SortBool)
    («lastAfter(_,_)_VERIFICATION_Val_Val_ValSeq» : SortVal → SortValSeq → SortVal)
    («project:Int» : SortK → SortInt)
    : Prop :=
    (∀ (B : SortVal) (A : SortVal) (h : (_andBool_ (isInt (SortK.kseq ((@inj SortVal SortKItem) A) SortK.dotk)) (isInt (SortK.kseq ((@inj SortVal SortKItem) B) SortK.dotk))) = true), («applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» "<" A B : SortBool) = («_<Int_» («project:Int» (SortK.kseq ((@inj SortVal SortKItem) A) SortK.dotk)) («project:Int» (SortK.kseq ((@inj SortVal SortKItem) B) SortK.dotk)) : SortBool))
    ∧ (∀ (VS : SortValSeq) (P : SortVal) (A : SortVal) (h : (_andBool_ (_andBool_ (isInt (SortK.kseq ((@inj SortVal SortKItem) A) SortK.dotk)) (isInt (SortK.kseq ((@inj SortVal SortKItem) P) SortK.dotk))) («allInts(_)_VERIFICATION_Bool_ValSeq» VS)) = true), («applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» "<" A («lastAfter(_,_)_VERIFICATION_Val_Val_ValSeq» P VS) : SortBool) = («_<Int_» («project:Int» (SortK.kseq ((@inj SortVal SortKItem) A) SortK.dotk)) («project:Int» (SortK.kseq ((@inj SortVal SortKItem) («lastAfter(_,_)_VERIFICATION_Val_Val_ValSeq» P VS)) SortK.dotk)) : SortBool))

end Klean109MoveOneBall.Lemmas
