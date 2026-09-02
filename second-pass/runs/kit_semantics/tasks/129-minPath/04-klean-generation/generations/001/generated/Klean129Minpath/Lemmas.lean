import Klean129Minpath.Inj

/- K trust-boundary goals. The second-pass agent must replace every
   writable opaque stub with an honest definition and prove this
   immutable proposition in the separate Proof.lean workspace. -/

namespace Klean129Minpath.Lemmas

def targetStatement
    (_andBool_ : SortBool → SortBool → SortBool)
    («_>=Int_» : SortInt → SortInt → SortBool)
    («_<Int_» : SortInt → SortInt → SortBool)
    («_==Int_» : SortInt → SortInt → SortBool)
    («_+Int_» : SortInt → SortInt → SortInt)
    («_*Int_» : SortInt → SortInt → SortInt)
    (gridAt : SortIntSeq → SortInt → SortInt → SortInt → SortInt)
    (gridRow : SortIntSeq → SortInt → SortInt → SortValSeq)
    (gridRows : SortIntSeq → SortInt → SortValSeq)
    (oddDone : SortValSeq → SortValSeq → SortInt → SortInt → SortBool)
    (oneCol : SortIntSeq → SortInt → SortInt)
    (oneRow : SortIntSeq → SortInt → SortInt)
    (pairDone : SortValSeq → SortValSeq → SortInt → SortInt → SortBool)
    (snocVS : SortValSeq → SortVal → SortValSeq)
    («valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int» : SortValSeq → SortInt → SortVal)
    («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» : SortValSeq → SortValSeq → SortValSeq)
    (validPerm : SortIntSeq → SortInt → SortBool)
    («vsLen(_)_MPY-CORE_Int_ValSeq» : SortValSeq → SortInt)
    : Prop :=
    (∀ (N : SortInt) (P : SortIntSeq) (h : (_andBool_ («_>=Int_» N 2) (validPerm P («_*Int_» N N))) = true), («vsLen(_)_MPY-CORE_Int_ValSeq» (gridRows P N) : SortInt) = (N : SortInt))
    ∧ (∀ (I : SortInt) (N : SortInt) (P : SortIntSeq) (h : (_andBool_ (_andBool_ (_andBool_ («_>=Int_» N 2) (validPerm P («_*Int_» N N))) («_>=Int_» I 0)) («_<Int_» I N)) = true), («valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int» (gridRows P N) I : SortVal) = ((@inj SortIterable SortVal) (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» (gridRow P N I)) : SortVal))
    ∧ (∀ (J : SortInt) (I : SortInt) (N : SortInt) (P : SortIntSeq) (h : (_andBool_ (_andBool_ (_andBool_ (_andBool_ (_andBool_ («_>=Int_» N 2) (validPerm P («_*Int_» N N))) («_>=Int_» I 0)) («_<Int_» I N)) («_>=Int_» J 0)) («_<Int_» J N)) = true), («valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int» (gridRow P N I) J : SortVal) = (SortVal.inj_SortInt (gridAt P N I J) : SortVal))
    ∧ (∀ (J : SortInt) (I : SortInt) (N : SortInt) (P : SortIntSeq) (h : (_andBool_ (_andBool_ (_andBool_ (_andBool_ (_andBool_ («_>=Int_» N 2) (validPerm P («_*Int_» N N))) («_>=Int_» I 0)) («_<Int_» I N)) («_>=Int_» J 0)) («_<Int_» J N)) = true), («_==Int_» (gridAt P N I J) 1 : SortBool) = (_andBool_ («_==Int_» I (oneRow P N)) («_==Int_» J (oneCol P N)) : SortBool))
    ∧ (∀ (N : SortInt) (J : SortInt) (I : SortInt) (P : SortIntSeq) (h : (_andBool_ (_andBool_ (_andBool_ (_andBool_ (_andBool_ («_>=Int_» N 2) (validPerm P («_*Int_» N N))) («_>=Int_» I 0)) («_<Int_» I N)) («_>=Int_» J 0)) («_<Int_» J N)) = true), («_<Int_» (gridAt P N I J) («_+Int_» («_*Int_» N N) 1) : SortBool) = (true : SortBool))
    ∧ (∀ (V : SortVal) (A : SortValSeq), («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» A (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V SortValSeq.«.ValSeq_MPY-CORE_ValSeq») : SortValSeq) = (snocVS A V : SortValSeq))
    ∧ (∀ (M : SortInt) (R : SortInt) (P : SortValSeq) (A : SortValSeq) (h : («_>=Int_» R 0) = true), (oddDone A (snocVS P (SortVal.inj_SortInt 1)) R M : SortBool) = (pairDone A P R M : SortBool))

end Klean129Minpath.Lemmas
